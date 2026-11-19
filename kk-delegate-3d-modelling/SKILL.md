---
name: kk-delegate-3d-modelling
description: Build or revise individual 3D game assets (props, weapons, characters, vehicles, modular kit pieces) in Blender, from a user-approved reference image through blockout, geometry, UVs, materials, textures and rig to a validated GLB plus editable .blend. Use whenever the user wants a 3D model made, remodelled, rigged, textured or exported for a game, including from a concept image or character turnaround, even if they don't mention Blender or MCP, and whenever several assets should be modelled in parallel. Each modeller runs in its own isolated live Blender process, so other Blender sessions stay untouched. Not for engine import, level placement, runtime materials or game logic; those belong to the project's integration workflow.
---

# Delegate 3D modelling

Two roles share this file:

- **Coordinator**: the chat the user is talking to. It gets the reference approved,
  writes the brief and worker prompt, launches an isolated modeller, reviews the
  result and closes the worker. Read everything except "Modeller requirements".
- **Modeller**: a CLI run started by the launcher. Its prompt begins with an
  identity preamble naming a PID, token and port. If that is you, read
  [Model phases](#model-phases), [Checkpoint and redo](#checkpoint-and-redo) and
  [Modeller requirements](#modeller-requirements), and skip the launch and close
  sections. Build the asset yourself; don't allocate workers or delegate further.

## Complexity and model settings

The coordinator picks a complexity for each launch from the actual modelling and
validation work. The launcher applies the settings to that run only, leaving the
user's Codex defaults intact.

| Complexity | Typical work | Model | Reasoning | Speed |
| --- | --- | --- | --- | --- |
| `simple` | Simple props, blockouts, small mesh edits | `gpt-6.1-terra` | High | Fast (`priority`) |
| `complex` | Detailed props, modular kits, routine rigged assets | `gpt-6.2-sol` | High | Normal (`default`) |
| `toughest` | Hero characters, difficult sculpts, complex deformation or reference matching | `gpt-6.2-astra` | High | Normal (`default`) |

Prerequisites: macOS with Python 3.9+, or Windows with PowerShell 7.4+; Codex CLI,
interactive Blender and the Blender MCP addon/server configured in Codex, plus the
separate global `blender-skills` pack. Start with its `blender-director/SKILL.md`,
`~/.agents/skills/references/reference-image-match.md` and the relevant specialist
skills.

## Scope

One worker builds one independently deliverable model in a dedicated output folder.
A model can have moving parts and companion meshes. Run batches as independent model
jobs. The deliverable is a staged asset package handed to the coordinator. The
downstream integration workflow owns runtime assets and manifests, engine imports,
level placement, game logic and in-game testing, so asset edits stay inside the
assigned model's folder.

## Model phases

Run phases in order and save a checked checkpoint before moving on. When a phase
doesn't apply, record why in its checkpoint and reference the last usable snapshot.

| Phase | Owner | Work and checkpoint acceptance |
| --- | --- | --- |
| 01 Brief and reference | Coordinator | Record intended viewing distance, style, metre dimensions, orientation, pivot, anchors, required movement, and geometry, material and texture budgets. State the runtime target explicitly: a triangle/material/texture budget for in-game use, or "review asset, no runtime budget" when fidelity matters more for now. Budgets left implicit tend to drift toward whatever the reference detail invites. Declare image maps by purpose or specify solid materials. Complete the user reference review below, write the reference analysis, and retain the inputs. The modeller adds its launcher record to this checkpoint. |
| 02 Blockout | Modeller | Match camera, primary masses and silhouette. Check proportions, scale, pivot and footprint using the modelling views below. |
| 03 Geometry | Modeller | Finish shapes, moving parts and topology. Check shading, mesh counts, dimensions and required attachment points. Prepare companion collision geometry when the brief calls for it. |
| 04 UVs | Modeller | Unwrap the surfaces that need images. Inspect a checker for distortion, seams, unintended overlaps and usable texel density. |
| 05 Materials | Modeller | Assign the palette and exportable surface properties. Check color, roughness, metalness and any required transparency or emission under review lighting. |
| 06 Textures | Modeller | Create, adapt or bake the maps declared in the brief. Check placement, seams, color space, resolution, and that images are bound to their intended material slots. Retain editable source images and pack or copy required dependencies. |
| 07 Rig and motion | Modeller | Build or preserve required rigs, pivots, skin weights and sockets. Inspect deformation or mechanical travel in representative Blender poses. Validate animation clips when the brief assigns them to this asset. |
| 08 Export and review | Modeller, then coordinator | Save the editable asset and staged GLB. Validate the actual exported structure, required maps, budgets and any rig or companion files. Compare finished Blender previews with the approved reference and complete the handoff report. The coordinator then reviews (see [Review and close](#review-and-close)). |

### User reference review

The user's approval of the exact image is what makes the rest of the work worth
doing. A model built from an unapproved or silently swapped reference usually has
to be redone.

1. Prepare the reference and inspect the actual image at a readable size. Check the
   requested views, design, proportions and important details. For a character
   turnaround, check silhouettes, pose, ground alignment and design consistency
   across panels.
2. Show the exact image or sheet to the user and ask them to approve it. Label
   multiple candidates so the user can identify their pick. When the user asks for
   changes, revise the reference and show the new version.
3. Wait for explicit approval of that version before starting a blockout,
   launching a modeller or making modelling changes through Blender MCP. Record the
   selected file or version and the user's approval in `APPROVAL.md` beside
   `reference_approved.png`. Reuse that approval while the same reference still
   applies; present any replacement for approval again.

### Modelling views and previews

Use front, left profile and back orthographic views as a starting point for
characters and detailed props. Keep comparable views at the same scale and pose,
aligned to a common ground line or other reference plane. Choose the views that
show the asset's shape and important features: two may be enough for a simple
symmetric prop; add the opposite side for an asymmetric feature or a top view when
the footprint matters.

Use a quick three-quarter viewport check during blockout when depth, curved
transitions or part fit need inspection. Include a three-quarter render alongside
the front view in the final preview package.

## Checkpoint and redo

- Save a new revision under `checkpoints/<phase>/rNN/` for each completed phase.
  Record the parent checkpoint, scene name, source and input versions, evidence and
  validation outcome in the checkpoint index. Keep approved references and imported
  or generated inputs with their provenance. The brief phase is documents and
  inputs. For Blender phases, write an asset-only `.blend` with
  `bpy.data.libraries.write()` through MCP. Pack asset-owned images or keep copies
  alongside the snapshot with working relative paths, and verify the saved scene
  and its dependencies load before relying on it.
- To redo a phase, start from the checkpoint just before it. Append only that
  snapshot's named asset scene into a fresh scene namespace via the verified live
  MCP session, switch the worker to it, and restore prior context afterwards. If
  restoring would interfere with the current scene, use a new owned worker. Check
  the restored scene, geometry and materials before changing anything.
- Keep earlier revisions intact, record the new parent and rerun dependent phases.
  A UV redo, for example, means rechecking material bindings, rebaking affected
  textures and validating a new export. Deliver only a package that passed review
  against the current checkpoint chain.

## Launch an isolated modeller

Each new asset or independent revision gets its own interactive Blender process,
MCP endpoint and output folder. This matters across chats and projects, not just
between subagents: native subagents inherit their parent's MCP routing, so giving
them different scenes or ports does not isolate them. Native agents can coordinate,
research and review, but only the CLI launcher routes a modeller to its own
Blender. [parallel-workers.md](references/parallel-workers.md) has the full
commands, identity checks, failure handling and cleanup.

1. Write `worker-prompt.md` in the output folder (see below).
2. Allocate one session per output folder: on macOS
   `python3 scripts/blender_worker.py allocate --output-directory <asset-folder>`;
   on Windows `scripts/New-BlenderWorker.ps1 -OutputDirectory <asset-folder>`.
3. Launch with the returned session file: on macOS `blender_worker.py run` with
   `--session-file`, `--prompt-file`, `--reference-image` and `--complexity`; on
   Windows `Invoke-BlenderModel.ps1` with `-WorkDirectory`, `-PromptFile`,
   `-ReferenceImage`, `-SessionFile` and `-Complexity`.

The launcher applies the model, reasoning effort, speed and MCP endpoint to that
run and prepends the identity check the modeller must pass before any mutation.

N independent jobs get N sessions; there is no application worker cap, only ports,
RAM, GPU memory and OS limits. One session takes one modeller at a time, so never
share an endpoint or output folder to squeeze in more concurrency.

The helper keeps normal sandboxing and automatic approval review. Launch may need
normal escalation to authenticate and start GUI processes. Don't widen the asset
scope, disable sandboxing, substitute models, or edit global MCP config or default
ports.

If the user explicitly needs an existing live scene, explain before substituting an
isolated copy. Writing to that shared endpoint requires a lease that **all** chats
respect; a queue inside one chat isn't enough. Stop and resolve ownership if another
writer or an endpoint identity change appears.

### Worker prompt

The modeller knows only the preamble, this skill and the prompt you write, so the
prompt decides most of the run's quality. Cover:

- The approved reference and `APPROVAL.md`, and the brief/reference-analysis path.
- What the asset is, in a sentence, and what matters most visually.
- Why any earlier attempt was rejected, so the modeller targets that gap rather
  than repeating it.
- Pose, scale and runtime target from the brief, including whether an old budget
  still applies.
- Input rules: permitted bases or downloads, licences and provenance to record,
  paid services to avoid, designs not to copy.
- Deliverables, and which parts (rig, retopology, LODs) may be labelled as limits
  rather than forced through.

[assets/example-worker-prompt.md](assets/example-worker-prompt.md) is a good
example from a character run.

## Modeller requirements

- Confirm the reference has documented user approval, and read the reference
  analysis and relevant specialist guidance before the blockout.
- Run the identity check from your preamble through the configured Blender MCP
  before any write, and save the result. On a mismatch or failed connection, stop
  and diagnose. Port 9876 and other endpoints usually belong to someone's unsaved
  scene, so reconnecting there to "make progress" can destroy their work.
- Model and review through live Blender MCP `execute_blender_code` and `look`. Don't
  fall back to background/headless Blender: viewport captures, `look` and render
  review need a real window context, and the visual review is the point of the run.
- Work in dedicated scenes, collections and materials. Don't reset the session,
  open another file over it, purge globally, change preferences or run a legacy
  script's destructive startup. Downloaded and AI-generated meshes are fine when
  they fit the brief and project requirements.
- Match camera and silhouette early, compare screenshots and correct the largest
  gaps first. Complete at least one visual review round before acceptance and
  repeat as needed to meet the brief; this overrides iteration limits in the
  reference-matching guide. Keep gameplay anchors and declared budgets.
- Export only the selected asset/rig in its active scene. For glTF, pass both
  `use_selection=True` and `use_active_scene=True`: selection alone can pull in a
  selected baseline object from another scene. Parse the exported GLB's actual
  scene roots, nodes and meshes rather than inferring contents or triangle counts
  from the source collection. Join game meshes where appropriate, keeping real
  skin weights. After positioning the final review camera, save a separate blend
  containing only the asset scenes and dependencies.
- Deliver reproducible source, the editable blend, texture sources when used, the
  staged GLB, front and three-quarter previews, the checkpoint index and
  `REPORT.md`. Report actual counts, dimensions, texture slots and resolutions, rig
  or socket details, whether the runtime target was met, deviations, MCP identity
  evidence and preservation checks, and what the downstream integrator needs.
- Keep PID/token/port values in per-run metadata, not in geometry source. Confirm
  the requested model settings from the launch record rather than demanding an
  internal model-identity attestation.

## Review and close

Inspect the actual previews and GLB structure, compare them with the reference,
and use checkpoints to redo any phase that needs it. Acceptance covers the
individual model package; the downstream workflow reviews it in game context.

Check the required outputs before accepting a modeller's final response. If it
stopped at planning without a blocker, resume its thread in the same live session
with `--resume-thread` (macOS) or `-ResumeThread` (Windows), naming the latest valid
checkpoint and the missing deliverables. Keep retries proportional to the remaining
work and real failures. Stop and diagnose any crash or identity mismatch.

After saving and validating the wanted outputs, close only that owned process: on
macOS `blender_worker.py stop --session-file <session> --exports-validated`; on
Windows `Stop-BlenderWorker.ps1 -SessionFile <session> -ExportsValidated`. Keep
output files and logs. Never kill other Blender processes or recover unsaved user
scenes automatically. After a crash, release the dead worker's reservations before
allocating a fresh worker from the latest saved checkpoint: on macOS run
`blender_worker.py recover --session-file <session>`; on Windows, once the Blender
process is confirmed gone, run `Stop-BlenderWorker.ps1 -SessionFile <session>
-ExportsValidated`, which releases the leases without signalling any process.
