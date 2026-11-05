"""Start the installed official addon in a NEW interactive worker process only."""
import importlib.util
import json
import os
import sys
import time
import traceback
from pathlib import Path
import bpy

session_path = Path(sys.argv[sys.argv.index('--') + 1]).resolve()
session = json.loads(session_path.read_text(encoding='utf-8-sig'))

def publish(path, value):
    path = Path(path)
    temporary = path.with_name(path.name + '.' + str(os.getpid()) + '.tmp')
    temporary.write_text(json.dumps(value, indent=2), encoding='utf-8')
    for attempt in range(20):
        try:
            os.replace(temporary, path)
            return
        except PermissionError:
            if attempt == 19:
                raise
            time.sleep(.05)

try:
    launch_path = Path(session['run_root'], 'launch.json')
    deadline = time.monotonic() + 5
    while not launch_path.exists() and time.monotonic() < deadline:
        time.sleep(.05)
    launch = json.loads(launch_path.read_text(encoding='utf-8-sig'))
    if launch['process_id'] != os.getpid():
        raise RuntimeError('Launch PID ownership mismatch')
    session['process_started_utc'] = launch['process_started_utc']
    if bpy.app.background or bpy.context.window is None:
        raise RuntimeError('An interactive Blender process is required')
    if Path(os.environ.get('BLENDER_USER_CONFIG', '')).resolve() != Path(session['run_root'], 'config').resolve():
        raise RuntimeError('Worker config directory is not isolated')
    if session['port'] == 9876 or session['host'] != '127.0.0.1':
        raise RuntimeError('Worker must use a dedicated loopback endpoint')
    if getattr(bpy.types, 'blendermcp_server', None) is not None:
        raise RuntimeError('Unexpected pre-existing server in fresh worker')
    spec = importlib.util.spec_from_file_location('blender_mcp', session['addon_path'])
    addon = importlib.util.module_from_spec(spec)
    sys.modules['blender_mcp'] = addon
    spec.loader.exec_module(addon)
    addon.register()
    # All changes here affect this newly launched, separately configured process.
    for scene in bpy.data.scenes:
        scene.blendermcp_auto_start_server = False
        scene.blendermcp_port = session['port']
    server = addon.BlenderMCPServer(host=session['host'], port=session['port'])
    bpy.types.blendermcp_server = server
    server.start()
    if not server.running:
        raise RuntimeError('Dedicated MCP socket failed to start')
    bpy.context.scene.blendermcp_server_running = True
    bpy.context.scene.name = 'Worker sandbox ' + session['token'][:8]
    bpy.context.scene['codex_worker_token'] = session['token']
    bpy.app.driver_namespace['codex_worker_token'] = session['token']
    bpy.app.driver_namespace['codex_worker_port'] = session['port']
    session.update(status='ready', process_id=os.getpid(), background=False,
                   initial_scene=bpy.context.scene.name, blender_version=bpy.app.version_string,
                   baseline_objects=sorted(o.name for o in bpy.data.objects))
    publish(session['lease_file'], session)
    publish(session_path, session) # Publish readiness only after registry completion.
    print('CODEX_WORKER_READY', json.dumps(session), flush=True)
except Exception:
    session.update(status='failed', process_id=os.getpid(), error=traceback.format_exc())
    publish(session['lease_file'], session)
    publish(session_path, session)
    traceback.print_exc()

