#!/usr/bin/env python3
"""
Section 4 Project Definitions: Arrays, Vectors & Memory Locality
Contains 11 comprehensive project definitions covering stack vs heap arrays,
cache-line locality, 2D memory layout, DMA transfers, and zero-heap std::array.
"""

SECTION_4_PROJECTS = [
    {
        "id": "array_fun",
        "name": "ArrayFun",
        "title": "C-Style Arrays, Stack Allocation & Bounds Hazards",
        "headline": "Fixed-Size C Arrays, Stack Allocation & Array Decay to Raw Pointers",
        "emb_class": "emb-high",
        "emb_badge": "⚡ Embedded Relevance: Critical",
        "tags": ["C-Style Arrays", "Stack Memory", "Array Decay", "sizeof Trap", "Buffer Overflow"],
        "summary": "Exploring foundational C-style arrays on the CPU stack. We examine array declaration, zero-based indexing, how arrays implicitly decay into raw pointers when passed to functions (losing size metadata), and why stack buffer overflows are the #1 cause of embedded security exploits.",
        "files": ["section_4/ArrayFun/ArrayFun/main.cpp"],
        "concepts_html": """
        <h3>1. Contiguous Stack Allocation</h3>
        <p>A C-style array (<code>int arr[5]</code>) allocates a contiguous sequence of elements directly on the current stack frame. The variable name <code>arr</code> represents the starting memory address of the block.</p>

        <h3>2. The Array-to-Pointer Decay Trap</h3>
        <p>When passed to a function (<code>void print(int arr[])</code>), the array decays into a raw pointer (<code>int*</code>). <code>sizeof(arr)</code> inside the function returns the pointer size (4 or 8 bytes), NOT the total array size!</p>
        """,
        "embedded_html": """
        <h3>1. Stack Buffer Overflows & Return Address Hijacking</h3>
        <p>In microcontrollers without virtual memory protection, writing beyond an array index corrupts the function's saved <strong>Link Register (LR) / Return Address</strong> on the stack frame. When the function returns, the CPU jumps to an arbitrary address, causing execution hijacking or HardFault crashes.</p>

        <h3>2. MISRA C++:2008 Rule 5-0-15</h3>
        <p>Array indexing shall be the only form of pointer arithmetic. Pointer decay when passing arrays across API boundaries is strongly discouraged in favor of <code>std::array</code> or bounded span wrappers.</p>
        """,
        "refactor_html": """
        <p>Replace raw decaying arrays with zero-overhead, size-preserving <code>std::array</code>:</p>
        <pre class="code-block" style="background:#0d1117; padding:16px; border-radius:8px; border:1px solid #30363d;">#include &lt;cstdint&gt;
#include &lt;array&gt;

// Type-safe, non-decaying array parameter
template &lt;size_t N&gt;
void processSamples(const std::array&lt;uint16_t, N&gt;&amp; samples) noexcept {
    static_assert(N &gt; 0, "Sample buffer cannot be empty");
    for (uint16_t val : samples) {
        // Process sensor sample...
    }
}</pre>
        """,
        "quiz": [
            {
                "question": "What happens when a C-style array is passed by value to a function (void func(int arr[]))?",
                "options": ["It decays into a raw pointer (int*), losing compile-time size information", "A deep copy of the entire array is pushed to the stack", "A compile-time syntax error is generated", "The array is moved into the heap"],
                "correct": 0,
                "explanation": "In C and C++, arrays passed by name decay into a pointer to the first element (<code>int*</code>), discarding container size information."
            },
            {
                "question": "Why is sizeof(arr) / sizeof(arr[0]) hazardous when used inside a function on a decayed array parameter?",
                "options": ["It computes sizeof(int*) / sizeof(int), yielding 1 on 32-bit MCUs regardless of actual array size", "It causes a hardware division-by-zero trap", "It dynamically allocates heap memory", "It changes the array elements to zero"],
                "correct": 0,
                "explanation": "Because the array decayed to a pointer, <code>sizeof(arr)</code> evaluates to the pointer size (4 bytes), yielding <code>4 / 4 = 1</code>."
            },
            {
                "question": "How does a stack buffer overflow compromise microcontroller firmware?",
                "options": ["Writing past array boundaries overwrites the saved return address (LR) on the stack, crashing the CPU or hijacking execution flow", "It erases the EEPROM memory chips", "It lowers the microcontroller voltage supply", "It permanently disables the JTAG debugger"],
                "correct": 0,
                "explanation": "The stack frame stores local variables adjacent to saved registers (LR/PC). Overwriting these registers diverts CPU execution to corrupted addresses."
            },
            {
                "question": "What is the memory overhead of std::array<int, 10> compared to a raw int arr[10] array?",
                "options": ["Exactly 0 bytes; std::array is a zero-cost abstraction with identical memory layout", "4 bytes for the size field", "16 bytes for heap allocator pointers", "24 bytes for virtual method tables"],
                "correct": 0,
                "explanation": "<code>std::array</code> contains only the underlying C array internally with zero extra members, making its size and memory layout identical to a raw array."
            }
        ]
    },
    {
        "id": "array_fun_test",
        "name": "ArrayFunTest",
        "title": "Array Initialization, Size Computation & Uninitialized Memory",
        "headline": "Array Size Calculation, Garbage Stack Data & Value-Initialization ({})",
        "emb_class": "emb-core",
        "emb_badge": "⚡ Embedded Relevance: Core",
        "tags": ["Array Initialization", "Value Init {}", "Garbage RAM", "sizeof", "BSS vs Stack"],
        "summary": "Analyzing array initialization syntax, calculating element counts via sizeof, and the dangers of uninitialized stack variables containing random SRAM power-on garbage.",
        "files": ["section_4/ArrayFunTest/ArrayFunTest/main.cpp"],
        "concepts_html": """
        <h3>1. Uninitialized Stack Arrays vs Value-Initialization</h3>
        <p>Declaring <code>int arr[5];</code> leaves memory uninitialized. Reading these elements reads whatever residual charges remained in SRAM silicon (garbage values). Using <code>int arr[5]{};</code> or <code>int arr[5] = {0};</code> value-initializes all elements to zero.</p>

        <h3>2. Element Count Idiom</h3>
        <p>In C++11 and earlier, array length was computed via <code>sizeof(arr) / sizeof(arr[0])</code>. In C++17+, <code>std::size(arr)</code> provides a type-safe alternative.</p>
        """,
        "embedded_html": """
        <h3>1. Power-On SRAM Residual State</h3>
        <p>When a microcontroller powers on, SRAM bit cells power up in unpredictable states determined by silicon transistor mismatch. Uninitialized stack variables can cause intermittent, hardware-dependent bugs that disappear during debugging.</p>

        <h3>2. Zero-Cost <code>.bss</code> Initialization</h3>
        <p>Global/static uninitialized arrays are placed in the <code>.bss</code> section, which the C runtime startup code (<code>Reset_Handler</code>) clears to zero before <code>main()</code> is invoked.</p>
        """,
        "refactor_html": """
        <p>Modern C++ guarantees zero-initialization with clean syntax:</p>
        <pre class="code-block" style="background:#0d1117; padding:16px; border-radius:8px; border:1px solid #30363d;">#include &lt;cstdint&gt;
#include &lt;array&gt;

// Guaranteed zero-initialized on the stack (zero garbage RAM)
std::array&lt;uint32_t, 16&gt; telemetry_buffer{};

// Compile-time verified size
constexpr size_t BUFFER_LEN = std::size(telemetry_buffer);</pre>
        """,
        "quiz": [
            {
                "question": "What is stored in an array declared as 'int buffer[10];' on the stack in C++?",
                "options": ["Indeterminate (garbage) values from residual SRAM charges", "All zeros", "All negative ones", "Null pointers"],
                "correct": 0,
                "explanation": "Local stack variables without an explicit initializer are default-initialized, which for fundamental types means their memory retains whatever garbage was previously in that stack location."
            },
            {
                "question": "How does 'int buffer[10]{};' differ from 'int buffer[10];'?",
                "options": ["The empty braces {} guarantee that all 10 elements are zero-initialized", "It allocates memory on the heap", "It makes the array read-only", "It converts the array into a pointer"],
                "correct": 0,
                "explanation": "Value-initialization with <code>{}</code> initializes fundamental numeric types to zero."
            },
            {
                "question": "Which section of microcontroller memory holds global uninitialized variables and is cleared to zero during startup?",
                "options": [".bss section", ".text section", ".rodata section", ".heap section"],
                "correct": 0,
                "explanation": "The <code>.bss</code> section contains uninitialized global and static variables. The startup assembly routine (<code>Reset_Handler</code>) zeroes this region before jumping to <code>main()</code>."
            },
            {
                "question": "What is the benefit of std::size(arr) over sizeof(arr)/sizeof(arr[0]) in C++17?",
                "options": ["std::size will fail to compile if passed a decayed pointer, preventing accidental size bugs", "std::size calculates size in megabytes", "std::size executes faster at runtime", "std::size works with void pointers"],
                "correct": 0,
                "explanation": "<code>std::size()</code> expects a container or fixed array reference. Passing a decayed pointer causes a compilation error rather than silently returning a wrong calculation."
            }
        ]
    },
    {
        "id": "more_array_fun",
        "name": "MoreArrayFun",
        "title": "Range-Based For Loops & Instruction Cache Efficiency",
        "headline": "Modern Range-Based For Loops vs Indexed Iteration in Embedded Assembly",
        "emb_class": "emb-core",
        "emb_badge": "⚡ Embedded Relevance: Core",
        "tags": ["Range-Based For", "Iteration", "Loop Unrolling", "Compiler Optimization"],
        "summary": "Exploring C++11 range-based for loops over arrays. We inspect compiler assembly generation, loop unrolling optimizations (-O3), and eliminating index variable overhead.",
        "files": ["section_4/MoreArrayFun/MoreArrayFun/main.cpp"],
        "concepts_html": """
        <h3>1. Range-Based For Loop Syntax</h3>
        <p>The C++11 range-based for loop (<code>for (auto elem : arr)</code>) simplifies iteration by binding directly to elements, eliminating off-by-one boundary errors (<code>i &lt;= size</code> vs <code>i &lt; size</code>).</p>

        <h3>2. Value vs Const Reference Binding</h3>
        <p>Using <code>for (const auto&amp; x : arr)</code> avoids unnecessary copy construction when elements are larger structs or objects.</p>
        """,
        "embedded_html": """
        <h3>1. Assembly Generation on ARM Cortex-M</h3>
        <p>Compilers translate range-based loops into pointer-increment instructions (<code>LDR.W r3, [r2], #4</code> with post-index addressing), utilizing efficient hardware auto-increment addressing modes.</p>

        <h3>2. Loop Unrolling</h3>
        <p>With <code>-O3</code> optimization, GCC/Clang unrolls fixed-size array loops into straight-line assembly instructions, eliminating branch instruction overhead and pipeline stalls.</p>
        """,
        "refactor_html": """
        <p>Idiomatic modern C++ array processing with auto deduction:</p>
        <pre class="code-block" style="background:#0d1117; padding:16px; border-radius:8px; border:1px solid #30363d;">#include &lt;cstdint&gt;
#include &lt;array&gt;

constexpr std::array&lt;uint8_t, 8&gt; CAN_PAYLOAD = {0x01, 0x02, 0x03, 0x04, 0xAA, 0xBB, 0xCC, 0xDD};

uint16_t computeChecksum() noexcept {
    uint16_t sum = 0;
    for (const uint8_t byte : CAN_PAYLOAD) {
        sum += byte;
    }
    return sum;
}</pre>
        """,
        "quiz": [
            {
                "question": "What is the primary safety benefit of range-based for loops over traditional indexed for loops?",
                "options": ["They completely eliminate off-by-one index boundary errors (out-of-bounds access)", "They run in parallel across multiple CPU cores automatically", "They allocate elements in CPU registers only", "They prevent loops from executing more than 10 times"],
                "correct": 0,
                "explanation": "Range-based for loops operate from <code>begin()</code> to <code>end()</code> automatically, eliminating manual index variables and off-by-one errors."
            },
            {
                "question": "Why should 'const auto& item' be used when iterating over an array of large structures?",
                "options": ["It binds by reference without copying, eliminating CPU cycles spent copying bytes on each iteration", "It converts the struct into an integer", "It moves the struct into Flash ROM", "It allows modifying const variables"],
                "correct": 0,
                "explanation": "Binding by const reference (<code>const auto&amp;</code>) passes the memory address directly, avoiding expensive copy constructor calls for large structs."
            },
            {
                "question": "What does compiler 'loop unrolling' accomplish?",
                "options": ["It duplicates the loop body in assembly, reducing branch instructions and branch misprediction stalls", "It converts loops into recursive functions", "It decreases the total binary Flash size", "It forces the microcontroller to restart"],
                "correct": 0,
                "explanation": "Loop unrolling replicates loop iterations into sequential instructions, trading a small amount of ROM size for faster execution by removing branch instructions."
            },
            {
                "question": "Can a range-based for loop iterate over a dynamically allocated raw pointer array (int* ptr = new int[10])?",
                "options": ["No, because raw pointers do not have compile-time size or begin()/end() iterators", "Yes, it automatically detects the size from heap headers", "Yes, but only in C++20", "Yes, if the pointer is volatile"],
                "correct": 0,
                "explanation": "Range-based for loops require <code>std::begin()</code> and <code>std::end()</code> or fixed array bounds. Raw pointers lack boundary metadata, causing compilation to fail."
            }
        ]
    },
    {
        "id": "twice_numbers",
        "name": "TwiceNumbers",
        "title": "Array Population, In-Place Transformation & SIMD Vectorization",
        "headline": "In-Place Array Mutation, Data Hazards & Microcontroller SIMD Instructions",
        "emb_class": "emb-core",
        "emb_badge": "⚡ Embedded Relevance: Core",
        "tags": ["In-Place Mutation", "SIMD", "ARM DSP", "Data Hazards", "Cache Locality"],
        "summary": "Populating arrays through algorithmic generation and mutating elements in place. We explore ARM Cortex-M4/M7 DSP SIMD instructions (e.g. SADD16, PKHBT) that process multiple array elements in a single clock cycle.",
        "files": ["section_4/TwiceNumbers/TwiceNumbers/main.cpp"],
        "concepts_html": """
        <h3>1. In-Place Transformation</h3>
        <p>In-place mutation updates array elements directly in their existing memory locations (<code>arr[i] *= 2</code>), requiring $O(1)$ auxiliary memory.</p>

        <h3>2. Contiguous Access and Vectorization</h3>
        <p>Sequential memory access allows modern compilers to auto-vectorize loops, generating SIMD (Single Instruction Multiple Data) machine instructions.</p>
        """,
        "embedded_html": """
        <h3>1. ARM Cortex-M4/M7 DSP SIMD Extensions</h3>
        <p>ARM Cortex-M4 and M7 cores include hardware DSP instructions that operate on packed 16-bit or 8-bit integers inside a 32-bit register simultaneously (e.g. two 16-bit multiplications in 1 cycle).</p>

        <h3>2. Memory Alignment for Vector Loads</h3>
        <p>SIMD vector load/store instructions require 4-byte or 8-byte aligned addresses. Unaligned data forces the CPU into slower multiple load cycles.</p>
        """,
        "refactor_html": """
        <p>In-place scaling using modern C++ algorithms:</p>
        <pre class="code-block" style="background:#0d1117; padding:16px; border-radius:8px; border:1px solid #30363d;">#include &lt;cstdint&gt;
#include &lt;array&gt;
#include &lt;algorithm&gt;

template &lt;size_t N&gt;
void doubleValues(std::array&lt;uint32_t, N&gt;&amp; arr) noexcept {
    std::transform(arr.begin(), arr.end(), arr.begin(), [](uint32_t val) {
        return val * 2;
    });
}</pre>
        """,
        "quiz": [
            {
                "question": "What is 'SIMD' in microcontroller CPU architectures?",
                "options": ["Single Instruction Multiple Data: performing the same arithmetic operation on multiple data elements in a single clock cycle", "System Interrupt Memory Dispatcher", "Serial Interface Mode Driver", "Synchronous Instruction Multiplexer"],
                "correct": 0,
                "explanation": "SIMD instructions allow a single CPU instruction to compute operations on multiple packed data values (e.g., two 16-bit integers in one 32-bit register) in parallel."
            },
            {
                "question": "What is the memory complexity of transforming an array in-place?",
                "options": ["O(1) auxiliary memory space", "O(N) memory space", "O(N^2) memory space", "O(log N) memory space"],
                "correct": 0,
                "explanation": "In-place algorithms modify the input array directly without allocating extra buffers, requiring $O(1)$ auxiliary memory."
            },
            {
                "question": "Which ARM Cortex-M processor family first introduced hardware DSP and SIMD instructions?",
                "options": ["ARM Cortex-M4 / Cortex-M7", "ARM Cortex-M0", "ARM Cortex-M0+", "ARM Cortex-M3"],
                "correct": 0,
                "explanation": "The ARM Cortex-M4 and M7 architectures feature dedicated hardware DSP extensions and packed SIMD instructions."
            },
            {
                "question": "Why is sequential array access faster than random array access on cached microcontrollers?",
                "options": ["Sequential access maximizes spatial cache locality, loading full cache lines that satisfy upcoming reads without memory stalls", "Sequential access bypasses the memory bus", "Random access turns off CPU clock gating", "Random access causes the CPU to overheat"],
                "correct": 0,
                "explanation": "CPUs fetch memory in multi-byte cache lines (e.g. 32 bytes). Sequential access hits cached data on consecutive iterations, avoiding high-latency RAM reads."
            }
        ]
    },
    {
        "id": "names_array",
        "name": "NamesArray",
        "title": "String Arrays, Dynamic Heap Overhead & Flash String Pools",
        "headline": "std::string Array Heap Overhead vs string_view Flash String Literals",
        "emb_class": "emb-high",
        "emb_badge": "⚡ Embedded Relevance: High",
        "tags": ["std::string", "std::string_view", "Heap Overhead", "Small String Optimization", ".rodata"],
        "summary": "Comparing arrays of std::string objects with lightweight string_view arrays. We reveal how an array of std::string objects triggers hidden heap allocations and RAM bloat, and demonstrate how to store string tables entirely in Flash ROM.",
        "files": ["section_4/NamesArray/NamesArray/main.cpp"],
        "concepts_html": """
        <h3>1. Memory Layout of <code>std::string</code></h3>
        <p>In standard C++ implementations (like GCC libstdc++), a <code>std::string</code> object occupies <strong>24 to 32 bytes</strong> of stack space even when empty, containing pointer, size, and capacity fields.</p>

        <h3>2. Small String Optimization (SSO)</h3>
        <p>Short strings ($\\le 15$ characters) are stored inside the string object's internal stack buffer. Strings exceeding 15 characters trigger a dynamic heap allocation (<code>malloc</code>).</p>
        """,
        "embedded_html": """
        <h3>1. The RAM Cost of <code>std::string[]</code> in Microcontrollers</h3>
        <p>An array of 10 <code>std::string</code> objects consumes <strong>320 bytes of SRAM</strong> just for object headers, plus extra heap memory for long strings. In a 16KB RAM microcontroller, this wastes significant memory.</p>

        <h3>2. Flash String Pools with <code>std::string_view</code></h3>
        <p>By declaring arrays as <code>constexpr std::string_view[]</code>, string characters and pointers are placed 100% in <strong>Flash ROM (<code>.rodata</code>)</strong> with <strong>0 bytes of SRAM overhead</strong>.</p>
        """,
        "refactor_html": """
        <p>Zero-SRAM Flash string table:</p>
        <pre class="code-block" style="background:#0d1117; padding:16px; border-radius:8px; border:1px solid #30363d;">#include &lt;string_view&gt;
#include &lt;array&gt;

// Stored 100% in Flash ROM (.rodata); Zero SRAM consumed
static constexpr std::array&lt;std::string_view, 4&gt; DEVICE_NAMES = {
    "Telemetry_Sensor",
    "Imu_Accelerometer",
    "Gps_Receiver",
    "Can_Transceiver"
};</pre>
        """,
        "quiz": [
            {
                "question": "What is 'Small String Optimization' (SSO) in std::string?",
                "options": ["An optimization where short strings (typically <= 15 chars) are stored directly inside the string's stack buffer without heap allocation", "A compression algorithm that reduces ASCII text size by 50%", "A feature that converts all strings to uppercase", "An optimization that places strings in CPU registers"],
                "correct": 0,
                "explanation": "SSO uses the internal pointer/capacity member space to store small string payloads directly on the stack, avoiding heap allocation."
            },
            {
                "question": "How much SRAM does 'static constexpr std::string_view names[]' consume when placed in Flash memory?",
                "options": ["0 bytes of SRAM (it resides completely in Flash ROM .rodata)", "320 bytes of SRAM", "1024 bytes of SRAM", "4 bytes per character in SRAM"],
                "correct": 0,
                "explanation": "<code>static constexpr</code> tables are placed by the linker into the read-only data section in Flash ROM, allocating 0 bytes in SRAM."
            },
            {
                "question": "What is the size of a std::string_view object on a 32-bit architecture?",
                "options": ["8 bytes (4-byte pointer + 4-byte length)", "32 bytes", "1 byte", "Variable size based on text length"],
                "correct": 0,
                "explanation": "<code>std::string_view</code> consists of exactly one pointer to the character buffer (4 bytes) and one size integer (4 bytes), totaling 8 bytes."
            },
            {
                "question": "Why can using std::string in deeply nested microcontroller functions cause stack overflow?",
                "options": ["Each std::string instance consumes 24-32 bytes of stack frame space, quickly exhausting small 1KB-2KB microcontroller stacks", "std::string disables the CPU stack pointer", "std::string forces memory alignment to 4KB", "std::string executes in interrupt mode"],
                "correct": 0,
                "explanation": "Because <code>sizeof(std::string)</code> is 24-32 bytes, creating multiple strings inside recursive or deeply nested function calls rapidly exhausts small microcontroller stack spaces."
            }
        ]
    },
    {
        "id": "temperature_converter",
        "name": "TemperatureConverter",
        "title": "Floating-Point Arrays vs Fixed-Point Arithmetic (Q-Format)",
        "headline": "Float vs Double Array Footprint & Q15/Q31 Fixed-Point Math on Hardware without FPU",
        "emb_class": "emb-high",
        "emb_badge": "⚡ Embedded Relevance: High",
        "tags": ["Floating Point", "FPU", "Fixed-Point Math", "Q15 Format", "ARM Cortex-M0"],
        "summary": "Converting temperature sensor readings stored in arrays. We explore the memory difference between float (32-bit IEEE 754) and double (64-bit), and show how to implement fixed-point arithmetic (Q-format) for microcontrollers without a hardware Floating Point Unit (FPU).",
        "files": ["section_4/TemperatureConverter/TemperatureConverter/main.cpp"],
        "concepts_html": """
        <h3>1. IEEE 754 Floating-Point Sizing</h3>
        <ul>
          <li><code>float</code>: 32 bits (1 sign bit, 8 exponent bits, 23 mantissa bits) $\\approx 7$ decimal digits precision.</li>
          <li><code>double</code>: 64 bits (1 sign bit, 11 exponent bits, 52 mantissa bits) $\\approx 15-17$ decimal digits precision.</li>
        </ul>

        <h3>2. Float Literal Suffix</h3>
        <p>In C++, floating literals without a suffix (e.g. <code>32.0</code>) default to <code>double</code>. Writing <code>32.0f</code> ensures single-precision operations.</p>
        """,
        "embedded_html": """
        <h3>1. Software Emulation vs Hardware FPU</h3>
        <p>Microcontrollers like ARM Cortex-M0, M0+, and M3 lack a hardware FPU. Floating-point operations pull in <strong>software emulation library routines (<code>__aeabi_fadd</code>, <code>__aeabi_fmul</code>)</strong>, adding 4KB-10KB of Flash bloat and taking <strong>20-100 clock cycles per operation</strong>.</p>

        <h3>2. Q-Format Fixed-Point Arithmetic</h3>
        <p>Fixed-point representation uses standard integer registers to represent fractions with deterministic, single-cycle integer instructions.</p>
        """,
        "refactor_html": """
        <p>Q8.8 Fixed-Point Temperature Representation (Single-Cycle Arithmetic):</p>
        <pre class="code-block" style="background:#0d1117; padding:16px; border-radius:8px; border:1px solid #30363d;">#include &lt;cstdint&gt;

// Fixed-Point Q8.8 (16-bit integer: 8 bits integer, 8 bits fraction)
struct FixedQ8_8 {
    int16_t raw;

    static constexpr FixedQ8_8 from_float(float val) noexcept {
        return FixedQ8_8{static_cast&lt;int16_t&gt;(val * 256.0f)};
    }

    constexpr int16_t to_celsius_int() const noexcept {
        return raw &gt;&gt; 8; // Fast single-cycle bit shift
    }
};

// Celsius to Fahrenheit in Q8.8 fixed-point: (C * 9/5) + 32
constexpr FixedQ8_8 celsiusToFahrenheit(FixedQ8_8 c) noexcept {
    int32_t intermediate = (static_cast&lt;int32_t&gt;(c.raw) * 9) / 5;
    return FixedQ8_8{static_cast&lt;int16_t&gt;(intermediate + (32 &lt;&lt; 8))};
}</pre>
        """,
        "quiz": [
            {
                "question": "What happens when floating-point math is executed on a microcontroller without a hardware FPU (e.g. Cortex-M0)?",
                "options": ["The compiler links software emulation library routines, increasing code size and taking dozens of clock cycles per operation", "A hardware HardFault occurs immediately", "The CPU automatically upgrades to 64-bit mode", "Floating point operations are rounded to zero instantly"],
                "correct": 0,
                "explanation": "Without an FPU, floating-point operations are emulated in software via math routines, consuming extra Flash space and hundreds of clock cycles."
            },
            {
                "question": "Why is 'float x = 5.0;' suboptimal on a 32-bit MCU with single-precision FPU?",
                "options": ["5.0 is a double literal, causing the compiler to perform double-precision promotion before converting back to float", "5.0 is interpreted as an integer", "It causes a memory leak on the heap", "It disables the compiler optimizer"],
                "correct": 0,
                "explanation": "Unadorned floating literals default to <code>double</code> (64-bit). On MCUs with only a single-precision (32-bit) FPU, this invokes slow software double-precision emulation."
            },
            {
                "question": "What does Q8.8 fixed-point format represent?",
                "options": ["A 16-bit integer where the upper 8 bits represent the integer part and the lower 8 bits represent the fractional part", "An 8-bit float with 8 exponent bits", "A quaternion rotation matrix", "An encrypted 8-byte buffer"],
                "correct": 0,
                "explanation": "Q8.8 uses an integer variable where the radix point is fixed: 8 bits for integer magnitude and 8 bits for fractional precision ($1/256$ resolution)."
            },
            {
                "question": "How fast is a fixed-point division by 256 compared to floating-point division on a Cortex-M0?",
                "options": ["Fixed point uses a single-cycle arithmetic right-shift (ASR #8), executing 20x-50x faster than software float division", "Both take exactly 1 clock cycle", "Floating point division is faster", "Fixed point cannot perform division"],
                "correct": 0,
                "explanation": "Dividing by $2^8 = 256$ in fixed-point is a single-cycle bit shift (<code>ASR #8</code>), whereas software float division takes dozens of cycles."
            }
        ]
    },
    {
        "id": "2d_array_fun",
        "name": "2DArrayFun",
        "title": "2D Arrays, Row-Major Layout & DMA Burst Transfers",
        "headline": "Row-Major Memory Contiguity, Nested Loops & Direct Memory Access (DMA)",
        "emb_class": "emb-high",
        "emb_badge": "⚡ Embedded Relevance: Critical",
        "tags": ["2D Arrays", "Row-Major", "DMA Transfers", "Stride", "Display Buffers"],
        "summary": "Deep dive into two-dimensional arrays in C++. We examine row-major contiguous memory layouts, why row-first iteration maximizes CPU cache hits, and how hardware Direct Memory Access (DMA) controllers stream 2D display and sensor buffers without CPU intervention.",
        "files": ["section_4/2DArrayFun/2DArrayFun/main.cpp"],
        "concepts_html": """
        <h3>1. Row-Major Contiguous Memory Layout</h3>
        <p>In C and C++, multidimensional arrays are laid out in <strong>row-major order</strong>: the second index changes fastest. In memory, <code>grid[2][3]</code> is stored as a single contiguous 1D block of 6 elements.</p>

        <h3>2. Address Calculation Formula</h3>
        <p>The memory address of element <code>grid[row][col]</code> is calculated as:</p>
        <p>$$\\text{Address} = \\text{Base} + ((\\text{row} \\times \\text{COLS}) + \\text{col}) \\times \\text{sizeof}(T)$$</p>
        """,
        "embedded_html": """
        <h3>1. Cache Line Thrashing from Column-Major Access</h3>
        <p>Iterating column-first (<code>grid[col][row]</code>) strides through memory by <code>COLS * sizeof(T)</code> bytes on every step. This causes a <strong>cache miss on every single access</strong>. Always iterate row-first!</p>

        <h3>2. Direct Memory Access (DMA) Framebuffers</h3>
        <p>Because 2D arrays are contiguous in SRAM, a microcontroller DMA controller (e.g. STM32 DMA2D / Chrom-ART) can stream full display frames directly from SRAM to an SPI/I2C TFT display with <strong>0% CPU utilization</strong>.</p>
        """,
        "refactor_html": """
        <p>Type-safe flat 2D display framebuffer wrapper with DMA compatibility:</p>
        <pre class="code-block" style="background:#0d1117; padding:16px; border-radius:8px; border:1px solid #30363d;">#include &lt;cstdint&gt;
#include &lt;array&gt;

template &lt;size_t Rows, size_t Cols&gt;
class Framebuffer2D {
private:
    // Contiguous in memory; 100% DMA transfer compatible
    std::array&lt;uint16_t, Rows * Cols&gt; pixels_{};

public:
    constexpr void set_pixel(size_t r, size_t c, uint16_t rgb565) noexcept {
        if (r &lt; Rows &amp;&amp; c &lt; Cols) {
            pixels_[r * Cols + c] = rgb565;
        }
    }

    const uint16_t* dma_buffer() const noexcept { return pixels_.data(); }
    constexpr size_t byte_size() const noexcept { return pixels_.size() * sizeof(uint16_t); }
};</pre>
        """,
        "quiz": [
            {
                "question": "How are 2D arrays organized in C and C++ memory?",
                "options": ["Row-Major order: elements of the first row are stored contiguously, followed by elements of the second row", "Column-Major order: columns are stored sequentially", "Fragmented linked blocks across the heap", "Randomly distributed by the linker"],
                "correct": 0,
                "explanation": "C and C++ use row-major ordering where consecutive elements of a row occupy adjacent memory addresses."
            },
            {
                "question": "Why does column-major iteration over a large 2D array degrade CPU performance?",
                "options": ["It accesses memory with large address strides, causing frequent CPU data cache misses and memory stalls", "It triggers compiler syntax errors", "It forces the array to reallocate on the heap", "It changes the values of adjacent elements"],
                "correct": 0,
                "explanation": "Striding across rows skips memory lines, causing cache misses on every access rather than reusing loaded cache lines."
            },
            {
                "question": "What is the primary role of a Direct Memory Access (DMA) controller when managing 2D graphics buffers?",
                "options": ["It transfers pixel data from SRAM to peripheral hardware (e.g. SPI display) in the background without CPU intervention", "It compiles graphics shaders at runtime", "It formats the SD card file system", "It increases the microcontroller crystal clock speed"],
                "correct": 0,
                "explanation": "DMA controllers transfer memory blocks directly between SRAM and peripheral hardware asynchronously, freeing the CPU to execute application logic."
            },
            {
                "question": "For an array int grid[4][8] on a 32-bit MCU, what is the byte offset of grid[2][3] from the array base address?",
                "options": ["76 bytes ( (2 * 8 + 3) * 4 bytes )", "19 bytes", "48 bytes", "96 bytes"],
                "correct": 0,
                "explanation": "Linear index $= (2 \\times 8) + 3 = 19$. Byte offset $= 19 \\times 4\\text{ bytes} = 76\\text{ bytes}$."
            }
        ]
    },
    {
        "id": "move_ratings",
        "name": "MoveRatings",
        "title": "Nested Array Iteration, Matrix Math & Boundary Invariants",
        "headline": "Matrix Transformation, Cache Warmth & Memory Strides in Embedded DSP",
        "emb_class": "emb-core",
        "emb_badge": "⚡ Embedded Relevance: Core",
        "tags": ["Matrix Math", "Nested Loops", "Cache Lines", "DSP", "Bounds Safety"],
        "summary": "Manipulating 2D data grids with nested loops. We explore matrix processing patterns, row vs column accumulation, and memory alignment rules for high-speed embedded DSP filters.",
        "files": ["section_4/MoveRatings/MoveRatings/main.cpp"],
        "concepts_html": """
        <h3>1. Nested Loop Iteration Order</h3>
        <p>Nested loops iterating over 2D data structures must match the memory layout: outer loop for rows, inner loop for columns.</p>

        <h3>2. Aggregation & Accumulation</h3>
        <p>Computing row/column averages requires accumulator registers. Using fixed-width integer accumulators prevents overflow bugs.</p>
        """,
        "embedded_html": """
        <h3>1. Cache Warmth & Burst Transfers</h3>
        <p>In DSP systems, reading contiguous array elements triggers hardware burst read cycles on external SDRAM/Quad-SPI Flash, doubling memory throughput compared to single random reads.</p>
        """,
        "refactor_html": """
        <p>Cache-friendly matrix row accumulator:</p>
        <pre class="code-block" style="background:#0d1117; padding:16px; border-radius:8px; border:1px solid #30363d;">#include &lt;cstdint&gt;
#include &lt;array&gt;

template &lt;size_t Rows, size_t Cols&gt;
void computeRowSums(const std::array&lt;std::array&lt;uint16_t, Cols&gt;, Rows&gt;&amp; matrix,
                    std::array&lt;uint32_t, Rows&gt;&amp; out_sums) noexcept {
    for (size_t r = 0; r &lt; Rows; ++r) {
        uint32_t sum = 0;
        for (size_t c = 0; c &lt; Cols; ++c) {
            sum += matrix[r][c]; // Optimal sequential memory access
        }
        out_sums[r] = sum;
    }
}</pre>
        """,
        "quiz": [
            {
                "question": "Which loop nesting order provides the highest memory throughput when iterating over a 2D array grid[ROWS][COLS]?",
                "options": ["Outer loop: rows (0 to ROWS-1), Inner loop: columns (0 to COLS-1)", "Outer loop: columns (0 to COLS-1), Inner loop: rows (0 to ROWS-1)", "Diagonal iteration", "Random index iteration"],
                "correct": 0,
                "explanation": "Iterating rows in the outer loop and columns in the inner loop traverses memory sequentially, maximizing CPU cache line hits."
            },
            {
                "question": "Why should a 32-bit integer accumulator (uint32_t) be used when summing an array of 16-bit integers (uint16_t)?",
                "options": ["To prevent integer arithmetic overflow when the cumulative sum exceeds 65,535", "Because 16-bit integers cannot be added in C++", "To force the compiler to use double precision", "To reduce RAM consumption"],
                "correct": 0,
                "explanation": "Summing multiple 16-bit values (max 65,535) can easily overflow a 16-bit variable. A 32-bit accumulator safely accommodates sums up to 4,294,967,295."
            },
            {
                "question": "What is a memory 'burst read' in microcontroller external memory interfaces (FMC / FSMC)?",
                "options": ["A hardware transaction where a continuous stream of consecutive data words is transferred following a single address setup", "An intentional hardware short-circuit", "A memory wipe cycle", "An interrupt storm"],
                "correct": 0,
                "explanation": "Burst transfers send a starting address and read multiple sequential words over consecutive clock cycles, dramatically increasing bus bandwidth."
            },
            {
                "question": "What happens if loop termination conditions read beyond the row bound of a 2D stack array?",
                "options": ["The loop reads into adjacent stack frames or local variables, producing corrupted data or HardFault crashes", "The compiler wraps the index to 0 safely", "The array automatically resizes", "The program pauses for 10ms"],
                "correct": 0,
                "explanation": "C++ does not perform automatic bounds checks; overflowing 2D array bounds reads adjacent memory addresses on the stack."
            }
        ]
    },
    {
        "id": "vector_fun",
        "name": "VectorFun",
        "title": "std::vector Dynamic Growth & Heap Reallocation Penalties",
        "headline": "Capacity vs Size, Geometric Growth Reallocation & Real-Time Heap Hazards",
        "emb_class": "emb-high",
        "emb_badge": "⚡ Embedded Relevance: Critical",
        "tags": ["std::vector", "push_back", "Capacity vs Size", "Heap Reallocation", "Real-Time Jitter"],
        "summary": "Exploring dynamic arrays via std::vector. We analyze capacity vs size, geometric heap reallocation mechanics, pointer invalidation risks during push_back(), and why dynamic vectors are replaced by static bounded vectors in real-time firmware.",
        "files": ["section_4/VectorFun/VectorFun/main.cpp"],
        "concepts_html": """
        <h3>1. Size vs Capacity</h3>
        <ul>
          <li><strong>Size:</strong> The number of active elements currently in the vector (<code>.size()</code>).</li>
          <li><strong>Capacity:</strong> The total number of elements allocated in heap memory before reallocation is needed (<code>.capacity()</code>).</li>
        </ul>

        <h3>2. Geometric Growth & Iterator Invalidation</h3>
        <p>When <code>push_back()</code> exceeds current capacity, <code>std::vector</code> allocates a new heap buffer (typically $1.5\\times$ or $2\\times$ larger), copies/moves all existing elements, and frees the old buffer. <strong>All existing pointers and iterators to elements are invalidated!</strong></p>
        """,
        "embedded_html": """
        <h3>1. Real-Time Latency Spikes during Vector Growth</h3>
        <p>A <code>push_back()</code> is usually $O(1)$ amortized, but when reallocation occurs, it spikes to $O(N)$ with dynamic heap allocation latency, causing missed real-time deadlines in motor control or audio processing loops.</p>

        <h3>2. Memory Fragmentation</h3>
        <p>Repeated vector expansion allocates and frees progressively larger blocks, causing severe heap fragmentation on constrained SRAM microcontrollers.</p>
        """,
        "refactor_html": """
        <p>Pre-reserving capacity or using fixed-capacity bounded vectors:</p>
        <pre class="code-block" style="background:#0d1117; padding:16px; border-radius:8px; border:1px solid #30363d;">#include &lt;vector&gt;

// If std::vector MUST be used, reserve capacity upfront at boot
std::vector&lt;int&gt; createTelemetryVector(size_t expected_items) {
    std::vector&lt;int&gt; vec;
    vec.reserve(expected_items); // Allocates ONCE; eliminates dynamic reallocations
    return vec;
}</pre>
        """,
        "quiz": [
            {
                "question": "What occurs internally when push_back() is called on a std::vector whose size() equals its capacity()?",
                "options": ["A new larger heap buffer is allocated, all existing elements are copied/moved, the old buffer is deleted, and existing pointers/iterators are invalidated", "The newest element is silently dropped", "The vector throws a std::out_of_range exception", "The microcontroller restarts"],
                "correct": 0,
                "explanation": "When capacity is exhausted, <code>std::vector</code> reallocates a larger memory block on the heap, moves existing elements, and frees the old block, invalidating all existing references/iterators."
            },
            {
                "question": "What is the time complexity of vector::push_back() when a reallocation is triggered?",
                "options": ["O(N) linear time (proportional to element count)", "O(1) constant time", "O(log N) logarithmic time", "O(1/N) inverse time"],
                "correct": 0,
                "explanation": "Reallocation requires allocating new memory and copying/moving all $N$ existing elements, taking $O(N)$ time."
            },
            {
                "question": "How does vector::reserve(N) protect embedded applications from reallocation jitter?",
                "options": ["It pre-allocates heap memory for N elements upfront, guaranteeing zero reallocations for insertions up to size N", "It limits the vector to N bytes in ROM", "It converts the vector to a stack array", "It enables multithreading synchronization"],
                "correct": 0,
                "explanation": "<code>reserve()</code> allocates the requested capacity in a single initial allocation, ensuring subsequent <code>push_back()</code> operations run in deterministic $O(1)$ time without reallocation."
            },
            {
                "question": "Why is storing raw pointers to std::vector elements dangerous?",
                "options": ["Any subsequent push_back() that triggers a reallocation will invalidate the pointer, creating a hazardous dangling pointer", "Vectors encrypt pointer addresses", "Pointers cannot address heap memory", "Vectors delete elements after 1 second"],
                "correct": 0,
                "explanation": "If a vector reallocates its internal buffer, existing elements move to a new memory address, leaving stored pointers pointing to freed memory (use-after-free bug)."
            }
        ]
    },
    {
        "id": "vector_practice",
        "name": "VectorPractice",
        "title": "Vector Modifiers (pop_back, insert) & Embedded Alternatives",
        "headline": "pop_back(), insert() Cost & Zero-Heap Embedded Template Library (ETL) Containers",
        "emb_class": "emb-core",
        "emb_badge": "⚡ Embedded Relevance: Core",
        "tags": ["pop_back()", "insert()", "ETL", "Zero-Heap", "Deterministic Timing"],
        "summary": "Practicing vector modification operations: push_back, pop_back, and insert. We examine the O(N) element shifting cost of mid-vector insertions and demonstrate how the Embedded Template Library (ETL) delivers STL-like containers with zero heap allocations.",
        "files": ["section_4/VectorPractice/VectorPractice/main.cpp"],
        "concepts_html": """
        <h3>1. <code>pop_back()</code> vs <code>insert()</code> Complexity</h3>
        <ul>
          <li><code>pop_back()</code>: Destroys the last element in $O(1)$ constant time without shrinking capacity.</li>
          <li><code>insert(pos, val)</code>: Shifts all trailing elements one position to the right ($O(N)$ time complexity).</li>
        </ul>
        """,
        "embedded_html": """
        <h3>1. The Embedded Template Library (ETL)</h3>
        <p>The <strong>Embedded Template Library (ETL)</strong> is an open-source C++ library specifically designed for microcontrollers. It mirrors C++ STL containers (<code>etl::vector</code>, <code>etl::list</code>, <code>etl::queue</code>) but uses <strong>statically allocated internal storage</strong>, completely eliminating dynamic heap allocations.</p>
        """,
        "refactor_html": """
        <p>Deterministic ETL fixed-capacity vector usage:</p>
        <pre class="code-block" style="background:#0d1117; padding:16px; border-radius:8px; border:1px solid #30363d;">#include &lt;cstdint&gt;
// Conceptually equivalent to etl::vector&lt;uint32_t, 10&gt;
template &lt;typename T, size_t MAX_SIZE&gt;
class EtlVectorDemo {
    T storage_[MAX_SIZE];
    size_t current_size_{0};

public:
    bool push_back(const T&amp; item) noexcept {
        if (current_size_ &gt;= MAX_SIZE) return false;
        storage_[current_size_++] = item;
        return true;
    }

    void pop_back() noexcept {
        if (current_size_ &gt; 0) --current_size_;
    }

    size_t size() const noexcept { return current_size_; }
};</pre>
        """,
        "quiz": [
            {
                "question": "What is the time complexity of inserting an element at the beginning of a std::vector?",
                "options": ["O(N) linear time because all existing elements must be shifted one slot to the right", "O(1) constant time", "O(log N) logarithmic time", "O(N^2) quadratic time"],
                "correct": 0,
                "explanation": "Inserting at index 0 requires moving every existing element one index forward in memory to make room, taking $O(N)$ operations."
            },
            {
                "question": "Does calling vector::pop_back() reduce the vector's heap memory capacity?",
                "options": ["No, pop_back() decrements size and destroys the element, but capacity remains unchanged", "Yes, it frees memory immediately", "Yes, it reallocates a smaller buffer", "It deletes all elements"],
                "correct": 0,
                "explanation": "<code>pop_back()</code> only reduces <code>size()</code>; the allocated memory <code>capacity()</code> remains intact to avoid reallocation overhead on future insertions."
            },
            {
                "question": "Why is the Embedded Template Library (ETL) widely adopted in automotive and medical device firmware?",
                "options": ["It provides STL-like containers that allocate all storage statically inside the object, guaranteeing zero heap fragmentation and deterministic execution", "It automatically generates microcontroller PCB layouts", "It replaces the C++ compiler", "It requires no CPU clock"],
                "correct": 0,
                "explanation": "ETL provides standard container interfaces with fixed-capacity stack/static storage, meeting MISRA and safety-critical deterministic memory requirements."
            },
            {
                "question": "Which method removes all elements from a vector while preserving its allocated capacity?",
                "options": [".clear()", ".shrink_to_fit()", ".pop_back()", ".erase()"],
                "correct": 0,
                "explanation": "<code>vec.clear()</code> resets the size to 0 and invokes destructors for all elements, but retains the allocated capacity buffer."
            }
        ]
    },
    {
        "id": "shopping_list",
        "name": "ShoppingList",
        "title": "Interactive Vector Modification & Real-Time Queuing",
        "headline": "Dynamic Item Insertion, String Vectors & Circular Buffers for Real-Time Streaming",
        "emb_class": "emb-core",
        "emb_badge": "⚡ Embedded Relevance: Core",
        "tags": ["Vector Modification", "FIFO Queue", "Circular Buffer", "Dynamic Collections"],
        "summary": "Building dynamic list management with interactive user input. We contrast general-purpose dynamic list manipulation with embedded FIFO circular queues used for sensor message streams and serial packet buffering.",
        "files": ["section_4/ShoppingList/ShoppingList/main.cpp"],
        "concepts_html": """
        <h3>1. Dynamic Collection Growth</h3>
        <p>Interactive applications collect unpredictable numbers of items from user input, making resizable containers like <code>std::vector</code> standard in hosted environments.</p>

        <h3>2. String Serialization</h3>
        <p>Managing collections of text requires handling string copying, delimiters, and terminal character outputs.</p>
        """,
        "embedded_html": """
        <h3>1. Circular FIFO Ring Buffers vs Vectors</h3>
        <p>In streaming embedded applications (e.g. UART serial input, CAN bus message queues), fixed-size <strong>Circular Ring Buffers</strong> are used instead of vectors. Elements are pushed and popped in $O(1)$ time with zero heap allocation.</p>
        """,
        "refactor_html": """
        <p>Embedded ring buffer for streaming data:</p>
        <pre class="code-block" style="background:#0d1117; padding:16px; border-radius:8px; border:1px solid #30363d;">#include &lt;cstdint&gt;
#include &lt;array&gt;

template &lt;typename T, size_t Capacity&gt;
class RingBuffer {
    static_assert((Capacity &amp; (Capacity - 1)) == 0, "Capacity must be power of 2");
    std::array&lt;T, Capacity&gt; buffer_{};
    uint32_t head_{0};
    uint32_t tail_{0};

public:
    bool push(T item) noexcept {
        uint32_t next = (head_ + 1) &amp; (Capacity - 1);
        if (next == tail_) return false; // Full
        buffer_[head_] = item;
        head_ = next;
        return true;
    }

    bool pop(T&amp; out) noexcept {
        if (head_ == tail_) return false; // Empty
        out = buffer_[tail_];
        tail_ = (tail_ + 1) &amp; (Capacity - 1);
        return true;
    }
};</pre>
        """,
        "quiz": [
            {
                "question": "Why are Circular Ring Buffers preferred over std::vector for UART serial receive buffers?",
                "options": ["Ring buffers provide deterministic O(1) push/pop operations with fixed static memory and zero dynamic allocation", "Ring buffers automatically translate baud rates", "Ring buffers compress ASCII characters", "Ring buffers use double precision floats"],
                "correct": 0,
                "explanation": "Ring buffers use a fixed array with wrap-around head and tail indices, operating in $O(1)$ deterministic time without allocating memory."
            },
            {
                "question": "Why is the capacity of high-speed ring buffers often constrained to powers of two (e.g. 64, 128, 256)?",
                "options": ["It allows replacing expensive modulo division (%) with a single-cycle bitwise AND (& (Capacity - 1))", "Microcontrollers can only count in powers of two", "It prevents memory from overheating", "It disables the floating point unit"],
                "correct": 0,
                "explanation": "When $N$ is a power of 2, index wrap-around <code>idx % N</code> can be computed via <code>idx & (N - 1)</code>, which executes in a single clock cycle on all CPUs."
            },
            {
                "question": "What happens in a circular ring buffer when head == tail?",
                "options": ["The buffer is completely empty", "The buffer is 100% full", "A hardware fault is triggered", "The memory is cleared to zero"],
                "correct": 0,
                "explanation": "When the write index (head) matches the read index (tail), no unread elements remain, indicating an empty buffer."
            },
            {
                "question": "What happens if an interrupt routine pushes data to a full ring buffer without checking available space?",
                "options": ["A buffer overflow occurs, overwriting unread historical data", "The CPU freezes permanently", "The compiler throws an exception", "The data is cached on disk"],
                "correct": 0,
                "explanation": "Failing to check if the buffer is full causes the head to overwrite unread elements at the tail, corrupting the data stream."
            }
        ]
    }
]
