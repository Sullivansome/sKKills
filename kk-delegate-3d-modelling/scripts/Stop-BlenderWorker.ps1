param(
    [Parameter(Mandatory=$true)][string]$SessionFile,
    [Parameter(Mandatory=$true)][switch]$ExportsValidated
)
$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot 'BlenderWorkerState.ps1')
if (-not $ExportsValidated) { throw 'Save and validate all wanted outputs before closing an owned test worker.' }
$sessionPath = (Resolve-Path -LiteralPath $SessionFile).Path
$rootPath = Split-Path -LiteralPath $sessionPath
$statePath = Split-Path -LiteralPath $rootPath
try { $workerLock = [IO.File]::Open((Join-Path $rootPath 'worker.lock'),[IO.FileMode]::OpenOrCreate,[IO.FileAccess]::ReadWrite,[IO.FileShare]::None) }
catch { throw 'A modelling worker is still active; finish it before closing its Blender process.' }
try {
    $session = Get-Content -LiteralPath $sessionPath -Raw | ConvertFrom-Json
    if ($session.token -notmatch '^[a-f0-9]{32}$' -or $session.port -eq 9876 -or
        $session.status -notin @('ready', 'closed') -or
        (Split-Path -Leaf $rootPath) -ne $session.token -or $session.run_root -ne $rootPath -or
        $session.session_file -ne $sessionPath) { throw 'Not a dedicated owned worker' }
    $expectedLease = Join-Path $statePath "ports/$($session.port).json"
    if ([IO.Path]::GetFullPath($session.lease_file) -ne [IO.Path]::GetFullPath($expectedLease)) {
        throw 'Port lease path is outside the worker registry'
    }
    $lease = $null
    if (Test-Path -LiteralPath $expectedLease -PathType Leaf) {
        $lease = Get-Content -LiteralPath $expectedLease -Raw | ConvertFrom-Json
    }
    if ($session.status -ne 'closed' -and
        ($null -eq $lease -or $lease.token -ne $session.token -or $lease.process_id -ne $session.process_id)) {
        throw 'Port lease belongs to another worker'
    }
    $outputLease = Get-BlenderOutputLease $session $statePath
    $modellerPath = Join-Path $rootPath 'modeller.json'
    if (Test-Path -LiteralPath $modellerPath) {
        $modeller = Get-Content -LiteralPath $modellerPath -Raw | ConvertFrom-Json
        $child = Get-Process -Id $modeller.process_id -ErrorAction SilentlyContinue
        if ($null -ne $child -and $child.StartTime.ToUniversalTime().Ticks -eq ([DateTime]$modeller.process_started_utc).ToUniversalTime().Ticks) {
            throw 'The Codex modeller process is still alive; refusing to close its Blender session.'
        }
    }
    if ($session.status -ne 'closed') {
        $target = Get-Process -Id $session.process_id -ErrorAction SilentlyContinue
        if ($null -ne $target) {
            $ownedHandle = $target.SafeHandle
            $process = Get-CimInstance Win32_Process -Filter "ProcessId = $($session.process_id)"
            if (-not $target.HasExited) {
                if ($null -eq $process -or $process.ExecutablePath -ne $session.blender_executable -or
                    -not $process.CommandLine.Contains($sessionPath, [StringComparison]::OrdinalIgnoreCase) -or
                    $target.StartTime.ToUniversalTime().Ticks -ne ([DateTime]$session.process_started_utc).ToUniversalTime().Ticks) {
                    throw 'PID identity changed; refusing to close another process'
                }
                $target.Kill() # Cached owned handle prevents numeric PID reuse races.
                if (-not $target.WaitForExit(15000)) { throw 'Owned worker did not exit; leases retained' }
            }
        }
        $session.status = 'closed'
        $temporary = "$sessionPath.closed.tmp"
        $session | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $temporary -Encoding utf8
        [IO.File]::Move($temporary, $sessionPath, $true)
    }
    if ($outputLease) { Remove-BlenderOutputLease $statePath $session.output_lease_file $session.token }
    if ($lease -and $lease.token -eq $session.token) { Remove-Item -LiteralPath $expectedLease }
    Write-Output "Closed only owned Blender worker $($session.process_id) on port $($session.port); output files retained."
} finally { $workerLock.Dispose() }
