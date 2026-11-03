# Game Idea Critic — Scoring rubric

Use for a requested score, deep review, or fair side-by-side comparison. The score is a **decision aid, not a probability of success**. It measures the currently articulated concept. Display scores to the nearest integer only; never assert numerically precise chances of commercial success.

## Common weighted rubric

| Criterion | Weight | What a high score requires |
|---|---:|---|
| Player promise and clarity | 10 | Concrete player fantasy, understandable role and immediate objective; not just genre keywords |
| Core interaction and feedback | 20 | An interesting primary action, legible response, meaningful agency / skill / interpretation, and a reason to repeat or continue |
| Distinctiveness of the rule | 15 | A demonstrable mechanical or experiential difference, not just theme, art, or stacked genres |
| Depth or authored payoff | 10 | Replayable games: viable decisions, emergent possibilities; authored games: pacing, revelation, craft, narrative or mastery payoff |
| Experience cohesion | 10 | Setting, systems, pacing, story, sound and rewards support the intended feeling |
| Visual and UX identity | 10 | Recognizable presentation that also communicates state and affordances; aesthetics feasible for production |
| Audience and discoverability | 10 | Identifiable player audience, honest hook for trailer/store page, plausible reason to choose it over close alternatives |
| Feasibility under constraints | 10 | Scope plausible for the actual team/AI workflow, tech, platform, QA and content budget |
| Fastest useful validation | 5 | Central claim can be tested inexpensively with a small playable slice and falsification criteria |
| **Total** | **100** | |

### Anchors for each criterion

- **0/4 — Missing or contradictory:** no plausible mechanism/value is shown, or conflicts with a hard constraint.
- **1/4 — Weak:** generic, loosely asserted, depends on too many unproven systems, or a clear failure mode dominates.
- **2/4 — Plausible:** coherent on paper but ordinary or too many uncertainties remain.
- **3/4 — Strong:** specific, differentiated, credible and testable, albeit not yet demonstrated.
- **4/4 — Exceptional evidence:** unusually coherent and distinctive, with directly relevant playable or market evidence **where that evidence applies**. Creative excellence cannot be confirmed merely through a pitch.

**Calculation:** `weighted score = sum(weight × rating / 4)` across all criteria. Do not round intermediate results. Avoid `N/A` by selecting the intended style (e.g. authored payoff instead of replayability). If a category truly does not apply, explicitly state why and normalize remaining weights to 100.

**Confidence:** `High` requires direct playtest/observed evidence across core interaction and production assumptions; `Medium` means concrete rules and relevant precedents, but no meaningful playtest; `Low` means high-level pitch only. Concept strength and evidence confidence must be separate. "Exceptional" in one dimension does not require a shipped game, but it must have unusually convincing supporting material rather than hype.

## Critical blockers overriding averages

Flag separately regardless of score:

1. **No core verb:** player can't do anything interesting without progression rewards or content volume.
2. **Unresolved feature soup:** main systems don't affect each other; no coherent minute-to-minute game.
3. **Dominant strategy destroys variety:** rational play is repetitive and eliminates meaningful choice.
4. **Scope inversion:** the difficult/expensive features are prerequisites for testing the hook.
5. **Unshippable at stated constraints:** the concept inherently requires quality assurance, art, tech, or content capacity that the available process cannot support.
6. **Monetization conflict:** a proposed business model undermines the core promise or relies on unsupported assumptions.

A paper idea **never receives a full production go-ahead** on the basis of score. Numerical bands can guide *triage* but do not replace blockers or confidence. As optional shorthand: ~75+ suggests prioritizing prototype exploration; ~55–74 needs targeted redesign or evidence; below ~55 likely needs a new core proposition. Do not treat these bands as proven industry statistics.

## Comparison mode

Score every candidate using the same rubric and the same **goal and assumptions**. Then show:

- **Best next prototype**: achievable test cost, differentiated core, fastest evidence.
- **Highest upside**: strong possible audience effect with acknowledged risk.
- **Biggest trap**: the idea that looks good visually or on a feature list but fails in play.

If changing player segment, price model, or genre between candidates, explain the mismatch rather than pretend numbers are directly comparable. Offer a ranking with short causal explanations and propose the one test most likely to reverse that ranking.

## Context-specific lenses (do not automatically add score points)

- **Short narrative / psychological horror:** pacing, atmosphere, readable stakes, emotional integration, surprise with thematic meaning; do not penalize limited replayability.
- **City builder / management:** conflict between scarce resources, consequences after multiple cycles, comprehensible causal simulation, prevention of solved build orders.
- **Roguelike / card game:** combination diversity, viable different builds, interesting adaptations, visible counterplay, avoidance of degenerate dominant strategies.
- **Collection / incremental / pack opening:** reveal is only the beginning; ownership changes player decisions or the world; redundant unlocks, empty randomness and progression pacing are hazards.
- **Precision action / platformer:** expressive controls, frictionless restarts, skill ceiling, and motion polish outweigh systemic complexity.
- **Atmospheric puzzle / mystery:** quality of inference, novelty of the player's knowledge, rule consistency, and payoff outweigh action density.
- **F2P mobile:** touch-first readability, session cadence, organic retention from real play, ethical optional monetization, accessibility, and distribution.
- **Premium PC / Steam:** sufficient differentiated value and an honest store/trailer promise without importing mobile economies by default.
