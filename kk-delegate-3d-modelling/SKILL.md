---
name: kk-delegate-3d-modelling
description: Create or revise 3D models with GPT-6.1 Terra at medium effort and Fast priority requested, using blender-skills, approved ChatGPT references and isolated live Blender MCP workers. Supports parallel modelling through separate Blender processes and endpoints.
---

# Delegate 3D modelling

The coordinator directs and reviews; an explicitly assigned modeller builds the asset
itself without recursively delegating. Use `gpt-6.1-terra`, medium reasoning and
`service_tier="priority"` per run. Do not change the user's default model. Priority
is a requested configuration, not a guarantee of latency.

Prerequisites: Windows, PowerShell 7.4+, Codex CLI, interactive Blender and the
Blender MCP addon/server configured in Codex. Install the separate `blender-skills`
pack before use; it is not bundled here. The local skill may also be installed
as `delegate-3d-modelling`; this package uses the repository namespace.

Use the global `blender-skills` pack. Start with `blender-director/SKILL.md`,
`blender-director/references/reference-image-match.md`, and the relevant specialist skills.

## Reference and scope

Write a brief with purpose, style, metre dimensions, pivot, rig/interaction anchors,
triangle/material budgets and outputs. Generate a ChatGPT reference, inspect it,
and record the coordinator's visual approval in `APPROVAL.md` beside
`reference_approved.png`. An existing generated reference with documented approval
may be reused. This is art review, not another user permission request. If three
reference attempts fail, show the best and explain the remaining issue.

Keep each worker in a dedicated output folder with its own prompt and source.
Workers stage assets; the coordinator reviews and integrates shared files such as
runtime GLBs and manifests. Preserve pre-existing edits and user scene data.

## Isolated live worker launch

For new assets and independent revisions, use a separate interactive Blender process
per worker. Read [parallel-workers.md](references/parallel-workers.md) for commands,
endpoint identity checks, failures and cleanup. This applies across chats/projects,
not merely to subagents in one chat.

1. Run `scripts/New-BlenderWorker.ps1 -OutputDirectory <asset-folder>`.
2. Read its ready session record; run `scripts/Invoke-BlenderModel.ps1` with
   `-WorkDirectory`, `-PromptFile`, `-ReferenceImage`, and **`-SessionFile`**.
3. The launcher requests Terra/medium/priority and overrides only that CLI run's
   Blender MCP endpoint. Its worker must verify live PID, token, actual server port
   and `bpy.app.background == False` through MCP before any mutation.

Different sessions may run simultaneously. Native subagents inherit their parent's
MCP configuration; assigning different scenes or telling them to use another port
does not reroute their tools. Use the configured CLI helper for isolated modellers.
Native agents can coordinate, research and review without touching shared Blender.

The helper keeps normal sandboxing and automatic approval review. Launch may need
normal escalation to authenticate and start GUI processes. Do not widen the asset
scope, disable sandboxing, substitute models, or edit global MCP config/default ports.

If the user explicitly needs an existing live scene, do not substitute an isolated
copy without explaining the change. That endpoint requires a lease respected by
**all** chats/writers; a queue in one chat is insufficient. Stop and resolve ownership
if another writer or an endpoint identity change is detected.

## Modeller requirements

- Read this skill in modeller mode, the approval, reference analysis workflow and
  relevant specialists; write Reference Analysis before building.
- Use actual live Blender MCP `execute_blender_code` and `look` for modelling and
  viewport/render review. Never fall back to background/headless Blender. Diagnose
  failed connections and identity checks; never reconnect silently to port 9876.
- Create dedicated scenes/collections/materials. Do not reset the running session,
  open another file over it, purge globally, change preferences, or execute a legacy
  script's destructive startup. `--factory-startup` is used only when the helper
  launches a new owned GUI process. No downloaded or AI-generated meshes.
- Match camera and silhouette early; compare screenshots and correct the largest
  gaps, up to three review rounds. Keep gameplay anchors and declared budgets.
- Export only the selected asset/rig in its active scene, without unrelated content.
  For glTF use both `use_selection=True` and `use_active_scene=True` explicitly:
  selection alone can include a selected baseline object from another scene.
  Parse the exported GLB's actual scene roots, nodes and meshes; do not infer its
  contents or triangle count from the source collection alone.
  Join game meshes where appropriate, retaining real skin weights. Save a separate
  blend containing only the asset scenes and dependencies after positioning the
  final review camera.
- Deliver reproducible source, blend, GLB, front/three-quarter previews and REPORT.md
  with actual counts, dimensions, deviations, MCP identity/execution evidence and
  preservation checks. Disclose failed attempts and remaining errors. Do not claim
  engine integration tests that were not run.

## Review and close

Inspect actual previews and GLB structure, compare the reference, and request concrete
revisions when needed. Validate engine import, labels and relevant gameplay when
integrating. A successful export alone does not prove correct animation or interaction.

After saving and validating wanted outputs, close only that owned dedicated process
with `scripts/Stop-BlenderWorker.ps1 -SessionFile <session> -ExportsValidated`.
Keep output files and logs. Never kill other Blender processes or recover unsaved
user scenes automatically. A crash ends the lease; diagnose before any new writes.
