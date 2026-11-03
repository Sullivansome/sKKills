# Versioned skill and traffic evaluation

Use this reference when releasing the skill or implementing/evaluating SEO changes whose outcomes will be compared. Keep ordinary reviews and narrow fixes proportionate; do not require analytics setup for an unrelated edit.

## Identify and preserve the skill

[VERSION](../VERSION) is the release label; [CHANGELOG.md](../CHANGELOG.md) defines version increments. The package SHA-256 identifies the exact file contents, including references, assets, scripts, and evaluations. A version label alone cannot distinguish local edits.

Use the Python 3.9+ standard-library helper:

```bash
python3 <skill-dir>/scripts/skill_release.py identity
python3 <skill-dir>/scripts/skill_release.py verify --registry <release-registry>
python3 <skill-dir>/scripts/skill_release.py snapshot --registry <release-registry> --out <project-evidence-dir>/kk-seo-growth-1.1.0.zip
```

Use the actual VERSION in archive names. Identity reports `released`, `modified-release`, `unregistered`, or `development`. A stable package must match a saved registry entry before it can be snapshotted; a copied standalone package needs an explicit registry path. Use `major.minor.patch-dev.N` for work in progress; it must not be presented as a stable release. The repository validator verifies archived releases and requires stable working contents to match their registered fingerprint; it permits an explicitly labeled development version. The explicit [PACKAGE_FILES.json](../PACKAGE_FILES.json) lists every bundled file. Review new entries rather than auto-adding all files during release; unexpected files and missing declared files stop packaging before their contents are read. This controls file inclusion, not secrets accidentally written into a declared file. The helper hashes sorted relative paths and their file hashes, ignores Python caches and OS metadata, rejects internal symlinks, and writes an archive containing the package and release manifest. It refuses to overwrite an existing archive. A matching hash proves content identity, not quality or publisher authenticity. Store the snapshot outside the skill folder with the site's experiment evidence; existing matching release archives can be reused. Do not edit released archives. Preserve raw exports in an access-appropriate project location, not inside this reusable skill or a public repository.

When changing released guidance, set a new development VERSION and describe the change. Validate the package and experiments, then set the new stable VERSION and run `python3 <skill-dir>/scripts/skill_release.py publish --registry <release-registry>`. This creates a new manifest/ZIP pair with exclusive writes and rejects reuse of a registered version. Run `verify` and repository validation after publication. Never regenerate or edit old release pairs, including the legacy 1.0.0 archive. SHA-256 verifies consistency, not authenticity; the repository history remains the audit trail. Experiments already in progress retain their recorded version/hash. Earlier uses without recoverable packages remain `legacy-unknown`; do not invent their version or deployment date.

## Record the intervention, not just the installed version

Extend a project's existing experiment ledger or copy [experiment-log.csv](../assets/experiment-log.csv). The new columns append to the earlier contract; migrate old rows by header and leave unavailable values blank. Do not rewrite existing files from the blank template.

Record experiment ID, skill version/hash/snapshot, actual deployed site revision (and artifact digest when the commit is insufficient), template/data revision, model/settings when available, affected URLs, publication time, hypothesis, budget, primary metric, and decision condition. Distinguish skill release date from deployment date and first observations. Installing a new skill does not apply it to old pages.

Freeze URL membership in [page-cohorts.csv](../assets/page-cohorts.csv): `arm` is treatment or control; each row identifies one page in a cohort. Preserve prior identity. New pages, refreshed pages, and unchanged comparison pages need separate cohorts. If a page receives another substantive change during observation, end the period or mark the overlapping intervention; do not assign all its traffic to the latest installed skill. Retain redirected/retired members and explain their handling to avoid selecting only survivors.

## Define comparable observations

