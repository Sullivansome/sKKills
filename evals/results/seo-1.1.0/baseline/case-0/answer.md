Prioritize correcting the canonical to `https://example.test/sketch-dash/` (P1, high confidence in the source defect). The saved HTML points to `https://preview.example.test/sketch-dash/`, conflicting with the intended public URL. This may direct consolidation toward the preview URL; actual indexing impact is unknown. Acceptance: the public response/rendered page has one intended canonical and no conflicting headers, redirects, or sitemap entries.

Observed in `landing.html`, inspected 2026-10-12: descriptive title and description, English language, one meaningful H1, readable game copy, an ordinary store anchor, a platform/controls table, and `index,follow`. These are positive source signals. The table's omitted optional closing tags do not by themselves establish invalid HTML or an SEO problem.

P2: the source has no viewport meta tag. Check a mobile render before deciding whether this causes a usability problem; add a viewport declaration only if supported by that check and authorized implementation.

Unknown: served HTTP status and headers, robots.txt, sitemap, whether the preview is public, Google-selected canonical/index status, store destination behavior, actual mobile rendering, performance, and traffic. No live audit or edits were performed. The saved source does not prove either indexation or deindexing.
