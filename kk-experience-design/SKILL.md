---
name: kk-experience-design
description: Design user journeys, information architecture, interaction states, accessible interfaces, and testable prototypes for web, mobile, desktop, or developer tools. Use when interaction or usability decisions are unresolved; use kk-product-spec for product value/scope and kk-software-verification for review-only acceptance checks.
---

# Experience Design

Turn an agreed user outcome into an interaction contract that can be implemented and evaluated. Preserve the product brief and existing design language; do not turn a scoped implementation into an unrequested redesign.

## Ground the experience

Inspect existing screens or interfaces, components, terminology, user tasks, constraints, and available research. Distinguish observed usability problems from hypotheses. Identify the user's starting knowledge, device/input modes, permissions, context of use, and desired end state. For a CLI or API, include discoverability, examples, errors and recovery rather than inventing a graphical interface.

Use the established design system and available design/platform specialists when relevant. If they are unavailable, produce the scoped interaction work directly; this workflow does not require an externally installed design skill.

## Define the task and state model

Map the critical task from entry to successful completion, including navigation, information hierarchy, decisions, feedback and recovery. For each important state, specify the trigger, visible information, available actions and next state. Cover loading, empty, validation, denied access, partial success, interruption, offline behavior and conflicting edits when exercised by the product.

Distinguish server-confirmed outcomes from optimistic UI. Show what remains pending after a timeout; retries must not silently duplicate consequential actions. Explain destructive actions, reversibility and recovery proportional to their consequences. Do not remove legitimate user choices or hide costs/consent to improve a conversion metric.

Design error and help content with concrete corrective actions. Plan long/localized text, number/date formats, narrow layouts, zoom, keyboard navigation, focus movement, semantic labels, reduced motion and assistive technology where relevant. Accessibility starts with design and continues through implementation; a visual mockup cannot prove it. Use current [W3C evaluation guidance](https://www.w3.org/WAI/test-evaluate/) for web work and the target platform's official guidance for native behavior.

## Resolve uncertainty with a prototype

Choose the smallest prototype that tests the unresolved decision: a flow diagram, wireframe, interactive screen, or working vertical slice. Preserve constraints such as an approved visual style or a specific platform. Use realistic synthetic content and representative edge states; never present fabricated research participants or task results as evidence.

Define the task, participant/context assumptions, observable success and the finding that would change the design. Execute available interaction checks and authorized user research, or mark them unrun. An agent walking through a prototype is useful inspection, not a substitute for observed user research. Compare alternatives only when a consequential uncertainty remains.

## Hand off and close the loop

Deliver the requested prototype or implementation plus a concise state/interaction contract: component reuse, behavior, content, responsive/input rules, accessibility expectations and unresolved decisions. Carry observable acceptance examples into implementation and verification. Product scope remains with `kk-product-spec` when available; runtime contracts remain with architecture.

Check the implemented experience against the intended task after integration. Feed observed task failures, support feedback and accessibility regressions back into design and requirements. Report precisely which devices, input methods and states were exercised; a polished screenshot is not proof of usable software.
