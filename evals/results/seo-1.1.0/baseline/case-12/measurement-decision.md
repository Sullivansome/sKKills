# Planned navigation experiment — measurement decision

Status: **gather evidence; not deployed**. This is a planned intervention on https://example.test/, not a result. No traffic baseline or task-completion observation exists. Audience/market and exact Search Console property remain unverified.

Candidate: kk-seo-growth 1.0.0, SHA-256 `3c1e35ae7ddb304721025a3e666ebdaeacd6be95550963aafef69ee0666c3d32`. `skill-identity.json` and `kk-seo-growth-1.0.0.zip` preserve the exact supplied package; content identity does not establish effectiveness. Prior package identity is `legacy-unknown`. Model/settings, effort costs and approved budget are unknown and blank in the ledger.

`page-cohorts.csv` fixes the two treatment members, `/templates/onboarding/` and `/templates/followup/`. IDs are ledger-local stable identifiers. Both are existing pages receiving a planned navigation refresh; neither is a new-page cohort. No control pages were supplied, so no fabricated control rows exist. Candidate fields refer to planned authorship; blank deployment timestamps/revisions must not be interpreted as exposure.

Hypothesis: useful topic navigation increases Google web-search clicks to these pages while preserving users' ability to complete a template task. The primary metric is clicks, not impressions, sessions or revenue. Proposed guardrail: task completion rate, successful completed template-use tasks divided by eligible resource visits from the same measurement population. Before launch, define completion precisely with the site's owner and available measurement: copying text alone is only a proxy. If measurement is unavailable, record `not_measured`; do not claim the guardrail passed.

## Record at deployment

1. Save baseline HTML/source and the exact implemented navigation diff. Record site commit and served artifact digest when needed, template/data revision, relevant model/settings, implementation/maintenance cost and concurrent changes.
2. Record publication timestamp with timezone and actual public verification of both URLs, links, canonicals and usability. A build or source edit alone is not deployment. Keep skill snapshot time, installation time, publication time and observation time separate.
3. Populate ledger release/revision fields and cohort `changed_at`; retain known first-publication dates or leave unknown. Preserve prior skill identity if recoverable, otherwise keep `legacy-unknown`.
4. Resolve exact Search Console property, metric definition, reporting timezone, filters, export freshness and raw-export storage location. Preserve exports unchanged and record extraction timestamps. Collect compatible page/day counts for the fixed cohort, excluding incomplete recent days and overlapping/duplicate rows.
5. Define and check guardrail measurement before release. Set an effort budget and decision date/window before looking at follow-up results; none is scheduled by these files.

## Comparison contract

A provisional window is 28 complete days before and 28 complete days after deployment, with comparable weekdays and a prospectively chosen treatment of crawl/indexing lag. Finalize dates before follow-up inspection based on expected volume; 28 days is neither a maturity promise nor a significance threshold. Preserve both windows even if results are disappointing. If the sample is too small, report counts and uncertainty and gather more evidence under an explicitly documented extension.

Against the prior skill: compare the same fixed pages before and after the deployed change, retaining prior package/hash and revision if recoverable. Missing prior packages prevent a defensible exact-version comparison; label the historical arm legacy-unknown. This evaluates a navigation intervention only, not the installed skill in isolation. A stronger skill comparison needs matched implementation tasks with fixed model/settings, site inputs, comparable page cohorts, exact prior/candidate packages, and recorded deployed changes; none of those historic identities may be reconstructed from today's package.

Against unchanged pages: choose comparable existing resource pages before release and append their exact URLs in a separate fixed control cohort with `arm=control`. Check similar page age, search intent, baseline volume and pre-trends; randomize only where practical. Confirm the new topic navigation does not materially expose/control-link those pages or alter their shared template. If navigation creates spillover, choose uncontaminated comparators or report a descriptive before/after study. Do not label unrelated sites or different page families valid controls automatically.

For each arm report raw before/after clicks, absolute change, and relative change only for complete comparable observations with positive baseline. For unequal group sizes use clicks / (fixed page count × complete days). Optional difference-in-differences = treatment change in clicks/page-day minus control change in clicks/page-day. Parallel pre-trends and no differential confounding remain assumptions; the arithmetic alone proves no causal effect. Preserve redirected/retired members and document their treatment; do not select only survivors. Mark overlapping interventions or end the observation period.

## Decision rules and unknowns

Current classification: **inconclusive**, with no outcome yet measured. Traffic cells are blank: baseline `missing`, follow-up `not_measured`. Zero will be recorded only for confirmed observed zeros.

Continue a bounded pilot when complete comparable evidence supports improved clicks and the task-completion guardrail is preserved. Revise navigation if it causes broken paths or observed task difficulty; stop or roll back the experiment if the change harms task completion. Gather evidence if counts, guardrail measurement, controls or provenance cannot support a decision. Select any practical minimum improvement and acceptable guardrail tolerance prospectively with the site's actual baseline and costs; neither is invented here. Report confidence/uncertainty and confounders, not a winning skill label from one lift.

No publication, account access, invented baseline or scheduling occurred.
