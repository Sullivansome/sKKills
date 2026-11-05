param(
    [Parameter(Mandatory=$true)][string]$WorkDirectory,
    [Parameter(Mandatory=$true)][string]$PromptFile,
    [Parameter(Mandatory=$true)][string]$ReferenceImage,
    [Parameter(Mandatory=$true)][string]$SessionFile
)
$ErrorActionPreference = 'Stop'
$workerRoot = (Resolve-Path -LiteralPath $WorkDirectory).Path
$briefPath = (Resolve-Path -LiteralPath $PromptFile).Path
$imagePath = (Resolve-Path -LiteralPath $ReferenceImage).Path
$sessionPath = (Resolve-Path -LiteralPath $SessionFile).Path
$session = Get-Content -LiteralPath $sessionPath -Raw | ConvertFrom-Json
if ($session.status -ne 'ready' -or $session.host -ne '127.0.0.1' -or $session.port -eq 9876 -or
    $session.token -notmatch '^[a-f0-9]{32}$' -or $session.background -ne $false) {
    throw 'A ready isolated interactive worker session is required; shared-port fallback is forbidden.'
}
if (([IO.Path]::GetFullPath($session.output_directory)).TrimEnd('\','/') -ne $workerRoot.TrimEnd('\','/')) {
    throw 'Session output directory does not match the modeller workspace'
}
$blenderProcess = Get-Process -Id $session.process_id -ErrorAction Stop
if ($blenderProcess.ProcessName -ne 'blender') { throw 'Assigned Blender process is not alive' }
$listener = @(Get-NetTCPConnection -LocalPort $session.port -State Listen -ErrorAction Stop)
if ($listener.Count -ne 1 -or $listener[0].OwningProcess -ne $session.process_id) { throw 'Dedicated port does not belong to assigned Blender process' }
$lockPath = Join-Path $session.run_root 'worker.lock'
try { $workerLock = [IO.File]::Open($lockPath,[IO.FileMode]::OpenOrCreate,[IO.FileAccess]::ReadWrite,[IO.FileShare]::None) }
catch { throw 'This session already has an active modelling worker; allocate another session.' }
try {
    $modellerPath = Join-Path $session.run_root 'modeller.json'
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
    $serverEnv = 'mcp_servers.blender.env={BLENDER_HOST="127.0.0.1",BLENDER_PORT="'+$session.port+'",DISABLE_TELEMETRY="true",PYTHONUTF8="1"}'
    $workerArgs = @('exec','--skip-git-repo-check','--approve-for-me','-C',$workerRoot,
        '-m','gpt-6.1-terra','-c','model_reasoning_effort="medium"','-c','service_tier="priority"',
        '-c',$serverEnv,'-o',(Join-Path $workerRoot 'last-model.md'),'-i',$imagePath,'--','-')
    $identity = @"
You are the assigned modeller. Do not recursively delegate. Use kk-delegate-3d-modelling and blender-skills.
This run is assigned a NEW dedicated interactive Blender MCP process, not the global shared endpoint.
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
Requested model gpt-6.1-terra, effort medium, service_tier priority. Never substitute another model or headless Blender.

"@
    @{model='gpt-6.1-terra';reasoning_effort='medium';service_tier='priority';executable=$codexBinary;
      work_directory=$workerRoot;reference=$imagePath;session_file=$sessionPath;blender_process_id=$session.process_id;
      blender_host=$session.host;blender_port=$session.port;token=$session.token;started_utc=[DateTime]::UtcNow.ToString('o')} |
        ConvertTo-Json | Set-Content -LiteralPath (Join-Path $workerRoot 'run-config.json') -Encoding utf8
    $promptText = $identity + (Get-Content -LiteralPath $briefPath -Raw)
    $psi = [Diagnostics.ProcessStartInfo]::new()
    $psi.FileName = $codexBinary; $psi.WorkingDirectory = $workerRoot; $psi.UseShellExecute = $false
    $psi.CreateNoWindow = $true
    $psi.RedirectStandardInput = $true; $psi.RedirectStandardOutput = $true; $psi.RedirectStandardError = $true
    foreach ($arg in $workerArgs) { $psi.ArgumentList.Add($arg) }
    $child = [Diagnostics.Process]::new(); $child.StartInfo = $psi
    if (-not $child.Start()) { throw 'Codex child process did not start' }
    $childHandle = $child.SafeHandle
    $modeller = @{process_id=$child.Id;process_started_utc=$child.StartTime.ToUniversalTime().ToString('o');
        executable=$codexBinary;status='running';session_file=$sessionPath}
    # Persist ownership BEFORE providing the prompt: an orphan may keep modelling.
    $modeller | ConvertTo-Json | Set-Content -LiteralPath $modellerPath -Encoding utf8
    $outStream = [IO.File]::Open((Join-Path $workerRoot 'codex-model.stdout.log'),[IO.FileMode]::Create,[IO.FileAccess]::Write,[IO.FileShare]::ReadWrite)
    $errStream = [IO.File]::Open((Join-Path $workerRoot 'codex-model.log'),[IO.FileMode]::Create,[IO.FileAccess]::Write,[IO.FileShare]::ReadWrite)
    $outTask = $child.StandardOutput.BaseStream.CopyToAsync($outStream)
    $errTask = $child.StandardError.BaseStream.CopyToAsync($errStream)
    $child.StandardInput.Write($promptText); $child.StandardInput.Close()
    while (-not $child.HasExited) { Start-Sleep -Milliseconds 200 }
    [void]$outTask.GetAwaiter().GetResult(); [void]$errTask.GetAwaiter().GetResult()
    $outStream.Dispose(); $errStream.Dispose()
    $modeller.status = 'exited'; $modeller['exit_code'] = $child.ExitCode
    $modeller | ConvertTo-Json | Set-Content -LiteralPath $modellerPath -Encoding utf8
    if ($child.ExitCode -ne 0) { throw "Codex modelling failed ($($child.ExitCode)); see codex-model.log" }
    Write-Output "Codex modeller completed; logs and last-model.md: $workerRoot"
} finally { $workerLock.Dispose() }