Use [traffic-observations.csv](../assets/traffic-observations.csv) for normalized observations and [version-evaluation.md](../assets/version-evaluation.md) for the decision. Each observation is one metric for one cohort/arm and non-overlapping period; `period` is baseline or followup. Do not mix site totals, query rows, page rows, or overlapping segments. Record source/property, export timestamp, timezone, filters, and raw export reference. Use `data_status` complete, partial, missing, or not_measured; unavailable values stay blank. Zero means an observed zero only after source verification: add `zero_evidence=observed` and `zero_evidence_ref`. Some exports replace unavailable data with zero; preserve ambiguous zeros in the raw export and notes, but normalize their value to blank and status to missing. See [source-specific export handling](measurement.md#search-console). The added columns are optional for nonzero historical observations; do not manufacture zero evidence during migration.

Choose one primary traffic metric before reviewing results, such as Google organic landing sessions or Search Console web-search clicks. These are different measures, not interchangeable counts. Impressions indicate exposure; include them as context rather than calling them visits. Record a useful-action metric (task completion, qualified inquiry, store click, or purchase where measurable), rates with denominators, and production/maintenance effort. Avoid collecting personal visitor data just to label a skill version; a page/release ledger is normally sufficient.

Compare equal completed periods with comparable weekdays, page age, country, device, search type, and brand/non-brand definitions. A pair of 28-day periods is an example, not a fixed requirement or guaranteed SEO maturation time. Set the review window from traffic, deployment timing, data lag, seasonality, and the hypothesis; exclude incomplete recent reporting days. New pages have no observed pre-launch page traffic baseline: compare equally aged launch cohorts or report a descriptive pilot, not an infinite lift from zero.

With adequate comparable pages, preassign a treatment group and an unchanged control group, ideally randomized when appropriate. Check pre-trends and spillover from shared navigation/templates. A site-wide navigation change can affect the supposed control; unrelated sites or dissimilar page types are not automatically valid controls. Keep existing successful pages stable while testing where practical.

## Validate inputs before calculating

Run the standard-library checker against the project's normalized CSVs:

```bash
python3 <skill-dir>/scripts/validate_traffic.py --observations observations.csv --cohorts cohorts.csv --experiments experiments.csv
```

Use the bundled headers. Dates are inclusive ISO dates; page `first_published_at` and `changed_at` use reporting-local dates. `release_at` and `extracted_at` are ISO timestamps with UTC offsets; `timezone` uses an IANA name. Context fields must be explicit, using `all` or `none` where applicable. `unit=count` requires nonnegative integers. Each cohort/arm/metric has one aggregate baseline and one aggregate followup, not multiple query or daily rows. Normalize upstream with documented aggregation before validation. Supply unavailable baseline rows as not_measured/blank for new-page cohorts; the checker withholds their comparison.

The checker validates membership, deployment provenance syntax, duplicate observations, source/filter consistency, periods, publication timing, unavailable values, and zero evidence references. Invalid data suppresses all calculated comparisons and exits nonzero. Partial/missing observations produce warnings and no comparison for that pair. It reports descriptive changes only and never declares a winning version. References are provenance pointers, not proof: independently inspect original exports and verify actual package hashes with the release helper. It cannot detect unreported concurrent interventions, tracking defects, false records, or determine whether a sample is sufficient.

Follow the [worked synthetic experiment](../examples/traffic-pilot/README.md) for a complete ledger, cohorts, raw counts, normalized observations, and decision. Keep real site evidence outside the reusable package.

## Calculate and interpret

- Report baseline and follow-up absolute counts. Absolute change = follow-up minus baseline. Relative change = absolute change / baseline only when baseline > 0 and observations are comparable and complete; otherwise mark it unavailable and explain.
- Aggregate CTR as summed clicks / summed impressions, with an available positive denominator. Calculate conversion rate only from matching populations and compatible source/event definitions. Never join Search Console query rows to individual purchases.
- With a defensible control, report both trends. An optional additive difference-in-differences is (treatment after − treatment before) − (control after − control before), using a consistently defined measure such as clicks per page-day when group sizes differ. Parallel pre-trends and absence of differential confounders remain assumptions; the calculation alone proves no causal lift.
- Record promotions, pricing/product changes, migrations, consent/tracking changes, seasonality, search updates, concurrent content work, and model/tool differences. More total traffic from more pages does not by itself establish better quality per page or per unit effort. Do not prescribe universal significance thresholds or choose winning windows after seeing results.

Classify outcomes as **promising**, **inconclusive**, **regressed**, or **invalid comparison**, with reasons and a continue/revise/gather-evidence/stop decision. Before/after traffic is usually directional evidence about a deployed intervention. Repeated comparable experiments across page groups and sites support a stronger assessment of a skill release; a single site's lift does not establish that the skill caused it. Report missing analytics as unknown, not zero, and complete a measurement plan without inventing a result.

## Comparing skill versions versus testing a site change

An unchanged control estimates the effect of applying a change; it is not an active comparison with the prior skill. To assess versions, run the same held-out tasks with the prior and candidate skill using the same model/settings, inputs, available tools, and time budget. Hide grading expectations, retain exact package identities and outputs, and grade correct decisions plus delivered artifacts. Repeat across task types and seeds/sessions before claiming reliability.

For field evidence, compare appropriately matched interventions produced by the two versions where feasible, recording implementation effort and content differences. Keep unchanged controls separately when useful. Avoid applying competing versions sequentially to the same URLs and pretending there is no carryover; ranking and content history persist. A low-traffic site may support only descriptive evidence. Combine model task evidence with site outcomes; neither alone establishes general skill superiority.

## Two quality gates

Before release, validate packaging, helper behavior, and realistic authored decision scenarios. Distinguish authored cases, deterministic tests, and actually executed model evaluations. Run matched prior/candidate model evaluations where feasible, retaining prompts, model/settings, artifacts, and grades.

After deployment, evaluate traffic and useful outcomes with the recorded contract. Passing local tests cannot establish traffic gains; traffic gains cannot excuse incorrect claims or broken functionality. Use both kinds of evidence to choose the next release. A proposed review date is not authorization to create a recurring automation.
