---
name: kk-security-review
description: Threat-model or review application, infrastructure, dependency, and AI-agent trust boundaries; implement scoped mitigations and security regression tests when requested. Use for sensitive data, authentication/authorization changes, exposed APIs, supply-chain risks, or security readiness reviews.
---

# Security Review

Find exploitable paths and reduce risk with concrete controls. Scope the review to the requested system and authorized environments; a checklist or clean scanner result is not a security guarantee.

## Map what needs protecting

Inspect relevant code, architecture, dependencies, configuration, and deployment permissions. Identify assets, data classification, actors, entry points, tenant boundaries, privileged operations, and external services. Trace one normal request and one abuse path. State what is outside the review and what cannot be inspected.

Use a lightweight threat table: asset/boundary, adversary capability, concrete abuse path, existing control, evidence, impact, mitigation, and verification. Do not assign severity from a keyword alone; assess exploitability and affected users.

## Examine the relevant paths

- **Identity and authorization:** server-side checks on every protected operation, object and tenant scope, role changes, session invalidation, recovery flows, and default denial. A hidden UI control is not authorization.
- **Input and output:** injection, unsafe deserialization, path traversal, SSRF and outbound destinations, file upload handling, output encoding, and unsafe rendering. Validate at boundaries with appropriate libraries and parameterization.
- **Secrets and data:** storage, transport, least privilege, logging/redaction, retention and deletion, backup access, and third-party disclosure. Do not print live secrets to prove exposure; use redacted evidence and arrange rotation for confirmed compromise.
- **Business abuse:** replay, duplicate mutations, race conditions, resource exhaustion, enumeration, and bypassed workflow transitions. Rate limiting does not replace authorization or transactional invariants.
- **Dependencies and builds:** verify package identity and actual versions, advisories and reachable usage, licenses and provenance where distribution requires them. Inspect install scripts, update sources, lockfiles, CI token scope, and untrusted-code execution. Prefer verified immutable action references and short-lived scoped credentials where supported.
- **AI and agent boundaries:** retrieved content and model output are untrusted; prompts are not an access-control mechanism. Enforce per-user permissions, argument schemas, destination restrictions, side-effect authorization, and bounded execution outside the model. Test indirect prompt injection and attempted data/tool privilege escalation.

Use current official advisories and platform documentation for version-sensitive claims. Do not claim a dependency is safe solely because it is popular or a scanner has no finding. Avoid custom cryptography and improvised authentication protocols.

## Verify mitigations

Prefer minimal safe local reproductions using synthetic data. Do not probe unrelated systems, exfiltrate real records, or perform destructive production tests. Apply requested fixes at the authoritative boundary, then test normal use plus denied/abusive inputs. Check that fixes preserve legitimate access and fail safely.

When scanning, scope tools and report their coverage and blind spots. Triage findings rather than dumping raw scanner output. Preserve evidence for incident handling if active compromise is suspected; use incident response for containment rather than treating it as routine cleanup.

## Deliver

Report concrete findings ordered by risk, with location, abuse preconditions, impact, evidence, fix, and validation. Separate confirmed defects from hypotheses. Record accepted residual risks only if an actual owner accepted them; otherwise mark unresolved. Do not infer regulatory compliance from this review.

For deeper guidance, consult [NIST SSDF](https://csrc.nist.gov/pubs/sp/800/218/final) for secure development activities, [GitHub secure workflow use](https://docs.github.com/en/actions/reference/security/secure-use) for CI trust boundaries, and [OWASP prompt injection prevention](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html) for AI threat details. Load only what the task needs.
