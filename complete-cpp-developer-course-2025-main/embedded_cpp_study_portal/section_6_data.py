#!/usr/bin/env python3
"""
Section 6 Project Definitions: OOP Foundations, Classes & Memory Layout
Contains 6 comprehensive project definitions covering object memory layout,
struct alignment and padding (alignas, #pragma pack), encapsulation, constructors/destructors,
and preventing the static initialization order fiasco in bare-metal bootloaders.
"""

SECTION_6_PROJECTS = [
    {
        "id": "book_fun",
        "name": "BookFun",
        "title": "Class Encapsulation, Getters/Setters & Struct Memory Layout",
        "headline": "Classes vs Structs, Encapsulation & Member Variable Memory Alignment in RAM",
        "emb_class": "emb-high",
        "emb_badge": "⚡ Embedded Relevance: High",
        "tags": ["Classes vs Structs", "Encapsulation", "Struct Padding", "Memory Alignment", "alignas"],
        "summary": "Exploring foundational C++ classes: access specifiers (public vs private), member functions, constructors, and encapsulation. We examine the exact memory layout of class instances in SRAM, how compiler alignment rules insert hidden padding bytes, and how to reorder member variables to minimize RAM consumption.",
        "files": [
            "section_6/BookFun/BookFun/main.cpp",
            "section_6/BookFun/BookFun/Book.h",
            "section_6/BookFun/BookFun/Book.cpp"
        ],
        "concepts_html": """
        <h3>1. Classes vs Structs in C++</h3>
        <p>In C++, the only difference between <code>class</code> and <code>struct</code> is the default access level: members and base classes default to <strong>private</strong> in a class, and <strong>public</strong> in a struct.</p>

        <div class="diagram-container">
          <h4>📐 Book Class UML Architecture</h4>
          <div class="uml-grid">
            <div class="uml-class-card">
              <div class="uml-class-header">
                <span class="uml-stereotype">&lt;&lt;entity&gt;&gt;</span>
                <span class="uml-class-name">Book</span>
              </div>
              <div class="uml-section">
                <div class="uml-item private">- author : string</div>
                <div class="uml-item private">- title : string</div>
                <div class="uml-item private">- numPages : int</div>
              </div>
              <div class="uml-section">
                <div class="uml-item public">+ Book(author, title, numPages)</div>
                <div class="uml-item public">+ printBookDetails() : void</div>
                <div class="uml-item public">+ getAuthor() : string const</div>
                <div class="uml-item public">+ getTitle() : string const</div>
                <div class="uml-item public">+ getNumPages() : int const</div>
              </div>
            </div>
          </div>
        </div>

        <h3>2. Encapsulation & Invariants</h3>
        <p>Private member variables enforce data hiding; public member functions validate inputs and preserve object invariants.</p>
        """,
        "embedded_html": """
        <h3>1. Struct Padding & Hidden RAM Waste</h3>
        <p>On 32-bit microcontrollers, variables are aligned to their natural boundaries (4 bytes for <code>uint32_t</code>, 2 bytes for <code>uint16_t</code>). Declaring members in suboptimal order forces the compiler to insert <strong>padding bytes</strong>:</p>
        <pre class="code-block" style="background:#0d1117; padding:12px; border-radius:6px;">struct BadOrder {
    uint8_t  flag1;    // 1 byte + 3 PADDING bytes!
    uint32_t address;  // 4 bytes
    uint8_t  flag2;    // 1 byte + 3 PADDING bytes!
}; // Total size: 12 bytes (6 bytes wasted on padding!)

struct GoodOrder {
    uint32_t address;  // 4 bytes
    uint8_t  flag1;    // 1 byte
    uint8_t  flag2;    // 1 byte + 2 PADDING bytes
}; // Total size: 8 bytes (33% RAM savings!)</pre>
        """,
        "refactor_html": """
        <p>Optimized, compact embedded device metadata class:</p>
        <pre class="code-block" style="background:#0d1117; padding:16px; border-radius:8px; border:1px solid #30363d;">#include &lt;cstdint&gt;
#include &lt;string_view&gt;
#include &lt;array&gt;

class EmbeddedBookRecord {
private:
    // Arranged from largest to smallest type to eliminate internal padding
    uint32_t page_count_{0};
    uint16_t publication_year_{0};
    uint8_t  edition_{1};
    uint8_t  is_checked_out_{0};
    std::array&lt;char, 24&gt; title_{};

public:
    constexpr EmbeddedBookRecord(uint32_t pages, uint16_t year, std::string_view title) noexcept
        : page_count_(pages), publication_year_(year) {
        size_t len = title.size() &lt; 23 ? title.size() : 23;
        for (size_t i = 0; i &lt; len; ++i) title_[i] = title[i];
        title_[len] = '\\0';
    }

    constexpr uint32_t pages() const noexcept { return page_count_; }
    constexpr std::string_view title() const noexcept { return title_.data(); }
};</pre>
        """,
        "quiz": [
            {
                "question": "What is the ONLY difference between 'class' and 'struct' in C++?",
                "options": ["Members of a struct default to public, while members of a class default to private", "Structs cannot have member functions", "Classes are stored on the heap while structs are on the stack", "Structs cannot use templates"],
                "correct": 0,
                "explanation": "In C++, <code>class</code> and <code>struct</code> are identical except for default member and inheritance access specifiers (private for class, public for struct)."
            },
            {
                "question": "Why does the order of member variable declarations in a class matter on 32-bit microcontrollers?",
                "options": ["Suboptimal member ordering forces the compiler to insert alignment padding bytes, bloating the object's RAM footprint", "Member order changes the clock frequency", "Variables declared first are read-only", "Member order changes function return types"],
                "correct": 0,
                "explanation": "CPUs require aligned memory access. Interleaving 1-byte and 4-byte members creates wasted padding holes. Ordering by descending size minimizes padding."
            },
            {
                "question": "On a 32-bit ARM processor, what is the sizeof a struct containing: 'uint8_t a; uint32_t b; uint8_t c;' without packing?",
                "options": ["12 bytes (1 byte + 3 pad + 4 bytes + 1 byte + 3 pad)", "6 bytes", "8 bytes", "4 bytes"],
                "correct": 0,
                "explanation": "Due to 4-byte alignment, 3 padding bytes follow <code>a</code> and 3 padding bytes follow <code>c</code>, yielding $1+3+4+1+3 = 12$ bytes."
            },
            {
                "question": "What compiler attribute or pragma disables alignment padding entirely for network/telemetry packets?",
                "options": ["#pragma pack(push, 1) or __attribute__((packed))", "#pragma inline", "__attribute__((aligned(32)))", "#pragma optimize"],
                "correct": 0,
                "explanation": "<code>__attribute__((packed))</code> or <code>#pragma pack(1)</code> instructs the compiler to omit padding, essential for matching exact binary network wire protocols."
            }
        ]
    },
    {
        "id": "rectangle_fun",
        "name": "RectangleFun",
        "title": "Constructors, Member Initializers & constexpr Computations",
        "headline": "Member Initializer Lists, Invariant Verification & constexpr Geometry Math",
        "emb_class": "emb-core",
        "emb_badge": "⚡ Embedded Relevance: Core",
        "tags": ["Member Initializer List", "constexpr", "OOP", "Const Correctness", "Invariants"],
        "summary": "Building geometric classes with constructors and member initializer lists. We analyze why member initializer lists are strictly more efficient than assignment inside the constructor body, and how to make geometry classes 100% constexpr for compile-time layout calculations.",
        "files": [
            "section_6/RectangleFun/RectangleFun/main.cpp",
            "section_6/RectangleFun/RectangleFun/Rectangle.h",
            "section_6/RectangleFun/RectangleFun/Rectangle.cpp"
        ],
        "concepts_html": """
        <h3>1. Member Initializer Lists vs Body Assignment</h3>
        <p>In a constructor, member initializer lists (<code>Rectangle::Rectangle(double l, double w) : length(l), width(w) {}</code>) initialize members directly when memory is allocated, avoiding double-initialization overhead.</p>

        <div class="diagram-container">
          <h4>📐 Rectangle Class UML Architecture</h4>
          <div class="uml-grid">
            <div class="uml-class-card">
              <div class="uml-class-header">
                <span class="uml-stereotype">&lt;&lt;value-object&gt;&gt;</span>
                <span class="uml-class-name">Rectangle</span>
              </div>
              <div class="uml-section">
                <div class="uml-item private">- length : double</div>
                <div class="uml-item private">- width : double</div>
              </div>
              <div class="uml-section">
                <div class="uml-item public">+ Rectangle()</div>
                <div class="uml-item public">+ Rectangle(l: double, w: double)</div>
                <div class="uml-item public">+ getLength() : double const</div>
                <div class="uml-item public">+ getWidth() : double const</div>
                <div class="uml-item public">+ area() : double const</div>
                <div class="uml-item public">+ perimeter() : double const</div>
              </div>
            </div>
          </div>
        </div>

        <h3>2. <code>const</code> Member Functions</h3>
        <p>Methods that do not modify class state (<code>getLength() const</code>, <code>area() const</code>) must be marked <code>const</code>, allowing them to be called on const objects in Flash ROM.</p>
        """,
        "embedded_html": """
        <h3>1. <code>constexpr</code> Compile-Time Objects</h3>
        <p>Declaring geometry constructors and methods <code>constexpr</code> allows UI display coordinates, bounding boxes, and clip rects to be calculated during compilation, producing <strong>zero runtime CPU cycle overhead</strong>.</p>
        """,
        "refactor_html": """
        <p>100% constexpr UI bounding box class:</p>
        <pre class="code-block" style="background:#0d1117; padding:16px; border-radius:8px; border:1px solid #30363d;">#include &lt;cstdint&gt;

class BoundingBox {
private:
    int16_t x_{0};
    int16_t y_{0};
    uint16_t width_{0};
    uint16_t height_{0};

public:
    constexpr BoundingBox(int16_t x, int16_t y, uint16_t w, uint16_t h) noexcept
        : x_(x), y_(y), width_(w), height_(h) {}

    constexpr uint32_t area() const noexcept { return static_cast&lt;uint32_t&gt;(width_) * height_; }
    constexpr bool contains(int16_t px, int16_t py) const noexcept {
        return (px &gt;= x_ &amp;&amp; px &lt; (x_ + width_) &amp;&amp; py &gt;= y_ &amp;&amp; py &lt; (y_ + height_));
    }
};

// Computed at compile-time and placed in Flash .rodata
constexpr BoundingBox STATUS_BAR_RECT{0, 0, 320, 24};
constexpr uint32_t STATUS_BAR_AREA = STATUS_BAR_RECT.area(); // 7680</pre>
        """,
        "quiz": [
            {
                "question": "Why is using a member initializer list (Class() : member(val) {}) preferred over body assignment (Class() { member = val; })?",
                "options": ["It initializes the member directly during object construction, avoiding default-initialization followed by assignment", "It automatically allocates memory on the heap", "It makes the class abstract", "It disables constructor overloading"],
                "correct": 0,
                "explanation": "Member initializer lists construct fields in-place. Body assignments default-construct the member first and then invoke the assignment operator, wasting cycles for complex objects."
            },
            {
                "question": "In what order are member variables initialized in a C++ class?",
                "options": ["In the exact order they are declared in the class definition, regardless of their order in the constructor initializer list", "In the order listed in the constructor initializer list", "Alphabetical order", "Random order determined by the compiler"],
                "correct": 0,
                "explanation": "C++ strictly specifies that members are initialized in the order of their declaration inside the class body. Compilers with <code>-Wreorder</code> warn if the initializer list is in a different order."
            },
            {
                "question": "What does marking a member function 'const' guarantee?",
                "options": ["The function promises not to modify any non-mutable member variables of the object and can be called on const instances", "The function executes in constant O(1) time", "The function returns a constant pointer", "The function cannot accept parameters"],
                "correct": 0,
                "explanation": "<code>const</code> member functions guarantee that <code>this</code> is a pointer to const, permitting calls on immutable objects stored in Flash memory."
            },
            {
                "question": "Can a constexpr class constructor execute at runtime if passed non-constant arguments?",
                "options": ["Yes, constexpr constructors can run either at compile-time or runtime depending on whether their inputs are constant expressions", "No, constexpr functions only work at compile time", "No, it causes a compilation failure", "Yes, but only in debug mode"],
                "correct": 0,
                "explanation": "<code>constexpr</code> functions and constructors are versatile: when given compile-time constants they evaluate during compilation; when given runtime variables they execute normally at runtime."
            }
        ]
    },
    {
        "id": "houses",
        "name": "Houses",
        "title": "Multiple Object Instances & Memory Stride in SRAM",
        "headline": "Managing Multiple Class Instances, Memory Arrays & Cache Stride",
        "emb_class": "emb-core",
        "emb_badge": "⚡ Embedded Relevance: Core",
        "tags": ["Instances", "Memory Stride", "Array of Objects", "Encapsulation", "State"],
        "summary": "Instantiating and managing multiple distinct class objects. We examine memory footprints of multiple instances in SRAM, contiguous array storage, and avoiding duplicate member storage.",
        "files": [
            "section_6/Houses/Houses/main.cpp",
            "section_6/Houses/Houses/House.h",
            "section_6/Houses/Houses/House.cpp"
        ],
        "concepts_html": """
        <h3>1. Object Independence</h3>
        <p>Each instantiated object owns its distinct set of non-static member variables in memory. Member functions are shared across all instances in Flash (<code>.text</code>), receiving a hidden <code>this</code> pointer to the target object.</p>
        """,
        "embedded_html": """
        <h3>1. The <code>this</code> Pointer in Assembly</h3>
        <p>Under the ARM AAPCS, calling a member function (<code>house.print()</code>) automatically passes the object's memory address as the first argument in <strong>register R0</strong> (the <code>this</code> pointer).</p>
        """,
        "refactor_html": """
        <p>Compact building telemetry node array:</p>
        <pre class="code-block" style="background:#0d1117; padding:16px; border-radius:8px; border:1px solid #30363d;">#include &lt;cstdint&gt;
#include &lt;array&gt;

struct RoomNode {
    uint8_t  room_id;
    int16_t  temp_centi_celsius; // e.g. 2150 = 21.50 C
    uint16_t light_lux;
};

class SmartBuilding {
private:
    std::array&lt;RoomNode, 8&gt; rooms_{};

public:
    void update_sensor(uint8_t room_idx, int16_t temp, uint16_t lux) noexcept {
        if (room_idx &lt; rooms_.size()) {
            rooms_[room_idx].temp_centi_celsius = temp;
            rooms_[room_idx].light_lux = lux;
        }
    }
};</pre>
        """,
        "quiz": [
            {
                "question": "Where is the machine code for a class's non-virtual member functions stored in an embedded system?",
                "options": ["In Flash ROM (.text section), shared once by all instances of that class", "Duplicated in SRAM for each created object instance", "On the CPU stack frame", "In battery-backed RTC memory"],
                "correct": 0,
                "explanation": "Function machine code is stored once in Flash ROM (<code>.text</code>). Objects in RAM contain only their member variables."
            },
            {
                "question": "How is the 'this' pointer passed to member functions in ARM Cortex-M machine code?",
                "options": ["Passed as the implicit first argument in hardware register R0", "Pushed to the bottom of the stack", "Stored in the Program Counter", "Transmitted over the CAN bus"],
                "correct": 0,
                "explanation": "Member functions receive the instance address (<code>this</code>) as an implicit first parameter in register R0."
            },
            {
                "question": "If a class has 3 integer members (12 bytes total) and 10 member functions, what is the sizeof an object instance of this class on a 32-bit MCU?",
                "options": ["12 bytes (member functions add zero bytes to object size)", "52 bytes (12 bytes data + 40 bytes for 10 function pointers)", "4 bytes", "120 bytes"],
                "correct": 0,
                "explanation": "Non-virtual member functions add zero size overhead to object instances. The instance size is strictly the sum of its member variables plus any alignment padding."
            },
            {
                "question": "What is the memory overhead of having 50 instances of the same C++ class in SRAM?",
                "options": ["50 * sizeof(member variables + padding) in SRAM", "50 * sizeof(code + variables)", "Zero bytes", "100 kilobytes"],
                "correct": 0,
                "explanation": "Each instance allocates only its private member variable data in SRAM."
            }
        ]
    },
    {
        "id": "library_card_project",
        "name": "LibraryCardProject",
        "title": "Data Validation, Class Invariants & String References",
        "headline": "Class Invariant Preservation, Setter Input Validation & Small Object Design",
        "emb_class": "emb-core",
        "emb_badge": "⚡ Embedded Relevance: Core",
        "tags": ["Invariants", "Validation", "OOP", "Encapsulation", "State Management"],
        "summary": "Designing classes that enforce strict data validation rules through encapsulation. We analyze invariant preservation in setter methods and modern techniques for managing identity and credentials in embedded IoT devices.",
        "files": [
            "section_6/LibraryCardProject/LibraryCardProject/main.cpp",
            "section_6/LibraryCardProject/LibraryCardProject/LibraryCard.h",
            "section_6/LibraryCardProject/LibraryCardProject/LibraryCard.cpp"
        ],
        "concepts_html": """
        <h3>1. Setter Validation</h3>
        <p>Setters act as gatekeepers, verifying input ranges before mutating private member variables to guarantee the object never enters an invalid state.</p>
        """,
        "embedded_html": """
        <h3>1. Secure Device Identity Storage</h3>
        <p>In IoT edge devices, credentials (e.g. device serial numbers, cryptographic MAC addresses) are validated during provisioning and stored in secure write-once Flash sectors.</p>
        """,
        "refactor_html": """
        <p>Type-safe validated identity class:</p>
        <pre class="code-block" style="background:#0d1117; padding:16px; border-radius:8px; border:1px solid #30363d;">#include &lt;cstdint&gt;
#include &lt;string_view&gt;

class DeviceAuthToken {
private:
    uint32_t device_uid_{0};
    uint16_t security_pin_{0};
    bool     is_valid_{false};

public:
    constexpr bool provision(uint32_t uid, uint16_t pin) noexcept {
        if (uid == 0 || pin &lt; 1000 || pin &gt; 9999) {
            return false; // Invariant violation: PIN must be 4 digits
        }
        device_uid_ = uid;
        security_pin_ = pin;
        is_valid_ = true;
        return true;
    }

    constexpr bool is_authenticated() const noexcept { return is_valid_; }
};</pre>
        """,
        "quiz": [
            {
                "question": "What is an 'object invariant' in class design?",
                "options": ["A condition or rule that must always hold true for an object to remain in a valid, functional state throughout its lifetime", "A variable marked const that cannot be changed", "A function that runs in constant time", "A class with no private members"],
                "correct": 0,
                "explanation": "An invariant is a fundamental truth about an object's state (e.g., speed $\\ge 0$, pointer $\\ne$ null) that constructors establish and methods maintain."
            },
            {
                "question": "Why should member variables generally be kept private with public getters/setters instead of being made public?",
                "options": ["To prevent external code from setting members to invalid/corrupt values, preserving class invariants", "To make the binary file smaller", "To enable multithreading automatically", "To force variables into Flash memory"],
                "correct": 0,
                "explanation": "Private fields force all modifications to pass through validator methods, preventing external corruption of object state."
            },
            {
                "question": "What should a setter function do if passed an invalid argument in an embedded system compiled with -fno-exceptions?",
                "options": ["Reject the mutation and return a boolean false or error status code without changing state", "Execute a busy loop forever", "Overwrite the variable with zero silently", "Restart the CPU"],
                "correct": 0,
                "explanation": "When exceptions are disabled, setters should return a boolean or status code indicating rejection, preserving the existing valid state."
            },
            {
                "question": "What is the benefit of making accessor (getter) methods inline?",
                "options": ["The compiler replaces the function call with direct memory access in assembly, eliminating function call overhead completely", "It converts the getter into a macro", "It allocates getters on the heap", "It allows getters to mutate private members"],
                "correct": 0,
                "explanation": "Inline getters eliminate function call branches (<code>BL</code>/<code>BX LR</code>) in assembly, executing as fast as raw field access while preserving encapsulation."
            }
        ]
    },
    {
        "id": "sundae_project",
        "name": "SundaeProject",
        "title": "Class Composition, Destructors & Embedded Resource Lifecycles",
        "headline": "Object Composition (HAS-A), Destructor Chains & Deterministic Hardware Teardown",
        "emb_class": "emb-core",
        "emb_badge": "⚡ Embedded Relevance: Core",
        "tags": ["Composition", "HAS-A", "Destructors", "RAII", "Hardware Cleanup"],
        "summary": "Building composite objects through composition (HAS-A relationships). We examine constructor and destructor execution chains, and demonstrate how composite RAII classes automatically power down peripherals in reverse order of initialization upon scope exit.",
        "files": [
            "section_6/SundaeProject/SundaeProject/main.cpp",
            "section_6/SundaeProject/SundaeProject/IceCreamSundae.h",
            "section_6/SundaeProject/SundaeProject/IceCreamSundae.cpp"
        ],
        "concepts_html": """
        <h3>1. Object Composition (HAS-A)</h3>
        <p>Composition embeds one class instance inside another as a member variable. The composite object controls the lifetime of its member sub-objects.</p>

        <h3>2. Constructor & Destructor Execution Order</h3>
        <ul>
          <li><strong>Construction:</strong> Member objects are constructed first (in declaration order), followed by the enclosing class constructor body.</li>
          <li><strong>Destruction:</strong> The enclosing class destructor executes first, followed by member destructors in <strong>reverse order</strong> of declaration.</li>
        </ul>
        """,
        "embedded_html": """
        <h3>1. Safe Hardware Peripheral Teardown Chains</h3>
        <p>In power-sensitive embedded systems, RAII composite drivers leverage reverse-order destruction to power down sub-peripherals in strictly safe sequences (e.g. disabling DMA $\\rightarrow$ disabling SPI $\\rightarrow$ gating peripheral clock).</p>
        """,
        "refactor_html": """
        <p>RAII composite sensor subsystem with automatic hardware teardown:</p>
        <pre class="code-block" style="background:#0d1117; padding:16px; border-radius:8px; border:1px solid #30363d;">#include &lt;cstdint&gt;

struct SpiClockGate {
    SpiClockGate() noexcept { /* RCC-&gt;APB2ENR |= SPI1_EN; */ }
    ~SpiClockGate() noexcept { /* RCC-&gt;APB2ENR &amp;= ~SPI1_EN; Disable clock on exit! */ }
};

struct GpioChipSelect {
    GpioChipSelect() noexcept { /* Set CS Pin LOW (Active) */ }
    ~GpioChipSelect() noexcept { /* Set CS Pin HIGH (Idle) */ }
};

class SpiTransactionScope {
private:
    SpiClockGate clock_gate_;      // Constructed 1st; Destroyed 2nd
    GpioChipSelect chip_select_;    // Constructed 2nd; Destroyed 1st
public:
    void write_data(uint8_t byte) noexcept { /* SPI1-&gt;DR = byte; */ }
};</pre>
        """,
        "quiz": [
            {
                "question": "In what order are member sub-objects destroyed when an enclosing class instance goes out of scope?",
                "options": ["In the exact reverse order of their declaration in the class definition", "In the exact order of declaration", "Alphabetical order", "Simultaneously in 1 clock cycle"],
                "correct": 0,
                "explanation": "C++ guarantees that destructors are invoked in reverse order of member declaration, ensuring proper symmetric teardown of dependent resources."
            },
            {
                "question": "What relationship does 'composition' represent in Object-Oriented Design?",
                "options": ["A 'HAS-A' relationship where one class contains instances of other classes as member components", "An 'IS-A' inheritance relationship", "A dynamic link relationship", "A friend class relationship"],
                "correct": 0,
                "explanation": "Composition represents a 'HAS-A' relationship (e.g., a Car HAS-A Engine), where the outer class owns and manages the lifecycle of the inner component."
            },
            {
                "question": "How does RAII (Resource Acquisition Is Initialization) prevent peripheral power drain in battery devices?",
                "options": ["Peripheral clocks and GPIOs are acquired in constructors and automatically powered down in destructors when leaving scope", "It turns off the microcontroller battery", "It decreases the baud rate", "It converts integers to floating point"],
                "correct": 0,
                "explanation": "RAII ties hardware peripheral power states to object lifetimes, guaranteeing that peripherals are safely disabled as soon as their enclosing scope exits."
            },
            {
                "question": "If class A contains member class B, when is B's constructor executed relative to A's constructor body?",
                "options": ["B's constructor is fully executed BEFORE A's constructor body begins", "B's constructor is executed after A's constructor body finishes", "B's constructor is ignored", "Only when explicitly called"],
                "correct": 0,
                "explanation": "All member sub-objects are fully constructed before the body of the enclosing class constructor starts execution."
            }
        ]
    },
    {
        "id": "triangle_project",
        "name": "TriangleProject",
        "title": "Geometry Encapsulation & The Static Initialization Fiasco",
        "headline": "Class Invariant Enforcement & Preventing the Static Initialization Order Fiasco",
        "emb_class": "emb-high",
        "emb_badge": "⚡ Embedded Relevance: Critical",
        "tags": ["Triangle Inequality", "Invariants", "Static Initialization Fiasco", "Construct on First Use", "Bootloader"],
        "summary": "Building validated geometric triangle classes enforcing the Triangle Inequality Theorem. We explore how global object constructors execute during microcontroller startup, and how to prevent the dreaded Static Initialization Order Fiasco using the Construct-On-First-Use idiom.",
        "files": [
            "section_6/TriangleProject/TriangleProject/main.cpp",
            "section_6/TriangleProject/TriangleProject/Triangle.h",
            "section_6/TriangleProject/TriangleProject/Triangle.cpp"
        ],
        "concepts_html": """
        <h3>1. Multi-Field Invariant Enforcement</h3>
        <p>A valid triangle must satisfy the <strong>Triangle Inequality Theorem</strong>: the sum of the lengths of any two sides must be strictly greater than the length of the remaining side ($a + b &gt; c$, $a + c &gt; b$, and $b + c &gt; a$).</p>
        """,
        "embedded_html": """
        <h3>1. The Static Initialization Order Fiasco</h3>
        <p>When multiple global C++ objects exist across different <code>.cpp</code> files, the order in which their constructors execute before <code>main()</code> is <strong>undefined by the C++ standard</strong>.</p>
        <p>If global object <code>A</code> (e.g. <code>DisplayDriver</code>) accesses global object <code>B</code> (e.g. <code>SpiBusDriver</code>) inside its constructor, and <code>B</code> has not yet initialized its hardware registers, the microcontroller will crash with a <strong>fatal HardFault before reaching <code>main()</code>!</strong></p>

        <h3>2. The Construct-On-First-Use Idiom (Meyers Singleton)</h3>
        <p>Wrapping static instances inside a function returning a reference guarantees the object is constructed upon its first call, completely eliminating initialization order bugs.</p>
        """,
        "refactor_html": """
        <p>Construct-On-First-Use idiom preventing bootloader crashes:</p>
        <pre class="code-block" style="background:#0d1117; padding:16px; border-radius:8px; border:1px solid #30363d;">#include &lt;cstdint&gt;

class SpiBusManager {
private:
    SpiBusManager() noexcept {
        // Initialize SPI hardware registers safely...
    }
public:
    // Guaranteed to initialize safely on first call!
    static SpiBusManager&amp; instance() noexcept {
        static SpiBusManager bus; // Meyers' Singleton
        return bus;
    }

    void write(uint8_t byte) noexcept { /* ... */ }
};</pre>
        """,
        "quiz": [
            {
                "question": "What is the 'Static Initialization Order Fiasco' in C++?",
                "options": ["The undefined order in which global/static object constructors across different .cpp translation units execute before main(), causing crashes if one uninitialized global accesses another", "A failure in the compiler's syntax analyzer", "A bug in static casting", "An error when compiling without optimization"],
                "correct": 0,
                "explanation": "C++ does not define constructor execution order for global objects across different translation units, leading to crashes if one global constructor depends on another unconstructed global."
            },
            {
                "question": "How does the 'Construct-On-First-Use' idiom (Meyers Singleton) solve global initialization order bugs?",
                "options": ["By placing the static instance inside a function; the object is initialized on its first invocation with thread-safe guarantees", "By moving all objects into the heap", "By declaring all variables const", "By compiling with -O0"],
                "correct": 0,
                "explanation": "Local static variables inside a function are initialized only when control first passes through their declaration, guaranteeing initialization before use."
            },
            {
                "question": "What does the Triangle Inequality Theorem state for sides a, b, and c?",
                "options": ["a + b > c AND a + c > b AND b + c > a (sum of any two sides must exceed the third)", "a^2 + b^2 = c^2", "a * b = c", "a + b + c = 180"],
                "correct": 0,
                "explanation": "For any non-degenerate triangle, the sum of any two side lengths must strictly exceed the length of the third side."
            },
            {
                "question": "When are global C++ object constructors executed in an embedded microcontroller application?",
                "options": ["During the C++ runtime startup routine (__libc_init_array / static constructors) before main() is called", "When the first interrupt fires", "After main() returns", "When the user presses a button"],
                "correct": 0,
                "explanation": "Microcontroller startup assembly (after copying <code>.data</code> and zeroing <code>.bss</code>) calls <code>__libc_init_array</code> to invoke all global C++ constructors before branching to <code>main()</code>."
            }
        ]
    }
]
