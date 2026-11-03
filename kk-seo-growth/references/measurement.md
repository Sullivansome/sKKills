# Measurement and experiments

## Outcomes and events

Select one primary outcome suited to the site. Keep discovery, arrival, first value, continuation, and payment separate. For app/store flows, a store click is not an install. Use available campaign attribution and report gaps.

Possible events: demo_started, task_completed, sample_downloaded, prompt_copied, exercise_passed, store_clicked, trial_activated, purchase_completed, returned_to_task. Use actual conventions and implement only authorized events. Define semantics and prevent duplicate firing.

Record source/medium/campaign and landing page without leaking sensitive data into URLs. Preserve established consent and analytics policies. Consider blocking, redirects, cross-domain flows, duplicate events, bots, and missing referrers.

## Search Console

Record property, search type, dates, timezone, filters, freshness, and dimensions. Use current documentation for report definitions.

Compare equal completed periods and similar weekday/seasonal conditions. Distinguish brand/non-brand intent where useful. Inspect query mix and average position before diagnosing CTR. A site-wide average can hide opposing page changes.

Query totals may differ from property totals due to omitted/anonymized data, aggregation, and API/export limits. Do not replace missing with zero. Distinguish missing data, zero observed events, and not measured. Do not sum or join incompatible grains.

For CSV exports, inspect headers, units, and source-specific missing-value encoding first. Google's [generative AI report export](https://support.google.com/webmasters/answer/16984139) can serialize unavailable UI values as zero. Preserve the original export; do not treat such a zero as observed without corroboration. In the normalized observation log use a blank value with `data_status=missing` when it is ambiguous, and retain the raw value and reason in notes. For a verified zero, record `zero_evidence=observed` and `zero_evidence_ref` pointing to the supporting source or capture. Other numeric observations may leave these fields blank. Normalize dates, numeric separators, percentages, encoding, URL forms, and duplicates. Record transformations. Derive weighted CTR from total clicks / total impressions, not an average of row percentages. Do not invent weighting for average position when required data is missing.

## Business data and attribution

Use compatible aggregation such as landing page/day/channel. Search Console queries normally do not supply a direct user-level join to purchases. Do not claim exact keyword revenue through an unsupported join.

Measure contribution with supplied costs: revenue minus refunds, fees, variable delivery/API costs, and attributable ads; state excluded overhead and labor. Do not label gross sales as profit or GMV as revenue.

Distinguish Google organic, other search, AI referrals, social/video, paid, and direct/unknown where available. Missing AI referrers do not prove no AI influence. Citations are not traffic. Keep assisted and last-touch attribution explicit.

## Bounded experiments

Use assets/experiment-log.csv. Record hypothesis, eligible audience/pages, baseline, exact change, release date, primary metric, guardrail, observation window, source, and decision condition.

Use controlled tests when traffic and implementation permit them. With low traffic, use direct observation and descriptive counts. Do not call a few conversions statistically conclusive. For formal testing, determine samples/duration from meaningful effect, traffic, and uncertainty rather than universal thresholds.

Avoid changing copy, pricing, distribution, and onboarding simultaneously when attribution matters. Record concurrent changes and confounders. Treat before/after differences as directional without stronger causal evidence.

Direct tests can reveal comprehension quickly; crawling, indexing, ranking, seasonality, and repeat use may require longer. Set a budget and review date matching the hypothesis. Do not require indefinite effort or prematurely reject SEO from a few days of data.

## Monitoring

Monitor only when authorized or requested. A proposed cadence is not permission to schedule. For requested recurrence, use actual automation capabilities and define site/timezone, access, budget, deliverable, and failure handling.

Require a meaningful baseline, minimum absolute volume, comparable periods, and completeness before percentage alerts. Investigate tracking failure, outages, indexability, changed URLs, query mix, seasonality, and releases before declaring a penalty.

## Report

Show dates, absolute counts, denominators, rate definitions, and evidence quality. Include changes, useful outcomes, uncertainty, and decisions. Choose continue, revise, gather evidence, or stop this experiment. Stopping a page experiment does not establish that the product should be abandoned.
