# Worked traffic pilot (synthetic)

All dates, revisions, fingerprints, records, and outcomes here are fictional. The all-a fingerprint is a placeholder, not a real release identity. This fixture demonstrates mechanics and supplies no evidence of live traffic growth. Copy the blank templates for real work; never reuse this fixture's identifiers as provenance.

The proposed intervention is improved topic navigation on one existing resource. Two unchanged resources form a descriptive comparison group. [Experiment ledger](experiments.csv), [fixed membership](cohorts.csv), [raw counts](raw-counts.json), and [normalized observations](observations.csv) connect the deployment to the measurement. Raw page clicks are summed within each fixed group; no query rows or property totals are mixed in. Timezone/date fields are illustrative, not assertions about a provider's native export timezone.

From the repository root:

```bash
python3 kk-seo-growth/scripts/validate_traffic.py --observations kk-seo-growth/examples/traffic-pilot/observations.csv --cohorts kk-seo-growth/examples/traffic-pilot/cohorts.csv --experiments kk-seo-growth/examples/traffic-pilot/experiments.csv
```

Expected validation: valid, no warnings, two descriptive comparisons. Treatment clicks rise 100 to 140 (+40, +40%); control clicks rise 200 to 280 (+80, +40%). Both periods contain 28 days. Treatment has one page and control has two, so both go from 100 to 140 clicks per page per period. The illustrative additive adjustment at that grain is (140−100)−(140−100)=0. Comparing unnormalized total changes would incorrectly suggest −40.

**Decision: inconclusive; gather evidence.** The common trend does not demonstrate incremental benefit. There are no pre-trend series, randomized assignment, task-completion counts, or implementation-cost observations. No claim about conversions or superiority over another skill version is justified. Keep the deployment record, inspect comparable prior periods, and obtain useful-action evidence before expanding the intervention. Do not choose a different date window just to obtain a lift.

For a zero copied from an export that may encode unavailable values, preserve the raw zero, set normalized value blank and status missing, and explain the ambiguity in notes. The checker should then withhold that pair's comparison. A confirmed zero requires zero_evidence=observed and a zero_evidence_ref pointing to corroborating evidence. A complete zero without this provenance is rejected.
