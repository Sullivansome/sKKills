function Get-BlenderOutputScope([string]$Path) {
    if (-not ('BlenderWorker.DirectoryPath' -as [type])) {
        Add-Type -TypeDefinition @'
using System;
using System.ComponentModel;
using System.Runtime.InteropServices;
using System.Text;
using Microsoft.Win32.SafeHandles;

namespace BlenderWorker {
    public static class DirectoryPath {
        [DllImport("kernel32.dll", CharSet = CharSet.Unicode, ExactSpelling = true, SetLastError = true)]
        private static extern SafeFileHandle CreateFileW(string path, uint access, uint share,
            IntPtr security, uint disposition, uint flags, IntPtr template);

        [DllImport("kernel32.dll", CharSet = CharSet.Unicode, ExactSpelling = true, SetLastError = true)]
        private static extern uint GetFinalPathNameByHandleW(SafeFileHandle handle,
            StringBuilder path, uint capacity, uint flags);

        public static string Resolve(string path) {
            // Open an existing directory, following junctions and symlinks.
            using (var handle = CreateFileW(path, 0, 7, IntPtr.Zero, 3, 0x02000000, IntPtr.Zero)) {
                if (handle.IsInvalid) throw new Win32Exception(Marshal.GetLastWin32Error());
                var result = new StringBuilder(260);
                while (true) {
                    // Request the normalized path using the NT volume name instead of a drive alias.
                    uint length = GetFinalPathNameByHandleW(handle, result, (uint)result.Capacity, 2);
                    if (length == 0) throw new Win32Exception(Marshal.GetLastWin32Error());
                    if (length < result.Capacity) return result.ToString();
                    result.EnsureCapacity(checked((int)length));
                }
            }
        }
    }
}
'@
    }
    if (-not (Test-Path -LiteralPath $Path -PathType Container)) {
        throw "Output directory must exist: $Path"
    }
    [BlenderWorker.DirectoryPath]::Resolve($Path)
}

