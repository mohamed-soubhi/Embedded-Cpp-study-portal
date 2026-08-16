# ⚡ Modern C++ & Embedded Systems Deep-Dive Study Portal
### *An Interactive Engineering Companion & Architectural Curriculum (116 Projects)*

[![Live Study Portal](https://img.shields.io/badge/🌐_Live_Portal-GitHub_Pages-10b981?style=for-the-badge&logo=github)](https://mohamed-soubhi.github.io/The-Complete-Cpp-Developer-Course/)
[![Curriculum Projects](https://img.shields.io/badge/Projects-116_Interactive_Deep--Dives-38bdf8?style=for-the-badge&logo=c%2B%2B)](https://mohamed-soubhi.github.io/The-Complete-Cpp-Developer-Course/)
[![Quizzes](https://img.shields.io/badge/Self--Checking_MCQs-464_Questions-a855f7?style=for-the-badge)](https://mohamed-soubhi.github.io/The-Complete-Cpp-Developer-Course/)
[![Standard](https://img.shields.io/badge/Standard-C%2B%2B11%20%7C%2014%20%7C%2017%20%7C%2020-f59e0b?style=for-the-badge&logo=c%2B%2B)](https://mohamed-soubhi.github.io/The-Complete-Cpp-Developer-Course/)
[![Target](https://img.shields.io/badge/Target-ARM_Cortex--M_%7C_MISRA_C%2B%2B-ef4444?style=for-the-badge&logo=arm)](https://mohamed-soubhi.github.io/The-Complete-Cpp-Developer-Course/)
[![Release](https://img.shields.io/badge/Release-v1.0-00ff88?style=for-the-badge)](https://github.com/mohamed-soubhi/The-Complete-Cpp-Developer-Course/releases/tag/v1.0)

---

## 🚀 Live Interactive Portal

Explore the live web application here:  
👉 **[https://mohamed-soubhi.github.io/The-Complete-Cpp-Developer-Course/](https://mohamed-soubhi.github.io/The-Complete-Cpp-Developer-Course/)**

---

## 📖 About This Project

This repository hosts both the complete source code solutions for **The Complete C++ Developer Course** (Packt Publishing / Dr. John P. Baugh) and an **interactive, production-grade Study Portal**. 

The portal elevates traditional desktop C++ curriculum code into **bare-metal embedded systems engineering**, analyzing how every construct (from basic variables to templates and data structures) maps down to assembly instructions, cache hierarchies, CPU register files (ARM AAPCS), and physical hardware peripherals.

```
       ┌──────────────────────────────────────────────────────────┐
       │     Modern C++ & Embedded Systems Study Portal (v1.0)    │
       │     116 Projects • 464 Quizzes • Cyber Matrix UI         │
       └────────────────────────────┬─────────────────────────────┘
                                    │
          ┌─────────────────────────┴─────────────────────────┐
          ▼                                                   ▼
 📘 Track 1: Foundations (61 Projects)       🚀 Track 2: Advanced Systems (55 Projects)
  • Sec 1: Toolchains & Linker Scripts (2)    • Sec 7: Exceptions, Faults & MPU (9)
  • Sec 2: Data Types, Memory & UB (14)       • Sec 8: Pointers, Const & MMIO (7)
  • Sec 3: Control Flow & Pipelines (13)      • Sec 9: Streams, LittleFS & Flash (7)
  • Sec 4: Arrays, DMA & Cache Lines (11)     • Sec 10: OOP, Enums & CRTP (3)
  • Sec 5: Functions, AAPCS & Scope (15)      • Sec 11: Templates, STL & Memory (19)
  • Sec 6: OOP Foundations & Padding (6)      • Sec 12: Data Structures & Trees (10)
```

---

## ✨ Key Features of the Study Portal

1. **5-Pillar Deep-Dive per Project**:
   - 💻 **Annotated Source Code**: Full syntax-highlighted code viewers with multi-file tab switching and 1-click clipboard copy.
   - 📐 **Architecture & UML Class Model**: Complete UML Class Diagrams showcasing class hierarchies (`is-a`, `has-a`, `implements`, `composes`), stereotypes (`<<abstract>>`, `<<template>>`, `<<struct>>`, `<<enum class>>`, `<<compilation-unit>>`), member variable access specifiers (`+ public`, `- private`, `# protected`), and method signatures.
   - 📚 **Core C++ Mechanics**: Deep architectural breakdown of language rules, C++11/14/17/20 idioms, and standard compliance.
   - ⚡ **Embedded Systems & Hardware Reality**: Assembly instruction generation (Thumb-2), stack frame analysis, CPU pipeline stalls, cache locality, and register passing.
   - 💡 **Production-Ready Embedded Refactoring**: Zero-cost, MISRA-compliant, MISRA-safe alternatives (e.g. `std::string_view`, `etl::vector`, static ring buffers, `constexpr` tables, tagged error codes).
2. **Interactive MCQ Self-Checking Engine**:
   - **464 technical quiz questions** with immediate feedback and detailed explanations for self-assessment.
3. **Cyber Matrix / Terminal Emerald UI**:
   - High-contrast, dark terminal aesthetic (`#0a0e14` obsidian backdrop with `#10b981` and `#00ff88` neon accents).
   - Equal-height, symmetrical card layout with instant search across concepts (`AAPCS`, `MMIO`, `vtable`, `LittleFS`, `DMA`, `CRTP`, `alignas`).
4. **Dual-Track Categorization**:
   - Instant filtering between **Track 1: Foundations** (61 projects) and **Track 2: Advanced Systems** (55 projects).

---

## 🗂️ Complete Curriculum Roadmap (116 Projects)

### 📘 Track 1: Foundations & Core Architecture (61 Projects)

| Section | Domain Focus | Projects | Key Embedded & Hardware Systems Realities |
|---|---|:---:|---|
| **Section 1** | **Toolchains & Linkers** | **2** | Hosted vs Freestanding environments, `arm-none-eabi-gcc`, Linker scripts (`.ld`), ELF memory sections (`.text`, `.rodata`, `.data`, `.bss`), SWD/JTAG debuggers, OpenOCD. |
| **Section 2** | **Types, Variables & Memory** | **14** | Architecture-dependent `sizeof(int)`, Fixed-width integers (`<cstdint>`), Arithmetic promotion rules, Signed overflow UB, Saturating math (`QADD`), Floating-point epsilon drift, 1-byte packed bitfields, Zero-SRAM `constexpr` constants. |
| **Section 3** | **Control Flow & Branching** | **13** | ARM condition flags (APSR: N, Z, C, V), Instruction pipeline flush penalties, C++20 `[[likely]]`/`[[unlikely]]`, Cyclomatic complexity bounds (ISO 26262), Switch jump tables (`TBB`/`TBH`), Super-loops, Watchdogs, Hardware TRNG peripherals. |
| **Section 4** | **Arrays & Memory Locality** | **11** | C-array pointer decay traps, Uninitialized SRAM garbage, SIMD DSP instructions, `std::string` heap bloat vs Flash string pools (`std::string_view`), Row-major contiguity, DMA framebuffers, `std::vector` reallocation latency, `etl::vector`, Circular ring buffers. |
| **Section 5** | **Functions & AAPCS** | **15** | ARM AAPCS calling conventions (R0–R3 register passing, Link Register R14), Parameter passing (`const&`), `extern "C"` name mangling, RTOS stack hazards of recursion, Hardware CORDIC math, SysTick delays, Branchless counting, RVO, `std::span`, `[[nodiscard]]`. |
| **Section 6** | **OOP Foundations & Alignment** | **6** | Classes vs Structs, Natural alignment, Struct padding RAM waste, `alignas`, `__attribute__((packed))`, `constexpr` bounding boxes, `this` pointer in R0, RAII peripheral power gating, Solving Static Initialization Order Fiasco (Meyers Singleton). |

---

### 🚀 Track 2: Advanced Systems, Real-Time Hardware & Memory (55 Projects)

| Section | Domain Focus | Projects | Key Embedded & Hardware Systems Realities |
|---|---|:---:|---|
| **Section 7** | **Exceptions & Fault Systems** | **9** | ARM Cortex-M Hardware Faults (`HardFault`, `MemManage`, `BusFault`), `.eh_frame` DWARF ROM bloat (15–40KB penalty), 1-byte tagged error enums, Invariant enforcement, Stack unwinding latency jitter vs `std::expected<T, E>`, Analog Watchdog (AWD), Constructor exception hazards. |
| **Section 8** | **Pointers & Memory Access** | **7** | Memory-Mapped I/O (MMIO), `volatile` hardware register wrappers, 4 pointer constness permutations, Flash ROM `.rodata` placement, Heap fragmentation hazards, Placement-new in pre-allocated static pools, Flat Array-of-Structures (AoS), Deterministic fixed-block allocators. |
| **Section 9** | **Streams & Flash File Systems** | **7** | `std::ifstream`/`ofstream` lifecycles, LittleFS & FatFS on Quad-SPI NOR Flash, Dynamic wear leveling, Power-cut corruption resilience, Circular EEPROM event rings, Multi-sensor timestamp synchronization, Static histogram bins, `<iomanip>` vs `snprintf`, Hardware CRC32. |
| **Section 10** | **OOP, Enums & Polymorphism** | **3** | Scoped enum classes (`uint8_t`), Bitmask operations, Switch jump tables, Abstract classes, VTable & VPtr RAM overhead (4 bytes/object), Disabling RTTI (`-fno-rtti`), Curiously Recurring Template Pattern (CRTP) for zero-cost static polymorphism, Virtual destructors. |
| **Section 11** | **Templates & STL Mastery** | **19** | `std::unique_ptr` exclusive ownership & zero memory overhead, Custom RAII deleters for hardware peripherals, Rule of Three/Five/Zero, `std::map` Red-Black tree heap fragmentation vs cache-friendly sorted flat maps, FIFO queues, Erase-Remove idiom, Template bloat mitigation (`-Wtemplates`). |
| **Section 12** | **Data Structures Deep-Dive** | **10** | ArrayQueue, ArrayList, ArrayStack, LinkedChain, LinkedList, LinkedQueue, LinkedStack, ListStack, Templated ArrayStack, Proj12.2 — analyzed for worst-case time complexity, cache lines, pointer chasing, and deterministic embedded safety. |

---

## 🛠️ Local Development & Portal Generation

The study portal is built with a fast, dependency-free Python static generator and Vanilla HTML5/CSS3/JavaScript.

```bash
# 1. Clone the repository
git clone https://github.com/mohamed-soubhi/The-Complete-Cpp-Developer-Course.git
cd The-Complete-Cpp-Developer-Course

# 2. Navigate to the portal generator directory
cd complete-cpp-developer-course-2025-main/embedded_cpp_study_portal

# 3. Regenerate all 116 pages and the master landing index
python3 generate_all.py

# 4. Preview locally with any static web server
python3 -m http.server 8000
# Open http://localhost:8000 in your browser
```

---

## 🎓 Attribution & Upstream Acknowledgement

- **Original Course Curriculum & Projects:** Created and published by **Packt Publishing** and authored by **Dr. John P. Baugh** (*The Complete C++ Developer Course*).
- **Embedded Architecture & Interactive Study Portal:** Designed, refactored, and authored by **Mohamed Soubhi**.
- **License:** Educational & Open Reference.
