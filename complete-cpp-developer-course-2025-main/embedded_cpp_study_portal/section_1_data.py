#!/usr/bin/env python3
"""
Section 1 Project Definitions: Toolchains, Cross-Compilation & Embedded Linkers
Contains 2 comprehensive project definitions covering GCC/Clang cross-compilation,
ELF binaries, memory maps (.text/.data/.bss), and microcontroller startup vector tables.
"""

SECTION_1_PROJECTS = [
    {
        "id": "hello",
        "name": "Hello (Visual Studio / MSVC)",
        "title": "C++ Compilation Pipeline, Hosted vs Freestanding & Linker Maps",
        "headline": "The C++ Build Pipeline: Preprocessor, Compiler, Assembler & Freestanding Linker Maps",
        "emb_class": "emb-high",
        "emb_badge": "⚡ Embedded Relevance: Critical",
        "tags": ["Toolchains", "Preprocessing", "Compilation", "Freestanding", "ELF / Linker Scripts"],
        "summary": "Exploring the classic C++ entry point. We deconstruct the 4 stages of the C++ compilation pipeline (Preprocessor, Compiler AST to Assembly, Assembler to Relocatable Object .o, and Linker), contrast Hosted OS environments with Freestanding Bare-Metal microcontrollers, and inspect how linker scripts (.ld) map code sections to Flash and RAM.",
        "files": ["section_1/Hello/Hello/main.cpp"],
        "concepts_html": """
        <h3>1. The 4 Stages of C++ Compilation</h3>
        <ul>
          <li><strong>1. Preprocessor (<code>cpp</code>):</strong> Resolves <code>#include</code>, <code>#define</code>, and conditional compilation flags (<code>#ifdef</code>), emitting pure translation units.</li>
          <li><strong>2. Compiler (<code>g++ / clang++</code>):</strong> Parses tokens, generates Abstract Syntax Trees (AST), performs type checking and optimizations, and outputs assembly (<code>.s</code>).</li>
          <li><strong>3. Assembler (<code>as</code>):</strong> Translates assembly mnemonics into machine opcodes, producing relocatable object files (<code>.o</code> / <code>.obj</code>).</li>
          <li><strong>4. Linker (<code>ld</code>):</strong> Resolves symbols across object files and libraries, calculating absolute memory addresses using a linker script (<code>.ld</code>).</li>
        </ul>

        <h3>2. Hosted vs Freestanding Environments</h3>
        <p>A <strong>Hosted Environment</strong> runs on top of an OS (Windows/Linux) providing standard library features (dynamic heap, file I/O, threads). A <strong>Freestanding Environment</strong> (bare-metal microcontroller) has no OS; execution begins directly at the hardware Reset Vector.</p>
        """,
        "embedded_html": """
        <h3>1. Microcontroller Linker Script Anatomy (<code>.ld</code>)</h3>
        <p>In bare-metal embedded systems, the linker script maps ELF sections to physical silicon memory regions:</p>
        <ul>
          <li><code>.text</code>: Executable machine code $\\rightarrow$ <strong>Flash ROM (Read-Only)</strong>.</li>
          <li><code>.rodata</code>: Constants, string literals, lookup tables $\\rightarrow$ <strong>Flash ROM</strong>.</li>
          <li><code>.data</code>: Initialized global/static variables $\\rightarrow$ <strong>VMA in SRAM, LMA in Flash ROM</strong> (copied to RAM at boot).</li>
          <li><code>.bss</code>: Zero-initialized global/static variables $\\rightarrow$ <strong>SRAM</strong> (cleared to 0 at boot).</li>
          <li><code>.stack</code> / <code>.heap</code>: Runtime stack and heap allocations $\\rightarrow$ <strong>Top and bottom of SRAM</strong>.</li>
        </ul>
        """,
        "refactor_html": """
        <p>Minimal freestanding bare-metal main with zero OS dependencies:</p>
        <pre class="code-block" style="background:#0d1117; padding:16px; border-radius:8px; border:1px solid #30363d;">#include &lt;cstdint&gt;

// Bare-metal main: never returns in an embedded system
extern "C" int main(void) {
    // Hardware peripheral initialization (RCC clocks, GPIO pins)...
    
    while (true) {
        // Super-loop / RTOS scheduler...
    }
    
    // Unreachable in bare metal
    return 0;
}</pre>
        """,
        "quiz": [
            {
                "question": "What is the primary difference between a 'Hosted' and a 'Freestanding' C++ implementation?",
                "options": ["A Hosted environment provides full standard libraries and OS services, while Freestanding runs without an OS directly on bare metal with limited standard headers", "Hosted runs only on web browsers", "Freestanding does not support functions", "Hosted code cannot use pointers"],
                "correct": 0,
                "explanation": "C++ standard specifies Freestanding environments for bare-metal targets without an operating system, providing only essential headers like <code>&lt;cstdint&gt;</code>, <code>&lt;cstddef&gt;</code>, and <code>&lt;type_traits&gt;</code>."
            },
            {
                "question": "Which stage of the compilation pipeline replaces '#include <header>' with the actual text content of the header file?",
                "options": ["Preprocessor", "Compiler Optimizer", "Assembler", "Linker"],
                "correct": 0,
                "explanation": "The C++ preprocessor performs text substitutions, macro expansions, and file inclusions before compilation begins."
            },
            {
                "question": "Where is an initialized global variable (int baud_rate = 115200;) placed in a microcontroller memory map?",
                "options": [".data section (Load Memory Address in Flash ROM, Virtual Memory Address in SRAM)", ".bss section in SRAM", ".text section in Flash ROM", "On the stack frame"],
                "correct": 0,
                "explanation": "Initialized static variables have their initial values stored in Flash ROM (.rodata/LMA), which startup assembly copies into SRAM (.data/VMA) during boot."
            },
            {
                "question": "Why should main() in a bare-metal microcontroller application never return?",
                "options": ["There is no host operating system to return control to; returning jumps to undefined memory or triggers a HardFault/infinite restart", "Returning erases the Flash memory", "Returning lowers the crystal clock", "Returning disables compiler optimizations"],
                "correct": 0,
                "explanation": "On bare-metal CPUs without an OS, returning from <code>main()</code> would branch into whatever uninitialized code exists after <code>main</code>, causing crashes."
            }
        ]
    },
    {
        "id": "vsc_hello",
        "name": "VSC Hello (Cross-Compilation & Toolchains)",
        "title": "Cross-Compilation Toolchains (arm-none-eabi-g++) & GDB Debugging",
        "headline": "Host vs Target Architectures, Cross-Compilers (arm-none-eabi-gcc) & SWD/JTAG Debugging",
        "emb_class": "emb-high",
        "emb_badge": "⚡ Embedded Relevance: Critical",
        "tags": ["Cross-Compilation", "arm-none-eabi-gcc", "GDB", "OpenOCD", "SWD / JTAG"],
        "summary": "Building modern C++ projects using cross-platform toolchains (VS Code, CMake, Ninja). We dissect Host vs Target compilation architecture, the arm-none-eabi-gcc cross-compiler toolchain, generating .bin / .hex Flash artifacts, and hardware debugging via OpenOCD, GDB, and SWD/JTAG probes.",
        "files": ["section_1/vsc-hello/main.cpp"],
        "concepts_html": """
        <h3>1. Host vs Target Architecture</h3>
        <ul>
          <li><strong>Host System:</strong> The development PC (e.g. x86_64 Linux/Windows) where code is edited and compiled.</li>
          <li><strong>Target System:</strong> The target embedded microcontroller (e.g. ARM Cortex-M4 32-bit RISC) where the compiled binary runs.</li>
        </ul>

        <h3>2. Cross-Compiler Toolchain Triplet</h3>
        <p>The GNU toolchain naming convention <code>arch-vendor-os-abi</code> indicates the target:</p>
        <p><code>arm-none-eabi-g++</code> $\\rightarrow$ <strong>ARM architecture</strong>, <strong>No OS (bare-metal)</strong>, <strong>Embedded ABI</strong>.</p>
        """,
        "embedded_html": """
        <h3>1. Firmware Binary Formats</h3>
        <ul>
          <li><strong>ELF (Executable and Linkable Format):</strong> Contains symbols, debug metadata (DWARF), and section headers. Used by GDB for debugging.</li>
          <li><strong>HEX (Intel HEX) / BIN (Raw Binary):</strong> Stripped flat memory images programmed directly into microcontroller Flash memory via programmer probes (ST-Link / J-Link).</li>
        </ul>

        <h3>2. Hardware In-Circuit Debugging (SWD / JTAG)</h3>
        <p>Hardware debuggers communicate with on-chip CoreSight debug units via Serial Wire Debug (SWD: SWDIO + SWCLK) or JTAG, allowing hardware breakpoints, register inspection, and Flash programming.</p>
        """,
        "refactor_html": """
        <p>CMake cross-compilation toolchain setup snippet:</p>
        <pre class="code-block" style="background:#0d1117; padding:16px; border-radius:8px; border:1px solid #30363d;"># CMake Cross-Compilation Definition for ARM Cortex-M
set(CMAKE_SYSTEM_NAME Generic)
set(CMAKE_SYSTEM_PROCESSOR arm)

set(CMAKE_C_COMPILER arm-none-eabi-gcc)
set(CMAKE_CXX_COMPILER arm-none-eabi-g++)

# Cortex-M4 Hardware FPU compiler flags
set(CPU_FLAGS "-mcpu=cortex-m4 -mthumb -mfpu=fpv4-sp-d16 -mfloat-abi=hard")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${CPU_FLAGS} -std=c++20 -Wall -Wextra -O2")</pre>
        """,
        "quiz": [
            {
                "question": "What does the 'none' in the toolchain triplet 'arm-none-eabi-gcc' signify?",
                "options": ["Target system has no operating system (bare-metal freestanding target)", "No optimization flags are enabled", "No C++ standard library is present", "No hardware floating-point unit is supported"],
                "correct": 0,
                "explanation": "In GNU toolchain triplets (<code>arch-vendor-os-abi</code>), <code>none</code> denotes the absence of an underlying operating system kernel (bare metal)."
            },
            {
                "question": "What is the difference between an ELF file and a raw BIN binary file in firmware development?",
                "options": ["An ELF file contains debug symbols, section tables, and metadata for GDB; a BIN file is a raw binary flash image containing only pure machine opcodes and data", "An ELF file is only for Linux; BIN is for Windows", "An ELF file cannot be flashed to microcontrollers", "BIN files are human-readable text"],
                "correct": 0,
                "explanation": "ELF binaries retain full symbol and debugging tables for debuggers (GDB/OpenOCD), while <code>objcopy -O binary</code> extracts the raw byte image flashed into ROM."
            },
            {
                "question": "How many physical signal pins are required for ARM Serial Wire Debug (SWD)?",
                "options": ["2 pins (SWDIO bidirectional data + SWCLK clock), plus Ground", "4 pins (TDI, TDO, TMS, TCK)", "8 pins", "16 pins"],
                "correct": 0,
                "explanation": "ARM SWD reduces traditional 4-pin JTAG to just 2 pins: SWDIO (bidirectional data) and SWCLK (clock), conserving GPIO pins on low-pin-count chips."
            },
            {
                "question": "Which tool acts as the bridge between a GDB debugger on a host PC and physical hardware debug probes (ST-Link / J-Link)?",
                "options": ["OpenOCD / PyOCD / J-Link GDB Server", "Git", "CMake", "Make"],
                "correct": 0,
                "explanation": "On-chip debugger servers (OpenOCD, pyOCD) translate GDB remote serial protocol commands into low-level USB/SWD hardware transactions."
            }
        ]
    }
]
