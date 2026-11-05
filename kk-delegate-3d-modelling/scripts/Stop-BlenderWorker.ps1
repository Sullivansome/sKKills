param(
    [Parameter(Mandatory=$true)][string]$SessionFile,
    [Parameter(Mandatory=$true)][switch]$ExportsValidated
)
$ErrorActionPreference = 'Stop'
if (-not $ExportsValidated) { throw 'Save and validate all wanted outputs before closing an owned test worker.' }
$sessionPath = (Resolve-Path -LiteralPath $SessionFile).Path
$session = Get-Content -LiteralPath $sessionPath -Raw | ConvertFrom-Json
if ($session.token -notmatch '^[a-f0-9]{32}$' -or $session.port -eq 9876) { throw 'Not a dedicated owned worker' }
$rootPath = [IO.Path]::GetFullPath($session.run_root)
if ((Split-Path $rootPath -Leaf) -ne $session.token) { throw 'Run folder does not match session token' }
$expectedLease = Join-Path (Split-Path $rootPath -Parent) "ports/$($session.port).json"
if ([IO.Path]::GetFullPath($session.lease_file) -ne [IO.Path]::GetFullPath($expectedLease)) { throw 'Lease path is outside the worker registry' }
$lease = Get-Content -LiteralPath $expectedLease -Raw | ConvertFrom-Json
if ($lease.token -ne $session.token -or $lease.process_id -ne $session.process_id) { throw 'Port lease belongs to another worker' }
try { $workerLock = [IO.File]::Open((Join-Path $rootPath 'worker.lock'),[IO.FileMode]::OpenOrCreate,[IO.FileAccess]::ReadWrite,[IO.FileShare]::None) }
catch { throw 'A modelling worker is still active; finish it before closing its Blender process.' }
try {
    $modellerPath = Join-Path $rootPath 'modeller.json'
    if (Test-Path -LiteralPath $modellerPath) {
        $modeller = Get-Content -LiteralPath $modellerPath -Raw | ConvertFrom-Json
        $child = Get-Process -Id $modeller.process_id -ErrorAction SilentlyContinue
        if ($null -ne $child -and $child.StartTime.ToUniversalTime().Ticks -eq ([DateTime]$modeller.process_started_utc).ToUniversalTime().Ticks) {
            throw 'The Codex modeller process is still alive; refusing to close its Blender session.'
        }
    }
    $target = Get-Process -Id $session.process_id -ErrorAction SilentlyContinue
    if ($null -ne $target) { $ownedHandle = $target.SafeHandle }
    $process = Get-CimInstance Win32_Process -Filter "ProcessId = $($session.process_id)"
    if ($null -ne $process) {
        if ($process.ExecutablePath -ne $session.blender_executable -or $process.CommandLine -notlike "*$sessionPath*") {
            throw 'PID identity changed; refusing to close another process'
        }
        if ($null -ne $session.process_started_utc -and $target.StartTime.ToUniversalTime().Ticks -ne ([DateTime]$session.process_started_utc).ToUniversalTime().Ticks) {
            throw 'Blender process creation time changed; refusing to close it'
        }
        if ($null -ne $target -and -not $target.HasExited) {
            $target.Kill() # Cached owned handle prevents numeric PID reuse races.
            if (-not $target.WaitForExit(15000)) { throw 'Owned worker did not exit; lease retained' }
        }
    }
    $session.status = 'closed'
    $session | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $sessionPath -Encoding utf8
    Remove-Item -LiteralPath $expectedLease
    Write-Output "Closed only owned Blender worker $($session.process_id) on port $($session.port); output files retained."
} finally { $workerLock.Dispose() }