function Test-BlenderOutputOverlap([string]$First, [string]$Second) {
    $firstPath = $First.TrimEnd('\') + '\'
    $secondPath = $Second.TrimEnd('\') + '\'
    $comparison = [StringComparison]::OrdinalIgnoreCase
    $firstPath.StartsWith($secondPath, $comparison) -or $secondPath.StartsWith($firstPath, $comparison)
}

function Open-BlenderOutputRegistry([string]$StatePath) {
    $lockPath = Join-Path $StatePath 'outputs.lock'
    $clock = [Diagnostics.Stopwatch]::StartNew()
    while ($true) {
        try { return [IO.File]::Open($lockPath, 'OpenOrCreate', 'ReadWrite', 'None') }
        catch [IO.IOException] {
            if (($_.Exception.GetBaseException().HResult -band 0xffff) -notin @(32, 33) -or
                $clock.Elapsed.TotalSeconds -ge 15) { throw }
            Start-Sleep -Milliseconds 50
        }
    }
}

function New-BlenderOutputLease([string]$StatePath, [string]$OutputRoot, [string]$Token) {
    $outputs = Join-Path $StatePath 'outputs'
    New-Item -ItemType Directory -Force -Path $outputs | Out-Null
    $scope = Get-BlenderOutputScope $OutputRoot
    $registry = Open-BlenderOutputRegistry $StatePath
    try {
        foreach ($file in Get-ChildItem -LiteralPath $outputs -Filter '*.json' -File) {
            $record = Get-Content -LiteralPath $file.FullName -Raw | ConvertFrom-Json
            if ($record.token -notmatch '^[a-f0-9]{32}$' -or $file.BaseName -ne $record.token -or
                -not $record.output_scope -or -not $record.output_directory) {
                throw "Malformed output lease: $($file.FullName)"
            }
            if ((Test-BlenderOutputOverlap $scope $record.output_scope) -or
                (Test-BlenderOutputOverlap $OutputRoot $record.output_directory)) {
                throw "Output directory overlaps reserved scope: $($record.output_directory)"
            }
        }
        # Sessions allocated by the earlier Windows launcher only reserved a port.
        foreach ($folder in Get-ChildItem -LiteralPath $StatePath -Directory) {
            if ($folder.Name -notmatch '^[a-f0-9]{32}$') { continue }
            $path = Join-Path $folder.FullName 'session.json'
            if (-not (Test-Path -LiteralPath $path -PathType Leaf)) { continue }
            $session = Get-Content -LiteralPath $path -Raw | ConvertFrom-Json
            if ($session.output_lease_file -or $session.status -notin @('starting', 'ready') -or
                $session.platform -ne 'windows' -or $session.token -ne $folder.Name) { continue }
            $portLease = Join-Path $StatePath "ports/$($session.port).json"
            if (-not (Test-Path -LiteralPath $portLease -PathType Leaf)) { continue }
            $portRecord = Get-Content -LiteralPath $portLease -Raw | ConvertFrom-Json
            if ($portRecord.token -ne $session.token) { continue }
            if ((Test-BlenderOutputOverlap $OutputRoot $session.output_directory) -or
                ((Test-Path -LiteralPath $session.output_directory -PathType Container) -and
                    (Test-BlenderOutputOverlap $scope (Get-BlenderOutputScope $session.output_directory)))) {
                throw "Output directory overlaps a previous worker's scope: $($session.output_directory)"
            }
        }
        $leasePath = Join-Path $outputs "$Token.json"
        $temporary = "$leasePath.tmp"
        try {
            @{token=$Token; output_directory=$OutputRoot; output_scope=$scope} |
                ConvertTo-Json | Set-Content -LiteralPath $temporary -Encoding utf8
            [IO.File]::Move($temporary, $leasePath)
        } finally {
            [IO.File]::Delete($temporary)
        }
        return $leasePath
    } finally {
        $registry.Dispose()
    }
}

function Get-BlenderOutputLease($Session, [string]$StatePath) {
    if (-not $Session.output_lease_file) { return }
    $expected = Join-Path $StatePath "outputs/$($Session.token).json"
    if ([IO.Path]::GetFullPath($Session.output_lease_file) -ne [IO.Path]::GetFullPath($expected)) {
        throw 'Output lease path is outside the worker registry'
    }
    if ($Session.status -eq 'closed' -and -not (Test-Path -LiteralPath $expected -PathType Leaf)) { return }
    $record = Get-Content -LiteralPath $expected -Raw | ConvertFrom-Json
    if ($record.token -ne $Session.token -or $record.output_directory -ne $Session.output_directory) {
        throw 'Output lease belongs to another worker'
    }
    return $record
}

function Remove-BlenderOutputLease([string]$StatePath, [string]$Path, [string]$Token) {
    $registry = Open-BlenderOutputRegistry $StatePath
    try {
        $record = Get-Content -LiteralPath $Path -Raw | ConvertFrom-Json
        if ($record.token -ne $Token) { throw 'Output lease belongs to another worker' }
        Remove-Item -LiteralPath $Path
    } finally {
        $registry.Dispose()
    }
}

function New-BlenderModellerAttempt($Session, [string]$WorkDirectory, [string]$ReferenceImage,
    [string]$Complexity, [string]$Model, [string]$ReasoningEffort, [string]$ServiceTier,
    [string]$CodexBinary, [string]$ResumeThread) {
    $directory = Join-Path $Session.run_root ("attempt-" + [guid]::NewGuid().ToString('N'))
    New-Item -ItemType Directory -Path $directory | Out-Null
    $configPath = Join-Path $directory 'run-config.json'
    $serverEnv = 'mcp_servers.blender.env={BLENDER_HOST="127.0.0.1",BLENDER_PORT="'+$Session.port+'",DISABLE_TELEMETRY="true",PYTHONUTF8="1"}'
    $arguments = @('--approve-for-me','-C',$WorkDirectory,
        '-m',$Model,'-c',('model_reasoning_effort="{0}"' -f $ReasoningEffort),'-c',('service_tier="{0}"' -f $ServiceTier),
        '-c',$serverEnv,'exec')
    if ($ResumeThread) { $arguments += 'resume' }
    $arguments += @('--skip-git-repo-check','-o',(Join-Path $directory 'last-model.md'))
    if ($ResumeThread) { $arguments += @('--',$ResumeThread,'-') }
    else { $arguments += @('-i',$ReferenceImage,'--','-') }
    @{args=$arguments;resume_thread=$ResumeThread;complexity=$Complexity;model=$Model;
      reasoning_effort=$ReasoningEffort;service_tier=$ServiceTier;executable=$CodexBinary;
      work_directory=$WorkDirectory;reference=$ReferenceImage;session_file=$Session.session_file;
      blender_process_id=$Session.process_id;blender_host=$Session.host;blender_port=$Session.port;
      token=$Session.token;started_utc=[DateTime]::UtcNow.ToString('o')} |
        ConvertTo-Json | Set-Content -LiteralPath $configPath -Encoding utf8
    @{attempt_directory=$directory;run_config=$configPath;session_file=$Session.session_file} |
        ConvertTo-Json | Set-Content -LiteralPath (Join-Path $WorkDirectory 'model-run.json') -Encoding utf8
    return @{directory=$directory;config_path=$configPath;arguments=$arguments}
}
