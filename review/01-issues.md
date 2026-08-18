# Review Findings — copy-paste into GitHub Issues

Severity: 🔴 High (misleads students or blocks verification) · 🟡 Medium (quality/consistency) · 🟢 Low (polish)

---

## ISSUE-01 🔴 No build system — 116 projects can't be compiled or verified

**Where:** `complete-cpp-developer-course-2025-main/section_1` … `section_12` (all projects)

**Problem:** There is no `CMakeLists.txt`, `Makefile`, `.vcxproj`, or any build file anywhere under `complete-cpp-developer-course-2025-main/section_*`. Every project is a bare folder of `.cpp`/`.h` files. A student can't `git clone` and build — they have to reverse-engineer a Visual Studio project manually, guess include paths for multi-file projects (e.g. `DroneFleet/Drone.cpp` + `Drone.h` + `main.cpp`), and there's no CI proving any of the 116 projects actually compiles.

**Fix:** Add one root `CMakeLists.txt` with a subdirectory per project (or a single generated `add_executable` per folder via `file(GLOB ...)` + loop), plus a GitHub Actions job that builds every project on push. This alone would catch stale/broken code before students hit it.

---

## ISSUE-02 🔴 Portal's embedded narrative isn't demonstrated in the actual code

**Where:** `embedded_cpp_study_portal/section_8_data.py` (MMIO/`volatile` deep-dive) vs. `section_8/PointerFun/PointerFun/main.cpp`

**Problem:** The portal page for this project talks about memory-mapped I/O, `volatile` hardware registers, ARM AAPCS register passing. The actual source it's describing is:

```cpp
int myLovelyInt = 150;
int* somePtr = &myLovelyInt;
cout << "pointer holds value: " << somePtr << endl;
```

Plain heap-free pointer demo, `<iostream>`, zero hardware content. The embedded framing is bolted on in the portal's prose/diagrams, not shown as a `volatile uint32_t* const REG = (volatile uint32_t*)0x4002...;` example anywhere. A student who reads the portal page and then opens the linked source will find the two don't visibly connect — the connection is asserted, not shown.

**Fix:** For each project, add a *second* code sample in the portal ("Embedded version") that is real, compilable, freestanding-flavored C++ illustrating the concept discussed — not just refactoring bullet points. `section_8`, `section_7` (faults/MPU), and `section_9` (LittleFS/flash) are the projects where this gap is most visible because the desktop code has nothing structurally in common with the embedded claims.

---

## ISSUE-03 🟡 Raw course code teaches patterns the portal tells students to avoid

**Where:** `section_8/DynamicFun/DynamicFun/main.cpp`, most `main.cpp` files across all sections

**Problem:**
```cpp
int* myIntPtr = new int;
delete myIntPtr;
myIntPtr = nullptr;
```
and `using namespace std;` at file scope in nearly every `main.cpp`. Meanwhile the portal's own "Production-Ready Embedded Refactoring" pillar tells students to avoid heap allocation and prefer RAII/smart pointers. The base code the student actually reads and runs contradicts the lesson the portal teaches about it two clicks later.

**Fix:** Not asking to rewrite Packt's original solutions (that'd break attribution/fidelity to the course). Instead: in the portal's "Core C++ Mechanics" or refactoring section, explicitly call out *why* the shown code uses raw `new`/`using namespace std`, and mark it "desktop-teaching-code, not embedded-safe" rather than silently jumping to the embedded refactor. Right now the jump from raw→refactored looks unmotivated to a student who hasn't been told the raw code is the "before," not the target.

---

## ISSUE-04 🟡 Template code shown without move semantics in the STL/templates section

**Where:** `section_11/SwapperTest/SwapperTest/Swapper.h`

**Problem:**
```cpp
template <class T>
void Swapper<T>::swap() {
    T temp = first;
    first = second;
    second = temp;
}
```
Section 11 is billed as "Templates, STL & Memory" and covers `std::unique_ptr`, Rule of Three/Five/Zero elsewhere — but this specific class does a copy-based swap with no `std::move`, right in the section that's supposed to be teaching move semantics and STL idioms. For a student moving from C, this reads as "that's just how C++ swap works," reinforcing a copy-heavy mental model exactly where the course should be breaking it.

**Fix:** Either fix `Swapper<T>::swap()` to use `std::move`, or if intentionally left naive as a teaching contrast, add a comment/portal callout: "this copies — see std::swap / move semantics for the zero-copy version."

---

## ISSUE-05 🟡 No tests anywhere in the repository

**Where:** whole repo

**Problem:** Zero unit tests for the 116 course projects, and none for the portal generator itself (`builder.py`, `generator.py`, `section_*_data.py`). The portal's own generation pipeline (`generate_all.py`) has no regression check beyond "0 audit errors" mentioned in a commit message — i.e. someone eyeballed it once. A broken `section_N_data.py` edit (bad HTML escaping, broken quiz answer key, etc.) would ship silently.

**Fix:** For the course code: not critical (see ISSUE-01, a build-only CI check covers the main risk). For the portal generator: add a small pytest suite that runs `generate_all.py` against a temp dir and asserts (a) exit code 0, (b) every section's page count matches its data file's project count, (c) no unescaped `{{` placeholders leak into output HTML.

---

## ISSUE-06 🟢 Generator files will exceed maintainable size as content grows

**Where:** `embedded_cpp_study_portal/glossary_data.py` (902 lines), `section_8_data.py` (631 lines), `builder.py` (581 lines)

**Problem:** These are single flat files holding large embedded dicts/strings. Currently fine, but `section_N_data.py` for the bigger sections (11 has 19 projects, 12 has 10) will keep growing, and there's no per-project file split. At 800+ lines a single bad edit is hard to diff/review.

**Fix:** Not urgent. If sections keep growing, split `section_N_data.py` into `section_N/<project_id>.py` fragments imported into a dict, same pattern already used for the `section_N/` HTML output folders.

---

## ISSUE-07 🟢 `PointerFun` (and similar single-file demos) have no header/const-correctness examples

**Where:** `section_8/PointerFun/PointerFun/main.cpp`

**Problem:** No `const int*` vs `int* const` vs `const int* const` demonstrated in code, even though `section_8`'s own portal topic list promises "4 pointer constness permutations." The four permutations are explained in prose on the portal page but not exercised in the compilable source.

**Fix:** Add the four-permutation snippet directly into `PointerFun/main.cpp` (or a new small project) so the portal's claim and the code line up 1:1.
