#!/usr/bin/env python3
"""
Generate complete UML Architecture & Class Model definitions for all 116 curriculum projects.
"""

import os
import pprint

UML_DATA = {
    # =========================================================================
    # SECTION 1: TOOLCHAINS & LINKERS (2 Projects)
    # =========================================================================
    "hello": {
        "title": "C++ Build Pipeline & Linker Section Memory Architecture",
        "classes": [
            {
                "name": "HelloApp",
                "stereotype": "<<compilation-unit>>",
                "badge": "Main Translation Unit",
                "type": "module",
                "attributes": [
                    "+ EXIT_SUCCESS : const int32_t = 0",
                    "- std::cout : std::ostream&"
                ],
                "methods": [
                    "+ main() : int32_t",
                    "- printBanner() : void"
                ]
            },
            {
                "name": "ELFSectionMapper",
                "stereotype": "<<linker-script>>",
                "badge": "Memory Map Layout",
                "type": "struct",
                "attributes": [
                    "+ FLASH_BASE : uintptr_t = 0x08000000",
                    "+ SRAM_BASE : uintptr_t = 0x20000000",
                    "+ .text : Flash ROM [Machine Code]",
                    "+ .rodata : Flash ROM [Constants & Literals]",
                    "+ .data : SRAM (VMA) / Flash (LMA) [Initialized]",
                    "+ .bss : SRAM [Zero-Initialized Globals]"
                ],
                "methods": [
                    "+ Reset_Handler() : void",
                    "+ SystemInit() : void"
                ]
            }
        ],
        "relationships": [
            {"from": "HelloApp", "to": "ELFSectionMapper", "type": "uses", "label": "compiled & linked into"}
        ],
        "notes": "Deconstructs how the high-level C++ entry point maps through preprocessor, compiler, assembler, and linker script into physical Flash and SRAM memory banks."
    },
    "vsc_hello": {
        "title": "Cross-Compilation Toolchain & Embedded Serial Architecture",
        "classes": [
            {
                "name": "VscHelloApp",
                "stereotype": "<<compilation-unit>>",
                "badge": "Main Entry Point",
                "type": "module",
                "attributes": [
                    "- bannerText : const char*",
                    "- std::cout : std::ostream&"
                ],
                "methods": [
                    "+ main() : int32_t",
                    "- renderBanner(title: const char*) : void"
                ]
            },
            {
                "name": "UARTStreamBuffer",
                "stereotype": "<<hardware-driver>>",
                "badge": "Embedded Serial Console",
                "type": "struct",
                "attributes": [
                    "+ USART1_DR : volatile uint32_t*",
                    "+ USART1_SR : volatile uint32_t*",
                    "+ baudRate : uint32_t = 115200"
                ],
                "methods": [
                    "+ init(baud: uint32_t) : void",
                    "+ writeChar(c: char) : void",
                    "+ writeString(str: const char*) : void"
                ]
            }
        ],
        "relationships": [
            {"from": "VscHelloApp", "to": "UARTStreamBuffer", "type": "uses", "label": "routes stdout to"}
        ]
    },

    # =========================================================================
    # SECTION 2: TYPES, VARIABLES & MEMORY (14 Projects)
    # =========================================================================
    "hello_world": {
        "title": "Standard I/O Translation Unit Model",
        "classes": [
            {
                "name": "HelloWorldApp",
                "stereotype": "<<compilation-unit>>",
                "badge": "Main Unit",
                "type": "module",
                "attributes": [
                    "+ greeting : const char* = \"Hello World!\""
                ],
                "methods": [
                    "+ main() : int32_t"
                ]
            }
        ]
    },
    "comment_fun": {
        "title": "Source Comment Parser & Doxygen Firmware Documentation Model",
        "classes": [
            {
                "name": "CommentFunApp",
                "stereotype": "<<compilation-unit>>",
                "badge": "Documentation Unit",
                "type": "module",
                "attributes": [
                    "- singleLineComment : const char*",
                    "- multiLineComment : const char*"
                ],
                "methods": [
                    "+ main() : int32_t",
                    "+ documentedApiFunction(param: int32_t) : bool [Doxygen Documented]"
                ]
            }
        ]
    },
    "variable_fun": {
        "title": "Fundamental Types & Stack Memory Layout Model",
        "classes": [
            {
                "name": "TypeMemoryLayout",
                "stereotype": "<<struct>>",
                "badge": "Stack Frame Layout",
                "type": "struct",
                "attributes": [
                    "+ myInt : int32_t (4 bytes @ SP+0)",
                    "+ myDouble : double (8 bytes @ SP+4)",
                    "+ myChar : char (1 byte @ SP+12)",
                    "+ myBool : bool (1 byte @ SP+13)",
                    "- padding : uint8_t[2] (Alignment Pad)"
                ],
                "methods": [
                    "+ inspectSizes() : void",
                    "+ printMemoryAddresses() : void"
                ]
            }
        ]
    },
    "text_fun": {
        "title": "Character Encoding & ASCII Memory Mapping Model",
        "classes": [
            {
                "name": "TextManipulator",
                "stereotype": "<<compilation-unit>>",
                "badge": "ASCII Processor",
                "type": "module",
                "attributes": [
                    "- rawChar : char",
                    "- asciiCode : uint8_t"
                ],
                "methods": [
                    "+ toUpper(c: char) : char",
                    "+ toLower(c: char) : char",
                    "+ isDigit(c: char) : bool",
                    "+ printHexCode(c: char) : void"
                ]
            }
        ]
    },
    "arithmetic_fun": {
        "title": "ALU Arithmetic Pipeline & Overflow Guard Model",
        "classes": [
            {
                "name": "ArithmeticEngine",
                "stereotype": "<<compilation-unit>>",
                "badge": "ALU Operations",
                "type": "module",
                "attributes": [
                    "- opA : int32_t",
                    "- opB : int32_t"
                ],
                "methods": [
                    "+ add(a: int32_t, b: int32_t) : int32_t",
                    "+ subtract(a: int32_t, b: int32_t) : int32_t",
                    "+ multiply(a: int32_t, b: int32_t) : int32_t",
                    "+ divide(a: int32_t, b: int32_t) : int32_t",
                    "+ modulo(a: int32_t, b: int32_t) : int32_t"
                ]
            },
            {
                "name": "SaturatingMath",
                "stereotype": "<<embedded-dsp>>",
                "badge": "QADD / QSUB",
                "type": "struct",
                "attributes": [
                    "+ INT32_SAT_MAX : const int32_t",
                    "+ INT32_SAT_MIN : const int32_t"
                ],
                "methods": [
                    "+ addSaturate(a: int32_t, b: int32_t) : int32_t",
                    "+ subSaturate(a: int32_t, b: int32_t) : int32_t"
                ]
            }
        ],
        "relationships": [
            {"from": "ArithmeticEngine", "to": "SaturatingMath", "type": "uses", "label": "refactors to"}
        ]
    },
    "relational_fun": {
        "title": "Relational Comparison & CPU Condition Flags Model",
        "classes": [
            {
                "name": "RelationalEvaluator",
                "stereotype": "<<compilation-unit>>",
                "badge": "APSR Flags (N, Z, C, V)",
                "type": "module",
                "attributes": [
                    "- threshold : int32_t",
                    "- currentValue : int32_t"
                ],
                "methods": [
                    "+ isEqual(a: int, b: int) : bool",
                    "+ isGreater(a: int, b: int) : bool",
                    "+ isLessOrEqual(a: int, b: int) : bool"
                ]
            }
        ]
    },
    "logical_fun": {
        "title": "Logical Operators & Short-Circuit Optimization Model",
        "classes": [
            {
                "name": "LogicEngine",
                "stereotype": "<<compilation-unit>>",
                "badge": "Short-Circuit Optimizer",
                "type": "module",
                "attributes": [
                    "- isRaining : bool",
                    "- isWarm : bool"
                ],
                "methods": [
                    "+ evaluateAnd(condA: bool, condB: bool) : bool",
                    "+ evaluateOr(condA: bool, condB: bool) : bool",
                    "+ evaluateNot(cond: bool) : bool"
                ]
            }
        ]
    },
    "boolean_fun": {
        "title": "Boolean Bitfield Compression & 1-Byte Packing Model",
        "classes": [
            {
                "name": "BitfieldFlags",
                "stereotype": "<<struct>>",
                "badge": "1-Byte Packed Struct",
                "type": "struct",
                "attributes": [
                    "+ isReady : uint8_t : 1",
                    "+ hasError : uint8_t : 1",
                    "+ isArmed : uint8_t : 1",
                    "+ mode : uint8_t : 2",
                    "- reserved : uint8_t : 3"
                ],
                "methods": [
                    "+ printFlags() : void const"
                ]
            }
        ]
    },
    "constant_fun": {
        "title": "Compile-Time Constants & Flash ROM (.rodata) Model",
        "classes": [
            {
                "name": "ConstexprMemoryPool",
                "stereotype": "<<struct>>",
                "badge": ".rodata Placement (Zero SRAM)",
                "type": "struct",
                "attributes": [
                    "+ PI : constexpr double = 3.141592653589793",
                    "+ MAX_BUFFER_SIZE : constexpr size_t = 128",
                    "+ DEVICE_ID : constexpr uint32_t = 0xAA5500FF"
                ],
                "methods": [
                    "+ calculateCircumference(radius: double) : constexpr double"
                ]
            }
        ]
    },
    "keyboard_input": {
        "title": "Stream Input & UART Buffer Parsing Model",
        "classes": [
            {
                "name": "StreamInputHandler",
                "stereotype": "<<compilation-unit>>",
                "badge": "Input Stream Handler",
                "type": "module",
                "attributes": [
                    "- inputBuffer : char[64]",
                    "- inputState : uint8_t"
                ],
                "methods": [
                    "+ readInteger() : int32_t",
                    "+ readString(dest: char*, maxLen: size_t) : bool",
                    "+ clearErrors() : void"
                ]
            }
        ]
    },
    "sunny_warm": {
        "title": "Boolean Multi-Sensor Fusion Decision Model",
        "classes": [
            {
                "name": "WeatherSensorFusion",
                "stereotype": "<<compilation-unit>>",
                "badge": "Sensor Evaluator",
                "type": "module",
                "attributes": [
                    "- isSunny : bool",
                    "- isWarm : bool"
                ],
                "methods": [
                    "+ evaluateOutdoorConditions(sunny: bool, warm: bool) : bool",
                    "+ printRecommendation() : void"
                ]
            }
        ]
    },
    "percentages": {
        "title": "Fixed-Point Fraction & Floating-Point Model",
        "classes": [
            {
                "name": "PercentageCalculator",
                "stereotype": "<<compilation-unit>>",
                "badge": "Math Pipeline",
                "type": "module",
                "attributes": [
                    "- numerator : double",
                    "- denominator : double"
                ],
                "methods": [
                    "+ calculatePercentage(num: double, den: double) : double",
                    "+ calculateBpsFixedPoint(num: int32_t, den: int32_t) : int32_t"
                ]
            }
        ]
    },
    "tip_calculator": {
        "title": "Tip Calculator & Currency Decimal Accuracy Model",
        "classes": [
            {
                "name": "TipCalculatorEngine",
                "stereotype": "<<compilation-unit>>",
                "badge": "Financial Calculator",
                "type": "module",
                "attributes": [
                    "- billAmountCents : int64_t",
                    "- tipPercentageBps : int32_t"
                ],
                "methods": [
                    "+ calculateTipCents(billCents: int64_t, pct: int32_t) : int64_t",
                    "+ printBillBreakdown() : void"
                ]
            }
        ]
    },
    "secret_agent_id": {
        "title": "Agent Identity Record & String Token Injection Model",
        "classes": [
            {
                "name": "AgentIdentity",
                "stereotype": "<<struct>>",
                "badge": "Identity Record",
                "type": "struct",
                "attributes": [
                    "+ firstName : std::string",
                    "+ lastName : std::string",
                    "+ agentNumber : int32_t"
                ],
                "methods": [
                    "+ formatAgentCode() : std::string"
                ]
            }
        ]
    },

    # =========================================================================
    # SECTION 3: CONTROL FLOW & BRANCHING (13 Projects)
    # =========================================================================
    "control_statements_intro": {
        "title": "Branch Prediction & Conditional Pipeline Model",
        "classes": [
            {
                "name": "BranchController",
                "stereotype": "<<compilation-unit>>",
                "badge": "Control Flow Unit",
                "type": "module",
                "attributes": [
                    "- age : int32_t",
                    "- isAuthorized : bool"
                ],
                "methods": [
                    "+ checkPermission(age: int) : bool",
                    "+ routeBranch(flag: bool) : void"
                ]
            }
        ]
    },
    "selection_fun": {
        "title": "Multi-Way Branch & Nested If-Else Model",
        "classes": [
            {
                "name": "SelectionEngine",
                "stereotype": "<<compilation-unit>>",
                "badge": "Decision Logic",
                "type": "module",
                "attributes": [
                    "- selectionState : int32_t"
                ],
                "methods": [
                    "+ evaluateCategory(val: int32_t) : const char*",
                    "+ processNestedCondition(x: int, y: int) : void"
                ]
            }
        ]
    },
    "retired_women": {
        "title": "Demographic Rule Evaluator & Karnaugh Map Model",
        "classes": [
            {
                "name": "DemographicProfile",
                "stereotype": "<<struct>>",
                "badge": "Packed Record",
                "type": "struct",
                "attributes": [
                    "+ age : uint8_t",
                    "+ gender : char ('M' / 'F')",
                    "+ isRetired : bool"
                ],
                "methods": [
                    "+ qualifyDiscount() : bool"
                ]
            },
            {
                "name": "PensionRuleEngine",
                "stereotype": "<<compilation-unit>>",
                "badge": "Rule Matrix",
                "type": "module",
                "attributes": [
                    "+ MIN_RETIRE_AGE : constexpr uint8_t = 60"
                ],
                "methods": [
                    "+ evaluatePension(profile: const DemographicProfile&) : bool"
                ]
            }
        ],
        "relationships": [
            {"from": "PensionRuleEngine", "to": "DemographicProfile", "type": "uses", "label": "evaluates"}
        ]
    },
    "grade_fun": {
        "title": "Switch Jump Table & Score Classifier Model",
        "classes": [
            {
                "name": "GradeClassifier",
                "stereotype": "<<compilation-unit>>",
                "badge": "Jump Table (TBB/TBH)",
                "type": "module",
                "attributes": [
                    "- letterGrade : char"
                ],
                "methods": [
                    "+ classifyScore(score: int) : char",
                    "+ printGradeFeedback(grade: char) : void"
                ]
            }
        ]
    },
    "leap_year_checker": {
        "title": "Calendar Rule Evaluator & Century Boundary Model",
        "classes": [
            {
                "name": "LeapYearEvaluator",
                "stereotype": "<<compilation-unit>>",
                "badge": "Calendar Pipeline",
                "type": "module",
                "attributes": [
                    "- year : int32_t"
                ],
                "methods": [
                    "+ isLeapYear(y: int32_t) : bool [(y%4==0 && y%100!=0) || y%400==0]"
                ]
            }
        ]
    },
    "rock_paper_scissors": {
        "title": "Rock Paper Scissors State Machine & Matrix Model",
        "classes": [
            {
                "name": "HandMove",
                "stereotype": "<<enum class : uint8_t>>",
                "badge": "Move Enum",
                "type": "struct",
                "attributes": [
                    "+ ROCK : uint8_t = 0",
                    "+ PAPER : uint8_t = 1",
                    "+ SCISSORS : uint8_t = 2"
                ],
                "methods": []
            },
            {
                "name": "RpsGameEngine",
                "stereotype": "<<compilation-unit>>",
                "badge": "Decision Matrix",
                "type": "module",
                "attributes": [
                    "- userMove : HandMove",
                    "- cpuMove : HandMove"
                ],
                "methods": [
                    "+ determineWinner(p1: HandMove, p2: HandMove) : int32_t [1: P1, -1: P2, 0: Tie]",
                    "+ generateCpuMove() : HandMove"
                ]
            }
        ],
        "relationships": [
            {"from": "RpsGameEngine", "to": "HandMove", "type": "uses", "label": "switches on"}
        ]
    },
    "repetition_fun": {
        "title": "Loop Constructs & Branch-Loop Overhead Model",
        "classes": [
            {
                "name": "LoopExecutionEngine",
                "stereotype": "<<compilation-unit>>",
                "badge": "Loop Pipeline",
                "type": "module",
                "attributes": [
                    "- loopCounter : uint32_t"
                ],
                "methods": [
                    "+ executeWhileLoop(limit: uint32_t) : void",
                    "+ executeDoWhileLoop(limit: uint32_t) : void",
                    "+ executeForLoop(limit: uint32_t) : void"
                ]
            }
        ]
    },
    "sum_fun": {
        "title": "Loop Accumulator & Integer Overflow Guard Model",
        "classes": [
            {
                "name": "SumAccumulator",
                "stereotype": "<<compilation-unit>>",
                "badge": "Accumulator",
                "type": "module",
                "attributes": [
                    "- currentSum : int64_t",
                    "- inputCount : uint32_t"
                ],
                "methods": [
                    "+ addValue(val: int32_t) : bool",
                    "+ getAverage() : double const",
                    "+ reset() : void"
                ]
            }
        ]
    },
    "even_only": {
        "title": "Even-Number Loop Filtering & Step Increment Model",
        "classes": [
            {
                "name": "EvenFilterEngine",
                "stereotype": "<<compilation-unit>>",
                "badge": "Filter Unit",
                "type": "module",
                "attributes": [
                    "- lowerBound : int32_t",
                    "- upperBound : int32_t"
                ],
                "methods": [
                    "+ printEvenRange(start: int, end: int) : void [i += 2 step]"
                ]
            }
        ]
    },
    "continue_break": {
        "title": "Loop Control Flow: Break and Continue Execution Paths",
        "classes": [
            {
                "name": "LoopControlOptimizer",
                "stereotype": "<<compilation-unit>>",
                "badge": "Jump Controller",
                "type": "module",
                "attributes": [],
                "methods": [
                    "+ processWithEarlyExit(maxIters: int, target: int) : void [break]",
                    "+ filterIgnoredValues(items: const int*, count: size_t) : void [continue]"
                ]
            }
        ]
    },
    "die_rolls": {
        "title": "Die Rolling State Machine & Pseudo-Random Model",
        "classes": [
            {
                "name": "DieSimulator",
                "stereotype": "<<struct>>",
                "badge": "Die State",
                "type": "struct",
                "attributes": [
                    "+ sides : uint8_t = 6",
                    "+ lastRoll : uint8_t"
                ],
                "methods": [
                    "+ roll() : uint8_t"
                ]
            }
        ]
    },
    "random_fun": {
        "title": "Hardware TRNG vs PRNG Linear Congruential Model",
        "classes": [
            {
                "name": "RandomGenerator",
                "stereotype": "<<compilation-unit>>",
                "badge": "RNG Engine",
                "type": "module",
                "attributes": [
                    "- seedValue : uint32_t"
                ],
                "methods": [
                    "+ seed(s: uint32_t) : void",
                    "+ getRandRange(min: int, max: int) : int32_t"
                ]
            },
            {
                "name": "HwTrngDriver",
                "stereotype": "<<hardware-driver>>",
                "badge": "STM32 TRNG Peripheral",
                "type": "struct",
                "attributes": [
                    "+ RNG_CR : volatile uint32_t*",
                    "+ RNG_SR : volatile uint32_t*",
                    "+ RNG_DR : volatile uint32_t*"
                ],
                "methods": [
                    "+ getTrueRandomWord() : uint32_t"
                ]
            }
        ],
        "relationships": [
            {"from": "RandomGenerator", "to": "HwTrngDriver", "type": "uses", "label": "entropy source"}
        ]
    },
    "streaming_calculator": {
        "title": "Streaming Arithmetic Operator Parser & Accumulator Model",
        "classes": [
            {
                "name": "StreamingCalculator",
                "stereotype": "<<compilation-unit>>",
                "badge": "Stream Processor",
                "type": "module",
                "attributes": [
                    "- runningTotal : double = 0.0",
                    "- isRunning : bool = true"
                ],
                "methods": [
                    "+ applyOperation(op: char, val: double) : void",
                    "+ getResult() : double const",
                    "+ reset() : void"
                ]
            }
        ]
    },

    # =========================================================================
    # SECTION 4: ARRAYS, DMA & CACHE LINES (11 Projects)
    # =========================================================================
    "array_fun": {
        "title": "Fixed Array Memory Contiguity & DMA Model",
        "classes": [
            {
                "name": "StaticArrayBuffer",
                "stereotype": "<<struct>>",
                "badge": "Contiguous SRAM Block",
                "type": "struct",
                "attributes": [
                    "+ data[5] : int32_t (20 bytes contiguous)",
                    "+ size : constexpr size_t = 5"
                ],
                "methods": [
                    "+ at(idx: size_t) : int32_t&",
                    "+ fill(val: int32_t) : void",
                    "+ printElements() : void const"
                ]
            }
        ]
    },
    "array_fun_test": {
        "title": "Array Boundary Verification & Assertion Test Harness",
        "classes": [
            {
                "name": "ArrayTestHarness",
                "stereotype": "<<compilation-unit>>",
                "badge": "Test Harness",
                "type": "module",
                "attributes": [
                    "- testBuffer[10] : int32_t"
                ],
                "methods": [
                    "+ testIndexRead(idx: size_t) : bool",
                    "+ testIndexWrite(idx: size_t, val: int) : bool"
                ]
            }
        ]
    },
    "more_array_fun": {
        "title": "Array Bounds Safety & Range-Based For Loop Model",
        "classes": [
            {
                "name": "ArrayIteratorEngine",
                "stereotype": "<<compilation-unit>>",
                "badge": "Iteration Pipeline",
                "type": "module",
                "attributes": [
                    "- scores[10] : int32_t"
                ],
                "methods": [
                    "+ iterateIndexed(arr: const int*, len: size_t) : void",
                    "+ iterateRangeFor(span: std::span<const int>) : void",
                    "+ computeSum(arr: const int*, len: size_t) : int32_t"
                ]
            }
        ]
    },
    "twice_numbers": {
        "title": "Array Element Transformation & SIMD Scaling Model",
        "classes": [
            {
                "name": "ArrayTransformer",
                "stereotype": "<<compilation-unit>>",
                "badge": "Transformation Engine",
                "type": "module",
                "attributes": [
                    "- numbers[5] : int32_t"
                ],
                "methods": [
                    "+ doubleElements(arr: int*, size: size_t) : void",
                    "+ printArray(arr: const int*, size: size_t) : void"
                ]
            }
        ]
    },
    "names_array": {
        "title": "String Array Memory Layout & Pointer Tables",
        "classes": [
            {
                "name": "NamesRegistry",
                "stereotype": "<<compilation-unit>>",
                "badge": "String Array Table",
                "type": "module",
                "attributes": [
                    "- names[5] : std::string"
                ],
                "methods": [
                    "+ populateNames() : void",
                    "+ displayNames() : void const"
                ]
            }
        ]
    },
    "temperature_converter": {
        "title": "Array Temperature Conversion & DSP Scaling Model",
        "classes": [
            {
                "name": "TemperatureConverter",
                "stereotype": "<<compilation-unit>>",
                "badge": "Scaling Pipeline",
                "type": "module",
                "attributes": [
                    "- fahrenheitTemps[5] : double",
                    "- celsiusTemps[5] : double"
                ],
                "methods": [
                    "+ convertFtoC(f: double) : double",
                    "+ batchConvert(fArr: const double*, cArr: double*, len: size_t) : void"
                ]
            }
        ]
    },
    "2d_array_fun": {
        "title": "2D Row-Major Matrix & DMA Framebuffer Model",
        "classes": [
            {
                "name": "Matrix2D",
                "stereotype": "<<struct>>",
                "badge": "Row-Major Memory Grid",
                "type": "struct",
                "attributes": [
                    "+ grid[2][3] : int32_t (6 elements, 24 contiguous bytes)",
                    "+ ROWS : constexpr size_t = 2",
                    "+ COLS : constexpr size_t = 3"
                ],
                "methods": [
                    "+ at(r: size_t, c: size_t) : int32_t&",
                    "+ printRowMajor() : void const",
                    "+ sumAllElements() : int32_t const"
                ]
            }
        ]
    },
    "move_ratings": {
        "title": "2D Matrix Rating Table & Row-Major Analytics Model",
        "classes": [
            {
                "name": "MovieRatingMatrix",
                "stereotype": "<<struct>>",
                "badge": "2D Review Table",
                "type": "struct",
                "attributes": [
                    "+ ratings[3][4] : double (3 reviewers, 4 movies)",
                    "+ REVIEWERS : constexpr size_t = 3",
                    "+ MOVIES : constexpr size_t = 4"
                ],
                "methods": [
                    "+ calculateMovieAverage(col: size_t) : double",
                    "+ calculateReviewerAverage(row: size_t) : double"
                ]
            }
        ]
    },
    "vector_fun": {
        "title": "Dynamic std::vector Heap Allocation vs etl::vector Model",
        "classes": [
            {
                "name": "StdVectorModel",
                "stereotype": "<<class>>",
                "badge": "Heap Dynamic Vector",
                "type": "class",
                "attributes": [
                    "- _M_start : T* (Heap Pointer)",
                    "- _M_finish : T* (End Element Pointer)",
                    "- _M_end_of_storage : T* (Capacity Pointer)"
                ],
                "methods": [
                    "+ push_back(val: const T&) : void",
                    "+ capacity() : size_t const",
                    "+ size() : size_t const"
                ]
            },
            {
                "name": "EtlVectorFixed",
                "stereotype": "<<embedded-etl>>",
                "badge": "Zero-Heap Alternative",
                "type": "struct",
                "attributes": [
                    "+ buffer[CAPACITY] : T",
                    "+ currentSize : size_t"
                ],
                "methods": [
                    "+ push_back(val: const T&) : bool",
                    "+ is_full() : bool const"
                ]
            }
        ],
        "relationships": [
            {"from": "StdVectorModel", "to": "EtlVectorFixed", "type": "uses", "label": "refactors to in embedded"}
        ]
    },
    "vector_practice": {
        "title": "Vector Population & Accumulator Pipeline Model",
        "classes": [
            {
                "name": "VectorPracticeEngine",
                "stereotype": "<<compilation-unit>>",
                "badge": "Vector Pipeline",
                "type": "module",
                "attributes": [
                    "- numberList : std::vector<double>"
                ],
                "methods": [
                    "+ populateFromUser() : void",
                    "+ computeStatistics(mean: double&, maxVal: double&) : void"
                ]
            }
        ]
    },
    "shopping_list": {
        "title": "Shopping List Dynamic Collection & Item Search Model",
        "classes": [
            {
                "name": "ShoppingListManager",
                "stereotype": "<<class>>",
                "badge": "List Manager",
                "type": "class",
                "attributes": [
                    "- items : std::vector<std::string>"
                ],
                "methods": [
                    "+ addItem(item: string) : void",
                    "+ removeItem(item: string) : bool",
                    "+ printList() : void const",
                    "+ contains(item: string) : bool const"
                ]
            }
        ]
    },

    # =========================================================================
    # SECTION 5: FUNCTIONS & AAPCS (15 Projects)
    # =========================================================================
    "function_fun_1": {
        "title": "ARM AAPCS Register Calling Convention Model (R0-R3)",
        "classes": [
            {
                "name": "AAPCSCallingUnit",
                "stereotype": "<<compilation-unit>>",
                "badge": "Register Passing Engine",
                "type": "module",
                "attributes": [
                    "- R0 : uint32_t (Param 1 / Return Value)",
                    "- R1 : uint32_t (Param 2)",
                    "- R2 : uint32_t (Param 3)",
                    "- R3 : uint32_t (Param 4)",
                    "- R14_LR : uint32_t (Link Register - Return Addr)"
                ],
                "methods": [
                    "+ printHello() : void",
                    "+ doWork() : void"
                ]
            }
        ]
    },
    "passing_schemes": {
        "title": "Pass-by-Value vs Pass-by-Reference Assembly Mechanics",
        "classes": [
            {
                "name": "PassingSchemesUnit",
                "stereotype": "<<compilation-unit>>",
                "badge": "Calling Convention",
                "type": "module",
                "attributes": [],
                "methods": [
                    "+ passByValue(x: int32_t) : void (Local register copy in R0)",
                    "+ passByRef(x: int32_t&) : void (Passes memory address, stores via STR)",
                    "+ passByConstRef(x: const int32_t&) : void (Zero-copy read-only)"
                ]
            }
        ]
    },
    "function_overloading": {
        "title": "Function Overloading & C++ Name Mangling Architecture",
        "classes": [
            {
                "name": "OverloadDispatchTable",
                "stereotype": "<<compilation-unit>>",
                "badge": "Mangled Symbol Table",
                "type": "module",
                "attributes": [],
                "methods": [
                    "+ print(val: int) : void [_Z5printi]",
                    "+ print(val: double) : void [_Z5printd]",
                    "+ print(val: string) : void [_Z5printNSt7__cxx1112basic_string...]",
                    "+ extern \"C\" c_compatible_print(val: int) : void [c_compatible_print]"
                ]
            }
        ]
    },
    "factorial_fun": {
        "title": "Recursive Factorial Stack Frames & Tail-Call Optimization",
        "classes": [
            {
                "name": "FactorialEngine",
                "stereotype": "<<compilation-unit>>",
                "badge": "Recursion Pipeline",
                "type": "module",
                "attributes": [
                    "- maxDepth : constexpr uint32_t = 32"
                ],
                "methods": [
                    "+ factorial(n: uint32_t) : uint64_t",
                    "+ factorialTail(n: uint32_t, acc: uint64_t = 1) : uint64_t [Tail-Call Optimized to B]"
                ]
            }
        ]
    },
    "math_fun": {
        "title": "Hardware FPU & CORDIC Math Acceleration Model",
        "classes": [
            {
                "name": "MathLibrary",
                "stereotype": "<<compilation-unit>>",
                "badge": "Math Library",
                "type": "module",
                "attributes": [],
                "methods": [
                    "+ calculatePower(base: double, exp: double) : double",
                    "+ calculateSqrt(val: double) : double",
                    "+ calculateSin(angleRad: double) : double"
                ]
            }
        ]
    },
    "count_down": {
        "title": "Recursive Countdown vs Iterative SysTick Loop Model",
        "classes": [
            {
                "name": "CountdownEngine",
                "stereotype": "<<compilation-unit>>",
                "badge": "Timer Pipeline",
                "type": "module",
                "attributes": [],
                "methods": [
                    "+ countDownRecursive(num: int32_t) : void",
                    "+ countDownIterative(num: int32_t) : void"
                ]
            }
        ]
    },
    "count_evens": {
        "title": "Array Event Filtering & Branchless Counting Model",
        "classes": [
            {
                "name": "EvenCounterEngine",
                "stereotype": "<<compilation-unit>>",
                "badge": "Counting ALU",
                "type": "module",
                "attributes": [],
                "methods": [
                    "+ countEvens(arr: const int*, size: size_t) : size_t",
                    "+ countEvensBranchless(arr: const int*, size: size_t) : size_t"
                ]
            }
        ]
    },
    "average_of_three": {
        "title": "Average Calculation Function & Register Optimization",
        "classes": [
            {
                "name": "AverageFunctionModule",
                "stereotype": "<<compilation-unit>>",
                "badge": "Function Pipeline",
                "type": "module",
                "attributes": [],
                "methods": [
                    "+ averageThree(a: double, b: double, c: double) : double"
                ]
            }
        ]
    },
    "parameter_challenge": {
        "title": "Parameter Passing Challenge & Out-Parameter Design",
        "classes": [
            {
                "name": "ParameterChallengeUnit",
                "stereotype": "<<compilation-unit>>",
                "badge": "Out Parameters",
                "type": "module",
                "attributes": [],
                "methods": [
                    "+ computeStats(a: int, b: int, sum: int&, product: int&) : void"
                ]
            }
        ]
    },
    "product_array_by_reference": {
        "title": "Array Product Calculation via Reference Passing",
        "classes": [
            {
                "name": "ProductReferenceEngine",
                "stereotype": "<<compilation-unit>>",
                "badge": "Reference Pipeline",
                "type": "module",
                "attributes": [],
                "methods": [
                    "+ computeArrayProduct(arr: const int*, size: size_t, productOut: int64_t&) : void"
                ]
            }
        ]
    },
    "product_array_object": {
        "title": "Array Container Object & Encapsulated Multiplication",
        "classes": [
            {
                "name": "ProductArrayObject",
                "stereotype": "<<struct>>",
                "badge": "Array Wrapper",
                "type": "struct",
                "attributes": [
                    "+ values[5] : int32_t",
                    "+ length : size_t = 5"
                ],
                "methods": [
                    "+ getProduct() : int64_t const"
                ]
            }
        ]
    },
    "return_type_parameter_fun": {
        "title": "Return Mechanisms & Multiple Output Types Model",
        "classes": [
            {
                "name": "MultiReturnEngine",
                "stereotype": "<<compilation-unit>>",
                "badge": "Return Resolver",
                "type": "module",
                "attributes": [],
                "methods": [
                    "+ getStatus() : int32_t [[nodiscard]]",
                    "+ processValues(inA: int, inB: int, outSum: int&, outDiff: int&) : bool"
                ]
            }
        ]
    },
    "scope_fun": {
        "title": "Variable Lifetime & Scope Resolution Model",
        "classes": [
            {
                "name": "ScopeResolver",
                "stereotype": "<<compilation-unit>>",
                "badge": "Lifetime Matrix",
                "type": "module",
                "attributes": [
                    "+ globalVar : int32_t (.data section)",
                    "- staticVar : int32_t (.bss persistent)"
                ],
                "methods": [
                    "+ testScope() : void",
                    "+ shadowDemo(globalVar: int) : void"
                ]
            }
        ]
    },
    "scope_challenge": {
        "title": "Block Scope Shadowing & Memory Lifetime Challenge",
        "classes": [
            {
                "name": "ScopeChallengeUnit",
                "stereotype": "<<compilation-unit>>",
                "badge": "Scope Verifier",
                "type": "module",
                "attributes": [
                    "+ globalCounter : int32_t"
                ],
                "methods": [
                    "+ demonstrateBlockShadowing() : void",
                    "+ modifyGlobal() : void"
                ]
            }
        ]
    },
    "tic_tac_toe": {
        "title": "Modular Procedural Tic-Tac-Toe Game Architecture",
        "classes": [
            {
                "name": "TicTacToeModule",
                "stereotype": "<<compilation-unit>>",
                "badge": "Game Module",
                "type": "module",
                "attributes": [
                    "- grid[3][3] : char",
                    "- currentTurn : char"
                ],
                "methods": [
                    "+ initializeGame() : void",
                    "+ drawBoard() : void",
                    "+ takeTurn(row: int, col: int) : bool",
                    "+ checkWinner() : char"
                ]
            }
        ]
    },

    # =========================================================================
    # SECTION 6: OOP FOUNDATIONS & ALIGNMENT (6 Projects)
    # =========================================================================
    "book_fun": {
        "title": "Book Class Encapsulation & Natural Struct Alignment Model",
        "classes": [
            {
                "name": "Book",
                "stereotype": "<<class>>",
                "badge": "Encapsulated Entity",
                "type": "class",
                "attributes": [
                    "- author : std::string",
                    "- title : std::string",
                    "- numPages : int32_t"
                ],
                "methods": [
                    "+ Book(author: string, title: string, numPages: int)",
                    "+ printBookDetails() : void const",
                    "+ getAuthor() : std::string const",
                    "+ getTitle() : std::string const",
                    "+ getNumPages() : int32_t const"
                ]
            }
        ]
    },
    "rectangle_fun": {
        "title": "Rectangle Class Invariant Enforcement & Area Model",
        "classes": [
            {
                "name": "Rectangle",
                "stereotype": "<<class>>",
                "badge": "Geometric Entity",
                "type": "class",
                "attributes": [
                    "- length : double",
                    "- width : double"
                ],
                "methods": [
                    "+ Rectangle()",
                    "+ Rectangle(length: double, width: double)",
                    "+ getLength() : double const",
                    "+ getWidth() : double const",
                    "+ setLength(length: double) : void",
                    "+ setWidth(width: double) : void",
                    "+ area() : double const",
                    "+ perimeter() : double const"
                ]
            }
        ]
    },
    "houses": {
        "title": "House Class Lifecycle, RAII & Destructor Call Stack",
        "classes": [
            {
                "name": "House",
                "stereotype": "<<class>>",
                "badge": "RAII Entity",
                "type": "class",
                "attributes": [
                    "- numStories : int32_t",
                    "- numWindows : int32_t",
                    "- color : std::string"
                ],
                "methods": [
                    "+ House()",
                    "+ House(numStories: int, numWindows: int, color: string)",
                    "+ ~House()",
                    "+ getNumStories() : int32_t const",
                    "+ setNumStories(stories: int) : void",
                    "+ getNumWindows() : int32_t const",
                    "+ setNumWindows(windows: int) : void",
                    "+ getColor() : std::string const",
                    "+ setColor(color: string) : void",
                    "+ printHouse() : void const"
                ]
            }
        ]
    },
    "library_card_project": {
        "title": "LibraryCard Entity & Transactional Method Model",
        "classes": [
            {
                "name": "LibraryCard",
                "stereotype": "<<class>>",
                "badge": "Domain Entity",
                "type": "class",
                "attributes": [
                    "- cardHolderName : std::string",
                    "- cardNumber : int32_t",
                    "- booksCheckedOut : int32_t = 0"
                ],
                "methods": [
                    "+ LibraryCard(holder: string, cardNum: int)",
                    "+ checkOutBook() : bool",
                    "+ returnBook() : bool",
                    "+ getCardHolderName() : std::string const",
                    "+ getCardNumber() : int32_t const",
                    "+ getBooksCheckedOut() : int32_t const"
                ]
            }
        ]
    },
    "sundae_project": {
        "title": "IceCreamSundae Aggregation & Dynamic Toppings Model",
        "classes": [
            {
                "name": "IceCreamSundae",
                "stereotype": "<<class>>",
                "badge": "Aggregator",
                "type": "class",
                "attributes": [
                    "- numScoops : int32_t",
                    "- flavor : std::string",
                    "- toppings : std::vector<std::string>"
                ],
                "methods": [
                    "+ IceCreamSundae(flavor: string, numScoops: int)",
                    "+ addTopping(topping: string) : void",
                    "+ printSundae() : void const",
                    "+ getFlavor() : std::string const",
                    "+ getNumScoops() : int32_t const"
                ]
            }
        ]
    },
    "triangle_project": {
        "title": "Triangle Geometric Invariants & Type Classification",
        "classes": [
            {
                "name": "Triangle",
                "stereotype": "<<class>>",
                "badge": "Geometric Model",
                "type": "class",
                "attributes": [
                    "- sideA : double",
                    "- sideB : double",
                    "- sideC : double"
                ],
                "methods": [
                    "+ Triangle(a: double, b: double, c: double)",
                    "+ isEquilateral() : bool const",
                    "+ isIsosceles() : bool const",
                    "+ isScalene() : bool const",
                    "+ area() : double const",
                    "+ perimeter() : double const"
                ]
            }
        ]
    },

    # =========================================================================
    # SECTION 7: EXCEPTIONS & FAULT SYSTEMS (9 Projects)
    # =========================================================================
    "bug_fun": {
        "title": "Runtime Bug Tracing & Assert Verification Model",
        "classes": [
            {
                "name": "BugFunDebugEngine",
                "stereotype": "<<compilation-unit>>",
                "badge": "Debug & Diagnostics",
                "type": "module",
                "attributes": [
                    "- testBuffer[4] : int32_t"
                ],
                "methods": [
                    "+ triggerOutOfBounds(idx: int) : void",
                    "+ safeAccess(idx: size_t) : int32_t"
                ]
            }
        ]
    },
    "custom_exceptions": {
        "title": "Custom Exception Class Hierarchy & DWARF .eh_frame Model",
        "classes": [
            {
                "name": "std::runtime_error",
                "stereotype": "<<class>>",
                "badge": "Base Exception",
                "type": "class",
                "attributes": [],
                "methods": [
                    "+ runtime_error(what_arg: const string&)",
                    "+ what() : const char* [virtual, noexcept]"
                ]
            },
            {
                "name": "CustomException",
                "stereotype": "<<class>>",
                "badge": "Custom Domain Exception",
                "type": "class",
                "attributes": [
                    "- errorCode : int32_t"
                ],
                "methods": [
                    "+ CustomException(msg: string, code: int = -1)",
                    "+ getErrorCode() : int32_t const",
                    "+ what() : const char* [override, noexcept]"
                ]
            }
        ],
        "relationships": [
            {"from": "CustomException", "to": "std::runtime_error", "type": "inherits", "label": "public inherits"}
        ]
    },
    "dog_fun": {
        "title": "Dog Entity & Out-of-Range Bounds Exception Model",
        "classes": [
            {
                "name": "Dog",
                "stereotype": "<<class>>",
                "badge": "Entity",
                "type": "class",
                "attributes": [
                    "- name : std::string",
                    "- breed : std::string"
                ],
                "methods": [
                    "+ Dog(name: string, breed: string)",
                    "+ getName() : std::string const",
                    "+ getBreed() : std::string const"
                ]
            }
        ]
    },
    "exception_fun_1": {
        "title": "Standard Exception Try-Catch Pipeline Architecture",
        "classes": [
            {
                "name": "ExceptionPipeline",
                "stereotype": "<<compilation-unit>>",
                "badge": "Exception Dispatcher",
                "type": "module",
                "attributes": [],
                "methods": [
                    "+ divideSafe(a: int, b: int) : int [throws std::runtime_error]"
                ]
            }
        ]
    },
    "fuel_monitor_project": {
        "title": "LowFuelException & Fuel Tank Safety Invariants Model",
        "classes": [
            {
                "name": "std::runtime_error",
                "stereotype": "<<class>>",
                "badge": "Base Exception",
                "type": "class",
                "attributes": [],
                "methods": [
                    "+ what() : const char* [virtual, noexcept]"
                ]
            },
            {
                "name": "LowFuelException",
                "stereotype": "<<class>>",
                "badge": "Domain Fault Exception",
                "type": "class",
                "attributes": [
                    "- remainingGallons : double"
                ],
                "methods": [
                    "+ LowFuelException(gallons: double)",
                    "+ getRemainingGallons() : double const",
                    "+ what() : const char* [override, noexcept]"
                ]
            },
            {
                "name": "FuelTank",
                "stereotype": "<<class>>",
                "badge": "Tank Monitor",
                "type": "class",
                "attributes": [
                    "- capacityGallons : double = 15.0",
                    "- currentFuel : double",
                    "- MIN_SAFE_FUEL : constexpr double = 2.0"
                ],
                "methods": [
                    "+ FuelTank(initialFuel: double)",
                    "+ consumeFuel(gallons: double) : void [throws LowFuelException]",
                    "+ addFuel(gallons: double) : void",
                    "+ getCurrentFuel() : double const"
                ]
            }
        ],
        "relationships": [
            {"from": "LowFuelException", "to": "std::runtime_error", "type": "inherits", "label": "inherits"},
            {"from": "FuelTank", "to": "LowFuelException", "type": "uses", "label": "throws on low level"}
        ]
    },
    "logic_error_fun": {
        "title": "std::logic_error & Invariant Verification Model",
        "classes": [
            {
                "name": "std::logic_error",
                "stereotype": "<<class>>",
                "badge": "Standard Logic Exception",
                "type": "class",
                "attributes": [
                    "- _M_msg : std::string"
                ],
                "methods": [
                    "+ logic_error(msg: const string&)",
                    "+ what() : const char* [override, noexcept]"
                ]
            },
            {
                "name": "std::length_error",
                "stereotype": "<<class>>",
                "badge": "Derived Logic Exception",
                "type": "class",
                "attributes": [],
                "methods": [
                    "+ length_error(msg: const string&)",
                    "+ what() : const char* [override, noexcept]"
                ]
            }
        ],
        "relationships": [
            {"from": "std::length_error", "to": "std::logic_error", "type": "inherits", "label": "inherits"}
        ]
    },
    "month_name_project": {
        "title": "Month Lookup Bounds Validation & std::out_of_range",
        "classes": [
            {
                "name": "MonthLookupEngine",
                "stereotype": "<<compilation-unit>>",
                "badge": "Bounds Validator",
                "type": "module",
                "attributes": [
                    "- MONTHS[12] : const char* const"
                ],
                "methods": [
                    "+ getMonthName(monthNum: int) : const char* [throws std::out_of_range]"
                ]
            }
        ]
    },
    "person_fun": {
        "title": "Person Invariant Validation & std::invalid_argument",
        "classes": [
            {
                "name": "Person",
                "stereotype": "<<class>>",
                "badge": "Entity",
                "type": "class",
                "attributes": [
                    "- name : std::string",
                    "- age : int32_t"
                ],
                "methods": [
                    "+ Person(name: string, age: int)",
                    "+ setName(name: string) : void [throws std::invalid_argument]",
                    "+ setAge(age: int) : void [throws std::invalid_argument]",
                    "+ getName() : std::string const",
                    "+ getAge() : int32_t const"
                ]
            }
        ]
    },
    "rethrow_fun_1": {
        "title": "Exception Rethrow (throw;) & Stack Unwinding Mechanics",
        "classes": [
            {
                "name": "ExceptionRethrowModule",
                "stereotype": "<<compilation-unit>>",
                "badge": "Stack Unwinder",
                "type": "module",
                "attributes": [],
                "methods": [
                    "+ processAction() : void [rethrows via throw;]",
                    "+ topLevelHandler() : void"
                ]
            }
        ]
    },

    # =========================================================================
    # SECTION 8: POINTERS & MEMORY (7 Projects)
    # =========================================================================
    "pointer_fun": {
        "title": "Raw Pointer Memory Addresses & Indirection Model",
        "classes": [
            {
                "name": "PointerAccessModel",
                "stereotype": "<<compilation-unit>>",
                "badge": "32-Bit Address Space",
                "type": "module",
                "attributes": [
                    "- myVal : int32_t = 150 (@ 0x20000010)",
                    "- pVal : int32_t* = &myVal (Holds 0x20000010 in 4 bytes)"
                ],
                "methods": [
                    "+ dereference() : int32_t [*pVal]",
                    "+ modifyTarget(newVal: int32_t) : void [*pVal = newVal]"
                ]
            }
        ]
    },
    "const_correctness": {
        "title": "The 4 Pointer Constness Permutations & Flash ROM Model",
        "classes": [
            {
                "name": "ConstPointerMatrix",
                "stereotype": "<<compilation-unit>>",
                "badge": "Constness Enforcer",
                "type": "module",
                "attributes": [
                    "+ ptrToNonConst : int* (Mutable Pointer, Mutable Data)",
                    "+ ptrToConst : const int* (Mutable Pointer, Read-Only Data in Flash)",
                    "+ constPtrToNonConst : int* const (Fixed Pointer, Mutable Data in RAM)",
                    "+ constPtrToConst : const int* const (Fixed Pointer, Read-Only Data in Flash)"
                ],
                "methods": [
                    "+ testMutations() : void"
                ]
            }
        ]
    },
    "dynamic_fun": {
        "title": "Heap Allocation (new/delete) vs Static Memory Pools",
        "classes": [
            {
                "name": "HeapManager",
                "stereotype": "<<compilation-unit>>",
                "badge": "Dynamic Allocator",
                "type": "module",
                "attributes": [
                    "- pDynamicInt : int32_t* (Allocated via new)",
                    "- pDynamicArray : double* (Allocated via new[])"
                ],
                "methods": [
                    "+ allocateHeap() : void",
                    "+ deallocateHeap() : void [delete / delete[]]"
                ]
            },
            {
                "name": "StaticMemoryPool",
                "stereotype": "<<embedded-pool>>",
                "badge": "Zero-Fragmentation Pool",
                "type": "struct",
                "attributes": [
                    "+ poolBuffer[1024] : uint8_t (Fixed SRAM Block)",
                    "+ allocatedOffset : size_t"
                ],
                "methods": [
                    "+ allocate(size: size_t) : void*",
                    "+ reset() : void"
                ]
            }
        ],
        "relationships": [
            {"from": "HeapManager", "to": "StaticMemoryPool", "type": "uses", "label": "refactors to"}
        ]
    },
    "dynamic_dogs": {
        "title": "Dynamic Dog Pointer Allocation & Lifecycle Model",
        "classes": [
            {
                "name": "Dog",
                "stereotype": "<<class>>",
                "badge": "Dynamic Entity",
                "type": "class",
                "attributes": [
                    "- name : std::string",
                    "- breed : std::string"
                ],
                "methods": [
                    "+ Dog(name: string, breed: string)",
                    "+ ~Dog()",
                    "+ getName() : std::string const",
                    "+ getBreed() : std::string const"
                ]
            },
            {
                "name": "DogOwnerApp",
                "stereotype": "<<compilation-unit>>",
                "badge": "Lifecycle Controller",
                "type": "module",
                "attributes": [
                    "- myDogPtr : Dog*"
                ],
                "methods": [
                    "+ createDog(name: string, breed: string) : void",
                    "+ releaseDog() : void [delete myDogPtr]"
                ]
            }
        ],
        "relationships": [
            {"from": "DogOwnerApp", "to": "Dog", "type": "composes", "label": "dynamically allocates"}
        ]
    },
    "dynamic_array_test": {
        "title": "Dynamic Array Scaling & Memory Leak Prevention",
        "classes": [
            {
                "name": "DynamicArrayTester",
                "stereotype": "<<struct>>",
                "badge": "Dynamic Array",
                "type": "struct",
                "attributes": [
                    "+ pArray : int32_t*",
                    "+ arraySize : size_t"
                ],
                "methods": [
                    "+ allocate(n: size_t) : void",
                    "+ fill(val: int32_t) : void",
                    "+ free() : void [delete[] pArray]"
                ]
            }
        ]
    },
    "drone_fleet": {
        "title": "Drone Class & Fleet Dynamic Manager Model",
        "classes": [
            {
                "name": "Drone",
                "stereotype": "<<class>>",
                "badge": "Telemetry Device",
                "type": "class",
                "attributes": [
                    "- droneId : int32_t",
                    "- batteryLevel : float",
                    "- altitudeMeters : float"
                ],
                "methods": [
                    "+ Drone(id: int, battery: float)",
                    "+ takeOff(targetAlt: float) : void",
                    "+ land() : void",
                    "+ getAltitude() : float const",
                    "+ getBattery() : float const"
                ]
            },
            {
                "name": "DroneFleet",
                "stereotype": "<<class>>",
                "badge": "Fleet Manager",
                "type": "class",
                "attributes": [
                    "- drones : Drone** (Dynamic Pointer Array)",
                    "- fleetSize : size_t"
                ],
                "methods": [
                    "+ DroneFleet(size: size_t)",
                    "+ ~DroneFleet() [frees all drones]",
                    "+ getDrone(idx: size_t) : Drone*"
                ]
            }
        ],
        "relationships": [
            {"from": "DroneFleet", "to": "Drone", "type": "composes", "label": "manages array of drone pointers"}
        ]
    },
    "exhibit_tracker": {
        "title": "Museum Exhibit Revenue & Attendance Tracker Model",
        "classes": [
            {
                "name": "Exhibit",
                "stereotype": "<<class>>",
                "badge": "Exhibit Model",
                "type": "class",
                "attributes": [
                    "- name : std::string",
                    "- visitorsCount : int32_t = 0",
                    "- ticketPriceCents : int32_t"
                ],
                "methods": [
                    "+ Exhibit(name: string, price: int)",
                    "+ recordVisitor() : void",
                    "+ getTotalRevenueCents() : int64_t const",
                    "+ getName() : std::string const"
                ]
            }
        ]
    },

    # =========================================================================
    # SECTION 9: STREAMS & FLASH FILESYSTEMS (7 Projects)
    # =========================================================================
    "file_input_fun": {
        "title": "std::ifstream File Descriptors vs LittleFS Flash NOR Filesystem",
        "classes": [
            {
                "name": "std::ifstream",
                "stereotype": "<<class>>",
                "badge": "Hosted File Stream",
                "type": "class",
                "attributes": [
                    "- file_descriptor : int32_t",
                    "- stream_buffer : std::filebuf"
                ],
                "methods": [
                    "+ open(filename: const char*) : void",
                    "+ is_open() : bool const",
                    "+ close() : void"
                ]
            },
            {
                "name": "LittleFS_Driver",
                "stereotype": "<<embedded-driver>>",
                "badge": "Power-Cut Resilient NOR Flash FS",
                "type": "struct",
                "attributes": [
                    "+ lfs_t : struct lfs",
                    "+ lfs_file_t : struct lfs_file",
                    "+ read_buffer[256] : uint8_t"
                ],
                "methods": [
                    "+ mount() : int32_t",
                    "+ fileOpen(path: const char*, flags: int) : int32_t",
                    "+ fileRead(buf: void*, size: size_t) : lfs_ssize_t",
                    "+ fileClose() : int32_t"
                ]
            }
        ],
        "relationships": [
            {"from": "std::ifstream", "to": "LittleFS_Driver", "type": "uses", "label": "embedded equivalent"}
        ]
    },
    "file_output_fun": {
        "title": "std::ofstream File Writing & Flash Wear-Leveling Model",
        "classes": [
            {
                "name": "std::ofstream",
                "stereotype": "<<class>>",
                "badge": "Hosted Output Stream",
                "type": "class",
                "attributes": [
                    "- file_descriptor : int32_t"
                ],
                "methods": [
                    "+ open(filename: const char*, mode: openmode) : void",
                    "+ write(data: const char*, size: size_t) : ostream&",
                    "+ flush() : ostream&",
                    "+ close() : void"
                ]
            }
        ]
    },
    "twice_file": {
        "title": "File-to-File Stream Transformation Pipeline Model",
        "classes": [
            {
                "name": "TwiceFileProcessor",
                "stereotype": "<<compilation-unit>>",
                "badge": "Stream Pipeline",
                "type": "module",
                "attributes": [
                    "- inFilePath : const char*",
                    "- outFilePath : const char*"
                ],
                "methods": [
                    "+ processDoubling(inFile: const char*, outFile: const char*) : bool"
                ]
            }
        ]
    },
    "names_ages": {
        "title": "Dual-Stream Parsing & Data Merging Model",
        "classes": [
            {
                "name": "PersonRecord",
                "stereotype": "<<struct>>",
                "badge": "Merged Record",
                "type": "struct",
                "attributes": [
                    "+ name : std::string",
                    "+ age : int32_t"
                ],
                "methods": []
            },
            {
                "name": "ParallelStreamMerger",
                "stereotype": "<<compilation-unit>>",
                "badge": "Stream Merger",
                "type": "module",
                "attributes": [
                    "- records : std::vector<PersonRecord>"
                ],
                "methods": [
                    "+ mergeFiles(namesFile: const char*, agesFile: const char*, outFile: const char*) : void"
                ]
            }
        ],
        "relationships": [
            {"from": "ParallelStreamMerger", "to": "PersonRecord", "type": "composes", "label": "creates records"}
        ]
    },
    "movie_genres": {
        "title": "Movie Genre Classifier & File Parsing Architecture",
        "classes": [
            {
                "name": "MovieEntry",
                "stereotype": "<<struct>>",
                "badge": "Catalog Entry",
                "type": "struct",
                "attributes": [
                    "+ title : std::string",
                    "+ genre : std::string"
                ],
                "methods": []
            },
            {
                "name": "MovieGenreParser",
                "stereotype": "<<compilation-unit>>",
                "badge": "Catalog Parser",
                "type": "module",
                "attributes": [
                    "- catalog : std::vector<MovieEntry>"
                ],
                "methods": [
                    "+ parseGenreFile(path: const char*) : void",
                    "+ filterByGenre(genre: string) : void const"
                ]
            }
        ],
        "relationships": [
            {"from": "MovieGenreParser", "to": "MovieEntry", "type": "composes", "label": "populates catalog"}
        ]
    },
    "employee_salary_report": {
        "title": "Employee Salary File Parser & Aggregate Report Model",
        "classes": [
            {
                "name": "EmployeeRecord",
                "stereotype": "<<struct>>",
                "badge": "Payroll Record",
                "type": "struct",
                "attributes": [
                    "+ employeeName : std::string",
                    "+ baseSalaryCents : int64_t",
                    "+ taxWithheldCents : int64_t"
                ],
                "methods": [
                    "+ getNetSalaryCents() : int64_t const"
                ]
            },
            {
                "name": "SalaryReportGenerator",
                "stereotype": "<<compilation-unit>>",
                "badge": "Payroll Engine",
                "type": "module",
                "attributes": [
                    "- employees : std::vector<EmployeeRecord>"
                ],
                "methods": [
                    "+ loadSalaries(path: const char*) : void",
                    "+ printFinancialSummary() : void const"
                ]
            }
        ],
        "relationships": [
            {"from": "SalaryReportGenerator", "to": "EmployeeRecord", "type": "composes", "label": "aggregates"}
        ]
    },
    "student_roster": {
        "title": "Student Class & Persistent Roster File Manager",
        "classes": [
            {
                "name": "Student",
                "stereotype": "<<class>>",
                "badge": "Academic Entity",
                "type": "class",
                "attributes": [
                    "- studentId : int32_t",
                    "- fullName : std::string",
                    "- gpa : double"
                ],
                "methods": [
                    "+ Student(id: int, name: string, gpa: double)",
                    "+ getId() : int32_t const",
                    "+ getName() : std::string const",
                    "+ getGpa() : double const",
                    "+ printStudent() : void const"
                ]
            },
            {
                "name": "RosterManager",
                "stereotype": "<<class>>",
                "badge": "Roster Controller",
                "type": "class",
                "attributes": [
                    "- roster : std::vector<Student>"
                ],
                "methods": [
                    "+ loadRoster(filePath: const char*) : void",
                    "+ saveRoster(filePath: const char*) : void",
                    "+ addStudent(s: const Student&) : void",
                    "+ findStudent(id: int) : Student*"
                ]
            }
        ],
        "relationships": [
            {"from": "RosterManager", "to": "Student", "type": "composes", "label": "manages student roster"}
        ]
    },

    # =========================================================================
    # SECTION 10: OOP, ENUMS & CRTP (3 Projects)
    # =========================================================================
    "enum_fun": {
        "title": "Scoped enum class (uint8_t) & Bitmask Memory Model",
        "classes": [
            {
                "name": "Direction",
                "stereotype": "<<enum class : uint8_t>>",
                "badge": "1-Byte Scoped Enum",
                "type": "struct",
                "attributes": [
                    "+ NORTH : uint8_t = 0",
                    "+ SOUTH : uint8_t = 1",
                    "+ EAST : uint8_t = 2",
                    "+ WEST : uint8_t = 3"
                ],
                "methods": []
            },
            {
                "name": "SystemStatus",
                "stereotype": "<<enum class : uint8_t>>",
                "badge": "Status Enum",
                "type": "struct",
                "attributes": [
                    "+ IDLE : uint8_t = 0",
                    "+ RUNNING : uint8_t = 1",
                    "+ ERROR : uint8_t = 2",
                    "+ FAULT : uint8_t = 3"
                ],
                "methods": []
            },
            {
                "name": "EnumDispatcher",
                "stereotype": "<<compilation-unit>>",
                "badge": "Switch Jump Table",
                "type": "module",
                "attributes": [],
                "methods": [
                    "+ processDirection(dir: Direction) : void",
                    "+ getStatusString(s: SystemStatus) : std::string_view"
                ]
            }
        ],
        "relationships": [
            {"from": "EnumDispatcher", "to": "Direction", "type": "uses", "label": "switches on"},
            {"from": "EnumDispatcher", "to": "SystemStatus", "type": "uses", "label": "switches on"}
        ]
    },
    "animal_fun": {
        "title": "Virtual Table (vtable/vptr) Polymorphism Architecture",
        "classes": [
            {
                "name": "Animal",
                "stereotype": "<<abstract class>>",
                "badge": "Base Class (Has vptr)",
                "type": "abstract",
                "attributes": [
                    "# _vptr : void** (4 bytes hidden RAM pointer)",
                    "# name : std::string",
                    "# weight : double"
                ],
                "methods": [
                    "+ Animal(name: string, weight: double)",
                    "+ getName() : std::string const",
                    "+ getWeight() : double const",
                    "+ makeNoise() : std::string [pure virtual =0]",
                    "+ eat() : void [virtual]",
                    "+ ~Animal() [virtual]"
                ]
            },
            {
                "name": "Dog",
                "stereotype": "<<class>>",
                "badge": "Derived Class",
                "type": "class",
                "attributes": [
                    "- breed : std::string"
                ],
                "methods": [
                    "+ Dog(name: string, weight: double, breed: string)",
                    "+ getBreed() : std::string const",
                    "+ makeNoise() : std::string [override]",
                    "+ digHole() : void",
                    "+ chaseCat() : void"
                ]
            },
            {
                "name": "Cat",
                "stereotype": "<<class>>",
                "badge": "Derived Class",
                "type": "class",
                "attributes": [],
                "methods": [
                    "+ Cat(name: string, weight: double)",
                    "+ makeNoise() : std::string [override]",
                    "+ chaseMouse() : void"
                ]
            }
        ],
        "relationships": [
            {"from": "Dog", "to": "Animal", "type": "inherits", "label": "public inherits (vtable override)"},
            {"from": "Cat", "to": "Animal", "type": "inherits", "label": "public inherits (vtable override)"}
        ]
    },
    "rpg_project": {
        "title": "RPG Polymorphic Character Hierarchy & VTable Architecture",
        "classes": [
            {
                "name": "Race",
                "stereotype": "<<enum class : uint8_t>>",
                "badge": "Character Race",
                "type": "struct",
                "attributes": [
                    "+ HUMAN : uint8_t = 0",
                    "+ ELF : uint8_t = 1",
                    "+ DWARF : uint8_t = 2",
                    "+ ORC : uint8_t = 3",
                    "+ TROLL : uint8_t = 4"
                ],
                "methods": []
            },
            {
                "name": "Player",
                "stereotype": "<<abstract class>>",
                "badge": "Base Class (vtable owner)",
                "type": "abstract",
                "attributes": [
                    "# _vptr : void** (4 bytes)",
                    "# name : std::string",
                    "# race : Race",
                    "# hitPoints : int32_t",
                    "# magicPoints : int32_t"
                ],
                "methods": [
                    "+ Player(name: string, race: Race, hp: int, mp: int)",
                    "+ getName() : std::string const",
                    "+ getRace() : Race const",
                    "+ getHitPoints() : int32_t const",
                    "+ getMagicPoints() : int32_t const",
                    "+ setName(name: string) : void",
                    "+ setRace(race: Race) : void",
                    "+ setHitPoints(hp: int) : void",
                    "+ setMagicPoints(mp: int) : void",
                    "+ attack() : std::string [pure virtual =0]",
                    "+ ~Player() [virtual]"
                ]
            },
            {
                "name": "Warrior",
                "stereotype": "<<class>>",
                "badge": "Melee Subclass",
                "type": "class",
                "attributes": [],
                "methods": [
                    "+ Warrior(name: string, race: Race)",
                    "+ attack() : std::string [override]"
                ]
            },
            {
                "name": "Mage",
                "stereotype": "<<class>>",
                "badge": "Caster Subclass",
                "type": "class",
                "attributes": [],
                "methods": [
                    "+ Mage(name: string, race: Race)",
                    "+ attack() : std::string [override]"
                ]
            },
            {
                "name": "Priest",
                "stereotype": "<<class>>",
                "badge": "Healer Subclass",
                "type": "class",
                "attributes": [],
                "methods": [
                    "+ Priest(name: string, race: Race)",
                    "+ attack() : std::string [override]"
                ]
            }
        ],
        "relationships": [
            {"from": "Player", "to": "Race", "type": "composes", "label": "holds race"},
            {"from": "Warrior", "to": "Player", "type": "inherits", "label": "inherits (virtual attack)"},
            {"from": "Mage", "to": "Player", "type": "inherits", "label": "inherits (virtual attack)"},
            {"from": "Priest", "to": "Player", "type": "inherits", "label": "inherits (virtual attack)"}
        ]
    },

    # =========================================================================
    # SECTION 11: TEMPLATES, STL & CRTP (19 Projects)
    # =========================================================================
    "smart_pointer_fun": {
        "title": "std::unique_ptr Exclusive Ownership & Custom RAII Deleter Model",
        "classes": [
            {
                "name": "std::unique_ptr<T, Deleter>",
                "stereotype": "<<template class>>",
                "badge": "Zero-Overhead Smart Pointer",
                "type": "class",
                "attributes": [
                    "- _M_ptr : T* (Single 4-byte pointer)"
                ],
                "methods": [
                    "+ unique_ptr(ptr: T*)",
                    "+ ~unique_ptr() [invokes Deleter]",
                    "+ operator->() : T*",
                    "+ operator*() : T&",
                    "+ release() : T*",
                    "+ reset(p: T* = nullptr) : void"
                ]
            },
            {
                "name": "SpiPeripheral",
                "stereotype": "<<struct>>",
                "badge": "Hardware MMIO Device",
                "type": "struct",
                "attributes": [
                    "+ SPI_CR1 : volatile uint32_t*",
                    "+ SPI_DR : volatile uint32_t*"
                ],
                "methods": [
                    "+ writeByte(b: uint8_t) : void"
                ]
            },
            {
                "name": "SpiDeleter",
                "stereotype": "<<struct (functor)>>",
                "badge": "Hardware Safe-Shutdown",
                "type": "struct",
                "attributes": [],
                "methods": [
                    "+ operator()(spi: SpiPeripheral*) : void const [Gates clock off]"
                ]
            }
        ],
        "relationships": [
            {"from": "std::unique_ptr<T, Deleter>", "to": "SpiPeripheral", "type": "composes", "label": "owns exclusive"},
            {"from": "std::unique_ptr<T, Deleter>", "to": "SpiDeleter", "type": "uses", "label": "executes on scope exit"}
        ]
    },
    "rule_of_three_five_zero": {
        "title": "Rule of Three / Five / Zero Memory Lifecycle Architecture",
        "classes": [
            {
                "name": "RuleOfFiveResource",
                "stereotype": "<<class>>",
                "badge": "Manual Resource Handler",
                "type": "class",
                "attributes": [
                    "- dataPtr : int32_t*",
                    "- bufferSize : size_t"
                ],
                "methods": [
                    "+ RuleOfFiveResource(size: size_t)",
                    "+ ~RuleOfFiveResource() [1. Destructor]",
                    "+ RuleOfFiveResource(const RuleOfFiveResource&) [2. Copy Ctor]",
                    "+ operator=(const RuleOfFiveResource&) : RuleOfFiveResource& [3. Copy Assign]",
                    "+ RuleOfFiveResource(RuleOfFiveResource&&) : noexcept [4. Move Ctor]",
                    "+ operator=(RuleOfFiveResource&&) : RuleOfFiveResource& [5. Move Assign]"
                ]
            },
            {
                "name": "RuleOfZeroResource",
                "stereotype": "<<class>>",
                "badge": "Modern RAII Idiom",
                "type": "class",
                "attributes": [
                    "- buffer : std::vector<int32_t> (Automatic RAII Management)"
                ],
                "methods": [
                    "+ RuleOfZeroResource() = default"
                ]
            }
        ]
    },
    "map_vs_unordered_map": {
        "title": "std::map (Red-Black) vs std::unordered_map (Hash Table) Architecture",
        "classes": [
            {
                "name": "std::map<Key, Value>",
                "stereotype": "<<template class>>",
                "badge": "O(log N) Red-Black Tree",
                "type": "class",
                "attributes": [
                    "- _M_root : _Rb_tree_node*"
                ],
                "methods": [
                    "+ operator[](k: const Key&) : Value& [O(log N)]",
                    "+ insert(p: pair<const Key, Value>) : pair<iterator, bool>"
                ]
            },
            {
                "name": "std::unordered_map<Key, Value>",
                "stereotype": "<<template class>>",
                "badge": "O(1) Hash Table (Unbounded Worst-Case)",
                "type": "class",
                "attributes": [
                    "- _M_buckets : _Hash_node** (Dynamic Bucket Array)"
                ],
                "methods": [
                    "+ operator[](k: const Key&) : Value& [O(1) Avg, O(N) Worst]",
                    "+ rehash(n: size_t) : void"
                ]
            },
            {
                "name": "FlatSortedMap<Key, Value, N>",
                "stereotype": "<<embedded-etl>>",
                "badge": "Zero-Heap Contiguous Flat Map",
                "type": "struct",
                "attributes": [
                    "+ keys[N] : Key",
                    "+ values[N] : Value",
                    "+ count : size_t"
                ],
                "methods": [
                    "+ find(k: Key) : Value* [Binary Search O(log N)]"
                ]
            }
        ],
        "relationships": [
            {"from": "std::map<Key, Value>", "to": "FlatSortedMap<Key, Value, N>", "type": "uses", "label": "embedded deterministic alternative"}
        ]
    },
    "queue_projects": {
        "title": "STL Queue Adapters & Hardware FIFO Ring Buffer Model",
        "classes": [
            {
                "name": "std::queue<T, Container>",
                "stereotype": "<<template class>>",
                "badge": "FIFO Adapter",
                "type": "class",
                "attributes": [
                    "# c : Container (std::deque<T>)"
                ],
                "methods": [
                    "+ push(val: const T&) : void",
                    "+ pop() : void",
                    "+ front() : T&",
                    "+ empty() : bool const"
                ]
            },
            {
                "name": "HardwareRingBuffer<T, N>",
                "stereotype": "<<embedded-driver>>",
                "badge": "Zero-Heap UART FIFO",
                "type": "struct",
                "attributes": [
                    "+ storage[N] : T",
                    "+ head : size_t",
                    "+ tail : size_t"
                ],
                "methods": [
                    "+ write(item: T) : bool",
                    "+ read(item: T&) : bool"
                ]
            }
        ],
        "relationships": [
            {"from": "std::queue<T, Container>", "to": "HardwareRingBuffer<T, N>", "type": "uses", "label": "refactors to in bare-metal"}
        ]
    },
    "remove_erase_idiom": {
        "title": "Erase-Remove Idiom & std::erase / std::erase_if (C++20)",
        "classes": [
            {
                "name": "EraseRemovePipeline",
                "stereotype": "<<compilation-unit>>",
                "badge": "Iterator Algorithm",
                "type": "module",
                "attributes": [],
                "methods": [
                    "+ eraseRemoveClassic(vec: vector<int>&, val: int) : void [vec.erase(std::remove(...), vec.end())]",
                    "+ eraseModernCpp20(vec: vector<int>&, val: int) : size_t [std::erase(vec, val)]"
                ]
            }
        ]
    },
    "templates": {
        "title": "Function & Class Template Specialization Architecture",
        "classes": [
            {
                "name": "TemplateEngine",
                "stereotype": "<<template functions>>",
                "badge": "Monomorphization Pipeline",
                "type": "module",
                "attributes": [],
                "methods": [
                    "+ printGeneric<T>(val: const T&) : void",
                    "+ sumGeneric<T>(a: T, b: T) : T"
                ]
            },
            {
                "name": "GenericBox<T>",
                "stereotype": "<<template class>>",
                "badge": "Generic Container",
                "type": "class",
                "attributes": [
                    "- item : T"
                ],
                "methods": [
                    "+ GenericBox(initialItem: const T&)",
                    "+ getItem() : T const",
                    "+ setItem(newItem: const T&) : void"
                ]
            }
        ]
    },
    "rules_challenge": {
        "title": "Rule of Five Dynamic Buffer Challenge Architecture",
        "classes": [
            {
                "name": "Buffer",
                "stereotype": "<<class>>",
                "badge": "Rule of Five Buffer",
                "type": "class",
                "attributes": [
                    "- data : int32_t*",
                    "- size : size_t"
                ],
                "methods": [
                    "+ Buffer(size: size_t)",
                    "+ ~Buffer() [delete[] data]",
                    "+ Buffer(const Buffer&) [Copy Ctor]",
                    "+ operator=(const Buffer&) : Buffer& [Copy Assign]",
                    "+ Buffer(Buffer&&) : noexcept [Move Ctor]",
                    "+ operator=(Buffer&&) : Buffer& [Move Assign]"
                ]
            }
        ]
    },
    "algorithm_fun": {
        "title": "STL Iterator Algorithms: std::sort, std::find, std::count_if",
        "classes": [
            {
                "name": "StlAlgorithmsEngine",
                "stereotype": "<<compilation-unit>>",
                "badge": "Generic Algorithm Pipeline",
                "type": "module",
                "attributes": [],
                "methods": [
                    "+ sort<RandomIt>(first: RandomIt, last: RandomIt) : void [IntroSort]",
                    "+ find_if<InputIt, Pred>(first: InputIt, last: InputIt, p: Pred) : InputIt",
                    "+ transform<InputIt, OutputIt, Op>(first: InputIt, last: InputIt, d_first: OutputIt, op: Op) : OutputIt",
                    "+ count_if<InputIt, Pred>(first: InputIt, last: InputIt, p: Pred) : size_t"
                ]
            }
        ]
    },
    "stl_fun1": {
        "title": "STL Sequential Containers (vector, deque, list) Architecture",
        "classes": [
            {
                "name": "std::vector<T>",
                "stereotype": "<<template class>>",
                "badge": "Contiguous Array",
                "type": "class",
                "attributes": [
                    "- _M_start : T*",
                    "- _M_finish : T*"
                ],
                "methods": [
                    "+ push_back(val: const T&) : void",
                    "+ operator[](idx: size_t) : T&"
                ]
            },
            {
                "name": "std::deque<T>",
                "stereotype": "<<template class>>",
                "badge": "Chunked Map",
                "type": "class",
                "attributes": [
                    "- _M_map : T**"
                ],
                "methods": [
                    "+ push_front(val: const T&) : void",
                    "+ push_back(val: const T&) : void"
                ]
            },
            {
                "name": "std::list<T>",
                "stereotype": "<<template class>>",
                "badge": "Doubly-Linked List",
                "type": "class",
                "attributes": [
                    "- _M_node : _List_node_base"
                ],
                "methods": [
                    "+ insert(pos: iterator, val: const T&) : iterator",
                    "+ erase(pos: iterator) : iterator"
                ]
            }
        ]
    },
    "advanced_stl_app": {
        "title": "Associative STL Trees (std::set, std::map) Architecture",
        "classes": [
            {
                "name": "std::set<Key>",
                "stereotype": "<<template class>>",
                "badge": "Red-Black Tree",
                "type": "class",
                "attributes": [
                    "- _M_t : _Rb_tree<Key, Key, ...>"
                ],
                "methods": [
                    "+ insert(val: const Key&) : pair<iterator, bool>",
                    "+ find(k: const Key&) : iterator"
                ]
            },
            {
                "name": "std::map<Key, Value>",
                "stereotype": "<<template class>>",
                "badge": "Red-Black KV Tree",
                "type": "class",
                "attributes": [
                    "- _M_tree : _Rb_tree<Key, pair<const Key, Value>, ...>"
                ],
                "methods": [
                    "+ operator[](k: const Key&) : Value&",
                    "+ find(k: const Key&) : iterator"
                ]
            }
        ]
    },
    "advanced_stl_challenge_app": {
        "title": "Complex STL Functors & Lambda Expression Pipelines",
        "classes": [
            {
                "name": "AdvancedStlPipeline",
                "stereotype": "<<compilation-unit>>",
                "badge": "Pipeline Controller",
                "type": "module",
                "attributes": [
                    "- dataStore : std::map<std::string, std::vector<int32_t>>"
                ],
                "methods": [
                    "+ computeAggregates() : void",
                    "+ filterData(pred: std::function<bool(int)>) : void"
                ]
            }
        ]
    },
    "car_project": {
        "title": "Car Class Encapsulation & Automotive Control State Model",
        "classes": [
            {
                "name": "Car",
                "stereotype": "<<class>>",
                "badge": "Vehicle Model",
                "type": "class",
                "attributes": [
                    "- make : std::string",
                    "- model : std::string",
                    "- year : int32_t",
                    "- speedMph : int32_t = 0"
                ],
                "methods": [
                    "+ Car(make: string, model: string, year: int)",
                    "+ accelerate(amount: int) : void",
                    "+ brake(amount: int) : void",
                    "+ getSpeed() : int32_t const",
                    "+ printCarDetails() : void const"
                ]
            }
        ]
    },
    "contacts_fun": {
        "title": "Contact Book Associative std::map Architecture",
        "classes": [
            {
                "name": "Contact",
                "stereotype": "<<struct>>",
                "badge": "Contact Record",
                "type": "struct",
                "attributes": [
                    "+ name : std::string",
                    "+ phone : std::string",
                    "+ email : std::string"
                ],
                "methods": [
                    "+ printContact() : void const"
                ]
            },
            {
                "name": "ContactBook",
                "stereotype": "<<class>>",
                "badge": "Address Book",
                "type": "class",
                "attributes": [
                    "- contacts : std::map<std::string, Contact>"
                ],
                "methods": [
                    "+ addContact(c: const Contact&) : void",
                    "+ findContact(name: string) : Contact*",
                    "+ removeContact(name: string) : bool",
                    "+ displayAll() : void const"
                ]
            }
        ],
        "relationships": [
            {"from": "ContactBook", "to": "Contact", "type": "composes", "label": "maps name to contact"}
        ]
    },
    "crop_hybridization_simulator": {
        "title": "Crop Hybridization Genetic Operator Architecture",
        "classes": [
            {
                "name": "Crop",
                "stereotype": "<<class>>",
                "badge": "Agricultural Model",
                "type": "class",
                "attributes": [
                    "- cropName : std::string",
                    "- yieldPerAcre : double",
                    "- diseaseResistance : double"
                ],
                "methods": [
                    "+ Crop(name: string, yield: double, resist: double)",
                    "+ hybridizeWith(other: const Crop&) : Crop",
                    "+ printCrop() : void const",
                    "+ getYield() : double const",
                    "+ getResistance() : double const"
                ]
            }
        ]
    },
    "friend_fun": {
        "title": "Friend Classes & Private Encapsulation Bypass Mechanics",
        "classes": [
            {
                "name": "Rectangle",
                "stereotype": "<<class>>",
                "badge": "Encapsulated Entity",
                "type": "class",
                "attributes": [
                    "- length : double",
                    "- width : double"
                ],
                "methods": [
                    "+ Rectangle(l: double, w: double)",
                    "+ friend class RectangleHelper"
                ]
            },
            {
                "name": "RectangleHelper",
                "stereotype": "<<class>>",
                "badge": "Friend Utility",
                "type": "class",
                "attributes": [],
                "methods": [
                    "+ modifyDimensions(r: Rectangle&, l: double, w: double) : void [Direct Private Access]",
                    "+ printDiagnostics(r: const Rectangle&) : void"
                ]
            }
        ],
        "relationships": [
            {"from": "RectangleHelper", "to": "Rectangle", "type": "uses", "label": "granted friend access to private fields"}
        ]
    },
    "language_translator_project": {
        "title": "Language Translator & Dictionary Lookup Architecture",
        "classes": [
            {
                "name": "LanguageTranslator",
                "stereotype": "<<class>>",
                "badge": "Translator Engine",
                "type": "class",
                "attributes": [
                    "- dictionary : std::map<std::string, std::string>"
                ],
                "methods": [
                    "+ addWordPair(source: string, target: string) : void",
                    "+ translate(source: string) : std::string const",
                    "+ containsWord(source: string) : bool const"
                ]
            }
        ]
    },
    "overloading_fun": {
        "title": "Operator Overloading (+, ==, !=, <<) on Rectangle Class",
        "classes": [
            {
                "name": "Rectangle",
                "stereotype": "<<class>>",
                "badge": "Overloaded Entity",
                "type": "class",
                "attributes": [
                    "- length : double",
                    "- width : double"
                ],
                "methods": [
                    "+ Rectangle(l: double, w: double)",
                    "+ operator+(other: const Rectangle&) : Rectangle const",
                    "+ operator==(other: const Rectangle&) : bool const",
                    "+ operator!=(other: const Rectangle&) : bool const",
                    "+ friend operator<<(os: ostream&, r: const Rectangle&) : ostream&"
                ]
            }
        ]
    },
    "stack_fun": {
        "title": "std::stack Container Adapter (LIFO) Model",
        "classes": [
            {
                "name": "std::stack<T, Container>",
                "stereotype": "<<template class>>",
                "badge": "LIFO Adapter",
                "type": "class",
                "attributes": [
                    "# c : Container (defaults to std::deque<T>)"
                ],
                "methods": [
                    "+ push(val: const T&) : void [calls c.push_back]",
                    "+ pop() : void [calls c.pop_back]",
                    "+ top() : T& [calls c.back]",
                    "+ empty() : bool const",
                    "+ size() : size_t const"
                ]
            }
        ]
    },
    "swapper_test": {
        "title": "Templated Swapper<T> Generic Pair Manipulation Model",
        "classes": [
            {
                "name": "Swapper<T>",
                "stereotype": "<<template class>>",
                "badge": "Generic Swapper",
                "type": "class",
                "attributes": [
                    "- first : T",
                    "- second : T"
                ],
                "methods": [
                    "+ Swapper(a: const T&, b: const T&)",
                    "+ swap() : void [std::swap(first, second)]",
                    "+ getFirst() : T const",
                    "+ getSecond() : T const"
                ]
            }
        ]
    },

    # =========================================================================
    # SECTION 12: DATA STRUCTURES DEEP-DIVE (10 Projects)
    # =========================================================================
    "array_queue_app": {
        "title": "ArrayQueue Fixed Circular Ring Buffer Architecture",
        "classes": [
            {
                "name": "Queue<T>",
                "stereotype": "<<interface>>",
                "badge": "Queue Interface Contract",
                "type": "abstract",
                "attributes": [],
                "methods": [
                    "+ enqueue(item: const T&) : bool [pure virtual =0]",
                    "+ dequeue() : bool [pure virtual =0]",
                    "+ peekFront() : T const [pure virtual =0]",
                    "+ isEmpty() : bool const [pure virtual =0]",
                    "+ ~Queue() [virtual]"
                ]
            },
            {
                "name": "ArrayQueue<T>",
                "stereotype": "<<template class>>",
                "badge": "Circular Ring Buffer",
                "type": "class",
                "attributes": [
                    "- items[CAPACITY] : T (Contiguous Array)",
                    "- front : int32_t = 0",
                    "- back : int32_t = CAPACITY - 1",
                    "- count : size_t = 0",
                    "+ DEFAULT_CAPACITY : constexpr size_t = 5"
                ],
                "methods": [
                    "+ ArrayQueue()",
                    "+ enqueue(newEntry: const T&) : bool [override, O(1)]",
                    "+ dequeue() : bool [override, O(1)]",
                    "+ peekFront() : T const [override, O(1)]",
                    "+ isEmpty() : bool const [override, O(1)]",
                    "+ isFull() : bool const [O(1)]",
                    "+ size() : size_t const [O(1)]"
                ]
            }
        ],
        "relationships": [
            {"from": "ArrayQueue<T>", "to": "Queue<T>", "type": "implements", "label": "implements interface"}
        ]
    },
    "array_list_app": {
        "title": "ArrayList Contiguous Sequential List Architecture",
        "classes": [
            {
                "name": "List<T>",
                "stereotype": "<<interface>>",
                "badge": "List Interface Contract",
                "type": "abstract",
                "attributes": [],
                "methods": [
                    "+ insert(pos: int, entry: const T&) : bool [pure virtual =0]",
                    "+ remove(pos: int) : bool [pure virtual =0]",
                    "+ getEntry(pos: int) : T const [pure virtual =0]",
                    "+ isEmpty() : bool const [pure virtual =0]",
                    "+ getLength() : size_t const [pure virtual =0]",
                    "+ ~List() [virtual]"
                ]
            },
            {
                "name": "ArrayList<T>",
                "stereotype": "<<template class>>",
                "badge": "Contiguous List",
                "type": "class",
                "attributes": [
                    "- items[CAPACITY] : T",
                    "- itemCount : size_t = 0",
                    "- maxItems : size_t = CAPACITY"
                ],
                "methods": [
                    "+ ArrayList()",
                    "+ insert(newPosition: int, newEntry: const T&) : bool [override, O(N) Shift]",
                    "+ remove(position: int) : bool [override, O(N) Shift]",
                    "+ getEntry(position: int) : T const [override, O(1)]",
                    "+ replace(position: int, newEntry: const T&) : T [O(1)]",
                    "+ clear() : void [O(1)]",
                    "+ isEmpty() : bool const [override]",
                    "+ getLength() : size_t const [override]"
                ]
            }
        ],
        "relationships": [
            {"from": "ArrayList<T>", "to": "List<T>", "type": "implements", "label": "implements interface"}
        ]
    },
    "array_stack_app": {
        "title": "ArrayStack LIFO Fixed Memory Architecture",
        "classes": [
            {
                "name": "Stack<T>",
                "stereotype": "<<interface>>",
                "badge": "Stack Interface Contract",
                "type": "abstract",
                "attributes": [],
                "methods": [
                    "+ push(entry: const T&) : bool [pure virtual =0]",
                    "+ pop() : bool [pure virtual =0]",
                    "+ peek() : T const [pure virtual =0]",
                    "+ isEmpty() : bool const [pure virtual =0]",
                    "+ ~Stack() [virtual]"
                ]
            },
            {
                "name": "ArrayStack<T>",
                "stereotype": "<<template class>>",
                "badge": "LIFO Array Stack",
                "type": "class",
                "attributes": [
                    "- items[CAPACITY] : T",
                    "- top : int32_t = -1",
                    "+ MAX_STACK : constexpr size_t = 10"
                ],
                "methods": [
                    "+ ArrayStack()",
                    "+ push(newEntry: const T&) : bool [override, O(1)]",
                    "+ pop() : bool [override, O(1)]",
                    "+ peek() : T const [override, O(1)]",
                    "+ isEmpty() : bool const [override, O(1)]"
                ]
            }
        ],
        "relationships": [
            {"from": "ArrayStack<T>", "to": "Stack<T>", "type": "implements", "label": "implements interface"}
        ]
    },
    "linked_chain_fun": {
        "title": "LinkedChain Node Pointer-Chaining Architecture",
        "classes": [
            {
                "name": "Node<T>",
                "stereotype": "<<struct>>",
                "badge": "Chain Node",
                "type": "struct",
                "attributes": [
                    "+ item : T",
                    "+ next : Node<T>* (Heap pointer)"
                ],
                "methods": [
                    "+ Node(anItem: const T&)",
                    "+ Node(anItem: const T&, nextNodePtr: Node<T>*)"
                ]
            },
            {
                "name": "LinkedChain<T>",
                "stereotype": "<<template class>>",
                "badge": "Pointer Chain",
                "type": "class",
                "attributes": [
                    "- headPtr : Node<T>*",
                    "- itemCount : size_t"
                ],
                "methods": [
                    "+ LinkedChain()",
                    "+ ~LinkedChain()",
                    "+ add(newEntry: const T&) : bool",
                    "+ remove(anEntry: const T&) : bool",
                    "+ clear() : void",
                    "+ contains(anEntry: const T&) : bool const",
                    "+ getLength() : size_t const"
                ]
            }
        ],
        "relationships": [
            {"from": "LinkedChain<T>", "to": "Node<T>", "type": "composes", "label": "chains nodes"}
        ]
    },
    "linked_list_app": {
        "title": "LinkedList Dynamic Pointer-Linked Sequential List",
        "classes": [
            {
                "name": "ListNode<T>",
                "stereotype": "<<struct>>",
                "badge": "Linked Node",
                "type": "struct",
                "attributes": [
                    "+ item : T",
                    "+ next : ListNode<T>*"
                ],
                "methods": [
                    "+ ListNode(item: const T&, next: ListNode<T>* = nullptr)"
                ]
            },
            {
                "name": "LinkedList<T>",
                "stereotype": "<<template class>>",
                "badge": "Dynamic Linked List",
                "type": "class",
                "attributes": [
                    "- headPtr : ListNode<T>*",
                    "- itemCount : size_t = 0"
                ],
                "methods": [
                    "+ LinkedList()",
                    "+ ~LinkedList()",
                    "+ insert(newPosition: int, newEntry: const T&) : bool [O(N)]",
                    "+ remove(position: int) : bool [O(N)]",
                    "+ getEntry(position: int) : T const [O(N)]",
                    "+ clear() : void",
                    "+ isEmpty() : bool const",
                    "+ getLength() : size_t const"
                ]
            }
        ],
        "relationships": [
            {"from": "LinkedList<T>", "to": "ListNode<T>", "type": "composes", "label": "manages heap chain"}
        ]
    },
    "linked_queue_project": {
        "title": "LinkedQueue FIFO Pointer Queue with Head & Tail Pointers",
        "classes": [
            {
                "name": "QueueNode<T>",
                "stereotype": "<<struct>>",
                "badge": "Queue Node",
                "type": "struct",
                "attributes": [
                    "+ item : T",
                    "+ next : QueueNode<T>*"
                ],
                "methods": []
            },
            {
                "name": "LinkedQueue<T>",
                "stereotype": "<<template class>>",
                "badge": "FIFO Linked Queue",
                "type": "class",
                "attributes": [
                    "- frontPtr : QueueNode<T>*",
                    "- backPtr : QueueNode<T>*"
                ],
                "methods": [
                    "+ LinkedQueue()",
                    "+ ~LinkedQueue()",
                    "+ enqueue(newEntry: const T&) : bool [O(1)]",
                    "+ dequeue() : bool [O(1)]",
                    "+ peekFront() : T const [O(1)]",
                    "+ isEmpty() : bool const"
                ]
            }
        ],
        "relationships": [
            {"from": "LinkedQueue<T>", "to": "QueueNode<T>", "type": "composes", "label": "enqueues & dequeues"}
        ]
    },
    "linked_stack_app": {
        "title": "LinkedStack Dynamic Pointer-Chained LIFO Stack Model",
        "classes": [
            {
                "name": "StackNode<T>",
                "stereotype": "<<struct>>",
                "badge": "Stack Node",
                "type": "struct",
                "attributes": [
                    "+ item : T",
                    "+ next : StackNode<T>*"
                ],
                "methods": []
            },
            {
                "name": "LinkedStack<T>",
                "stereotype": "<<template class>>",
                "badge": "Dynamic LIFO Stack",
                "type": "class",
                "attributes": [
                    "- topPtr : StackNode<T>*"
                ],
                "methods": [
                    "+ LinkedStack()",
                    "+ ~LinkedStack()",
                    "+ push(newEntry: const T&) : bool [O(1)]",
                    "+ pop() : bool [O(1)]",
                    "+ peek() : T const [O(1)]",
                    "+ isEmpty() : bool const"
                ]
            }
        ],
        "relationships": [
            {"from": "LinkedStack<T>", "to": "StackNode<T>", "type": "composes", "label": "pushes onto topPtr"}
        ]
    },
    "list_stack_project": {
        "title": "ListStack Adapter Pattern over LinkedList Backend",
        "classes": [
            {
                "name": "LinkedList<T>",
                "stereotype": "<<template class>>",
                "badge": "Adaptee Container",
                "type": "class",
                "attributes": [
                    "- headPtr : ListNode<T>*",
                    "- itemCount : size_t"
                ],
                "methods": [
                    "+ insert(pos: int, entry: const T&) : bool",
                    "+ remove(pos: int) : bool",
                    "+ getEntry(pos: int) : T const",
                    "+ isEmpty() : bool const"
                ]
            },
            {
                "name": "ListStack<T>",
                "stereotype": "<<template class>>",
                "badge": "Stack Adapter",
                "type": "class",
                "attributes": [
                    "- listPtr : LinkedList<T>*"
                ],
                "methods": [
                    "+ ListStack()",
                    "+ ~ListStack()",
                    "+ push(newEntry: const T&) : bool [delegates to listPtr->insert(1, entry)]",
                    "+ pop() : bool [delegates to listPtr->remove(1)]",
                    "+ peek() : T const [delegates to listPtr->getEntry(1)]",
                    "+ isEmpty() : bool const"
                ]
            }
        ],
        "relationships": [
            {"from": "ListStack<T>", "to": "LinkedList<T>", "type": "composes", "label": "adapts interface (composition)"}
        ]
    },
    "templated_array_stack_app": {
        "title": "TemplatedArrayStack Pure Interface Implementation Architecture",
        "classes": [
            {
                "name": "StackInterface<T>",
                "stereotype": "<<interface>>",
                "badge": "Abstract Stack Contract",
                "type": "abstract",
                "attributes": [],
                "methods": [
                    "+ push(newEntry: const T&) : bool [pure virtual =0]",
                    "+ pop() : bool [pure virtual =0]",
                    "+ peek() : T const [pure virtual =0]",
                    "+ isEmpty() : bool const [pure virtual =0]",
                    "+ ~StackInterface() [virtual]"
                ]
            },
            {
                "name": "TemplatedArrayStack<T>",
                "stereotype": "<<template class>>",
                "badge": "Concrete Array Implementation",
                "type": "class",
                "attributes": [
                    "- items[CAPACITY] : T",
                    "- top : int32_t = -1"
                ],
                "methods": [
                    "+ TemplatedArrayStack()",
                    "+ push(newEntry: const T&) : bool [override]",
                    "+ pop() : bool [override]",
                    "+ peek() : T const [override]",
                    "+ isEmpty() : bool const [override]"
                ]
            }
        ],
        "relationships": [
            {"from": "TemplatedArrayStack<T>", "to": "StackInterface<T>", "type": "implements", "label": "implements interface"}
        ]
    },
    "for_proj12_2_files": {
        "title": "Hierarchical Data Structure Framework (Stack & List Polymorphism)",
        "classes": [
            {
                "name": "List<T>",
                "stereotype": "<<interface>>",
                "badge": "List Contract",
                "type": "abstract",
                "attributes": [],
                "methods": [
                    "+ insert(pos: int, entry: const T&) : bool [pure virtual =0]",
                    "+ remove(pos: int) : bool [pure virtual =0]",
                    "+ getEntry(pos: int) : T const [pure virtual =0]",
                    "+ isEmpty() : bool const [pure virtual =0]",
                    "+ getLength() : size_t const [pure virtual =0]"
                ]
            },
            {
                "name": "LinkedList<T>",
                "stereotype": "<<template class>>",
                "badge": "Linked Implementation",
                "type": "class",
                "attributes": [
                    "- headPtr : Node<T>*",
                    "- itemCount : size_t"
                ],
                "methods": [
                    "+ insert(pos: int, entry: const T&) : bool [override]",
                    "+ remove(pos: int) : bool [override]",
                    "+ getEntry(pos: int) : T const [override]"
                ]
            },
            {
                "name": "Stack<T>",
                "stereotype": "<<interface>>",
                "badge": "Stack Contract",
                "type": "abstract",
                "attributes": [],
                "methods": [
                    "+ push(entry: const T&) : bool [pure virtual =0]",
                    "+ pop() : bool [pure virtual =0]",
                    "+ peek() : T const [pure virtual =0]",
                    "+ isEmpty() : bool const [pure virtual =0]"
                ]
            }
        ],
        "relationships": [
            {"from": "LinkedList<T>", "to": "List<T>", "type": "implements", "label": "implements interface"}
        ]
    }
}

target_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uml_data_definitions.py")
with open(target_file, "w", encoding="utf-8") as f:
    f.write("#!/usr/bin/env python3\n")
    f.write('"""\nComprehensive UML Class & Architectural Models for all 116 Projects\n"""\n\n')
    f.write("UML_DEFINITIONS = ")
    f.write(pprint.pformat(UML_DATA, indent=4, width=120))
    f.write("\n")

print(f"Generated {len(UML_DATA)} UML definitions into {target_file}!")
