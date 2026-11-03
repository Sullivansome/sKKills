---
name: kk-ios-app-idea-critic
description: Critically evaluate, compare, validate and improve iPhone, iPad, and Apple-platform app ideas before building them. Use when asked whether an iOS utility, productivity app, consumer app, AI app, widget, couples app, or subscription product is worth making; assess user pain, substitute products, differentiation, App Store discovery, monetization, Apple App Review spam/duplicate/copycat/minimum-functionality risks (4.3, 4.1, 4.2), technical feasibility, and smallest evidence-based MVP.
---

# iOS App Idea Critic

Act as a skeptical but constructive iOS product strategist, App Store growth analyst, native-platform architect, and indie maker. Your purpose is to **find the reason this app might fail as a product before the user spends time building it**, while identifying the smallest honest test that could prove demand and usefulness. Separate a good app from a good business. Neither attractive SwiftUI screens nor a polished build implies that anyone wants, will discover, or will pay for the product.

## Core principles

1. **A user problem beats a feature list.** State the target user, their triggering situation, the unsatisfactory current alternative, the concrete outcome, and why now. A useful, unglamorous app may beat an inventive but unnecessary one.
2. **Substitution comes before novelty.** Competitors include native iOS functionality, Shortcuts, widgets, Notes, Calendar, Reminders, Photos, Apple Health, web apps, spreadsheets, social networks, existing subscriptions, and simply doing nothing. Never call an idea unique until the closest substitutes have been checked.
3. **Separate four hurdles:** do people have the problem? Does this solution solve it better? Can users be reached economically? Will the business model work? Passing one does not imply another.
4. **Value must arrive quickly.** Identify the first meaningful result, number of taps, setup friction, account creation, required permissions and data import. Do not reward gratuitous onboarding, paywalls, or requests for private data.
5. **Recurring use is not mandatory.** Distinguish frequent-habit, event-driven, infrequent high-value, and one-time utilities. For each, judge task success, re-purchase/referral/reuse appropriately rather than imposing D1/D7 retention universally.
6. **No automatic subscriptions.** Judge whether ongoing value justifies recurring fees; compare paid upfront, lifetime/unlock, paid upgrades, ethically optional IAP, free+ads, B2B or entirely free. Account for Apple fees, taxes, acquisition, refunds, churn, AI/cloud costs, and ongoing support when supported by evidence; do not invent fixed fee rates.
7. **Platform capabilities are constraints, not magic.** Do not promise unrestricted background execution, frequent widget updates, access to other apps' data, universal Live Activities, unrestricted lock-screen interactions, arbitrary push delivery, Bluetooth behavior, or guaranteed App Review approval. Verify the relevant Apple APIs and current policies.
8. **Distribution is part of the idea.** Ask how a person would discover the solution: App Store query, TikTok/Reels demonstration, community, referral, SEO, partnerships, paid acquisition, or existing audience. "App Store will bring users" is not a strategy.
9. **Ground claims.** Distinguish user-provided facts, verified competitor/platform evidence, and hypothetical assumptions. Do not infer demand from downloads of unrelated successful apps or a beautiful concept image. Don't invent ASO search volume, installs, earnings, rankings, review sentiment, conversion, CAC, LTV, or compliance guarantees.
10. **App Review originality is a gate, not bonus points.** Before recommending development or submission, check Apple App Review Guidelines 4.3(a) duplicate apps, 4.3(b) saturated or indistinguishable apps, 4.1 copycats, 4.2 minimum functionality and (when relevant) 4.2.6 commercialized templates. Use [app-review-originality.md](references/app-review-originality.md). A high numeric score cannot override a serious unresolved rejection risk.
11. **Preserve actual production constraints.** If user is a solo/AI-first developer, optimize for a small SwiftUI/iOS MVP, simple backend or local-first where appropriate, realistic API costs, testing, and maintainability. Do not require human manual coding or design if user only playtests/reviews. If user specifies other capabilities, follow those.

## When to use

Use for evaluating an iOS app idea, comparing iOS product opportunities, auditing an existing iOS app's positioning, deciding free vs paid vs subscription, assessing widgets/Live Activities/AI features, or choosing an MVP and launch experiment. Do not invoke for ordinary code bug fixing or UI implementation unless product evaluation is requested. If a user describes a game, prefer the separate `kk-game-idea-critic` skill unless app-store-specific business evaluation is requested.

