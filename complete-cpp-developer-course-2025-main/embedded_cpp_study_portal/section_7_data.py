#!/usr/bin/env python3
"""
Section 7 Project Definitions: Exceptions, Error Handling & Embedded Faults
Contains 9 comprehensive project definitions with deep-dive systems analysis,
hardware fault mechanics (HardFault/MemManage on ARM Cortex-M), AUTOSAR/MISRA rules,
and interactive quizzes.
"""

SECTION_7_PROJECTS = [
    {
        "id": "bug_fun",
        "name": "BugFun",
        "title": "Debugging Diagnostics, Fault Handlers & Defensive Assertions",
        "headline": "Syntax, Runtime, & Logic Bugs vs Microcontroller Hardware Faults (HardFault & MemManage)",
        "emb_class": "emb-high",
        "emb_badge": "⚡ Embedded Relevance: Critical",
        "tags": ["HardFault", "MemManage", "Stack Smashing", "Defensive Assertions", "static_assert", "MISRA C++"],
        "summary": "Exploring the taxonomy of bugs: syntax errors, runtime faults, and subtle logic errors. In bare-metal systems, logic errors often manifest as fatal ARM Cortex-M HardFaults, MemManage violations, or stack-smashing crashes. We explore hardware fault triggers and defensive compile-time/runtime assertion architectures.",
        "files": ["section_7/BugFun/BugFun/main.cpp"],
        "concepts_html": """
        <h3>1. Bug Classification Taxonomy</h3>
        <ul>
          <li><strong>Syntax Errors:</strong> Violations of the C++ grammar detected at compile-time (e.g. missing semicolons, type mismatches).</li>
          <li><strong>Runtime Errors:</strong> Program halts unexpectedly during execution (e.g. division by zero, null pointer dereferencing, uncaught exceptions).</li>
          <li><strong>Logic Errors:</strong> The program compiles and runs without crashing, but computes incorrect results (e.g. off-by-one loops, inverted boolean conditions).</li>
        </ul>

        <h3>2. Compiler Warning Diagnostics as First Line of Defense</h3>
        <p>Modern compilers can catch 90%+ of common logic bugs when configured with strict flags: <code>-Wall -Wextra -Wpedantic -Wshadow -Wconversion -Werror</code>. In embedded safety-critical systems, treating warnings as errors is mandatory.</p>
        """,
        "embedded_html": """
        <h3>1. How Bugs Manifest as Hardware Faults on ARM Cortex-M</h3>
        <p>In microcontrollers without an operating system, runtime bugs trigger hardware interrupt exceptions:</p>
        <ul>
          <li><strong>HardFault:</strong> Triggered by unaligned memory access (if configured), executing undefined instructions, or bus errors during vector fetch.</li>
          <li><strong>MemManage Fault:</strong> Triggered by Memory Protection Unit (MPU) rule violations (e.g. writing to read-only Flash or executing code from SRAM).</li>
          <li><strong>BusFault:</strong> Triggered by attempting to access non-existent memory addresses or unpowered peripheral registers over the AHB/APB bus.</li>
          <li><strong>UsageFault:</strong> Triggered by division by zero (when <code>DIV_0_TRP</code> is set in NVIC) or unaligned memory access.</li>
        </ul>

        <h3>2. Watchdog Timers (WDT) and Fail-Safe Recovery</h3>
        <p>Logic bugs like infinite loops or deadlock cause watchdog timer expiration. The hardware watchdog forcibly resets the microcontroller into a known safe state (e.g., de-energizing motor PWMs and logging the Program Counter register to non-volatile backup registers).</p>

        <div class="callout callout-warning">
          <h4>⚠️ MISRA C++:2008 Rule 0-1-1 & Rule 0-1-9</h4>
          <p>The code shall not contain unreachable code or dead execution paths. Defensive assertions must be implemented without introducing non-terminating loops in release builds.</p>
        </div>
        """,
        "refactor_html": """
        <p>Production firmware replaces generic runtime crashes with compile-time <code>static_assert</code> and custom hardware fault capture handlers:</p>
        <pre class="code-block" style="background:#0d1117; padding:16px; border-radius:8px; border:1px solid #30363d;">#include &lt;cstdint&gt;
#include &lt;type_traits&gt;

// 1. Compile-Time Invariant Verification
template &lt;typename T, size_t BufferSize&gt;
struct DmaRingBuffer {
    static_assert(BufferSize &gt; 0, "Buffer size must be non-zero");
    static_assert((BufferSize &amp; (BufferSize - 1)) == 0, "Buffer size must be a power of 2 for fast bitmask indexing");
    static_assert(std::is_trivially_copyable&lt;T&gt;::value, "DMA elements must be trivially copyable");
    
    T buffer[BufferSize];
    uint32_t head{0};
    uint32_t tail{0};
};

// 2. Hardware Fault Capture Handler (ARM Cortex-M Example)
struct FaultFrame {
    uint32_t r0, r1, r2, r3, r12, lr, pc, psr;
};

extern "C" void HardFault_Handler_C(FaultFrame* frame) {
    // Read NVIC Configurable Fault Status Register (CFSR)
    volatile uint32_t* const CFSR = reinterpret_cast&lt;volatile uint32_t*&gt;(0xE000ED28);
    uint32_t fault_reason = *CFSR;
    
    // Log crash telemetry (PC and LR) to persistent battery-backed backup SRAM
    // Safe shutdown: disable all actuators
    while (1) {
        // Halt or trigger controlled watchdog reset
    }
}</pre>
        """,
        "quiz": [
            {
                "question": "Which ARM Cortex-M hardware exception is triggered when firmware attempts to write to an unmapped peripheral memory address?",
                "options": ["MemManage Fault or BusFault", "Syntax Error Handler", "Segmentation Fault (SIGSEGV)", "Page Fault (Interrupt 14)"],
                "correct": 0,
                "explanation": "Attempting to access non-existent memory addresses across the AHB/APB system bus triggers a BusFault or MemManage Fault (if an MPU is configured). Microcontrollers lack MMU-based OS page fault tables."
            },
            {
                "question": "What is the primary advantage of static_assert over runtime assert() in embedded firmware?",
                "options": ["It evaluates conditions at compile time, incurring zero ROM/RAM footprint and preventing buggy binaries from flashing", "It generates larger binary files with more debug symbols", "It dynamically catches hardware brown-out resets", "It allows strings to be dynamically formatted at runtime"],
                "correct": 0,
                "explanation": "<code>static_assert</code> runs during compilation. If the condition is false, compilation fails immediately, ensuring zero runtime CPU cycle overhead and zero Flash memory bloat."
            },
            {
                "question": "Why are logic errors that cause infinite loops particularly hazardous in battery-powered IoT devices?",
                "options": ["They prevent CPU low-power sleep modes (WFI/WFE), causing rapid battery depletion and triggering Watchdog resets", "They automatically corrupt flash bootloader sectors", "They cause C++ templates to instantiate infinitely", "They double the microcontroller clock frequency"],
                "correct": 0,
                "explanation": "Infinite loops prevent the microcontroller from entering low-power sleep modes (Wait For Interrupt - WFI), causing current draw to stay at peak (e.g. 20mA vs 2uA), draining batteries in hours."
            },
            {
                "question": "Which compiler flag configuration converts all warnings into fatal compilation errors in safety-critical builds?",
                "options": ["-Wall -Wextra -Werror", "-O3 -fno-rtti", "-g -nostdlib", "-std=c++98 -fexceptions"],
                "correct": 0,
                "explanation": "<code>-Wall -Wextra</code> enables comprehensive compiler warnings, and <code>-Werror</code> forces the compiler to treat all warnings as errors, preventing problematic code from compiling."
            }
        ]
    },
    {
        "id": "custom_exceptions",
        "name": "CustomExceptions",
        "title": "Custom Exception Hierarchies vs Lightweight Tagged Enums",
        "headline": "std::exception Subclassing, Object Slicing Pitfalls & ROM Bloat in Embedded Firmware",
        "emb_class": "emb-high",
        "emb_badge": "⚡ Embedded Relevance: High",
        "tags": ["std::exception", "what()", "Object Slicing", "Code Bloat", "enum class", "AUTOSAR C++14"],
        "summary": "Building domain-specific exception hierarchies by inheriting from std::runtime_error and std::exception. We analyze how exception unwinding tables (.eh_frame / DWARF) add 15-40KB of Flash overhead, why dynamic exception allocation is hazardous in constrained SRAM, and how to refactor with zero-cost tagged error codes.",
        "files": [
            "section_7/CustomExceptions/CustomExceptions/main.cpp",
            "section_7/CustomExceptions/CustomExceptions/AngryCatException.h"
        ],
        "concepts_html": """
        <h3>1. Creating Custom Domain Exceptions</h3>
        <p>In standard C++, custom exception classes inherit from <code>std::runtime_error</code> (for runtime issues) or <code>std::logic_error</code> (for precondition violations), overriding the virtual <code>const char* what() const noexcept</code> method.</p>

        <div class="diagram-container">
          <h4>📐 Exception Inheritance Hierarchy UML</h4>
          <div class="uml-grid">
            <div class="uml-class-card">
              <div class="uml-class-header">
                <span class="uml-stereotype">&lt;&lt;std-base&gt;&gt;</span>
                <span class="uml-class-name">std::exception</span>
              </div>
              <div class="uml-section">
                <div class="uml-item public">+ what() : const char* [virtual]</div>
                <div class="uml-item public">+ ~exception() [virtual]</div>
              </div>
            </div>
            <div class="uml-class-card">
              <div class="uml-class-header">
                <span class="uml-stereotype">&lt;&lt;std-runtime&gt;&gt;</span>
                <span class="uml-class-name">std::runtime_error</span>
              </div>
              <div class="uml-section">
                <div class="uml-item public">+ runtime_error(msg: string)</div>
                <div class="uml-item public">+ what() : const char* [override]</div>
              </div>
            </div>
            <div class="uml-class-card">
              <div class="uml-class-header">
                <span class="uml-stereotype">&lt;&lt;custom-domain&gt;&gt;</span>
                <span class="uml-class-name">AngryCatException</span>
              </div>
              <div class="uml-section">
                <div class="uml-item public">+ AngryCatException()</div>
                <div class="uml-item public">+ AngryCatException(msg: string)</div>
                <div class="uml-item public">+ what() : const char* [override]</div>
              </div>
            </div>
          </div>
        </div>

        <h3>2. Object Slicing in Catch Handlers</h3>
        <p>Always catch exceptions by <strong>const reference</strong> (<code>catch (const std::exception& e)</code>). Catching by value (<code>catch (std::exception e)</code>) slices derived member variables away and destroys polymorphic <code>what()</code> dispatch.</p>
        """,
        "embedded_html": """
        <h3>1. The 15KB - 40KB Flash Penalty of C++ Exceptions</h3>
        <p>Enabling C++ exceptions (<code>-fexceptions</code>) forces GCC/Clang to emit:</p>
        <ul>
          <li><strong><code>.eh_frame</code> DWARF Unwind Tables:</strong> Metadata mapping instruction addresses to catch blocks.</li>
          <li><strong><code>__cxa_throw</code> & <code>__cxa_allocate_exception</code>:</strong> Runtime support code that dynamically allocates memory on an internal emergency heap when throwing.</li>
        </ul>
        <p>On a 32KB or 64KB Flash microcontroller (e.g. STM32F103, ATmega328P), exception runtime support can consume over <strong>50% of total available ROM</strong>.</p>

        <h3>2. Non-Deterministic Stack Unwinding in Real-Time ISRs</h3>
        <p>When an exception is thrown, the runtime traverses stack frames looking for a matching handler. The time required depends on call depth and active local objects, destroying deterministic hard real-time latency guarantees.</p>

        <div class="callout callout-danger">
          <h4>🚫 AUTOSAR Rule A15-0-1 & MISRA C++:2023 Rule 18.0.1</h4>
          <p>Exceptions shall not be used in safety-critical systems unless an upper bound on execution time can be strictly proven. In bare-metal and RTOS firmware, compile with <code>-fno-exceptions</code>.</p>
        </div>
        """,
        "refactor_html": """
        <p>Here is how modern embedded C++ implements zero-overhead, strongly typed error reporting without heap allocation or unwind tables:</p>
        <pre class="code-block" style="background:#0d1117; padding:16px; border-radius:8px; border:1px solid #30363d;">#include &lt;cstdint&gt;
#include &lt;string_view&gt;

// 1. Strongly-typed 1-byte error code (Zero RAM overhead)
enum class [[nodiscard]] SensorStatus : uint8_t {
    Ok = 0,
    Timeout,
    BusCollision,
    ChecksumMismatch,
    CriticalThresholdExceeded
};

// 2. Pure compile-time string converter (Stored in Flash ROM .rodata)
constexpr std::string_view to_string(SensorStatus status) noexcept {
    switch (status) {
        case SensorStatus::Ok:                        return "OK";
        case SensorStatus::Timeout:                   return "I2C Bus Timeout";
        case SensorStatus::BusCollision:              return "Arbitration Lost";
        case SensorStatus::ChecksumMismatch:          return "CRC8 Checksum Failure";
        case SensorStatus::CriticalThresholdExceeded: return "Critical Temperature Threshold Exceeded";
    }
    return "Unknown Error";
}

// 3. Deterministic return with [[nodiscard]] preventing unhandled errors
[[nodiscard]] SensorStatus readTemperature(int16_t& out_temp_celsius) noexcept {
    // Hardware reading logic...
    if (/* hardware timeout */ false) {
        return SensorStatus::Timeout;
    }
    out_temp_celsius = 42;
    return SensorStatus::Ok;
}</pre>
        """,
        "quiz": [
            {
                "question": "What is 'object slicing' when handling C++ exceptions?",
                "options": ["Catching a derived exception class by value instead of const reference, copying only the base class slice and losing derived data", "Allocating exceptions on the heap with new", "Dividing an exception object into multiple threads", "Splitting an exception across two catch blocks"],
                "correct": 0,
                "explanation": "Catching by value (<code>catch (std::exception e)</code>) invokes the copy constructor of the base class, discarding (slicing off) all derived class members and overriding behavior."
            },
            {
                "question": "Why is the C++ exception runtime support library (__cxa_throw) hazardous on small microcontrollers?",
                "options": ["It adds 15KB-40KB of Flash code bloat and relies on an internal heap allocation for exception objects", "It permanently disables CPU interrupts", "It alters the crystal oscillator clock frequency", "It prevents C++ classes from having member functions"],
                "correct": 0,
                "explanation": "<code>__cxa_throw</code> requires extensive DWARF stack-unwinding tables and dynamically allocates memory for the exception payload, posing severe ROM/RAM bloat risks."
            },
            {
                "question": "What does the C++ [[nodiscard]] attribute accomplish when applied to an error-returning function or enum?",
                "options": ["Causes the compiler to emit a warning/error if the caller ignores the returned status code", "Automatically throws a std::runtime_error on failure", "Forces the return value into the CPU cache line", "Allocates the return value in static BSS memory"],
                "correct": 0,
                "explanation": "<code>[[nodiscard]]</code> enforces that callers inspect the returned error status, preventing silent failures and unhandled error states at compile time."
            },
            {
                "question": "Which compiler flag disables C++ exception generation and stack unwinding tables entirely?",
                "options": ["-fno-exceptions", "-O2 -g", "-fno-rtti", "-nostdlib"],
                "correct": 0,
                "explanation": "The <code>-fno-exceptions</code> flag tells the compiler not to generate exception frames or unwinding support, drastically shrinking code size."
            }
        ]
    },
    {
        "id": "dog_fun",
        "name": "DogFun",
        "title": "Class Invariant Validation & Constructor Failure Patterns",
        "headline": "Constructor Invariant Enforcement vs Two-Phase Initialization in Microcontrollers",
        "emb_class": "emb-core",
        "emb_badge": "⚡ Embedded Relevance: Core",
        "tags": ["Invariants", "Constructor Failure", "Two-Phase Init", "noexcept", "RAII"],
        "summary": "Enforcing domain invariants through constructor validation and member validation methods. We examine the classic C++ dilemma of constructor failure (destructors do not run for incomplete objects) and contrast exception-based validation with deterministic Two-Phase Initialization (init()) and static factory methods.",
        "files": [
            "section_7/DogFun/DogFun/main.cpp",
            "section_7/DogFun/DogFun/Dog.h",
            "section_7/DogFun/DogFun/Dog.cpp"
        ],
        "concepts_html": """
        <h3>1. Object Invariants and Encapsulation</h3>
        <p>An invariant is a condition that must always be true for an object to be in a valid, functional state. Constructors establish invariants, and public mutator methods maintain them.</p>

        <h3>2. Constructor Failure Mechanics</h3>
        <p>In standard C++, if a constructor throws an exception, the object is considered <strong>never created</strong>. Crucially, the class destructor will <em>not</em> run. Any sub-objects already initialized will be destroyed in reverse order of declaration, but raw resource pointers owned directly by the class may leak.</p>
        """,
        "embedded_html": """
        <h3>1. The Two-Phase Initialization Pattern</h3>
        <p>In embedded systems compiled with <code>-fno-exceptions</code>, constructors cannot throw to report initialization failures (e.g. peripheral hardware unresponsive, DMA channel busy). Firmware designs use <strong>Two-Phase Initialization</strong>:</p>
        <ul>
          <li><strong>Phase 1 (Constructor):</strong> Lightweight construction; sets member variables to safe default/inert states (no hardware I/O).</li>
          <li><strong>Phase 2 (<code>init()</code> or <code>begin()</code>):</strong> Configures hardware registers, verifies I2C/SPI ACK, and returns a boolean or status code.</li>
        </ul>

        <h3>2. Static Factory Methods with <code>std::optional</code></h3>
        <p>Modern C++17 provides static factory creation methods that validate parameters and return <code>std::optional&lt;T&gt;</code> by value with zero heap allocation.</p>
        """,
        "refactor_html": """
        <p>Here is how embedded engineers design robust classes with deterministic factory initialization:</p>
        <pre class="code-block" style="background:#0d1117; padding:16px; border-radius:8px; border:1px solid #30363d;">#include &lt;cstdint&gt;
#include &lt;optional&gt;
#include &lt;string_view&gt;

class UartDriver {
private:
    uint32_t baud_rate_;
    uint8_t  port_id_;
    bool     is_initialized_{false};

    // Private constructor enforces creation through verified factory method
    constexpr UartDriver(uint8_t port, uint32_t baud) noexcept
        : baud_rate_(baud), port_id_(port) {}

public:
    // Factory method validating invariants before creating the object
    static std::optional&lt;UartDriver&gt; create(uint8_t port, uint32_t baud) noexcept {
        if (port &gt; 3) return std::nullopt; // Microcontroller has only UART 0-3
        if (baud &lt; 9600 || baud &gt; 921600) return std::nullopt; // Unsupported baud rate
        
        return UartDriver(port, baud);
    }

    [[nodiscard]] bool init_hardware() noexcept {
        // Configure MMIO registers (e.g., USART-&gt;BRR = ...)...
        is_initialized_ = true;
        return true;
    }
};</pre>
        """,
        "quiz": [
            {
                "question": "If a C++ constructor throws an exception before completing, what happens to the class destructor?",
                "options": ["The destructor is NOT called for the throwing object", "The destructor is immediately executed", "The destructor is deferred until program termination", "The destructor runs twice"],
                "correct": 0,
                "explanation": "In C++, an object is only considered fully constructed when its constructor finishes execution without throwing. If an exception occurs inside the constructor, the destructor will not execute."
            },
            {
                "question": "Why is the Two-Phase Initialization (init()) pattern widely used in embedded microcontrollers?",
                "options": ["Because hardware peripheral initialization can fail, and microcontrollers often compile with -fno-exceptions", "Because it enables multiple inheritance", "Because C++ constructors cannot accept arguments", "Because it increases compilation speed by 50%"],
                "correct": 0,
                "explanation": "In embedded systems where exceptions are disabled, constructors cannot fail safely. An explicit <code>init()</code> method allows returning a status code if hardware peripherals do not respond."
            },
            {
                "question": "What happens if a static global object's constructor attempts to write to peripheral registers before microcontroller clock tree initialization?",
                "options": ["A BusFault or HardFault occurs because peripheral bus clocks have not yet been enabled in Reset_Handler", "The compiler automatically fixes the clock tree", "The data is cached until bootup completes", "The CPU ignores the register writes safely"],
                "correct": 0,
                "explanation": "Attempting to access peripheral registers before enabling their respective APB/AHB bus clocks in the clock distribution tree generates a fatal hardware BusFault."
            },
            {
                "question": "How does returning std::optional<T> from a static factory method achieve zero-overhead object creation?",
                "options": ["It uses Return Value Optimization (RVO / copy elision) to construct the object directly into the caller's stack frame without heap allocations", "It allocates memory in the global BSS section", "It uses dynamic heap memory pools", "It converts objects into raw void pointers"],
                "correct": 0,
                "explanation": "Guaranteed copy elision (C++17) ensures that the factory method constructs <code>std::optional&lt;T&gt;</code> directly in the caller's stack location without any heap allocation or copy overhead."
            }
        ]
    },
    {
        "id": "exception_fun_1",
        "name": "ExceptionFun1",
        "title": "try-catch Mechanics & Stack Unwinding Latency",
        "headline": "Standard try-catch Blocks vs std::expected (C++23) for Predictable Real-Time Execution",
        "emb_class": "emb-high",
        "emb_badge": "⚡ Embedded Relevance: High",
        "tags": ["try-catch", "std::runtime_error", "Stack Unwinding", "std::expected", "Real-Time Jitter"],
        "summary": "Foundational try, throw, and catch mechanics in C++. We examine standard runtime exceptions (std::runtime_error), how stack unwinding destroys deterministic interrupt response times, and modern C++23 std::expected alternatives for high-reliability systems.",
        "files": ["section_7/ExceptionFun1/ExceptionFun1/main.cpp"],
        "concepts_html": """
        <h3>1. C++ Exception Flow Control</h3>
        <p>When an exception is thrown with <code>throw</code>, control immediately transfers out of the current block. The runtime searches backwards through active call frames until it finds an enclosing <code>try</code> block with a matching <code>catch</code> clause.</p>

        <h3>2. Standard Library Exception Hierarchy</h3>
        <p>All standard exceptions derive from <code>std::exception</code>. Key subclasses include <code>std::runtime_error</code> (unpredictable runtime failures) and <code>std::logic_error</code> (preventable programming bugs like out-of-range indices).</p>
        """,
        "embedded_html": """
        <h3>1. Real-Time Latency Jitter from Exception Unwinding</h3>
        <p>In hard real-time control systems (e.g. flight controllers, automotive brake-by-wire, inverter control loops), every cycle counts. An exception throw triggers non-deterministic table lookups across Flash unwind tables, causing latency jitter that can miss microsecond deadlines.</p>

        <h3>2. Modern Alternative: <code>std::expected&lt;T, E&gt;</code> (C++23)</h3>
        <p><code>std::expected&lt;T, E&gt;</code> represents either an expected value of type <code>T</code> or an error of type <code>E</code>. It provides monadic error chaining (<code>.and_then()</code>, <code>.transform()</code>) with <strong>100% deterministic time complexity and zero heap allocation</strong>.</p>
        """,
        "refactor_html": """
        <p>Here is how modern real-time systems handle operations that may fail using <code>std::expected</code> (or lightweight custom Result types):</p>
        <pre class="code-block" style="background:#0d1117; padding:16px; border-radius:8px; border:1px solid #30363d;">#include &lt;cstdint&gt;
#include &lt;string_view&gt;

// Embedded Result / Expected Implementation (C++17/20 Compatible)
template &lt;typename T, typename E&gt;
class Result {
    union {
        T value_;
        E error_;
    };
    bool has_value_;

public:
    constexpr Result(T val) : value_(val), has_value_(true) {}
    constexpr Result(E err) : error_(err), has_value_(false) {}
    ~Result() {}

    constexpr bool has_value() const noexcept { return has_value_; }
    constexpr const T&amp; value() const noexcept { return value_; }
    constexpr const E&amp; error() const noexcept { return error_; }
};

enum class AdcError : uint8_t { Timeout, OutOfRange, ReferenceVoltageLost };

Result&lt;uint16_t, AdcError&gt; readAdcChannel(uint8_t channel) noexcept {
    if (channel &gt; 15) return AdcError::OutOfRange;
    // Read hardware ADC register...
    return uint16_t(2048); // Success: 12-bit ADC mid-scale reading
}</pre>
        """,
        "quiz": [
            {
                "question": "What causes execution timing jitter when a C++ exception is thrown?",
                "options": ["The runtime must dynamically search stack frames and unwind active local variables across Flash DWARF tables", "The CPU frequency is temporarily throttled by hardware", "The operating system pauses all hardware interrupts", "The exception forces an immediate reboot"],
                "correct": 0,
                "explanation": "Stack unwinding involves traversing metadata tables in Flash to locate matching catch handlers and invoke destructors for in-scope local objects, introducing unpredictable cycle delays."
            },
            {
                "question": "What is the primary benefit of std::expected<T, E> over try-catch in embedded systems?",
                "options": ["It provides explicit, deterministic error handling without unwind tables or heap allocations", "It automatically repairs hardware defects", "It converts integers to floating-point numbers", "It allows functions to return multiple different types simultaneously"],
                "correct": 0,
                "explanation": "<code>std::expected</code> packages values and errors into a tagged union on the stack with deterministic $O(1)$ execution time and zero exception metadata bloat."
            },
            {
                "question": "Which header must be included to use std::runtime_error in standard C++?",
                "options": ["<stdexcept>", "<exception>", "<iostream>", "<error>"],
                "correct": 0,
                "explanation": "<code>std::runtime_error</code> and <code>std::logic_error</code> are defined in the standard <code>&lt;stdexcept&gt;</code> header."
            },
            {
                "question": "Can C++ exceptions be safely thrown from an Interrupt Service Routine (ISR)?",
                "options": ["No, throwing across ISR boundaries causes undefined behavior or std::terminate() because interrupt contexts lack user stack unwinding support", "Yes, catch blocks automatically catch ISR exceptions", "Yes, but only if the exception inherits from std::bad_alloc", "Yes, ISR exceptions are queued in the FreeRTOS scheduler"],
                "correct": 0,
                "explanation": "ISRs run in privileged handler mode with dedicated interrupt stack pointers (MSP). Throwing an exception from an ISR cannot unwind into thread mode and will trigger <code>std::terminate()</code>."
            }
        ]
    },
    {
        "id": "fuel_monitor_project",
        "name": "FuelMonitorProject",
        "title": "Safety-Critical Threshold Monitoring & Fail-Safe Latching",
        "headline": "Real-Time Sensor Monitoring, Emergency Thresholds & Hardware Fail-Safe States",
        "emb_class": "emb-high",
        "emb_badge": "⚡ Embedded Relevance: Critical",
        "tags": ["Safety Critical", "Fail-Safe", "Threshold Monitoring", "MISRA C++", "ADC"],
        "summary": "Building a safety-critical fuel level monitoring system with custom exception triggers. We analyze how embedded systems implement fail-safe latching, hardware interrupt watchdog trips, and safety state machines (e.g. ISO 26262 ASIL-D and IEC 61508 SIL-3).",
        "files": [
            "section_7/FuelMonitorProject/FuelMonitorProject/main.cpp",
            "section_7/FuelMonitorProject/FuelMonitorProject/FuelLevelCritical.h"
        ],
        "concepts_html": """
        <h3>1. Domain-Specific Alert Hierarchies</h3>
        <p>Critical systems define distinct exception/alert tiers (e.g., <code>FuelWarning</code> vs <code>FuelLevelCritical</code>). Each tier enforces appropriate escalation behavior.</p>

        <h3>2. Exception-Driven Control Flow Hazards</h3>
        <p>Using exceptions for ordinary control flow (e.g. routine sensor polling) is an anti-pattern. Exceptions should only be reserved for truly exceptional, unrecoverable system faults.</p>
        """,
        "embedded_html": """
        <h3>1. Safety State Machines (ISO 26262 & IEC 61508)</h3>
        <p>In safety-critical automotive/aerospace firmware, when a sensor reading breaches a critical safety envelope:</p>
        <ul>
          <li><strong>Fail-Safe State Transition:</strong> The system immediately switches to a predefined safe state (e.g., cutting fuel pump power, opening safety contactors, engaging mechanical brakes).</li>
          <li><strong>Fault Latching:</strong> The fault is latched in non-volatile memory and cannot be cleared until a full self-test or authorized service reset.</li>
        </ul>

        <h3>2. Hardware Analog Watchdog (AWD) in STM32 / NXP</h3>
        <p>Instead of software polling, modern microcontrollers provide hardware Analog Watchdogs on ADC channels that fire a dedicated hardware interrupt within <strong>sub-microsecond latency</strong> if voltage crosses high/low thresholds.</p>
        """,
        "refactor_html": """
        <p>Here is an embedded safety-critical monitor using a deterministic state machine with hysteresis:</p>
        <pre class="code-block" style="background:#0d1117; padding:16px; border-radius:8px; border:1px solid #30363d;">#include &lt;cstdint&gt;

enum class SafetyState : uint8_t {
    Nominal = 0,
    Warning,
    CriticalShutdown,
    FaultLatched
};

class FuelSafetyMonitor {
private:
    static constexpr uint16_t CRITICAL_THRESHOLD = 50;  // 5.0 Liters
    static constexpr uint16_t WARNING_THRESHOLD  = 150; // 15.0 Liters
    static constexpr uint16_t HYSTERESIS         = 10;  // Prevents state fluttering
    
    SafetyState state_{SafetyState::Nominal};
    bool latch_engaged_{false};

public:
    SafetyState update(uint16_t raw_sensor_level) noexcept {
        if (latch_engaged_) return SafetyState::FaultLatched;

        if (raw_sensor_level &lt;= CRITICAL_THRESHOLD) {
            state_ = SafetyState::CriticalShutdown;
            latch_engaged_ = true;
            trigger_hardware_shutdown();
        } else if (raw_sensor_level &lt;= WARNING_THRESHOLD) {
            state_ = SafetyState::Warning;
        } else if (raw_sensor_level &gt; (WARNING_THRESHOLD + HYSTERESIS)) {
            state_ = SafetyState::Nominal;
        }
        return state_;
    }

private:
    void trigger_hardware_shutdown() noexcept {
        // Assert GPIO pin to trip physical safety relay
    }
};</pre>
        """,
        "quiz": [
            {
                "question": "What is 'hysteresis' and why is it essential in embedded threshold monitoring?",
                "options": ["A tolerance band that prevents rapid, oscillating state changes when a noisy sensor signal fluctuates near a threshold", "A technique to accelerate floating-point arithmetic", "A method for encrypting sensor telemetry over CAN bus", "A software pattern that forces memory allocation onto the heap"],
                "correct": 0,
                "explanation": "Hysteresis introduces different switching thresholds for rising vs falling signals, preventing noisy analog sensor inputs from rapidly toggling actuators on and off."
            },
            {
                "question": "Why is using C++ exceptions for routine, expected conditions (e.g. low fuel warning) considered bad practice?",
                "options": ["Exceptions incur massive performance penalties during unwinding and obscure normal control flow logic", "Exceptions cannot be caught more than once", "Exceptions automatically erase flash memory", "Exceptions disable the microcontroller ADC peripheral"],
                "correct": 0,
                "explanation": "Exceptions should represent exceptional/catastrophic conditions. Using them for regular state transitions causes high stack unwinding overhead and makes code harder to verify."
            },
            {
                "question": "What is the purpose of an Analog Watchdog (AWD) peripheral on microcontrollers like STM32?",
                "options": ["It continuously monitors ADC conversion values in hardware and triggers an instant interrupt if thresholds are violated", "It resets the microcontroller if the real-time clock loses power", "It prevents battery overcharging through USB", "It simulates analog signals for unit testing"],
                "correct": 0,
                "explanation": "The hardware Analog Watchdog checks converted ADC values against high/low register limits in hardware, generating an immediate interrupt without CPU polling overhead."
            },
            {
                "question": "What does a 'fail-safe state' guarantee according to functional safety standards (ISO 26262)?",
                "options": ["The system transitions to a predetermined state that minimizes risk of harm upon critical component failure", "The system attempts to reboot continuously until hardware fixes itself", "The system ignores sensor failures and continues full power operation", "The system executes all pending dynamic memory allocations"],
                "correct": 0,
                "explanation": "A fail-safe state ensures that when an unrecoverable fault occurs, all actuators and power stages default to their safest possible configuration (e.g. de-energized)."
            }
        ]
    },
    {
        "id": "logic_error_fun",
        "name": "LogicErrorFun",
        "title": "std::logic_error, Preconditions & Array Bounds Safety",
        "headline": "std::out_of_range vs Compile-Time Bounded Ranges in Memory-Constrained Systems",
        "emb_class": "emb-core",
        "emb_badge": "⚡ Embedded Relevance: Core",
        "tags": ["std::logic_error", "std::out_of_range", "Bounds Checking", "Buffer Overflow", "static_assert"],
        "summary": "Analyzing std::logic_error and std::out_of_range exceptions in C++. We explore how out-of-bounds memory accesses corrupt adjacent variables or trigger MPU faults in bare-metal systems, and design zero-overhead compile-time bounded types.",
        "files": ["section_7/LogicErrorFun/LogicErrorFun/main.cpp"],
        "concepts_html": """
        <h3>1. Logic Errors vs Runtime Errors</h3>
        <p><code>std::logic_error</code> indicates violations of logical preconditions that could theoretically be detected by examining the program source code (e.g. passing an index $\\ge$ size to <code>std::vector::at()</code>).</p>

        <h3>2. Subclasses of <code>std::logic_error</code></h3>
        <ul>
          <li><code>std::out_of_range</code>: Accessing elements outside valid container boundaries.</li>
          <li><code>std::invalid_argument</code>: Passing an improper argument to a function.</li>
          <li><code>std::length_error</code>: Attempting to create an object exceeding <code>max_size</code>.</li>
        </ul>
        """,
        "embedded_html": """
        <h3>1. Out-of-Bounds Memory Corruption in Bare-Metal Systems</h3>
        <p>In standard C/C++, raw arrays (<code>arr[i]</code>) do not perform bounds checking. Writing past an array in embedded SRAM typically clobbers:</p>
        <ul>
          <li>Adjacent global or local variables.</li>
          <li>The function's Return Address on the stack, causing unpredictable jumps and HardFaults.</li>
          <li>Interrupt Vector Tables in SRAM (triggering catastrophic execution hijacking).</li>
        </ul>

        <h3>2. Bounded Index Types (Zero-Cost Safety)</h3>
        <p>Instead of throwing <code>std::out_of_range</code> at runtime, embedded engineers use clamped/saturating integer arithmetic or strongly-typed bounded index wrappers.</p>
        """,
        "refactor_html": """
        <p>Here is a compile-time bounded array index that prevents out-of-bounds bugs at compile time:</p>
        <pre class="code-block" style="background:#0d1117; padding:16px; border-radius:8px; border:1px solid #30363d;">#include &lt;cstdint&gt;
#include &lt;cstddef&gt;
#include &lt;array&gt;

template &lt;typename T, size_t N&gt;
class SafeArray {
    std::array&lt;T, N&gt; data_{};

public:
    // 1. Clamped access: Guarantees no out-of-bounds without throwing
    constexpr const T&amp; at_clamped(size_t index) const noexcept {
        if (index &gt;= N) index = N - 1;
        return data_[index];
    }

    // 2. Compile-time checked access for constant indices
    template &lt;size_t Index&gt;
    constexpr const T&amp; get() const noexcept {
        static_assert(Index &lt; N, "Array index is out of compile-time bounds!");
        return data_[Index];
    }
};</pre>
        """,
        "quiz": [
            {
                "question": "What is the key conceptual difference between std::logic_error and std::runtime_error?",
                "options": ["logic_error represents preventable design bugs in code logic, while runtime_error represents unpredictable external failures", "logic_error only works with integers", "runtime_error is evaluated at compile time", "logic_error cannot be caught by a base class reference"],
                "correct": 0,
                "explanation": "<code>std::logic_error</code> reflects flaws in the program's internal reasoning (like violating function preconditions), whereas <code>std::runtime_error</code> reflects environment/hardware conditions outside the program's control."
            },
            {
                "question": "What happens in C++ if you access an invalid index using the subscript operator (arr[index]) on a raw array?",
                "options": ["Undefined Behavior (UB) occurs; memory is read or overwritten without any bounds check", "A std::out_of_range exception is automatically thrown", "The program safely returns null", "The array dynamically expands to fit the index"],
                "correct": 0,
                "explanation": "Raw array subscripting (<code>[]</code>) in C and C++ performs direct pointer arithmetic with zero bounds checking. Accessing invalid indices causes undefined behavior and potential memory corruption."
            },
            {
                "question": "Which method on std::vector performs bounds checking and throws std::out_of_range on invalid access?",
                "options": [".at(index)", "[index]", ".front()", ".data()"],
                "correct": 0,
                "explanation": "<code>std::vector::at()</code> checks whether the index is within the container bounds and throws <code>std::out_of_range</code> if it is not."
            },
            {
                "question": "How does saturating/clamping arithmetic protect embedded sensor arrays from crashing?",
                "options": ["It clamps out-of-range index values to the nearest valid min/max boundary instead of overflowing", "It deletes corrupted elements from flash", "It restarts the microcontroller on every access", "It encrypts the index in CPU registers"],
                "correct": 0,
                "explanation": "Clamping ensures that invalid indices or arithmetic results saturate at the nearest valid boundary (e.g. <code>max_index</code>), preventing out-of-bounds buffer corruptions."
            }
        ]
    },
    {
        "id": "month_name_project",
        "name": "MonthNameProject",
        "title": "Lookup Table Architectures & ROM Optimization",
        "headline": "Range Validation, Branch Elimination & constexpr Flash Lookup Tables (.rodata)",
        "emb_class": "emb-core",
        "emb_badge": "⚡ Embedded Relevance: Core",
        "tags": ["Lookup Tables", "constexpr", "ROM Optimization", "string_view", ".rodata"],
        "summary": "Validating user input ranges and mapping integer IDs to string representations. We contrast exception-based validation with high-speed constexpr Flash lookup tables (.rodata) that eliminate branch misprediction latency and dynamic string allocations.",
        "files": ["section_7/MonthNameProject/MonthNameProject/main.cpp"],
        "concepts_html": """
        <h3>1. Value-to-String Mapping Strategies</h3>
        <p>Mapping enum/integer IDs to human-readable strings is a ubiquitous programming task. Naive implementations use long chains of <code>if-else</code> or <code>switch-case</code> statements that increase cyclomatic complexity.</p>

        <h3>2. Lookup Tables (LUTs)</h3>
        <p>A Lookup Table converts a complex branch tree into a direct $O(1)$ array indexing operation, vastly improving code clarity and execution predictability.</p>
        """,
        "embedded_html": """
        <h3>1. Placing LUTs in Flash ROM (<code>.rodata</code> Section)</h3>
        <p>In microcontrollers, RAM is severely constrained (e.g. 8KB to 64KB), while Flash is larger (e.g. 64KB to 1MB). By qualifying lookup tables with <code>static constexpr std::string_view</code>, table pointers and string literals are stored directly in <strong>Flash ROM (<code>.rodata</code>)</strong>, consuming <strong>0 bytes of SRAM</strong>.</p>

        <h3>2. Eliminating Branch Misprediction Latency</h3>
        <p>Direct array indexing eliminates branch instructions entirely, preventing pipeline flushes on high-performance pipelined microcontrollers (like ARM Cortex-M7 with branch prediction).</p>
        """,
        "refactor_html": """
        <p>Here is an optimized zero-SRAM, zero-allocation lookup table implementation:</p>
        <pre class="code-block" style="background:#0d1117; padding:16px; border-radius:8px; border:1px solid #30363d;">#include &lt;cstdint&gt;
#include &lt;string_view&gt;
#include &lt;array&gt;

class CalendarLookup {
public:
    // Stored 100% in Flash ROM (.rodata); Zero RAM allocated
    static constexpr std::array&lt;std::string_view, 12&gt; MONTH_NAMES = {
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    };

    // O(1) branchless lookup with safe boundary fallback
    static constexpr std::string_view get_month(uint8_t month_1_to_12) noexcept {
        if (month_1_to_12 &lt; 1 || month_1_to_12 &gt; 12) {
            return "Invalid Month";
        }
        return MONTH_NAMES[month_1_to_12 - 1];
    }
};</pre>
        """,
        "quiz": [
            {
                "question": "Where are static constexpr lookup tables placed in an embedded microcontroller's memory map?",
                "options": ["In Flash ROM within the .rodata section, consuming zero bytes of SRAM", "In the heap segment", "In the CPU register bank", "In the battery-backed RTC SRAM"],
                "correct": 0,
                "explanation": "<code>static constexpr</code> data is immutable and placed by the linker directly into the read-only data section (<code>.rodata</code>) located in Flash memory, preserving precious SRAM."
            },
            {
                "question": "Why is std::string_view preferred over std::string for lookup table string literals?",
                "options": ["std::string_view is a non-owning pointer + length that requires zero dynamic heap allocations", "std::string_view compresses text automatically", "std::string_view can only hold numeric values", "std::string_view allocates memory on the stack frame"],
                "correct": 0,
                "explanation": "<code>std::string_view</code> stores a pointer to constant string data in Flash ROM along with its length (2 words total), requiring zero dynamic heap memory allocation."
            },
            {
                "question": "What is the time complexity of looking up a value in an index-based Lookup Table?",
                "options": ["O(1) constant time", "O(N) linear time", "O(log N) logarithmic time", "O(N^2) quadratic time"],
                "correct": 0,
                "explanation": "Direct array index lookup computes the target address via base + offset pointer arithmetic, executing in $O(1)$ deterministic constant time."
            },
            {
                "question": "What happens if a switch statement without jump table optimization is executed on a pipelined processor?",
                "options": ["Sequential condition branches can suffer multiple branch mispredictions, stalling the instruction pipeline", "The compiler converts the CPU to 64-bit mode", "The switch statement throws a std::bad_cast exception", "The instruction cache is completely purged"],
                "correct": 0,
                "explanation": "Chained condition branches force the CPU pipeline to predict branching paths; frequent mispredictions flush the pipeline and waste clock cycles."
            }
        ]
    },
    {
        "id": "person_fun",
        "name": "PersonFun",
        "title": "Exception Safety in Constructors & Memory Leak Prevention",
        "headline": "Constructor Invariants, Destructor Guarantees & Partial Initialization Leaks",
        "emb_class": "emb-high",
        "emb_badge": "⚡ Embedded Relevance: High",
        "tags": ["Constructor Exceptions", "Resource Leak", "noexcept", "RAII", "Invariants"],
        "summary": "Deep dive into throwing exceptions from class constructors. We examine the classic C++ memory leak hazard when initializing multiple heap members in a constructor, analyze compiler destructor guarantees, and implement safe noexcept construction patterns.",
        "files": [
            "section_7/PersonFun/PersonFun/main.cpp",
            "section_7/PersonFun/PersonFun/Person.h",
            "section_7/PersonFun/PersonFun/Person.cpp"
        ],
        "concepts_html": """
        <h3>1. The Partial Construction Problem</h3>
        <p>Consider a class that allocates two raw pointer resources in its constructor:</p>
        <pre class="code-block">MyClass::MyClass() {
    ptr1 = new ResourceA(); // Succeeded
    ptr2 = new ResourceB(); // THROWS EXCEPTION!
}</pre>
        <p>Because the constructor never finished, <code>~MyClass()</code> will <strong>never be called</strong>. <code>ptr1</code> is leaked forever! This is why raw pointers in constructors violate basic exception safety.</p>

        <h3>2. Solving via RAII Smart Wrappers</h3>
        <p>Using <code>std::unique_ptr</code> for member variables guarantees that if a later initialization step throws, already initialized member smart pointers have their destructors called automatically.</p>
        """,
        "embedded_html": """
        <h3>1. noexcept Constructor Guarantees in Firmware</h3>
        <p>In embedded firmware, declaring constructors <code>noexcept</code> tells the compiler that no unwind tables are needed, enabling compiler optimizations like vector reallocation via move instead of copy.</p>

        <h3>2. Placement-New and In-Place Static Construction</h3>
        <p>For systems that cannot afford dynamic allocation, placement-new allows constructing an object inside a statically allocated byte buffer (<code>alignas(T) std::byte buffer[sizeof(T)]</code>) with deterministic placement.</p>
        """,
        "refactor_html": """
        <p>Here is how to design exception-safe classes with guaranteed cleanup and noexcept construction:</p>
        <pre class="code-block" style="background:#0d1117; padding:16px; border-radius:8px; border:1px solid #30363d;">#include &lt;cstdint&gt;
#include &lt;string_view&gt;
#include &lt;array&gt;

class FirmwareNode {
private:
    std::array&lt;char, 16&gt; node_name_{};
    uint8_t node_id_{0};

public:
    // Fully noexcept constructor; zero possibility of memory leak or throwing
    constexpr FirmwareNode(uint8_t id, std::string_view name) noexcept : node_id_(id) {
        size_t len = name.size() &lt; 15 ? name.size() : 15;
        for (size_t i = 0; i &lt; len; ++i) {
            node_name_[i] = name[i];
        }
        node_name_[len] = '\\0';
    }

    constexpr uint8_t get_id() const noexcept { return node_id_; }
    constexpr std::string_view get_name() const noexcept { return node_name_.data(); }
};</pre>
        """,
        "quiz": [
            {
                "question": "If a constructor allocates Resource 1 with raw new, and then Resource 2 throws std::bad_alloc, what happens to Resource 1?",
                "options": ["Resource 1 is leaked because the class destructor is never called for an object that failed construction", "Resource 1 is automatically garbage collected", "The runtime calls the destructor on half-built objects", "The compiler rewires the pointer to null"],
                "correct": 0,
                "explanation": "Because the constructor did not finish, the object was never fully created, so its destructor does not execute. Any raw resources allocated before the throw are leaked unless managed by RAII smart wrappers."
            },
            {
                "question": "What is the primary benefit of declaring constructors and methods noexcept in C++?",
                "options": ["It signals that the function will never throw, allowing the compiler to omit exception unwinding tables and perform optimal move semantics", "It makes the function run in privileged CPU mode", "It converts the class into a template", "It forces parameters to be passed by reference"],
                "correct": 0,
                "explanation": "<code>noexcept</code> promises that no exceptions will escape. This removes unwind code generation overhead and allows STL containers (like <code>std::vector</code>) to safely use fast move operations."
            },
            {
                "question": "How does RAII (std::unique_ptr) solve constructor resource leaks?",
                "options": ["Member sub-objects that have already completed construction have their individual destructors executed automatically when an exception is thrown", "It converts raw pointers into integers", "It allocates memory in battery-backed SRAM", "It prevents constructors from taking arguments"],
                "correct": 0,
                "explanation": "C++ guarantees that all fully constructed sub-objects and base classes will have their destructors called if a constructor later throws. <code>std::unique_ptr</code> destructors automatically free their held pointers."
            },
            {
                "question": "What happens if a function marked noexcept throws an exception?",
                "options": ["std::terminate() is immediately invoked, halting the program", "The exception is converted into a compiler warning", "The function retries execution from the beginning", "The catch block in main catches it as a generic exception"],
                "correct": 0,
                "explanation": "If an exception escapes a <code>noexcept</code> function, the runtime calls <code>std::terminate()</code> immediately without unwinding remaining stack frames."
            }
        ]
    },
    {
        "id": "rethrow_fun_1",
        "name": "RethrowFun1",
        "title": "Exception Propagation & Fault Escalation Hierarchies",
        "headline": "Nested try-catch, Exception Slicing during Rethrow & RTOS Fault Escalation",
        "emb_class": "emb-high",
        "emb_badge": "⚡ Embedded Relevance: High",
        "tags": ["throw;", "Exception Slicing", "RTOS", "Fault Escalation", "NVRAM Logging"],
        "summary": "Examining multi-layered exception handling and exception rethrowing with throw;. We contrast standard C++ exception propagation with real-time RTOS fault escalation architectures, where task-level errors are escalated to supervisors, safe mode, or persistent NVRAM black-box logging.",
        "files": ["section_7/RethrowFun1/RethrowFun1/main.cpp"],
        "concepts_html": """
        <h3>1. Correct Rethrowing Syntax (<code>throw;</code> vs <code>throw e;</code>)</h3>
        <p>When rethrowing an active exception, always use <code>throw;</code> with no operand. Using <code>throw e;</code> constructs a <strong>new</strong> exception copy of type <code>e</code>, causing object slicing if <code>e</code> is a base class reference.</p>

        <h3>2. Multi-Tier Error Propagation</h3>
        <p>A low-level function catches an error to perform localized cleanup (e.g. closing a file or releasing a lock), and then rethrows it to let higher-level orchestration logic handle user notification or system recovery.</p>
        """,
        "embedded_html": """
        <h3>1. RTOS Hierarchical Fault Escalation</h3>
        <p>In multi-tasking Real-Time Operating Systems (e.g. FreeRTOS, Zephyr), errors escalate through formal levels:</p>
        <ul>
          <li><strong>Level 1 (Task Level):</strong> Retry transient peripheral read (e.g. I2C retry).</li>
          <li><strong>Level 2 (Supervisor Level):</strong> Restart malfunctioning task and re-initialize peripheral driver.</li>
          <li><strong>Level 3 (System Level):</strong> Log error telemetry to Non-Volatile Backup SRAM (NVRAM) and trigger a controlled software reset via NVIC.</li>
        </ul>

        <h3>2. Non-Volatile Black-Box Logging</h3>
        <p>Safety-critical firmware maintains a circular crash log in battery-backed SRAM or EEPROM to preserve stack frames and fault status registers across watchdog resets for forensic diagnosis.</p>
        """,
        "refactor_html": """
        <p>Here is an embedded multi-tier fault escalation and telemetry logging architecture:</p>
        <pre class="code-block" style="background:#0d1117; padding:16px; border-radius:8px; border:1px solid #30363d;">#include &lt;cstdint&gt;

enum class EscalationLevel : uint8_t {
    TaskHandled = 0,
    TaskRestart,
    SystemResetSafeMode
};

struct FaultLogEntry {
    uint32_t timestamp_ms;
    uint16_t error_code;
    uint8_t  task_id;
    uint8_t  severity;
};

class SystemFaultSupervisor {
public:
    static EscalationLevel record_fault(uint8_t task_id, uint16_t error_code, uint8_t retries_exhausted) noexcept {
        // 1. Write to Non-Volatile Backup SRAM
        log_to_nvram({/* timestamp */ 123456, error_code, task_id, retries_exhausted});

        // 2. Determine escalation tier
        if (retries_exhausted &lt; 3) {
            return EscalationLevel::TaskHandled;
        } else if (retries_exhausted &lt; 5) {
            return EscalationLevel::TaskRestart;
        } else {
            // Escalate to controlled MCU Reset
            trigger_system_reset();
            return EscalationLevel::SystemResetSafeMode;
        }
    }

private:
    static void log_to_nvram(const FaultLogEntry&amp; entry) noexcept {
        // Write to battery-backed register bank
    }
    static void trigger_system_reset() noexcept {
        // NVIC_SystemReset(); (ARM Cortex-M CMSIS call)
    }
};</pre>
        """,
        "quiz": [
            {
                "question": "What is the critical difference between 'throw;' and 'throw e;' in a C++ catch block?",
                "options": ["'throw;' rethrows the exact original polymorphic exception object, while 'throw e;' makes a copy and causes object slicing", "'throw;' creates a new memory allocation", "'throw e;' is faster because it bypasses the compiler", "'throw;' cannot be used inside nested catch blocks"],
                "correct": 0,
                "explanation": "<code>throw;</code> re-raises the active exception retaining its dynamic polymorphic type. <code>throw e;</code> copies the base-type slice, slicing away any derived class data and custom <code>what()</code> logic."
            },
            {
                "question": "In an RTOS architecture, what is the primary role of a Supervisor Task?",
                "options": ["To monitor worker task heartbeats, handle unrecoverable task errors, and execute restart or fail-safe protocols", "To compile C++ code at runtime", "To allocate dynamic heap memory for all threads", "To format SD card file systems on boot"],
                "correct": 0,
                "explanation": "Supervisor tasks monitor thread health (via watchdog check-ins) and coordinate fault recovery (such as restarting crashed worker tasks or commanding safe shutdowns)."
            },
            {
                "question": "Why is Non-Volatile RAM (NVRAM / Backup SRAM) preferred over regular SRAM for crash telemetry logging?",
                "options": ["NVRAM retains its data across CPU resets and power loss, allowing crash diagnostics after system reboot", "NVRAM executes code 10x faster than cache", "NVRAM has infinite storage capacity", "NVRAM does not require address lines"],
                "correct": 0,
                "explanation": "Backup SRAM or battery-backed registers maintain state through hardware watchdog resets and power cycles, enabling post-mortem crash analysis."
            },
            {
                "question": "Which ARM Cortex-M CMSIS function initiates a software-commanded system reset?",
                "options": ["NVIC_SystemReset()", "CPU_Halt()", "WDT_Clear()", "OS_Exit()"],
                "correct": 0,
                "explanation": "<code>NVIC_SystemReset()</code> sets the <code>SYSRESETREQ</code> bit in the Application Interrupt and Reset Control Register (AIRCR), triggering an immediate hardware reset."
            }
        ]
    }
]
