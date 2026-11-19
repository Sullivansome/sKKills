param(
    [Parameter(Mandatory=$true)][string]$WorkDirectory,
    [Parameter(Mandatory=$true)][string]$PromptFile,
    [Parameter(Mandatory=$true)][string]$ReferenceImage,
    [Parameter(Mandatory=$true)][string]$SessionFile,
    [Parameter(Mandatory=$true)][ValidateSet('simple','complex','toughest')][string]$Complexity,
    [string]$ResumeThread
)
$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot 'BlenderWorkerState.ps1')
$workerProfiles = @{
    simple = @{model='gpt-6.1-terra'; service_tier='priority'}
    complex = @{model='gpt-6.2-sol'; service_tier='default'}
    toughest = @{model='gpt-6.2-astra'; service_tier='default'}
}
$profileSettings = $workerProfiles[$Complexity]
$model = $profileSettings.model
$reasoningEffort = 'high'
$serviceTier = $profileSettings.service_tier
$workerRoot = (Resolve-Path -LiteralPath $WorkDirectory).Path
$briefPath = (Resolve-Path -LiteralPath $PromptFile).Path
$imagePath = (Resolve-Path -LiteralPath $ReferenceImage).Path
$sessionPath = (Resolve-Path -LiteralPath $SessionFile).Path
$runRoot = Split-Path -LiteralPath $sessionPath
$statePath = Split-Path -LiteralPath $runRoot
$lockPath = Join-Path $runRoot 'worker.lock'
try { $workerLock = [IO.File]::Open($lockPath,[IO.FileMode]::OpenOrCreate,[IO.FileAccess]::ReadWrite,[IO.FileShare]::None) }
catch { throw 'This session already has an active modelling worker; allocate another session.' }
try {
    $session = Get-Content -LiteralPath $sessionPath -Raw | ConvertFrom-Json
    if ($session.status -ne 'ready' -or $session.host -ne '127.0.0.1' -or $session.port -eq 9876 -or
        $session.token -notmatch '^[a-f0-9]{32}$' -or $session.background -ne $false -or
        (Split-Path -Leaf $runRoot) -ne $session.token -or $session.run_root -ne $runRoot -or
        $session.session_file -ne $sessionPath) {
        throw 'A ready isolated interactive worker session is required; shared-port fallback is forbidden.'
    }
    $scope = Get-BlenderOutputScope $workerRoot
    $outputLease = Get-BlenderOutputLease $session $statePath
    if ($scope -ne (Get-BlenderOutputScope $session.output_directory) -or
        ($outputLease -and $scope -ne $outputLease.output_scope)) {
        throw 'Session output directory does not match the modeller workspace'
    }
    $blenderProcess = Get-Process -Id $session.process_id -ErrorAction Stop
    if ($blenderProcess.ProcessName -ne 'blender' -or
        $blenderProcess.StartTime.ToUniversalTime().Ticks -ne ([DateTime]$session.process_started_utc).ToUniversalTime().Ticks) {
        throw 'Assigned Blender process identity changed'
    }
    $listener = @(Get-NetTCPConnection -LocalPort $session.port -State Listen -ErrorAction Stop)
    if ($listener.Count -ne 1 -or $listener[0].OwningProcess -ne $session.process_id) {
        throw 'Dedicated port does not belong to assigned Blender process'
    }
    $modellerPath = Join-Path $runRoot 'modeller.json'
    if (Test-Path -LiteralPath $modellerPath) {
        $previous = Get-Content -LiteralPath $modellerPath -Raw | ConvertFrom-Json
        $priorProcess = Get-Process -Id $previous.process_id -ErrorAction SilentlyContinue
        if ($null -ne $priorProcess -and $priorProcess.StartTime.ToUniversalTime().Ticks -eq ([DateTime]$previous.process_started_utc).ToUniversalTime().Ticks) {
            throw 'A previously launched Codex child still owns this Blender session, even if its wrapper exited.'
        }
    }
    $codexBinary = Get-ChildItem -LiteralPath "$env:USERPROFILE/AppData/Local/OpenAI/Codex/bin" -Recurse -Filter codex.exe |
        Sort-Object LastWriteTime -Descending | Select-Object -First 1 -ExpandProperty FullName
    if (-not $codexBinary) { throw 'Installed Codex CLI was not found' }
    $launch = New-BlenderModellerAttempt $session $workerRoot $imagePath $Complexity $model `
        $reasoningEffort $serviceTier $codexBinary $ResumeThread
    $attempt = $launch.directory
    $configPath = $launch.config_path
    $identity = @"
You are the assigned modeller. Do not recursively delegate. Use kk-delegate-3d-modelling and blender-skills.
This run is assigned the dedicated interactive Blender MCP process listed below.
Before ANY Blender mutation, call Blender MCP get_addon_status and then execute_blender_code with:
import bpy, os, json
server = getattr(bpy.types, 'blendermcp_server', None)
identity = {'pid':os.getpid(), 'token':bpy.app.driver_namespace.get('codex_worker_token'), 'port':getattr(server,'port',None), 'background':bpy.app.background}
assert identity == {'pid':$($session.process_id), 'token':'$($session.token)', 'port':$($session.port), 'background':False}, identity
print(json.dumps(identity))
Save the actual returned identity in your output folder. If it fails, STOP and report; no fallback or reconnection to port9876.
Use only the configured blender MCP server. Never change ports, server config, preferences, existing scenes, or open/reset files.
Build in new isolated scenes/collections and save separate assets. The initial Cube/Camera/Light and marker scene must survive.
An independent GUI process was created specifically for this job; --factory-startup was used only at its launch, not on an existing session.
Session metadata (read-only): $sessionPath
Confirm the requested model $model, $reasoningEffort reasoning effort and service tier $serviceTier in $configPath.

"@
    $promptText = $identity + (Get-Content -LiteralPath $briefPath -Raw)
    $psi = [Diagnostics.ProcessStartInfo]::new()
    $psi.FileName = $codexBinary; $psi.WorkingDirectory = $workerRoot; $psi.UseShellExecute = $false
    $psi.CreateNoWindow = $true
    $psi.RedirectStandardInput = $true; $psi.RedirectStandardOutput = $true; $psi.RedirectStandardError = $true
    foreach ($arg in $launch.arguments) { $psi.ArgumentList.Add($arg) }
    $child = [Diagnostics.Process]::new(); $child.StartInfo = $psi
    if (-not $child.Start()) { throw 'Codex child process did not start' }
    $outStream = $null
    $errStream = $null
    try {
        $childHandle = $child.SafeHandle
        $modeller = @{process_id=$child.Id;process_started_utc=$child.StartTime.ToUniversalTime().ToString('o');
            executable=$codexBinary;status='running';session_file=$sessionPath}
        # Persist ownership before providing the prompt: an orphan may keep modelling.
        $modeller | ConvertTo-Json | Set-Content -LiteralPath $modellerPath -Encoding utf8
        $outStream = [IO.File]::Open((Join-Path $attempt 'stdout.log'),[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::ReadWrite)
        $errStream = [IO.File]::Open((Join-Path $attempt 'stderr.log'),[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::ReadWrite)
        $outTask = $child.StandardOutput.BaseStream.CopyToAsync($outStream)
        $errTask = $child.StandardError.BaseStream.CopyToAsync($errStream)
        $child.StandardInput.Write($promptText)
        $child.StandardInput.Close()
        $child.WaitForExit()
        [void]$outTask.GetAwaiter().GetResult()
        [void]$errTask.GetAwaiter().GetResult()
    } finally {
        $child.StandardInput.Close()
        if ($outStream) { $outStream.Dispose() }
        if ($errStream) { $errStream.Dispose() }
    }
    $modeller.status = 'exited'; $modeller['exit_code'] = $child.ExitCode
    $modeller | ConvertTo-Json | Set-Content -LiteralPath $modellerPath -Encoding utf8
    if ($child.ExitCode -ne 0) { throw "Codex modelling failed ($($child.ExitCode)); logs: $attempt" }
    Write-Output "ATTEMPT_DIRECTORY=$attempt"
} finally { $workerLock.Dispose() }