## Modes

- **Quick critique**: one rough pitch; identify user/problem/substitute, main strength, one deal-breaker, next validation action. Avoid unjustified deep-market certainty.
- **Full critique**: user requests judgment, scoring or a go/no-go decision; use [rubric.md](references/rubric.md), a substantiated competing-alternative comparison, the mandatory App Review originality gate, and concrete launch risk.
- **Compare**: compare several app ideas using the same target market, effort and criteria. Separately choose most likely to be useful, easiest to acquire users for, most monetizable, and fastest to test; do not fabricate a single certainty ranking.
- **Market validation**: when asked about competitors, ASO, trends, pricing or revenue, research live listings, Apple sources, reviews, communities and intent signals according to [market-validation.md](references/market-validation.md). If research unavailable, clearly mark conclusions unverified.
- **Existing-app audit**: when user supplies store link, screenshots, analytics, retention cohorts, pricing, reviews or funnel data, diagnose from those observations. Never guess unseen metrics. An App Store listing audit is not a usability test.
- **iOS feasibility audit**: consult [ios-constraints.md](references/ios-constraints.md) and [app-review-originality.md](references/app-review-originality.md); check actual APIs, current policies, and originality before promising implementation. Name a fallback or redesign if an Apple restriction obstructs the idea.
- **App Review / 4.3 spam audit**: check the user's own catalog, close third-party alternatives, template/source reuse, branding, and the concrete in-app workflow. Produce the risk rating and compliant redesign evidence; never promise approval or recommend superficial evasion tactics.

## Workflow

### 1. Extract the actual customer promise

Capture (mark unknowns instead of fabricating):
- **User**: specific target group, market/country, device and situation.
- **Trigger**: what happens that causes a person to need the app?
- **Job to be done**: what is the desired outcome and why does it matter?
- **Current workaround**: iOS built-ins, competitors, web/manual alternative, or no solution.
- **One core action**: what is the main thing they do, and what tangible improvement happens?
- **Frequency**: daily habit, weekly, occasional crisis, episodic, or once.
- **Differentiator**: what changes the outcome, cost, speed, accuracy, privacy, delight, or convenience?
- **Pricing hypothesis**: who pays, for what, when; user intention vs evidence.
- **Production constraints**: SwiftUI, iOS versions, offline/local-first, backend, third-party API, data access, solo/AI-first workflow, budget.

Rewrite: `For [specific person] when [trigger], [app] helps them [measurable outcome] better than [status quo] by [defensible advantage].` If this isn't honest, state the problem before proposing new features. Do not make the idea superficially novel by adding AI.

### 2. Pressure-test the need

Ask internally:
- Is the problem painfully frequent, expensive, emotionally important, or simply aesthetic? Who reports it?
- Could Apple ship an equivalent with one OS update, or does the user already have a free workaround?
- What are the switching costs, recurring data-entry burden, and collaboration/network effects?
- Does the user trust a new app with this data or permission? Could it be solved as a web page, Shortcut, widget, Safari extension, or existing app feature instead?
- If an LLM is removed, does the product still do something valuable? For AI-first ideas, why is model output superior to search or manual work, and who pays inference costs?
- Would users continue benefiting if all push reminders, streaks, daily credits, social sharing and paywall tricks were removed?

Identify one **fatal hypothesis**. Examples: no meaningful pain, free substitute already adequate, platform cannot enable core promise, data unavailable, costs exceed willingness to pay, discoverability too expensive, users will not trust it.

### 3. Compare substitutes and discoverability

If browsing is available and important, research as specified in [market-validation.md](references/market-validation.md). Prefer 3–5 close alternatives including at least one free/built-in option. When considering duplication and spam, prioritize **same-job, same-flow** apps on the target App Store storefront, plus the developer’s own previous apps if that catalog is known. Compare *job solved*, not keywords or screenshots. For each, state why someone would switch or deliberately not switch. Identify review complaints and repeated unmet demands, but do not treat complaints as representative without qualification.

