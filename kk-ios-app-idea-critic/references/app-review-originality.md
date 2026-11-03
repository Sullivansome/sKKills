# Mandatory App Review originality / spam / duplication gate

**Read on every app-idea critique, not just explicit compliance requests.** Verify the current English-language official Apple [App Review Guidelines](https://developer.apple.com/app-store/review/guidelines/) before making policy-specific or release advice; guidelines and enforcement can evolve. This is a risk assessment, not a guarantee, legal judgment, or private knowledge of App Review's review process.

## Distinguish the relevant rules exactly

| Rule | Apple's primary concern | Prototype/idea screening question |
|---|---|---|
| **4.3(a) Spam — multiple Bundle IDs** | Several variants of essentially the same app instead of one app serving users with selectable content/features | Does the developer already ship, or plan to submit, essentially the same app for each theme, location, language, customer, company or community? Could this be one app with modules, settings, location filters or IAP? |
| **4.3(b) Spam — indistinguishable/saturated** | Submissions indistinguishable from apps already widely available, particularly saturated categories | What does the new app **materially do better or differently** than its closest same-job, same-flow alternatives? |
| **4.1(a–c) Copycats/impersonation** | Passing another app's concepts/appearance/name/brand as one's own; brand or icon misuse | Does its name, icon, visual design, screenshots, navigation, copy, or key interactions closely mimic a specific app? Is it impersonating another service? |
| **4.2 Minimum Functionality** | Inadequate standalone utility/entertainment, repackaged websites, thin content/links or poor native usefulness | Can a new user complete a real end-to-end task without another app? Is there enough useful function, content and iOS-appropriate interaction to justify a separate app? |
| **4.2.6 Commercialized Templates** | Apps created through commercialized templates or generation services improperly submitted, without the required content-provider relationship and unique experience | Was this produced as one of multiple nearly identical client apps? Who owns/provides the content, and who submits it? Is it an acceptable single aggregated app? |

Official text: https://developer.apple.com/app-store/review/guidelines/ (Design §4.1, §4.2, §4.3). Apple also provides a [review overview](https://developer.apple.com/app-store/review/) and [copycat guidance](https://developer.apple.com/help/app-review/guideline-reference/4-1-prevent-copycat-rejection).

**Important distinctions:**
- Competing with an established app is not, by itself, a ban. A crowded category increases scrutiny; meaningfully improved experiences may be accepted.
- Visual uniqueness **alone** does not establish a different product, and generic AI integration **alone** does not establish useful differentiation. Ask what the user does that they could not do, or do as well, elsewhere.
- Reusing common libraries, open-source modules, SwiftUI patterns, or using AI coding assistance does **not automatically** make an app spam. Near-identical binaries, app-generator templates, copied assets and metadata are potential risk signals, not an exhaustive list of automatic violations. Do not advise evasion of similarity checks.
- A very small app can still provide strong utility. Don't equate number of features with minimum functionality; analyze actual standalone value.
- Multiple iOS *targets/extensions* inside a single product are not automatically the same as submitting multiple cloned stand-alone apps.

## Mandatory comparison protocol

1. Write a **single-sentence job-to-be-done** and the actual first-to-last user flow.
2. Examine at least **three closest competitors** when available (same audience, problem and workflow) on the intended country's App Store; also check Apple's built-in tools and the developer's own portfolio when supplied. Use direct official listings/screenshots/demos/release notes, not keyword similarity alone. Label unknown when unavailable.
3. Compare **five aspects**: target/trigger; central action; result delivered; differentiating experience; overlapping UI/branding/implementation. A different icon, color, localization, paywall or stack isn't a substantive differentiator.
4. Write an explicit **differentiation test**: `Compared with [closest app], this app lets [target user] accomplish [outcome] through [distinct, observable workflow/advantage]`. If you cannot support it, treat originality as unresolved.
5. Check **self-duplication**: planned apps under separate Bundle IDs, existing catalog, and whether one extensible app (content packs, localizations, subprofiles, IAP where appropriate) is the more compliant product.
6. Check **minimum-functionality value** by outlining a working end-to-end user journey. A mockup or planned feature is not implemented evidence.
7. Produce the risk rating, rule references, evidence, unknowns, product redesign, and **specific submission evidence** the developer could include in App Review notes. Only describe features that actually exist; do not suggest deceptive screenshots or claims.

## Risk classification and verdict gate

- **Low:** No observed substantial copying or cloned submissions; specific useful difference is evident and testable; adequate end-to-end utility. *Not an approval prediction.*
- **Medium:** Same category/use case as competitors with plausible differences still needing proof; small app whose standalone utility needs validation; common template risk manageable with substantive product work.
- **High:** Known same-app reskins submitted separately, obvious copying/impersonation, an indistinguishable crowded-category app, template/white-label submission concerns directly covered by current guidelines, or near-zero standalone utility. **Override numerical score: do not recommend shipping unchanged.**
- **Unknown:** Missing details on competitors, developer catalog, actual functionality or submission arrangement that are required to assess the specific risk; request or research only the decisive missing evidence before release.

Do not convert the rating into a fabricated probability of rejection. A live reviewer may make a different decision. Explicitly separate **verified evidence**, **reasonable inference**, and **unknowns**.

## Suitable compliant design responses

- **4.3(a):** combine duplicated verticals/locations/themes into one product with relevant browsing/filtering, content packs or IAP where appropriate, rather than clone several binaries.
- **4.3(b):** narrow to an underserved, specific job **and introduce a measurable differentiated workflow** (e.g., solves an unsolved user constraint, materially reduces steps, works offline where alternatives cannot, supports a neglected accessibility need with evidence). Naming a new niche alone is not enough.
- **4.1:** establish independent branding, assets, interactions and information architecture while focusing on a distinctive real user problem; don't imitate another icon/name.
- **4.2:** deliver one complete, useful task with durable value and appropriate native behavior; a simple focused utility can qualify if it actually works and is valuable.
- **4.2.6:** verify who provides content, who submits, and whether a genuinely customized client experience or single aggregated host app fits current policy.

**Never propose** resubmitting the same app under a new developer account, changing a Bundle ID, renaming the app, altering superficial UI/metadata, randomizing source code, or obfuscating the binary just to bypass review detection. Solve the underlying product issue.

## Required output, even for Quick critique

`App Review originality: [Low/Medium/High/Unknown]`

`Relevant guidelines: [4.3(a), 4.3(b), 4.1, 4.2, 4.2.6 as appropriate]`

`Closest functional overlap: [specific app/workflow or not verified]`

`Meaningful distinction: [testable user outcome/workflow or none shown]`

`Action before App Store submission: [one concrete change, evidence check, or none identified]`

For Full critique, explain the above in prose or a compact table and **enforce the stop/go gate before the weighted score**. Cite verified rules and live competitor evidence when available.
