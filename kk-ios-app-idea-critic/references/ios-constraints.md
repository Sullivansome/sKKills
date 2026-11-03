# iOS platform, review and production feasibility checks

Read for iOS feasibility audits or when a concept depends on platform capabilities. Treat these as **questions to verify against current Apple documentation and target iOS versions**, not as permanent rules or substitutes for review of an actual implementation.

## Frequent architecture and capability traps

| Promised feature | What must be verified |
|---|---|
| Lock-screen widget / interactive widget | WidgetKit supported actions and widget families, update budget, user configuration, offline fallback, disabled interactions and deep-link behavior. Widgets do not offer arbitrarily fast continuous data updates. |
| Live Activities / Dynamic Island | ActivityKit eligibility, user authorization, push update design, lifecycle, supported OS/devices, and display fallback. They are not persistent arbitrary background UIs. |
| Background AI, GPS, BLE and sync | Specific supported background modes, entitlement, execution limits, power/connection conditions, network unreliability, and behavior when app is terminated. |
| Shared couples / social features | Invitations, linking identities without exposing private contacts, 2-sided onboarding, permissions, sync conflicts, offline behavior, notification opt-out and abusive-use scenarios. |
| Camera, mic, Photos, Health, location | Permission timing, purpose descriptions, restricted access, on-device processing options, export/deletion and data minimization. Never assume full access without consent. |
| Apple Photos / Live Photos / wallpaper | What PhotoKit APIs actually read/write, editing/rendering/export behavior, limited photo library permissions, wallpaper and lock-screen customization restrictions. |
| AI agent executing system tasks | Sandbox restrictions, available App Intents/Shortcuts interfaces, user consent, accessibility/security limits; cannot control unrelated apps without authorized pathways. |
| Payment / subscriptions | Current StoreKit APIs, paid entitlement restoration, subscription renewal state, refund handling, region rules, business-model fit and readable price disclosure. |
| Cloud sync / multi-device | Apple ID/iCloud sign-in conditions, conflict resolution, restore, migration, data loss, encryption and ongoing server cost. |
| Ads / attribution / tracking | Consent, ATT where applicable, SDK disclosures, privacy practices, ad load versus the promise of a utility. |
| Kids, health, finance, sensitive data | App Review category-specific rules, safety and consent, claims that may need specialist review; flag legal review when appropriate. |

## App Review check

Before building, ask:
- **Mandatory originality gate:** compare closest same-job/same-flow apps and any sibling apps; classify risk under 4.3(a) duplicate Bundle IDs, 4.3(b) indistinguishable saturated categories, 4.1 copycats, 4.2 minimum functionality, and 4.2.6 commercialized templates. Use [app-review-originality.md](app-review-originality.md).
- Does the app deliver more than a minimal website wrapper, collection of links, or extremely thin derivative? Review guideline 4.2 / 4.3 as currently written.
- Does it use licensed content and respect trademarks/copyright?
- Does the store listing accurately describe features, subscriptions and IAP, rather than depicting unavailable content?
- Are account and data deletion, purpose strings, privacy policy, third-party processing disclosures and permission handling appropriate?
- Can App Review reach the full functionality through a working account/demo, and test purchases?
- Are users harmed by misleading health/financial predictions or aggressive dark patterns?

Apple review acceptance is not guaranteed by a checklist; describe policy risks, not legal verdicts.

## AI-first solo build / QA

Validate the smallest architecture that can fulfill the promise:
- Prefer SwiftUI + native framework + local persistence when practical.
- Add backend only where multi-device sync, sharing, secure server secrets, durable accounts, purchase entitlements or model services genuinely require it.
- Account for account deletion, secret storage, credentials, lost devices, internet loss, migration and restoring purchases.
- Automated build, unit/UI tests, simulator coverage, TestFlight, crash reporting, accessibility, localization, permission-denied flows, and real-device testing especially for notifications/widgets/BLE/camera.
- If AI builds the entire app, it still needs integration testing and user-played feedback; AI code generation does not eliminate OS-specific edge cases.

## Current Apple reference URLs to verify

- App Review Guidelines (4.1, 4.2, 4.3): https://developer.apple.com/app-store/review/guidelines/
- Apple review overview (duplicate submissions/copycats): https://developer.apple.com/app-store/review/
- Apple guidance on 4.1 copycats: https://developer.apple.com/help/app-review/guideline-reference/4-1-prevent-copycat-rejection
- Human Interface Guidelines: https://developer.apple.com/design/human-interface-guidelines/
- Widgets: https://developer.apple.com/design/human-interface-guidelines/widgets
- Apple's In-App Purchase guidance: https://developer.apple.com/in-app-purchase/
- App Store Connect analytics: https://developer.apple.com/help/app-store-connect-analytics/
- App Store product-page guidance: https://developer.apple.com/app-store/product-page/

Verify at the time of evaluation; policy, regional payment rules, support and limits change.
