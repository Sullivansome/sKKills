---
name: kk-architecture-design
description: Design or review system boundaries, new API/event contracts, data models, and consequential technical choices. Use for new services or structural design decisions; use kk-software-evolution to plan changes constrained by existing data or supported consumers.
---

# Architecture Design

Choose the simplest design that satisfies the actual requirements and can evolve without hiding operational costs.

## Read the system before drawing it

Trace the current execution path and ownership boundaries. Inspect callers, schemas, jobs, infrastructure, authentication, and deployment topology relevant to the change. Separate implemented behavior from proposed behavior. Use the existing domain vocabulary; record important ambiguous terms.

Establish hard constraints: user journey, data sensitivity, expected load, latency/reliability needs, supported clients, team capacity, budget, and deployment constraints. Treat missing traffic figures as unknown; use labeled scenarios rather than fabricated forecasts.

## Compare consequential choices

For a decision expensive to reverse, compare the current approach and one or two plausible alternatives against the constraints. Explain failure behavior, migration effort, operational burden, and a trigger for revisiting the choice. Prefer the existing stack and a cohesive module until evidence justifies another service, queue, cache, framework, or generic abstraction.

Investigate unfamiliar or version-sensitive APIs in the repository and official documentation before designing around them. A generated interface is not evidence that an SDK supports it.

## Define boundaries and contracts

- State who owns each datum and invariant. Enforce important invariants in the authoritative layer, using database constraints or transactions where appropriate.
- Define API/event shapes, validation, authorization and tenant scope, error semantics, pagination, version compatibility, and producer/consumer ownership. Treat authentication and authorization as separate decisions.
- For mutations, define transaction boundaries, idempotency keys and scope, conflict handling, ordering, and behavior under retries or partial failure. Do not promise exactly-once effects merely because a queue deduplicates messages.
- For concurrency and background work, define cancellation, deadlines, bounded retries with jitter, backpressure, and poison-message handling. Account for retry amplification across layers.
- For data storage, consider index access paths, consistency, retention/deletion, migration compatibility, and restore needs. For caches, state invalidation and the source of truth.
- For infrastructure, define configuration/secret boundaries, environments, resource limits, drift handling, and ownership. Prefer reproducible configuration using the existing platform.
- For client software, consider device capability, offline/conflict behavior, accessibility, distribution constraints, and old client versions that cannot be upgraded immediately.

Choose only the concerns exercised by the change. A local utility does not need a distributed-system design review.

## Make the design falsifiable

Trace one successful request and the highest-impact failure through the design. Identify where to measure user success, diagnose failure, and recover. Estimate capacity and cost using stated assumptions, then select a benchmark or spike if a key choice depends on the estimate.

Specify compatibility during rollout, a recovery path, and what cannot be undone after new writes. Define contract/integration tests and the first vertical slice. Describe how a proposed abstraction could be removed if its assumptions do not hold.

## Deliver

Use the project's existing architecture document or a small ADR for a consequential decision: context, decision, alternatives, consequences, validation, and revisit trigger. Add a diagram only if it clarifies boundaries. Update contracts alongside code when implementation is requested. Do not equate a diagram or accepted ADR with a tested system.
