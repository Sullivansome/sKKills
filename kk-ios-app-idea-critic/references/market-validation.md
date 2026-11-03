# Competitive and market validation protocol

Use when a user asks about originality, market size, current competitors, app store rankings, keyword demand, ASO, revenue, pricing, ads, subscriptions or commercial prospects. Browse where available; cite current primary sources and date claims.

## Evidence order

1. The user-provided app, prototype, store listing, usage data and real user interviews.
2. Apple App Store listings for the relevant **country storefront**, current features, purchase labels, subscription offerings, screenshots, release notes and review topics. Check Apple built-ins and default workflows.
3. Official developer websites, demos, help centers, public product roadmaps, Apple Developer documentation for claimed platform features.
4. Independent first-hand user complaints/discussions (Reddit, forums, communities), noting selection bias and how often a complaint repeats.
5. Third-party intelligence estimates only with explicit attribution, methodology/uncertainty and date. Do not convert store ranks, review count or community anecdotes into invented install or revenue figures.

## Competitor shortlist

Search by **job and triggering situation**, not only the app's genre or name. Identify:
- `Direct`: same user, same job, similar flow.
- `Native/free`: Apple's built-in app, iOS setting, Shortcuts, existing Apple service or no-cost workflow.
- `Adjacent`: same job solved by another form factor or distribution method (web tool, bot, spreadsheet, paper, SaaS).
- `Counterexample`: a discontinued/poorly reviewed or underperforming alternative whose failure may reveal weak demand.

For each, compare one sentence on feature parity, switching cost, major complaint, and the proposed app's actual advantage. An original UI does not necessarily change job-to-be-done. **When checking 4.3(b), prioritize closest workflow and outcome similarities, not only search-keyword overlap; when checking 4.3(a), compare the developer's own apps or planned Bundle IDs.** Read [app-review-originality.md](app-review-originality.md). Look for competitors' downside, not just their success.

## App Store discovery and acquisition

- Distinguish **search-intent** apps (user already knows problem) from **education-dependent** apps (must persuade people they need a new behavior).
- Hypothesize real query phrases; if search volume is unavailable, say so. Don't invent keyword search volume or score difficulty.
- Evaluate the title, subtitle, app icon, first 1–3 screenshots and real before/after result for conversion *in principle*—no assumed conversion rates.
- Distinguish impressions, product-page views, downloads, first successful outcome, activation, repeat task usage, trials, paid conversions, refunds, churn and proceeds. They measure different steps.
- For organic, name where target users already express the pain and a specific demo/answer that could reach them. For paid, assess ability to measure CAC, payer conversion and contribution margin rather than calling paid ads a growth plan.
- Localize pricing, competition, user needs, legal/regulatory and cultural assumptions to actual intended storefronts.

## Financial sanity check

When the user requests projections, write the formula and input assumptions:

`first_time_downloads * activation_rate * eligible_payment_conversion * net_revenue_per_payer - variable_costs - acquisition_spend - fixed_costs = approximate contribution`

For subscriptions, consider cohort conversion, renewal, churn, refunds, chargebacks, support, ongoing cloud/API costs and acquisition. The formula above is a simplification, not recognized accounting profit. Separate paid unlocks, ads, subscription MRR and one-off IAP. Use scenario tables only when asked for forecasting. Clearly label invented illustrative inputs. Avoid universal App Store fee statements; storefront, program, product type and policy vary.

## Current primary references

- Apple's review guidelines: https://developer.apple.com/app-store/review/guidelines/
- Apple's product-page guidance: https://developer.apple.com/app-store/product-page/
- Apple's App Store Connect analytics: https://developer.apple.com/help/app-store-connect-analytics/
- Apple's In-App Purchase documentation: https://developer.apple.com/in-app-purchase/

Recheck pages and dates at evaluation time; these links are starting points, not permanently fixed rules.
