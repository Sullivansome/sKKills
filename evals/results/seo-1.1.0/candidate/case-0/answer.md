Prioritize the canonical mismatch (P1, high confidence).

Observed in the supplied landing.html on 2026-10-12: its canonical points to `https://preview.example.test/sketch-dash/`, while the intended public URL is `https://example.test/sketch-dash/`. This conflicting consolidation signal could favor the preview URL; actual Google selection is unknown. Change the canonical to the intended URL. Acceptance: exactly one canonical with that URL, then verify the served production HTML when deployment is separately authorized.

Observed positives: descriptive title and description, English language declaration, index/follow directive, readable main text and heading, ordinary store anchor, and platform/controls table. There is no viewport meta tag; mobile readability is a P2 check, not a proven rendering failure from this file.

Scope: saved HTML only. HTTP status, redirects, headers, robots.txt, sitemap, store destination behavior, rendered layout, performance, and indexing are unknown. No files were edited, and no live account or site was inspected.
