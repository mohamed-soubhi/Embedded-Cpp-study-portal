#!/usr/bin/env python3
"""
Section 8 Project Definitions: Pointers, Memory Management & Hardware Access
Contains 7 comprehensive project definitions covering pointer arithmetic,
Memory-Mapped I/O (MMIO), const-correctness in Flash ROM, heap fragmentation hazards,
and fixed-block pool allocators for microcontrollers.
"""

SECTION_8_PROJECTS = [
    {
        "id": "pointer_fun",
        "name": "PointerFun",
        "title": "Raw Pointers, Address Arithmetic & Hardware MMIO Registers",
        "headline": "Memory Addresses, Dereferencing & Type-Safe Memory-Mapped I/O (MMIO) Peripheral Access",
        "emb_class": "emb-high",
        "emb_badge": "⚡ Embedded Relevance: Critical",
        "tags": ["Pointers", "Address-of &", "Dereference *", "MMIO", "volatile", "ARM Cortex-M"],
        "summary": "Exploring the fundamentals of pointers: memory addresses, the address-of operator (&), and dereferencing (*). In embedded firmware, pointers are the foundational mechanism for communicating directly with hardware peripherals via Memory-Mapped I/O (MMIO) register addresses.",
        "files": ["section_8/PointerFun/PointerFun/main.cpp"],
        "concepts_html": """
        <h3>1. Pointer Mechanics: Addresses vs Values</h3>
        <p>A pointer is a variable that stores the physical or virtual memory address of another object. The address-of operator (<code>&amp;</code>) retrieves an object's memory address, while the dereference operator (<code>*</code>) reads or writes the data stored at that address.</p>

        <h3>2. Pointer Sizing & Architecture</h3>
        <p>The size of a pointer matches the CPU architecture's address bus width: <strong>4 bytes (32 bits)</strong> on 32-bit microcontrollers (e.g. ARM Cortex-M0/M3/M4/M7, ESP32) and <strong>8 bytes (64 bits)</strong> on 64-bit systems (x86_64, AArch64).</p>
        """,
        "embedded_html": """
        <h3>1. Memory-Mapped I/O (MMIO) and the <code>volatile</code> Keyword</h3>
        <p>In microcontrollers, hardware peripherals (GPIO, Timers, UART, SPI) are mapped directly to specific physical memory addresses in the CPU memory map (e.g., STM32 GPIOA output data register at <code>0x40020014</code>).</p>
        <p>Because peripheral registers can change asynchronously due to external hardware events or clock edges, pointers to MMIO registers <strong>must always be qualified with <code>volatile</code></strong>. This prevents the compiler's optimizer from caching register reads in CPU general-purpose registers.</p>

        <div class="callout callout-warning">
          <h4>⚠️ MISRA C++:2008 Rule 5-2-7 & Rule 5-2-8</h4>
          <p>Casting an integer memory address to a pointer is prohibited in general application code, except in low-level hardware abstraction layers (BSP/HAL) accessing hardware registers.</p>
        </div>
        """,
        "refactor_html": """
        <p>Modern embedded C++ wraps raw MMIO addresses in type-safe, zero-overhead register abstractions:</p>
        <pre class="code-block" style="background:#0d1117; padding:16px; border-radius:8px; border:1px solid #30363d;">#include &lt;cstdint&gt;

// Type-safe, zero-cost MMIO Register Wrapper
template &lt;uintptr_t Address, typename T = uint32_t&gt;
struct MmioRegister {
    static void write(T value) noexcept {
        *reinterpret_cast&lt;volatile T*&gt;(Address) = value;
    }
    
    static T read() noexcept {
        return *reinterpret_cast&lt;volatile T*&gt;(Address);
    }
    
    static void set_bit(uint8_t bit) noexcept {
        *reinterpret_cast&lt;volatile T*&gt;(Address) |= (1UL &lt;&lt; bit);
    }
    
    static void clear_bit(uint8_t bit) noexcept {
        *reinterpret_cast&lt;volatile T*&gt;(Address) &amp;= ~(1UL &lt;&lt; bit);
    }
};

// Concrete GPIO Pin Definition (STM32 GPIOA ODR at 0x40020014)
using GpioA_ODR = MmioRegister&lt;0x40020014, uint32_t&gt;;

void toggle_status_led() noexcept {
    GpioA_ODR::set_bit(5);   // Set Pin 5 HIGH (LED ON)
    GpioA_ODR::clear_bit(5); // Set Pin 5 LOW (LED OFF)
}</pre>
        """,
        "quiz": [
            {
                "question": "Why is the volatile qualifier required when creating pointers to hardware MMIO peripheral registers?",
                "options": ["It forces the compiler to generate actual load/store instructions on every access, preventing the optimizer from caching values in CPU registers", "It allocates the pointer in battery-backed SRAM", "It encrypts the memory bus against side-channel attacks", "It converts 32-bit pointers into 64-bit pointers"],
                "correct": 0,
                "explanation": "<code>volatile</code> informs the compiler that the value at the address can change outside the program's control (e.g., by hardware circuitry), preventing the compiler from omitting or reordering reads/writes."
            },
            {
                "question": "On a 32-bit ARM Cortex-M4 microcontroller, what is the value of sizeof(void*)?",
                "options": ["4 bytes", "8 bytes", "2 bytes", "1 byte"],
                "correct": 0,
                "explanation": "In 32-bit architectures, memory addresses are 32 bits wide, making all pointers exactly 4 bytes in size."
            },
            {
                "question": "What is the result of dereferencing a nullptr or unaligned pointer on an ARM Cortex-M microcontroller with UNALIGN_TRP set?",
                "options": ["A hardware UsageFault or HardFault exception is triggered immediately", "The CPU prints a segmentation fault to the console", "The pointer is automatically rounded to the nearest word boundary", "The instruction executes normally with 2 clock cycles delay"],
                "correct": 0,
                "explanation": "Dereferencing invalid or unaligned addresses triggers a hardware UsageFault (or HardFault), causing the microcontroller to jump into its fault ISR."
            },
            {
                "question": "What does the address-of operator (&) return when applied to a local variable?",
                "options": ["The memory address on the CPU stack where that variable is currently stored", "The size of the variable in bytes", "The ASCII value of the variable's name", "The CPU clock cycle timestamp"],
                "correct": 0,
                "explanation": "Applying <code>&amp;</code> to a local variable yields its stack memory address."
            }
        ]
    },
    {
        "id": "const_correctness",
        "name": "ConstCorrectness",
        "title": "Const Pointers, ROM-ability & Flash Memory (.rodata)",
        "headline": "Pointer to Const vs Const Pointer & Placing Lookups in Microcontroller Flash ROM",
        "emb_class": "emb-high",
        "emb_badge": "⚡ Embedded Relevance: Critical",
        "tags": ["const", "ROM-ability", ".rodata", "Pointer to Const", "Const Pointer", "MISRA C++"],
        "summary": "Mastering the four permutations of const with pointers: mutable pointer to mutable data, pointer to const data, const pointer to mutable data, and const pointer to const data. We analyze how const enables ROM-ability, placing lookup tables and calibration data into Flash ROM (.rodata) to save precious SRAM.",
        "files": ["section_8/ConstCorrectness/ConstCorrectness/main.cpp"],
        "concepts_html": """
        <h3>1. The Four Permutations of Pointer Constness</h3>
        <ul>
          <li><code>int* ptr</code>: Mutable pointer to mutable data (can reassign pointer, can mutate value).</li>
          <li><code>const int* ptr</code> (or <code>int const* ptr</code>): <strong>Pointer to const data</strong> (cannot mutate data via pointer; can reassign pointer).</li>
          <li><code>int* const ptr</code>: <strong>Const pointer to mutable data</strong> (can mutate data; cannot reassign pointer).</li>
          <li><code>const int* const ptr</code>: <strong>Const pointer to const data</strong> (immutable address, immutable data).</li>
        </ul>

        <h3>2. Read-Right-to-Left Rule</h3>
        <p>To decipher complex pointer declarations, read from right to left: <code>const int* const ptr</code> $\\rightarrow$ "ptr is a <strong>const pointer</strong> to a <strong>const int</strong>".</p>
        """,
        "embedded_html": """
        <h3>1. ROM-ability and the <code>.rodata</code> Section</h3>
        <p>In microcontrollers with limited SRAM (e.g. 16KB-64KB) and larger Flash (e.g. 128KB-1MB), saving RAM is critical. When data structures, calibration maps, and strings are declared <code>const</code> or <code>constexpr</code>, the linker places them in the <strong><code>.rodata</code> section in Flash ROM</strong>.</p>

        <h3>2. Hardware Peripheral Base Address Safety</h3>
        <p>Pointers to hardware peripheral register blocks must be declared as <strong>const pointers to volatile data</strong> (<code>volatile RegisterMap* const</code>). This ensures the pointer permanently addresses the peripheral and cannot be accidentally redirected.</p>
        """,
        "refactor_html": """
        <p>Here is how const correctness is applied in production hardware peripheral drivers:</p>
        <pre class="code-block" style="background:#0d1117; padding:16px; border-radius:8px; border:1px solid #30363d;">#include &lt;cstdint&gt;

// Hardware register map structure
struct UartHardwareMap {
    volatile uint32_t SR;   // Status Register
    volatile uint32_t DR;   // Data Register
    volatile uint32_t BRR;  // Baud Rate Register
    volatile uint32_t CR1;  // Control Register 1
};

// 1. Const pointer to volatile hardware register (Permanent MMIO base address)
UartHardwareMap* const UART1_HW = reinterpret_cast&lt;UartHardwareMap* const&gt;(0x40011000);

// 2. Calibration curve stored 100% in Flash ROM (.rodata section)
struct AdcCalibrationCurve {
    const uint16_t raw_counts[5];
    const float    voltage_volts[5];
};

static constexpr AdcCalibrationCurve SENSOR_CALIB = {
    .raw_counts    = {0, 1024, 2048, 3072, 4095},
    .voltage_volts = {0.0f, 0.825f, 1.65f, 2.475f, 3.3f}
};</pre>
        """,
        "quiz": [
            {
                "question": "What is the meaning of 'const uint8_t* const ptr'?",
                "options": ["A const (immutable) pointer pointing to const (read-only) data", "A pointer that can be reassigned to any memory address", "A mutable pointer to mutable uint8_t data", "An array of 8-bit integers on the heap"],
                "correct": 0,
                "explanation": "Reading right-to-left: <code>ptr</code> is a <code>const</code> pointer (its stored address cannot change) to a <code>const uint8_t</code> (the pointed-to data cannot be modified)."
            },
            {
                "question": "Why is const-correctness vital for conserving SRAM in embedded firmware?",
                "options": ["Data marked const/constexpr is placed by the linker in Flash ROM (.rodata), consuming 0 bytes of SRAM", "It compresses variables using ZIP encoding in RAM", "It makes the CPU run at double clock frequency", "It automatically deletes unused variables during runtime"],
                "correct": 0,
                "explanation": "Linkers place immutable (<code>const</code> / <code>constexpr</code>) data into Flash memory (<code>.rodata</code>), freeing SRAM for dynamic stack variables and buffers."
            },
            {
                "question": "Which pointer declaration correctly models a permanent hardware peripheral base address whose registers change asynchronously?",
                "options": ["volatile PeripheralRegs* const PERIPHERAL_BASE", "const PeripheralRegs* PERIPHERAL_BASE", "PeripheralRegs* volatile PERIPHERAL_BASE", "const volatile PeripheralRegs* PERIPHERAL_BASE"],
                "correct": 0,
                "explanation": "<code>volatile PeripheralRegs* const</code> specifies a <strong>const pointer</strong> (the base memory address is permanent) pointing to <strong>volatile hardware registers</strong> (the register values change in hardware)."
            },
            {
                "question": "What happens if code attempts to write to a variable placed in Flash ROM (.rodata)?",
                "options": ["A hardware MemManage Fault or BusFault occurs because Flash memory is read-only at runtime", "The Flash controller automatically updates the sector in 1 clock cycle", "The write succeeds without errors", "The CPU ignores the write and resets the stack pointer"],
                "correct": 0,
                "explanation": "Flash memory cannot be written like RAM at runtime without unlocking the flash controller; writes trigger a hardware fault (BusFault / MemManage Fault)."
            }
        ]
    },
    {
        "id": "dynamic_fun",
        "name": "DynamicFun",
        "title": "Heap Allocation Mechanics & The Hazards of Dynamic Memory in MCU",
        "headline": "new / delete Lifecycles, Dangling Pointers & Heap Fragmentation in Microcontrollers",
        "emb_class": "emb-high",
        "emb_badge": "⚡ Embedded Relevance: Critical",
        "tags": ["new", "delete", "Heap Fragmentation", "Memory Leaks", "nullptr", "MISRA C++"],
        "summary": "Analyzing dynamic memory allocation via new and delete, pointer resets to nullptr, and dangling pointer hazards. We explore why dynamic heap allocation is prohibited in high-reliability embedded systems (AUTOSAR / MISRA) due to heap fragmentation, non-deterministic latency, and catastrophic stack-heap collisions.",
        "files": ["section_8/DynamicFun/DynamicFun/main.cpp"],
        "concepts_html": """
        <h3>1. Heap Allocation with <code>new</code> and <code>delete</code></h3>
        <p>The <code>new</code> operator requests memory from the free store (heap), invokes the object's constructor, and returns a pointer. The <code>delete</code> operator invokes the destructor and releases the memory back to the heap.</p>

        <h3>2. Dangling Pointers and Double-Free Bugs</h3>
        <p>After calling <code>delete ptr;</code>, the pointer variable still holds the original address (a <em>dangling pointer</em>). Dereferencing it is Undefined Behavior. Calling <code>delete</code> twice on the same pointer corrupts the heap metadata. Always set <code>ptr = nullptr;</code> immediately after deletion.</p>
        """,
        "embedded_html": """
        <h3>1. Why Dynamic Heap Allocation is Banned in Embedded Safety Systems</h3>
        <ul>
          <li><strong>Heap Fragmentation:</strong> Repeated allocations and deallocations of varying sizes create tiny free holes across SRAM. Eventually, a small allocation request fails (<code>std::bad_alloc</code>) even if total free RAM exceeds the requested size.</li>
          <li><strong>Non-Deterministic Latency:</strong> Heap allocators (<code>malloc</code>) search free lists. The time required varies wildly based on fragmentation state, violating real-time deadlines.</li>
          <li><strong>Stack-Heap Collision:</strong> In bare-metal linker scripts, the stack grows downwards while the heap grows upwards. A heap overflow silently overwrites the active stack, corrupting return addresses.</li>
        </ul>

        <div class="callout callout-danger">
          <h4>🚫 MISRA C++:2008 Rule 18-0-1 & NASA C Style Guide</h4>
          <p>Dynamic memory allocation shall not be used after firmware startup initialization. All buffers and objects must be statically or stack allocated.</p>
        </div>
        """,
        "refactor_html": """
        <p>Here is how embedded engineers replace heap <code>new</code> with static storage buffers (zero heap allocation):</p>
        <pre class="code-block" style="background:#0d1117; padding:16px; border-radius:8px; border:1px solid #30363d;">#include &lt;cstdint&gt;
#include &lt;cstddef&gt;
#include &lt;new&gt;

// Statically allocated memory slot (Zero Heap Overhead)
template &lt;typename T&gt;
class StaticSlot {
    alignas(T) std::byte storage_[sizeof(T)];
    bool occupied_{false};

public:
    template &lt;typename... Args&gt;
    T* construct(Args&amp;&amp;... args) noexcept {
        if (occupied_) return nullptr;
        T* obj = new (storage_) T(std::forward&lt;Args&gt;(args)...); // Placement new
        occupied_ = true;
        return obj;
    }

    void destroy() noexcept {
        if (occupied_) {
            reinterpret_cast&lt;T*&gt;(storage_)-&gt;~T(); // Explicit destructor call
            occupied_ = false;
        }
    }
};</pre>
        """,
        "quiz": [
            {
                "question": "What is 'heap fragmentation' and why is it fatal in long-running embedded devices?",
                "options": ["Interspersed allocations and deallocations leave unusable gaps in SRAM, eventually causing allocation failure despite sufficient total free memory", "The CPU hardware clock frequency degrades over time", "The Flash ROM sectors wear out after 1000 writes", "The linker script fails to locate main()"],
                "correct": 0,
                "explanation": "Heap fragmentation breaks contiguous free memory into small disjoint chunks. Over weeks or months of operation, memory requests fail because no single contiguous block is large enough."
            },
            {
                "question": "What is a 'dangling pointer'?",
                "options": ["A pointer that still holds the memory address of an object that has already been deallocated/deleted", "A pointer that points to address 0x00000000", "A pointer stored inside an interrupt vector table", "A pointer passed to a function by reference"],
                "correct": 0,
                "explanation": "A dangling pointer references memory that has been freed. Dereferencing or accessing a dangling pointer causes undefined behavior and data corruption."
            },
            {
                "question": "What happens during a Stack-Heap collision in microcontroller SRAM?",
                "options": ["The downward-growing CPU stack and upward-growing heap overlap, causing silent data and return address corruption", "The compiler throws a std::stack_overflow exception", "The microcontroller enters low-power sleep mode", "The memory bus automatically expands into external flash"],
                "correct": 0,
                "explanation": "In microcontrollers without an MMU/MPU guard band, the stack and heap grow toward each other. An overflow overwrites stack frames, causing unpredictable crashes."
            },
            {
                "question": "Why is setting a pointer to nullptr after calling delete recommended?",
                "options": ["It prevents accidental use-after-free bugs and makes subsequent delete calls harmless (deleting nullptr is a safe no-op in C++)", "It physically erases the SRAM silicon cells", "It forces the compiler to inline the destructor", "It returns memory directly to the bootloader"],
                "correct": 0,
                "explanation": "Deleting <code>nullptr</code> is guaranteed to be a safe no-op in C++, and setting freed pointers to <code>nullptr</code> prevents accidental double-free and use-after-free bugs."
            }
        ]
    },
    {
        "id": "dynamic_dogs",
        "name": "DynamicDogs",
        "title": "Object Pointer Member Access & Placement Mechanics",
        "headline": "Arrow Operator (->) vs Dereference Dot (*ptr). & Zero-Heap Object Placement",
        "emb_class": "emb-core",
        "emb_badge": "⚡ Embedded Relevance: Core",
        "tags": ["Arrow Operator ->", "Dereference Dot (*ptr).", "Object Lifecycles", "Placement New", "Cache Lines"],
        "summary": "Exploring object member access via pointer: the arrow operator (->) vs explicit dereferencing (*ptr).member. We analyze memory layouts of heap objects, cache-line alignment, and how placement-new constructs objects in predefined static memory pools with zero allocation latency.",
        "files": [
            "section_8/DynamicDogs/DynamicDogs/main.cpp",
            "section_8/DynamicDogs/Dog.h",
            "section_8/DynamicDogs/Dog.cpp"
        ],
        "concepts_html": """
        <h3>1. Arrow Operator Syntax Sugar</h3>
        <p>The arrow operator (<code>ptr-&gt;member</code>) is syntactically equivalent to dereferencing the pointer and accessing the member via the dot operator: <code>(*ptr).member</code>. Parentheses are required around <code>*ptr</code> because the dot operator (<code>.</code>) has higher operator precedence than the dereference operator (<code>*</code>).</p>

        <h3>2. Heap Object Lifecycles</h3>
        <p>Objects allocated on the heap exist until explicitly deleted. Failing to call <code>delete</code> produces a memory leak that permanently consumes SRAM until the microcontroller is reset.</p>
        """,
        "embedded_html": """
        <h3>1. Placement-New for Deterministic Object Construction</h3>
        <p>Placement-new constructs an object at a specific, pre-allocated memory address without calling the heap allocator (<code>malloc</code>). In embedded systems, this allows creating objects in:</p>
        <ul>
          <li>Fast tightly-coupled SRAM (DTCM).</li>
          <li>Battery-backed backup SRAM.</li>
          <li>Pre-allocated static object pools with zero heap fragmentation.</li>
        </ul>

        <h3>2. Memory Alignment (<code>alignas</code>)</h3>
        <p>Microcontrollers require objects to be aligned to their natural boundaries (e.g. 32-bit integers at 4-byte aligned addresses). Unaligned access causes hardware UsageFaults on ARM Cortex-M processors when unaligned trapping is active.</p>
        """,
        "refactor_html": """
        <p>Here is an embedded object pool utilizing placement-new for zero-heap, deterministic object creation:</p>
        <pre class="code-block" style="background:#0d1117; padding:16px; border-radius:8px; border:1px solid #30363d;">#include &lt;cstdint&gt;
#include &lt;cstddef&gt;
#include &lt;new&gt;

template &lt;typename T, size_t MaxCount&gt;
class StaticObjectPool {
private:
    alignas(alignof(T)) std::byte storage_[MaxCount][sizeof(T)];
    bool in_use_[MaxCount]{false};

public:
    template &lt;typename... Args&gt;
    T* allocate(Args&amp;&amp;... args) noexcept {
        for (size_t i = 0; i &lt; MaxCount; ++i) {
            if (!in_use_[i]) {
                in_use_[i] = true;
                return new (storage_[i]) T(std::forward&lt;Args&gt;(args)...);
            }
        }
        return nullptr; // Pool exhausted (no heap fallback)
    }

    void free(T* ptr) noexcept {
        if (!ptr) return;
        for (size_t i = 0; i &lt; MaxCount; ++i) {
            if (reinterpret_cast&lt;T*&gt;(storage_[i]) == ptr) {
                ptr-&gt;~T(); // Explicit destructor call
                in_use_[i] = false;
                return;
            }
        }
    }
};</pre>
        """,
        "quiz": [
            {
                "question": "Why are parentheses required in (*ptr).member when accessing an object member through a dereferenced pointer?",
                "options": ["The dot operator (.) has higher operator precedence than the dereference operator (*)", "C++ requires parentheses around all pointer operations", "Parentheses force the compiler to check for nullptr", "Parentheses allocate stack memory for the member"],
                "correct": 0,
                "explanation": "Because <code>.</code> has higher precedence than <code>*</code>, writing <code>*ptr.member</code> is parsed as <code>*(ptr.member)</code>, causing a compiler error. <code>(*ptr).member</code> or <code>ptr-&gt;member</code> ensures correct evaluation."
            },
            {
                "question": "What is 'placement new' in C++?",
                "options": ["A syntax that constructs an object inside a pre-allocated memory buffer without invoking the heap allocator", "A compiler directive that moves objects to external Flash memory", "A keyword that automatically deletes objects when out of scope", "A function that resizes dynamic arrays"],
                "correct": 0,
                "explanation": "Placement-new (<code>new (buffer) Type(args)</code>) constructs an object directly into a provided memory buffer without any dynamic heap allocation."
            },
            {
                "question": "When an object created with placement-new is destroyed, how must its destructor be called?",
                "options": ["By calling the destructor explicitly (ptr->~Type()) without calling delete", "By calling standard delete ptr", "By calling free(ptr)", "Destructors run automatically when the microcontroller sleeps"],
                "correct": 0,
                "explanation": "Because the memory was not allocated via standard <code>new</code>, calling <code>delete ptr</code> would corrupt the heap. The destructor must be invoked explicitly: <code>ptr-&gt;~Type()</code>."
            },
            {
                "question": "What does alignas(alignof(T)) guarantee when creating raw byte storage for an object?",
                "options": ["That the storage buffer is aligned to the exact hardware boundary required by type T, preventing unaligned hardware faults", "That the buffer is stored in Flash ROM", "That the buffer size is rounded up to 1024 bytes", "That the buffer is accessible by DMA controllers only"],
                "correct": 0,
                "explanation": "<code>alignas(alignof(T))</code> ensures the byte array starts at an address divisible by <code>alignof(T)</code>, avoiding hardware alignment faults on processors like ARM Cortex-M."
            }
        ]
    },
    {
        "id": "dynamic_array_test",
        "name": "DynamicArrayTest",
        "title": "Dynamic Array Allocation (new[]) & Fixed-Capacity Bounded Vectors",
        "headline": "new[] / delete[] Pairing Rules vs Zero-Heap Fixed-Capacity Bounded Vectors",
        "emb_class": "emb-high",
        "emb_badge": "⚡ Embedded Relevance: High",
        "tags": ["new[]", "delete[]", "Bounded Arrays", "etl::vector", "Heap Corruption"],
        "summary": "Analyzing dynamic array allocation with new[] and deallocation with delete[]. We explain the undefined behavior of mismatched delete operators (scalar delete on array new), and demonstrate how embedded systems replace dynamic arrays with zero-heap fixed-capacity containers (such as ETL or inplace_vector).",
        "files": ["section_8/DynamicArrayTest/DynamicArrayTest/main.cpp"],
        "concepts_html": """
        <h3>1. Array Allocation (<code>new[]</code>) vs Scalar Allocation (<code>new</code>)</h3>
        <p>Allocating an array of $N$ objects requires <code>new Type[N]</code>. The runtime allocates memory for all elements plus internal array-size metadata (often stored in an invisible header prefix).</p>

        <h3>2. The Mismatched Deallocation Trap</h3>
        <p>Deallocating an array with scalar <code>delete ptr;</code> instead of <code>delete[] ptr;</code> is <strong>Undefined Behavior</strong>. In non-trivial classes, scalar <code>delete</code> calls the destructor of only the first element (<code>ptr[0]</code>) and corrupts the heap metadata manager.</p>
        """,
        "embedded_html": """
        <h3>1. The Embedded Solution: Bounded Capacity Containers</h3>
        <p>Embedded applications need array-like containers with dynamic size (count of active elements) but <strong>bounded maximum capacity</strong> (zero heap allocation). Libraries like <strong>Embedded Template Library (ETL)</strong> provide <code>etl::vector&lt;T, Capacity&gt;</code>:</p>
        <ul>
          <li>Storage is allocated directly inside the object (on the stack or in static RAM).</li>
          <li>Element count can vary from $0$ to $Capacity$.</li>
          <li>Zero dynamic memory allocations; zero heap fragmentation.</li>
        </ul>

        <h3>2. C++26 <code>std::inplace_vector&lt;T, N&gt;</code></h3>
        <p>Standard C++26 standardizes this exact container as <code>std::inplace_vector</code>, bringing zero-heap vector semantics to modern C++ standard libraries.</p>
        """,
        "refactor_html": """
        <p>Here is an embedded fixed-capacity bounded array container with zero dynamic allocation:</p>
        <pre class="code-block" style="background:#0d1117; padding:16px; border-radius:8px; border:1px solid #30363d;">#include &lt;cstdint&gt;
#include &lt;cstddef&gt;
#include &lt;array&gt;

template &lt;typename T, size_t Capacity&gt;
class BoundedVector {
private:
    std::array&lt;T, Capacity&gt; data_{};
    size_t size_{0};

public:
    constexpr bool push_back(const T&amp; item) noexcept {
        if (size_ &gt;= Capacity) return false; // Fixed capacity reached
        data_[size_++] = item;
        return true;
    }

    constexpr void clear() noexcept { size_ = 0; }
    constexpr size_t size() const noexcept { return size_; }
    constexpr size_t capacity() const noexcept { return Capacity; }

    constexpr T&amp; operator[](size_t idx) noexcept { return data_[idx]; }
    constexpr const T&amp; operator[](size_t idx) const noexcept { return data_[idx]; }
};</pre>
        """,
        "quiz": [
            {
                "question": "What happens if you allocate an array with 'new int[10]' and deallocate it with scalar 'delete myArray;' instead of 'delete[] myArray;'?",
                "options": ["Undefined Behavior occurs, potentially causing heap corruption and failing to call destructors for elements 1 through 9", "The compiler automatically fixes the syntax at runtime", "Only the last element is deleted", "The program executes 10% faster"],
                "correct": 0,
                "explanation": "Calling scalar <code>delete</code> on an array allocated with <code>new[]</code> is undefined behavior. The runtime cannot determine the array length, destructors for subsequent elements are skipped, and heap bookkeeping is corrupted."
            },
            {
                "question": "How does a Bounded Vector (like etl::vector or std::inplace_vector) differ from std::vector?",
                "options": ["Its elements are stored entirely within the container's inline storage on the stack/static memory without heap allocation", "It can grow infinitely in size", "It requires an operating system kernel", "It only accepts integer data types"],
                "correct": 0,
                "explanation": "Bounded vectors allocate a fixed-capacity inline buffer inside the object itself, providing variable length up to a maximum capacity with zero dynamic heap allocation."
            },
            {
                "question": "Why are Variable-Length Arrays (VLAs, e.g. int arr[n];) prohibited in safety-critical C++?",
                "options": ["They can silently blow past the available CPU stack size, causing catastrophic stack overflow crashes without any error handling", "They increase binary Flash size by 500KB", "They convert all variables to 64-bit doubles", "They disable compiler optimizations permanently"],
                "correct": 0,
                "explanation": "VLAs allocate variable amounts of memory on the stack at runtime. If the size is large or uncontrolled, the stack silently collides with SRAM variables, causing catastrophic system crashes."
            },
            {
                "question": "What is the time complexity of pushing an element to a BoundedVector with available capacity?",
                "options": ["O(1) strictly deterministic constant time", "O(N) linear time", "O(log N) logarithmic time", "O(N^2) quadratic time"],
                "correct": 0,
                "explanation": "Because capacity is pre-allocated inline and never requires dynamic memory reallocation or element copying, inserting into a bounded vector is strictly $O(1)$ deterministic."
            }
        ]
    },
    {
        "id": "drone_fleet",
        "name": "DroneFleet",
        "title": "Double Indirection (Pointers-to-Pointers) & Cache Locality",
        "headline": "Pointer-to-Pointer (Drone**) Fleet Arrays vs Flat Contiguous Array-of-Structures (AoS)",
        "emb_class": "emb-high",
        "emb_badge": "⚡ Embedded Relevance: High",
        "tags": ["Double Indirection", "Pointer to Pointer", "Cache Locality", "Pointer Chasing", "AoS vs SoA"],
        "summary": "Analyzing dynamic fleet management using double pointer indirection (Drone**). We contrast pointer-to-pointer architectures with contiguous flat memory buffers, showing how pointer chasing destroys CPU cache performance and wastes precious RAM on microcontrollers.",
        "files": [
            "section_8/DroneFleet/DroneFleet/main.cpp",
            "section_8/DroneFleet/DroneFleet/Drone.h",
            "section_8/DroneFleet/DroneFleet/Drone.cpp"
        ],
        "concepts_html": """
        <h3>1. Pointer-to-Pointer Mechanics (<code>Type**</code>)</h3>
        <p>A pointer-to-pointer stores the memory address of another pointer. In classical C++, dynamic 2D tables or arrays of polymorphic objects are created by allocating an array of pointers (<code>Drone** fleet = new Drone*[N]</code>) and then individually allocating each object (<code>fleet[i] = new Drone(...)</code>).</p>

        <h3>2. Double Allocation Overhead</h3>
        <p>Managing $N$ objects requires $N + 1$ distinct heap allocations ($1$ array of pointers $+ N$ individual objects) and $N + 1$ corresponding <code>delete</code> calls.</p>
        """,
        "embedded_html": """
        <h3>1. The Hardware Cost of Pointer Chasing</h3>
        <p>Accessing <code>fleet[i]-&gt;getBatteryLife()</code> requires <strong>double dereferencing</strong>:</p>
        <ol>
          <li>Read the pointer from the pointer array: <code>ptr = *(fleet + i)</code>.</li>
          <li>Dereference <code>ptr</code> to read the object in distant heap memory: <code>ptr-&gt;battery</code>.</li>
        </ol>
        <p>Because each object was allocated separately on the heap, they are scattered randomly across SRAM. On modern pipelined microcontrollers (ARM Cortex-M7 with L1 data cache), this causes frequent <strong>cache misses and memory stall cycles</strong>.</p>

        <h3>2. Flat Contiguous Storage: Array of Structures (AoS)</h3>
        <p>Storing objects contiguously in a single flat array (<code>std::array&lt;Drone, MaxDrones&gt;</code>) requires <strong>zero pointer storage</strong> (saving $4 \\times N$ bytes of RAM) and maximizes CPU spatial cache locality.</p>
        """,
        "refactor_html": """
        <p>Here is an embedded fleet manager using flat contiguous memory with zero pointer indirection:</p>
        <pre class="code-block" style="background:#0d1117; padding:16px; border-radius:8px; border:1px solid #30363d;">#include &lt;cstdint&gt;
#include &lt;string_view&gt;
#include &lt;array&gt;

struct DroneTelemetry {
    char     model_name[16];
    uint16_t battery_milli_volts; // e.g. 3700 mV
    uint8_t  active_status;
};

template &lt;size_t MaxFleetSize&gt;
class FlatDroneFleet {
private:
    // Contiguous in SRAM; 100% spatial cache locality; 0 pointer overhead
    std::array&lt;DroneTelemetry, MaxFleetSize&gt; drones_{};
    size_t active_count_{0};

public:
    bool register_drone(std::string_view model, uint16_t battery_mv) noexcept {
        if (active_count_ &gt;= MaxFleetSize) return false;
        
        DroneTelemetry&amp; d = drones_[active_count_++];
        size_t len = model.size() &lt; 15 ? model.size() : 15;
        for (size_t i = 0; i &lt; len; ++i) d.model_name[i] = model[i];
        d.model_name[len] = '\\0';
        d.battery_milli_volts = battery_mv;
        d.active_status = 1;
        return true;
    }

    const DroneTelemetry* data() const noexcept { return drones_.data(); }
    size_t count() const noexcept { return active_count_; }
};</pre>
        """,
        "quiz": [
            {
                "question": "What is 'pointer chasing' and why does it degrade execution speed on pipelined microcontrollers?",
                "options": ["Following multiple levels of pointer indirection to scattered memory locations, causing CPU pipeline stalls and cache misses", "A compiler optimization that speeds up loops", "A tool for debugging memory leaks", "A technique to compress pointer tables in ROM"],
                "correct": 0,
                "explanation": "Pointer chasing forces the CPU to wait for memory loads before it can determine the next address to fetch. When data is scattered across SRAM, cache misses stall the pipeline."
            },
            {
                "question": "How much RAM is wasted storing a Drone** array of 50 pointers on a 32-bit ARM Cortex-M microcontroller?",
                "options": ["200 bytes (50 pointers * 4 bytes per pointer) plus heap allocator bookkeeping headers", "0 bytes", "1024 bytes", "4 bytes"],
                "correct": 0,
                "explanation": "On a 32-bit MCU, each pointer requires 4 bytes. 50 pointers consume 200 bytes just for address storage, plus 8-16 bytes of heap allocator metadata per object."
            },
            {
                "question": "Why is a contiguous flat array (std::array<Drone, N>) superior to an array of pointers (Drone*[])?",
                "options": ["It guarantees sequential memory layout for optimal spatial cache locality, eliminates pointer storage overhead, and requires zero heap allocations", "It allows drones to fly faster", "It converts the class to pure virtual methods", "It automatically generates unit tests"],
                "correct": 0,
                "explanation": "Flat contiguous arrays place objects sequentially in memory, maximizing CPU cache line hits, eliminating pointer overhead, and removing dynamic memory risks."
            },
            {
                "question": "What happens if an individual Drone object in a Drone** array is deleted, but the pointer in the array is not set to nullptr?",
                "options": ["The array retains a dangling pointer; iterating over the array and calling methods on it causes undefined behavior", "The compiler automatically re-allocates the drone", "The pointer becomes a null reference safely", "The CPU hardware halts with a power-saving mode"],
                "correct": 0,
                "explanation": "The array element still points to the freed memory. If loop code attempts to read that array element, a use-after-free bug occurs."
            }
        ]
    },
    {
        "id": "exhibit_tracker",
        "name": "ExhibitTracker",
        "title": "Static Arrays of Pointers & Fixed-Block Allocators",
        "headline": "Managing Fixed Arrays of Heap Objects vs Intrusive Lists & Bitmask Memory Pools",
        "emb_class": "emb-high",
        "emb_badge": "⚡ Embedded Relevance: High",
        "tags": ["Array of Pointers", "Fixed-Block Allocator", "Intrusive List", "Bitmask Pool", "Memory Management"],
        "summary": "Tracking museum exhibits via a fixed array of heap pointers (Exhibit* exhibitPtrs[COUNT]). We explore the cleanup lifecycle of pointer arrays, analyze the fragmentation hazards of out-of-order deallocations in long-running firmware, and build a deterministic bitmask fixed-block memory pool.",
        "files": [
            "section_8/ExhibitTracker/ExhibitTracker/main.cpp",
            "section_8/ExhibitTracker/ExhibitTracker/Exhibit.h",
            "section_8/ExhibitTracker/ExhibitTracker/Exhibit.cpp"
        ],
        "concepts_html": """
        <h3>1. Fixed Arrays of Pointers</h3>
        <p>A static array of pointers (<code>Exhibit* exhibits[3]</code>) holds pointers to individually allocated heap objects. While the array container is statically sized on the stack or in BSS, the individual objects reside on the dynamic heap.</p>

        <h3>2. Multi-Object Deallocation Lifecycle</h3>
        <p>To prevent memory leaks, every element in the pointer array must be explicitly deleted and reset to <code>nullptr</code> when its lifecycle ends.</p>
        """,
        "embedded_html": """
        <h3>1. Out-of-Order Deallocation Fragmentation</h3>
        <p>If exhibits (or network packets, sensor readings) are allocated and freed in random order, general-purpose heap allocators create fragmented memory holes that cannot be coalesced, eventually causing allocation failure.</p>

        <h3>2. Fixed-Block Allocator with Bitmask Free-List</h3>
        <p>A Fixed-Block Allocator pre-allocates $N$ memory blocks of identical size in static SRAM. A single integer bitmask tracks which blocks are free. Allocation and deallocation are <strong>$O(1)$ constant time operations</strong> with zero fragmentation.</p>
        """,
        "refactor_html": """
        <p>Here is a deterministic, zero-fragmentation Fixed-Block Pool Allocator using a bitmask:</p>
        <pre class="code-block" style="background:#0d1117; padding:16px; border-radius:8px; border:1px solid #30363d;">#include &lt;cstdint&gt;
#include &lt;cstddef&gt;
#include &lt;new&gt;

template &lt;typename T, size_t BlockCount = 32&gt;
class FixedBlockPool {
    static_assert(BlockCount &lt;= 32, "Bitmask supports up to 32 blocks");

    alignas(alignof(T)) std::byte memory_[BlockCount][sizeof(T)];
    uint32_t allocation_mask_{0}; // Bit = 1 (Used), Bit = 0 (Free)

public:
    template &lt;typename... Args&gt;
    T* allocate(Args&amp;&amp;... args) noexcept {
        for (size_t i = 0; i &lt; BlockCount; ++i) {
            if (!(allocation_mask_ &amp; (1UL &lt;&lt; i))) {
                allocation_mask_ |= (1UL &lt;&lt; i); // Mark block as used
                return new (memory_[i]) T(std::forward&lt;Args&gt;(args)...);
            }
        }
        return nullptr; // Out of blocks
    }

    void free(T* ptr) noexcept {
        if (!ptr) return;
        for (size_t i = 0; i &lt; BlockCount; ++i) {
            if (reinterpret_cast&lt;T*&gt;(memory_[i]) == ptr) {
                ptr-&gt;~T();
                allocation_mask_ &amp;= ~(1UL &lt;&lt; i); // Clear bitmask
                return;
            }
        }
    }
};</pre>
        """,
        "quiz": [
            {
                "question": "What is the primary advantage of a Fixed-Block Memory Pool over general-purpose malloc() in embedded firmware?",
                "options": ["It guarantees zero memory fragmentation and strictly deterministic O(1) allocation/deallocation time", "It dynamically increases the SRAM capacity of the microcontroller", "It automatically runs garbage collection during interrupt routines", "It encrypts the heap memory"],
                "correct": 0,
                "explanation": "Because all memory blocks are uniform in size, any freed block can satisfy any future allocation request, completely eliminating heap fragmentation and providing guaranteed $O(1)$ latency."
            },
            {
                "question": "In a 32-block Fixed-Block Allocator, how much memory is required to track the free/used state of all 32 blocks using a bitmask?",
                "options": ["Exactly 4 bytes (a single 32-bit integer)", "128 bytes", "32 kilobytes", "1 byte per object pointer"],
                "correct": 0,
                "explanation": "A single 32-bit unsigned integer (<code>uint32_t</code>, 4 bytes) has 32 individual bits, where each bit represents the used/free state of one block."
            },
            {
                "question": "What happens if a loop deletes exhibitPtrs[i] but does not set exhibitPtrs[i] = nullptr, and a subsequent function checks 'if (exhibitPtrs[i] != nullptr)'?",
                "options": ["The condition evaluates to true (because the pointer still holds the old address), leading to a hazardous use-after-free crash", "The compiler converts the pointer to nullptr automatically", "The condition evaluates to false safely", "The microcontroller reboots into DFU bootloader mode"],
                "correct": 0,
                "explanation": "Calling <code>delete</code> frees the target memory but does not modify the pointer variable itself. Failing to set <code>nullptr</code> causes null checks to pass incorrectly, resulting in use-after-free bugs."
            },
            {
                "question": "What is an 'intrusive data structure' in low-level systems programming?",
                "options": ["A data structure where linkage pointers (next/prev) are embedded directly inside the payload object itself, requiring zero auxiliary node memory allocation", "A virus that infects microcontroller firmware", "A data structure that only operates inside hardware registers", "A structure that allocates memory on external SPI Flash"],
                "correct": 0,
                "explanation": "Intrusive containers store node pointers directly inside the managed objects, allowing objects to be linked into queues/lists without requiring separate node memory allocations."
            }
        ]
    }
]
