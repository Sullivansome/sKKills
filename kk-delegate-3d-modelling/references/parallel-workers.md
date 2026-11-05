# Dedicated live Blender workers

These Windows helpers start non-headless Blender GUI processes with separate user
config/script/data directories, using the installed official Blender MCP addon.
They do not modify the user's existing Blender processes or global MCP configuration.

```powershell
$skill = "$env:USERPROFILE/.codex/skills/kk-delegate-3d-modelling"
# Create the dedicated asset folder before allocating its session.
& "$skill/scripts/New-BlenderWorker.ps1" -OutputDirectory 'D:/project/art/source/asset-a'
# Copy the returned session.json path into the next command.
& "$skill/scripts/Invoke-BlenderModel.ps1" `
  -WorkDirectory 'D:/project/art/source/asset-a' `
  -PromptFile 'D:/project/art/source/asset-a/worker-prompt.md' `
  -ReferenceImage 'D:/project/art/source/asset-a/reference_approved.png' `
  -SessionFile 'C:/Users/<user>/.codex/blender-workers/<token>/session.json'
```

The default port pool is 19876–19975. Atomic registry files under
`~/.codex/blender-workers/ports/` reserve ports across chats. Existing listeners and
existing lease files are skipped, never displaced. Session records include host,
port, PID, random token, output directory and isolated config directory. The addon
bootstrap stores the token in Blender's driver namespace. Per-session file locks
prevent two launcher processes from using the same session concurrently.
The launcher also records the Codex child's PID and creation time before sending
its prompt; reuse and cleanup refuse a still-live child even if its wrapper died.
Run these helpers in PowerShell 7.4 or newer (`Start-Process -Environment` is used).

Run a second allocation and launcher for another asset to work in parallel. The
launcher uses a per-run `-c mcp_servers.blender.env={...}` override retaining the
installed server command. This routes that CLI's `blender` tools to its dedicated
port. Different server names alone, environment variables on the coordinator alone,
or different scenes do not prove client routing.

Before writes the worker must get addon status and execute the launcher's PID/token/
actual-server-port/background assertion through the configured MCP tool. Record the
response. On a mismatch, stop; never edit the other process to make the assertion
pass. No model process may use the coordinator's inherited shared Blender endpoint.

The normal GUI worker window starts hidden to avoid interrupting the user. It still
has a real interactive window/context and `bpy.app.background=False`; MCP camera/
viewport captures and renders are required. This is not background/headless Blender.

For a parallelism test, use two independent model source scripts and log actual
build/render start/end times and PID/port/token inside each Blender process. Coordinate
a start barrier and report the measured overlap, rather than assuming simultaneous
CLI launch proves concurrent Blender execution. Inspect both previews and assert that
each output/scene contains only its own model and untouched baseline sentinels.

After completion, verify saved exports before cleanup:

```powershell
& "$skill/scripts/Stop-BlenderWorker.ps1" -SessionFile '<session.json>' -ExportsValidated
```

Cleanup validates the token, registry record and PID's executable/launch command,
and refuses an active modeller lock. It closes only its owned process, releases its
port lease and retains files. A new instance is not a recovery of an unsaved crashed
session. Do not open autosaves over user scenes or close unrelated Blender windows.

If bootstrap fails, inspect that run's session status and stdout/stderr logs. A stale
lease is skipped automatically, not stolen. Confirm its PID is dead and its port is
unused before manually removing exactly that verified lease. No recursive cleanup.
