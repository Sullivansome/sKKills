# Dedicated live Blender workers

Allocate one interactive Blender GUI process, one MCP endpoint and one output folder
for each independent modeller. In the examples, set `skill` to wherever this skill is
installed; the paths shown are only common locations. Native subagents share inherited MCP routing; use these
CLI launchers to route each modelling run. Separate scenes in one process do not isolate
active context, selection or render state.

Before launching a modelling run, verify that the user approved the exact
reference image and that `APPROVAL.md` records the approval. Follow the
[user reference review](../SKILL.md#user-reference-review) for new or revised references.

## macOS

Requires Python 3.9+, interactive Blender, the installed Blender MCP addon, and a working
Codex `blender` MCP server definition. The launcher discovers standard Blender/addon
locations; use `--blender-executable` and `--addon-path` on `allocate` for other installs.
It does not run Blender headless to discover paths. It launches a new GUI process with
`--factory-startup` only for that new owned process; `bpy.app.background` must be false.

```sh
skill="$HOME/.agents/skills/kk-delegate-3d-modelling"   # adjust to your install
mkdir -p /path/to/project/art/source/asset-a
python3 "$skill/scripts/blender_worker.py" allocate \
  --output-directory /path/to/project/art/source/asset-a
# Use the returned session_file for both commands below.
python3 "$skill/scripts/blender_worker.py" run \
  --session-file /path/from/allocate/session.json \
  --prompt-file /path/to/project/art/source/asset-a/worker-prompt.md \
  --complexity simple \
  --reference-image /path/to/project/art/source/asset-a/reference_approved.png
# Only after inspecting and validating wanted exports:
python3 "$skill/scripts/blender_worker.py" stop \
  --session-file /path/from/allocate/session.json --exports-validated
```

Inventory existing job/session records before allocating; resume an existing job instead
of creating a duplicate writer. The CLI prints `session id:` in the attempt `stderr.log`;
`model-run.json` in the output folder points to that attempt and captured configuration.
Use that thread ID when continuing.

To continue an incomplete modeller, use the same `run` arguments and complexity with
`--resume-thread <CLI-session-id>` and a prompt naming the checkpoint and missing work.
A resume rechecks the owned Blender identity and retains earlier attempt logs.

## Windows

Requires PowerShell 7.4+ (`Start-Process -Environment`), installed Blender/MCP, and Codex.
Pass `-BlenderExecutable` and `-AddonPath` when they differ from the helper defaults.

```powershell
$skill = "$env:USERPROFILE/.codex/skills/kk-delegate-3d-modelling"   # adjust to your install
& "$skill/scripts/New-BlenderWorker.ps1" -OutputDirectory 'D:/project/art/source/asset-a'
& "$skill/scripts/Invoke-BlenderModel.ps1" `
  -WorkDirectory 'D:/project/art/source/asset-a' `
  -PromptFile 'D:/project/art/source/asset-a/worker-prompt.md' `
  -ReferenceImage 'D:/project/art/source/asset-a/reference_approved.png' `
  -Complexity simple `
  -SessionFile 'C:/Users/<user>/.codex/blender-workers/<token>/session.json'
# After validating wanted outputs:
& "$skill/scripts/Stop-BlenderWorker.ps1" -SessionFile '<session.json>' -ExportsValidated
```

To continue, read the `session id:` in the previous attempt's `stderr.log` and add
`-ResumeThread '<CLI-session-id>'` to the same `Invoke-BlenderModel.ps1` command.
`-WorkDirectory` must be the session's recorded output folder; the launcher rejects a mismatch.
Keep its session and complexity and supply a continuation prompt naming the checkpoint
and missing work. Each attempt has its own `run-config.json`, `stdout.log`,
`stderr.log`, and last response. The output folder's `model-run.json` points to the latest
attempt. For a run started by the previous launcher, look in its `codex-model.log`
for the thread ID.

## N simultaneous jobs

There is no fixed application worker-count cap. For N independent jobs, allocate N
sessions in distinct output folders, then start their N `run`/`Invoke-BlenderModel.ps1`
commands concurrently using the coordinator's process runner. A shell loop or process
pool can launch any requested positive N; choose concurrency that the machine can run.
A batch may finish or fail per job: retain session records, report partial results and
close only validated owned jobs. Do not label unstarted/failed allocations complete.

The default candidate pool starts at 19876, scans through 65535, then wraps through
1024–19875, always excluding shared port 9876. Existing listeners and existing lease
files are skipped, never displaced. This removes the old 100-port default pool and
200-port argument ceiling. Ports are finite: with resource exhaustion, report the
specific allocation failure and release only confirmed owned reservations. Stale leases
are skipped, not stolen. Explicit port-pool limits, when supplied, are user constraints.

All chats should use the same default registry `~/.codex/blender-workers`; custom state
roots must be shared by cooperating launchers. Atomic files under `ports/` reserve
endpoints before Blender startup. Each token directory holds the session record,
isolated config/scripts/datafiles, bootstrap logs and worker ownership metadata.
Both launchers lease output folders under a registry lock and reject equal or nested
folders, including filesystem aliases. Windows also checks output folders recorded
by earlier versions that reserved only a port.

## Identity and ownership

Each session records host, actual assigned port, PID, process creation identity, random
token, output directory and isolated config directory. The bootstrap stores the token
in Blender's driver namespace. Launchers check the PID, executable/launch arguments,
listener ownership, registry identity and session lock before reuse or cleanup. They
record a modeller child's PID/birth identity before sending its prompt; a still-live
child continues to own the session even if its wrapper exited.

Each launcher requires the complexity for the run and applies the model, high reasoning
effort and service tier listed in [SKILL.md](../SKILL.md). It overrides that run's
`mcp_servers.blender.env`, retaining the installed server command. Different MCP names,
coordinator environment variables alone, or separate scenes do not prove routing.
Before writes the modeller must call `get_addon_status` and execute the supplied
PID/token/actual-server-port/background assertion through that configured MCP tool.
Persist the returned values. On mismatch, stop: never adjust the other endpoint to
make it pass or silently reconnect to port 9876. Source scripts load current session
metadata rather than baking one run's PID/token into the geometry recipe.

GUI worker windows may be visible on macOS. They remain interactive processes with
real window/context; MCP viewport/camera captures and renders are required. Hidden
Windows windows are likewise interactive, not background/headless Blender.

## Test and cleanup

Run the PowerShell launcher regression checks from the skill folder with
`pwsh -NoProfile -File tests/test_blender_worker_windows.ps1`. Run them on Windows
to exercise native folder normalization and junction handling.

For a concurrency test, use at least three independent workers and log actual
build/render start/end times and PID/port/token inside each process. Coordinate a start
barrier. Report measured interval overlap and the tested worker count; launching N
CLIs alone proves neither simultaneous Blender execution nor unbounded capacity.
Inspect every output, verify each GLB's actual nodes/meshes/rig, and check that each
worker preserves its initial Cube/Camera/Light and marker scene. Confirm unrelated
Blender processes and global MCP configuration are preserved.

After saving and validating wanted outputs, use the platform's stop command. It refuses
active modeller ownership, verifies identity again, closes only the owned process,
releases its lease and retains evidence. A new instance cannot recover unsaved data
from a crashed session. Never open autosaves over user scenes or kill other processes.
After a previously ready worker crashes, release its output and port reservations.
On macOS run `blender_worker.py recover --session-file <session>`. Recovery checks the recorded process identity, modeller lock and
loopback port. It leaves the files and diagnostics in place and can be rerun if cleanup
was interrupted. On Windows, confirm the Blender PID is gone, then run
`Stop-BlenderWorker.ps1 -SessionFile <session> -ExportsValidated`: with no live owned
process it marks the session closed and releases only leases carrying its token. It
still refuses a live modeller child or a PID whose identity changed.
Allocate a new session before continuing from a saved checkpoint.

If bootstrap fails before the worker is ready, inspect the session record and Blender
logs. When automatic cleanup retained a reservation, release it manually only after
confirming the process is dead, the endpoint is unused, and the reservation belongs
to that worker. Never recursively delete the registry.
