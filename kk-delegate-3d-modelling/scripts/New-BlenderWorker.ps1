param(
    [Parameter(Mandatory=$true)][string]$OutputDirectory,
    [string]$BlenderExecutable = "$env:USERPROFILE/AppData/Local/Programs/Blender/blender-4.5.14-windows-x64/blender.exe",
    [string]$AddonPath = "$env:USERPROFILE/AppData/Roaming/Blender Foundation/Blender/4.5/scripts/addons/blender_mcp.py",
    [string]$StateRoot = "$env:USERPROFILE/.codex/blender-workers",
    [ValidateRange(1024,65000)][int]$FirstPort = 19876,
    [ValidateRange(1,200)][int]$PortCount = 100
)
$ErrorActionPreference = 'Stop'
$outputRoot = (Resolve-Path -LiteralPath $OutputDirectory).Path
$blenderPath = (Resolve-Path -LiteralPath $BlenderExecutable).Path
$addonSource = (Resolve-Path -LiteralPath $AddonPath).Path
$bootstrap = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot 'blender_worker_bootstrap.py')).Path
New-Item -ItemType Directory -Force -Path $StateRoot | Out-Null
$statePath = (Resolve-Path -LiteralPath $StateRoot).Path
$portsPath = Join-Path $statePath 'ports'
New-Item -ItemType Directory -Force -Path $portsPath | Out-Null
$token = [guid]::NewGuid().ToString('N')
$reservation = $null
for ($candidate = $FirstPort; $candidate -lt ($FirstPort + $PortCount); $candidate++) {
    if ($candidate -eq 9876 -or $candidate -gt 65535) { continue }
    $leasePath = Join-Path $portsPath "$candidate.json"
    try { $reservation = [IO.File]::Open($leasePath, [IO.FileMode]::CreateNew, [IO.FileAccess]::Write, [IO.FileShare]::None) }
    catch [IO.IOException] { continue }
    $probe = [Net.Sockets.TcpListener]::new([Net.IPAddress]::Loopback, $candidate)
    try { $probe.Server.ExclusiveAddressUse = $true; $probe.Start(); $probe.Stop() }
    catch {
        $probe.Stop(); $reservation.Dispose(); $reservation = $null
        Remove-Item -LiteralPath $leasePath
        continue
    }
    $port = $candidate
    break
}
if ($null -eq $reservation) { throw 'No unleased dedicated port available; inspect owned worker sessions, do not reuse the shared endpoint.' }
$runRoot = Join-Path $statePath $token
foreach ($sub in @('', 'config', 'scripts', 'datafiles')) {
    New-Item -ItemType Directory -Force -Path (Join-Path $runRoot $sub) | Out-Null
}
$sessionPath = Join-Path $runRoot 'session.json'
$session = [ordered]@{
    host='127.0.0.1'; port=$port; token=$token; run_root=$runRoot; session_file=$sessionPath
    output_directory=$outputRoot; status='starting'; process_id=$null
    reservation_process_id=$PID; lease_file=$leasePath
    blender_executable=$blenderPath; addon_path=$addonSource
    started_utc=[DateTime]::UtcNow.ToString('o')
}
$bytes = [Text.Encoding]::UTF8.GetBytes(($session | ConvertTo-Json))
$reservation.Write($bytes,0,$bytes.Length); $reservation.Dispose()
$process = $null
try {
$session | ConvertTo-Json | Set-Content -LiteralPath $sessionPath -Encoding utf8
$workerEnvironment = @{
    BLENDER_USER_CONFIG=(Join-Path $runRoot 'config')
    BLENDER_USER_SCRIPTS=(Join-Path $runRoot 'scripts')
    BLENDER_USER_DATAFILES=(Join-Path $runRoot 'datafiles')
    DISABLE_TELEMETRY='true'; PYTHONUTF8='1'
}
# Quotes are for Windows argv parsing, not shell code; paths cannot contain quotes.
$launchArgs = @('--factory-startup','--python',('"'+$bootstrap+'"'),'--',('"'+$sessionPath+'"'))
$process = Start-Process -FilePath $blenderPath -ArgumentList $launchArgs -Environment $workerEnvironment `
    -WindowStyle Hidden -PassThru -RedirectStandardOutput (Join-Path $runRoot 'blender.stdout.log') `
    -RedirectStandardError (Join-Path $runRoot 'blender.stderr.log')
$ownedHandle = $process.SafeHandle
$launchTemporary = Join-Path $runRoot 'launch.json.tmp'
@{process_id=$process.Id;process_started_utc=$process.StartTime.ToUniversalTime().ToString('o')} |
    ConvertTo-Json | Set-Content -LiteralPath $launchTemporary -Encoding utf8
Move-Item -LiteralPath $launchTemporary -Destination (Join-Path $runRoot 'launch.json')
$deadline = [DateTime]::UtcNow.AddSeconds(45)
do {
    if ($process.HasExited) { throw "Blender exited before readiness: $runRoot" }
    Start-Sleep -Milliseconds 200
    try { $current = Get-Content -LiteralPath $sessionPath -Raw | ConvertFrom-Json }
    catch { continue } # Bootstrap may be replacing the initial record at this instant.
    if ($current.status -eq 'failed') { throw $current.error }
} while ($current.status -ne 'ready' -and [DateTime]::UtcNow -lt $deadline)
if ($current.status -ne 'ready') { throw "Timed out waiting for dedicated Blender MCP: $sessionPath" }
if ($current.process_id -ne $process.Id) { throw 'Bootstrap PID did not match launched process' }
$current | ConvertTo-Json -Depth 5
} catch {
    $failure = $_.Exception.Message
    if ($null -ne $process -and -not $process.HasExited) {
        $process.Kill() # Uses the handle of the process created by this invocation.
        $process.WaitForExit(15000) | Out-Null
    }
    $session.status = 'failed'
    $session['error'] = $failure
    if ($null -ne $process) { $session.process_id = $process.Id }
    $session | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $sessionPath -Encoding utf8
    if (Test-Path -LiteralPath $leasePath) {
        $record = Get-Content -LiteralPath $leasePath -Raw | ConvertFrom-Json
        if ($record.token -eq $token) { Remove-Item -LiteralPath $leasePath }
    }
    throw "Dedicated Blender startup failed; owned process/lease cleaned, logs retained at $runRoot. $failure"
}