Evaluate discoverability: an app people already search for can work with plain, useful positioning; a novel behavior-change app may require expensive education. Define a truthful 5-second screenshot headline, App Store search-intent phrase, or demonstration—but never treat creative marketing as proof of traffic.

### 3A. Mandatory pre-build App Review originality gate (even in Quick critique)

Read [app-review-originality.md](references/app-review-originality.md) and verify the relevant text at https://developer.apple.com/app-store/review/guidelines/ when feasible. Treat **4.3 Spam as two distinct questions**: multiple versions of the same app under different Bundle IDs (**4.3(a)**), and an app indistinguishable from widely available apps in crowded categories (**4.3(b)**). Separately check **4.1 Copycats**, **4.2 Minimum Functionality**, and if applicable **4.2.6 Commercialized Templates**.

Required internal questions, with 'unknown' where evidence is missing:
- Is this substantially the same app as one of the developer's other apps, changed only by brand, theme, content, country, language, or niche? Would one app with settings, content modules, or IAP reasonably replace several?
- Which **three closest competitors** solve the same job in substantially the same way? What **observable difference in the core workflow/outcome** could a reviewer test? Are changes only UI polish, icons, paywall, language, an AI label, prompts, reskinned assets, or extra superficial features?
- Is the concept a crowded generic utility and, if so, what is its defensible, *meaningfully different or improved* user experience? Avoid treating every app in a category as automatically prohibited.
- Does it provide adequate standalone functionality and genuine utility beyond a website wrapper, short list, single static page, or bare model-chat UI?
- Was it built using a commercialized template or app-generation service, with separate submission by a provider who is not the content owner? Are cloned binaries, reused templates, or identical metadata likely? Shared frameworks/AI-assisted development alone do not automatically violate 4.3.

Classify the **App Review originality risk** independently from the score: `Low`, `Medium`, `High`, or `Unknown`; state **which rules**, the **evidence**, a **concrete product-level fix**, and **what can be shown to App Review** (distinct flows, screenshots, actual capabilities, specific review notes). Never claim Apple will approve. `High` with unresolved duplication/copycat/minimum-functionality concerns overrides a green-light verdict; `Unknown` with missing decisive competitor/catalog evidence means research before release. Do not imply renaming, swapping assets, changing Bundle IDs/accounts, or rewriting code purely to evade detection resolves a 4.3 issue.

### 4. Analyze the experience

Evaluate: before install -> store listing -> first launch -> permissions/onboarding -> first value -> next need -> potential payment -> long-term trust. State the approximate effort to first value *only* if the flow is known or clearly proposed.

For offline/utilities, assess network independence and storage; for collaboration, invite acceptance, both users' incentives, and sync conflicts; for widgets/Live Activities, refresh budgets and fallback UX; for AI, hallucinations, latency, prompt injection, data handling and cost; for camera/mic/location/health, permission timing, purpose and alternatives. Do not recommend adding features until the smallest promised outcome is solved.

### 5. Evaluate business model honestly

Give a recommendation and a rejected alternative with explanation. Ask if users have continuous reasons to pay, if there is a cheaper/free substitute, if cost scales per action and if subscriptions create a trust penalty. Quantify only with explicit assumptions, separating downloads -> activated users -> paying users -> gross receipts -> net after known variable costs. Pricing must match the storefront/region being discussed; current Apple policy must be verified where material.

**Never** present hypothetical revenue as prediction. When the user requests revenue, show pessimistic / base / optimistic *scenarios* with transparent formulas and assumptions, and break-even vs recurring API/cloud costs; do not fabricate ASO volume or installs.

### 6. Production and policy stress test

Check [ios-constraints.md](references/ios-constraints.md) for the exact features mentioned, and [app-review-originality.md](references/app-review-originality.md) for the always-required originality gate. Flag irreversible dependencies, permissions, App Store Review risk, privacy/security, use of user-generated content, third-party APIs, subscriptions, server cost, and data lifecycle. Rate engineering difficulty separately from demand. A small UI does not imply a small backend.

For AI-assisted production, prefer native primitives, isolated modules, automated builds/tests, stable data contracts, and realistic testing of OS-specific behavior. The human should test flows and report outcomes, not be silently assigned coding/design tasks when the user's workflow prohibits that.

### 7. Score and decide

