#!/usr/bin/env python3
"""
Section 2 Project Definitions: Data Types, Variables & Arithmetic Mechanics
Contains 14 comprehensive project definitions covering fixed-width integers (<cstdint>),
integer promotion, signed overflow UB, floating-point representations, and bitwise operations.
"""

SECTION_2_PROJECTS = [
    {
        "id": "hello_world",
        "name": "HelloWorld",
        "title": "Standard Streams vs Microcontroller Semihosting & ITM",
        "headline": "std::cout I/O Overhead vs Microcontroller UART & ARM Cortex-M ITM Trace",
        "emb_class": "emb-high",
        "emb_badge": "⚡ Embedded Relevance: High",
        "tags": ["std::cout", "UART", "Semihosting", "ITM Trace", "SWO Console"],
        "summary": "Exploring console output via std::cout and std::endl. We analyze why C++ iostreams introduce 20KB-50KB of binary Flash bloat in microcontroller firmware, how std::endl causes unintended buffer flushes, and contrast semihosting traps with zero-overhead hardware ITM/SWO instrumentation tracing.",
        "files": ["section_2/HelloWorld/HelloWorld/main.cpp"],
        "concepts_html": """
        <h3>1. Standard Output Streams (<code>std::cout</code>)</h3>
        <p><code>std::cout</code> is an instance of <code>std::ostream</code> that buffers characters before flushing to standard output.</p>

        <h3>2. <code>std::endl</code> vs <code>'\\n'</code></h3>
        <p><code>std::endl</code> writes a newline character <strong>AND forces an explicit buffer flush</strong> (<code>stream.flush()</code>). In high-frequency logging loops, this ruins I/O performance. Using <code>'\\n'</code> avoids unnecessary flushing.</p>
        """,
        "embedded_html": """
        <h3>1. The Flash ROM Bloat of <code>&lt;iostream&gt;</code></h3>
        <p>Including <code>&lt;iostream&gt;</code> pulls in heavy locale formatting machinery, dynamic stream buffers, and static initializers, instantly consuming <strong>20KB to 50KB of Flash ROM</strong>—often exceeding total available ROM on small microcontrollers!</p>

        <h3>2. Instrumentation Trace Macrocell (ITM / SWO)</h3>
        <p>ARM Cortex-M3/M4/M7 cores feature a dedicated hardware <strong>ITM (Instrumentation Trace Macrocell)</strong> peripheral. Writing a byte to <code>ITM-&gt;PORT[0]</code> outputs debug characters over the 1-pin Serial Wire Output (SWO) at 2+ MBaud with <strong>zero CPU latency</strong> and 0 Flash bloat.</p>
        """,
        "refactor_html": """
        <p>Zero-overhead hardware ITM debug logging:</p>
        <pre class="code-block" style="background:#0d1117; padding:16px; border-radius:8px; border:1px solid #30363d;">#include &lt;cstdint&gt;

// Hardware ITM Stimulus Port 0 write (0 ROM bloat!)
void itm_putc(char ch) noexcept {
    volatile uint32_t* const ITM_STIM0 = reinterpret_cast&lt;volatile uint32_t*&gt;(0xE0000000);
    volatile uint32_t* const ITM_TER   = reinterpret_cast&lt;volatile uint32_t*&gt;(0xE0000E00);
    
    if (*ITM_TER &amp; 1UL) { // If ITM Port 0 is enabled by debugger
        while (*ITM_STIM0 == 0); // Wait until FIFO ready
        *reinterpret_cast&lt;volatile uint8_t*&gt;(ITM_STIM0) = static_cast&lt;uint8_t&gt;(ch);
    }
}</pre>
        """,
        "quiz": [
            {
                "question": "Why is '<iostream>' (std::cout) frequently avoided in resource-constrained microcontroller firmware?",
                "options": ["It links heavy formatting machinery, dynamic stream buffers, and locales, adding 20KB-50KB of Flash ROM bloat", "Microcontrollers do not support character data", "std::cout causes immediate memory corruption", "std::cout requires an internet connection"],
                "correct": 0,
                "explanation": "<code>&lt;iostream&gt;</code> includes extensive formatting and locale infrastructure that inflates the final binary footprint."
            },
            {
                "question": "How does 'std::endl' differ from the newline character '\\n'?",
                "options": ["std::endl writes '\\n' AND forces an explicit stream flush, degrading throughput in high-frequency loops", "std::endl outputs two newlines", "std::endl works only on Windows", "std::endl allocates memory on the heap"],
                "correct": 0,
                "explanation": "<code>std::endl</code> writes <code>'\\n'</code> and calls <code>flush()</code>, which flushes underlying I/O buffers immediately and incurs heavy latency."
            },
            {
                "question": "What is ARM Cortex-M 'Instrumentation Trace Macrocell' (ITM) SWO logging?",
                "options": ["A dedicated hardware debug peripheral that streams printf/trace characters over the 1-pin SWO debug line without halting the CPU", "A software UART emulator", "A compiler optimization", "An SPI display driver"],
                "correct": 0,
                "explanation": "ITM streams trace packets over the dedicated Serial Wire Output (SWO) pin via hardware FIFO with negligible CPU instruction overhead."
            },
            {
                "question": "What is the danger of ARM 'Semihosting' printf in battery-powered or standalone devices?",
                "options": ["The BKPT #0xAB instruction halts CPU execution until a host JTAG debugger acknowledges the call; without a debugger connected, the MCU hangs forever", "It causes flash memory to erase", "It overclocks the CPU", "It disables all interrupts permanently"],
                "correct": 0,
                "explanation": "Semihosting executes software breakpoint traps (<code>BKPT 0xAB</code>) expecting a debugger. In standalone deployment, this triggers unhandled breakpoint faults."
            }
        ]
    },
    {
        "id": "comment_fun",
        "name": "CommentFun",
        "title": "Code Documentation, Doxygen & Self-Documenting Firmware",
        "headline": "C/C++ Comment Syntax, Doxygen Tags (@brief, @param) & Self-Documenting Code",
        "emb_class": "emb-core",
        "emb_badge": "⚡ Embedded Relevance: Core",
        "tags": ["Comments", "Doxygen", "Documentation", "MISRA", "Clean Code"],
        "summary": "Exploring single-line (//) and multi-line (/* */) comments. We analyze Doxygen documentation tag standards for embedded APIs (@brief, @param, @return), comment nesting syntax errors, and MISRA C++ guidelines for maintaining clean, self-documenting firmware.",
        "files": ["section_2/CommentFun/CommentFun/main.cpp"],
        "concepts_html": """
        <h3>1. Comment Syntax in C++</h3>
        <ul>
          <li><code>//</code>: Single-line comment (continues until the end of the line).</li>
          <li><code>/* ... */</code>: Multi-line block comment. <strong>Block comments cannot be nested!</strong></li>
        </ul>

        <h3>2. Doxygen Markup Standards</h3>
        <p>Embedded hardware drivers use structured Doxygen tags to auto-generate PDF and HTML documentation for hardware registers and HAL APIs.</p>
        """,
        "embedded_html": """
        <h3>1. MISRA C++:2008 Rule 2-7-1</h3>
        <p>The character sequence <code>/*</code> shall not appear within comments, and code shall not be commented out using block comments (conditional compilation <code>#if 0 ... #endif</code> must be used instead).</p>
        """,
        "refactor_html": """
        <p>Production Doxygen driver header documentation:</p>
        <pre class="code-block" style="background:#0d1117; padding:16px; border-radius:8px; border:1px solid #30363d;">/**
 * @brief  Transmits a single data byte over the SPI1 hardware bus.
 * @param  payload: The 8-bit unsigned byte to transmit.
 * @param  timeout_ms: Maximum duration in milliseconds to wait for TXE flag.
 * @retval 0 on success, -1 on timeout or bus fault error.
 * @note   This function is reentrant and thread-safe.
 */
[[nodiscard]] int32_t spi_transmit_byte(uint8_t payload, uint32_t timeout_ms) noexcept;</pre>
        """,
        "quiz": [
            {
                "question": "What happens if you attempt to nest block comments: /* outer /* inner */ outer */ in C++?",
                "options": ["A syntax error occurs because the first '*/' closes the entire comment, leaving trailing characters as invalid code", "The compiler nests them safely", "The inner comment is converted to uppercase", "The comment is saved in Flash ROM"],
                "correct": 0,
                "explanation": "Block comments terminate at the very first <code>*/</code> encountered, leaving subsequent text exposed as invalid syntax."
            },
            {
                "question": "What is the recommended MISRA method for disabling a block of experimental code?",
                "options": ["Using preprocessor '#if 0 ... #endif' directives rather than block comments", "Writing 'TODO' on every line", "Deleting the code permanently from Git", "Setting all variables to zero"],
                "correct": 0,
                "explanation": "<code>#if 0 ... #endif</code> cleanly disables code blocks without nesting issues or risking accidental unclosed comment syntax bugs."
            },
            {
                "question": "Which Doxygen tag is standard for documenting the return value of a hardware driver function?",
                "options": ["@retval or @return", "@output", "@result", "@exit"],
                "correct": 0,
                "explanation": "<code>@retval</code> (for specific status return codes) or <code>@return</code> (for general return descriptions) is standard in Doxygen."
            },
            {
                "question": "Do comments have any impact on the compiled binary file size or RAM usage?",
                "options": ["No, all comments are stripped during the Preprocessing phase and generate zero bytes in Flash or RAM", "Yes, they add 1 byte per character to Flash", "Yes, they consume stack memory", "Yes, in debug mode only"],
                "correct": 0,
                "explanation": "The C++ preprocessor strips all comments before compilation begins; comments have zero impact on compiled code or memory."
            }
        ]
    },
    {
        "id": "variable_fun",
        "name": "VariableFun",
        "title": "Fundamental Types vs Fixed-Width Integers (<cstdint>)",
        "headline": "Fundamental Types, Implementation-Defined Widths vs Fixed-Width <cstdint> Types",
        "emb_class": "emb-high",
        "emb_badge": "⚡ Embedded Relevance: Critical",
        "tags": ["<cstdint>", "uint8_t", "uint32_t", "Data Types", "Implementation-Defined"],
        "summary": "Exploring fundamental C++ data types (int, double, char, bool). We demonstrate why non-standardized integer widths (e.g. sizeof(int) varies between 16-bit, 32-bit, and 64-bit architectures) cause critical cross-platform bugs, and enforce fixed-width integer types (<cstdint>) across all embedded firmware.",
        "files": ["section_2/VariableFun/VariableFun/main.cpp"],
        "concepts_html": """
        <h3>1. Fundamental Types in C++</h3>
        <p>In C++, fundamental types like <code>int</code>, <code>short</code>, <code>long</code> have implementation-defined bit widths. An <code>int</code> is 16 bits on an 8-bit AVR microcontroller, but 32 bits on an ARM Cortex-M.</p>

        <h3>2. Fixed-Width Integers (<code>&lt;cstdint&gt;</code>)</h3>
        <p>The <code>&lt;cstdint&gt;</code> header guarantees exact bit-widths across all compilers and CPU architectures (e.g. <code>uint8_t</code>, <code>int16_t</code>, <code>uint32_t</code>, <code>uint64_t</code>).</p>
        """,
        "embedded_html": """
        <h3>1. MISRA C++:2008 Rule 3-9-2</h3>
        <p>The basic numerical types (<code>int</code>, <code>short</code>, <code>long</code>) shall not be used; fixed-width types from <code>&lt;cstdint&gt;</code> (or typedefs indicating size and signedness) must be used exclusively to guarantee deterministic hardware bitmasks and avoid porting bugs.</p>
        """,
        "refactor_html": """
        <p>Explicit fixed-width register structures:</p>
        <pre class="code-block" style="background:#0d1117; padding:16px; border-radius:8px; border:1px solid #30363d;">#include &lt;cstdint&gt;

// Deterministic width across 8-bit, 16-bit, 32-bit, and 64-bit CPUs
struct AdcChannelConfig {
    uint8_t  channel_number; // Exactly 8 bits (0-255)
    uint16_t sampling_cycles;// Exactly 16 bits (0-65535)
    uint32_t calibration_val;// Exactly 32 bits
};</pre>
        """,
        "quiz": [
            {
                "question": "Why is 'int' avoided in embedded systems in favor of 'int32_t' or 'uint16_t' from <cstdint>?",
                "options": ["The bit width of 'int' is implementation-defined (16 bits on 8-bit MCUs, 32 bits on ARM), causing arithmetic bugs when porting code", "The keyword 'int' is deprecated in C++20", "'int' allocates memory on the heap", "'int' cannot be stored in Flash memory"],
                "correct": 0,
                "explanation": "Standard C++ allows <code>int</code> to be 16 or 32 bits depending on architecture. <code>&lt;cstdint&gt;</code> guarantees explicit bit-widths everywhere."
            },
            {
                "question": "What is the value range of an 8-bit unsigned integer (uint8_t)?",
                "options": ["0 to 255", "-128 to 127", "0 to 65,535", "-32,768 to 32,767"],
                "correct": 0,
                "explanation": "An unsigned 8-bit integer ($2^8 = 256$ distinct values) spans from 0 to 255."
            },
            {
                "question": "Which header must be included to access types like uint32_t, int16_t, and uint8_t in modern C++?",
                "options": ["<cstdint>", "<iostream>", "<stdlib.h>", "<types.h>"],
                "correct": 0,
                "explanation": "<code>&lt;cstdint&gt;</code> is the standard C++ header providing exact-width integer typedefs."
            },
            {
                "question": "What is 'size_t' in C++?",
                "options": ["An unsigned integer type capable of representing the size of any object in bytes on the target CPU architecture", "A 16-bit floating point type", "A type used only for strings", "A pointer to Flash memory"],
                "correct": 0,
                "explanation": "<code>size_t</code> is the unsigned architecture-native integer type returned by <code>sizeof</code> and container size methods."
            }
        ]
    },
    {
        "id": "text_fun",
        "name": "TextFun",
        "title": "Character Encodings, ASCII Tables & Control Codes",
        "headline": "char Representations, ASCII Control Codes & Serial Protocol Framing",
        "emb_class": "emb-core",
        "emb_badge": "⚡ Embedded Relevance: Core",
        "tags": ["char", "ASCII", "Escape Sequences", "Control Codes", "UART Framing"],
        "summary": "Exploring character types and escape sequences. We examine ASCII encoding tables, character-to-integer conversion, and how non-printable ASCII control codes (STX 0x02, ETX 0x03, ACK 0x06, NAK 0x15, CR '\\r', LF '\\n') frame serial communication packets.",
        "files": ["section_2/TextFun/TextFun/main.cpp"],
        "concepts_html": """
        <h3>1. Character Literals & ASCII Encodings</h3>
        <p>In C++, a <code>char</code> literal (<code>'A'</code>) evaluates to its integer ASCII numeric representation (<code>65</code> / <code>0x41</code>).</p>

        <h3>2. Escape Sequences</h3>
        <p>Special characters are represented via escape sequences: <code>'\\n'</code> (Line Feed - 0x0A), <code>'\\r'</code> (Carriage Return - 0x0D), <code>'\\t'</code> (Tab - 0x09), <code>'\\0'</code> (Null terminator - 0x00).</p>
        """,
        "embedded_html": """
        <h3>1. Serial Protocol Packet Framing</h3>
        <p>UART, RS-485, and Modbus ASCII protocols rely on control characters for message boundaries:</p>
        <ul>
          <li><code>0x02 (STX)</code>: Start of Text.</li>
          <li><code>0x03 (ETX)</code>: End of Text.</li>
          <li><code>0x0D 0x0A (CR LF)</code>: AT Command Line Terminations (GSM / GPS / WiFi modules).</li>
        </ul>
        """,
        "refactor_html": """
        <p>ASCII serial framing parser:</p>
        <pre class="code-block" style="background:#0d1117; padding:16px; border-radius:8px; border:1px solid #30363d;">#include &lt;cstdint&gt;

enum class AsciiControl : uint8_t {
    STX = 0x02, // Start of Packet
    ETX = 0x03, // End of Packet
    ACK = 0x06, // Acknowledge
    NAK = 0x15, // Negative Acknowledge
    CR  = 0x0D, // Carriage Return
    LF  = 0x0A  // Line Feed
};

constexpr bool isPacketBoundary(uint8_t byte) noexcept {
    return byte == static_cast&lt;uint8_t&gt;(AsciiControl::ETX) || 
           byte == static_cast&lt;uint8_t&gt;(AsciiControl::LF);
}</pre>
        """,
        "quiz": [
            {
                "question": "What is the ASCII integer value of the character '0' (zero)?",
                "options": ["48 (0x30)", "0", "1", "255"],
                "correct": 0,
                "explanation": "ASCII character <code>'0'</code> is encoded as decimal 48 (hexadecimal <code>0x30</code>). Subtracting <code>'0'</code> converts an ASCII digit character into its numeric integer value."
            },
            {
                "question": "How does a null terminator '\\0' differ from the digit character '0' in memory?",
                "options": ["'\\0' has numeric value 0x00 (all bits zero), while '0' has numeric value 0x30 (decimal 48)", "They are identical in memory", "'\\0' is 2 bytes while '0' is 1 byte", "'\\0' cannot be stored in an array"],
                "correct": 0,
                "explanation": "<code>'\\0'</code> is the null byte with numerical value 0, whereas the ASCII character <code>'0'</code> is 0x30 (48)."
            },
            {
                "question": "Why is 'char' signedness implementation-defined in standard C++?",
                "options": ["The standard allows compilers to make 'char' signed or unsigned depending on CPU architecture efficiency (e.g. ARM defaults to unsigned char, x86 to signed char)", "To encrypt string variables", "Because char can hold 16 bits", "To prevent string manipulation"],
                "correct": 0,
                "explanation": "Whether <code>char</code> is signed or unsigned is target-specific. On ARM Cortex-M, GCC defaults to unsigned char unless <code>-fsigned-char</code> is specified."
            },
            {
                "question": "Which escape sequence represents the Carriage Return (0x0D) character commonly required in cellular modem AT commands?",
                "options": ["'\\r'", "'\\n'", "'\\t'", "'\\0'"],
                "correct": 0,
                "explanation": "<code>'\\r'</code> represents Carriage Return (ASCII 0x0D), used with Line Feed (<code>'\\n'</code>, 0x0A) to terminate AT commands."
            }
        ]
    },
    {
        "id": "arithmetic_fun",
        "name": "ArithmeticFun",
        "title": "Arithmetic Operators, Integer Promotion & Overflow UB",
        "headline": "Integer Promotion Rules, Signed Overflow Undefined Behavior & Saturating Math",
        "emb_class": "emb-high",
        "emb_badge": "⚡ Embedded Relevance: Critical",
        "tags": ["Arithmetic", "Integer Promotion", "Signed Overflow UB", "Saturating Math", "Assembly"],
        "summary": "Analyzing arithmetic operators (+, -, *, /, %). We explore C++ Integer Promotion rules (small integer types are promoted to int during math), Signed Overflow Undefined Behavior (UB) which compilers exploit to optimize away safety checks, and ARM Cortex-M hardware saturating arithmetic instructions (QADD, QSUB).",
        "files": ["section_2/ArithmeticFun/ArithmeticFun/main.cpp"],
        "concepts_html": """
        <h3>1. Integer Promotion</h3>
        <p>In C++, arithmetic operations on types smaller than <code>int</code> (<code>uint8_t</code>, <code>int8_t</code>, <code>int16_t</code>) automatically promote operands to <code>int</code> before computation.</p>

        <h3>2. Signed vs Unsigned Overflow</h3>
        <ul>
          <li><strong>Unsigned Overflow:</strong> Well-defined by the standard to wrap around modulo $2^N$.</li>
          <li><strong>Signed Overflow:</strong> <strong>UNDEFINED BEHAVIOR (UB)</strong>. The compiler assumes signed overflow never occurs, and may optimize away sanity/safety bounds checks!</li>
        </ul>
        """,
        "embedded_html": """
        <h3>1. Hardware Saturating Arithmetic (DSP QADD / QSUB)</h3>
        <p>In audio and sensor processing, wrap-around overflow causes deafening acoustic clicks or motor runaway. ARM Cortex-M DSP instructions clamp out-of-range results to maximum/minimum limits in a single clock cycle.</p>
        """,
        "refactor_html": """
        <p>Software saturating integer addition:</p>
        <pre class="code-block" style="background:#0d1117; padding:16px; border-radius:8px; border:1px solid #30363d;">#include &lt;cstdint&gt;
#include &lt;algorithm&gt;

// Saturating addition: Clamps to 255 rather than wrapping to 0
constexpr uint8_t add_saturating_u8(uint8_t a, uint8_t b) noexcept {
    uint16_t sum = static_cast&lt;uint16_t&gt;(a) + b;
    return static_cast&lt;uint8_t&gt;(sum &gt; 255 ? 255 : sum);
}</pre>
        """,
        "quiz": [
            {
                "question": "What is the behavior of signed integer overflow (e.g. INT_MAX + 1) in standard C++?",
                "options": ["Undefined Behavior (UB); the compiler may optimize away downstream bounds checks assuming it is impossible", "Guaranteed to wrap around to INT_MIN", "Throws a std::overflow_error exception", "Sets the integer to 0"],
                "correct": 0,
                "explanation": "Signed overflow is Undefined Behavior in C++. Compilers are free to assume overflow never happens, often eliminating critical safety range checks."
            },
            {
                "question": "What happens under C++ Integer Promotion rules when two uint8_t variables are added (uint8_t a = 100, b = 200; auto c = a + b;)?",
                "options": ["Both operands are promoted to 'int' (32 bits), and the expression evaluates to an 'int' with value 300", "The result immediately wraps to uint8_t (44)", "A compile-time type mismatch occurs", "The variables are cast to float"],
                "correct": 0,
                "explanation": "Under integer promotion rules, types narrower than <code>int</code> are promoted to <code>int</code> before arithmetic evaluation."
            },
            {
                "question": "What is 'saturating arithmetic' in embedded DSP and motor control algorithms?",
                "options": ["Arithmetic where results that exceed the maximum representable value clamp to MAX instead of wrapping around to 0 or negative numbers", "Arithmetic performed in liquids", "Arithmetic that disables the CPU clock", "Floating-point math in software"],
                "correct": 0,
                "explanation": "Saturating arithmetic clamps values at bounds limits (e.g. 255 for uint8_t), preventing sudden sign inversion or wrap-around glitches in control loops."
            },
            {
                "question": "What does unsigned integer overflow guarantee in C++?",
                "options": ["Deterministic modulo arithmetic wrap-around (e.g. 255 + 1 == 0 for uint8_t)", "Undefined Behavior", "Hardware HardFault trap", "Stack frame corruption"],
                "correct": 0,
                "explanation": "Unsigned integer arithmetic in C++ is guaranteed to wrap modulo $2^N$ according to the standard."
            }
        ]
    },
    {
        "id": "relational_fun",
        "name": "RelationalFun",
        "title": "Relational Operators, Floating-Point Epsilon & Condition Flags",
        "headline": "Comparisons (<, <=, ==, !=), Floating-Point Epsilon & ARM Condition Codes (APSR)",
        "emb_class": "emb-core",
        "emb_badge": "⚡ Embedded Relevance: Core",
        "tags": ["Relational Operators", "Epsilon Comparison", "ARM Flags", "APSR", "CMP Instruction"],
        "summary": "Exploring relational comparison operators. We demonstrate why exact equality comparisons (==) on floating-point numbers fail due to binary representation inaccuracy and how to compare using an epsilon tolerance, and inspect ARM Application Program Status Register (APSR) condition flags (N, Z, C, V).",
        "files": ["section_2/RelationalFun/RelationalFun/main.cpp"],
        "concepts_html": """
        <h3>1. Relational Operators</h3>
        <p>Relational operators (<code>&lt;</code>, <code>&gt;</code>, <code>&lt;=</code>, <code>&gt;=</code>, <code>==</code>, <code>!=</code>) return boolean values (<code>true</code> / <code>false</code>).</p>

        <h3>2. The Floating-Point Equality Hazard</h3>
        <p>Binary floating-point numbers cannot represent decimal fractions like 0.1 exactly ($0.1 + 0.2 \\ne 0.3$). Direct equality comparisons (<code>a == b</code>) are dangerous. Use epsilon tolerance checks: <code>std::abs(a - b) &lt; EPSILON</code>.</p>
        """,
        "embedded_html": """
        <h3>1. ARM Cortex-M Condition Flags (APSR)</h3>
        <p>The <code>CMP</code> instruction subtracts two operands and sets flags in the <strong>Application Program Status Register (APSR)</strong>:</p>
        <ul>
          <li><strong>Z (Zero):</strong> Set if result is zero (equality).</li>
          <li><strong>N (Negative):</strong> Set if result is negative.</li>
          <li><strong>C (Carry):</strong> Set on unsigned overflow/no-borrow.</li>
          <li><strong>V (oVerflow):</strong> Set on signed arithmetic overflow.</li>
        </ul>
        """,
        "refactor_html": """
        <p>Robust floating-point and fixed-point comparison helper:</p>
        <pre class="code-block" style="background:#0d1117; padding:16px; border-radius:8px; border:1px solid #30363d;">#include &lt;cmath&gt;

constexpr float EPSILON = 0.0001f;

constexpr bool areFloatsEqual(float a, float b) noexcept {
    float diff = a - b;
    return (diff &lt; 0.0f ? -diff : diff) &lt; EPSILON;
}</pre>
        """,
        "quiz": [
            {
                "question": "Why does the expression '0.1f + 0.2f == 0.3f' evaluate to false in C++?",
                "options": ["Binary IEEE 754 floating-point cannot represent 0.1 and 0.2 exactly, resulting in small rounding discrepancies", "C++ does not allow adding two float literals", "Floating point equality is disabled at -O2", "0.3f is promoted to double automatically"],
                "correct": 0,
                "explanation": "Binary floating-point represents numbers as fractions with powers of 2 in the denominator; decimal fractions like 0.1 produce repeating binary fractions that suffer rounding truncation."
            },
            {
                "question": "How should two floating-point sensor values be compared for equality in safety-critical firmware?",
                "options": ["Check if the absolute difference is less than an acceptable epsilon threshold: std::abs(a - b) < EPSILON", "Use the '===' operator", "Cast both floats to void*", "Multiply both by zero"],
                "correct": 0,
                "explanation": "Comparing against an epsilon tolerance accounts for floating-point representation and calculation rounding errors."
            },
            {
                "question": "Which ARM APSR status flag is set to 1 when a comparison (CMP R0, R1) detects two equal values?",
                "options": ["Z (Zero) flag", "N (Negative) flag", "V (Overflow) flag", "C (Carry) flag"],
                "correct": 0,
                "explanation": "<code>CMP R0, R1</code> computes $R0 - R1$. If they are equal, the result is zero, setting the Z (Zero) condition flag to 1."
            },
            {
                "question": "What is the return type of relational expressions (e.g. 5 > 3) in C++?",
                "options": ["bool (evaluating to true or false)", "int (1 or 0)", "uint8_t", "size_t"],
                "correct": 0,
                "explanation": "Relational operators in C++ return boolean type (<code>bool</code>)."
            }
        ]
    },
    {
        "id": "logical_fun",
        "name": "LogicalFun",
        "title": "Logical Operators & Short-Circuit Evaluation Safety",
        "headline": "Short-Circuit Evaluation (&&, ||), Hardware Null Guards & Bitwise vs Logical Gotchas",
        "emb_class": "emb-high",
        "emb_badge": "⚡ Embedded Relevance: Critical",
        "tags": ["Logical Operators", "Short-Circuit", "Null Guards", "&& vs &", "Safety Guards"],
        "summary": "Exploring logical operators (&&, ||, !). We analyze Short-Circuit Evaluation, demonstrate how short-circuiting provides safe null pointer guards before hardware MMIO register dereferencing, and highlight dangerous bugs caused by confusing logical (&&) with bitwise (&) operators.",
        "files": ["section_2/LogicalFun/LogicalFun/main.cpp"],
        "concepts_html": """
        <h3>1. Short-Circuit Evaluation</h3>
        <ul>
          <li><code>A &amp;&amp; B</code>: If <code>A</code> is <code>false</code>, <code>B</code> is <strong>never evaluated</strong>.</li>
          <li><code>A || B</code>: If <code>A</code> is <code>true</code>, <code>B</code> is <strong>never evaluated</strong>.</li>
        </ul>

        <h3>2. Null Pointer Guard Idiom</h3>
        <p>Thanks to short-circuiting, <code>if (ptr != nullptr &amp;&amp; ptr-&gt;status == OK)</code> is completely safe; if <code>ptr</code> is null, the second expression is never executed, preventing null pointer dereference crashes.</p>
        """,
        "embedded_html": """
        <h3>1. Dangerous Bug: <code>&amp;</code> vs <code>&amp;&amp;</code></h3>
        <p>Using bitwise <code>&amp;</code> instead of logical <code>&amp;&amp;</code> evaluates <strong>both sides unconditionally</strong> without short-circuiting. If applied to a null guard, it will crash the CPU with a HardFault.</p>
        """,
        "refactor_html": """
        <p>Short-circuit hardware peripheral guard:</p>
        <pre class="code-block" style="background:#0d1117; padding:16px; border-radius:8px; border:1px solid #30363d;">#include &lt;cstdint&gt;

struct UartHardware {
    volatile uint32_t SR;
    volatile uint32_t DR;
};

// Safe: If dev is null, dev->SR is never accessed
bool isUartReady(const UartHardware* dev) noexcept {
    return (dev != nullptr) &amp;&amp; ((dev-&gt;SR &amp; (1UL &lt;&lt; 7)) != 0);
}</pre>
        """,
        "quiz": [
            {
                "question": "How does 'Short-Circuit Evaluation' protect the expression 'if (ptr != nullptr && ptr->val > 0)' from crashing when ptr is null?",
                "options": ["Because the first condition is false, C++ guarantees the second condition (ptr->val) is never evaluated, preventing null dereferencing", "The compiler allocates dummy memory for ptr", "The operating system catches the null pointer", "C++ replaces null with address 0x0001"],
                "correct": 0,
                "explanation": "In <code>&amp;&amp;</code> expressions, if the left operand is false, the right operand is guaranteed not to execute."
            },
            {
                "question": "What happens if a developer mistakenly writes 'if (ptr != nullptr & ptr->val > 0)' with a single bitwise '&' when ptr is null?",
                "options": ["Both sides are evaluated unconditionally, dereferencing the null pointer and triggering a fatal CPU HardFault crash", "It behaves identically to &&", "The compiler fixes the error automatically", "The loop terminates cleanly"],
                "correct": 0,
                "explanation": "Bitwise <code>&amp;</code> is an arithmetic operator that does not short-circuit; both operands evaluate, causing a null pointer dereference."
            },
            {
                "question": "What is the result of '!true' in C++?",
                "options": ["false", "true", "-1", "0xFF"],
                "correct": 0,
                "explanation": "The logical NOT operator (<code>!</code>) inverts boolean truth, turning true into false."
            },
            {
                "question": "In the expression 'if (is_admin || check_database())', when will 'check_database()' be executed?",
                "options": ["Only if 'is_admin' evaluates to false", "Always, unconditionally", "Only if 'is_admin' evaluates to true", "Never"],
                "correct": 0,
                "explanation": "In <code>||</code> expressions, if the left operand is true, the overall result is already known to be true, so the right operand is skipped."
            }
        ]
    },
    {
        "id": "boolean_fun",
        "name": "BooleanFun",
        "title": "Boolean Types, Bitfields & Packed Flag Registers",
        "headline": "bool Size Overhead (1 Byte) vs Bitfields & std::bitset for Packed Bitmasks",
        "emb_class": "emb-high",
        "emb_badge": "⚡ Embedded Relevance: High",
        "tags": ["bool", "Bitfields", "Bitmasks", "std::bitset", "Register Bit Packing"],
        "summary": "Exploring the boolean data type. We analyze why sizeof(bool) occupies a full 8 bits (1 byte) in memory rather than 1 single bit due to byte-addressability, and demonstrate how to pack 8 boolean flags into a single byte using bitwise bitmasks and C++ bitfields.",
        "files": ["section_2/BooleanFun/BooleanFun/main.cpp"],
        "concepts_html": """
        <h3>1. <code>sizeof(bool)</code> is 1 Byte</h3>
        <p>Even though a boolean holds only 1 bit of information (0 or 1), the CPU's smallest addressable memory unit is a <strong>byte (8 bits)</strong>. Storing 8 independent <code>bool</code> variables consumes 8 bytes of RAM.</p>

        <h3>2. Bitfield Structures</h3>
        <p>C++ bitfields allow specifying exact bit widths for structure members: <code>uint8_t flag : 1;</code>.</p>
        """,
        "embedded_html": """
        <h3>1. Register Bit Packing with Bitmasks</h3>
        <p>Microcontroller hardware control registers (e.g. GPIO MODER, CR1) pack dozens of configuration flags into a single 32-bit word. Bitwise operations (<code>|</code>, <code>&amp;</code>, <code>~</code>, <code>^</code>) configure registers without wasting RAM.</p>
        """,
        "refactor_html": """
        <p>Packed 8-flag status register (1 Byte Total):</p>
        <pre class="code-block" style="background:#0d1117; padding:16px; border-radius:8px; border:1px solid #30363d;">#include &lt;cstdint&gt;

struct SystemFlags {
    uint8_t power_good    : 1;
    uint8_t wifi_connected: 1;
    uint8_t sd_card_ready : 1;
    uint8_t motor_fault   : 1;
    uint8_t over_temp     : 1;
    uint8_t reserved      : 3;
}; // Exactly 1 byte in SRAM!</pre>
        """,
        "quiz": [
            {
                "question": "Why does a single 'bool' variable in C++ occupy 1 full byte (8 bits) in memory instead of 1 bit?",
                "options": ["Modern CPU architectures are byte-addressable; individual bits cannot have unique memory addresses", "Because bool is a 64-bit float internally", "To store Unicode characters", "Because C++ forbids binary storage"],
                "correct": 0,
                "explanation": "CPU memory pointers address byte boundaries (8 bits). Single bits cannot be directly addressed by pointer, so <code>bool</code> occupies 1 byte."
            },
            {
                "question": "How much RAM do 8 independent 'bool' variables consume vs a single uint8_t bitmask byte?",
                "options": ["8 bools consume 8 bytes (64 bits); a bitmask consumes exactly 1 byte (8 bits), saving 87.5% RAM", "Both consume 1 byte", "8 bools consume 32 bytes", "Bitmasks consume more RAM"],
                "correct": 0,
                "explanation": "8 individual <code>bool</code> variables take 8 bytes (64 bits), whereas a packed <code>uint8_t</code> stores all 8 flags in 1 single byte."
            },
            {
                "question": "Which bitwise operator is used to set bit 3 (0x08) of a hardware register to 1 without altering other bits?",
                "options": ["Bitwise OR: REG |= (1UL << 3)", "Bitwise AND: REG &= (1UL << 3)", "Bitwise NOT: REG = ~3", "Bitwise XOR: REG ^= 3"],
                "correct": 0,
                "explanation": "Bitwise OR (<code>REG |= (1UL &lt;&lt; 3)</code>) sets target bits to 1 while leaving all other bits unaffected."
            },
            {
                "question": "Which bitwise operator is used to clear bit 4 (0x10) of a register to 0 without modifying any other bits?",
                "options": ["Bitwise AND with inverted mask: REG &= ~(1UL << 4)", "Bitwise OR: REG |= (1UL << 4)", "Bitwise XOR: REG ^= (1UL << 4)", "Addition: REG += 4"],
                "correct": 0,
                "explanation": "<code>REG &amp;= ~(1UL &lt;&lt; 4)</code> creates a bitmask with bit 4 cleared to 0 and all other bits 1, clearing bit 4 safely."
            }
        ]
    },
    {
        "id": "constant_fun",
        "name": "ConstantFun",
        "title": "Constants: #define vs const vs constexpr",
        "headline": "Macros (#define) vs const vs constexpr: Flash ROM (.rodata) & Scope Safety",
        "emb_class": "emb-high",
        "emb_badge": "⚡ Embedded Relevance: Critical",
        "tags": ["constexpr", "const", "#define", ".rodata", "Type Safety"],
        "summary": "Analyzing constants in C++. We contrast legacy C preprocessor macros (#define) with type-safe const and compile-time constexpr, explaining why macros lack scope and type verification, and how static constexpr constants are placed 100% in Flash ROM (.rodata) with 0 SRAM consumption.",
        "files": ["section_2/ConstantFun/ConstantFun/main.cpp"],
        "concepts_html": """
        <h3>1. Legacy <code>#define</code> Macros</h3>
        <p><code>#define BUFFER_SIZE 64</code> is a dumb text substitution performed by the preprocessor. It ignores scope, has no type verification, and is invisible to GDB symbolic debuggers.</p>

        <h3>2. <code>const</code> vs <code>constexpr</code></h3>
        <ul>
          <li><code>const</code>: Read-only variable; may be evaluated at runtime.</li>
          <li><code>constexpr</code>: Guaranteed compile-time constant expression; evaluated by the compiler during build.</li>
        </ul>
        """,
        "embedded_html": """
        <h3>1. Zero SRAM Overhead with <code>constexpr</code></h3>
        <p><code>constexpr</code> primitive values are embedded directly into assembly instructions as immediate operands (<code>MOV R0, #64</code>), consuming <strong>0 bytes of SRAM and 0 memory read cycles</strong>.</p>
        """,
        "refactor_html": """
        <p>Replacing macros with type-safe constexpr definitions:</p>
        <pre class="code-block" style="background:#0d1117; padding:16px; border-radius:8px; border:1px solid #30363d;">#include &lt;cstdint&gt;

// BAD (Legacy C Macro): No type, no scope, debugger blind
// #define MAX_VOLTAGE 3.3

// GOOD (Modern C++): Type-safe, scoped, compile-time verified
namespace HardwareConfig {
    constexpr float    MAX_VOLTAGE_V  = 3.3f;
    constexpr uint32_t SPI_BAUD_RATE  = 10'000'000; // 10 MHz
    constexpr uint8_t  MAX_RETRY_COUNT = 3;
}</pre>
        """,
        "quiz": [
            {
                "question": "Why is 'constexpr uint32_t MAX_SIZE = 128;' superior to '#define MAX_SIZE 128'?",
                "options": ["It is type-safe, respects C++ namespace scoping, and provides symbolic debugging information in GDB", "It executes in half the clock cycles", "It allows modifying the constant at runtime", "It allocates constants on the heap"],
                "correct": 0,
                "explanation": "<code>constexpr</code> offers strong type checking, respects namespace encapsulation, and produces debug symbols for GDB."
            },
            {
                "question": "Where are 'static constexpr' lookup tables placed in the microcontroller memory map?",
                "options": ["In Flash ROM (.rodata section), consuming 0 bytes of SRAM", "In SRAM (.bss section)", "On the CPU stack frame", "In the heap"],
                "correct": 0,
                "explanation": "The linker places <code>static constexpr</code> tables in the read-only data (<code>.rodata</code>) section in Flash ROM."
            },
            {
                "question": "What happens if a macro '#define SQUARE(x) x * x' is called as 'SQUARE(2 + 3)'?",
                "options": ["It expands to '2 + 3 * 2 + 3' which evaluates to 11 instead of 25 due to operator precedence bugs", "It evaluates to 25 correctly", "It causes a compile error", "It creates a runtime exception"],
                "correct": 0,
                "explanation": "Macros perform raw text substitution; without parenthesis <code>(x) * (x)</code>, operator precedence produces <code>2 + 6 + 3 = 11</code>."
            },
            {
                "question": "Can a constexpr variable be modified after its definition?",
                "options": ["No, constexpr implies const and is strictly immutable", "Yes, using const_cast", "Yes, in debug mode", "Yes, if declared inside a class"],
                "correct": 0,
                "explanation": "<code>constexpr</code> guarantees immutability; values cannot be changed after definition."
            }
        ]
    },
    {
        "id": "keyboard_input",
        "name": "KeyboardInput",
        "title": "Interactive Console I/O vs Microcontroller UART Ring Buffers",
        "headline": "std::cin Stream Blocking vs Non-Blocking Interrupt-Driven UART RX",
        "emb_class": "emb-core",
        "emb_badge": "⚡ Embedded Relevance: Core",
        "tags": ["std::cin", "Blocking I/O", "UART RX", "Interrupts", "Input Validation"],
        "summary": "Exploring keyboard user input via std::cin. We examine the hazards of blocking I/O in real-time systems, stream fail states (cin.fail()), and how embedded systems replace console streams with non-blocking interrupt-driven UART serial receivers.",
        "files": ["section_2/KeyboardInput/KeyboardInput/main.cpp"],
        "concepts_html": """
        <h3>1. <code>std::cin</code> Stream Extraction</h3>
        <p><code>std::cin &gt;&gt; var</code> extracts formatted tokens from standard input. If input formatting fails (e.g. typing characters into an integer variable), the stream enters a fail state (<code>cin.fail()</code>) and stops processing input.</p>
        """,
        "embedded_html": """
        <h3>1. The Danger of Blocking I/O in Firmware</h3>
        <p>Functions that block waiting for input halt the entire CPU. In an embedded controller running a motor or heater, blocking for serial input causes runaway hardware destruction. All embedded I/O must be <strong>non-blocking or interrupt-driven</strong>.</p>
        """,
        "refactor_html": """
        <p>Non-blocking interrupt-driven UART byte receiver:</p>
        <pre class="code-block" style="background:#0d1117; padding:16px; border-radius:8px; border:1px solid #30363d;">#include &lt;cstdint&gt;

// Non-blocking UART receiver check
bool uart_try_read(uint8_t&amp; out_byte) noexcept {
    volatile uint32_t* const USART1_SR = reinterpret_cast&lt;volatile uint32_t*&gt;(0x40013800);
    volatile uint32_t* const USART1_DR = reinterpret_cast&lt;volatile uint32_t*&gt;(0x40013804);

    if (*USART1_SR &amp; (1UL &lt;&lt; 5)) { // RXNE: Read Data Register Not Empty
        out_byte = static_cast&lt;uint8_t&gt;(*USART1_DR &amp; 0xFF);
        return true; // Byte received instantly!
    }
    return false; // No data available; does NOT block CPU!
}</pre>
        """,
        "quiz": [
            {
                "question": "Why is blocking input (like std::cin >> x) unacceptable in real-time embedded control systems?",
                "options": ["Blocking freezes the CPU, preventing safety control loops (e.g. thermal regulation, motor PWM) from executing", "std::cin causes physical damage to RAM", "std::cin requires 64-bit registers", "Blocking increases power consumption by 1000%"],
                "correct": 0,
                "explanation": "Blocking operations monopolize CPU execution, preventing critical real-time sensor sampling and actuator control loops from running."
            },
            {
                "question": "What happens to std::cin when a user enters alphabetic text into an integer variable (int x; cin >> x;)?",
                "options": ["The stream sets its failbit flag (cin.fail() becomes true), leaves x unmodified, and ignores future extractions until cin.clear() is called", "The program crashes with a segmentation fault", "The characters are converted to ASCII sums", "The variable x is set to infinity"],
                "correct": 0,
                "explanation": "Stream extraction sets <code>failbit</code> upon formatting failure, requiring <code>cin.clear()</code> and <code>cin.ignore()</code> to recover."
            },
            {
                "question": "How do embedded systems handle incoming serial data asynchronously without blocking the CPU?",
                "options": ["Hardware UART Receive Interrupts (RXNE ISR) push bytes into a circular ring buffer in the background", "By polling the port every 5 seconds", "By using virtual memory", "By creating infinite while loops"],
                "correct": 0,
                "explanation": "UART RX interrupts trigger whenever a byte arrives in hardware, placing it into a background FIFO queue without stalling the main loop."
            },
            {
                "question": "Which method clears the error state flags on a C++ input stream?",
                "options": ["cin.clear()", "cin.reset()", "cin.flush()", "cin.empty()"],
                "correct": 0,
                "explanation": "<code>cin.clear()</code> clears the error state flags (<code>failbit</code>, <code>badbit</code>), restoring the stream to a working state."
            }
        ]
    },
    {
        "id": "sunny_warm",
        "name": "SunnyWarm",
        "title": "Boolean Logic, Condition Inversion & De Morgan's Laws",
        "headline": "Compound Boolean Expressions, Truth Tables & De Morgan's Optimization Laws",
        "emb_class": "emb-core",
        "emb_badge": "⚡ Embedded Relevance: Core",
        "tags": ["De Morgan's Laws", "Boolean Logic", "Truth Tables", "Optimization", "Logic Inversion"],
        "summary": "Analyzing compound boolean logic and truth tables. We explore De Morgan's Laws for simplifying complex nested conditions, reducing branch instruction count in assembly, and ensuring logic inversion safety in mission-critical systems.",
        "files": ["section_2/SunnyWarm/SunnyWarm/main.cpp"],
        "concepts_html": """
        <h3>1. De Morgan's Laws</h3>
        <p>De Morgan's laws state that:</p>
        <ul>
          <li><code>!(A &amp;&amp; B) == (!A || !B)</code></li>
          <li><code>!(A || B) == (!A &amp;&amp; !B)</code></li>
        </ul>
        <p>Applying these rules simplifies boolean condition checks in firmware.</p>
        """,
        "embedded_html": """
        <h3>1. Reducing Branch Instructions</h3>
        <p>Simplifying complex logical conditions reduces conditional branch instructions (<code>BNE</code>, <code>BEQ</code>), minimizing CPU pipeline hazard penalties.</p>
        """,
        "refactor_html": """
        <p>Simplified, branch-efficient flight safety check:</p>
        <pre class="code-block" style="background:#0d1117; padding:16px; border-radius:8px; border:1px solid #30363d;">#include &lt;cstdint&gt;

struct FlightConditions {
    bool is_battery_healthy;
    bool is_gps_locked;
    bool is_motor_armed;
};

// Simplified using De Morgan's laws for fastest early exit
constexpr bool isFlightReady(FlightConditions f) noexcept {
    return f.is_battery_healthy &amp;&amp; f.is_gps_locked &amp;&amp; f.is_motor_armed;
}</pre>
        """,
        "quiz": [
            {
                "question": "According to De Morgan's Laws, what is the equivalent expression for '!(A && B)'?",
                "options": ["!A || !B", "!A && !B", "A || B", "A && !B"],
                "correct": 0,
                "explanation": "De Morgan's law states that negating a logical AND produces a logical OR of the negated terms: <code>!(A &amp;&amp; B) &equiv; (!A || !B)</code>."
            },
            {
                "question": "According to De Morgan's Laws, what is the equivalent expression for '!(A || B)'?",
                "options": ["!A && !B", "!A || !B", "A && B", "!A || B"],
                "correct": 0,
                "explanation": "Negating a logical OR produces a logical AND of the negated terms: <code>!(A || B) &equiv; (!A &amp;&amp; !B)</code>."
            },
            {
                "question": "Why does simplifying boolean expressions improve microcontroller assembly execution?",
                "options": ["It eliminates redundant comparison and conditional branch instructions, preventing pipeline stalls", "It increases CPU voltage", "It moves variables into Flash ROM", "It converts integers to floating point"],
                "correct": 0,
                "explanation": "Simplified boolean expressions generate fewer conditional jumps in assembly, preventing branch mispredictions."
            },
            {
                "question": "In the truth table for logical AND (A && B), how many out of the 4 input combinations yield 'true'?",
                "options": ["1 combination (only when both A and B are true)", "2 combinations", "3 combinations", "4 combinations"],
                "correct": 0,
                "explanation": "Logical AND yields true only when both operands are true ($1 \\times 1 = 1$)."
            }
        ]
    },
    {
        "id": "percentages",
        "name": "Percentages",
        "title": "Ratio Calculations, Integer Scaling & Loss of Precision",
        "headline": "Integer Ratio Division, Order of Operations & Multiply-Before-Divide Scaling",
        "emb_class": "emb-core",
        "emb_badge": "⚡ Embedded Relevance: Core",
        "tags": ["Integer Scaling", "Precision Loss", "Multiply-Before-Divide", "Overflow", "Percentages"],
        "summary": "Calculating percentage ratios from integer variables. We examine the classic beginner integer division pitfall (e.g. (count / total) * 100 evaluating to 0), enforce the Multiply-Before-Divide rule, and protect against 32-bit overflow using 64-bit intermediate accumulators.",
        "files": ["section_2/Percentages/Percentages/main.cpp"],
        "concepts_html": """
        <h3>1. The Zero-Result Pitfall</h3>
        <p>In integer arithmetic, evaluating <code>(part / total) * 100</code> performs integer division first. When <code>part &lt; total</code>, <code>part / total</code> truncates to <code>0</code>, resulting in <code>0 * 100 = 0%</code>!</p>

        <h3>2. The Multiply-Before-Divide Rule</h3>
        <p>To preserve precision, always multiply first: <code>(part * 100) / total</code>.</p>
        """,
        "embedded_html": """
        <h3>1. Preventing Intermediate Overflow</h3>
        <p>Multiplying <code>part * 100</code> can overflow 32-bit integer limits if <code>part &gt; 42,949,672</code>. Casting to <code>uint64_t</code> during the multiplication step guarantees 100% overflow immunity.</p>
        """,
        "refactor_html": """
        <p>Safe, high-precision integer percentage calculation:</p>
        <pre class="code-block" style="background:#0d1117; padding:16px; border-radius:8px; border:1px solid #30363d;">#include &lt;cstdint&gt;

// Calculates percentage (0-100%) with 0 float overhead and 0 overflow risk
constexpr uint32_t calculatePercentage(uint32_t part, uint32_t total) noexcept {
    if (total == 0) return 0;
    // 64-bit promotion prevents 32-bit intermediate multiplication overflow
    return static_cast&lt;uint32_t&gt;((static_cast&lt;uint64_t&gt;(part) * 100UL) / total);
}</pre>
        """,
        "quiz": [
            {
                "question": "Why does the C++ integer expression '(5 / 10) * 100' evaluate to 0 instead of 50?",
                "options": ["Integer division 5 / 10 truncates to 0 before multiplication by 100 occurs", "The compiler replaces 100 with 0", "Parentheses are illegal in arithmetic expressions", "C++ does not support percentages"],
                "correct": 0,
                "explanation": "Because division occurs first, $5/10 = 0$ in integer arithmetic. Then $0 \\times 100 = 0$."
            },
            {
                "question": "What is the 'Multiply-Before-Divide' rule in fixed-point and integer embedded math?",
                "options": ["Perform multiplication by the scale factor (e.g. 100) before dividing, preserving precision without fractional truncation", "Always use double precision", "Divide by zero first to check bounds", "Multiply by 2 then shift left"],
                "correct": 0,
                "explanation": "Multiplying before dividing preserves resolution in the upper bits before integer truncation occurs."
            },
            {
                "question": "What is the danger of '(part * 1000) / total' when 'part' is a large uint32_t variable?",
                "options": ["'part * 1000' can overflow the 32-bit integer limit (4,294,967,295), causing silent data corruption", "It triggers a division by zero", "It deletes the total variable", "It causes flash memory wear"],
                "correct": 0,
                "explanation": "If $part \\times 1000 > 2^{32}-1$, 32-bit overflow occurs. Casting to <code>uint64_t</code> before multiplication prevents this."
            },
            {
                "question": "How do you calculate basis points (0.01% resolution, e.g. 5000 = 50.00%) using integer math?",
                "options": ["(static_cast<uint64_t>(part) * 10000UL) / total", "(part / total) * 10000", "(part * 10) / total", "part % total"],
                "correct": 0,
                "explanation": "Multiplying by 10,000 provides $1/10,000$ ($0.01\\%$) resolution with integer arithmetic."
            }
        ]
    },
    {
        "id": "tip_calculator",
        "name": "TipCalculator",
        "title": "Financial Calculations & Currency Fixed-Point (Cents Math)",
        "headline": "Currency Fixed-Point Representation vs Floating-Point Rounding Hazards",
        "emb_class": "emb-core",
        "emb_badge": "⚡ Embedded Relevance: Core",
        "tags": ["Fixed-Point", "Cents Math", "Currency", "IEEE 754 Rounding", "Financial Systems"],
        "summary": "Building tip and tax computation utilities. We explore why floating-point types (float, double) are strictly banned in banking, POS terminals, and ticketing firmware due to decimal fraction rounding errors, and implement exact integer fixed-point (cents/millicents) arithmetic.",
        "files": ["section_2/TipCalculator/TipCalculator/main.cpp"],
        "concepts_html": """
        <h3>1. The Floating-Point Currency Disaster</h3>
        <p>Floating-point numbers cannot represent exact decimal amounts (e.g. <code>$0.10</code>). Performing financial calculations in <code>double</code> causes fractional penny drift that fails accounting audits.</p>

        <h3>2. Integer Cents Representation</h3>
        <p>Financial and metering embedded systems store all monetary amounts as integer cents (<code>$19.99 = 1999</code> cents) or millicents ($1/1000$), guaranteeing 100% exact math.</p>
        """,
        "embedded_html": """
        <h3>1. Point-of-Sale (POS) & Smart Card Terminals</h3>
        <p>In EMV payment terminals and utility energy meters, all billing algorithms use integer currency units to prevent rounding errors.</p>
        """,
        "refactor_html": """
        <p>Exact integer fixed-point currency calculation:</p>
        <pre class="code-block" style="background:#0d1117; padding:16px; border-radius:8px; border:1px solid #30363d;">#include &lt;cstdint&gt;

struct CurrencyUSD {
    uint64_t total_cents{0};

    // Calculate tip (e.g. 15% tip on $20.00 = 2000 cents)
    constexpr CurrencyUSD calculate_tip(uint32_t percent) const noexcept {
        return CurrencyUSD{(total_cents * percent + 50) / 100}; // +50 for rounding
    }
};</pre>
        """,
        "quiz": [
            {
                "question": "Why are floating-point types (float, double) strictly prohibited for currency calculations in POS payment terminals?",
                "options": ["Binary floating-point cannot represent decimal fractions like 0.01 or 0.10 exactly, causing cumulative penny rounding errors", "Floats cannot represent numbers greater than $100", "Floating point operations require an internet connection", "POS chips do not have an ALU"],
                "correct": 0,
                "explanation": "Binary float representations produce rounding errors that violate financial accounting standards; integer cents must be used."
            },
            {
                "question": "How is $49.95 represented in standard integer currency fixed-point?",
                "options": ["4995 (stored as an integer count of cents)", "49.95f", "49", "0.4995"],
                "correct": 0,
                "explanation": "Storing currency as integer cents (4995) eliminates all floating-point rounding errors."
            },
            {
                "question": "How do you calculate a 15% tip on an integer amount of 'cents' with proper nearest-cent rounding?",
                "options": ["(cents * 15 + 50) / 100", "(cents * 15) / 100", "(cents / 100) * 15", "cents * 0.15f"],
                "correct": 0,
                "explanation": "Adding 50 (half the divisor 100) before dividing achieves exact nearest-cent rounding."
            },
            {
                "question": "What is the benefit of using uint64_t for currency calculations?",
                "options": ["It can safely store up to $184 billion without arithmetic overflow during multiplication", "It converts dollars to euros automatically", "It moves variables into Flash ROM", "It runs in constant O(0) time"],
                "correct": 0,
                "explanation": "<code>uint64_t</code> easily accommodates multi-billion dollar calculations and intermediate scaling multiplications without overflow."
            }
        ]
    },
    {
        "id": "secret_agent_id",
        "name": "SecretAgentID",
        "title": "String Parsing, Security Tokens & Stream Manipulation",
        "headline": "Formatted String Parsing, Buffer Boundaries & Embedded Authentication Tokens",
        "emb_class": "emb-core",
        "emb_badge": "⚡ Embedded Relevance: Core",
        "tags": ["String Parsing", "Buffer Safety", "Security Tokens", "Authentication", "Validation"],
        "summary": "Building security identifier formatting and user credential validation. We analyze formatted I/O manipulation, string parsing safety, and preventing buffer overflows when processing user authentication tokens in embedded access-control systems.",
        "files": ["section_2/SecretAgentID/SecretAgentID/main.cpp"],
        "concepts_html": """
        <h3>1. String Concatenation & Formatting</h3>
        <p>Combining text prefixes, numerical IDs, and formatting strings for identification records.</p>

        <h3>2. Input Sanitization</h3>
        <p>Validating user credentials and ID bounds to prevent malformed records.</p>
        """,
        "embedded_html": """
        <h3>1. Embedded Security Token Validation</h3>
        <p>In RFID badge readers and secure microcontrollers (e.g. ATECC608A cryptographic co-processors), token IDs are validated in constant time to prevent timing side-channel attacks.</p>
        """,
        "refactor_html": """
        <p>Constant-time token validation helper:</p>
        <pre class="code-block" style="background:#0d1117; padding:16px; border-radius:8px; border:1px solid #30363d;">#include &lt;cstdint&gt;
#include &lt;string_view&gt;

// Constant-time string comparison (prevents timing side-channel attacks!)
bool constantTimeCompare(std::string_view a, std::string_view b) noexcept {
    if (a.size() != b.size()) return false;
    uint8_t diff = 0;
    for (size_t i = 0; i &lt; a.size(); ++i) {
        diff |= static_cast&lt;uint8_t&gt;(a[i] ^ b[i]);
    }
    return diff == 0;
}</pre>
        """,
        "quiz": [
            {
                "question": "What is a 'timing side-channel attack' against security token verification?",
                "options": ["An attack where an adversary measures how long string comparison takes to determine how many leading characters were correct, allowing brute-forcing passwords in linear time", "An attack that overclocks the microcontroller crystal", "An attack that changes the RTC calendar time", "An attack using WiFi jamming"],
                "correct": 0,
                "explanation": "Standard <code>strcmp</code> exits on the first mismatched character; measuring response latency reveals the number of correct characters."
            },
            {
                "question": "How does a constant-time comparison algorithm prevent timing attacks?",
                "options": ["It always compares every character in the buffer regardless of where mismatches occur, ensuring identical execution time for all inputs", "It pauses the CPU for 1 second", "It encrypts the string", "It generates random numbers"],
                "correct": 0,
                "explanation": "Constant-time comparisons iterate across all bytes using bitwise OR (<code>diff |= a[i] ^ b[i]</code>), producing flat, invariant execution timing."
            },
            {
                "question": "What is the risk of using 'cin >> buffer' into a fixed-size char buffer[16] array?",
                "options": ["Buffer overflow vulnerability if the user enters more than 15 characters, corrupting adjacent stack variables", "It slows down the CPU clock", "It allocates heap memory", "It triggers a compilation error"],
                "correct": 0,
                "explanation": "Unbounded stream extraction writes beyond array limits, corrupting stack memory and creating exploitable buffer overflows."
            },
            {
                "question": "Which modern C++ type provides safe, non-owning string inspection without allocating memory?",
                "options": ["std::string_view", "std::string", "char*", "std::stringstream"],
                "correct": 0,
                "explanation": "<code>std::string_view</code> provides a lightweight (pointer + size) view over character buffers with zero heap allocation."
            }
        ]
    }
]
