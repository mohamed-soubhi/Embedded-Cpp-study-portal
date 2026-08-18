# Embedded-Boundary Gaps for a C-Background Student

The portal's *prose* already covers most of the right vocabulary (MMIO, AAPCS, MISRA, cache lines, `alignas`). What's missing is **hands-on code and exercises** that a student who knows C but is new to C++'s embedded-safe subset actually needs to practice. Grouped by theme.

## 1. The "no exceptions / no RTTI / no heap" freestanding subset

A C programmer already writes allocation-free, no-exception code by default — that part transfers. What doesn't transfer is knowing *which C++ features quietly assume a hosted environment*. None of the 116 projects show:

- A `-fno-exceptions -fno-rtti` build actually failing/succeeding to demonstrate what breaks (e.g. `dynamic_cast`, `throw`, `typeid`).
- `std::expected`/tagged error codes used *instead of* exceptions in a full worked example (Section 7 discusses this in prose, per README, but confirm a compiling example exists — it wasn't found among the sampled files).
- A comparison of `.eh_frame`/exception-table binary bloat with `-fno-exceptions` on vs off, with real `size` output.

## 2. Static/stack-only allocation patterns

C students are used to fixed-size arrays and manual buffers. The bridge to modern C++ is `std::array`, `etl::vector`, static ring buffers — the README promises this ("static ring buffers", "etl::vector") but the sampled course code uses raw `new`/`delete` and no `std::array` at all in the files reviewed. Concretely missing:

- A worked `std::array<T, N>` vs C array vs `std::vector` comparison with a stack/heap diagram.
- A static ring buffer / circular queue implemented with `std::array`, no dynamic allocation, no `%`-based wraparound bugs.
- Placement-new into a pre-allocated static byte pool (mentioned in Section 8's topic list) shown as actual code, not just a bullet point.

## 3. `volatile` and hardware register access

Central to embedded C++ and completely new to most C-background students who never had to think about compiler reordering with peripherals. Section 8 promises this but the sampled `PointerFun` source has none of it. Needed:

- A `volatile uint32_t* const REG = reinterpret_cast<volatile uint32_t*>(0x40021000);` pattern, contrasted with a non-volatile version and an explanation of what UB/optimization bug the `volatile` prevents.
- A tiny register wrapper struct/class (`class GpioRegister { volatile uint32_t& reg; ... }`) showing RAII applied to hardware, not just heap objects.

## 4. `const`-correctness beyond "add the keyword"

C has `const`, but C++ layers `const` onto pointers, methods, and references in ways that matter for embedded (read-only Flash placement, `.rodata`). Section 8 promises "4 pointer constness permutations" and const-correctness — but the reviewed `Swapper.h` doesn't even mark its getters' parameters const-correct beyond the trivial `const` return methods, and no permutation table exists in code. Needed: one concrete file showing all four `const`/pointer combinations with an ASM/`.rodata` placement note per line.

## 5. Move semantics as "the C++ answer to C's memcpy-and-hope"

C-background students default to copy-everything thinking (that's literally how C structs work). Section 11 is the natural home for un-teaching this, but the sampled `Swapper<T>::swap()` does a plain copy-based swap. This is the single highest-leverage fix in the repo: show `std::move`, `std::swap`, and *why* it matters for embedded (avoiding a redundant SRAM copy of a large buffer/DMA descriptor).

## 6. RAII for hardware resources, not just memory

C teaches "always match your `malloc`/`free`" as manual discipline. C++'s pitch is "make the compiler do it." The README's Section 6 mentions "RAII peripheral power gating" — that's exactly the right example, but confirm it exists as compiling code (not found in the sampled files) — a `class PeripheralPowerGuard` that enables a peripheral clock in its constructor and disables it in its destructor is the canonical bridge example and should be one of the very first embedded-flavored examples students see, not buried in Section 6 of 12.

## 7. Compile-time computation (`constexpr`) as a *zero-runtime-cost* concept

C students know `#define` and enum tricks for compile-time constants but not `constexpr` functions/classes computing lookup tables at compile time with zero flash/SRAM runtime cost. This is mentioned ("constexpr bounding boxes", "constexpr tables") but should get its own small, standalone, heavily-commented project early (Section 2 or 3) rather than only appearing as an embedded-refactor suggestion later.

## 8. Interrupt-safety vocabulary

Not seen anywhere in the sampled material: `sig_atomic_t`/atomic flag patterns, ISR-safe data sharing (no locks in ISR context), or `std::atomic` in a freestanding/no-OS context. If the course is going to claim ARM Cortex-M / bare-metal framing, at least one project should touch "this variable is written by an ISR and read by main — here's what changes" (`volatile` isn't enough by itself; students conflate `volatile` with atomicity, and this is the exact repo to correct that misconception cleanly).

---

**Net summary:** the curriculum's stated topic list (README's per-section "Key Embedded & Hardware Systems Realities" column) is the right list. The gap is between *portal narrative describing these ideas* and *course/portal code actually demonstrating them compiling and running*. Closing ISSUE-02 and ISSUE-07 from `01-issues.md` would fix most of items 1–4 above as a side effect.
