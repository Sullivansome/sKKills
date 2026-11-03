# iOS App Idea Critic — 100-point rubric

Evaluate the current proposed app, not an improved app you invented. Scores measure *concept strength under present evidence*, not percentage likelihood of a hit or expected revenue. Separate concept score from evidence confidence **and from the mandatory App Review originality risk gate** in [app-review-originality.md](app-review-originality.md).

| Criterion | Weight | A high score demonstrates |
|---|---:|---|
| Specific user problem and urgency | 15 | A clearly identified person, trigger, observable pain, outcome, real current workaround |
| Core utility and time to value | 15 | One useful result with little friction, understandable UX, sustained reason to choose the app |
| Differentiation vs substitutes | 15 | Concrete advantage over close apps, native Apple features, web/manual workflows, or doing nothing |
| Discoverability and acquisition path | 15 | Plausible reachable audience, search/referral/social/partnership strategy tied to real user intent |
| Repeat value or task completion | 10 | Appropriate habit/occasion/episodic utility, low churn friction or meaningful one-time success |
| Monetization and unit economics | 10 | Credible who/why/when to pay, ethical fit, plausible costs, no reliance on untested conversions |
| iOS-native experience and platform fit | 10 | Native APIs/UX used where justified; restrictions and privacy addressed without wishful assumptions |
| Technical/operational feasibility | 5 | Scope, testing, dependencies, data, content, server/AI bills and maintenance plausible for resources |
| Fastest falsifiable validation | 5 | A cheap, measurable next test whose failure would change the decision |
| **Total** | **100** | |

## Rating anchors per row

- `0 / 4`: absent, contradicts known facts, or violates a hard platform/technical constraint.
- `1 / 4`: weak or mostly wishful; obvious substitute or serious unresolved flaw.
- `2 / 4`: plausible but generic or unproven; reasonable open questions.
- `3 / 4`: clear, distinctive, testable; credible evidence or narrow, convincing mechanism.
- `4 / 4`: unusually strong and evidenced for its maturity; direct behavioral evidence where relevant. A pitch without user testing should almost never score 4 for demand, economics or retention.

Calculate: `total = sum(weight * rating / 4)`. Do not round category arithmetic mid-calculation. Show total to nearest integer. Explain any legitimately inapplicable category and renormalize transparently.

Evidence confidence:
- `Low`: pitch/spec only; no usable firsthand user, API, competitor or funnel evidence.
- `Medium`: concrete prototype / competing alternatives / interviews / feasibility checks, but key outcome remains untested.
- `High`: multiple relevant users actually succeeded, trusted the flow, and there is meaningful evidence of usage or purchasing behavior. High is about evidence quality, not score.

## App Review compliance gate (separate from points)

Before interpreting the total, report `App Review originality risk: Low / Medium / High / Unknown` under Apple's current 4.3(a), 4.3(b), 4.1, 4.2 and 4.2.6 as relevant. Checking competitors' functionality, Apple's built-ins, the developer's other bundle IDs, product-template origins, and *testable* differences is mandatory. The 15-point differentiation category measures market advantage; it does **not** substitute for a policy check or predict review approval. A high policy risk means `Rework` / `Do not build as pitched` regardless of a high score. Unknown decisive evidence means `Research first` before recommending submission.

## Deal-breakers override score

- Problem is a nice-to-have with no clear target or triggering need, despite a large attractive feature list.
- Apple built-in functionality or a free substitute already solves the complete job with negligible switching friction.
- Core feature depends on iOS permissions, background processing, data access or APIs the platform does not expose.
- The system cannot safely deliver promised outcomes (privacy, health, financial, misleading AI automation, severe mistakes) within constraints.
- Monetization requires users to pay repeatedly for no recurring value or costs outgrow plausible proceeds.
- No realistic way to reach the buyer; cost of acquisition is neglected.
- The proposed MVP cannot prove the important promise without building the whole product.
- Unresolved high App Review risk: same-app clones under multiple Bundle IDs (4.3(a)), indistinguishable crowded-category variants (4.3(b)), copycat branding/experience (4.1), inadequate standalone utility (4.2), or problematic commercial template submissions (4.2.6).

## Interpretations, not hard bands

`~75–100`: compelling **candidate for validation**, not automatic go-ahead. `~55–74`: targeted redesign or evidence needed. `<55`: generally reframe or rethink. A red-flag blocker always takes precedence. Avoid treating cross-genre scores as comparable when audiences, launch goals and evidence differ.

## App-specific lenses (adjust analysis, not weights)

- **Utility:** time saved, reliability, accessibility, offline use, and search intent matter more than entertainment or social sharing.
- **Couples/collaboration:** both users' activation, invitation acceptance, opt-outs, conflicts, notification reliability, privacy and relationship asymmetry.
- **Widgets/lock-screen:** screen utility, update frequency limits, iOS version support, limited interaction, and graceful degradation.
- **AI wrapper:** accuracy, error recoverability, defensible workflow, cost per successful user outcome, trust, model changes and privacy.
- **Subscription productivity:** long-lived repeated value, renewal justification, migration, data export, refund/trust risks and pricing alternatives.
- **Creative/photo/video:** permission access, output quality, social sharing, editing latency, export, accessibility and storage costs.
- **Health/finance/safety:** elevated accuracy, consent, policy, regulated claims and compliance caution; never infer safety from an attractive mockup.
- **One-shot task:** end-to-end task success, no coercive streaks, willingness to pay once; retention not an inherent goal.
