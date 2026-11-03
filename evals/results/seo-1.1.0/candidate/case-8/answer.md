The supplied totals do not show that skill 1.0.0 is better. Classification: invalid version comparison; gather evidence.

Illustrative arithmetic from the synthetic counts (not a validated experiment):

| Group | Pages | Before → after clicks, each 28 days | Change | Clicks/page/day before → after |
|---|---:|---:|---:|---:|
| Treatment | 10 | 100 → 140 | +40, +40% | 0.3571 → 0.5000 |
| Unchanged control | 20 | 200 → 280 | +80, +40% | 0.3571 → 0.5000 |

Treatment relative change = (140−100)/100 = 40%; control = (280−200)/200 = 40%. Size-normalized difference-in-differences = [(140−100)/(10×28)] − [(280−200)/(20×28)] = 0 clicks/page/day. Equivalently both rose 4 clicks/page, yielding zero differential change. This is descriptive arithmetic; it neither proves an effect nor proves no effect.

The bundled checker was run on normalized files and stopped at the empty cohort file: exact URL membership was not supplied, so no comparisons were produced. Independently, calendar periods, timezone/extraction provenance, deployment revision/time, and package identity are also missing. Unknowns were left blank; see execution.log. The raw export is preserved. Its complete-data label does not repair missing experimental provenance.

No pre-trends or randomization evidence supports the control assumptions. Clicks are not sessions, conversions or profit; those outcomes and costs are unknown. An unchanged control tests an intervention, not the prior skill. A version label without a recoverable hash/snapshot cannot identify the exact package.

Next: retrieve raw dated exports and page membership, deployment records and recoverable skill packages; inspect comparability, pre-trends and concurrent changes. To assess versions, run matched held-out tasks with prior/candidate packages under identical inputs, tools and settings, then compare matched deployed interventions with useful-action guardrails. Do not declare a winner from this export.
