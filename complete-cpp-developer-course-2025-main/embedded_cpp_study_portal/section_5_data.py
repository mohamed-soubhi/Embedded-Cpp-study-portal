#!/usr/bin/env python3
"""
Section 5 Project Definitions: Functions, Parameter Schemes & Stack Calling Conventions
Contains 15 comprehensive project definitions covering AAPCS ARM calling conventions (R0-R3),
pass-by-value vs pass-by-reference overhead, recursion stack hazards, inlining, and Return Value Optimization.
"""

SECTION_5_PROJECTS = [
    {
        "id": "function_fun_1",
        "name": "FunctionFun1",
        "title": "Function Declarations, Prototypes & AAPCS Calling Conventions",
        "headline": "Function Signatures, Header Prototypes & ARM Register Passing (R0–R3)",
        "emb_class": "emb-high",
        "emb_badge": "⚡ Embedded Relevance: Critical",
        "tags": ["Prototypes", "AAPCS", "Stack Frames", "Calling Convention", "Registers R0-R3"],
        "summary": "Exploring function prototypes, definitions, and execution flow. We analyze the ARM Architecture Procedure Call Standard (AAPCS), demonstrating how the first 4 function arguments are passed in CPU registers (R0-R3) with zero memory latency, while additional arguments spill onto the stack.",
        "files": ["section_5/FunctionFun1/FunctionFun1/main.cpp"],
        "concepts_html": """
        <h3>1. Forward Declarations & Prototypes</h3>
        <p>A function prototype informs the compiler of a function's name, return type, and parameter types before its definition, allowing the compiler to perform type verification and code generation across translation units.</p>

        <h3>2. Function Call Overhead</h3>
        <p>A standard function call executes a branch with link (<code>BL</code>) instruction, saving the return address into the Link Register (<code>LR</code>) and pushing caller-saved registers onto the stack.</p>
        """,
        "embedded_html": """
        <h3>1. The ARM AAPCS Calling Convention</h3>
        <p>Under the standard ARM 32-bit calling convention (AAPCS):</p>
        <ul>
          <li>The first 4 integer/pointer arguments are passed directly in CPU hardware registers: <strong>R0, R1, R2, R3</strong> (zero stack latency!).</li>
          <li>Return values are passed back in <strong>R0</strong> (or <strong>R0-R1</strong> for 64-bit integers).</li>
          <li>Arguments beyond the 4th are pushed onto the <strong>CPU stack</strong>, adding memory store and load instructions.</li>
        </ul>

        <div class="callout callout-tip">
          <h4>💡 Embedded Optimization Tip: 4-Parameter Rule</h4>
          <p>Design performance-critical functions to accept <strong>$\\le 4$ parameters</strong> so all inputs reside entirely in CPU hardware registers.</p>
        </div>
        """,
        "refactor_html": """
        <p>Register-friendly driver API design:</p>
        <pre class="code-block" style="background:#0d1117; padding:16px; border-radius:8px; border:1px solid #30363d;">#include &lt;cstdint&gt;

// Fits perfectly in R0, R1, R2 (Zero stack memory traffic)
void configureTimer(uint8_t timer_id, uint32_t prescaler, uint32_t auto_reload) noexcept {
    // Direct MMIO writes using hardware registers...
}</pre>
        """,
        "quiz": [
            {
                "question": "Under the ARM AAPCS calling convention, which CPU registers hold the first 4 integer arguments?",
                "options": ["R0, R1, R2, and R3", "R4, R5, R6, and R7", "Stack Pointer (SP) and Link Register (LR)", "Program Counter (PC) and Status Register (PSR)"],
                "correct": 0,
                "explanation": "AAPCS assigns registers R0 through R3 for passing the first four 32-bit arguments, executing function calls with zero stack memory overhead."
            },
            {
                "question": "What happens when a function accepts 6 integer parameters on an ARM Cortex-M processor?",
                "options": ["The first 4 are passed in R0-R3, and the remaining 2 are pushed onto the stack frame", "All 6 parameters are rejected by the compiler", "Parameters 5 and 6 are passed in floating point registers", "The CPU enters sleep mode"],
                "correct": 0,
                "explanation": "Arguments exceeding the four register slots spill onto the stack, requiring extra <code>STR</code> (store) and <code>LDR</code> (load) memory operations."
            },
            {
                "question": "Which CPU register stores the return address during a standard function call on ARM Cortex-M?",
                "options": ["Link Register (LR / R14)", "Stack Pointer (SP / R13)", "Program Counter (PC / R15)", "Frame Pointer (R11)"],
                "correct": 0,
                "explanation": "The <code>BL</code> (Branch with Link) instruction automatically loads the return address into the Link Register (LR / R14)."
            },
            {
                "question": "Why are forward declarations (prototypes) placed in .h header files in C++?",
                "options": ["To allow multiple .cpp translation units to call functions with compile-time type verification without duplicating function bodies", "To reduce the clock frequency of the processor", "To compress function code in flash", "To enable dynamic casting"],
                "correct": 0,
                "explanation": "Header prototypes let other source files verify parameter types and return types during compilation before the linker connects definitions."
            }
        ]
    },
    {
        "id": "passing_schemes",
        "name": "PassingSchemes",
        "title": "Passing Schemes: Pass-by-Value, Reference & Const Reference",
        "headline": "Pass-by-Value Copy Overhead vs Pass-by-Reference & const& in Microcontroller RAM",
        "emb_class": "emb-high",
        "emb_badge": "⚡ Embedded Relevance: Critical",
        "tags": ["Pass-by-Value", "Pass-by-Reference", "const&", "Stack Frames", "Memory Footprint"],
        "summary": "Comprehensive comparative study of the three parameter passing schemes: pass-by-value, pass-by-reference (&), and pass-by-const-reference (const &). We analyze assembly instruction differences, stack frame memory consumption, and reference aliasing in safety-critical systems.",
        "files": ["section_5/PassingSchemes/PassingSchemes/main.cpp"],
        "concepts_html": """
        <h3>1. Pass-by-Value</h3>
        <p>A complete copy of the argument is constructed in the callee's stack frame. Modifications inside the function do NOT affect the caller's variable.</p>

        <h3>2. Pass-by-Reference (<code>T&amp;</code>)</h3>
        <p>Passes an alias (internally implemented as a pointer). Modifications inside the function directly alter the caller's variable.</p>

        <h3>3. Pass-by-Const-Reference (<code>const T&amp;</code>)</h3>
        <p>Passes an alias with read-only guarantees. Prevents copying large structures while preventing accidental modifications.</p>
        """,
        "embedded_html": """
        <h3>1. The Embedded Rule of Thumb</h3>
        <ul>
          <li><strong>Primitive Types ($\\le 4$ bytes):</strong> Pass <strong>by value</strong> (<code>int</code>, <code>float</code>, <code>uint32_t</code>). They fit directly inside CPU registers (R0-R3), requiring zero pointer indirection.</li>
          <li><strong>Aggregates & Structs ($&gt; 4$ bytes):</strong> Pass <strong>by const reference</strong> (<code>const SensorPacket&amp;</code>). Passing by value copies bytes onto the stack, increasing execution time and RAM usage.</li>
        </ul>
        """,
        "refactor_html": """
        <p>Idiomatic passing schemes in embedded systems:</p>
        <pre class="code-block" style="background:#0d1117; padding:16px; border-radius:8px; border:1px solid #30363d;">#include &lt;cstdint&gt;

struct CanMessage {
    uint32_t id;
    uint8_t  payload[8];
    uint8_t  dlc;
};

// 1. Primitive: Pass-by-value (fits in R0)
void setFilterId(uint32_t id) noexcept;

// 2. Struct: Pass-by-const-ref (passes 4-byte pointer; avoids 16-byte copy)
void transmitCan(const CanMessage&amp; msg) noexcept;

// 3. Mutator: Pass-by-ref (modifies caller's object directly)
void readCan(CanMessage&amp; out_msg) noexcept;</pre>
        """,
        "quiz": [
            {
                "question": "Why is passing a 64-byte telemetry struct by value suboptimal on an embedded microcontroller?",
                "options": ["The compiler must copy all 64 bytes onto the stack, wasting clock cycles and consuming precious stack SRAM", "The struct will be corrupted during the call", "C++ forbids passing structs by value", "Passing by value deletes the original struct"],
                "correct": 0,
                "explanation": "Pass-by-value creates a full duplicate of the struct on the stack, consuming stack RAM and CPU cycles for memory copying."
            },
            {
                "question": "For a 32-bit integer (uint32_t), why is pass-by-value generally faster than pass-by-const-reference on ARM Cortex-M?",
                "options": ["Pass-by-value loads the value directly into register R0, whereas pass-by-reference passes an address that requires an extra dereferencing memory load instruction", "Pass-by-value uses floating point registers", "Pass-by-reference always allocates heap memory", "Pass-by-value disables interrupts"],
                "correct": 0,
                "explanation": "Passing a 4-byte integer by value puts it directly into a register (R0), while passing by reference passes a pointer that forces an extra <code>LDR</code> memory read."
            },
            {
                "question": "What is 'pointer aliasing' in C++ parameter passing?",
                "options": ["When two reference/pointer parameters in a function point to the same memory location, preventing certain compiler loop optimizations", "When a pointer points to address 0x00000000", "When a pointer is deleted twice", "When a function has more than 4 parameters"],
                "correct": 0,
                "explanation": "Aliasing occurs when multiple pointers/references refer to the same object. The compiler must assume writes through one pointer may modify the other, limiting optimization."
            },
            {
                "question": "What does passing by non-const reference (T&) signal in function API design?",
                "options": ["The function intends to modify the caller's argument directly (acting as an in-out or output parameter)", "The function will delete the caller's object", "The function executes in background threads", "The function returns a pointer to Flash ROM"],
                "correct": 0,
                "explanation": "Non-const reference parameters (<code>T&amp;</code>) indicate that the function will mutate the caller's object in place."
            }
        ]
    },
    {
        "id": "function_overloading",
        "name": "FunctionOverloading",
        "title": "Function Overloading, Name Mangling & C Linkage (extern \"C\")",
        "headline": "C++ Name Mangling, Type Ambiguity & Integrating C RTOS APIs with extern \"C\"",
        "emb_class": "emb-high",
        "emb_badge": "⚡ Embedded Relevance: High",
        "tags": ["Overloading", "Name Mangling", "extern \"C\"", "Linker Symbols", "FreeRTOS"],
        "summary": "Analyzing function overloading in C++. We examine compiler name mangling, resolving ambiguous type promotions, and how to use extern \"C\" to bridge modern C++ applications with C-based microcontroller HALs and RTOS kernels (e.g. FreeRTOS, STM32 HAL).",
        "files": ["section_5/FunctionOverloading/FunctionOverloading/main.cpp"],
        "concepts_html": """
        <h3>1. Function Overloading Resolution</h3>
        <p>Functions can share the same name if their parameter lists differ in count, types, or constness. Return type alone is insufficient to overload a function.</p>

        <h3>2. C++ Name Mangling</h3>
        <p>To differentiate overloaded functions at the object-file level, the C++ compiler encodes parameter types into the symbol name in the compiled binary (e.g., <code>_Z8transmiti</code> vs <code>_Z8transmitPKc</code>).</p>
        """,
        "embedded_html": """
        <h3>1. Interfacing with C Microcontroller HALs (<code>extern \"C\"</code>)</h3>
        <p>Most hardware vendor libraries (STM32 CubeHAL, ESP-IDF, FreeRTOS) are written in C. Because C compilers do not mangle symbol names, C++ code calling C functions—or C code calling C++ interrupt handlers—must be wrapped in <code>extern \"C\"</code> to disable name mangling.</p>
        """,
        "refactor_html": """
        <p>Robust C/C++ compatible header wrapper:</p>
        <pre class="code-block" style="background:#0d1117; padding:16px; border-radius:8px; border:1px solid #30363d;">#ifdef __cplusplus
extern "C" {
#endif

// Hardware ISR handler (must match C symbol name for vector table)
void USART1_IRQHandler(void);

// FreeRTOS Task Entry Point
void vSensorTask(void* pvParameters);

#ifdef __cplusplus
}
#endif</pre>
        """,
        "quiz": [
            {
                "question": "Why does C++ perform 'name mangling' on function symbols?",
                "options": ["To encode parameter types into symbol names, allowing linkers to distinguish between overloaded functions with the same name", "To encrypt proprietary algorithm code", "To compress binary Flash file sizes", "To force functions to run at higher CPU priorities"],
                "correct": 0,
                "explanation": "Name mangling generates unique symbol names based on function signatures, enabling the linker to bind overloaded function calls accurately."
            },
            {
                "question": "What is the purpose of 'extern \"C\"' when writing C++ firmware?",
                "options": ["It disables C++ name mangling for enclosed functions, enabling seamless linking with C libraries and hardware ISR vector tables", "It forces the compiler to compile in C89 mode only", "It allocates functions in external Flash memory", "It allows C++ classes to have virtual destructors"],
                "correct": 0,
                "explanation": "<code>extern \"C\"</code> instructs the C++ compiler to emit unmangled C symbol names, enabling interoperability with C HALs and hardware vector tables."
            },
            {
                "question": "Can two functions differ ONLY by their return type be overloaded in C++?",
                "options": ["No, return type alone is not sufficient to differentiate overloaded functions in C++", "Yes, the compiler determines which to call based on the assignment target", "Yes, but only if both functions are constexpr", "Yes, if compiled with -O3"],
                "correct": 0,
                "explanation": "C++ requires parameter lists to differ; return type alone cannot be used by the compiler to resolve function calls."
            },
            {
                "question": "What happens if a hardware Interrupt Service Routine (e.g. SysTick_Handler) in C++ is NOT declared extern \"C\"?",
                "options": ["The linker fails to match the mangled C++ symbol with the raw symbol in the vector table, causing the default handler or HardFault to execute", "The CPU clock stops", "The compiler automatically fixes the symbol", "The interrupt runs twice as fast"],
                "correct": 0,
                "explanation": "The vector table in startup assembly references <code>SysTick_Handler</code>. A mangled C++ symbol (like <code>_Z15SysTick_Handlerv</code>) will not match, leaving the interrupt bound to the default unhandled loop."
            }
        ]
    },
    {
        "id": "factorial_fun",
        "name": "FactorialFun",
        "title": "Recursion vs Iteration & Stack Overflow Dangers in RTOS",
        "headline": "Recursive Stack Frame Growth, Call Depth Hazards & constexpr Compile-Time Evaluation",
        "emb_class": "emb-high",
        "emb_badge": "⚡ Embedded Relevance: Critical",
        "tags": ["Recursion", "Stack Overflow", "constexpr", "Tail Call Optimization", "RTOS"],
        "summary": "Exploring recursive algorithms vs iterative implementations. We demonstrate why unbounded recursion is banned in embedded standards (MISRA / NASA) due to small RTOS task stack budgets (e.g. 512 bytes), analyze Tail-Call Optimization (TCO), and evaluate math at compile-time using constexpr.",
        "files": ["section_5/FactorialFun/FactorialFun/main.cpp"],
        "concepts_html": """
        <h3>1. Recursive Call Stack Mechanics</h3>
        <p>Each recursive function call creates a new stack frame storing local variables, parameters, and the return address. A recursion depth of $N$ consumes $O(N)$ stack memory.</p>

        <h3>2. Iterative & Tail-Call Alternatives</h3>
        <p>Iterative loops require $O(1)$ stack space. When the recursive call is the absolute last operation (tail recursion), optimizing compilers can reuse the existing stack frame (Tail-Call Optimization - TCO).</p>
        """,
        "embedded_html": """
        <h3>1. Why Recursion is Banned in Embedded Systems</h3>
        <p>In embedded systems and RTOS tasks, stack sizes are statically allocated and very small (e.g. 512 to 2048 bytes). Unbounded or deep recursion quickly exceeds the stack limit, silently clobbering adjacent RAM and causing catastrophic system crashes.</p>

        <div class="callout callout-danger">
          <h4>🚫 MISRA C++:2008 Rule 7-5-4 & NASA C Safety Rule #3</h4>
          <p>Functions shall not call themselves, either directly or indirectly. Execution bounds and stack depth must be deterministically provable.</p>
        </div>

        <h3>2. Compile-Time <code>constexpr</code> Evaluation</h3>
        <p>Modern C++ allows computing mathematical constants at compile time, consuming <strong>0 clock cycles and 0 stack frames at runtime</strong>.</p>
        """,
        "refactor_html": """
        <p>Compile-time constexpr factorial calculation:</p>
        <pre class="code-block" style="background:#0d1117; padding:16px; border-radius:8px; border:1px solid #30363d;">#include &lt;cstdint&gt;

// Evaluated 100% at compile-time; 0 runtime stack usage!
constexpr uint32_t factorial(uint32_t n) noexcept {
    uint32_t result = 1;
    for (uint32_t i = 2; i &lt;= n; ++i) {
        result *= i;
    }
    return result;
}

// Stored as an immediate constant in Flash ROM
constexpr uint32_t FACT_6 = factorial(6); // Emits MOV R0, #720</pre>
        """,
        "quiz": [
            {
                "question": "Why is recursion strictly prohibited by safety standards like MISRA C++ and NASA Power of 10?",
                "options": ["It creates variable-depth stack growth that risks catastrophic stack overflow in memory-constrained microcontrollers", "Recursion requires an operating system kernel", "Recursive functions cannot access global variables", "Recursion causes hardware clock jitter"],
                "correct": 0,
                "explanation": "Recursion makes maximum stack depth difficult to prove statically, posing severe risks of stack overflow crashes on microcontrollers with small fixed stacks."
            },
            {
                "question": "What is 'Tail Call Optimization' (TCO)?",
                "options": ["A compiler optimization where a recursive call at the end of a function reuses the current stack frame instead of allocating a new one", "A method for encrypting function returns", "A tool for debugging stack frames", "An algorithm that reverses array elements"],
                "correct": 0,
                "explanation": "TCO converts a tail-recursive function into a jump loop in assembly, executing in $O(1)$ stack space without growing the call stack."
            },
            {
                "question": "What is the runtime execution cost of a constexpr function evaluated with constant arguments at compile time?",
                "options": ["0 clock cycles and 0 stack frames at runtime; the precomputed value is embedded as an immediate constant", "1 clock cycle per recursive step", "50 clock cycles", "The same cost as runtime recursion"],
                "correct": 0,
                "explanation": "<code>constexpr</code> functions with constant arguments are computed by the compiler during compilation, embedding results directly into the binary."
            },
            {
                "question": "In a FreeRTOS task with a 512-byte stack, what happens if recursion depth exceeds available memory?",
                "options": ["A stack overflow occurs, corrupting task control blocks (TCBs) and triggering a fatal crash or vApplicationStackOverflowHook()", "The RTOS automatically doubles the stack size", "The recursive calls are redirected to flash", "The CPU ignores further function calls"],
                "correct": 0,
                "explanation": "Exceeding task stack bounds overflows into adjacent memory, corrupting RTOS task data structures and crashing the system."
            }
        ]
    },
    {
        "id": "math_fun",
        "name": "MathFun",
        "title": "Standard Math Library (<cmath>) vs Integer Fast Approximations",
        "headline": "pow, sqrt, sin in <cmath> vs Fast Integer Approximations (Lookup Tables & CORDIC)",
        "emb_class": "emb-high",
        "emb_badge": "⚡ Embedded Relevance: High",
        "tags": ["<cmath>", "FPU", "CORDIC", "Fast Integer Math", "Lookup Tables"],
        "summary": "Exploring mathematical functions in <cmath> (pow, sqrt, abs). We analyze why generic floating-point math libraries cause Flash bloat and execution delays on microcontrollers, and implement high-speed integer approximations (like integer sqrt and CORDIC trigonometry).",
        "files": ["section_5/MathFun/MathFun/main.cpp"],
        "concepts_html": """
        <h3>1. Standard <code>&lt;cmath&gt;</code> Functions</h3>
        <p>Standard C++ math functions (<code>std::pow</code>, <code>std::sqrt</code>, <code>std::sin</code>) operate on <code>double</code> precision by default. In resource-constrained systems, they add significant library overhead.</p>

        <h3>2. Integer Powers vs <code>std::pow</code></h3>
        <p>Using <code>std::pow(x, 2)</code> uses transcendental log/exp algorithms taking dozens of cycles. Simple multiplication (<code>x * x</code>) executes in a single cycle.</p>
        """,
        "embedded_html": """
        <h3>1. Hardware CORDIC Co-Processors</h3>
        <p>Modern microcontrollers (such as STM32G4 / STM32H7) include hardware <strong>CORDIC (Coordinate Rotation Digital Computer)</strong> accelerator peripherals that compute trigonometric, hyperbolic, and square root operations in <strong>sub-microsecond hardware cycles</strong>.</p>

        <h3>2. Fast Integer Square Root</h3>
        <p>For chips without FPUs, bitwise integer square root algorithms compute exact integer roots using simple bit shifts and subtractions.</p>
        """,
        "refactor_html": """
        <p>Fast bitwise integer square root (0 float overhead):</p>
        <pre class="code-block" style="background:#0d1117; padding:16px; border-radius:8px; border:1px solid #30363d;">#include &lt;cstdint&gt;

// Fast integer square root algorithm (Deterministic O(1) loop)
uint32_t isqrt(uint32_t val) noexcept {
    uint32_t res = 0;
    uint32_t bit = 1UL &lt;&lt; 30; // Second-to-top bit set

    while (bit &gt; val) bit &gt;&gt;= 2;

    while (bit != 0) {
        if (val &gt;= res + bit) {
            val -= res + bit;
            res = (res &gt;&gt; 1) + bit;
        } else {
            res &gt;&gt;= 1;
        }
        bit &gt;&gt;= 2;
    }
    return res;
}</pre>
        """,
        "quiz": [
            {
                "question": "Why is 'std::pow(x, 2.0)' an anti-pattern when squaring a number in performance-critical firmware?",
                "options": ["std::pow uses generic exp(2 * log(x)) algorithms taking dozens of cycles, whereas 'x * x' compiles to a single-cycle hardware multiplication", "std::pow cannot accept numbers greater than 100", "std::pow only works on 64-bit Linux systems", "std::pow deletes the variable x"],
                "correct": 0,
                "explanation": "<code>std::pow()</code> implements general exponentiation via transcendental algorithms; simple squaring should always be written as <code>x * x</code>."
            },
            {
                "question": "What is a CORDIC hardware accelerator on microcontrollers like STM32G4?",
                "options": ["A dedicated hardware co-processor that computes trigonometric, logarithmic, and square root operations in hardware with zero CPU load", "A tool that monitors battery voltage", "A software compiler optimization", "An external SPI memory chip"],
                "correct": 0,
                "explanation": "CORDIC hardware co-processors perform iterative vector rotation in hardware, delivering fast sine, cosine, and sqrt values for motor control."
            },
            {
                "question": "What precision does standard 'sqrt(x)' in <cmath> use when passed a float without the 'f' suffix in C++?",
                "options": ["double precision (64-bit)", "single precision (32-bit)", "16-bit integer", "arbitrary precision"],
                "correct": 0,
                "explanation": "In standard C/C++, <code>sqrt()</code> evaluates with <code>double</code> precision; single-precision floats require <code>std::sqrt(float)</code> or <code>sqrtf()</code>."
            },
            {
                "question": "How does integer square root (isqrt) benefit sensor processing on microcontrollers without an FPU?",
                "options": ["It computes square roots using simple bit shifts and additions in integer registers with zero software float library bloat", "It converts the sensor to analog mode", "It encrypts sensor telemetry", "It forces the ADC to sample at 100MHz"],
                "correct": 0,
                "explanation": "Bitwise integer square root algorithms use only integer ALU operations, avoiding slow software floating-point emulation routines."
            }
        ]
    },
    {
        "id": "count_down",
        "name": "CountDown",
        "title": "Loop Timing, Delay Loops vs Hardware Timers & RTOS Delays",
        "headline": "Software Busy-Wait Delays vs Hardware SysTick Timers & RTOS vTaskDelay",
        "emb_class": "emb-high",
        "emb_badge": "⚡ Embedded Relevance: Critical",
        "tags": ["Hardware Timers", "SysTick", "vTaskDelay", "Busy-Wait", "Low Power WFI"],
        "summary": "Exploring loop countdowns and delays. We demonstrate why software busy-wait loops (for(volatile int i=0...)) waste battery power and jitter across compiler optimization levels, and replace them with hardware SysTick timers and RTOS sleep delays (WFI).",
        "files": ["section_5/CountDown/CountDown/main.cpp"],
        "concepts_html": """
        <h3>1. Count-Down Loop Structures</h3>
        <p>Loops counting down to zero (<code>while (n &gt; 0) --n;</code>) often generate more efficient assembly on ARM processors because comparing against zero is handled automatically by CPU condition flags (<code>SUBS</code> instruction).</p>
        """,
        "embedded_html": """
        <h3>1. The Evils of Software Busy-Wait Loops</h3>
        <p>Software spin loops (<code>for (int i=0; i&lt;100000; ++i);</code>):</p>
        <ul>
          <li><strong>Are Optimized Away:</strong> Without <code>volatile</code>, the compiler deletes empty loops entirely under <code>-O2</code> or <code>-O3</code>.</li>
          <li><strong>Waste Battery:</strong> The CPU burns maximum active current (e.g. 20mA) instead of sleeping.</li>
          <li><strong>Are Non-Deterministic:</strong> Delay duration changes drastically if CPU clock frequency or compiler flags change.</li>
        </ul>

        <h3>2. Hardware SysTick & RTOS <code>vTaskDelay()</code></h3>
        <p>Production firmware uses hardware timer interrupts (SysTick) and puts the CPU to sleep using <strong>Wait For Interrupt (<code>WFI</code>)</strong>, reducing current draw by 99%.</p>
        """,
        "refactor_html": """
        <p>Non-blocking hardware timer delay:</p>
        <pre class="code-block" style="background:#0d1117; padding:16px; border-radius:8px; border:1px solid #30363d;">#include &lt;cstdint&gt;

extern volatile uint32_t g_system_ticks_ms; // Incremented by SysTick_Handler

void delay_ms(uint32_t ms) noexcept {
    uint32_t start = g_system_ticks_ms;
    while ((g_system_ticks_ms - start) &lt; ms) {
        __asm volatile("wfi"); // Wait For Interrupt: Sleep CPU until next timer tick!
    }
}</pre>
        """,
        "quiz": [
            {
                "question": "Why is an empty software delay loop (for(int i=0; i<10000; i++)) dangerous in production code?",
                "options": ["The optimizing compiler will delete the loop entirely, resulting in zero delay", "It causes an immediate memory leak", "It permanently disables interrupts", "It reboots the microcontroller"],
                "correct": 0,
                "explanation": "Because the loop has no observable side effects, modern optimizing compilers (<code>-O2</code>/<code>-O3</code>) completely remove empty loops."
            },
            {
                "question": "What does the ARM assembly instruction 'WFI' (Wait For Interrupt) do?",
                "options": ["Puts the CPU core into a low-power sleep state until the next hardware interrupt fires, drastically reducing current draw", "Resets the CPU stack pointer", "Waits for a serial character from UART", "Disables all hardware timers"],
                "correct": 0,
                "explanation": "<code>WFI</code> suspends CPU execution and clocks until an interrupt arrives, dropping current consumption to microamps."
            },
            {
                "question": "Why does counting down to zero (while(n-- > 0)) often produce smaller assembly code on ARM processors than counting up?",
                "options": ["ARM arithmetic instructions (SUBS) update the zero flag (Z) automatically, eliminating separate comparison (CMP) instructions", "ARM cannot count upwards", "The stack only allows decrements", "Down loops use 16-bit registers"],
                "correct": 0,
                "explanation": "The <code>SUBS</code> instruction subtracts and sets condition flags simultaneously; a branch instruction (<code>BNE</code>) can immediately test the zero flag without an extra <code>CMP</code> instruction."
            },
            {
                "question": "In FreeRTOS, what is the advantage of vTaskDelay(pdMS_TO_TICKS(100)) over a busy loop?",
                "options": ["It yields the CPU to lower-priority tasks and puts the current task into the Blocked state until the delay expires", "It overclock the CPU", "It disables task scheduling", "It formats the heap"],
                "correct": 0,
                "explanation": "<code>vTaskDelay</code> blocks the calling task, allowing other application tasks to execute while consuming zero CPU cycles."
            }
        ]
    },
    {
        "id": "count_evens",
        "name": "CountEvens",
        "title": "Bitwise Parity, Modulo Division & Branchless Algorithms",
        "headline": "Modulo (%) vs Bitwise AND (& 1) & Branchless Counting in Assembly",
        "emb_class": "emb-core",
        "emb_badge": "⚡ Embedded Relevance: Core",
        "tags": ["Bitwise &", "Modulo %", "Branchless", "Condition Codes", "Optimization"],
        "summary": "Analyzing parity checks and filtering in arrays. We contrast expensive hardware division (num % 2) with single-cycle bitwise operations (num & 1) and demonstrate branchless arithmetic algorithms that eliminate pipeline flushes.",
        "files": ["section_5/CountEvens/CountEvens/main.cpp"],
        "concepts_html": """
        <h3>1. Parity Checking: Modulo vs Bitwise</h3>
        <p>In standard arithmetic, even numbers satisfy <code>num % 2 == 0</code>. In binary representations, the Least Significant Bit (LSB) determines parity: <code>(num &amp; 1) == 0</code>.</p>
        """,
        "embedded_html": """
        <h3>1. Hardware Division vs Bitwise Masking</h3>
        <p>On microcontrollers lacking hardware division (e.g. ARM Cortex-M0), modulo division (<code>%</code>) calls software division routines (<code>__aeabi_idivmod</code>) taking 20-50 cycles. Bitwise AND (<code>&amp; 1</code>) executes in <strong>1 clock cycle</strong>.</p>

        <h3>2. Branchless Counting</h3>
        <p>By computing <code>count += (val &amp; 1) ^ 1</code>, code runs without <code>if</code> statements, eliminating CPU pipeline branch stalls.</p>
        """,
        "refactor_html": """
        <p>Branchless even-number counter:</p>
        <pre class="code-block" style="background:#0d1117; padding:16px; border-radius:8px; border:1px solid #30363d;">#include &lt;cstdint&gt;
#include &lt;cstddef&gt;

size_t countEvensBranchless(const uint32_t* data, size_t len) noexcept {
    size_t count = 0;
    for (size_t i = 0; i &lt; len; ++i) {
        // Branchless: (data[i] & 1) is 0 for even, 1 for odd
        count += (data[i] &amp; 1) ^ 1;
    }
    return count;
}</pre>
        """,
        "quiz": [
            {
                "question": "Why is '(num & 1) == 0' preferred over 'num % 2 == 0' on low-power microcontrollers?",
                "options": ["Bitwise AND is a single-cycle ALU instruction, whereas modulo may require expensive hardware or software division", "Modulo only works with positive floating-point numbers", "Bitwise AND prevents memory leaks", "Modulo requires heap memory allocation"],
                "correct": 0,
                "explanation": "Bitwise masking checks the least significant bit in 1 clock cycle, avoiding costly division instructions."
            },
            {
                "question": "What is the advantage of 'branchless programming' in high-speed firmware?",
                "options": ["It replaces conditional jump branches with arithmetic instructions, preventing CPU pipeline stalls and branch misprediction penalties", "It makes C++ code look shorter", "It removes the need for functions", "It runs without a power supply"],
                "correct": 0,
                "explanation": "Branchless code eliminates <code>if</code> branches, ensuring the CPU pipeline flows smoothly without stalls caused by branch mispredictions."
            },
            {
                "question": "What does '(val & 1) ^ 1' evaluate to when val is an even integer (e.g. 4)?",
                "options": ["1 (true)", "0 (false)", "4", "2"],
                "correct": 0,
                "explanation": "For even numbers: <code>val & 1 = 0</code>. Then <code>0 ^ 1 = 1</code>."
            },
            {
                "question": "Which ARM Cortex-M core lacks a hardware integer divide instruction (SDIV/UDIV)?",
                "options": ["ARM Cortex-M0 / Cortex-M0+", "ARM Cortex-M3", "ARM Cortex-M4", "ARM Cortex-M7"],
                "correct": 0,
                "explanation": "ARM Cortex-M0 and M0+ cores omit hardware division hardware to minimize silicon area and power consumption."
            }
        ]
    },
    {
        "id": "average_of_three",
        "name": "AverageOfThree",
        "title": "Integer Division Truncation & Rounding Corrections",
        "headline": "Integer Division Truncation vs Fixed-Point Scaling & Rounding Invariants",
        "emb_class": "emb-core",
        "emb_badge": "⚡ Embedded Relevance: Core",
        "tags": ["Integer Division", "Truncation", "Rounding Math", "Fixed-Point", "Arithmetic"],
        "summary": "Calculating statistical averages. We explore integer division truncation, precision loss in sensor data processing, and rounding strategies in integer arithmetic (e.g. (sum + N/2) / N).",
        "files": ["section_5/AverageOfThree/AverageOfThree/main.cpp"],
        "concepts_html": """
        <h3>1. Integer Division Truncation</h3>
        <p>In C++, dividing two integers truncates toward zero (<code>7 / 3 = 2</code>), discarding fractional remainders.</p>

        <h3>2. Correct Integer Rounding Idiom</h3>
        <p>To round to the nearest integer instead of truncating, add half the divisor before dividing: <code>(sum + (N / 2)) / N</code>.</p>
        """,
        "embedded_html": """
        <h3>1. Sensor Sampling Precision Loss</h3>
        <p>Raw ADC readings averaged via integer math suffer cumulative truncation bias. Fixed-point scaling (e.g. multiplying by 1000 before division) preserves millivolt precision without requiring floating-point calculations.</p>
        """,
        "refactor_html": """
        <p>Properly rounded integer average:</p>
        <pre class="code-block" style="background:#0d1117; padding:16px; border-radius:8px; border:1px solid #30363d;">#include &lt;cstdint&gt;

// Integer average with nearest-integer rounding
constexpr uint32_t averageThreeRounded(uint32_t a, uint32_t b, uint32_t c) noexcept {
    return (a + b + c + 1) / 3; // Adding divisor/2 (1 for divisor 3) rounds correctly
}</pre>
        """,
        "quiz": [
            {
                "question": "What is the result of the C++ integer expression '10 / 4'?",
                "options": ["2 (truncated toward zero)", "2.5", "3 (rounded up)", "0"],
                "correct": 0,
                "explanation": "Integer division in C++ discards fractional remainders, yielding 2."
            },
            {
                "question": "How do you achieve nearest-integer rounding when dividing an integer 'sum' by 'N' in integer arithmetic?",
                "options": ["(sum + (N / 2)) / N", "sum / N + 0.5", "(sum * N) / 2", "sum % N"],
                "correct": 0,
                "explanation": "Adding half the divisor (<code>N / 2</code>) before dividing rounds values $\\ge 0.5$ up to the next integer."
            },
            {
                "question": "Why should sensor ADC averaging avoid pure floating-point math on small microcontrollers?",
                "options": ["Floating-point division is slow and non-deterministic on MCUs without an FPU, whereas scaled integer math executes in single-digit clock cycles", "Float math destroys ADC calibration", "Floats cannot hold numbers smaller than 1", "Floating point math only works on Linux"],
                "correct": 0,
                "explanation": "Integer math executes rapidly on all microcontrollers; fixed-point scaling preserves precision without the cycle overhead of software float emulation."
            },
            {
                "question": "What is the risk of calculating '(a + b + c) / 3' when a, b, and c are large uint32_t values near 2^32 - 1?",
                "options": ["Integer overflow occurs during the addition before division takes place, producing a completely incorrect result", "The division fails with a CPU exception", "The compiler converts them to negative integers", "The compiler reorders the terms to prevent overflow"],
                "correct": 0,
                "explanation": "Summing large integers can overflow 32 bits before division. Using 64-bit accumulators (<code>uint64_t</code>) prevents overflow."
            }
        ]
    },
    {
        "id": "parameter_challenge",
        "name": "ParameterChallenge",
        "title": "Pass-by-Reference Mutators & Out-Parameter Design",
        "headline": "In-Out Parameters, Multiple Return Values & Struct Results vs std::tuple",
        "emb_class": "emb-core",
        "emb_badge": "⚡ Embedded Relevance: Core",
        "tags": ["Pass-by-Reference", "Out Parameters", "Multiple Returns", "Structured Binding", "C++17"],
        "summary": "Exploring functions that return multiple values via pass-by-reference out-parameters. We compare legacy out-parameters with modern C++17 structured bindings and small return structs.",
        "files": ["section_5/ParameterChallenge/ParameterChallenge/main.cpp"],
        "concepts_html": """
        <h3>1. Out-Parameters via References</h3>
        <p>Functions requiring multiple output values historically passed references or pointers as out-parameters (<code>void getCoordinates(int&amp; x, int&amp; y)</code>).</p>

        <h3>2. Modern Alternative: Value Structs & Structured Bindings</h3>
        <p>In C++17, returning a small struct by value is optimized via Return Value Optimization (RVO), enabling clean structured binding syntax: <code>auto [x, y] = getCoordinates();</code>.</p>
        """,
        "embedded_html": """
        <h3>1. RVO and Register Packing</h3>
        <p>Under the ARM AAPCS, small return structs containing two 32-bit integers are returned packed in registers <strong>R0 and R1</strong> with <strong>0 RAM overhead</strong>.</p>
        """,
        "refactor_html": """
        <p>Modern struct return with structured binding support:</p>
        <pre class="code-block" style="background:#0d1117; padding:16px; border-radius:8px; border:1px solid #30363d;">#include &lt;cstdint&gt;

struct Coordinate2D {
    int32_t x;
    int32_t y;
};

// Returned packed in registers R0 and R1 (0 stack traffic!)
constexpr Coordinate2D readGpsPosition() noexcept {
    return Coordinate2D{12345, 67890};
}</pre>
        """,
        "quiz": [
            {
                "question": "What feature introduced in C++17 allows cleanly unpacking members from a returned struct (auto [x, y] = getPos())?",
                "options": ["Structured Bindings", "Lambda Expressions", "Concepts", "Dynamic Casting"],
                "correct": 0,
                "explanation": "Structured bindings (C++17) allow directly unpacking struct members into local variables."
            },
            {
                "question": "How are small 2-word structs returned by value on ARM Cortex-M processors?",
                "options": ["Returned directly in hardware registers R0 and R1 without touching memory", "Allocated on the heap", "Stored in Flash memory", "Sent over the UART serial bus"],
                "correct": 0,
                "explanation": "Under AAPCS, return values up to 8 bytes (two 32-bit words) are passed back directly in CPU registers R0 and R1."
            },
            {
                "question": "Why is returning a struct by value often cleaner than using multiple non-const reference out-parameters?",
                "options": ["It makes function inputs and outputs explicit at the call site and eliminates pointer aliasing issues", "It allows functions to have duplicate names", "It disables compiler warnings", "It makes the function run in background threads"],
                "correct": 0,
                "explanation": "Returning structs keeps data flow clear and functional, avoiding side-effect bugs and compiler aliasing penalties."
            },
            {
                "question": "What is Return Value Optimization (RVO)?",
                "options": ["A compiler optimization that constructs a returned object directly into the caller's target storage, eliminating copy and move operations", "A technique to compress return values in Flash", "A method for checking return codes at runtime", "A compiler flag that deletes unused functions"],
                "correct": 0,
                "explanation": "RVO constructs the return value directly in the destination memory allocated by the caller, achieving zero copy overhead."
            }
        ]
    },
    {
        "id": "product_array_by_reference",
        "name": "ProductArrayByReference",
        "title": "Array Parameter Passing, Spans & Contiguous Memory Guarantees",
        "headline": "Passing Arrays by Reference (int(&)[N]) vs C++20 std::span in Embedded APIs",
        "emb_class": "emb-high",
        "emb_badge": "⚡ Embedded Relevance: High",
        "tags": ["Array References", "std::span", "Size Preservation", "Bounds Safety", "C++20"],
        "summary": "Passing fixed arrays by reference (int(&)[N]) to prevent pointer decay. We analyze template-based array references and modern C++20 std::span for zero-overhead, non-owning contiguous memory views.",
        "files": ["section_5/ProductArrayByReference/ProductArrayByReference/main.cpp"],
        "concepts_html": """
        <h3>1. Passing Arrays by Reference Syntax</h3>
        <p>Writing <code>void compute(int (&amp;arr)[5])</code> passes the array by reference without decay. The compiler strictly enforces that only arrays of exactly length 5 can be passed.</p>

        <h3>2. C++20 <code>std::span</code></h3>
        <p><code>std::span&lt;T&gt;</code> is a lightweight non-owning view over any contiguous sequence of elements (pointer + size, 8 bytes total on 32-bit MCU).</p>
        """,
        "embedded_html": """
        <h3>1. Unified Buffer Passing with <code>std::span</code></h3>
        <p>In driver development, <code>std::span&lt;const uint8_t&gt;</code> can accept a C array, a <code>std::array</code>, or an RTOS buffer seamlessly with zero copying.</p>
        """,
        "refactor_html": """
        <p>Clean driver buffer API using <code>std::span</code>:</p>
        <pre class="code-block" style="background:#0d1117; padding:16px; border-radius:8px; border:1px solid #30363d;">#include &lt;cstdint&gt;
#include &lt;numeric&gt;

// Non-decaying template array reference
template &lt;typename T, size_t N&gt;
T computeProduct(const T (&amp;arr)[N]) noexcept {
    T product = 1;
    for (size_t i = 0; i &lt; N; ++i) {
        product *= arr[i];
    }
    return product;
}</pre>
        """,
        "quiz": [
            {
                "question": "What is the key advantage of passing an array by reference using 'void func(int (&arr)[10])'?",
                "options": ["It prevents array-to-pointer decay, preserving compile-time size and preventing incorrect array sizes from being passed", "It makes the array dynamic", "It copies the array to the heap", "It doubles the array capacity"],
                "correct": 0,
                "explanation": "Array references (<code>(&amp;arr)[N]</code>) retain full array size metadata and cause compilation to fail if an array with different bounds is passed."
            },
            {
                "question": "What is C++20 std::span?",
                "options": ["A lightweight, non-owning view over contiguous memory storing a pointer and element count (8 bytes on 32-bit MCU)", "A dynamic heap container that resizes automatically", "A thread synchronization primitive", "A hardware timer driver"],
                "correct": 0,
                "explanation": "<code>std::span</code> represents a contiguous sequence of objects without owning the memory, encapsulating a pointer and length in a compact 8-byte structure."
            },
            {
                "question": "Does passing a std::span<uint8_t> copy the underlying array buffer?",
                "options": ["No, std::span is a non-owning view; only the pointer and size are passed", "Yes, it creates a deep copy in SRAM", "Yes, it copies data to Flash", "It moves data to the heap"],
                "correct": 0,
                "explanation": "<code>std::span</code> is a non-owning view; passing it passes only the pointer and length, performing zero buffer copying."
            },
            {
                "question": "Can std::span prevent buffer overflows in embedded drivers?",
                "options": ["Yes, std::span tracks buffer size, allowing range-based iteration and bounds-checked .subspan() operations", "No, spans disable bounds checking", "Only on 64-bit systems", "Only if memory is allocated on the heap"],
                "correct": 0,
                "explanation": "<code>std::span</code> retains element counts, enabling safe range-based iteration and bounded slicing."
            }
        ]
    },
    {
        "id": "product_array_object",
        "name": "ProductArrayObject",
        "title": "std::array Container Passing & Zero-Overhead Abstractions",
        "headline": "std::array Member Encapsulation, Iterators & Zero-Overhead C++ Idioms",
        "emb_class": "emb-core",
        "emb_badge": "⚡ Embedded Relevance: Core",
        "tags": ["std::array", "Zero-Cost Abstraction", "Iterators", "Const Reference", "Clean Code"],
        "summary": "Using std::array as an object container. We demonstrate how std::array provides STL iterator compatibility (begin/end) and value-type semantics while generating assembly identical to raw C arrays.",
        "files": ["section_5/ProductArrayObject/ProductArrayObject/main.cpp"],
        "concepts_html": """
        <h3>1. <code>std::array</code> as a First-Class Object</h3>
        <p>Unlike raw C arrays, <code>std::array</code> behaves as a first-class C++ object: it can be assigned (<code>=</code>), passed by value/reference, returned from functions, and queried for size (<code>.size()</code>).</p>
        """,
        "embedded_html": """
        <h3>1. Zero-Cost Abstraction Verification</h3>
        <p>Disassembling <code>std::array</code> member access in GCC/Clang reveals that <code>arr[i]</code> compiles to the exact same single-instruction memory load (<code>LDR</code>) as a raw C array, incurring <strong>zero performance or memory penalty</strong>.</p>
        """,
        "refactor_html": """
        <p>Functional array multiplication using standard algorithms:</p>
        <pre class="code-block" style="background:#0d1117; padding:16px; border-radius:8px; border:1px solid #30363d;">#include &lt;cstdint&gt;
#include &lt;array&gt;
#include &lt;numeric&gt;

template &lt;size_t N&gt;
uint32_t computeArrayProduct(const std::array&lt;uint32_t, N&gt;&amp; arr) noexcept {
    return std::accumulate(arr.begin(), arr.end(), 1UL, std::multiplies&lt;uint32_t&gt;());
}</pre>
        """,
        "quiz": [
            {
                "question": "Why is std::array considered a 'zero-cost abstraction' in C++?",
                "options": ["It wraps a raw C array with modern container interfaces without adding any memory overhead or runtime instruction penalties", "It is free to download from GitHub", "It uses 0 bytes of Flash memory", "It requires no CPU power"],
                "correct": 0,
                "explanation": "<code>std::array</code> contains only the underlying array; all member functions are inline and compile to identical assembly as raw C arrays."
            },
            {
                "question": "Can std::array be returned by value from a function without dynamic memory allocation?",
                "options": ["Yes, std::array is a value type that resides on the stack and is returned via Return Value Optimization (RVO)", "No, it requires malloc", "Only in C++23", "Only if size is 1"],
                "correct": 0,
                "explanation": "<code>std::array</code> is a standard value struct stored on the stack; modern compilers return it with zero heap allocation using RVO."
            },
            {
                "question": "What happens if you assign one std::array to another of the same type and size (arr1 = arr2)?",
                "options": ["A member-wise copy of all elements from arr2 to arr1 is performed", "Only the pointer address is copied", "A compiler error occurs", "Memory is allocated on the heap"],
                "correct": 0,
                "explanation": "<code>std::array</code> defines value copy assignment, copying all elements directly."
            },
            {
                "question": "Which method on std::array returns a raw pointer to the underlying contiguous C array?",
                "options": [".data()", ".raw()", ".get_ptr()", ".pointer()"],
                "correct": 0,
                "explanation": "<code>arr.data()</code> returns a direct pointer (<code>T*</code>) to the underlying contiguous buffer for C API compatibility."
            }
        ]
    },
    {
        "id": "return_type_parameter_fun",
        "name": "ReturnTypeParameterFun",
        "title": "Return Types, Side Effects & Pure Functions in Firmware",
        "headline": "Void Functions, In-Out Side Effects vs Pure Functions & [[nodiscard]]",
        "emb_class": "emb-core",
        "emb_badge": "⚡ Embedded Relevance: Core",
        "tags": ["Return Types", "Pure Functions", "[[nodiscard]]", "Side Effects", "Idempotence"],
        "summary": "Exploring return types and function side effects. We examine pure functions vs state-mutating functions and demonstrate how the [[nodiscard]] attribute prevents bugs by enforcing inspection of status returns.",
        "files": ["section_5/ReturnTypeParameterFun/ReturnTypeParameterFun/main.cpp"],
        "concepts_html": """
        <h3>1. Pure Functions vs Side Effects</h3>
        <ul>
          <li><strong>Pure Functions:</strong> Given the same arguments, always return the same result without modifying global state or hardware.</li>
          <li><strong>Side-Effecting Functions:</strong> Mutate global variables, modify parameters, or access hardware I/O registers.</li>
        </ul>
        """,
        "embedded_html": """
        <h3>1. The <code>[[nodiscard]]</code> Attribute</h3>
        <p>In firmware, functions returning error codes or hardware ACK statuses must not be ignored. Marking them <code>[[nodiscard]]</code> forces the compiler to flag ignored return values as errors.</p>
        """,
        "refactor_html": """
        <p>Enforcing error code checking with [[nodiscard]]:</p>
        <pre class="code-block" style="background:#0d1117; padding:16px; border-radius:8px; border:1px solid #30363d;">#include &lt;cstdint&gt;

enum class SpiStatus : uint8_t { Ok = 0, Busy, Timeout, WriteCollision };

[[nodiscard]] SpiStatus transmitByte(uint8_t byte) noexcept {
    // Write to SPI Data Register...
    return SpiStatus::Ok;
}</pre>
        """,
        "quiz": [
            {
                "question": "What is a 'pure function' in software architecture?",
                "options": ["A function whose return value depends solely on its input arguments with zero observable side effects on external state or hardware", "A function written in assembly language", "A function with no return type", "A function that runs in interrupt context"],
                "correct": 0,
                "explanation": "Pure functions depend only on inputs and cause no side effects (no global writes, no I/O), making them trivial to test and optimize."
            },
            {
                "question": "What compile-time protection does [[nodiscard]] provide when placed on a function?",
                "options": ["It emits a compiler warning/error if the caller calls the function without storing or inspecting its return value", "It prevents the function from returning null", "It makes the function execute faster", "It moves the function to Flash memory"],
                "correct": 0,
                "explanation": "<code>[[nodiscard]]</code> alerts the developer if a return value (like a status code) is discarded, preventing unhandled error bugs."
            },
            {
                "question": "Why is managing function side effects critical in concurrent RTOS tasks?",
                "options": ["Uncontrolled side effects on shared global variables create race conditions and data corruption without mutex protection", "Side effects delete task stacks", "Side effects lower microcontroller clock speeds", "Side effects disable compiler optimizations"],
                "correct": 0,
                "explanation": "Modifying shared global variables across tasks without synchronization causes race conditions and memory corruption."
            },
            {
                "question": "Can the compiler optimize away repeated calls to a pure function with identical arguments?",
                "options": ["Yes, the compiler can memoize or evaluate pure functions at compile time (Common Subexpression Elimination)", "No, every call must execute at runtime", "Only if written in C", "Only on 64-bit systems"],
                "correct": 0,
                "explanation": "Because pure functions have no side effects, compilers can optimize redundant calls through Common Subexpression Elimination."
            }
        ]
    },
    {
        "id": "scope_fun",
        "name": "ScopeFun",
        "title": "Variable Scope, Lifetime & Memory Storage Durations",
        "headline": "Local vs Global Scope, Static Variables (.data/.bss) & Reentrancy Hazards",
        "emb_class": "emb-high",
        "emb_badge": "⚡ Embedded Relevance: Critical",
        "tags": ["Scope", "Lifetime", "Static Variables", "Reentrancy", ".data vs .bss"],
        "summary": "Analyzing variable scope and lifetime: local (automatic stack), global, and local static storage. We analyze the memory map placement of static variables (.data vs .bss) and the severe reentrancy hazards of static variables in multi-threaded RTOS tasks.",
        "files": ["section_5/ScopeFun/ScopeFun/main.cpp"],
        "concepts_html": """
        <h3>1. Storage Duration Categories</h3>
        <ul>
          <li><strong>Automatic (Stack):</strong> Created at block entry, destroyed at block exit.</li>
          <li><strong>Static (RAM):</strong> Allocated once at startup, persists for the entire program execution.</li>
          <li><strong>Dynamic (Heap):</strong> Allocated via <code>new</code>, persists until <code>delete</code>.</li>
        </ul>
        """,
        "embedded_html": """
        <h3>1. The Reentrancy Hazard of Local Static Variables</h3>
        <p>A function containing a local static variable (<code>static int counter = 0;</code>) is <strong>NOT reentrant</strong>. If an interrupt routine (ISR) preempts the function and calls it again, or if two RTOS tasks execute it concurrently, the static variable will suffer race conditions.</p>

        <h3>2. Memory Placement: <code>.data</code> vs <code>.bss</code></h3>
        <p>Initialized static variables live in <code>.data</code> (copied from Flash to RAM at boot). Uninitialized static variables live in <code>.bss</code> (zeroed at boot).</p>
        """,
        "refactor_html": """
        <p>Reentrant task-safe function design:</p>
        <pre class="code-block" style="background:#0d1117; padding:16px; border-radius:8px; border:1px solid #30363d;">#include &lt;cstdint&gt;

// Reentrant: All state is passed via caller-provided context (Zero static state)
struct CounterContext {
    uint32_t count{0};
};

uint32_t incrementReentrant(CounterContext&amp; ctx) noexcept {
    return ++ctx.count; // 100% thread-safe across independent tasks
}</pre>
        """,
        "quiz": [
            {
                "question": "What is a 'reentrant function' in embedded systems?",
                "options": ["A function that can be safely interrupted and called simultaneously by another task or ISR without corrupting data", "A function that calls itself recursively", "A function stored in ROM", "A function that has no arguments"],
                "correct": 0,
                "explanation": "Reentrant functions rely only on caller-provided stack data and avoid shared static/global state, allowing safe concurrent execution."
            },
            {
                "question": "Why does a function containing a local 'static int count = 0;' fail reentrancy checks in an RTOS?",
                "options": ["The static variable resides in shared global RAM; concurrent execution by multiple threads or ISRs produces race conditions", "Static variables cannot be modified", "Static variables are erased when an interrupt fires", "Static variables use double precision"],
                "correct": 0,
                "explanation": "Local static variables share a single global memory location across all invocations, creating race conditions when called concurrently."
            },
            {
                "question": "Where is an initialized global variable (int sensor_id = 42;) stored in the microcontroller memory map?",
                "options": [".data section in RAM (initialized from Flash ROM during startup)", ".bss section in RAM", ".text section in ROM", ".stack section"],
                "correct": 0,
                "explanation": "Initialized static/global variables reside in <code>.data</code>; their initial values are stored in Flash and copied into RAM by startup code."
            },
            {
                "question": "What is the lifetime of a local variable declared inside a function body?",
                "options": ["Automatic lifetime: allocated on the stack when the enclosing block is entered and destroyed upon exit", "Permanent lifetime: exists until power-off", "Exists until explicitly deleted", "Exists for 1 millisecond"],
                "correct": 0,
                "explanation": "Local variables have automatic storage duration, existing only while execution is inside their enclosing lexical block."
            }
        ]
    },
    {
        "id": "scope_challenge",
        "name": "ScopeChallenge",
        "title": "Variable Shadowing, Namespace Pollution & Static Encapsulation",
        "headline": "Shadowing Pitfalls, Anonymous Namespaces vs C static & MISRA Scope Rules",
        "emb_class": "emb-core",
        "emb_badge": "⚡ Embedded Relevance: Core",
        "tags": ["Variable Shadowing", "Anonymous Namespaces", "static linkage", "MISRA C++"],
        "summary": "Practicing scope resolution and diagnosing variable shadowing bugs. We explore anonymous namespaces in C++ vs static file linkage in C, and analyze MISRA C++ guidelines for restricting variable scope to the narrowest possible block.",
        "files": ["section_5/ScopeChallenge/ScopeChallenge/main.cpp"],
        "concepts_html": """
        <h3>1. Variable Shadowing</h3>
        <p>Shadowing occurs when an inner block declares a variable with the same name as an outer block variable. The inner variable hides the outer one, causing logic errors where developers assume they are modifying the outer variable.</p>

        <h3>2. Anonymous Namespaces vs <code>static</code> Linkage</h3>
        <p>In modern C++, anonymous namespaces (<code>namespace { ... }</code>) replace C-style <code>static</code> functions/variables, providing internal linkage with full type safety.</p>
        """,
        "embedded_html": """
        <h3>1. MISRA C++:2008 Rule 2-10-2</h3>
        <p>Identifiers declared in an inner scope shall not hide an identifier declared in an outer scope. Compilers should enforce <code>-Wshadow</code> to eliminate shadowing bugs at compile time.</p>
        """,
        "refactor_html": """
        <p>Internal linkage with anonymous namespaces:</p>
        <pre class="code-block" style="background:#0d1117; padding:16px; border-radius:8px; border:1px solid #30363d;">#include &lt;cstdint&gt;

namespace {
    // Internal linkage: Invisible to other translation units (Zero symbol collisions)
    constexpr uint32_t INTERNAL_TIMEOUT_MS = 500;
    
    void configureHardwarePll() noexcept {
        // Driver internal initialization...
    }
}</pre>
        """,
        "quiz": [
            {
                "question": "What is 'variable shadowing'?",
                "options": ["Declaring a variable in an inner block that has the exact same name as a variable in an enclosing outer block, hiding the outer variable", "Allocating variables in dark theme IDEs", "Copying variables into Flash ROM", "Deleting a pointer twice"],
                "correct": 0,
                "explanation": "Shadowing hides outer variables with an identically named local variable, leading to subtle modification bugs."
            },
            {
                "question": "Which compiler warning flag catches variable shadowing bugs during compilation?",
                "options": ["-Wshadow", "-Werror", "-Wall", "-O3"],
                "correct": 0,
                "explanation": "<code>-Wshadow</code> instructs the compiler to emit a warning whenever an inner variable shadows an outer identifier."
            },
            {
                "question": "What is the purpose of an anonymous namespace (namespace { ... }) in a C++ source file?",
                "options": ["It grants internal linkage to enclosed variables and functions, restricting their visibility to that single translation unit", "It makes variables public to all files", "It encrypts variable names in memory", "It creates a dynamic heap pool"],
                "correct": 0,
                "explanation": "Anonymous namespaces give symbols internal linkage, preventing naming collisions across different <code>.cpp</code> files."
            },
            {
                "question": "What does MISRA C++ recommend regarding variable scope?",
                "options": ["Variables should be declared in the narrowest possible scope closest to their point of use", "All variables must be global", "Variables must be at least 100 lines long", "Variables can only be declared in header files"],
                "correct": 0,
                "explanation": "Declaring variables in the smallest feasible scope minimizes lifetime, reduces stack usage, and prevents accidental cross-block mutations."
            }
        ]
    },
    {
        "id": "tic_tac_toe",
        "name": "TicTacToe",
        "title": "State Machine Architecture & Modular Function Decomposition",
        "headline": "Modular Function Decomposition, Game State Machines & Embedded UI Input Scanning",
        "emb_class": "emb-high",
        "emb_badge": "⚡ Embedded Relevance: High",
        "tags": ["State Machines", "Modularity", "Matrix Grid", "Input Debouncing", "Embedded Architecture"],
        "summary": "Building a full interactive Tic-Tac-Toe system. We analyze functional modular decomposition, separation of display rendering from game logic state machines, and translating matrix grid games into embedded button matrix keypad scanning algorithms.",
        "files": ["section_5/Tic-Tac-Toe/Tic-Tac-Toe/main.cpp"],
        "concepts_html": """
        <h3>1. Functional Decomposition</h3>
        <p>Breaking a complex system into focused, single-responsibility functions (<code>drawBoard</code>, <code>getUserInput</code>, <code>checkWinCondition</code>, <code>switchPlayer</code>) maximizes testability and maintainability.</p>

        <h3>2. State Machine Logic</h3>
        <p>Managing turns, victory checks, and cat's game (draw) conditions using an explicit state machine model.</p>
        """,
        "embedded_html": """
        <h3>1. Matrix Keypad Scanning</h3>
        <p>In embedded hardware, a $3\\times 3$ grid is physically wired as a <strong>Matrix Keypad</strong> (3 row GPIOs, 3 column GPIOs). The microcontroller drives rows low sequentially and reads column inputs to detect button presses with hardware debounce filtering.</p>
        """,
        "refactor_html": """
        <p>Embedded matrix keypad scanner state machine:</p>
        <pre class="code-block" style="background:#0d1117; padding:16px; border-radius:8px; border:1px solid #30363d;">#include &lt;cstdint&gt;
#include &lt;array&gt;

enum class GridCell : uint8_t { Empty = 0, PlayerX, PlayerO };
enum class GameState : uint8_t { InProgress = 0, X_Won, O_Won, Draw };

class TicTacToeEngine {
private:
    std::array&lt;GridCell, 9&gt; board_{};
    GridCell current_player_{GridCell::PlayerX};

public:
    bool place_move(uint8_t cell_index) noexcept {
        if (cell_index &gt;= 9 || board_[cell_index] != GridCell::Empty) return false;
        board_[cell_index] = current_player_;
        current_player_ = (current_player_ == GridCell::PlayerX) ? GridCell::PlayerO : GridCell::PlayerX;
        return true;
    }

    const std::array&lt;GridCell, 9&gt;&amp; board() const noexcept { return board_; }
};</pre>
        """,
        "quiz": [
            {
                "question": "How does a microcontroller scan a 3x3 matrix button keypad using only 6 GPIO pins?",
                "options": ["It sequentially drives each row pin LOW and reads the 3 column pins to detect intersections", "It uses 9 separate analog-to-digital converters", "It connects all buttons to a single ground wire", "It uses WiFi telemetry"],
                "correct": 0,
                "explanation": "Matrix scanning drives one row active at a time and reads column pins, detecting 9 buttons with only 3 rows + 3 cols = 6 pins."
            },
            {
                "question": "Why is 'button debouncing' required when reading physical button matrix inputs?",
                "options": ["Mechanical switch contacts bounce physically for 5-20 milliseconds upon closing, creating rapid false transition pulses", "Buttons generate AC mains voltage", "To prevent the CPU clock from freezing", "To calibrate temperature drift"],
                "correct": 0,
                "explanation": "Mechanical contacts bounce when pressed; debouncing (software delay or timer filtering) ensures only a single stable transition is registered."
            },
            {
                "question": "What is the primary architectural advantage of decoupling game state logic from display rendering functions?",
                "options": ["The core state logic can be unit-tested on a PC without requiring physical LCD hardware or console I/O", "It makes the game run in 3D", "It compresses source code into binary", "It allows multiple players on CAN bus"],
                "correct": 0,
                "explanation": "Separating state logic from I/O allows running automated unit tests on host machines without hardware dependencies."
            },
            {
                "question": "How many total win combinations exist on a 3x3 Tic-Tac-Toe grid?",
                "options": ["8 combinations (3 horizontal rows, 3 vertical columns, 2 diagonals)", "9 combinations", "6 combinations", "12 combinations"],
                "correct": 0,
                "explanation": "There are 3 horizontal rows + 3 vertical columns + 2 diagonals = 8 possible winning lines."
            }
        ]
    }
]
