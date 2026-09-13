# Review assessment and namespace change

Date: 2026-09-13. The review was checked against the repository at commit `45b6576` before edits. Its core findings are useful; some claims are risks or opinions rather than demonstrated failures.

| Suggestion | Assessment | Action |
|---|---|---|
| TanStack detector uses unscoped package names | Confirmed defect: the table could confuse React Router or legacy React Query with TanStack | Match complete scoped package names; make Query-only and file-based routing conditions explicit |
| Generic Go routes through a Wails document | Confirmed ambiguity, not proof every agent would misroute | Extract generic `references/go.md`; Wails reuses it only for its backend |
| Implementation skill will steal most coding requests | Unproven prediction | Narrow the description and clarify the lead by requested operation; both original and revised catalogs matched 24/24 smoke-test labels |
| Bootstrap always teaches tag/GitHub artifact releases | Confirmed scope inconsistency between the entrypoint and references | Make release setup conditional on the requested deliverable, preserving service providers/triggers |
| Release eval prompt is a harness instruction | Confirmed | Put the realistic scenario directly in the prompt field; retain the source fixture |
| Bootstrap cases lack grading expectations | Confirmed for original cases 0–5 | Add expectations to each; validator rejects absent or empty expectations |
| Too few fixtures | Fair gap for tasks that claim repository-grounded evidence | Add four focused raw fixture cases; no claim that all existing cases now have runnable projects |
| No trigger/selection evals | Confirmed | Add 24 positive/negative lead-selection cases and independent original/revised description passes |
| “25/27” cases are unrun | Under-testing concern is valid; that exact count is unsupported | The initial record describes one scenario run in two conditions, not two separate suite cases; keep task execution separate from selection checks |
| Deduplicate all cross-cutting instructions | Only partly advisable | Keep short local rules needed for standalone use; deduplicate Go tooling and add routing guidance without mandatory sibling dependencies |
| Tagged CI templates can be copied without pinning | Valid risk, not an existing production-policy violation | Retain clearly labeled adaptation templates and their pinning instructions; the collection's real validation workflow remains SHA-pinned |
| Validator does not prove quality | Correct | Extend structural checks and regression tests, while keeping the claim explicitly limited to packaging and schema properties |

The review also says bootstrap is the only skill needing reference splitting. Operations and evolution already use conditional incident/migration/retirement references; keeping those is appropriate.

## Routing semantics

Select by the requested operation and the next unresolved decision, not just domain keywords. A specified authorization bug fix can lead with `kk-ai-implementation` and consult security guidance; a request to threat-model abuse paths leads with `kk-security-review`. Review-only correctness work leads with verification. Active incidents lead with operations; existing-consumer transitions with evolution; model/RAG behavior evaluation with AI evaluation.

The collection is not an exclusive classifier. More than one skill can be useful, and installed external specialists may be better for a specific stack. The routing smoke test measures a lead choice within this collection only.

## Personal namespace

All eleven directories and frontmatter names now start with `kk-`. Router references, eval identifiers, resource links, tests, CI paths, and documentation use the new names. Validation rejects an unprefixed name. Existing local bootstrap installation symlinks were renamed and retargeted to preserve their functionality; unrelated third-party skills were not renamed and previously uninstalled collection skills were not installed automatically.

This is an intentional identifier change. Other installations using old names must migrate their links or reinstall the chosen `kk-` skills and remove obsolete copies. Historical evaluation prose uses current names for navigation; it does not imply the old evaluations were rerun under renamed or revised skills.
