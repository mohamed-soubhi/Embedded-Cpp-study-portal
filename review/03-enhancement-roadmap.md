# Enhancement Roadmap — My Notes

Prioritized by impact-to-effort for a course whose real product is the portal, not the raw solutions.

## Do first (high impact, contained effort)

1. **ISSUE-01 — add a root CMake build + CI.** This is the single highest-leverage fix. Right now nothing proves the 116 projects compile. A GitHub Actions matrix job (`cmake --build` over every `section_*/*/` folder) turns "trust me it compiles" into a green badge, and catches regressions the moment someone edits old code. Cheap: one `CMakeLists.txt` pattern reused via `file(GLOB)`, one workflow file next to the existing `deploy-pages.yml`.

2. **ISSUE-02/07 — add a real "Embedded Version" code block per project, not just refactor bullets.** This is the difference between "a portal that talks about embedded C++" and "a portal that teaches it." Don't need to rewrite all 116 — start with the ones the README foregrounds as embedded-flagship topics: Section 8 (MMIO/volatile/const), Section 7 (faults/exceptions), Section 6 (RAII peripheral gating). Three sections, highest narrative-to-code gap, highest payoff.

3. **ISSUE-04 — fix or annotate `Swapper::swap()`.** Five-minute fix, but it's sitting in exactly the section (11: Templates/STL) meant to break students of C's copy-everything habit. Small effort, direct pedagogical win.

## Do next

4. **ISSUE-03 — add a short "why this code looks like this" note wherever raw course code (heap `new`, `using namespace std`) precedes an embedded refactor.** Doesn't require code changes, just a portal template addition (one paragraph, reusable across all 116 pages) explaining the desktop-teaching-code → embedded-refactor arc explicitly instead of implicitly.

5. **Embedded gaps items 5, 6, 8 (move semantics, RAII-for-hardware, ISR-safety)** — these are the three concepts a C-background student most reliably gets wrong when moving to embedded C++, per the gap analysis. Worth a dedicated small project each rather than folding into an existing one, since they're each a genuine "here's the C mental model, here's why it's wrong for C++/embedded" moment.

## Do eventually

6. **ISSUE-05 — pytest suite for the generator.** Low current risk (single maintainer, git history shows careful incremental commits with descriptive audit messages), but worth having before the portal gets community contributions.

7. **ISSUE-06 — split oversized `section_N_data.py` files** once any one file crosses ~800 lines. Not urgent today; `section_8_data.py` at 631 lines and `glossary_data.py` at 902 lines are the ones to watch.

## What's already working well — keep doing this

- **Data-driven generator architecture** (`section_N_data.py` feeding a shared `builder.py`) is the right call — it's what makes 116 consistent pages maintainable by one person. Don't refactor this away.
- **The 5-pillar-per-project structure** (source / UML / mechanics / hardware reality / production refactor) is a genuinely good pedagogical shape — it's the *content* inside pillars 4–5 that needs the code-backing described above, not the structure itself.
- **Commit discipline** — git history shows scoped, descriptive commits (theming, then glossary, then UML diagrams, then numbering) rather than giant dumps. Keep shipping in this style; it makes ISSUE-01's CI addition low-risk to bolt on.
- **README curriculum table** is honestly the best artifact in the repo right now — it's specific, accurate about what each section covers, and is the document I'd point a prospective student to first. The fixes above are about making the *code* live up to that table, not about improving the table itself.
