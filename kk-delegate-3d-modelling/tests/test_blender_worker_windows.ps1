$ErrorActionPreference = 'Stop'
$scripts = Join-Path (Split-Path -LiteralPath $PSScriptRoot) 'scripts'
foreach ($script in Get-ChildItem -LiteralPath $scripts -Filter '*.ps1') {
    $tokens = $null
    $errors = $null
    $null = [Management.Automation.Language.Parser]::ParseFile($script.FullName, [ref]$tokens, [ref]$errors)
    if ($errors) { throw ($errors -join "`n") }
}
. (Join-Path $scripts 'BlenderWorkerState.ps1')

if (-not $IsWindows) {
    # Exercise the PowerShell registry logic on Unix with deterministic Windows-style scopes.
    function Get-BlenderOutputScope([string]$Path) { $Path.Replace('/', '\') }
}

function Assert-Fails([scriptblock]$Action, [string]$Message) {
    try { & $Action | Out-Null }
    catch {
        if ($_.Exception.Message -notlike $Message) { throw }
        return
    }
    throw "Expected failure matching: $Message"
}

$root = Join-Path ([IO.Path]::GetTempPath()) ("blender-worker-test-" + [guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $root | Out-Null
try {
    $state = (New-Item -ItemType Directory -Path (Join-Path $root 'registry')).FullName
    $ports = (New-Item -ItemType Directory -Path (Join-Path $state 'ports')).FullName
    $asset = (New-Item -ItemType Directory -Path (Join-Path $root 'Asset')).FullName
    $nested = (New-Item -ItemType Directory -Path (Join-Path $asset 'part')).FullName
    $separate = (New-Item -ItemType Directory -Path (Join-Path $root 'Asset-other')).FullName
    $first = 'a' * 32
    $second = 'b' * 32
    $lease = New-BlenderOutputLease $state $asset $first
    Assert-Fails { New-BlenderOutputLease $state $asset $second } '*overlaps reserved scope*'
    Assert-Fails { New-BlenderOutputLease $state $nested $second } '*overlaps reserved scope*'
    if ($IsWindows) {
        $alias = (New-Item -ItemType Junction -Path (Join-Path $root 'Junction') -Target $asset).FullName
        try {
            Assert-Fails { New-BlenderOutputLease $state $asset.ToLowerInvariant() $second } '*overlaps reserved scope*'
            Assert-Fails { New-BlenderOutputLease $state (Join-Path $alias 'part') $second } '*overlaps reserved scope*'
        } finally {
            [IO.Directory]::Delete($alias)
        }
    }
    $secondLease = New-BlenderOutputLease $state $separate $second
    Assert-Fails { Remove-BlenderOutputLease $state $lease $second } '*belongs to another worker*'
    Remove-BlenderOutputLease $state $lease $first
    Remove-BlenderOutputLease $state $secondLease $second

    $run = (New-Item -ItemType Directory -Path (Join-Path $state $first)).FullName
    $session = @{
        run_root=$run; session_file=(Join-Path $run 'session.json'); token=$first
        host='127.0.0.1'; port=19876; process_id=123; status='ready'
        platform='windows'; output_directory=$asset
    }
    $portLease = Join-Path $ports '19876.json'
    $session | ConvertTo-Json | Set-Content -LiteralPath $session.session_file
    @{token=$first;process_id=$session.process_id} | ConvertTo-Json | Set-Content -LiteralPath $portLease
    Assert-Fails { New-BlenderOutputLease $state $nested $second } '*previous worker*'
    Remove-Item -LiteralPath $portLease
    $lease = New-BlenderOutputLease $state $asset $second
    Remove-BlenderOutputLease $state $lease $second

    # Retry cleanup after the owned process has exited and the session was marked closed.
    $session.status = 'closed'
    $session.lease_file = $portLease
    $session.output_lease_file = New-BlenderOutputLease $state $asset $first
    $session | ConvertTo-Json | Set-Content -LiteralPath $session.session_file
    @{token=$first;process_id=$session.process_id} | ConvertTo-Json | Set-Content -LiteralPath $portLease
    $stop = Join-Path $scripts 'Stop-BlenderWorker.ps1'
    & $stop -SessionFile $session.session_file -ExportsValidated | Out-Null
    if ((Test-Path -LiteralPath $session.output_lease_file) -or (Test-Path -LiteralPath $portLease)) {
        throw 'Stopping an owned worker must release its output and port leases'
    }
    @{token=$second;process_id=456} | ConvertTo-Json | Set-Content -LiteralPath $portLease
    & $stop -SessionFile $session.session_file -ExportsValidated | Out-Null
    if ((Get-Content -LiteralPath $portLease -Raw | ConvertFrom-Json).token -ne $second) {
        throw 'Retrying cleanup must preserve a new port owner'
    }

    $session.status = 'ready'
    $reference = Join-Path $asset 'reference image.png'
    $initial = New-BlenderModellerAttempt $session $asset $reference simple gpt-6.1-terra high priority 'codex.exe'
    Set-Content -LiteralPath (Join-Path $initial.directory 'stderr.log') 'session id: test-thread'
    $resume = New-BlenderModellerAttempt $session $asset $reference simple gpt-6.1-terra high priority 'codex.exe' 'test-thread'
    $config = Get-Content -LiteralPath $resume.config_path -Raw | ConvertFrom-Json
    $pointer = Get-Content -LiteralPath (Join-Path $asset 'model-run.json') -Raw | ConvertFrom-Json
    $execIndex = [array]::IndexOf($config.args, 'exec')
    if ($initial.arguments -notcontains $reference -or $initial.arguments -contains 'resume' -or
        $execIndex -lt 0 -or $config.args[$execIndex + 1] -ne 'resume' -or
        ($config.args[-3..-1] -join ' ') -ne '-- test-thread -' -or
        $config.args -notcontains ('-m') -or $config.args -notcontains 'gpt-6.1-terra' -or
        $config.args -notcontains 'service_tier="priority"' -or
        -not ($config.args -like '*BLENDER_PORT="19876"*') -or $config.session_file -ne $session.session_file -or
        $pointer.run_config -ne $resume.config_path -or $initial.directory -eq $resume.directory -or
        (-not (Test-Path -LiteralPath $initial.config_path)) -or
        (Get-Content -LiteralPath (Join-Path $initial.directory 'stderr.log')) -ne 'session id: test-thread') {
        throw 'Resume must keep the worker identity, thread, launch settings, and earlier attempt evidence'
    }
    Write-Output 'PowerShell launcher regression checks passed.'
} finally {
    Remove-Item -LiteralPath $root -Recurse -Force
}
