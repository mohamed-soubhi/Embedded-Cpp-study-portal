#!/usr/bin/env python3
"""
Technical Glossary Data Model for Modern C++ & Embedded Systems Study Portal.
Contains curated definitions, architectural hardware context, and cross-project references
for keywords, acronyms, registers, and low-level paradigms across all 12 sections.
"""

GLOSSARY_CATEGORIES = {
    "all": "All Terms",
    "embedded-hw": "⚡ Embedded & CPU Architecture",
    "cpp-idiom": "📚 Modern C++ Mechanics & Idioms",
    "memory-storage": "💾 Memory, Storage & Real-Time",
    "toolchain-standards": "🛡️ Toolchains, Linkers & Safety Standards",
    "data-structures": "📐 Data Structures & Algorithms",
}

GLOSSARY_TERMS = [
    {
        "id": "aapcs",
        "term": "AAPCS",
        "expansion": "ARM Architecture Procedure Call Standard",
        "category": "embedded-hw",
        "tags": ["ARM Cortex-M", "Calling Convention", "Registers", "ABI"],
        "definition": "The official ABI standard governing how subroutines and functions pass parameters, return values, and preserve registers in ARM processors.",
        "hardware_relevance": "Under AAPCS, the first 4 integer or pointer arguments (up to 32 bits each) are passed directly in CPU registers R0–R3 without touching RAM. Return values are passed in R0 (and R1 for 64-bit). The return address is stored in the Link Register (R14/LR). Keeping function parameter counts to 4 or fewer eliminates stack memory push/pop overhead completely.",
        "related_sections": [
            {"title": "Sec 5: Functions & AAPCS", "url": "section_5/function_fun_1.html"},
            {"title": "Sec 5: Parameter Schemes", "url": "section_5/passing_schemes.html"}
        ]
    },
    {
        "id": "adl",
        "term": "ADL",
        "expansion": "Argument-Dependent Lookup (Koenig Lookup)",
        "category": "cpp-idiom",
        "tags": ["C++ Language", "Name Lookup", "Namespaces", "STL"],
        "definition": "A C++ compiler name lookup rule that searches the namespaces of a function's arguments in addition to the local scope when resolving unqualified function calls.",
        "hardware_relevance": "Enables idiomatic, zero-cost customization points such as <code>swap(a, b)</code> (which selects specialized hardware or container swap functions before falling back to <code>std::swap</code>) and overloaded stream/math operators without requiring explicit namespace prefixes.",
        "related_sections": [
            {"title": "Sec 11: Advanced STL", "url": "section_11/advanced_stl_app.html"},
            {"title": "Sec 11: Remove-Erase Idiom", "url": "section_11/remove_erase_idiom.html"}
        ]
    },
    {
        "id": "alignas-alignof",
        "term": "alignas / alignof",
        "expansion": "Memory Alignment Specifier & Operator",
        "category": "cpp-idiom",
        "tags": ["C++11", "Memory Alignment", "DMA", "Cache Line"],
        "definition": "<code>alignas</code> forces a variable or struct to align on a specific byte boundary in memory. <code>alignof</code> queries the natural alignment requirements of a given type.",
        "hardware_relevance": "Hardware peripherals such as DMA controllers, cache lines (typically 32 or 64 bytes), and vector units require buffers to be placed at specific memory boundaries (e.g. <code>alignas(32) uint8_t dma_buf[512];</code>). Misaligned memory accesses on ARM Cortex-M0/M3 can trigger hardware usage faults or require multi-cycle bus transactions.",
        "related_sections": [
            {"title": "Sec 6: OOP & Struct Alignment", "url": "section_6/book_fun.html"},
            {"title": "Sec 4: DMA & Arrays", "url": "section_4/array_fun.html"}
        ]
    },
    {
        "id": "apsr",
        "term": "APSR",
        "expansion": "Application Program Status Register",
        "category": "embedded-hw",
        "tags": ["ARM Cortex-M", "ALU", "Condition Flags", "Branching"],
        "definition": "The hardware CPU status register that contains the arithmetic condition flags resulting from the most recent ALU operation.",
        "hardware_relevance": "Holds the Negative (N), Zero (Z), Carry (C), Overflow (V), and Q (Saturation) flags. Conditional branch instructions (<code>BEQ</code>, <code>BNE</code>, <code>BGT</code>, <code>BLT</code>) directly evaluate these flags to make zero-latency branch decisions. Mispredicting or stalling conditional checks causes CPU pipeline bubbles.",
        "related_sections": [
            {"title": "Sec 3: Control Flow & Flags", "url": "section_3/control_statements_intro.html"},
            {"title": "Sec 3: Selection Fun", "url": "section_3/selection_fun.html"}
        ]
    },
    {
        "id": "aos-vs-soa",
        "term": "AoS vs SoA",
        "expansion": "Array of Structures vs Structure of Arrays",
        "category": "memory-storage",
        "tags": ["Data Layout", "SIMD", "Cache Lines", "Performance"],
        "definition": "Two distinct memory organization patterns: AoS stores complete struct objects consecutively in memory; SoA separates each struct field into its own contiguous parallel array.",
        "hardware_relevance": "In embedded DSP and graphics processing, SoA maximizes cache locality when algorithms only read one or two specific fields across all elements (e.g. updating only X coordinates), enabling contiguous burst reads and SIMD execution without loading unused padding bytes.",
        "related_sections": [
            {"title": "Sec 8: Dynamic Arrays & Layout", "url": "section_8/dynamic_array_test.html"},
            {"title": "Sec 4: 2D Arrays", "url": "section_4/2d_array_fun.html"}
        ]
    },
    {
        "id": "autosar-cpp",
        "term": "AUTOSAR C++14",
        "expansion": "Automotive Open System Architecture C++ Guidelines",
        "category": "toolchain-standards",
        "tags": ["Automotive", "Safety-Critical", "MISRA", "ISO 26262"],
        "definition": "An authoritative coding standard for using Modern C++ (C++14) in safety-critical automotive systems (e.g. ADAS, engine controllers, braking ECUs).",
        "hardware_relevance": "Strictly forbids non-deterministic runtime operations including raw <code>new/delete</code>, dynamic exceptions without bounded catch times, recursion (due to stack overflow risk), and unbounded loops. Mandates static allocation, deterministic response times, and static analysis enforcement.",
        "related_sections": [
            {"title": "Sec 11: Smart Pointers & AUTOSAR", "url": "section_11/smart_pointer_fun.html"},
            {"title": "Sec 7: Faults & Exceptions", "url": "section_7/bug_fun.html"}
        ]
    },
    {
        "id": "branch-pipeline",
        "term": "Branch Prediction & Pipeline Flush",
        "expansion": "CPU Instruction Pipeline Flushes & Branch Penalties",
        "category": "embedded-hw",
        "tags": ["CPU Architecture", "Pipeline", "Thumb-2", "Optimization"],
        "definition": "When a CPU encounters a conditional jump (<code>if/else</code>, <code>switch</code>), branch prediction attempts to speculate the next instruction. If mispredicted, the processor must flush all instructions in the pipeline and reload from the jump target.",
        "hardware_relevance": "In Cortex-M3/M4/M7 processors with 3-to-6 stage pipelines, every mispredicted branch incurs a 2-to-5 clock cycle penalty. In high-frequency interrupt service routines (ISRs) and tight DSP loops, branchless code and C++20 <code>[[likely]]/[[unlikely]]</code> annotations eliminate costly pipeline stalls.",
        "related_sections": [
            {"title": "Sec 3: Control Statements", "url": "section_3/control_statements_intro.html"},
            {"title": "Sec 3: Branching Optimization", "url": "section_3/selection_fun.html"}
        ]
    },
    {
        "id": "bss-section",
        "term": ".bss Section",
        "expansion": "Block Started by Symbol",
        "category": "toolchain-standards",
        "tags": ["ELF", "Linker", "Memory Sections", "SRAM"],
        "definition": "A memory section in compiled ELF binaries dedicated to uninitialized global and static variables.",
        "hardware_relevance": "The <code>.bss</code> section occupies 0 bytes in Flash ROM storage. During startup before <code>main()</code> runs, the CRT0 startup code zeroes out the entire <code>.bss</code> RAM region in a tight loop. Grouping zero-initialized buffers into <code>.bss</code> saves vital Flash space.",
        "related_sections": [
            {"title": "Sec 1: Linker Scripts & Sections", "url": "section_1/hello.html"},
            {"title": "Sec 2: Variables & Memory", "url": "section_2/variable_fun.html"}
        ]
    },
    {
        "id": "busfault",
        "term": "BusFault",
        "expansion": "ARM Cortex-M Bus Error Exception",
        "category": "embedded-hw",
        "tags": ["Fault Handling", "ARM Cortex-M", "AHB/APB", "Hardware Error"],
        "definition": "A hardware CPU fault triggered when an error occurs during an instruction fetch or data access on the processor's system bus (AHB/APB).",
        "hardware_relevance": "Commonly caused by dereferencing invalid memory addresses, accessing unclocked hardware peripherals (forgetting to enable the APB peripheral clock in RCC registers), or attempting unaligned 32-bit accesses on strict buses. Logged in the BusFault Status Register (BFSR).",
        "related_sections": [
            {"title": "Sec 7: Hardware Faults & Exceptions", "url": "section_7/bug_fun.html"},
            {"title": "Sec 8: Pointer Safety & MMIO", "url": "section_8/pointer_fun.html"}
        ]
    },
    {
        "id": "cache-line",
        "term": "Cache Line & Locality",
        "expansion": "Spatial and Temporal CPU Cache Memory Blocks",
        "category": "memory-storage",
        "tags": ["Cache", "SRAM", "Locality", "Performance"],
        "definition": "The fundamental unit of data transfer between main memory (SRAM/DRAM) and CPU L1/L2 cache (typically 32 or 64 bytes).",
        "hardware_relevance": "When a single byte is accessed, the hardware cache controller loads the entire 32- or 64-byte line. Sequential array traversals exhibit high spatial locality (cache hits), running at ~1 cycle per access. In contrast, linked lists and pointer chasing cause frequent cache misses, stalling the CPU for 10-100+ cycles per dereference.",
        "related_sections": [
            {"title": "Sec 4: Arrays & Memory Locality", "url": "section_4/array_fun.html"},
            {"title": "Sec 12: Data Structures & Cache", "url": "section_12/array_list_app.html"}
        ]
    },
    {
        "id": "constexpr-consteval",
        "term": "constexpr / consteval / constinit",
        "expansion": "Compile-Time Evaluation & Initialization Qualifiers",
        "category": "cpp-idiom",
        "tags": ["C++11/14/20", "Zero-SRAM", "Flash ROM", "Optimization"],
        "definition": "<code>constexpr</code> marks values or functions that can be computed at compile-time. <code>consteval</code> guarantees immediate compile-time execution. <code>constinit</code> ensures static initialization without dynamic startup code.",
        "hardware_relevance": "Precomputing mathematical tables (trigonometric LUTs, CRC tables, state machine transitions) at compile time consumes zero runtime CPU cycles and places the result directly in Flash ROM (<code>.rodata</code>), eliminating RAM consumption and boot-time calculation overhead.",
        "related_sections": [
            {"title": "Sec 2: Constants & Compile-Time", "url": "section_2/constant_fun.html"},
            {"title": "Sec 5: Math & CORDIC", "url": "section_5/math_fun.html"}
        ]
    },
    {
        "id": "cordic",
        "term": "CORDIC",
        "expansion": "Coordinate Rotation Digital Computer",
        "category": "embedded-hw",
        "tags": ["Hardware Accelerator", "Trigonometry", "DSP", "ARM"],
        "definition": "A hardware iterative algorithm / coprocessor used in embedded microcontrollers (e.g. STM32G4) to compute trigonometric, hyperbolic, and logarithmic functions using only additions and bit-shifts.",
        "hardware_relevance": "Provides single-cycle or fixed microcode computation of <code>sin()</code>, <code>cos()</code>, <code>atan2()</code>, and polar-to-Cartesian conversions without requiring costly floating-point Taylor series approximations or large RAM lookup tables.",
        "related_sections": [
            {"title": "Sec 5: Math & CORDIC Acceleration", "url": "section_5/math_fun.html"},
            {"title": "Sec 2: Arithmetic Mechanics", "url": "section_2/arithmetic_fun.html"}
        ]
    },
    {
        "id": "crtp",
        "term": "CRTP",
        "expansion": "Curiously Recurring Template Pattern",
        "category": "cpp-idiom",
        "tags": ["C++ Templates", "Static Polymorphism", "Zero-Cost", "VTable-Free"],
        "definition": "A C++ template design idiom where a derived class inherits from a base class template instantiated with the derived class itself as a template argument (<code>class Derived : public Base&lt;Derived&gt;</code>).",
        "hardware_relevance": "Provides polymorphic interface behavior at compile time without any virtual functions. This completely avoids the VTable and VPtr RAM overhead (saving 4 bytes per object) and enables full function inlining, eliminating indirect jump instruction delays.",
        "related_sections": [
            {"title": "Sec 10: OOP & CRTP Refactoring", "url": "section_10/animal_fun.html"},
            {"title": "Sec 11: Templates Deep-Dive", "url": "section_11/templates.html"}
        ]
    },
    {
        "id": "cyclomatic-complexity",
        "term": "Cyclomatic Complexity",
        "expansion": "McCabe Software Complexity Metric (ISO 26262 / MISRA)",
        "category": "toolchain-standards",
        "tags": ["Safety Standards", "Testing", "Control Flow", "MISRA"],
        "definition": "A quantitative software metric measuring the number of linearly independent paths through a program's source code.",
        "hardware_relevance": "Safety standards like ISO 26262 (automotive) and IEC 61508 (industrial) mandate a cyclomatic complexity threshold (typically $\\le 10$ to $15$ per function). Lower complexity ensures every branch path can be fully tested with 100% MC/DC (Modified Condition/Decision Coverage) on target hardware.",
        "related_sections": [
            {"title": "Sec 3: Control Flow & Complexity", "url": "section_3/selection_fun.html"},
            {"title": "Sec 5: Functions & Scope", "url": "section_5/scope_fun.html"}
        ]
    },
    {
        "id": "data-section",
        "term": ".data Section",
        "expansion": "Initialized Data Memory Section",
        "category": "toolchain-standards",
        "tags": ["ELF", "Linker", "Memory Sections", "Flash & SRAM"],
        "definition": "The memory section holding global and static variables that are explicitly initialized to non-zero values (e.g. <code>int sensor_baud = 115200;</code>).",
        "hardware_relevance": "Requires dual storage: the initial values are stored in non-volatile Flash ROM (LMA - Load Memory Address). At startup, the reset handler copies these values byte-for-byte from Flash into volatile SRAM (VMA - Virtual Memory Address). Minimizing non-const globals directly reduces boot time and SRAM usage.",
        "related_sections": [
            {"title": "Sec 1: Linker Scripts", "url": "section_1/hello.html"},
            {"title": "Sec 2: Variables & Storage", "url": "section_2/variable_fun.html"}
        ]
    },
    {
        "id": "dma",
        "term": "DMA",
        "expansion": "Direct Memory Access Controller",
        "category": "embedded-hw",
        "tags": ["Hardware Peripheral", "Bus Master", "Zero-CPU", "Buffers"],
        "definition": "A dedicated hardware engine on microcontrollers that transfers data directly between peripherals (ADC, SPI, UART) and memory (SRAM) without CPU intervention.",
        "hardware_relevance": "Allows multi-kilobyte sensor or audio data streams to be received in circular ring buffers in the background while the CPU sleeps in low-power mode (WFI) or executes other real-time tasks. Requires contiguous, properly aligned memory buffers.",
        "related_sections": [
            {"title": "Sec 4: Arrays & DMA Buffers", "url": "section_4/array_fun.html"},
            {"title": "Sec 9: Streams & Buffering", "url": "section_9/file_output_fun.html"}
        ]
    },
    {
        "id": "dwarf-eh-frame",
        "term": "DWARF / .eh_frame",
        "expansion": "Debugging Format & Exception Unwinding Table",
        "category": "toolchain-standards",
        "tags": ["Compilers", "Exceptions", "ROM Overhead", "DWARF"],
        "definition": "The metadata format embedded in binaries to describe stack frames, local variable offsets, and exception handling unwinding instructions.",
        "hardware_relevance": "Enabling C++ exceptions generates the <code>.eh_frame</code> and <code>.gcc_except_table</code> sections in Flash ROM, causing a 15KB–40KB ROM code size penalty on 32-bit MCUs even if no exception is ever thrown. For this reason, bare-metal systems commonly compile with <code>-fno-exceptions</code>.",
        "related_sections": [
            {"title": "Sec 7: Exceptions & Faults", "url": "section_7/custom_exceptions.html"},
            {"title": "Sec 1: Toolchains & Linkers", "url": "section_1/hello.html"}
        ]
    },
    {
        "id": "eeprom",
        "term": "EEPROM",
        "expansion": "Electrically Erasable Programmable Read-Only Memory",
        "category": "memory-storage",
        "tags": ["Non-Volatile", "Storage", "Hardware", "Endurance"],
        "definition": "A non-volatile storage technology that allows individual bytes to be erased and rewritten repeatedly (typically rated for 100,000 to 1,000,000 write cycles).",
        "hardware_relevance": "Used for persistent configuration parameters, device serial numbers, and calibration offsets. Writes require significant time (3–10ms per byte) and block or require non-blocking I2C/SPI drivers with CRC checks.",
        "related_sections": [
            {"title": "Sec 9: Flash & Storage Streams", "url": "section_9/file_input_fun.html"},
            {"title": "Sec 8: Const Correctness", "url": "section_8/const_correctness.html"}
        ]
    },
    {
        "id": "elf",
        "term": "ELF",
        "expansion": "Executable and Linkable Format",
        "category": "toolchain-standards",
        "tags": ["Toolchain", "Linker", "Binary Format", "Embedded"],
        "definition": "The standard binary file format generated by cross-compilers (e.g. <code>arm-none-eabi-gcc</code>) containing compiled code, symbols, section headers, and debug data.",
        "hardware_relevance": "ELF files are processed by <code>objcopy</code> to generate flat binary (<code>.bin</code>) or Intel Hex (<code>.hex</code>) files for flashing directly onto physical microcontroller flash memory via JTAG/SWD debuggers.",
        "related_sections": [
            {"title": "Sec 1: Toolchains & Linker Scripts", "url": "section_1/hello.html"},
            {"title": "Sec 1: VS Code Toolchain Setup", "url": "section_1/vsc_hello.html"}
        ]
    },
    {
        "id": "erase-remove-idiom",
        "term": "Erase-Remove Idiom",
        "expansion": "STL Container Element Removal Pattern",
        "category": "data-structures",
        "tags": ["STL", "C++11/20", "std::vector", "Optimization"],
        "definition": "A C++ standard idiom combining <code>std::remove()</code> (which shifts valid elements to the front) with <code>container.erase()</code> (which adjusts container size) in a single linear $O(N)$ pass.",
        "hardware_relevance": "Avoids quadratic $O(N^2)$ memory copying that occurs when erasing elements individually in a naive loop. In C++20, replaced by the cleaner non-member <code>std::erase(vec, value)</code>.",
        "related_sections": [
            {"title": "Sec 11: Remove-Erase Idiom", "url": "section_11/remove_erase_idiom.html"},
            {"title": "Sec 11: STL Algorithms", "url": "section_11/algorithm_fun.html"}
        ]
    },
    {
        "id": "etl-vector",
        "term": "etl::vector",
        "expansion": "Embedded Template Library Fixed-Capacity Vector",
        "category": "data-structures",
        "tags": ["ETL", "Zero-Heap", "Deterministic", "MISRA"],
        "definition": "A container from the Embedded Template Library (ETL) that provides the full API of <code>std::vector</code> but stores elements in a statically allocated buffer with a fixed maximum capacity.",
        "hardware_relevance": "Guarantees zero heap allocation, eliminates memory fragmentation risks, ensures deterministic execution time, and provides MISRA/AUTOSAR compliance for safety-critical real-time applications.",
        "related_sections": [
            {"title": "Sec 4: Vector Fun & Fixed Allocations", "url": "section_4/vector_fun.html"},
            {"title": "Sec 11: Advanced STL", "url": "section_11/advanced_stl_app.html"}
        ]
    },
    {
        "id": "fatfs",
        "term": "FatFS",
        "expansion": "FAT File System Module for Embedded Microcontrollers",
        "category": "memory-storage",
        "tags": ["File System", "SD Card", "Storage", "FAT32"],
        "definition": "A lightweight, generic FAT/exFAT file system module designed specifically for resource-constrained 8/16/32-bit microcontrollers.",
        "hardware_relevance": "Enables microcontrollers to read and write SD cards, USB drives, and eMMC chips interoperably with PC operating systems (Windows, Linux, macOS) using standard FAT formats.",
        "related_sections": [
            {"title": "Sec 9: File Streams & Storage", "url": "section_9/file_input_fun.html"},
            {"title": "Sec 9: Student Roster Files", "url": "section_9/student_roster.html"}
        ]
    },
    {
        "id": "fixed-block-allocator",
        "term": "Fixed-Block Memory Pool Allocator",
        "expansion": "Deterministic Fixed-Size Pool Allocator",
        "category": "memory-storage",
        "tags": ["Memory Management", "Real-Time", "Zero-Fragmentation", "Deterministic"],
        "definition": "A custom memory allocator that divides a pre-allocated static RAM buffer into equal, fixed-size blocks (e.g. 64 bytes each) managed via a free-list.",
        "hardware_relevance": "Provides deterministic $O(1)$ allocation and deallocation without searching or splitting blocks. Completely prevents external memory fragmentation, making it safe for long-running embedded systems.",
        "related_sections": [
            {"title": "Sec 8: Dynamic Memory & Pools", "url": "section_8/dynamic_fun.html"},
            {"title": "Sec 8: Pointer Mechanics", "url": "section_8/pointer_fun.html"}
        ]
    },
    {
        "id": "flash-memory",
        "term": "Flash Memory (NOR / QSPI)",
        "expansion": "Non-Volatile NOR Flash & Quad-SPI Serial Flash",
        "category": "memory-storage",
        "tags": ["Flash ROM", "QSPI", "Execute-in-Place (XIP)", "Non-Volatile"],
        "definition": "Non-volatile semiconductor storage where code and static read-only data are stored. NOR Flash supports random-access byte reading, enabling Execute-in-Place (XIP).",
        "hardware_relevance": "Flash must be erased in entire sectors or blocks before new data can be written (turning 1s into 0s on write, and resetting to 1s on erase). Write operations are orders of magnitude slower than SRAM and wear down cells over time.",
        "related_sections": [
            {"title": "Sec 9: Streams & Flash Storage", "url": "section_9/file_output_fun.html"},
            {"title": "Sec 1: Linker Scripts & Flash", "url": "section_1/hello.html"}
        ]
    },
    {
        "id": "flat-map",
        "term": "Flat Map / Sorted Flat Vector",
        "expansion": "Contiguous Associative Sorted Container",
        "category": "data-structures",
        "tags": ["Cache Locality", "Binary Search", "Zero-Heap", "C++23 std::flat_map"],
        "definition": "An associative key-value container implemented as a single contiguous array sorted by key, performing lookups via binary search (<code>std::lower_bound</code>).",
        "hardware_relevance": "Provides $O(\\log N)$ lookup with optimal cache locality because elements are stored contiguously in memory, avoiding the pointer-chasing overhead and 24-byte per-node heap bloat of Red-Black trees (<code>std::map</code>).",
        "related_sections": [
            {"title": "Sec 11: Map vs Unordered Map", "url": "section_11/map_vs_unordered_map.html"},
            {"title": "Sec 12: List Search", "url": "section_12/array_list_app.html"}
        ]
    },
    {
        "id": "freestanding-env",
        "term": "Freestanding vs Hosted Environment",
        "expansion": "Bare-Metal Freestanding C++ Execution Environment",
        "category": "toolchain-standards",
        "tags": ["Standard Compliance", "Bare-Metal", "No-OS", "CRT0"],
        "definition": "In C++, a hosted environment includes a full operating system with all standard library facilities (threads, files, processes), while a freestanding environment executes on bare metal without an OS.",
        "hardware_relevance": "Freestanding C++ requires custom startup code (reset handlers, CRT0), custom linker scripts, and only guarantees access to core language headers (<code>&lt;cstdint&gt;</code>, <code>&lt;cstddef&gt;</code>, <code>&lt;type_traits&gt;</code>, <code>&lt;limits&gt;</code>).",
        "related_sections": [
            {"title": "Sec 1: Toolchains & Linkers", "url": "section_1/hello.html"},
            {"title": "Sec 2: Types & Precision", "url": "section_2/hello_world.html"}
        ]
    },
    {
        "id": "hardfault",
        "term": "HardFault",
        "expansion": "ARM Cortex-M Generic Unhandled Hardware Exception",
        "category": "embedded-hw",
        "tags": ["Fault Handling", "ARM Cortex-M", "Exceptions", "Safety"],
        "definition": "The top-level hardware exception handler invoked when a fault occurs that cannot be handled by another specialized handler (or when another fault handler escalates).",
        "hardware_relevance": "Triggered by null-pointer dereferences, executing invalid opcode bytes, unaligned memory accesses when unaligned traps are enabled, or stack overflows corrupting the vector table. Inspection requires reading the HardFault Status Register (HFSR) and Configurable Fault Status Register (CFSR).",
        "related_sections": [
            {"title": "Sec 7: Hardware Faults & Exceptions", "url": "section_7/bug_fun.html"},
            {"title": "Sec 8: Dynamic Pointer Safety", "url": "section_8/dynamic_dogs.html"}
        ]
    },
    {
        "id": "heap-fragmentation",
        "term": "Heap Fragmentation",
        "expansion": "Dynamic Memory External & Internal Fragmentation",
        "category": "memory-storage",
        "tags": ["Memory Hazards", "Heap", "malloc/new", "Real-Time"],
        "definition": "The phenomenon where free heap memory is broken into many small, non-contiguous pieces over time through repeated allocations and deallocations of varying sizes.",
        "hardware_relevance": "Can cause an allocation (<code>malloc</code> or <code>new</code>) to fail even when total free RAM exceeds the requested size. In mission-critical 24/7 firmware, dynamic heap allocation is strictly avoided or restricted to system bootup.",
        "related_sections": [
            {"title": "Sec 8: Dynamic Memory", "url": "section_8/dynamic_fun.html"},
            {"title": "Sec 11: Smart Pointers", "url": "section_11/smart_pointer_fun.html"}
        ]
    },
    {
        "id": "linker-script",
        "term": "Linker Script (.ld)",
        "expansion": "GNU Linker Memory Mapping Script",
        "category": "toolchain-standards",
        "tags": ["Linker", "Memory Map", "Flash", "SRAM"],
        "definition": "A script that instructs the GNU linker (<code>ld</code>) how to map compiled sections (<code>.text</code>, <code>.rodata</code>, <code>.data</code>, <code>.bss</code>) into the microcontroller's physical memory regions (Flash ROM and SRAM).",
        "hardware_relevance": "Defines the exact origin and length of Flash and SRAM, sets the initial stack pointer address, places the interrupt vector table at address <code>0x08000000</code> or <code>0x00000000</code>, and defines memory boundaries.",
        "related_sections": [
            {"title": "Sec 1: Linker Scripts", "url": "section_1/hello.html"},
            {"title": "Sec 1: VS Code Toolchain", "url": "section_1/vsc_hello.html"}
        ]
    },
    {
        "id": "littlefs",
        "term": "LittleFS",
        "expansion": "Fail-Safe Embedded Flash File System",
        "category": "memory-storage",
        "tags": ["File System", "Flash", "Wear Leveling", "Power-Cut Resilient"],
        "definition": "A high-integrity, fail-safe file system designed specifically for microcontrollers with external SPI/QSPI NOR and NAND Flash memory.",
        "hardware_relevance": "Provides power-cut resilience (guarantees file system integrity even if power is lost mid-write), dynamic wear leveling across flash erase blocks, and bounded RAM/ROM footprints.",
        "related_sections": [
            {"title": "Sec 9: Streams & File Systems", "url": "section_9/file_input_fun.html"},
            {"title": "Sec 9: File Output Logging", "url": "section_9/file_output_fun.html"}
        ]
    },
    {
        "id": "link-register-lr",
        "term": "LR (R14)",
        "expansion": "Link Register (CPU Register R14)",
        "category": "embedded-hw",
        "tags": ["ARM Cortex-M", "Registers", "AAPCS", "Branch"],
        "definition": "The ARM CPU register used to store the return address when a function call is made via branch-with-link (<code>BL</code> or <code>BLX</code>).",
        "hardware_relevance": "Leaf functions (functions that do not call any other functions) do not need to push LR to the stack, executing with zero stack frame memory overhead and returning via a direct <code>BX LR</code> instruction.",
        "related_sections": [
            {"title": "Sec 5: AAPCS & Calling Conventions", "url": "section_5/function_fun_1.html"},
            {"title": "Sec 5: Passing Schemes", "url": "section_5/passing_schemes.html"}
        ]
    },
    {
        "id": "memmanage-fault",
        "term": "MemManage Fault",
        "expansion": "ARM Cortex-M Memory Management / MPU Fault",
        "category": "embedded-hw",
        "tags": ["Fault Handling", "MPU", "Security", "ARM Cortex-M"],
        "definition": "A hardware memory protection fault generated when an instruction or data access violates rules configured in the Memory Protection Unit (MPU).",
        "hardware_relevance": "Triggered when user-level RTOS tasks attempt to execute code in SRAM (No-Execute NX violation), write to read-only Flash, or access private memory regions belonging to another task or the kernel.",
        "related_sections": [
            {"title": "Sec 7: Exceptions & MPU", "url": "section_7/bug_fun.html"},
            {"title": "Sec 8: Dynamic Memory Safety", "url": "section_8/dynamic_dogs.html"}
        ]
    },
    {
        "id": "misra-cpp",
        "term": "MISRA C++",
        "expansion": "Motor Industry Software Reliability Association C++ Standard",
        "category": "toolchain-standards",
        "tags": ["Safety-Critical", "Automotive", "Medical", "Static Analysis"],
        "definition": "An international set of software development guidelines for writing safe, secure, and reliable C++ code in embedded and safety-critical environments.",
        "hardware_relevance": "Rules restrict unsafe C++ features such as implicit type conversions, raw pointers without bounds checks, unbounded recursion, unhandled enum switches, and memory leaks.",
        "related_sections": [
            {"title": "Sec 6: OOP & MISRA", "url": "section_6/book_fun.html"},
            {"title": "Sec 10: Enums & Type Safety", "url": "section_10/enum_fun.html"}
        ]
    },
    {
        "id": "mmio",
        "term": "MMIO",
        "expansion": "Memory-Mapped Input/Output",
        "category": "embedded-hw",
        "tags": ["Hardware Registers", "Peripherals", "Pointers", "volatile"],
        "definition": "The architectural technique where hardware peripheral registers (GPIO, UART, Timers, SPI) are mapped directly into the CPU's physical memory address space.",
        "hardware_relevance": "Reading or writing to a specific memory address (e.g. <code>*(volatile uint32_t*)0x40020000</code>) interacts directly with physical hardware pins and registers. Always requires the <code>volatile</code> qualifier to prevent the compiler from optimizing away repeated hardware reads/writes.",
        "related_sections": [
            {"title": "Sec 8: Pointer Mechanics & MMIO", "url": "section_8/pointer_fun.html"},
            {"title": "Sec 8: Const Correctness & Registers", "url": "section_8/const_correctness.html"}
        ]
    },
    {
        "id": "mpu",
        "term": "MPU",
        "expansion": "Memory Protection Unit",
        "category": "embedded-hw",
        "tags": ["Hardware Security", "Isolation", "RTOS", "ARM Cortex-M"],
        "definition": "A hardware peripheral block on ARM Cortex-M microcontrollers that divides memory into 8 or 16 programmable regions with distinct access permissions.",
        "hardware_relevance": "Enforces spatial isolation between RTOS tasks, prevents stack overflow from corrupting neighboring memory, and flags buffer overruns with immediate hardware MemManage exceptions.",
        "related_sections": [
            {"title": "Sec 7: Hardware Faults & MPU", "url": "section_7/bug_fun.html"},
            {"title": "Sec 8: Memory Access", "url": "section_8/pointer_fun.html"}
        ]
    },
    {
        "id": "natural-alignment",
        "term": "Natural Alignment & Struct Padding",
        "expansion": "Memory Byte Alignment & Padding Waste",
        "category": "memory-storage",
        "tags": ["Memory Layout", "Struct Padding", "SRAM", "Optimization"],
        "definition": "The hardware requirement that data types be placed at memory addresses that are integer multiples of their size (e.g. 4-byte <code>uint32_t</code> must be at addresses ending in 0x0, 0x4, 0x8, 0xC).",
        "hardware_relevance": "Improperly ordered struct members cause the compiler to insert padding bytes, wasting up to 50% of SRAM. Reordering members from largest to smallest eliminates padding waste without requiring packed attributes that penalize bus performance.",
        "related_sections": [
            {"title": "Sec 6: OOP & Struct Alignment", "url": "section_6/book_fun.html"},
            {"title": "Sec 2: Variables & Types", "url": "section_2/variable_fun.html"}
        ]
    },
    {
        "id": "noexcept",
        "term": "noexcept",
        "expansion": "Non-Throwing Function Specification",
        "category": "cpp-idiom",
        "tags": ["C++11", "Exceptions", "Optimization", "Move Semantics"],
        "definition": "A C++ keyword declaring that a function is guaranteed not to throw exceptions.",
        "hardware_relevance": "Allows the compiler to omit exception-handling unwinding landing pads and vector reallocation copies (enabling move-if-noexcept optimizations), significantly reducing generated code size and execution time.",
        "related_sections": [
            {"title": "Sec 7: Exceptions & Faults", "url": "section_7/custom_exceptions.html"},
            {"title": "Sec 11: Rule of Three/Five/Zero", "url": "section_11/rule_of_three_five_zero.html"}
        ]
    },
    {
        "id": "program-counter-pc",
        "term": "PC (R15)",
        "expansion": "Program Counter (CPU Register R15)",
        "category": "embedded-hw",
        "tags": ["ARM Cortex-M", "Registers", "Instruction Fetch", "CPU"],
        "definition": "The hardware register holding the memory address of the next instruction being fetched for execution.",
        "hardware_relevance": "In ARM Cortex-M Thumb-2 state, bit 0 of the PC must always be 1 to indicate Thumb execution mode; jumping to an address with bit 0 set to 0 triggers an immediate UsageFault (INVSTATE).",
        "related_sections": [
            {"title": "Sec 5: AAPCS & Execution", "url": "section_5/function_fun_1.html"},
            {"title": "Sec 3: Control Statements", "url": "section_3/control_statements_intro.html"}
        ]
    },
    {
        "id": "placement-new",
        "term": "Placement-New",
        "expansion": "In-Place Object Construction",
        "category": "cpp-idiom",
        "tags": ["Memory Management", "C++ Idiom", "Zero-Heap", "Static Pools"],
        "definition": "A form of the <code>new</code> operator (<code>new (address) ClassName(...)</code>) that constructs an object inside a pre-allocated memory buffer without performing dynamic heap allocation.",
        "hardware_relevance": "Enables object-oriented C++ classes with constructors to be instantiated inside statically allocated SRAM pools, memory-mapped peripherals, or DMA buffers with zero heap allocation.",
        "related_sections": [
            {"title": "Sec 8: Dynamic Memory & Placement New", "url": "section_8/dynamic_fun.html"},
            {"title": "Sec 8: Dynamic Dogs", "url": "section_8/dynamic_dogs.html"}
        ]
    },
    {
        "id": "pointer-decay",
        "term": "Pointer Decay",
        "expansion": "Array-to-Pointer Implicit Conversion",
        "category": "cpp-idiom",
        "tags": ["Arrays", "Pointers", "Type Safety", "std::span"],
        "definition": "The automatic conversion of a C-style array to a raw pointer to its first element when passed into a function by value, losing all compile-time size information.",
        "hardware_relevance": "A major source of buffer overflow vulnerabilities in embedded C/C++. Modern C++ replaces decayed arrays with <code>std::span&lt;T&gt;</code> or <code>std::array&lt;T, N&gt;</code> to preserve bounds information with zero runtime overhead.",
        "related_sections": [
            {"title": "Sec 4: Arrays & Pointer Decay", "url": "section_4/array_fun.html"},
            {"title": "Sec 5: Passing Schemes & Pointers", "url": "section_5/passing_schemes.html"}
        ]
    },
    {
        "id": "raii",
        "term": "RAII",
        "expansion": "Resource Acquisition Is Initialization",
        "category": "cpp-idiom",
        "tags": ["C++ Core", "Resource Management", "Hardware Locks", "Safety"],
        "definition": "A fundamental C++ design pattern where resource allocation (memory, mutex locks, hardware peripheral clocks) is tied to object lifetime via constructors and automatically released in destructors upon scope exit.",
        "hardware_relevance": "Guarantees that hardware peripherals (SPI buses, DMA channels, interrupts) are safely closed, disabled, or unlocked even when functions exit early due to return statements or errors.",
        "related_sections": [
            {"title": "Sec 6: OOP Foundations & RAII", "url": "section_6/book_fun.html"},
            {"title": "Sec 11: Smart Pointers & Custom Deleters", "url": "section_11/smart_pointer_fun.html"}
        ]
    },
    {
        "id": "red-black-tree",
        "term": "Red-Black Tree",
        "expansion": "Self-Balancing Binary Search Tree (`std::map` / `std::set`)",
        "category": "data-structures",
        "tags": ["Data Structures", "STL", "std::map", "Binary Search Tree"],
        "definition": "A self-balancing binary search tree algorithm that guarantees $O(\\log N)$ worst-case search, insertion, and deletion time complexity.",
        "hardware_relevance": "Standard library containers like <code>std::map</code> and <code>std::set</code> use node-based Red-Black trees. Each node incurs a 3-pointer + color byte overhead (24–32 bytes/node) and triggers an individual dynamic heap allocation per element, making them poorly suited for cache performance and RAM-constrained MCUs.",
        "related_sections": [
            {"title": "Sec 11: Map vs Unordered Map", "url": "section_11/map_vs_unordered_map.html"},
            {"title": "Sec 12: Data Structures & Trees", "url": "section_12/linked_list_app.html"}
        ]
    },
    {
        "id": "ring-buffer",
        "term": "Ring Buffer / Circular FIFO",
        "expansion": "Circular First-In First-Out Buffer",
        "category": "data-structures",
        "tags": ["Data Structures", "UART/SPI", "Interrupts", "Zero-Copy"],
        "definition": "A fixed-size array treated as circular using head and tail indices with modulo arithmetic or bitmask wrapping.",
        "hardware_relevance": "The gold standard for asynchronous UART/SPI communication and interrupt service routines (ISRs). Enables lock-free single-producer single-consumer (SPSC) data transfer between hardware interrupts and main processing loops without dynamic memory.",
        "related_sections": [
            {"title": "Sec 4: Arrays & Ring Buffers", "url": "section_4/array_fun.html"},
            {"title": "Sec 12: Array Queue Implementation", "url": "section_12/array_queue_app.html"}
        ]
    },
    {
        "id": "rodata-section",
        "term": ".rodata Section",
        "expansion": "Read-Only Data Section",
        "category": "toolchain-standards",
        "tags": ["ELF", "Linker", "Flash ROM", "Zero-SRAM"],
        "definition": "The memory section containing read-only constants, string literals, and virtual method tables (VTables).",
        "hardware_relevance": "Mapped directly to non-volatile Flash ROM, consuming 0 bytes of precious SRAM. Marking lookup tables and configuration strings as <code>const</code> or <code>constexpr</code> ensures they are placed in <code>.rodata</code>.",
        "related_sections": [
            {"title": "Sec 1: Linker Scripts", "url": "section_1/hello.html"},
            {"title": "Sec 2: Constants & ROM", "url": "section_2/constant_fun.html"}
        ]
    },
    {
        "id": "rule-of-three-five-zero",
        "term": "Rule of Three / Five / Zero",
        "expansion": "C++ Resource Management Special Member Functions",
        "category": "cpp-idiom",
        "tags": ["C++11", "Special Members", "Destructors", "Move Semantics"],
        "definition": "A C++ design guideline dictating that if a class manages resources and defines a destructor, copy constructor, or copy assignment, it should explicitly define all three (C++98) or all five (including move constructor and move assignment in C++11), or none (Rule of Zero).",
        "hardware_relevance": "Prevents double-free errors, hardware register lock leaks, and shallow-copy memory corruption when objects managing hardware peripherals or static buffers are passed or returned.",
        "related_sections": [
            {"title": "Sec 11: Rule of Three/Five/Zero", "url": "section_11/rule_of_three_five_zero.html"},
            {"title": "Sec 6: OOP Foundations", "url": "section_6/book_fun.html"}
        ]
    },
    {
        "id": "rvo-nrvo",
        "term": "RVO & NRVO",
        "expansion": "Return Value Optimization & Named RVO",
        "category": "cpp-idiom",
        "tags": ["Compilers", "Optimization", "Zero-Copy", "Stack"],
        "definition": "A compiler optimization (mandatory copy elision in C++17) where a function returning an object constructs it directly inside the storage allocated by the caller's stack frame.",
        "hardware_relevance": "Eliminates temporary object construction, copy/move constructors, and destruction overhead, enabling large structs and buffers to be returned by value with zero runtime copy cost.",
        "related_sections": [
            {"title": "Sec 5: Return Types & RVO", "url": "section_5/return_type_parameter_fun.html"},
            {"title": "Sec 5: Function Overloading", "url": "section_5/function_overloading.html"}
        ]
    },
    {
        "id": "saturating-arithmetic",
        "term": "Saturating Math (QADD / QSUB)",
        "expansion": "Non-Wrapping Fixed-Point DSP Arithmetic",
        "category": "embedded-hw",
        "tags": ["ARM Cortex-M", "DSP", "ALU", "Arithmetic Safety"],
        "definition": "Arithmetic operations that clamp results to the maximum or minimum representable values upon overflow or underflow instead of wrapping around.",
        "hardware_relevance": "Essential in digital signal processing (DSP), motor control, and audio processing to prevent catastrophic audio clipping or motor control loop inversions. Executed in a single cycle via ARM DSP instructions (<code>QADD</code>, <code>QSUB</code>, <code>SSAT</code>, <code>USAT</code>).",
        "related_sections": [
            {"title": "Sec 2: Arithmetic & Overflow", "url": "section_2/arithmetic_fun.html"},
            {"title": "Sec 2: Variables & Types", "url": "section_2/variable_fun.html"}
        ]
    },
    {
        "id": "stack-pointer-sp",
        "term": "SP (R13 - MSP / PSP)",
        "expansion": "Stack Pointer (Main Stack Pointer & Process Stack Pointer)",
        "category": "embedded-hw",
        "tags": ["ARM Cortex-M", "Registers", "RTOS", "Stack"],
        "definition": "The CPU register pointing to the current top of the descending call stack in SRAM.",
        "hardware_relevance": "ARM Cortex-M cores feature dual banked stack pointers: MSP (Main Stack Pointer, used for bootup and interrupt service routines) and PSP (Process Stack Pointer, used by user-space RTOS tasks). This dual architecture isolates task stack overflows from crashing kernel interrupt handlers.",
        "related_sections": [
            {"title": "Sec 5: AAPCS & Call Stacks", "url": "section_5/function_fun_1.html"},
            {"title": "Sec 5: Scope & Stack Frames", "url": "section_5/scope_fun.html"}
        ]
    },
    {
        "id": "sram",
        "term": "SRAM",
        "expansion": "Static Random-Access Memory",
        "category": "memory-storage",
        "tags": ["Memory", "Volatile", "SRAM", "Microcontroller"],
        "definition": "Fast, volatile semiconductor memory that stores variables, stacks, heaps, and runtime buffers as long as power is supplied.",
        "hardware_relevance": "Typically scarce in microcontrollers (ranging from 2KB on low-end MCUs to 512KB on high-end Cortex-M7). Every global variable, stack frame, and struct member must be engineered to minimize SRAM consumption.",
        "related_sections": [
            {"title": "Sec 2: Variables & Types", "url": "section_2/variable_fun.html"},
            {"title": "Sec 4: Arrays & Memory", "url": "section_4/array_fun.html"}
        ]
    },
    {
        "id": "static-init-fiasco",
        "term": "Static Initialization Order Fiasco",
        "expansion": "Cross-Translation-Unit Global Object Initialization Order Hazard",
        "category": "cpp-idiom",
        "tags": ["C++ Idiom", "Initialization", "Singletons", "Safety"],
        "definition": "A critical C++ bug where the initialization order of global/static variables across different translation units (.cpp files) is undefined, potentially causing one global object to access an uninitialized global object during startup.",
        "hardware_relevance": "Commonly occurs when hardware driver objects (e.g. <code>UartDriver</code>) attempt to log to an uninitialized console object on bootup. Solved by Meyers' Singleton (lazy initialization of a function-local static).",
        "related_sections": [
            {"title": "Sec 6: OOP Foundations", "url": "section_6/book_fun.html"},
            {"title": "Sec 5: Scope & Lifetime", "url": "section_5/scope_fun.html"}
        ]
    },
    {
        "id": "std-expected",
        "term": "std::expected<T, E>",
        "expansion": "C++23 Deterministic Tagged Value/Error Return Type",
        "category": "cpp-idiom",
        "tags": ["C++23", "Error Handling", "Zero-Cost", "Deterministic"],
        "definition": "A standard library vocabulary type that represents either an expected value of type <code>T</code> or an unexpected error of type <code>E</code> without using exceptions.",
        "hardware_relevance": "Provides type-safe, deterministic error handling with zero ROM overhead from exception tables and zero heap allocation, making it the preferred modern error model for embedded firmware.",
        "related_sections": [
            {"title": "Sec 7: Exceptions & Faults", "url": "section_7/custom_exceptions.html"},
            {"title": "Sec 7: Logic Error Fun", "url": "section_7/logic_error_fun.html"}
        ]
    },
    {
        "id": "std-span",
        "term": "std::span",
        "expansion": "C++20 Non-Owning Contiguous Memory View",
        "category": "cpp-idiom",
        "tags": ["C++20", "Bounds Safety", "Zero-Copy", "Arrays"],
        "definition": "A lightweight non-owning reference to a contiguous sequence of objects (stores only a pointer and a length).",
        "hardware_relevance": "Eliminates C-style array pointer decay by passing bounds information cleanly into functions, working seamlessly across C arrays, <code>std::array</code>, and DMA buffers with zero allocation overhead.",
        "related_sections": [
            {"title": "Sec 5: Passing Schemes & std::span", "url": "section_5/passing_schemes.html"},
            {"title": "Sec 4: Arrays & Views", "url": "section_4/array_fun.html"}
        ]
    },
    {
        "id": "std-string-view",
        "term": "std::string_view",
        "expansion": "C++17 Non-Owning String Slice Reference",
        "category": "cpp-idiom",
        "tags": ["C++17", "Zero-Allocation", "Flash Strings", "Optimization"],
        "definition": "A non-owning view of a character string consisting of a pointer to character data and a length count.",
        "hardware_relevance": "Allows string slicing and parsing directly over Flash ROM string literals (<code>.rodata</code>) or UART receive buffers without triggering dynamic heap memory allocation or copying.",
        "related_sections": [
            {"title": "Sec 4: Text & Strings", "url": "section_4/names_array.html"},
            {"title": "Sec 2: Text Fun", "url": "section_2/text_fun.html"}
        ]
    },
    {
        "id": "std-unique-ptr",
        "term": "std::unique_ptr",
        "expansion": "Exclusive Ownership Smart Pointer",
        "category": "cpp-idiom",
        "tags": ["C++11", "Smart Pointers", "RAII", "Zero-Cost"],
        "definition": "A smart pointer that owns and manages another object through a pointer and disposes of that object when the <code>std::unique_ptr</code> goes out of scope.",
        "hardware_relevance": "Incurs zero memory overhead compared to a raw C pointer (<code>sizeof(unique_ptr&lt;T&gt;) == sizeof(T*)</code>). With custom deleters, provides automatic RAII management of hardware locks and peripheral clocks.",
        "related_sections": [
            {"title": "Sec 11: Smart Pointers & Custom Deleters", "url": "section_11/smart_pointer_fun.html"},
            {"title": "Sec 8: Dynamic Memory", "url": "section_8/dynamic_fun.html"}
        ]
    },
    {
        "id": "systick",
        "term": "SysTick",
        "expansion": "ARM Cortex-M System Timer Peripheral",
        "category": "embedded-hw",
        "tags": ["ARM Cortex-M", "Timers", "RTOS", "Interrupts"],
        "definition": "A standardized 24-bit down-counting hardware timer integrated directly inside the core of every ARM Cortex-M processor.",
        "hardware_relevance": "Provides the periodic system tick interrupt (typically configured for 1ms intervals) that drives RTOS kernel context switches, <code>HAL_Delay()</code> timing, and software timer callbacks.",
        "related_sections": [
            {"title": "Sec 5: Functions & SysTick Delays", "url": "section_5/function_fun_1.html"},
            {"title": "Sec 3: Control Flow & Timers", "url": "section_3/repetition_fun.html"}
        ]
    },
    {
        "id": "text-section",
        "term": ".text Section",
        "expansion": "Executable Code Memory Section",
        "category": "toolchain-standards",
        "tags": ["ELF", "Linker", "Flash ROM", "Machine Code"],
        "definition": "The memory section in binary files where compiled CPU machine code instructions reside.",
        "hardware_relevance": "Stored in and executed directly from non-volatile Flash ROM on microcontrollers, consuming zero SRAM space.",
        "related_sections": [
            {"title": "Sec 1: Linker Scripts", "url": "section_1/hello.html"},
            {"title": "Sec 1: Toolchains", "url": "section_1/vsc_hello.html"}
        ]
    },
    {
        "id": "thumb-2",
        "term": "Thumb-2",
        "expansion": "ARM Mixed 16-Bit / 32-Bit Instruction Set Architecture",
        "category": "embedded-hw",
        "tags": ["ARM Cortex-M", "ISA", "Code Density", "Performance"],
        "definition": "The core instruction set architecture utilized by all ARM Cortex-M processors, dynamically combining high-density 16-bit instructions with powerful 32-bit instructions.",
        "hardware_relevance": "Delivers up to 35% better code density than pure 32-bit ARM code while maintaining full 32-bit performance, fitting complex modern firmware into constrained Flash ROM budgets.",
        "related_sections": [
            {"title": "Sec 3: Control Statements & Assembly", "url": "section_3/control_statements_intro.html"},
            {"title": "Sec 5: Functions & Thumb-2", "url": "section_5/function_fun_1.html"}
        ]
    },
    {
        "id": "trng",
        "term": "TRNG",
        "expansion": "True Random Number Generator Peripheral",
        "category": "embedded-hw",
        "tags": ["Hardware Peripheral", "Cryptography", "Entropy", "Security"],
        "definition": "A dedicated hardware peripheral that harvests true physical entropy (such as thermal electronic noise and ring oscillator jitter) to produce cryptographically secure random numbers.",
        "hardware_relevance": "Unlike software pseudorandom algorithms (<code>rand()</code> / PRNG) which repeat predictable sequences if not seeded properly, hardware TRNGs provide unpredictable random numbers essential for cryptographic keys, TLS sessions, and secure boot authentication.",
        "related_sections": [
            {"title": "Sec 3: Random Numbers & Hardware TRNG", "url": "section_3/random_fun.html"},
            {"title": "Sec 3: Die Rolls", "url": "section_3/die_rolls.html"}
        ]
    },
    {
        "id": "undefined-behavior",
        "term": "Undefined Behavior (UB)",
        "expansion": "Language Unspecified Non-Deterministic Execution",
        "category": "cpp-idiom",
        "tags": ["C++ Standard", "UB", "Safety", "Compiler Optimizations"],
        "definition": "Situations in C++ where the language specification imposes no requirements, allowing the compiler to optimize under the assumption that the condition can never occur.",
        "hardware_relevance": "Signed integer overflow, out-of-bounds pointer indexing, and strict aliasing violations allow aggressive compiler optimizations to silently eliminate critical safety checks or crash the microcontroller in unpredictable ways.",
        "related_sections": [
            {"title": "Sec 2: Arithmetic & Signed Overflow UB", "url": "section_2/arithmetic_fun.html"},
            {"title": "Sec 8: Pointer Safety & UB", "url": "section_8/pointer_fun.html"}
        ]
    },
    {
        "id": "usagefault",
        "term": "UsageFault",
        "expansion": "ARM Cortex-M Program Execution Fault",
        "category": "embedded-hw",
        "tags": ["Fault Handling", "ARM Cortex-M", "Exceptions", "Instructions"],
        "definition": "A hardware fault triggered by execution errors such as undefined instructions, unaligned memory accesses (when unaligned trap is enabled), or division by zero (when DIVBYZERO trap is enabled).",
        "hardware_relevance": "Enabling the <code>DIV_0_TRP</code> bit in the CCR register ensures integer division by zero triggers a deterministic hardware exception instead of returning 0 silently.",
        "related_sections": [
            {"title": "Sec 7: Hardware Faults & UsageFault", "url": "section_7/bug_fun.html"},
            {"title": "Sec 2: Arithmetic Fun", "url": "section_2/arithmetic_fun.html"}
        ]
    },
    {
        "id": "vtable-vptr",
        "term": "VTable & VPtr",
        "expansion": "Virtual Method Table & Virtual Pointer",
        "category": "cpp-idiom",
        "tags": ["OOP", "Polymorphism", "VTable", "RAM Overhead"],
        "definition": "The compiler mechanism for dynamic polymorphism: a VTable is an array of function pointers stored in Flash ROM (<code>.rodata</code>), and a VPtr is a hidden pointer stored inside every polymorphic object in SRAM pointing to its VTable.",
        "hardware_relevance": "Adding a single virtual method adds 4 bytes of hidden SRAM overhead per object instance on a 32-bit MCU, and indirect branch calls through function pointers prevent compiler inlining and incur pipeline bubbles.",
        "related_sections": [
            {"title": "Sec 10: OOP Polymorphism & VTable Cost", "url": "section_10/animal_fun.html"},
            {"title": "Sec 10: Enums & Classes", "url": "section_10/enum_fun.html"}
        ]
    },
    {
        "id": "volatile-keyword",
        "term": "volatile",
        "expansion": "Compiler Optimization Barrier for Hardware Access",
        "category": "cpp-idiom",
        "tags": ["C++ Keyword", "MMIO", "Registers", "Interrupts"],
        "definition": "A type qualifier telling the compiler that a variable's value may change at any time through means outside the compiler's control (such as hardware peripherals or interrupt service routines).",
        "hardware_relevance": "Prevents the compiler from caching register reads in CPU registers or optimizing away repeated writes. Mandatory for memory-mapped I/O (MMIO) and shared ISR flags.",
        "related_sections": [
            {"title": "Sec 8: Pointers & volatile MMIO", "url": "section_8/pointer_fun.html"},
            {"title": "Sec 8: Const Correctness", "url": "section_8/const_correctness.html"}
        ]
    },
    {
        "id": "watchdog-timer",
        "term": "Watchdog Timer (WDT / IWDG)",
        "expansion": "Hardware Super-Loop Liveness Monitor",
        "category": "embedded-hw",
        "tags": ["Hardware Safety", "Reliability", "Reset", "Super-Loop"],
        "definition": "An independent hardware countdown timer that automatically resets the microcontroller if the main firmware loop fails to refresh ('kick' / 'feed') it within a specified timeout window.",
        "hardware_relevance": "Protects against firmware deadlocks, infinite loops, and hardware lockups in harsh EMI environments, ensuring automatic recovery in unattended systems.",
        "related_sections": [
            {"title": "Sec 3: Control Flow & Watchdogs", "url": "section_3/repetition_fun.html"},
            {"title": "Sec 3: Control Statements", "url": "section_3/control_statements_intro.html"}
        ]
    },
    {
        "id": "wear-leveling",
        "term": "Wear Leveling (Dynamic vs Static)",
        "expansion": "Flash Memory Erase-Cycle Distribution Algorithm",
        "category": "memory-storage",
        "tags": ["Flash Memory", "Storage", "Endurance", "File System"],
        "definition": "A technique used by embedded file systems (e.g. LittleFS) to distribute write and erase operations uniformly across all physical flash memory blocks.",
        "hardware_relevance": "NOR and NAND Flash blocks degrade after 10,000 to 100,000 erase cycles. Dynamic wear leveling rotates active data writes, while static wear leveling also periodically relocates read-only static files to equalize wear, extending hardware lifespan from months to decades.",
        "related_sections": [
            {"title": "Sec 9: Flash Streams & File Systems", "url": "section_9/file_input_fun.html"},
            {"title": "Sec 9: File Output Logging", "url": "section_9/file_output_fun.html"}
        ]
    },
    {
        "id": "zero-cost-abstraction",
        "term": "Zero-Cost Abstraction",
        "expansion": "Bjarne Stroustrup's Guiding C++ Principle",
        "category": "cpp-idiom",
        "tags": ["C++ Philosophy", "Optimization", "Compilers", "Efficiency"],
        "definition": "The foundational C++ principle stating: 'What you don't use, you don't pay for. What you do use, you couldn't hand code any better.'",
        "hardware_relevance": "Modern C++ features such as templates, <code>std::string_view</code>, <code>std::span</code>, <code>constexpr</code>, and range-based for loops compile down to the exact same or more optimal assembly instructions as hand-written C pointer arithmetic.",
        "related_sections": [
            {"title": "Sec 10: OOP & CRTP", "url": "section_10/animal_fun.html"},
            {"title": "Sec 11: Templates & Zero Cost", "url": "section_11/templates.html"}
        ]
    },
    {
        "id": "likely-unlikely",
        "term": "[[likely]] / [[unlikely]]",
        "expansion": "C++20 Branch Prediction Attributes",
        "category": "cpp-idiom",
        "tags": ["C++20", "Branch Prediction", "Pipeline", "Optimization"],
        "definition": "C++20 standard attributes applied to conditional branches to hint to the compiler which execution path is most or least probable.",
        "hardware_relevance": "Guides the compiler to place the hot/likely execution path in straight-line contiguous machine code, avoiding taken-branch instruction fetch pipeline stalls on the processor.",
        "related_sections": [
            {"title": "Sec 3: Control Statements & [[likely]]", "url": "section_3/selection_fun.html"},
            {"title": "Sec 3: Control Flow Intro", "url": "section_3/control_statements_intro.html"}
        ]
    },
    {
        "id": "nodiscard",
        "term": "[[nodiscard]]",
        "expansion": "C++17 Unused Return Value Warning Attribute",
        "category": "cpp-idiom",
        "tags": ["C++17", "Safety", "Error Handling", "MISRA"],
        "definition": "A standard C++ attribute that causes the compiler to emit a warning if a function's return value (e.g. error code or status enum) is discarded by the caller.",
        "hardware_relevance": "Enforces error handling at compile time, preventing bugs where firmware inadvertently ignores peripheral transmission errors or sensor timeout status codes.",
        "related_sections": [
            {"title": "Sec 5: Return Types & [[nodiscard]]", "url": "section_5/return_type_parameter_fun.html"},
            {"title": "Sec 7: Logic Errors", "url": "section_7/logic_error_fun.html"}
        ]
    },
    {
        "id": "fno-rtti-exceptions",
        "term": "-fno-rtti & -fno-exceptions",
        "expansion": "GCC/Clang Embedded Optimization Flags",
        "category": "toolchain-standards",
        "tags": ["Compiler Flags", "Embedded", "ROM Optimization", "Zero-Overhead"],
        "definition": "Compiler flags that disable Runtime Type Information (<code>typeid</code> and <code>dynamic_cast</code>) and C++ exception handling (<code>try/catch/throw</code>) respectively.",
        "hardware_relevance": "Disabling RTTI saves typenames and type descriptors in Flash ROM; disabling exceptions removes <code>.eh_frame</code> tables, reducing overall binary size by 15KB–50KB and ensuring deterministic real-time execution on microcontrollers.",
        "related_sections": [
            {"title": "Sec 10: OOP & -fno-rtti", "url": "section_10/animal_fun.html"},
            {"title": "Sec 7: Custom Exceptions", "url": "section_7/custom_exceptions.html"}
        ]
    }
]
