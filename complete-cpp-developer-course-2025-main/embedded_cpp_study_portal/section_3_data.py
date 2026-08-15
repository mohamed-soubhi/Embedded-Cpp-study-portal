#!/usr/bin/env python3
"""
Section 3 Project Definitions: Control Flow, Branching & Loop Mechanics
Contains 13 comprehensive project definitions covering if/else branching,
switch jump tables (TBB/TBH), while/do-while loops, break/continue,
and PRNG vs True Hardware Random Number Generators (TRNG / RNG peripherals).
"""

SECTION_3_PROJECTS = [
    {
        "id": "control_statements_intro",
        "name": "ControlStatementsIntro",
        "title": "Control Flow, Sequential Execution & Branch Instructions",
        "headline": "Sequential Execution, Conditional Branches & ARM Cortex-M Pipeline Behavior",
        "emb_class": "emb-high",
        "emb_badge": "⚡ Embedded Relevance: Critical",
        "tags": ["Control Flow", "Branches", "Pipeline Flushes", "Branch Prediction", "BNE / BEQ"],
        "summary": "Exploring the foundations of programmatic control flow. We analyze sequential instruction fetching, conditional branching (BNE, BEQ) in assembly, how branch mispredictions flush CPU execution pipelines, and techniques for writing branch-efficient embedded logic.",
        "files": ["section_3/ControlStatementsIntro/ControlStatementsIntro/main.cpp"],
        "concepts_html": """
        <h3>1. Sequential Execution vs Control Flow Modification</h3>
        <p>By default, the CPU Program Counter (PC) increments sequentially by 2 or 4 bytes after each instruction fetch. Control statements (<code>if</code>, <code>while</code>, <code>for</code>, <code>switch</code>) modify the PC to jump to non-consecutive memory addresses.</p>

        <h3>2. Conditional Branch Assembly Instructions</h3>
        <p>On ARM processors, comparisons set condition flags (N, Z, C, V) in the APSR register; conditional branch instructions (<code>BEQ</code>, <code>BNE</code>, <code>BGT</code>, <code>BLT</code>) jump based on these flag states.</p>
        """,
        "embedded_html": """
        <h3>1. CPU Pipeline Flushes & Branch Penalties</h3>
        <p>Modern microcontrollers (such as ARM Cortex-M7 with a 6-stage superscalar pipeline) fetch instructions ahead of execution. When a conditional branch is taken unpredictably, the prefetched pipeline instructions must be discarded (flushed), wasting <strong>3 to 7 clock cycles</strong>.</p>
        """,
        "refactor_html": """
        <p>Branch-predictable condition ordering (most likely path first):</p>
        <pre class="code-block" style="background:#0d1117; padding:16px; border-radius:8px; border:1px solid #30363d;">#include &lt;cstdint&gt;

// Optimize for the 99.9% common case (heartbeat healthy)
void evaluateHeartbeat(uint32_t missed_ticks) noexcept {
    if (missed_ticks == 0) [[likely]] {
        // Fast path: CPU pipeline runs straight through!
        return;
    }
    
    // Rare fault path
    triggerSafetyShutdown();
}</pre>
        """,
        "quiz": [
            {
                "question": "What happens inside a pipelined CPU when an unpredictable conditional branch is taken?",
                "options": ["The instruction pipeline is flushed, discarding prefetched instructions and incurring a latency penalty of several clock cycles", "The CPU switches to 64-bit mode", "The stack pointer is reset to zero", "The compiler re-runs in the background"],
                "correct": 0,
                "explanation": "Branching to a non-consecutive address invalidates instructions already loaded into the pipeline stages, forcing a pipeline reload (stall)."
            },
            {
                "question": "Which C++20 attributes allow developers to hint to the compiler which branch is most likely to execute?",
                "options": ["[[likely]] and [[unlikely]]", "[[fast]] and [[slow]]", "[[inline]] and [[noinline]]", "[[pure]] and [[const]]"],
                "correct": 0,
                "explanation": "<code>[[likely]]</code> and <code>[[unlikely]]</code> (C++20) guide the compiler's code layout to align the most frequent path for sequential execution."
            },
            {
                "question": "Which CPU register stores the memory address of the next instruction to be fetched and executed?",
                "options": ["Program Counter (PC / R15)", "Link Register (LR / R14)", "Stack Pointer (SP / R13)", "Status Register (PSR)"],
                "correct": 0,
                "explanation": "The Program Counter (PC / R15 on ARM) points to the memory address of the instruction being fetched."
            },
            {
                "question": "How does branchless programming help mitigate branch penalty stalls?",
                "options": ["It converts conditional logic into arithmetic operations (e.g. bitmasks and multiplexing) that execute in straight-line assembly with zero branches", "It removes all functions from the codebase", "It runs code in ROM only", "It disables the ALU"],
                "correct": 0,
                "explanation": "Branchless code eliminates jump instructions entirely, keeping the pipeline saturated and timing invariant."
            }
        ]
    },
    {
        "id": "selection_fun",
        "name": "SelectionFun",
        "title": "If-Else Branching & Boolean Decision Trees",
        "headline": "Nested if/else Decision Trees, Inverted Guards & Early Return Idioms",
        "emb_class": "emb-core",
        "emb_badge": "⚡ Embedded Relevance: Core",
        "tags": ["if/else", "Decision Trees", "Guard Clauses", "Early Return", "Clean Code"],
        "summary": "Exploring if/else selection statements and multi-branch decision trees. We contrast deeply nested if-else ladders ('Arrow Anti-Pattern') with clean Guard Clauses and Early Returns, analyzing their impact on stack frames and code readability.",
        "files": ["section_3/SelectionFun/SelectionFun/main.cpp"],
        "concepts_html": """
        <h3>1. Multi-Way Selection Trees</h3>
        <p>Nested <code>if-else</code> constructs evaluate conditions in top-down sequential order, executing the first block whose condition is true.</p>

        <h3>2. Guard Clauses & Early Returns</h3>
        <p>Inverting error checks to exit early (Guard Clauses) flattens nested code, reduces cyclomatic complexity, and makes execution paths immediately visible.</p>
        """,
        "embedded_html": """
        <h3>1. Reducing Cyclomatic Complexity</h3>
        <p>Automotive safety standards (ISO 26262 / MISRA) enforce strict limits on <strong>Cyclomatic Complexity (typically $\\le 10$)</strong> per function. Using guard clauses keeps complexity low and ensures all error paths are testable.</p>
        """,
        "refactor_html": """
        <p>Refactoring nested if-else ladders into clean early return guards:</p>
        <pre class="code-block" style="background:#0d1117; padding:16px; border-radius:8px; border:1px solid #30363d;">#include &lt;cstdint&gt;

enum class ValveState : uint8_t { Closed = 0, Open, Fault };

ValveState evaluatePressureSensor(uint32_t psi, bool is_powered) noexcept {
    // 1. Guard against hardware power failure
    if (!is_powered) return ValveState::Fault;
    
    // 2. Guard against over-pressure emergency
    if (psi &gt; 150) return ValveState::Open;
    
    // 3. Normal operating state
    return ValveState::Closed;
}</pre>
        """,
        "quiz": [
            {
                "question": "What is 'Cyclomatic Complexity' in software engineering?",
                "options": ["A quantitative metric measuring the number of linearly independent paths through a function's source code", "The clock speed of the CPU in GHz", "The amount of heap memory allocated by a class", "The number of lines in a header file"],
                "correct": 0,
                "explanation": "Cyclomatic complexity counts decision points (if, while, for, case), measuring code complexity and required unit test paths."
            },
            {
                "question": "What is the primary advantage of using 'Guard Clauses' with early returns over deeply nested if-else blocks?",
                "options": ["They eliminate deep nesting (the 'Arrow Anti-Pattern'), handle error cases immediately, and keep happy-path code linearly readable", "They make code compile in assembly", "They allocate variables in Flash memory", "They double CPU clock speed"],
                "correct": 0,
                "explanation": "Guard clauses validate preconditions upfront and return immediately, keeping main logic flat and unnested."
            },
            {
                "question": "In an 'if (A) ... else if (B) ... else ...' construct, how many blocks can possibly execute?",
                "options": ["At most 1 block (the first condition that evaluates to true, or the else fallback)", "All blocks that are true", "Exactly 2 blocks", "0 blocks always"],
                "correct": 0,
                "explanation": "An <code>if / else if / else</code> chain is mutually exclusive; exactly one branch executes."
            },
            {
                "question": "Why do safety-critical standards like ISO 26262 restrict cyclomatic complexity to small numbers (e.g. <= 10)?",
                "options": ["High complexity exponentially increases the number of execution paths, making 100% complete MC/DC test coverage impossible to verify", "To reduce power supply voltage", "Because microcontrollers can only count to 10", "To fit code onto floppy disks"],
                "correct": 0,
                "explanation": "Low complexity guarantees that all execution paths can be systematically tested and proven safe under formal verification."
            }
        ]
    },
    {
        "id": "retired_women",
        "name": "RetiredWomen",
        "title": "Complex Boolean Decision Rules & Truth Table Minimization",
        "headline": "Multi-Variable Boolean Logic, Karnaugh Maps & Embedded Interlock Systems",
        "emb_class": "emb-core",
        "emb_badge": "⚡ Embedded Relevance: Core",
        "tags": ["Boolean Logic", "Karnaugh Maps", "Safety Interlocks", "Optimization", "Rules Engine"],
        "summary": "Analyzing multi-variable conditional logic (age, gender, employment status). We examine Karnaugh Map boolean logic reduction, multi-condition safety interlocks (e.g. press brake safety guards), and eliminating redundant condition evaluations in firmware.",
        "files": ["section_3/RetiredWomen/RetiredWomen/main.cpp"],
        "concepts_html": """
        <h3>1. Multi-Variable Boolean Decision Logic</h3>
        <p>Combining multiple criteria (e.g. <code>gender == 'F' &amp;&amp; age &gt;= 60</code>) to enforce business or safety rules.</p>

        <h3>2. Boolean Simplification</h3>
        <p>Using algebraic rules or Karnaugh Maps to minimize boolean expressions into the fewest possible logic terms.</p>
        """,
        "embedded_html": """
        <h3>1. Industrial Safety Interlock Systems</h3>
        <p>In industrial machinery (e.g. robotic welding cells, high-tonnage stamping presses), physical safety interlocks (light curtains, E-stop buttons, door interlocks) must evaluate simultaneously to grant actuator power.</p>
        """,
        "refactor_html": """
        <p>Industrial machinery safety interlock evaluation:</p>
        <pre class="code-block" style="background:#0d1117; padding:16px; border-radius:8px; border:1px solid #30363d;">#include &lt;cstdint&gt;

struct MachineSafetySensors {
    bool emergency_stop_released;
    bool light_curtain_clear;
    bool guard_door_closed;
    bool hydraulic_pressure_ok;
};

// All interlocks must evaluate true simultaneously (Category 4 Safety)
constexpr bool isMachineInterlockSafe(MachineSafetySensors s) noexcept {
    return s.emergency_stop_released &amp;&amp;
           s.light_curtain_clear &amp;&amp;
           s.guard_door_closed &amp;&amp;
           s.hydraulic_pressure_ok;
}</pre>
        """,
        "quiz": [
            {
                "question": "What is a 'Karnaugh Map' (K-map) used for in logic design?",
                "options": ["A graphical method for minimizing complex boolean algebra expressions into minimal sum-of-products or product-of-sums terms", "A map of Flash ROM memory addresses", "A routing diagram for PCB traces", "A tool for debugging stack overflows"],
                "correct": 0,
                "explanation": "K-maps visually group adjacent boolean minterms, simplifying complex logic into minimal algebraic terms."
            },
            {
                "question": "In safety-critical industrial machinery (ISO 13849 Category 4), what is a 'safety interlock'?",
                "options": ["A hardware/software mechanism that prevents dangerous machine motion unless all protective safety conditions are proven satisfied", "A password lock on the LCD screen", "A circuit breaker for high voltage", "A software timer delay"],
                "correct": 0,
                "explanation": "Safety interlocks ensure hazardous machinery cannot operate unless all safety guards (doors, light curtains, E-stops) are secure."
            },
            {
                "question": "What is the boolean result of 'A && (A || B)'?",
                "options": ["A (Absorption Law)", "B", "A && B", "true"],
                "correct": 0,
                "explanation": "By the Absorption Law of Boolean Algebra: $A \\land (A \\lor B) \\equiv A$."
            },
            {
                "question": "Why should compound boolean expressions in firmware place the cheapest condition first in a logical AND (A && B)?",
                "options": ["Short-circuit evaluation will skip evaluating the expensive condition B if the cheap condition A is false, saving CPU clock cycles", "To make the binary file smaller", "Because C++ executes conditions in reverse", "To prevent stack overflow"],
                "correct": 0,
                "explanation": "Placing cheap checks (e.g. a flag variable) before expensive ones (e.g. an SPI sensor read) lets short-circuiting skip the expensive call."
            }
        ]
    },
    {
        "id": "grade_fun",
        "name": "GradeFun",
        "title": "Switch Statements, Jump Tables & TBB/TBH Instructions",
        "headline": "Switch Statements vs If-Else Ladders: Compiler Jump Tables (TBB / TBH)",
        "emb_class": "emb-high",
        "emb_badge": "⚡ Embedded Relevance: Critical",
        "tags": ["switch", "Jump Tables", "TBB / TBH", "Branch Performance", "O(1) Dispatch"],
        "summary": "Exploring multi-case selection via switch statements vs if-else chains. We analyze compiler jump table generation (ARM TBB - Table Branch Byte / TBH - Table Branch Halfword), demonstrating why switch statements achieve deterministic O(1) execution time for dense integer cases.",
        "files": ["section_3/GradeFun/GradeFun/main.cpp"],
        "concepts_html": """
        <h3>1. <code>switch</code> Statement Syntax</h3>
        <p><code>switch</code> evaluates an integral or enum expression and transfers control to matching <code>case</code> labels. Missing <code>break;</code> statements cause intentional or accidental fallthrough.</p>

        <h3>2. <code>[[fallthrough]]</code> Attribute (C++17)</h3>
        <p>Marking intentional case fallthrough with <code>[[fallthrough]];</code> silences compiler warnings (<code>-Wimplicit-fallthrough</code>).</p>
        """,
        "embedded_html": """
        <h3>1. Jump Tables in ARM Assembly (<code>TBB</code> / <code>TBH</code>)</h3>
        <p>When cases are contiguous integers (e.g. 0 to 7), the compiler does NOT emit a series of comparisons. Instead, it emits a <strong>Jump Table (<code>TBB [PC, R0]</code>)</strong> in Flash. The CPU indexes directly into the table in <strong>$O(1)$ constant time</strong>, regardless of case count!</p>
        """,
        "refactor_html": """
        <p>Deterministic command dispatcher using jump table switch:</p>
        <pre class="code-block" style="background:#0d1117; padding:16px; border-radius:8px; border:1px solid #30363d;">#include &lt;cstdint&gt;

enum class PacketCmd : uint8_t {
    Ping = 0,
    GetTelemetry,
    SetRelayOn,
    SetRelayOff,
    Reboot
};

// Compiles to a single ARM TBB jump table instruction (O(1) execution!)
void dispatchPacketCommand(PacketCmd cmd) noexcept {
    switch (cmd) {
        case PacketCmd::Ping:         sendAck(); break;
        case PacketCmd::GetTelemetry: streamSensors(); break;
        case PacketCmd::SetRelayOn:   relay_set(true); break;
        case PacketCmd::SetRelayOff:  relay_set(false); break;
        case PacketCmd::Reboot:       system_reset(); break;
        default:                      sendErrorNack(); break;
    }
}</pre>
        """,
        "quiz": [
            {
                "question": "How does an optimizing compiler execute a dense 'switch' statement with 10 sequential integer cases on ARM Cortex-M?",
                "options": ["It generates a Jump Table (using TBB/TBH instructions), indexing directly to target case addresses in deterministic O(1) time", "It compiles 10 sequential 'if-else' comparison instructions taking O(N) time", "It creates 10 separate threads", "It sends commands over the I2C bus"],
                "correct": 0,
                "explanation": "For dense integer cases, compilers generate a jump table containing branch offsets, achieving $O(1)$ dispatch in 2-3 clock cycles."
            },
            {
                "question": "What happens if a developer forgets a 'break;' statement at the end of a switch case in C++?",
                "options": ["Execution falls through into the next case statement, executing subsequent code unintentionally", "The compiler throws a syntax error", "The switch statement terminates immediately", "The microcontroller restarts"],
                "correct": 0,
                "explanation": "Without <code>break;</code>, execution continues into the subsequent <code>case</code> block (fallthrough), often causing serious logic bugs."
            },
            {
                "question": "Which C++17 attribute explicitly marks that a switch case fallthrough is intentional?",
                "options": ["[[fallthrough]];", "[[continue]];", "[[ignore]];", "[[next]];"],
                "correct": 0,
                "explanation": "<code>[[fallthrough]];</code> (C++17) informs the compiler that fallthrough is deliberate, silencing <code>-Wimplicit-fallthrough</code> warnings."
            },
            {
                "question": "Can floating-point variables (e.g. float x = 3.14f) be used as the condition in a switch statement?",
                "options": ["No, switch statements in C++ only accept integral or enumeration types", "Yes, in C++20 and later", "Yes, if cast to void*", "Yes, but only on 64-bit platforms"],
                "correct": 0,
                "explanation": "C++ strictly requires switch expressions to be integral (integers, characters) or enumeration types; floating-point values are not allowed."
            }
        ]
    },
    {
        "id": "leap_year_checker",
        "name": "LeapYearChecker",
        "title": "Real-Time Clocks (RTC), Calendar Math & Epoch Timestamps",
        "headline": "Gregorian Calendar Rules, RTC Peripheral Math & Unix Epoch Timestamps",
        "emb_class": "emb-core",
        "emb_badge": "⚡ Embedded Relevance: Core",
        "tags": ["RTC", "Epoch Time", "Leap Year", "Calendar Math", "Unix Timestamp"],
        "summary": "Implementing Gregorian calendar leap year determination. We examine the exact three-tier leap year algorithm (divisible by 4, except centuries unless divisible by 400), analyze hardware Real-Time Clock (RTC) calendar registers, and convert dates to Unix Epoch timestamps (seconds since Jan 1, 1970).",
        "files": ["section_3/LeapYearChecker/LeapYearChecker/main.cpp"],
        "concepts_html": """
        <h3>1. The Gregorian Leap Year Algorithm</h3>
        <p>A year is a leap year if:</p>
        <ul>
          <li>It is divisible by <strong>4</strong>,</li>
          <li><strong>EXCEPT</strong> if it is divisible by <strong>100</strong>,</li>
          <li><strong>UNLESS</strong> it is also divisible by <strong>400</strong>.</li>
        </ul>
        <p>Formula: <code>(year % 4 == 0 &amp;&amp; year % 100 != 0) || (year % 400 == 0)</code>.</p>
        """,
        "embedded_html": """
        <h3>1. Hardware Real-Time Clock (RTC) Subsystems</h3>
        <p>Microcontroller RTC peripherals (backed by a 32.768 kHz quartz crystal and coin cell battery) track calendar time (BCC year/month/day/hour/min/sec) with automatic leap year compensation up to year 2099.</p>
        """,
        "refactor_html": """
        <p>Compile-time constexpr leap year calculation:</p>
        <pre class="code-block" style="background:#0d1117; padding:16px; border-radius:8px; border:1px solid #30363d;">#include &lt;cstdint&gt;

constexpr bool isLeapYear(uint32_t year) noexcept {
    return ((year % 4 == 0) &amp;&amp; (year % 100 != 0)) || (year % 400 == 0);
}

constexpr uint8_t daysInMonth(uint32_t year, uint8_t month) noexcept {
    constexpr uint8_t DAYS[] = {0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};
    if (month == 2 &amp;&amp; isLeapYear(year)) return 29;
    return month &lt;= 12 ? DAYS[month] : 0;
}</pre>
        """,
        "quiz": [
            {
                "question": "Which of the following years is NOT a leap year under Gregorian calendar rules?",
                "options": ["1900 (divisible by 100 but not 400)", "2000 (divisible by 400)", "2024 (divisible by 4)", "2004 (divisible by 4)"],
                "correct": 0,
                "explanation": "Century years are only leap years if divisible by 400. 1900 is divisible by 100 but not 400, so it was a standard 365-day year."
            },
            {
                "question": "What is the standard quartz crystal frequency used by microcontroller Real-Time Clock (RTC) peripherals?",
                "options": ["32.768 kHz (2^15 Hz, which a 15-bit prescaler divides to exact 1 Hz ticks)", "8.000 MHz", "100.000 kHz", "1.000 GHz"],
                "correct": 0,
                "explanation": "$32,768\\text{ Hz} = 2^{15}\\text{ Hz}$. A 15-stage binary counter divides this frequency down to exactly 1 pulse per second ($1\\text{ Hz}$) with low power."
            },
            {
                "question": "What is the starting reference date (Epoch) for Unix timestamps?",
                "options": ["January 1, 1970 00:00:00 UTC", "January 1, 2000 00:00:00 UTC", "January 1, 1900 00:00:00 UTC", "December 31, 1999 23:59:59 UTC"],
                "correct": 0,
                "explanation": "Unix time measures the continuous elapsed seconds since 00:00:00 UTC on January 1, 1970."
            },
            {
                "question": "What is the 'Year 2038 Problem' in 32-bit embedded systems?",
                "options": ["32-bit signed time_t integers (seconds since 1970) will overflow on January 19, 2038, wrapping around to negative year 1901", "Microcontroller batteries expire", "Flash memory reaches 100% wear", "The RTC crystal stops oscillating"],
                "correct": 0,
                "explanation": "Signed 32-bit integers max out at $2,147,483,647$ seconds, which elapses on Jan 19, 2038. Upgrading to 64-bit <code>int64_t</code> time resolves this."
            }
        ]
    },
    {
        "id": "rock_paper_scissors",
        "name": "RockPaperScissors",
        "title": "State Machines, Game Trees & Discrete Event Logic",
        "headline": "Modular Game State Loops, Enum Representations & Transition Matrices",
        "emb_class": "emb-core",
        "emb_badge": "⚡ Embedded Relevance: Core",
        "tags": ["State Machines", "Enums", "Transition Matrix", "Modularity", "Game Logic"],
        "summary": "Building interactive decision trees and win/loss resolution matrices. We model cyclical dominance relationships (Rock beats Scissors, Scissors beats Paper, Paper beats Rock) using compact lookup matrices and clean scoped enums.",
        "files": ["section_3/RockPaperScissors/RockPaperScissors/main.cpp"],
        "concepts_html": """
        <h3>1. Cyclical Win/Loss Dominance</h3>
        <p>Rock-Paper-Scissors represents a 3-state cyclical dominance ring. Rather than writing 9 nested <code>if-else</code> branches, the result can be computed via a $3\\times 3$ transition lookup matrix.</p>
        """,
        "embedded_html": """
        <h3>1. Lookup Matrix vs Conditional Branching</h3>
        <p>A $3\\times 3$ matrix stored in Flash ROM resolves the winner in a <strong>single array access</strong> with <strong>0 conditional branches</strong>, demonstrating lookup-table optimization.</p>
        """,
        "refactor_html": """
        <p>Zero-branch matrix lookup for game outcome:</p>
        <pre class="code-block" style="background:#0d1117; padding:16px; border-radius:8px; border:1px solid #30363d;">#include &lt;cstdint&gt;

enum class Move : uint8_t { Rock = 0, Paper = 1, Scissors = 2 };
enum class Outcome : int8_t { Loss = -1, Tie = 0, Win = 1 };

// Stored in Flash ROM (.rodata)
constexpr Outcome OUTCOME_MATRIX[3][3] = {
    // Player: Rock, Paper, Scissors vs CPU:
    /* Rock */     { Outcome::Tie,  Outcome::Loss, Outcome::Win  },
    /* Paper */    { Outcome::Win,  Outcome::Tie,  Outcome::Loss },
    /* Scissors */ { Outcome::Loss, Outcome::Win,  Outcome::Tie  }
};

constexpr Outcome evaluateGame(Move player, Move cpu) noexcept {
    return OUTCOME_MATRIX[static_cast&lt;size_t&gt;(player)][static_cast&lt;size_t&gt;(cpu)];
}</pre>
        """,
        "quiz": [
            {
                "question": "What is the advantage of using a 2D lookup table matrix over 9 nested if-else branches to resolve game outcomes?",
                "options": ["It evaluates the outcome in constant O(1) time with a single memory load and zero conditional branch instructions", "It uses more RAM", "It requires floating-point hardware", "It converts the game to multithreaded mode"],
                "correct": 0,
                "explanation": "Matrix indexing (<code>table[player][cpu]</code>) executes in $O(1)$ time with zero branch instructions, eliminating branch misprediction penalties."
            },
            {
                "question": "Why should scoped enum classes (enum class Move : uint8_t) be used instead of raw unscoped enums?",
                "options": ["They prevent accidental implicit conversions to integer and enforce strict type safety and specified 1-byte storage", "They run in parallel across CPU cores", "They allocate enums in the heap", "They make enums dynamic"],
                "correct": 0,
                "explanation": "Scoped enum classes enforce explicit typing and prevent naming collisions and unsafe implicit promotions."
            },
            {
                "question": "How much Flash ROM does a 3x3 lookup matrix of int8_t values consume?",
                "options": ["Exactly 9 bytes", "36 bytes", "1024 bytes", "0 bytes"],
                "correct": 0,
                "explanation": "A $3\\times 3$ array of 1-byte integers takes exactly $3 \\times 3 \\times 1 = 9$ bytes in Flash ROM."
            },
            {
                "question": "What is the mathematical modulo formula for cyclical Rock-Paper-Scissors win evaluation (0=Rock, 1=Paper, 2=Scissors)?",
                "options": ["(player - cpu + 3) % 3 (where 1 = Win, 2 = Loss, 0 = Tie)", "(player + cpu) % 2", "(player * cpu) % 3", "player / cpu"],
                "correct": 0,
                "explanation": "The modular distance <code>(player - cpu + 3) % 3</code> yields 0 for Tie, 1 for Player Win, and 2 for CPU Win."
            }
        ]
    },
    {
        "id": "repetition_fun",
        "name": "RepetitionFun",
        "title": "Iteration Loops: While, Do-While & For Loop Mechanics",
        "headline": "Pre-Test (while) vs Post-Test (do-while) Loops & ARM Assembly Generation",
        "emb_class": "emb-core",
        "emb_badge": "⚡ Embedded Relevance: Core",
        "tags": ["while", "do-while", "for loops", "Pre-Test vs Post-Test", "Assembly"],
        "summary": "Exploring loop structures: while (pre-test), do-while (post-test), and for loops. We analyze their assembly generation on ARM Cortex-M, demonstrate why do-while loops execute the loop body at least once, and examine infinite loop super-loops in embedded systems.",
        "files": ["section_3/RepetitionFun/RepetitionFun/main.cpp"],
        "concepts_html": """
        <h3>1. Pre-Test vs Post-Test Loops</h3>
        <ul>
          <li><strong>Pre-Test (<code>while</code>, <code>for</code>):</strong> Evaluates condition BEFORE executing the body. May execute 0 times if condition is initially false.</li>
          <li><strong>Post-Test (<code>do-while</code>):</strong> Executes the body FIRST, then evaluates the condition at the end. <strong>Always executes at least once!</strong></li>
        </ul>
        """,
        "embedded_html": """
        <h3>1. The Embedded 'Super-Loop' Architecture</h3>
        <p>Bare-metal microcontrollers without an RTOS use an intentional infinite loop (<code>while (true) { ... }</code>) as the master task scheduler, servicing state machines and peripheral interrupts continuously.</p>
        """,
        "refactor_html": """
        <p>Embedded non-blocking super-loop architecture:</p>
        <pre class="code-block" style="background:#0d1117; padding:16px; border-radius:8px; border:1px solid #30363d;">#include &lt;cstdint&gt;

void serviceSensors() noexcept;
void updateActuators() noexcept;
void feedHardwareWatchdog() noexcept;

void mainSuperLoop() noexcept {
    while (true) { // Master bare-metal super-loop
        serviceSensors();
        updateActuators();
        feedHardwareWatchdog(); // Reset watchdog counter
    }
}</pre>
        """,
        "quiz": [
            {
                "question": "What is the fundamental operational difference between a 'while' loop and a 'do-while' loop?",
                "options": ["A 'while' loop tests its condition before the first iteration (may execute 0 times); a 'do-while' loop tests its condition after each iteration (guaranteed to execute at least once)", "A 'do-while' loop runs in background threads", "A 'while' loop can only count up to 100", "A 'do-while' loop uses double precision"],
                "correct": 0,
                "explanation": "<code>do-while</code> evaluates at the bottom of the loop, ensuring the loop body executes at least one time."
            },
            {
                "question": "What is a 'Super-Loop' architecture in bare-metal microcontroller firmware?",
                "options": ["An infinite while(true) loop in main() that continuously polls inputs, processes state machines, and drives outputs without an operating system", "A loop that overclocks the CPU", "A recursive function that never terminates", "A compiler optimization flag"],
                "correct": 0,
                "explanation": "Super-loops form the foundational execution model of bare-metal microcontrollers, executing sequential tasks in an infinite loop."
            },
            {
                "question": "Why is 'feeding the Watchdog Timer' essential inside an embedded super-loop?",
                "options": ["If the firmware hangs in a deadlock or infinite loop, failing to reset the watchdog causes hardware to reboot the MCU safely", "To keep the crystal warm", "To recharge the coin cell battery", "To clear Flash memory sectors"],
                "correct": 0,
                "explanation": "The hardware Watchdog Timer resets the microcontroller if software hangs and fails to reload the counter periodically."
            },
            {
                "question": "What does a 'for (init; cond; step)' loop compile to in assembly relative to a 'while (cond)' loop?",
                "options": ["Identical assembly code; 'for' and 'while' are syntactic variations of the same underlying loop construct", "A 'for' loop uses twice as much RAM", "A 'while' loop cannot be unrolled", "A 'for' loop disables compiler optimizations"],
                "correct": 0,
                "explanation": "Compilers generate identical branch/test instructions for both <code>for</code> and <code>while</code> loops."
            }
        ]
    },
    {
        "id": "sum_fun",
        "name": "SumFun",
        "title": "Loop Accumulators, Arithmetic Series & Gauss Sum Formula",
        "headline": "Loop Accumulation, Arithmetic Series & Gauss Closed-Form O(1) Optimization",
        "emb_class": "emb-core",
        "emb_badge": "⚡ Embedded Relevance: Core",
        "tags": ["Accumulator", "Gauss Formula", "Arithmetic Series", "O(1) Math", "Loop Elimination"],
        "summary": "Accumulating numeric series with loops. We contrast iterative $O(N)$ loop summation with Gauss's closed-form arithmetic series formula $\\frac{N(N+1)}{2}$, demonstrating how mathematical proofs eliminate loops and execute in $O(1)$ constant time.",
        "files": ["section_3/SumFun/SumFun/main.cpp"],
        "concepts_html": """
        <h3>1. Iterative Accumulation ($O(N)$)</h3>
        <p>Summing numbers from $1$ to $N$ with a loop executes $N$ additions taking $O(N)$ time.</p>

        <h3>2. Gauss's Closed-Form Formula ($O(1)$)</h3>
        <p>Carl Friedrich Gauss proved that the sum of the first $N$ natural numbers equals:</p>
        <p>$$\\text{Sum} = \\frac{N \\times (N + 1)}{2}$$</p>
        <p>This closed-form formula executes in <strong>$O(1)$ single-cycle time</strong>, completely eliminating the loop!</p>
        """,
        "embedded_html": """
        <h3>1. Compiler Optimization (Scalar Evolution - SCEV)</h3>
        <p>Modern optimizing compilers (GCC/Clang with <code>-O3</code>) recognize arithmetic summation patterns and automatically replace loops with the closed-form Gauss formula in the compiled binary.</p>
        """,
        "refactor_html": """
        <p>Closed-form $O(1)$ arithmetic series summation:</p>
        <pre class="code-block" style="background:#0d1117; padding:16px; border-radius:8px; border:1px solid #30363d;">#include &lt;cstdint&gt;

// O(1) Constant Time Summation: 1 + 2 + ... + N
constexpr uint64_t sumNaturalNumbers(uint32_t n) noexcept {
    return (static_cast&lt;uint64_t&gt;(n) * (n + 1)) / 2;
}</pre>
        """,
        "quiz": [
            {
                "question": "What is the closed-form mathematical formula to sum the first N integers from 1 to N?",
                "options": ["(N * (N + 1)) / 2", "N * (N - 1)", "N^2 / 2", "N * 2 + 1"],
                "correct": 0,
                "explanation": "Gauss's summation formula computes the sum of $1$ to $N$ as $\\frac{N(N+1)}{2}$ in $O(1)$ operations."
            },
            {
                "question": "What is the time complexity difference between a loop summing 1 to 1,000,000 vs Gauss's formula?",
                "options": ["The loop takes O(N) operations (1,000,000 cycles); Gauss's formula takes O(1) constant time (1-2 cycles)", "Both take O(N) time", "Gauss's formula takes O(log N) time", "The loop is faster on ARM"],
                "correct": 0,
                "explanation": "The loop performs $N$ iterations, while Gauss's formula performs 1 multiplication, 1 addition, and 1 bit-shift ($O(1)$)."
            },
            {
                "question": "Why is static_cast<uint64_t> important before computing 'n * (n + 1)' when n = 100,000?",
                "options": ["100,000 * 100,001 = 10,000,100,000 which exceeds 32-bit uint32_t maximum (4,294,967,295), causing silent overflow", "uint32_t cannot be divided by 2", "To convert the integer to float", "To enable multithreading"],
                "correct": 0,
                "explanation": "Multiplying large integers can exceed $2^{32}-1$; promoting to <code>uint64_t</code> prevents intermediate multiplication overflow."
            },
            {
                "question": "What compiler optimization replaces loops with closed-form mathematical formulas automatically?",
                "options": ["Scalar Evolution (SCEV) loop optimization", "Dead Code Elimination", "Inlining", "Tail Call Optimization"],
                "correct": 0,
                "explanation": "Compilers use Scalar Evolution (SCEV) analysis to identify induction variables and replace eligible loops with closed-form formulas."
            }
        ]
    },
    {
        "id": "even_only",
        "name": "EvenOnly",
        "title": "Conditional Skipping, Step Size Adjustments & Loop Efficiency",
        "headline": "Loop Stride Adjustments (i += 2) vs Internal Filtering & Branch Overhead",
        "emb_class": "emb-core",
        "emb_badge": "⚡ Embedded Relevance: Core",
        "tags": ["Loop Stride", "Filtering", "Branch Reduction", "Optimization", "Cycle Efficiency"],
        "summary": "Generating even-number sequences. We demonstrate why advancing the loop step size directly (i += 2) executes twice as fast as iterating every number and filtering with if (i % 2 == 0), eliminating half the loop iterations and 100% of branch conditions.",
        "files": ["section_3/EvenOnly/EvenOnly/main.cpp"],
        "concepts_html": """
        <h3>1. Iteration Filtering vs Stride Adjustment</h3>
        <ul>
          <li><strong>Filtering (<code>i++</code> with <code>if (i%2 == 0)</code>):</strong> Executes $N$ iterations and performs $N$ conditional tests.</li>
          <li><strong>Stride Adjustment (<code>i += 2</code>):</strong> Executes $\\frac{N}{2}$ iterations with <strong>0 conditional tests</strong>!</li>
        </ul>
        """,
        "embedded_html": """
        <h3>1. 50% Cycle Reduction</h3>
        <p>Adjusting the loop stride cuts instruction count in half, directly reducing CPU power consumption and thermal dissipation on battery-powered sensor nodes.</p>
        """,
        "refactor_html": """
        <p>Optimal stride-based iteration:</p>
        <pre class="code-block" style="background:#0d1117; padding:16px; border-radius:8px; border:1px solid #30363d;">#include &lt;cstdint&gt;

// Iterates only over even indices (50% fewer clock cycles!)
void processEvenSensors(const uint16_t* data, size_t count) noexcept {
    for (size_t i = 0; i &lt; count; i += 2) {
        // Direct processing with zero if-checks!
    }
}</pre>
        """,
        "quiz": [
            {
                "question": "Why is 'for (int i=0; i<100; i+=2)' strictly more efficient than 'for (int i=0; i<100; i++) if (i%2==0)'?",
                "options": ["It cuts the total number of loop iterations in half (50 vs 100) and completely eliminates the internal branch condition check", "It uses floating-point hardware", "It allocates memory on the stack", "It makes the loop compile in C89"],
                "correct": 0,
                "explanation": "Stepping by 2 executes 50 iterations instead of 100 and removes the <code>if</code> branch test entirely."
            },
            {
                "question": "How does reducing loop iteration count benefit battery-powered embedded devices?",
                "options": ["Fewer executed CPU instructions means the core completes tasks faster and returns to low-power Sleep/Stop mode sooner, conserving battery", "It decreases battery voltage", "It increases WiFi transmission speed", "It deletes unused variables"],
                "correct": 0,
                "explanation": "In energy-harvesting and battery systems ('race-to-sleep' strategy), finishing processing in fewer clock cycles allows the CPU to enter low-power sleep mode sooner."
            },
            {
                "question": "What is the initial value of 'i' to iterate over only odd numbers with 'i += 2'?",
                "options": ["1", "0", "2", "-1"],
                "correct": 0,
                "explanation": "Starting at 1 and stepping by 2 visits 1, 3, 5, 7... (all odd integers)."
            },
            {
                "question": "What assembly instruction increments a register by 2 on ARM Cortex-M?",
                "options": ["ADDS r0, r0, #2", "MUL r0, #2", "DIV r0, #2", "SUBS r0, #2"],
                "correct": 0,
                "explanation": "<code>ADDS r0, r0, #2</code> adds 2 to register r0 in a single clock cycle."
            }
        ]
    },
    {
        "id": "continue_break",
        "name": "ContinueBreak",
        "title": "Loop Control: Break, Continue & Early Loop Termination",
        "headline": "break vs continue Flow Control, Search Loops & Nested Loop Escape Idioms",
        "emb_class": "emb-core",
        "emb_badge": "⚡ Embedded Relevance: Core",
        "tags": ["break", "continue", "Early Exit", "Loop Control", "Linear Search"],
        "summary": "Analyzing loop interruption statements: break (immediate loop exit) and continue (skip to next iteration). We explore early loop termination during buffer searches and safe multi-level nested loop breakout idioms.",
        "files": ["section_3/ContinueBreak/ContinueBreak/main.cpp"],
        "concepts_html": """
        <h3>1. <code>break</code> vs <code>continue</code></h3>
        <ul>
          <li><code>break</code>: Immediately terminates the enclosing loop; execution resumes at the first statement following the loop.</li>
          <li><code>continue</code>: Skips the remainder of the current iteration and jumps directly to the loop update/condition check.</li>
        </ul>

        <h3>2. Multi-Level Loop Escapes</h3>
        <p>In C++, <code>break</code> exits only the innermost loop. Escaping nested loops cleanly is best achieved by refactoring the search into a dedicated function with an <code>early return</code>.</p>
        """,
        "embedded_html": """
        <h3>1. Real-Time Worst-Case vs Average-Case Search</h3>
        <p>While <code>break</code> speeds up average-case search, real-time safety systems must guarantee execution time under the <strong>Worst-Case Execution Time (WCET)</strong> scenario (when the target item is at the very last index or absent).</p>
        """,
        "refactor_html": """
        <p>Clean early-return linear search replacing nested break flags:</p>
        <pre class="code-block" style="background:#0d1117; padding:16px; border-radius:8px; border:1px solid #30363d;">#include &lt;cstdint&gt;
#include &lt;cstddef&gt;

// Early return cleanly terminates search without complex break flags
size_t findSensorFaultIndex(const uint16_t* samples, size_t count, uint16_t threshold) noexcept {
    for (size_t i = 0; i &lt; count; ++i) {
        if (samples[i] &gt; threshold) {
            return i; // Found fault! Exits loop and function immediately
        }
    }
    return static_cast&lt;size_t&gt;(-1); // No fault found
}</pre>
        """,
        "quiz": [
            {
                "question": "What is the difference between 'break' and 'continue' inside a for loop?",
                "options": ["'break' terminates the entire loop immediately; 'continue' skips the rest of the current iteration and advances to the next iteration", "'break' restarts the loop from 0", "'continue' terminates the program", "'break' pauses execution for 10ms"],
                "correct": 0,
                "explanation": "<code>break</code> exits the loop completely, while <code>continue</code> skips the rest of the current pass and begins the next loop cycle."
            },
            {
                "question": "How many levels of nested loops does a single 'break;' statement exit in C++?",
                "options": ["Exactly 1 level (the innermost enclosing loop)", "All nested loops", "2 levels", "It depends on the compiler"],
                "correct": 0,
                "explanation": "<code>break</code> applies strictly to the innermost loop or switch statement enclosing it."
            },
            {
                "question": "What is the cleanest C++ idiom to exit from 3 levels of deeply nested search loops?",
                "options": ["Encapsulate the nested loops in a dedicated helper function and execute an early 'return' when the item is found", "Use 3 consecutive break statements on the same line", "Throw an exception", "Restart the microcontroller"],
                "correct": 0,
                "explanation": "Extracting nested loops into a helper function allows an immediate <code>return</code> to exit all loops simultaneously with zero flag variables."
            },
            {
                "question": "What is 'WCET' in real-time safety-critical firmware analysis?",
                "options": ["Worst-Case Execution Time: the maximum possible execution duration a piece of code can take on target hardware under worst-case inputs", "Wireless Controller Energy Tracker", "Watchdog Clock Enable Timer", "Wideband Channel Error Test"],
                "correct": 0,
                "explanation": "WCET is the provable upper bound on execution duration, critical for verifying that real-time interrupt deadlines are never missed."
            }
        ]
    },
    {
        "id": "die_rolls",
        "name": "DieRolls",
        "title": "Random Numbers: PRNG vs Hardware True RNG (TRNG)",
        "headline": "std::rand() Hazards, Seed Management & Hardware True Random Number Generators (TRNG)",
        "emb_class": "emb-high",
        "emb_badge": "⚡ Embedded Relevance: High",
        "tags": ["PRNG", "TRNG", "Hardware RNG", "Entropy", "Cryptography"],
        "summary": "Exploring random number generation and dice simulation. We analyze the severe cryptographic and statistical flaws of std::rand() (Linear Congruential Generators), seed initialization from uninitialized ADC noise, and hardware True Random Number Generators (TRNG peripherals) on microcontrollers (e.g. STM32 RNG).",
        "files": ["section_3/DieRolls/DieRolls/main.cpp"],
        "concepts_html": """
        <h3>1. Pseudo-Random Number Generators (PRNG)</h3>
        <p>Standard <code>std::rand()</code> is a <strong>Linear Congruential Generator (LCG)</strong>. Given the same initial seed (<code>std::srand(seed)</code>), it produces the exact same deterministic sequence of numbers.</p>

        <h3>2. Modulo Bias</h3>
        <p>Computing <code>rand() % 6</code> introduces <strong>Modulo Bias</strong>: lower numbers have a slightly higher probability of being chosen because <code>RAND_MAX</code> is rarely an exact multiple of 6.</p>
        """,
        "embedded_html": """
        <h3>1. Microcontroller Hardware True RNG (TRNG)</h3>
        <p>Modern microcontrollers (such as STM32, ESP32, nRF52) feature dedicated on-chip <strong>Hardware TRNG peripherals</strong>. They harvest physical analog thermal noise from ring oscillators to produce 100% non-deterministic cryptographic entropy for AES keys, BLE pairing, and secure boot.</p>
        """,
        "refactor_html": """
        <p>Hardware True Random Number Generator (TRNG) driver:</p>
        <pre class="code-block" style="background:#0d1117; padding:16px; border-radius:8px; border:1px solid #30363d;">#include &lt;cstdint&gt;

// Hardware TRNG Peripheral Access (STM32 RNG)
struct HardwareRNG {
    volatile uint32_t CR;  // Control Register
    volatile uint32_t SR;  // Status Register
    volatile uint32_t DR;  // Data Register (32-bit random word)
};

uint32_t getHardwareTrueRandom() noexcept {
    HardwareRNG* const rng = reinterpret_cast&lt;HardwareRNG*&gt;(0x50060800);
    while ((rng-&gt;SR &amp; 1UL) == 0); // Wait for Data Ready (DRDY)
    return rng-&gt;DR; // True physical analog entropy!
}</pre>
        """,
        "quiz": [
            {
                "question": "Why is 'std::rand()' strictly prohibited for cryptographic keys, BLE pairing, or secure IoT boot?",
                "options": ["It is a deterministic Linear Congruential Generator with short cycles; observing a few outputs allows attackers to predict all future keys", "It runs too slowly", "It consumes 100KB of RAM", "It can only generate negative numbers"],
                "correct": 0,
                "explanation": "<code>std::rand()</code> is mathematically predictable and not cryptographically secure; attackers can reverse-engineer internal state from a few samples."
            },
            {
                "question": "What physical phenomenon do on-chip hardware True Random Number Generators (TRNG) sample to generate entropy?",
                "options": ["Analog thermal noise, transistor shot noise, and jitter from internal analog ring oscillators", "The CPU crystal frequency", "The number of lines of code", "The ambient room temperature in Celsius"],
                "correct": 0,
                "explanation": "Hardware TRNGs sample physical analog thermal noise across multiple asynchronous ring oscillators to produce true non-deterministic entropy."
            },
            {
                "question": "What is 'Modulo Bias' when scaling random numbers (e.g. rand() % 6)?",
                "options": ["A statistical distortion where numbers below the remainder of RAND_MAX % 6 occur with higher probability than numbers above it", "A compiler error caused by division", "A memory leak on the heap", "A hardware fault on ARM"],
                "correct": 0,
                "explanation": "When the generator range is not an exact multiple of the target range, smaller outcomes receive one extra value in the mapping, skewing fairness."
            },
            {
                "question": "How do developers without a hardware TRNG seed a PRNG on basic microcontrollers?",
                "options": ["Sample the least significant bits of an unconnected, floating analog ADC pin to capture ambient electromagnetic noise", "Hardcode the seed to 0", "Use the compiler version number", "Use the baud rate"],
                "correct": 0,
                "explanation": "Reading a floating ADC pin captures ambient atmospheric electromagnetic noise, providing an initial random seed for PRNG algorithms."
            }
        ]
    },
    {
        "id": "random_fun",
        "name": "RandomFun",
        "title": "Modern C++ <random> Library vs Legacy C rand()",
        "headline": "Modern C++ <random> Engines (std::mt19937) vs Distributions (uniform_int_distribution)",
        "emb_class": "emb-core",
        "emb_badge": "⚡ Embedded Relevance: Core",
        "tags": ["<random>", "std::mt19937", "uniform_int_distribution", "Mersenne Twister", "Distributions"],
        "summary": "Exploring the Modern C++ <random> library introduced in C++11. We contrast legacy C rand() with modern random engines (Mersenne Twister std::mt19937) and statistical distribution mappers (std::uniform_int_distribution), analyzing the 2.5KB RAM state footprint of mt19937 vs lightweight Xorshift32 PRNGs for microcontrollers.",
        "files": ["section_3/RandomFun/RandomFun/main.cpp"],
        "concepts_html": """
        <h3>1. Engine vs Distribution Separation</h3>
        <p>C++11 cleanly separates random number generation into two orthogonal concepts:</p>
        <ul>
          <li><strong>Random Engine:</strong> Generates a sequence of pseudo-random bits (e.g. <code>std::mt19937</code>).</li>
          <li><strong>Distribution:</strong> Maps bits into a target mathematical distribution without modulo bias (e.g. <code>std::uniform_int_distribution&lt;int&gt;(1, 6)</code>).</li>
        </ul>
        """,
        "embedded_html": """
        <h3>1. The RAM Footprint of <code>std::mt19937</code></h3>
        <p>The Mersenne Twister (<code>std::mt19937</code>) maintains a <strong>624-word state vector (2,496 bytes of SRAM)</strong>. In a 2KB RAM microcontroller, a single <code>mt19937</code> instance exhausts the entire system RAM! Embedded firmware uses lightweight <strong>Xorshift32 (4 bytes of RAM)</strong> instead.</p>
        """,
        "refactor_html": """
        <p>Ultra-lightweight Xorshift32 PRNG (4 Bytes of SRAM Total):</p>
        <pre class="code-block" style="background:#0d1117; padding:16px; border-radius:8px; border:1px solid #30363d;">#include &lt;cstdint&gt;

// Marsaglia Xorshift32: High-quality randomness; 4 bytes RAM; 3 clock cycles!
uint32_t xorshift32(uint32_t&amp; state) noexcept {
    uint32_t x = state;
    x ^= x &lt;&lt; 13;
    x ^= x &gt;&gt; 17;
    x ^= x &lt;&lt; 5;
    state = x;
    return x;
}</pre>
        """,
        "quiz": [
            {
                "question": "How much RAM state memory does a std::mt19937 (Mersenne Twister) instance consume?",
                "options": ["Approximately 2,500 bytes (624 32-bit state words)", "4 bytes", "16 bytes", "64 kilobytes"],
                "correct": 0,
                "explanation": "<code>std::mt19937</code> stores 624 32-bit state integers plus an index ($624 \\times 4 + 4 \\approx 2,500$ bytes), making it too large for microcontrollers with 2KB-4KB of RAM."
            },
            {
                "question": "What is the memory footprint and execution speed of a Xorshift32 PRNG?",
                "options": ["Consumes exactly 4 bytes of RAM (1 uint32_t state) and executes in 3 clock cycles using simple XOR and bit-shift operations", "Consumes 1MB of heap", "Takes 1,000 cycles", "Requires an external EEPROM"],
                "correct": 0,
                "explanation": "Xorshift32 uses a single 32-bit integer state and 3 ALU instructions (shift and XOR), executing in ~3 clock cycles with 4 bytes of RAM."
            },
            {
                "question": "What does std::uniform_int_distribution<int>(1, 10) guarantee?",
                "options": ["A flat, uniform probability distribution across integers 1 to 10 with zero modulo bias", "Only even numbers are generated", "Numbers are sorted in ascending order", "Numbers are generated in 1 clock cycle"],
                "correct": 0,
                "explanation": "<code>std::uniform_int_distribution</code> samples the engine and applies rejection sampling to guarantee statistically uniform, unbiased distributions."
            },
            {
                "question": "Why should a random engine and its distribution be passed to generator functions rather than recreated on every call?",
                "options": ["Re-instantiating the engine every call resets its state or re-seeds it with the same timestamp, producing repetitive identical sequences", "To prevent compiler syntax warnings", "To allow floating point operations", "To move the engine to Flash memory"],
                "correct": 0,
                "explanation": "Recreating engines on each call resets their internal sequence, generating duplicate values if called within the same timer tick."
            }
        ]
    },
    {
        "id": "streaming_calculator",
        "name": "StreamingCalculator",
        "title": "Interactive Stream Parsers & Polish Notation Machines",
        "headline": "Streaming Input Parsing, Operator Precedence & Embedded Command-Line Interfaces (CLI)",
        "emb_class": "emb-core",
        "emb_badge": "⚡ Embedded Relevance: Core",
        "tags": ["Stream Parsing", "CLI", "Command Dispatcher", "Operator Precedence", "Serial Console"],
        "summary": "Building a streaming arithmetic calculator with continuous input parsing. We analyze character stream tokenization, operator precedence state machines, and how embedded systems implement Serial Command Line Interfaces (CLI) for field calibration and hardware diagnostics over UART.",
        "files": ["section_3/StreamingCalculator/StreamingCalculator/main.cpp"],
        "concepts_html": """
        <h3>1. Streaming Token Parsing</h3>
        <p>Reading alternating numbers and operators from a continuous character stream until a termination command (e.g. <code>'q'</code> or <code>EOF</code>) is received.</p>

        <h3>2. Accumulator State Retention</h3>
        <p>Preserving running totals across sequential user operations in an accumulator register.</p>
        """,
        "embedded_html": """
        <h3>1. Embedded Serial Command Line Interfaces (CLI)</h3>
        <p>Production embedded devices implement interactive UART diagnostic CLIs (e.g. <code>set_voltage 3300</code>, <code>read_sensors</code>, <code>dump_logs</code>), parsing ASCII tokens character-by-character from serial buffers.</p>
        """,
        "refactor_html": """
        <p>Embedded UART CLI command tokenizer:</p>
        <pre class="code-block" style="background:#0d1117; padding:16px; border-radius:8px; border:1px solid #30363d;">#include &lt;cstdint&gt;
#include &lt;string_view&gt;

void executeCliCommand(std::string_view cmd) noexcept {
    if (cmd == "ping") {
        sendResponse("PONG\\r\\n");
    } else if (cmd == "status") {
        sendResponse("STATUS: ALL SYSTEMS OK\\r\\n");
    } else if (cmd == "reset") {
        system_reboot();
    } else {
        sendResponse("ERROR: UNKNOWN COMMAND\\r\\n");
    }
}</pre>
        """,
        "quiz": [
            {
                "question": "What is the primary role of a serial Command Line Interface (CLI) in embedded firmware development?",
                "options": ["Provides an interactive text console over UART for field calibration, firmware configuration, and real-time hardware diagnostics", "Compiles C++ code on the microcontroller", "Renders 3D graphics", "Replaces the hardware crystal oscillator"],
                "correct": 0,
                "explanation": "Embedded CLIs provide engineer interfaces over serial/UART ports for real-time testing, tuning, and field maintenance."
            },
            {
                "question": "Why is character-by-character tokenization preferred over full line buffering in memory-constrained microcontrollers?",
                "options": ["It processes tokens immediately as bytes arrive over UART, requiring only a tiny 16-32 byte buffer rather than storing large strings in RAM", "It requires 64-bit integers", "It disables UART interrupts", "It makes strings read-only"],
                "correct": 0,
                "explanation": "Stream tokenization evaluates tokens on the fly, consuming minimal SRAM compared to buffering entire multi-kilobyte text messages."
            },
            {
                "question": "What is 'Reverse Polish Notation' (RPN) in stack-based calculator architectures?",
                "options": ["A mathematical notation where operators follow their operands (e.g. '3 4 +'), eliminating the need for parentheses and complex operator precedence parsers", "A notation written in Russian", "An encrypted binary format", "A floating-point representation"],
                "correct": 0,
                "explanation": "RPN writes operators after operands, making arithmetic evaluation trivial to implement using a simple LIFO stack."
            },
            {
                "question": "What should an embedded serial parser do when receiving an unrecognized command string?",
                "options": ["Emit a structured error response (e.g. 'ERR: UNKNOWN CMD\\r\\n') and flush the current line buffer to recover cleanly", "Crash with a HardFault", "Erase the Flash memory", "Freeze the CPU in an infinite loop"],
                "correct": 0,
                "explanation": "Robust parsers reply with an error message and discard invalid characters, maintaining system stability."
            }
        ]
    }
]