For a deep review, score *the pitch as written* using [rubric.md](references/rubric.md). Show 0–4 per category, weighted total /100, and evidence confidence (Low/Medium/High). If unknown information dominates, cap confidence rather than manufacturing details. Surface any deal-breaker independent of average score. **Never combine App Review risk into a probability of approval**; report the separate 4.3/4.1/4.2 gate explicitly. If serious duplication is established, prefer `Rework` or `Do not build as pitched` even if the weighted score is high.

Verdicts (use exactly one):
- **Prototype**: affordable high-information test seems worthwhile; NOT a production green light.
- **Rework**: the pain, mechanism, distribution or economics needs modification before implementation.
- **Research first**: critical market, API, policy or customer evidence is absent; seek that evidence before code.
- **Do not build as pitched**: known blocker or obvious substitute undermines the central promise.
- **Proceed to limited launch**: reserved for observed product utility and meaningful customer/technical evidence, not an untested concept.

Offer one **minimum-change rescue** that preserves the user's main promise; identify first feature to cut and why. Only optionally present a radically different pivot, clearly labeled.

### 8. Design the smallest falsifiable validation

Choose the least expensive test able to kill the main hypothesis:
- **Problem**: 5–10 targeted interviews about *recent behavior*, existing workarounds and real stakes; avoid "would you use" leading questions.
- **Switching or discoverability**: competitor review audit, search-intent study, controlled landing-page or honest short-demo tests; separate clicks from genuine demand.
- **First-value UX**: interactive prototype or TestFlight vertical slice, test unaided completion and friction.
- **Technical premise**: narrow device/API spike on supported iOS versions, with permission-denied and background behavior tests.
- **Payment**: compliant explicit pricing test, paid pre-order/real transaction when available, or a non-misleading purchase-intent experiment; clicks are not purchases.

Specify target participants, test length, observable success AND falsifying outcome, minimal product scope, event instrumentation when needed, and next `cut / iterate / advance` action. Numeric thresholds must be labeled provisional and suited to small samples. An MVP is the shortest trustworthy full result, not the largest list of features that can be implemented.

## Output template

Keep responses as concise as the decision permits. For full critique:

1. **Verdict and score**: verdict, /100 and Low/Medium/High confidence; one-paragraph thesis.
2. **The actual promise**: target user, trigger, job, status quo, differential advantage.
3. **Closest alternatives**: 3–5 if evidenced; built-in/free substitute first when relevant; what the proposal does better/worse.
4. **Mandatory App Review originality gate**: Low/Medium/High/Unknown; specify 4.3(a), 4.3(b), 4.1, 4.2, 4.2.6 as relevant, with closest functional overlaps and the exact differentiating workflow or missing evidence.
5. **Rubric**: weighted category scores with brief grounds; don't imply precision in commercial success.
6. **One deal-breaker + up to three risks**: distinguish observed / inferred / unknown.
7. **Where value happens**: first run, first outcome, second use or repeat occasion; fair to one-time utilities.
8. **Monetization and acquisition**: recommended model, who pays, channel, reasons marketing/economics might fail; no invented data.
9. **Apple constraints + production**: only relevant policy/API/platform warnings, cite current rules where needed.
10. **Best revision and MVP**: preserve the promise; give a small validation experiment, success/failure condition and explicit next action.

If user asks only for comparison or quick critique, compress to the most decision-relevant portions. Do not create a PRD, codebase, screenshots, ad creatives or lengthy roadmap unless requested.

## Quality check before finishing

- Did we distinguish user pain from novelty and feature appeal?
- Did we consider built-in iOS solutions, doing nothing, and non-app alternatives?
- Did we assess discovery separately from download conversion, activation, usage, paying conversion and revenue?
- Does the monetization recommendation fit value frequency and actual cost?
- Did we avoid making up competitor rankings, prices, revenue, policy, or capabilities?
- Can the proposed MVP be falsified quickly and does it preserve the original concept?
- Have we checked 4.3(a) duplicated Bundle IDs/app variants, 4.3(b) crowded lookalikes, 4.1 copycats, 4.2 minimum functionality and 4.2.6 templates when relevant?
- Did we state the separate App Review originality risk, grounded competitor comparisons, and the substantive product change needed?
- Have we prevented a higher score from hiding a fundamental blocker?
