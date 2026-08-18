# Project Review — Overview

**Reviewed:** 2026-08-18
**Repo:** Embedded Modern C++: From Bare-Metal to STL (Complete C++ Developer Course + Study Portal)
**Audience for this review:** the course author/maintainer. Written for handoff to students who already know C and are learning modern C++ with an embedded-systems lens.

## What this repo is

Two things live side by side:

1. **`complete-cpp-developer-course-2025-main/section_1` … `section_12`** — the original Packt/Dr. John P. Baugh "Complete C++ Developer Course" solution code. Plain `.cpp`/`.h` files, one small project per folder (e.g. `PointerFun`, `DynamicDogs`, `Swapper`). No build files, no tests, no CI for this code.
2. **`embedded_cpp_study_portal/`** — a custom static-site generator (Python, data-driven: one `section_N_data.py` per section feeding a shared `builder.py`) that produces 116 project pages, a 68-term glossary, and 464 quiz questions. This is the actual teaching product — it re-frames each vanilla course exercise through an "embedded/bare-metal" lens (MMIO, AAPCS, cache lines, MISRA, etc.) and adds a "Production-Ready Embedded Refactoring" section per project.

## Why this split matters

The course code (part 1) is **desktop-oriented, C++11-ish, teaching-first code** — `using namespace std;`, raw `new`/`delete`, no `const`-correctness on template parameters, no move semantics. That's normal for an intro course. The portal (part 2) is where the "embedded boundary" content actually lives, and it's added *on top of* the raw code as narrative, not demonstrated as compiling embedded code.

That gap is the central finding of this review: **students read hardware-accurate prose next to code that never touches hardware and isn't restricted the way real embedded code is.** See `01-issues.md` for specifics.

## Files in this review folder

| File | Purpose |
|---|---|
| `00-overview.md` | this file |
| `01-issues.md` | numbered, severity-tagged findings — copy each into a GitHub issue directly |
| `02-embedded-gaps.md` | topics a C→embedded-C++ student needs that are missing or under-covered |
| `03-enhancement-roadmap.md` | prioritized recommendations, my notes for what to fix first |

Each `.md` has a matching `.html` for offline/browser reading.
