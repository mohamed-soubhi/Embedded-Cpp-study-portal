#!/usr/bin/env python3
"""
Section 10 Project Definitions: OOP, Enums & Polymorphism
Contains 3 comprehensive project definitions covering scoped enum classes,
vtable / vptr memory overhead, RTTI disablement, CRTP static polymorphism,
and memory safety in object pooling.
"""

SECTION_10_PROJECTS = [
    {
        "id": "enum_fun",
        "name": "EnumFun",
        "title": "Enumerations & Scoped Enum Classes",
        "headline": "Enumerations: Unscoped vs Scoped Enum Classes in Embedded Systems",
        "emb_class": "emb-high",
        "emb_badge": "⚡ Embedded Relevance: High",
        "tags": ["Scoped Enums", "uint8_t", "Jump Tables", "Memory Alignment", "Hardware Registers"],
        "summary": "Explores the transition from legacy C-style unscoped enum to modern C++11 enum class. Examines type safety, namespace pollution, explicit underlying fixed-width storage (uint8_t), bitmask register definitions, and compiler branch generation (Jump Tables vs Branch Cascades) in microcontroller environments.",
        "files": ["section_10/EnumFun/EnumFun/main.cpp"],
        "concepts_html": """
        <h3>Unscoped Enums vs C++11 Scoped Enums (<code>enum class</code>)</h3>
        <p>In classical C and pre-C++11, an <code>enum</code> exports its enumerators directly into the enclosing lexical scope. This creates severe identifier collisions (e.g., having <code>enum State { IDLE, RUNNING }</code> and <code>enum MotorState { IDLE, ACCELERATING }</code> in the same file triggers a redefinition error).</p>
        
        <div class="table-container">
          <table class="comp-table">
            <thead>
              <tr>
                <th>Feature</th>
                <th>Unscoped <code>enum</code> (C++98)</th>
                <th>Scoped <code>enum class</code> (C++11)</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>Scope</strong></td>
                <td>Leaked into surrounding namespace</td>
                <td>Strictly contained within enum name (<code>Direction::UP</code>)</td>
              </tr>
              <tr>
                <td><strong>Implicit Conversion</strong></td>
                <td>Silently converts to <code>int</code>, <code>bool</code>, <code>double</code></td>
                <td><strong>No implicit conversion</strong> (Requires <code>static_cast&lt;int&gt;</code>)</td>
              </tr>
              <tr>
                <td><strong>Underlying Type</strong></td>
                <td>Compiler-defined (typically signed 32-bit int)</td>
                <td>Default <code>int</code>, or user-specified (e.g., <code>: uint8_t</code>)</td>
              </tr>
              <tr>
                <td><strong>Forward Declaration</strong></td>
                <td>Not allowed in C++98</td>
                <td>Always allowed (improves header build times)</td>
              </tr>
            </tbody>
          </table>
        </div>
        """,
        "embedded_html": """
        <h3>1. Memory Footprint & Structure Packing (RAM Conservation)</h3>
        <p>When an enum is a member of a communication protocol frame or peripheral register struct, unspecified enum types default to 4 bytes on 32-bit architectures (ARM Cortex-M). Specifying an underlying type of <code>uint8_t</code> saves 3 bytes per field and prevents padding alignment overhead.</p>

        <div class="callout callout-tip">
          <h4>💡 Embedded Hardware Tip: Specifying Underlying Types</h4>
          <p>Always specify the underlying fixed-width integer type matching the physical register width:</p>
          <pre class="code-block" style="background:#0d1117; padding:10px; border-radius:6px;">enum class UartBaud : uint8_t {
    B9600   = 0x01,
    B19200  = 0x02,
    B115200 = 0x03
}; // Guaranteed exactly 1 byte in SRAM/Flash!</pre>
        </div>

        <h3>2. Microcontroller Branching: If-Else Cascades vs Jump Tables</h3>
        <p>Sequential <code>if-else</code> chains evaluate conditions linearly ($O(N)$ execution time). When switching over a dense <code>enum class</code>, optimizing compilers emit an ARM <strong>Table Branch Byte (TBB)</strong> instruction, yielding an $O(1)$ Jump Table that executes in constant clock cycles regardless of case count.</p>
        """,
        "refactor_html": """
        <p>Production-grade scoped enum with type-safe bitmask operators for peripheral control:</p>
        <pre class="code-block" style="background:#0d1117; padding:16px; border-radius:8px; border:1px solid #30363d;">#include &lt;cstdint&gt;
#include &lt;type_traits&gt;

// Scoped Enum with explicit 1-byte storage
enum class GpioPin : uint8_t {
    Pin0 = 1 &lt;&lt; 0,
    Pin1 = 1 &lt;&lt; 1,
    Pin2 = 1 &lt;&lt; 2,
    Pin3 = 1 &lt;&lt; 3
};

// Enable bitwise OR operator for type-safe pin masking
constexpr GpioPin operator|(GpioPin a, GpioPin b) noexcept {
    return static_cast&lt;GpioPin&gt;(
        static_cast&lt;std::underlying_type_t&lt;GpioPin&gt;&gt;(a) |
        static_cast&lt;std::underlying_type_t&lt;GpioPin&gt;&gt;(b)
    );
}</pre>
        """,
        "quiz": [
            {
                "question": "What is the primary safety advantage of C++11 'enum class' over traditional C-style 'enum'?",
                "options": [
                    "Scoped enums prevent implicit conversion to integer types and avoid namespace collisions",
                    "Scoped enums automatically execute in separate CPU threads",
                    "Scoped enums allow floating-point values as enumerators",
                    "Scoped enums eliminate the need for switch statements"
                ],
                "correct": 0,
                "explanation": "Scoped enumerations (<code>enum class</code>) are strongly typed. Implicit conversion to integer types is prohibited by the C++ compiler, preventing subtle assignment and arithmetic bugs."
            },
            {
                "question": "Why should embedded software developers explicitly define the underlying type of an enum (e.g. enum class State : uint8_t)?",
                "options": [
                    "To guarantee a deterministic 1-byte memory footprint and prevent struct padding bloat in RAM",
                    "To allow the compiler to overclock the microcontroller",
                    "To enable runtime reflection without RTTI",
                    "To convert the enum into a hardware interrupt handler"
                ],
                "correct": 0,
                "explanation": "By default, an enum may occupy 4 bytes (32-bit int). Specifying <code>uint8_t</code> reduces memory footprint by 75% per instance and ensures protocol serialization compatibility."
            },
            {
                "question": "How does an optimizing compiler execute a 'switch' over dense enum values compared to an 'if-else' cascade on ARM Cortex-M?",
                "options": [
                    "It generates a Jump Table (using TBB/TBH instructions) providing deterministic O(1) execution time",
                    "It calls an operating system API to evaluate conditions",
                    "It converts the switch into an infinite while loop",
                    "It executes all cases simultaneously using SIMD instructions"
                ],
                "correct": 0,
                "explanation": "A dense switch is compiled into an indexed jump table (e.g. <code>TBB [PC, R0]</code> on ARM Thumb-2), achieving single-cycle constant time dispatch rather than sequential comparisons."
            },
            {
                "question": "Can an 'enum class' be forward-declared in a C++ header file?",
                "options": [
                    "Yes, because its underlying size is known at declaration time (default int or explicitly specified)",
                    "No, C++ strictly prohibits forward-declaring any enum type",
                    "Only if the header file includes <iostream>",
                    "Only when compiling with the -O3 optimization flag"
                ],
                "correct": 0,
                "explanation": "Because scoped enums have fixed underlying types (defaulting to <code>int</code> if unspecified), the compiler knows their memory size and permits forward declarations."
            }
        ]
    },
    {
        "id": "animal_fun",
        "name": "AnimalFun",
        "title": "Polymorphism & VTable Mechanics",
        "headline": "Runtime Polymorphism vs Zero-Overhead Static Polymorphism (CRTP)",
        "emb_class": "emb-high",
        "emb_badge": "⚡ Embedded Relevance: Critical",
        "tags": ["VTable", "VPtr", "CRTP", "RTTI", "Dynamic Dispatch", "Flash Overhead"],
        "summary": "Exploring abstract classes, pure virtual functions, and dynamic polymorphism. We analyze the underlying VTable and VPtr memory overhead on ARM Cortex-M, why RTTI is disabled in embedded firmware (-fno-rtti), and how to replace dynamic dispatch with zero-cost CRTP (Curiously Recurring Template Pattern).",
        "files": [
            "section_10/AnimalFun/AnimalFun/main.cpp",
            "section_10/AnimalFun/AnimalFun/Animal.h",
            "section_10/AnimalFun/AnimalFun/Animal.cpp",
            "section_10/AnimalFun/AnimalFun/Dog.h",
            "section_10/AnimalFun/AnimalFun/Dog.cpp",
            "section_10/AnimalFun/AnimalFun/Cat.h",
            "section_10/AnimalFun/AnimalFun/Cat.cpp"
        ],
        "concepts_html": """
        <h3>1. Virtual Functions & Dynamic Dispatch</h3>
        <p>Declaring a method <code>virtual</code> instructs the compiler to perform dynamic dispatch at runtime via a <strong>Virtual Method Table (VTable)</strong>, enabling polymorphic behavior when calling methods through base class pointers.</p>

        <div class="diagram-container">
          <h4>📐 Polymorphic UML Class Hierarchy</h4>
          <div class="uml-grid">
            <div class="uml-class-card">
              <div class="uml-class-header">
                <span class="uml-stereotype">&lt;&lt;abstract&gt;&gt;</span>
                <span class="uml-class-name">Animal</span>
              </div>
              <div class="uml-section">
                <div class="uml-item protected"># name : string</div>
                <div class="uml-item protected"># weight : double</div>
              </div>
              <div class="uml-section">
                <div class="uml-item public">+ makeNoise() : void = 0</div>
                <div class="uml-item public">+ eat() : void</div>
                <div class="uml-item public">+ ~Animal() [virtual]</div>
              </div>
            </div>
            <div class="uml-class-card">
              <div class="uml-class-header">
                <span class="uml-stereotype">&lt;&lt;derived&gt;&gt;</span>
                <span class="uml-class-name">Dog : public Animal</span>
              </div>
              <div class="uml-section">
                <div class="uml-item private">- breed : string</div>
              </div>
              <div class="uml-section">
                <div class="uml-item public">+ makeNoise() : void [override]</div>
                <div class="uml-item public">+ chaseCat() : void</div>
              </div>
            </div>
            <div class="uml-class-card">
              <div class="uml-class-header">
                <span class="uml-stereotype">&lt;&lt;derived&gt;&gt;</span>
                <span class="uml-class-name">Cat : public Animal</span>
              </div>
              <div class="uml-section">
                <div class="uml-item public">+ makeNoise() : void [override]</div>
                <div class="uml-item public">+ chaseMouse() : void</div>
              </div>
            </div>
          </div>
        </div>

        <h3>2. Pure Virtual Functions & Abstract Classes</h3>
        <p>Declaring a method with <code>= 0</code> creates an Abstract Base Class (interface) that cannot be instantiated directly, enforcing contract compliance across derived classes.</p>
        """,
        "embedded_html": """
        <h3>1. The Hidden RAM & Flash Cost of VTables (ARM Architecture)</h3>
        <ul>
          <li><strong>VPtr Overhead:</strong> Every class instance with virtual functions includes a hidden 4-byte (or 8-byte on 64-bit) <code>vptr</code> pointer in SRAM. In an array of 1,000 sensor objects, this wastes 4KB of precious RAM!</li>
          <li><strong>Pointer Chasing Latency:</strong> Virtual calls require two memory dereferences (fetch object <code>vptr</code>, fetch function address from VTable in Flash, then branch via <code>BLX</code>), preventing compiler inlining.</li>
          <li><strong>RTTI Overhead:</strong> Run-Time Type Information adds type descriptor structures to Flash. Embedded firmware compiles with <code>-fno-rtti</code>.</li>
        </ul>
        """,
        "refactor_html": """
        <p>Zero-overhead static polymorphism using the Curiously Recurring Template Pattern (CRTP):</p>
        <pre class="code-block" style="background:#0d1117; padding:16px; border-radius:8px; border:1px solid #30363d;">#include &lt;cstdint&gt;

// CRTP Base Interface: 0 bytes RAM overhead, 0 vtable pointers!
template &lt;typename Derived&gt;
class SensorDriver {
public:
    uint16_t read() noexcept {
        return static_cast&lt;Derived*&gt;(this)-&gt;read_impl(); // Fully inlined!
    }
};

class TemperatureSensor : public SensorDriver&lt;TemperatureSensor&gt; {
public:
    uint16_t read_impl() noexcept {
        return 0x0123; // Direct hardware register read
    }
};</pre>
        """,
        "quiz": [
            {
                "question": "What is the memory overhead introduced to every object instance of a class containing virtual functions on a 32-bit ARM microcontroller?",
                "options": [
                    "A 4-byte virtual table pointer (vptr) stored in the object's RAM allocation",
                    "A copy of the entire compiled machine code in SRAM",
                    "64 bytes of heap metadata",
                    "Zero overhead; virtual functions are resolved entirely at compile time"
                ],
                "correct": 0,
                "explanation": "Each instance of a polymorphic class contains a 4-byte <code>vptr</code> pointing to the class's shared VTable in Flash ROM, increasing object size."
            },
            {
                "question": "Why is dynamic virtual function dispatch often avoided in high-frequency embedded interrupt handlers (ISRs)?",
                "options": [
                    "Indirect branch dereferences (pointer chasing) add CPU latency cycles and prevent compiler function inlining",
                    "Microcontrollers do not support pointers",
                    "Virtual functions can only be called from user space threads",
                    "The ARM ALU cannot perform conditional arithmetic"
                ],
                "correct": 0,
                "explanation": "Virtual calls require dereferencing the <code>vptr</code> and table index, introducing indirect branch latency and defeating compiler inlining optimizations."
            },
            {
                "question": "What is the Curiously Recurring Template Pattern (CRTP) used for in embedded C++ systems?",
                "options": [
                    "To achieve static (compile-time) polymorphism with zero RAM vptr overhead and complete function inlining",
                    "To dynamically allocate memory from external SPI RAM",
                    "To debug hardware trace registers over JTAG",
                    "To emulate an operating system kernel"
                ],
                "correct": 0,
                "explanation": "CRTP uses template inheritance to resolve polymorphic interface calls at compile time, eliminating VTables, VPtrs, and indirect branch penalties entirely."
            },
            {
                "question": "Which compiler flag disables Run-Time Type Information to reduce Flash binary size in embedded systems?",
                "options": ["-fno-rtti", "-fno-exceptions", "-O3", "-nostdlib"],
                "correct": 0,
                "explanation": "The <code>-fno-rtti</code> flag disables generation of typeinfo metadata tables in Flash ROM, reducing binary footprint when dynamic_cast is unused."
            }
        ]
    },
    {
        "id": "rpg_project",
        "name": "RPGProject",
        "title": "Class Hierarchies & Memory Safety",
        "headline": "Class Hierarchies, Member Initializers & Deterministic Object Pooling",
        "emb_class": "emb-high",
        "emb_badge": "⚡ Embedded Relevance: High",
        "tags": ["OOP", "Virtual Destructors", "Object Pools", "Member Initializer", "Deterministic Memory"],
        "summary": "Building complete class hierarchies with character progression systems. We analyze constructor member initialization lists, virtual destructor safety against memory leaks, and replacing dynamic heap allocations with static deterministic object pools in safety-critical firmware.",
        "files": [
            "section_10/RPGProject/RPGProject/main.cpp",
            "section_10/RPGProject/RPGProject/Player.h",
            "section_10/RPGProject/RPGProject/Player.cpp",
            "section_10/RPGProject/RPGProject/Mage.h",
            "section_10/RPGProject/RPGProject/Mage.cpp",
            "section_10/RPGProject/RPGProject/Warrior.h",
            "section_10/RPGProject/RPGProject/Warrior.cpp",
            "section_10/RPGProject/RPGProject/Priest.h",
            "section_10/RPGProject/RPGProject/Priest.cpp"
        ],
        "concepts_html": """
        <h3>1. Member Initializer Lists</h3>
        <p>Initializing member variables in constructor initialization lists directly initializes members rather than default-constructing and then assigning, eliminating redundant operations.</p>

        <div class="diagram-container">
          <h4>📐 RPG Class Hierarchy UML Architecture</h4>
          <div class="uml-grid">
            <div class="uml-class-card">
              <div class="uml-class-header">
                <span class="uml-stereotype">&lt;&lt;base&gt;&gt;</span>
                <span class="uml-class-name">Player</span>
              </div>
              <div class="uml-section">
                <div class="uml-item protected"># name : string</div>
                <div class="uml-item protected"># hitPoints : int</div>
                <div class="uml-item protected"># magicPoints : int</div>
              </div>
              <div class="uml-section">
                <div class="uml-item public">+ attack() : string [virtual]</div>
                <div class="uml-item public">+ ~Player() [virtual]</div>
              </div>
            </div>
            <div class="uml-class-card">
              <div class="uml-class-header">
                <span class="uml-stereotype">&lt;&lt;specialization&gt;&gt;</span>
                <span class="uml-class-name">Warrior : public Player</span>
              </div>
              <div class="uml-section">
                <div class="uml-item public">+ attack() : string [override]</div>
              </div>
            </div>
            <div class="uml-class-card">
              <div class="uml-class-header">
                <span class="uml-stereotype">&lt;&lt;specialization&gt;&gt;</span>
                <span class="uml-class-name">Mage : public Player</span>
              </div>
              <div class="uml-section">
                <div class="uml-item public">+ attack() : string [override]</div>
              </div>
            </div>
            <div class="uml-class-card">
              <div class="uml-class-header">
                <span class="uml-stereotype">&lt;&lt;specialization&gt;&gt;</span>
                <span class="uml-class-name">Priest : public Player</span>
              </div>
              <div class="uml-section">
                <div class="uml-item public">+ attack() : string [override]</div>
              </div>
            </div>
          </div>
        </div>

        <h3>2. Virtual Destructors</h3>
        <p>When deleting a derived class object through a base class pointer (<code>Base* ptr = new Derived(); delete ptr;</code>), the base class destructor <strong>must be virtual</strong>; otherwise, the derived class destructor is not called, causing silent resource leaks.</p>
        """,
        "embedded_html": """
        <h3>1. Static Object Pooling vs Dynamic Heap Allocation</h3>
        <p>In safety-critical avionics and medical devices (DO-178C / IEC 62304), dynamic heap allocation during runtime is prohibited due to fragmentation and non-deterministic allocation latency. Pre-allocating objects in a <strong>Fixed-Block Object Pool</strong> guarantees $O(1)$ allocation time and zero fragmentation.</p>
        """,
        "refactor_html": """
        <p>Fixed-capacity deterministic static object pool:</p>
        <pre class="code-block" style="background:#0d1117; padding:16px; border-radius:8px; border:1px solid #30363d;">#include &lt;cstdint&gt;
#include &lt;array&gt;

template &lt;typename T, size_t Capacity&gt;
class StaticObjectPool {
private:
    alignas(T) uint8_t storage_[Capacity][sizeof(T)];
    std::array&lt;bool, Capacity&gt; in_use_{};

public:
    template &lt;typename... Args&gt;
    T* allocate(Args&amp;&amp;... args) noexcept {
        for (size_t i = 0; i &lt; Capacity; ++i) {
            if (!in_use_[i]) {
                in_use_[i] = true;
                return new (&amp;storage_[i]) T(std::forward&lt;Args&gt;(args)...); // Placement new
            }
        }
        return nullptr; // Pool exhausted (predictable failure!)
    }
};</pre>
        """,
        "quiz": [
            {
                "question": "What happens if a base class does NOT have a virtual destructor and a derived object is deleted via a base class pointer?",
                "options": [
                    "Undefined behavior: the derived class destructor is not executed, leading to resource/memory leaks",
                    "The compiler generates a compilation error",
                    "The CPU automatically calls free() on all members",
                    "The object is moved to Flash memory"
                ],
                "correct": 0,
                "explanation": "Without a virtual destructor, <code>delete base_ptr</code> performs static binding, calling only the base destructor and leaving derived members uncleaned."
            },
            {
                "question": "Why are constructor Member Initializer Lists preferred over assignment inside the constructor body?",
                "options": [
                    "They construct members directly in-place, avoiding redundant default-construction followed by assignment",
                    "They allow calling virtual functions safely",
                    "They place objects in the CPU cache",
                    "They disable compiler optimizations"
                ],
                "correct": 0,
                "explanation": "Initializer lists construct members directly with their target arguments, preventing duplicate default constructor + copy assignment overhead."
            },
            {
                "question": "Why do safety-critical standards like MISRA C++ and DO-178C ban dynamic heap allocation (malloc/new) during real-time operation?",
                "options": [
                    "Heap allocation is non-deterministic (variable allocation time) and can fail due to memory fragmentation over extended operational lifetimes",
                    "Heap memory is slower than Flash memory",
                    "ARM microcontrollers cannot run code with pointers",
                    "Heap memory requires high voltage"
                ],
                "correct": 0,
                "explanation": "Heap managers have non-deterministic $O(N)$ worst-case search times and suffer from fragmentation, which can cause sudden allocation failures in mission-critical firmware."
            },
            {
                "question": "What C++ mechanism allows constructing an object inside pre-allocated static memory without calling the heap allocator?",
                "options": ["Placement new: new (buffer_ptr) Type(args...)", "reinterpret_cast", "std::malloc", "static_cast"],
                "correct": 0,
                "explanation": "Placement new constructs an object in-place at a specified memory address without allocating heap memory."
            }
        ]
    }
]
