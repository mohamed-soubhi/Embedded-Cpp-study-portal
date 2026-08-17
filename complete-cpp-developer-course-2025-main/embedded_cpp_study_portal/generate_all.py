#!/usr/bin/env python3
import os
import sys
import html
import re
from builder import generate_page, ROOT_DIR, PORTAL_DIR
from section_1_data import SECTION_1_PROJECTS
from section_2_data import SECTION_2_PROJECTS
from section_3_data import SECTION_3_PROJECTS
from section_4_data import SECTION_4_PROJECTS
from section_5_data import SECTION_5_PROJECTS
from section_6_data import SECTION_6_PROJECTS
from section_7_data import SECTION_7_PROJECTS
from section_8_data import SECTION_8_PROJECTS
from section_9_data import SECTION_9_PROJECTS
from section_10_data import SECTION_10_PROJECTS
from uml_data_definitions import UML_DEFINITIONS
from build_glossary import generate_glossary_page

def sanitize_card_desc(text, max_len=120):
    # Strip any HTML tags (e.g. <code>, <strong>, etc.)
    plain = re.sub(r'<[^>]+>', '', text)
    plain = plain.replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&').replace('&quot;', '"')
    if len(plain) > max_len:
        plain = plain[:max_len].rsplit(' ', 1)[0] + '...'
    return html.escape(plain)

# ==============================================================================
# SECTION 11 PROJECT DEFINITIONS
# ==============================================================================
SECTION_11_PROJECTS = [
    {
        "id": "smart_pointer_fun",
        "name": "SmartPointerFun",
        "title": "Smart Pointers & Memory Ownership in Embedded Systems",
        "headline": "std::unique_ptr, Ownership Transfer (std::move), and Custom Deleters for Hardware Registers",
        "emb_class": "emb-high",
        "emb_badge": "⚡ Embedded Relevance: Critical",
        "tags": ["std::unique_ptr", "std::make_unique", "Move Semantics", "Custom Deleters", "MMIO", "AUTOSAR A18-5-8"],
        "summary": "Deep dive into deterministic memory ownership via <code>std::unique_ptr</code>. Explores move semantics, zero-overhead memory guarantees, why <code>std::shared_ptr</code> is avoided in microcontrollers due to control block RAM overhead and atomic ref-counting, and how custom deleters enable RAII over hardware peripherals.",
        "files": ["section_11/SmartPointerFun/SmartPointerFun/main.cpp"],
        "concepts_html": """
        <h3>1. Exclusive Ownership & Zero-Cost Abstraction</h3>
        <p><code>std::unique_ptr&lt;T&gt;</code> represents exclusive ownership of a resource. Unlike raw pointers, it automatically calls <code>delete</code> when exiting scope (RAII). Because <code>std::unique_ptr</code> stores only the raw pointer (with default deleter), it has <strong>zero memory overhead</strong> compared to a raw C pointer (<code>sizeof(unique_ptr&lt;T&gt;) == sizeof(T*)</code>).</p>

        <h3>2. Move Semantics (Ownership Transfer)</h3>
        <p>Because ownership must be exclusive, <code>std::unique_ptr</code> has its copy constructor deleted. Transferring ownership requires explicit move semantics via <code>std::move()</code>, which resets the source pointer to <code>nullptr</code>.</p>
        """,
        "embedded_html": """
        <h3>1. Why std::shared_ptr is Often Banned in Bare-Metal Systems</h3>
        <ul>
          <li><strong>RAM Overhead:</strong> <code>std::shared_ptr</code> allocates a 16-to-24-byte control block on the heap containing two reference counters, a custom deleter, and an allocator pointer. On a 16KB SRAM microcontroller, this memory bloat is unacceptable.</li>
          <li><strong>Thread-Safety Atomic Latency:</strong> Incrementing and decrementing reference counters requires atomic instructions (e.g., <code>LDREX/STREX</code> on ARM Cortex-M), which disable compiler optimizations and increase instruction cycles.</li>
        </ul>

        <h3>2. Custom Deleters for Hardware Peripherals (RAII for MMIO)</h3>
        <p><code>std::unique_ptr</code> can manage non-heap hardware resources—such as hardware mutexes, DMA channels, or power rails—by supplying a custom deleter that turns off clocks or releases locks automatically on scope exit.</p>

        <div class="callout callout-warning">
          <h4>⚠️ AUTOSAR C++14 Rule A18-5-8</h4>
          <p>Objects shall not be created using raw <code>new</code> or <code>delete</code>. All dynamic allocation (if permitted during bootup) must be immediately wrapped in <code>std::unique_ptr</code> or <code>std::make_unique</code>.</p>
        </div>
        """,
        "refactor_html": """
        <p>Here is how embedded engineers use <code>std::unique_ptr</code> with a custom lambda deleter to automatically power-down an SPI peripheral when done:</p>
        <pre class="code-block" style="background:#0d1117; padding:16px; border-radius:8px; border:1px solid #30363d;">#include &lt;memory&gt;
#include &lt;iostream&gt;

struct SpiPeripheral {
    void write(uint8_t data) { std::cout &lt;&lt; "SPI Tx: " &lt;&lt; int(data) &lt;&lt; '\\n'; }
};

// Custom deleter that disables the hardware clock
struct SpiDeleter {
    void operator()(SpiPeripheral* spi) const {
        std::cout &lt;&lt; "Hardware Clock Disabled (Safe RAII State)\\n";
        // e.g., RCC-&gt;APB2ENR &amp;= ~SPI1_EN;
    }
};

using SpiHandle = std::unique_ptr&lt;SpiPeripheral, SpiDeleter&gt;;

void transmitSensorPacket() {
    SpiPeripheral hwSpi;
    SpiHandle handle(&amp;hwSpi); // Automatically unlocks on function exit!
    handle-&gt;write(0xAA);
} // &lt;-- SpiDeleter runs automatically here!</pre>
        """,
        "quiz": [
            {
                "question": "What is the memory size of a std::unique_ptr<int> with the default deleter on a 32-bit ARM Cortex-M architecture?",
                "options": [
                    "4 bytes (identical to a raw pointer)",
                    "8 bytes (pointer + reference count)",
                    "16 bytes (control block overhead)",
                    "0 bytes (fully optimized away)"
                ],
                "correct": 0,
                "explanation": "With the default stateless deleter, <code>std::unique_ptr</code> incurs zero space overhead and occupies exactly 4 bytes on a 32-bit CPU, perfectly mirroring a raw pointer while providing RAII safety."
            },
            {
                "question": "Why is std::make_unique<T>() preferred over std::unique_ptr<T>(new T()) in modern C++?",
                "options": [
                    "It automatically creates a thread for the pointer.",
                    "It guarantees exception safety and prevents resource leaks during multi-argument sub-expression evaluation.",
                    "It converts the pointer into a shared pointer.",
                    "It stores the object in Flash ROM instead of RAM."
                ],
                "correct": 1,
                "explanation": "<code>std::make_unique</code> prevents potential memory leaks when initializing multiple parameters in a function call where one constructor might throw before the pointer is assigned."
            },
            {
                "question": "What happens to the source pointer after executing: std::unique_ptr<int> p2 = std::move(p1);?",
                "options": [
                    "p1 continues to point to the same address.",
                    "p1 is immediately deleted.",
                    "p1 is set to nullptr, relinquishing ownership.",
                    "A compile-time error occurs."
                ],
                "correct": 2,
                "explanation": "<code>std::move()</code> transfers ownership from <code>p1</code> to <code>p2</code>, resetting <code>p1</code> to <code>nullptr</code>."
            }
        ]
    },
    {
        "id": "rule_of_three_five_zero",
        "name": "RuleOfThreeFiveZeroApp",
        "title": "Rule of Three, Five, and Zero in Embedded C++",
        "headline": "Managing Deep Resource Copies, Move Semantics, and Zero-Overhead Lifetime Guarantees",
        "emb_class": "emb-high",
        "emb_badge": "⚡ Embedded Relevance: Critical",
        "tags": ["Rule of 3/5/0", "Copy Ctor", "Move Ctor", "RAII", "Double Free", "DMA Buffers"],
        "summary": "Mastering resource management under C++11/14. We analyze the Rule of Three, the Rule of Five (move semantics), and the Rule of Zero. We investigate double-free hazards, DMA buffer ownership transfers without SRAM copying, and MISRA C++:2008 Rule 12-8-1 compliance.",
        "files": [
            "section_11/RuleOfThreeFiveZeroApp/RuleOfThreeFiveZeroApp/RulesDemo.h",
            "section_11/RuleOfThreeFiveZeroApp/RuleOfThreeFiveZeroApp/main.cpp"
        ],
        "concepts_html": """
        <h3>1. The Rule of Three (C++98)</h3>
        <p>If a class manages a raw resource and defines any of: <strong>Destructor</strong>, <strong>Copy Constructor</strong>, or <strong>Copy Assignment Operator</strong>, it must explicitly implement all three to avoid shallow copy double-free corruption.</p>

        <h3>2. The Rule of Five (C++11)</h3>
        <p>With modern move semantics, classes managing resources should also implement the <strong>Move Constructor</strong> and <strong>Move Assignment Operator</strong> (or mark them <code>= delete</code>). Move operations transfer raw pointer ownership in $O(1)$ time without re-allocating memory.</p>

        <h3>3. The Rule of Zero</h3>
        <p>Design classes that do not directly manage raw resources; use standard RAII wrappers (e.g. <code>std::unique_ptr</code>, <code>std::array</code>). The compiler will automatically generate correct lifetime operations.</p>
        """,
        "embedded_html": """
        <h3>1. Move Semantics for DMA and Sensor Buffers</h3>
        <p>In high-speed data acquisition (e.g. 1 MSPS ADC sampling), transferring 1024-byte buffers between an ISR queue and a processing task via copy constructor wastes CPU cycles and SRAM. Implementing move constructors allows instantaneous $O(1)$ pointer swaps with zero buffer copying.</p>

        <div class="callout callout-warning">
          <h4>⚠️ MISRA C++:2008 Rule 12-8-1 & AUTOSAR A12-8-1</h4>
          <p>A copy constructor and copy assignment operator shall be declared for any class that handles dynamic resources or hardware locks. If copying is nonsensical (e.g. a hardware UART peripheral), both copy operations MUST be explicitly deleted (<code>= delete</code>).</p>
        </div>
        """,
        "refactor_html": """
        <p>Here is an embedded non-copyable, move-only DMA packet buffer compliant with AUTOSAR A12-8-1:</p>
        <pre class="code-block" style="background:#0d1117; padding:16px; border-radius:8px; border:1px solid #30363d;">#include &lt;cstdint&gt;
#include &lt;utility&gt;

class DmaBuffer {
public:
    explicit DmaBuffer(size_t size) : size_(size), data_(new uint8_t[size]) {}
    ~DmaBuffer() { delete[] data_; }

    // Disable dangerous copying (Prevents double-free of DMA buffer)
    DmaBuffer(const DmaBuffer&amp;) = delete;
    DmaBuffer&amp; operator=(const DmaBuffer&amp;) = delete;

    // Enable fast zero-copy move operations
    DmaBuffer(DmaBuffer&amp;&amp; other) noexcept : size_(other.size_), data_(other.data_) {
        other.size_ = 0;
        other.data_ = nullptr;
    }

    DmaBuffer&amp; operator=(DmaBuffer&amp;&amp; other) noexcept {
        if (this != &amp;other) {
            delete[] data_;
            data_ = other.data_;
            size_ = other.size_;
            other.data_ = nullptr;
            other.size_ = 0;
        }
        return *this;
    }

private:
    size_t size_;
    uint8_t* data_;
};</pre>
        """,
        "quiz": [
            {
                "question": "What catastrophic failure occurs if a class allocating dynamic memory relies on the default compiler-generated copy constructor?",
                "options": [
                    "A compile-time template error.",
                    "A shallow copy is made, causing both objects to share the same pointer and triggering a fatal double-free crash upon destruction.",
                    "The object is automatically converted to an rvalue reference.",
                    "The heap memory is converted to static flash memory."
                ],
                "correct": 1,
                "explanation": "Default copy constructors perform a member-wise shallow copy. Both instances will point to the same memory block, and when both destructors run, the second will attempt to delete already-freed memory (double-free vulnerability)."
            },
            {
                "question": "Why should move constructors and move assignment operators always be marked `noexcept` in embedded C++?",
                "options": [
                    "To allow standard containers like std::vector to use move operations instead of falling back to expensive copy operations during reallocation.",
                    "To disable compiler optimization.",
                    "Because embedded microcontrollers do not support exceptions in any form.",
                    "To force the object to be placed in ROM."
                ],
                "correct": 0,
                "explanation": "Containers like <code>std::vector</code> verify if a type's move constructor is <code>noexcept</code>. If it is not, the container falls back to copying elements during reallocation to preserve the strong exception guarantee."
            },
            {
                "question": "What is the 'Rule of Zero'?",
                "options": [
                    "Never write classes with more than zero member variables.",
                    "Classes should rely on RAII member types (like smart pointers) so they do not need custom copy/move/destructor functions.",
                    "All member pointers must be initialized to 0 (NULL).",
                    "A function must take zero arguments to be real-time safe."
                ],
                "correct": 1,
                "explanation": "The Rule of Zero states that if a class is composed of types that already manage their own resources cleanly (e.g. smart pointers, standard containers), the class itself does not need custom special member functions."
            }
        ]
    },
    {
        "id": "map_vs_unordered_map",
        "name": "MapVsUnorderedMappApp",
        "title": "std::map vs std::unordered_map in Real-Time Embedded Systems",
        "headline": "Red-Black Trees vs Hash Tables: Deterministic O(log N) vs Unpredictable O(1) Rehash Latency",
        "emb_class": "emb-high",
        "emb_badge": "⚡ Embedded Relevance: Critical",
        "tags": ["std::map", "std::unordered_map", "Red-Black Trees", "Hash Tables", "Real-Time Determinism", "Flat Maps"],
        "summary": "Comparing ordered Red-Black Trees (<code>std::map</code>) against bucket-based Hash Tables (<code>std::unordered_map</code>). We explore time complexity determinism, catastrophic rehash latency spikes, dynamic node allocation heap fragmentation, and why static flat maps are the standard embedded choice.",
        "files": ["section_11/MapVsUnorderedMappApp/MapVsUnorderedMappApp/main.cpp"],
        "concepts_html": """
        <h3>1. Data Structure Architecture</h3>
        <p><code>std::map</code> is implemented as a <strong>Self-Balancing Red-Black Tree</strong> with strictly ordered keys. Search, insertion, and deletion are guaranteed $O(\log N)$ time.</p>
        <p><code>std::unordered_map</code> is implemented as a <strong>Hash Table with Chaining</strong>. Average lookup is $O(1)$, but worst-case lookup is $O(N)$ when hash collisions occur or when the table triggers a dynamic rehashing re-allocation.</p>
        """,
        "embedded_html": """
        <h3>1. Real-Time Determinism: The Rehash Latency Spike Hazard</h3>
        <p>In hard real-time systems (e.g. braking systems, avionics), an operation must NEVER exceed its worst-case execution time (WCET). While <code>std::unordered_map</code> is fast on average, inserting an element that triggers a bucket table resize reallocates memory and re-hashes every existing entry—causing latency spikes of several milliseconds!</p>

        <h3>2. Heap Fragmentation: 24 to 32 Bytes per Node</h3>
        <p>Both standard containers dynamically allocate individual heap nodes for every stored element (storing tree pointers: parent, left, right, color, or hash buckets). On microcontrollers with limited SRAM, this causes extreme memory fragmentation.</p>

        <div class="callout callout-tip">
          <h4>💡 The Embedded Solution: Flat Maps (Sorted Arrays)</h4>
          <p>For small, fixed sets of keys (e.g. CAN message IDs, sensor calibration tables), use a contiguous sorted <code>std::array&lt;std::pair&lt;K, V&gt;, N&gt;</code> with <code>std::lower_bound</code> for $O(\log N)$ binary search, <strong>zero heap allocations, and 100% L1 cache locality</strong>!</p>
        </div>
        """,
        "refactor_html": """
        <p>Here is an embedded compile-time Flash ROM lookup table using binary search on sorted array:</p>
        <pre class="code-block" style="background:#0d1117; padding:16px; border-radius:8px; border:1px solid #30363d;">#include &lt;array&gt;
#include &lt;algorithm&gt;
#include &lt;iostream&gt;
#include &lt;string_view&gt;

struct CanMessageDescriptor {
    uint32_t canId;
    std::string_view name;
};

// Stored directly in Flash ROM (.rodata) - ZERO RAM overhead!
constexpr std::array&lt;CanMessageDescriptor, 4&gt; CAN_LUT = {{
    {0x100, "Engine RPM"},
    {0x101, "Vehicle Speed"},
    {0x200, "Brake Pressure"},
    {0x305, "Battery Voltage"}
}};

std::string_view lookupCanName(uint32_t id) {
    auto it = std::lower_bound(CAN_LUT.begin(), CAN_LUT.end(), id,
        [](const CanMessageDescriptor&amp; item, uint32_t target) {
            return item.canId &lt; target;
        });

    if (it != CAN_LUT.end() &amp;&amp; it-&gt;canId == id) {
        return it-&gt;name;
    }
    return "Unknown ID";
}</pre>
        """,
        "quiz": [
            {
                "question": "Why is std::map often favored over std::unordered_map in hard real-time mission-critical systems?",
                "options": [
                    "std::map is faster in average lookup than std::unordered_map.",
                    "std::map provides guaranteed, predictable O(log N) worst-case timing without sudden rehashing pauses.",
                    "std::map stores all elements in CPU registers.",
                    "std::unordered_map does not support string keys."
                ],
                "correct": 1,
                "explanation": "<code>std::map</code> guarantees $O(\log N)$ worst-case time complexity, whereas <code>std::unordered_map</code> can spike to $O(N)$ during hash collisions and bucket table reallocations, violating real-time deadlines."
            },
            {
                "question": "What is the primary memory drawback of both std::map and std::unordered_map on memory-constrained microcontrollers?",
                "options": [
                    "They store all data in non-volatile ROM.",
                    "They allocate separate heap nodes for each inserted element, leading to severe RAM fragmentation.",
                    "They cannot store more than 16 elements.",
                    "They disable compiler inlining."
                ],
                "correct": 1,
                "explanation": "Both node-based containers invoke <code>malloc</code> for each element to allocate tree nodes or linked list collision nodes, causing severe SRAM fragmentation and pointer overhead."
            },
            {
                "question": "What embedded idiom offers O(log N) lookup with zero dynamic allocation and maximum cache locality?",
                "options": [
                    "A sorted `std::array` or `etl::vector` queried via `std::lower_bound` (Flat Map).",
                    "A circular singly linked list.",
                    "A global raw `void*` array.",
                    "A recursive switch statement."
                ],
                "correct": 0,
                "explanation": "A Flat Map (contiguous array sorted by key) performs binary search in $O(\log N)$ time, requires zero dynamic allocation, and delivers optimal CPU cache locality."
            }
        ]
    },
    {
        "id": "queue_projects",
        "name": "QueueProjects",
        "title": "Queue Containers & Hardware Ring Buffers",
        "headline": "FIFO Queue Mechanics vs Lock-Free Circular Buffers for Real-Time ISRs",
        "emb_class": "emb-high",
        "emb_badge": "⚡ Embedded Relevance: Critical",
        "tags": ["std::queue", "FIFO", "Circular Ring Buffer", "Lock-Free SPSC", "UART ISR", "DMA"],
        "summary": "Exploring FIFO queue operations and why <code>std::queue</code> (backed by <code>std::deque</code>) is replaced in embedded firmware by bounded, lock-free circular ring buffers for interrupt service routines (UART, SPI, CAN).",
        "files": ["section_11/QueueProjects/QueueProjects/main.cpp"],
        "concepts_html": """
        <h3>1. FIFO Queue Concept</h3>
        <p>A Queue is a First-In-First-Out (FIFO) container adapter providing <code>push()</code> at the back, <code>pop()</code> at the front, and <code>front()</code> element inspection. In standard C++, <code>std::queue</code> wraps an underlying container (defaulting to <code>std::deque</code>).</p>
        """,
        "embedded_html": """
        <h3>1. Why std::queue Cannot Be Used in Interrupt Service Routines (ISRs)</h3>
        <ul>
          <li><strong>Dynamic Chunk Allocation:</strong> <code>std::deque</code> dynamically allocates blocks of memory on the heap. Calling <code>push()</code> inside an ISR can invoke <code>malloc()</code>, which is not interrupt-safe (non-reentrant and non-deterministic).</li>
          <li><strong>Thread Safety:</strong> <code>std::queue</code> is not thread-safe or ISR-safe without mutex locks, which cannot be acquired inside interrupt contexts.</li>
        </ul>

        <div class="callout callout-embedded">
          <h4>💡 The Embedded Gold Standard: Single-Producer Single-Consumer (SPSC) Ring Buffer</h4>
          <p>By using a fixed-capacity circular buffer with atomic head/tail indices, an ISR can push incoming UART bytes while the main task pops them—<strong>with zero mutexes, zero dynamic memory, and zero blocking</strong>!</p>
        </div>
        """,
        "refactor_html": """
        <p>Here is an embedded lock-free SPSC circular ring buffer for microcontroller communication:</p>
        <pre class="code-block" style="background:#0d1117; padding:16px; border-radius:8px; border:1px solid #30363d;">#include &lt;array&gt;
#include &lt;atomic&gt;
#include &lt;optional&gt;
#include &lt;cstdint&gt;

template &lt;typename T, size_t Capacity&gt;
class RingBuffer {
public:
    // Called from ISR (Producer)
    bool push(T item) noexcept {
        size_t head = head_.load(std::memory_order_relaxed);
        size_t nextHead = (head + 1) % Capacity;
        if (nextHead == tail_.load(std::memory_order_acquire)) {
            return false; // Buffer Full! (Drop or flag error)
        }
        buffer_[head] = item;
        head_.store(nextHead, std::memory_order_release);
        return true;
    }

    // Called from Main Thread (Consumer)
    std::optional&lt;T&gt; pop() noexcept {
        size_t tail = tail_.load(std::memory_order_relaxed);
        if (tail == head_.load(std::memory_order_acquire)) {
            return std::nullopt; // Buffer Empty!
        }
        T item = buffer_[tail];
        tail_.store((tail + 1) % Capacity, std::memory_order_release);
        return item;
    }

private:
    std::array&lt;T, Capacity&gt; buffer_;
    std::atomic&lt;size_t&gt; head_{0};
    std::atomic&lt;size_t&gt; tail_{0};
};</pre>
        """,
        "quiz": [
            {
                "question": "What is the primary danger of pushing elements to a default std::queue inside an embedded Interrupt Handler (ISR)?",
                "options": [
                    "The queue automatically deletes all elements.",
                    "Underlying std::deque memory allocation invokes non-reentrant malloc(), causing deadlocks or crashes.",
                    "The CPU clock frequency drops.",
                    "The queue reverses element order."
                ],
                "correct": 1,
                "explanation": "<code>std::queue</code> backed by <code>std::deque</code> dynamically allocates memory chunks on the heap. Heap allocators are non-reentrant and must never be called from ISR context."
            },
            {
                "question": "In a circular ring buffer of capacity N using modulo arithmetic, how is the 'buffer full' condition detected?",
                "options": [
                    "When head == tail.",
                    "When (head + 1) % N == tail.",
                    "When head == N.",
                    "When memory is exhausted."
                ],
                "correct": 1,
                "explanation": "In standard circular buffer design, when incrementing the head index lands on the current tail index, the buffer is full."
            }
        ]
    },
    {
        "id": "remove_erase_idiom",
        "name": "RemoveEraseIdiomApp",
        "title": "The Remove-Erase Idiom and Memory Compaction",
        "headline": "In-Place Vector Compaction, Iterator Invalidation, and C++20 std::erase",
        "emb_class": "emb-med",
        "emb_badge": "⚡ Embedded Relevance: High",
        "tags": ["Erase-Remove", "std::remove", "Iterator Invalidation", "C++20 std::erase", "Memory Compaction"],
        "summary": "Understanding the separation of algorithms from containers in C++. We dissect why <code>std::remove</code> does not alter container size, analyze iterator invalidation hazards during array filtering, and review C++20 <code>std::erase</code>.",
        "files": ["section_11/RemoveEraseIdiomApp/RemoveEraseIdiomApp/main.cpp"],
        "concepts_html": """
        <h3>1. The Two-Step Remove-Erase Idiom</h3>
        <p>In standard C++, <code>std::remove</code> only shifts non-matching elements to the front of the range and returns a past-the-end iterator. It cannot alter the container's <code>size()</code> because generic algorithms operate only on iterators without knowledge of container topology. The container's <code>erase()</code> method must be called to truncate the tail.</p>
        <pre class="code-block" style="background:#161b22; padding:10px; border-radius:6px;">vec.erase(std::remove(vec.begin(), vec.end(), targetValue), vec.end());</pre>
        """,
        "embedded_html": """
        <h3>1. Deterministic In-Place Compaction</h3>
        <p>The remove-erase idiom operates strictly <strong>in-place with $O(N)$ linear time and $O(1)$ auxiliary space</strong>. In embedded sensor filtering (e.g. stripping corrupted checksum packets from an acquisition buffer), in-place compaction avoids allocating secondary temporary buffers.</p>

        <div class="callout callout-warning">
          <h4>⚠️ Iterator Invalidation Hazards</h4>
          <p>Calling <code>erase()</code> invalidates iterators pointing to deleted and subsequent elements. Performing manual loops with <code>vec.erase(it)</code> without updating <code>it = vec.erase(it)</code> results in undefined memory dereferences.</p>
        </div>
        """,
        "refactor_html": """
        <p>In modern C++20, the verbose two-step idiom is replaced with uniform, clear <code>std::erase</code>:</p>
        <pre class="code-block" style="background:#0d1117; padding:16px; border-radius:8px; border:1px solid #30363d;">#include &lt;vector&gt;
#include &lt;iostream&gt;

int main() {
    std::vector&lt;int&gt; sensorReadings = {10, -999, 25, -999, 32};

    // Modern C++20: Single expressive call
    std::erase(sensorReadings, -999);

    for (int val : sensorReadings) {
        std::cout &lt;&lt; val &lt;&lt; ' '; // Prints: 10 25 32
    }
    return 0;
}</pre>
        """,
        "quiz": [
            {
                "question": "Why does std::remove(vec.begin(), vec.end(), val) not change the size of the vector by itself?",
                "options": [
                    "It is a bug in the standard library.",
                    "std::remove operates solely on iterators and has no member access to the underlying container's size or memory allocator.",
                    "It only marks elements as invisible.",
                    "It converts elements to nullptrs."
                ],
                "correct": 1,
                "explanation": "STL algorithms are decoupled from containers. <code>std::remove</code> moves valid elements to the front and returns an iterator to the new logical end, requiring <code>vec.erase()</code> to deallocate the remaining tail."
            },
            {
                "question": "What is the time complexity of the Erase-Remove idiom on a contiguous array of N elements?",
                "options": [
                    "O(1)",
                    "O(N) linear time with O(1) extra memory",
                    "O(N^2) quadratic time",
                    "O(log N)"
                ],
                "correct": 1,
                "explanation": "The algorithm makes a single pass over the elements ($O(N)$ comparisons and moves) and shifts elements in-place with zero additional memory allocation."
            }
        ]
    },
    {
        "id": "templates",
        "name": "Templates",
        "title": "C++ Templates & Flash ROM Code Bloat Management",
        "headline": "Generic Programming vs Flash Memory Overhead in Embedded Microcontrollers",
        "emb_class": "emb-high",
        "emb_badge": "⚡ Embedded Relevance: Critical",
        "tags": ["Templates", "Generic Code", "Code Bloat", "Flash ROM", "Zero-Cost Inlining", "C++17 if constexpr"],
        "summary": "Exploring generic function and class templates. We examine compile-time monomorphization, compare zero-overhead inlining against Flash ROM binary expansion (template code bloat), and demonstrate techniques to share implementation code across instantiations.",
        "files": ["section_11/Templates/Templates/main.cpp"],
        "concepts_html": """
        <h3>1. Compile-Time Monomorphization</h3>
        <p>Unlike Java or C# generics (which use type erasure at runtime), C++ templates are instantiated at compile-time. The compiler generates an entirely dedicated copy of the machine code for each unique type (<code>print&lt;int&gt;</code>, <code>print&lt;double&gt;</code>, <code>print&lt;string&gt;</code>).</p>
        """,
        "embedded_html": """
        <h3>1. The Flash ROM Code Bloat Hazard</h3>
        <p>If a large template class is instantiated with 10 different types on a 64KB Flash microcontroller, the compiler will emit 10 distinct copies of the class binary, easily overflowing available Flash ROM.</p>

        <div class="callout callout-tip">
          <h4>💡 Embedded Optimization: Template Hoisting (Common Base Idiom)</h4>
          <p>Extract all type-independent code into a non-templated base class. The templated derived class only implements thin inline type-casts, sharing a single binary implementation in Flash ROM!</p>
        </div>
        """,
        "refactor_html": """
        <p>Template hoisting pattern reducing Flash ROM consumption:</p>
        <pre class="code-block" style="background:#0d1117; padding:16px; border-radius:8px; border:1px solid #30363d;">// Non-templated base: Single copy in Flash ROM (.text)
class CircularBufferBase {
protected:
    void* buffer_;
    size_t head_ = 0, tail_ = 0, capacity_;
    void advanceTail() { tail_ = (tail_ + 1) % capacity_; }
};

// Thin templated wrapper: Inlined with ZERO extra Flash code
template &lt;typename T, size_t N&gt;
class CircularBuffer : public CircularBufferBase {
public:
    CircularBuffer() { buffer_ = storage_; capacity_ = N; }
    void push(T val) { storage_[head_] = val; head_ = (head_ + 1) % N; }
private:
    T storage_[N];
};</pre>
        """,
        "quiz": [
            {
                "question": "What is 'template code bloat' in embedded microcontroller firmware?",
                "options": [
                    "A compiler warning when template parameters are too long.",
                    "The generation of multiple redundant machine-code copies in Flash ROM for every unique template type instantiation.",
                    "An error caused by insufficient stack memory.",
                    "A runtime exception thrown when templates exceed 1KB."
                ],
                "correct": 1,
                "explanation": "Because C++ instantiates dedicated machine code for every type passed to a template, instantiating templates with numerous types can rapidly exhaust MCU Flash ROM."
            }
        ]
    },
    {
        "id": "rules_challenge",
        "name": "RulesChallenge",
        "title": "Custom Dynamic Buffer & Memory Safety",
        "headline": "Deep Copy, Destructor Safety, and Bounded Buffer Alternatives",
        "emb_class": "emb-high",
        "emb_badge": "⚡ Embedded Relevance: High",
        "tags": ["Buffer Management", "Deep Copy", "Rule of Three", "Dynamic Memory", "Memory Leaks"],
        "summary": "Hands-on implementation of a custom dynamic buffer class adhering to the Rule of Three. We inspect deep copy allocation, memory leak prevention, and bounded static buffer alternatives for microcontrollers.",
        "files": [
            "section_11/RulesChallenge/RulesChallenge/Buffer.h",
            "section_11/RulesChallenge/RulesChallenge/main.cpp"
        ],
        "concepts_html": """
        <h3>1. Deep Copy Implementation</h3>
        <p>When copying a buffer, memory must be allocated independently for the destination instance, followed by copying the data payload using <code>std::copy</code> or <code>memcpy</code>.</p>
        """,
        "embedded_html": """
        <h3>1. Bounded Static Buffers vs Dynamic Buffers</h3>
        <p>In safety-critical firmware, dynamic buffers should be replaced with fixed-capacity stack/static buffers (<code>std::span</code> or <code>std::array</code>) to guarantee zero heap fragmentation and deterministic lifetime.</p>
        """,
        "refactor_html": """
        <pre class="code-block" style="background:#0d1117; padding:16px; border-radius:8px; border:1px solid #30363d;">#include &lt;array&gt;
#include &lt;cstdint&gt;
#include &lt;iostream&gt;

template &lt;size_t BoundedCapacity&gt;
class StaticBuffer {
public:
    bool append(uint8_t byte) {
        if (size_ &gt;= BoundedCapacity) return false;
        data_[size_++] = byte;
        return true;
    }
    size_t size() const { return size_; }
private:
    std::array&lt;uint8_t, BoundedCapacity&gt; data_;
    size_t size_ = 0;
};</pre>
        """,
        "quiz": [
            {
                "question": "What is the primary benefit of replacing dynamic buffers with bounded static buffers in embedded firmware?",
                "options": [
                    "Guaranteed memory allocation at compile-time with zero heap fragmentation.",
                    "Ability to resize buffers infinitely.",
                    "Automatic networking support.",
                    "Slower CPU frequency."
                ],
                "correct": 0,
                "explanation": "Static bounded buffers allocate fixed storage at compile time, eliminating all runtime heap allocation, memory leaks, and fragmentation."
            }
        ]
    },
    {
        "id": "algorithm_fun",
        "name": "AlgorithmFun",
        "title": "STL Algorithms, Lambdas, and Zero-Cost Inlining",
        "headline": "std::sort, std::count_if, and Lambda Inlining vs C qsort Function Pointers",
        "emb_class": "emb-high",
        "emb_badge": "⚡ Embedded Relevance: High",
        "tags": ["<algorithm>", "std::sort", "std::count_if", "Lambdas", "Zero-Cost Abstractions"],
        "summary": "Exploring the standard algorithm library. We demonstrate why C++ templates and lambdas outperform traditional C <code>qsort()</code> by enabling complete compiler inlining, and examine stack consumption during recursive algorithms.",
        "files": ["section_11/AlgorithmFun/AlgorithmFun/main.cpp"],
        "concepts_html": """
        <h3>1. Decoupled Iterators and Generic Predicates</h3>
        <p>STL algorithms in <code>&lt;algorithm&gt;</code> operate uniformly on iterator ranges <code>[begin, end)</code> and accept stateless or capturing lambdas as evaluation predicates.</p>
        """,
        "embedded_html": """
        <h3>1. Zero-Cost Abstraction: Lambdas vs C Function Pointers</h3>
        <p>In C, <code>qsort()</code> requires a function pointer callback, forcing an indirect call for every comparison. In C++, <code>std::sort</code> accepts a lambda whose type is known at compile time, allowing the compiler to <strong>inline the comparison directly into the sort loop</strong> for maximum throughput.</p>
        """,
        "refactor_html": """
        <pre class="code-block" style="background:#0d1117; padding:16px; border-radius:8px; border:1px solid #30363d;">#include &lt;algorithm&gt;
#include &lt;array&gt;
#include &lt;iostream&gt;

int main() {
    std::array&lt;int, 5&gt; telemetry = {45, 12, 85, 32, 89};
    
    // Fully inlined at -O2: Zero function pointer overhead
    std::sort(telemetry.begin(), telemetry.end(), [](int a, int b) {
        return a &lt; b;
    });

    for (int val : telemetry) std::cout &lt;&lt; val &lt;&lt; ' ';
    return 0;
}</pre>
        """,
        "quiz": [
            {
                "question": "Why is std::sort typically significantly faster than C qsort() on ARM microcontrollers?",
                "options": [
                    "std::sort uses hardware floating-point acceleration.",
                    "std::sort is templated on the comparator type, enabling the compiler to inline comparisons and eliminate indirect function calls.",
                    "qsort() allocates memory on the heap.",
                    "std::sort runs in parallel on all cores."
                ],
                "correct": 1,
                "explanation": "Because <code>std::sort</code> knows the exact comparator type at compile-time, it inlines the predicate directly, avoiding indirect function pointer jumps."
            }
        ]
    },
    {
        "id": "stl_fun1",
        "name": "STLFun1",
        "title": "std::vector Memory Growth & Allocation Hazards",
        "headline": "Capacity Doubling, Reallocation Overhead, and reserve() Optimization",
        "emb_class": "emb-high",
        "emb_badge": "⚡ Embedded Relevance: Critical",
        "tags": ["std::vector", "push_back", "Capacity Growth", "reserve()", "Reallocation Latency"],
        "summary": "Dissecting <code>std::vector</code> mechanics. We explore geometric capacity doubling, sudden heap reallocations during <code>push_back()</code>, pointer invalidation, and how <code>reserve()</code> guarantees deterministic performance.",
        "files": ["section_11/STLFun1/STLFun1/main.cpp"],
        "concepts_html": """
        <h3>1. Size vs Capacity and Geometric Growth</h3>
        <p>A vector maintains <code>size()</code> (active elements) and <code>capacity()</code> (allocated slots). When <code>size() == capacity()</code>, the next <code>push_back()</code> allocates a new block (typically $1.5\times$ or $2\times$ size), copies/moves existing elements, and frees the old block.</p>
        """,
        "embedded_html": """
        <h3>1. The Reallocation Latency Spike in Microcontrollers</h3>
        <p>A single <code>push_back()</code> can unexpectedly trigger a heavy memory reallocation, copying hundreds of elements and causing non-deterministic execution spikes.</p>

        <div class="callout callout-tip">
          <h4>💡 Mandatory Best Practice: Always Use reserve()</h4>
          <p>If maximum capacity is known in advance, call <code>vec.reserve(MAX_SIZE)</code> during initialization to eliminate all runtime reallocations.</p>
        </div>
        """,
        "refactor_html": """
        <pre class="code-block" style="background:#0d1117; padding:16px; border-radius:8px; border:1px solid #30363d;">#include &lt;vector&gt;
#include &lt;iostream&gt;

void initAdcTelemetry() {
    std::vector&lt;uint16_t&gt; adcSamples;
    adcSamples.reserve(256); // Pre-allocate: ZERO reallocations during sampling!

    for (int i = 0; i &lt; 256; ++i) {
        adcSamples.push_back(i * 4); // Deterministic O(1) insertion
    }
}</pre>
        """,
        "quiz": [
            {
                "question": "What happens when push_back() is called on a std::vector whose size() is equal to its capacity()?",
                "options": [
                    "The element is silently discarded.",
                    "A new larger heap memory block is allocated, all existing elements are copied or moved, the old block is freed, and existing iterators/pointers are invalidated.",
                    "A compile-time error occurs.",
                    "The vector size becomes 0."
                ],
                "correct": 1,
                "explanation": "When capacity is exceeded, the vector must allocate a new larger memory block, move all elements over, and release the old memory, invalidating all iterators and pointers to its elements."
            }
        ]
    },
    {
        "id": "advanced_stl_app",
        "name": "AdvancedSTLApp",
        "title": "std::deque & std::list: Cache Locality & Memory Layout",
        "headline": "Contiguous Memory vs Pointer Chasing and Node Allocation Overhead",
        "emb_class": "emb-high",
        "emb_badge": "⚡ Embedded Relevance: High",
        "tags": ["std::deque", "std::list", "Cache Locality", "Pointer Chasing", "L1 Data Cache"],
        "summary": "Comparing non-contiguous containers (<code>std::deque</code>, <code>std::list</code>) against contiguous arrays. We examine CPU cache lines, L1 cache misses from pointer chasing, and node memory overhead in embedded architectures.",
        "files": ["section_11/AdvancedSTLApp/AdvancedSTLApp/main.cpp"],
        "concepts_html": """
        <h3>1. Linked Lists vs Double-Ended Queues</h3>
        <p><code>std::list</code> is a doubly linked list where each node contains pointers to next and previous nodes. <code>std::deque</code> is a map of fixed-size chunks.</p>
        """,
        "embedded_html": """
        <h3>1. Cache Line Penalties and Memory Overhead</h3>
        <p>On modern MCUs with caches (e.g. ARM Cortex-M7), iterating through contiguous arrays (<code>std::vector</code> / <code>std::array</code>) triggers pre-fetching. In contrast, <code>std::list</code> causes constant L1 cache misses due to scattered heap node addresses (pointer chasing).</p>
        """,
        "refactor_html": """
        <pre class="code-block" style="background:#0d1117; padding:16px; border-radius:8px; border:1px solid #30363d;">// Prefer contiguous std::array for maximum CPU cache throughput
#include &lt;array&gt;
#include &lt;iostream&gt;

void processSensorArray() {
    std::array&lt;int, 64&gt; fastData;
    // Sequential memory access maximizes cache line utilization
}</pre>
        """,
        "quiz": [
            {
                "question": "Why does std::vector almost always outperform std::list for sequential iteration on modern microcontrollers?",
                "options": [
                    "std::vector utilizes CPU register caches.",
                    "Contiguous memory layout provides optimal CPU cache locality and spatial prefetching, avoiding pointer chasing.",
                    "std::list cannot store integers.",
                    "std::vector uses assembly language."
                ],
                "correct": 1,
                "explanation": "Contiguous storage means adjacent elements reside in the same CPU cache line, whereas linked list nodes are scattered across RAM, causing pipeline stalls on cache misses."
            }
        ]
    },
    {
        "id": "advanced_stl_challenge_app",
        "name": "AdvancedSTLChallengeApp",
        "title": "Advanced STL Container Operations",
        "headline": "Container Selection Trade-Offs in Embedded Design",
        "emb_class": "emb-med",
        "emb_badge": "⚡ Embedded Relevance: Medium",
        "tags": ["STL Containers", "Container Selection", "Performance"],
        "summary": "Hands-on challenge manipulating STL containers, demonstrating selection guidelines based on insertion patterns, search frequencies, and memory limits.",
        "files": ["section_11/AdvancedSTLChallengeApp/AdvancedSTLChallengeApp/main.cpp"],
        "concepts_html": "<h3>Container Selection Rules</h3><p>Select containers based on algorithmic complexity and memory topology.</p>",
        "embedded_html": "<h3>Embedded Guidelines</h3><p>Default to contiguous containers unless non-relocating element requirements mandate node containers.</p>",
        "refactor_html": "<pre class=\"code-block\" style=\"background:#0d1117; padding:16px; border-radius:8px;\">// Always prefer contiguous bounded memory\n#include &lt;array&gt;\nstd::array&lt;int, 10&gt; fixedContainer;</pre>",
        "quiz": [
            {
                "question": "Which container should be the default choice for sequential collections in modern C++?",
                "options": ["std::list", "std::vector (or std::array if size is fixed)", "std::deque", "std::forward_list"],
                "correct": 1,
                "explanation": "<code>std::vector</code> and <code>std::array</code> provide optimal cache performance and lowest per-element overhead."
            }
        ]
    },
    {
        "id": "car_project",
        "name": "CarProject",
        "title": "Encapsulation & Object Composition",
        "headline": "Modeling Hardware Subsystems using Class Encapsulation",
        "emb_class": "emb-core",
        "emb_badge": "⚡ Embedded Relevance: Core",
        "tags": ["Encapsulation", "Composition", "Object Design", "Hardware Modeling"],
        "summary": "Demonstrating class encapsulation, private data invariants, and composition to model automotive subsystems.",
        "files": [
            "section_11/CarProject/CarProject/Car.h",
            "section_11/CarProject/CarProject/Car.cpp",
            "section_11/CarProject/CarProject/main.cpp"
        ],
        "concepts_html": "<h3>Encapsulation & Invariants</h3><p>Encapsulation ensures object state is modified only via validated member functions.</p>",
        "embedded_html": "<h3>Hardware Abstraction Layers (HAL)</h3><p>Encapsulation models physical hardware modules (Engine Controller, Brake Actuator) cleanly.</p>",
        "refactor_html": "<pre class=\"code-block\" style=\"background:#0d1117; padding:16px; border-radius:8px;\">class MotorController {\npublic:\n    void setPwmDuty(uint8_t duty) { duty_ = (duty &gt; 100) ? 100 : duty; }\nprivate:\n    uint8_t duty_ = 0;\n};</pre>",
        "quiz": [
            {
                "question": "Why is encapsulation critical in embedded device drivers?",
                "options": ["It hides register manipulation details and enforces valid hardware operating states.", "It increases clock speed.", "It converts variables to pointers.", "It prevents compiling."],
                "correct": 0,
                "explanation": "Encapsulation protects hardware registers from invalid bit states and restricts access to validated driver methods."
            }
        ]
    },
    {
        "id": "contacts_fun",
        "name": "ContactsFun",
        "title": "Associative Key-Value Mappings",
        "headline": "std::map for Dynamic Configuration & Lookup Tables",
        "emb_class": "emb-med",
        "emb_badge": "⚡ Embedded Relevance: Medium",
        "tags": ["std::map", "Key-Value", "Associative Lookup"],
        "summary": "Using associative mappings for key-value pair storage, with focus on lookup mechanics and embedded ROM alternative tables.",
        "files": ["section_11/ContactsFun/ContactsFun/main.cpp"],
        "concepts_html": "<h3>Associative Access</h3><p>Maps allow lookup by arbitrary key types using balanced search trees.</p>",
        "embedded_html": "<h3>Flash ROM Lookups</h3><p>In firmware, key-value mappings are often stored in Flash ROM as constant arrays to conserve SRAM.</p>",
        "refactor_html": "<pre class=\"code-block\" style=\"background:#0d1117; padding:16px; border-radius:8px;\">struct KeyValue { const char* key; const char* val; };\nstatic constexpr KeyValue CONFIG_LUT[] = { {\"BAUD\", \"115200\"}, {\"NODE_ID\", \"0x42\"} };</pre>",
        "quiz": [
            {
                "question": "What is the key lookup complexity in std::map?",
                "options": ["O(1)", "O(log N)", "O(N)", "O(N log N)"],
                "correct": 1,
                "explanation": "<code>std::map</code> is a Red-Black Tree providing guaranteed $O(\log N)$ search time."
            }
        ]
    },
    {
        "id": "crop_hybridization_simulator",
        "name": "CropHybridizationSimulator",
        "title": "Value Types & Operator Overloading in Simulations",
        "headline": "Modeling Value Semantics without Pointer Overhead",
        "emb_class": "emb-core",
        "emb_badge": "⚡ Embedded Relevance: Core",
        "tags": ["Value Semantics", "Operator Overloading", "Copying"],
        "summary": "Exploring value types and operator overloading in simulation modeling.",
        "files": [
            "section_11/CropHybridizationSimulator/CropHybridizationSimulator/Crop.h",
            "section_11/CropHybridizationSimulator/CropHybridizationSimulator/Crop.cpp",
            "section_11/CropHybridizationSimulator/CropHybridizationSimulator/main.cpp"
        ],
        "concepts_html": "<h3>Value Semantics</h3><p>Value types manage their own state cleanly without requiring pointer indirection.</p>",
        "embedded_html": "<h3>Stack-Based Physics & Control</h3><p>Value objects are placed on the stack or in static arrays with zero dynamic allocation.</p>",
        "refactor_html": "<pre class=\"code-block\" style=\"background:#0d1117; padding:16px; border-radius:8px;\">struct Vector3D { float x, y, z; Vector3D operator+(const Vector3D&amp; o) const { return {x+o.x, y+o.y, z+o.z}; } };</pre>",
        "quiz": [
            {
                "question": "What is an advantage of value types in embedded systems?",
                "options": ["They reside on the stack or in static memory with zero heap allocation.", "They require heap allocation.", "They must use virtual functions.", "They cannot be copied."],
                "correct": 0,
                "explanation": "Value types avoid pointer dereferencing and heap allocation overhead."
            }
        ]
    },
    {
        "id": "friend_fun",
        "name": "FriendFun",
        "title": "Friend Functions & Classes in Driver Architectures",
        "headline": "Controlled Access to Private Hardware Drivers",
        "emb_class": "emb-high",
        "emb_badge": "⚡ Embedded Relevance: High",
        "tags": ["friend", "Encapsulation", "Hardware Drivers", "HAL"],
        "summary": "Understanding the <code>friend</code> keyword to grant privileged internal access to helper classes without exposing raw registers globally.",
        "files": [
            "section_11/FriendFun/FriendFun/Rectangle.h",
            "section_11/FriendFun/FriendFun/Rectangle.cpp",
            "section_11/FriendFun/FriendFun/RectangleHelper.h",
            "section_11/FriendFun/FriendFun/main.cpp"
        ],
        "concepts_html": "<h3>Friendship in C++</h3><p><code>friend</code> declarations grant external functions or classes access to private/protected members.</p>",
        "embedded_html": "<h3>HAL & Driver Cohesion</h3><p>A hardware Peripheral class can grant friend access to a Diagnostic Manager without making low-level configuration registers public.</p>",
        "refactor_html": "<pre class=\"code-block\" style=\"background:#0d1117; padding:16px; border-radius:8px;\">class UartDriver {\n    friend class UartDiagnostics;\nprivate:\n    uint32_t errorCount_ = 0;\n};</pre>",
        "quiz": [
            {
                "question": "Is friendship in C++ inherited or transitive?",
                "options": ["Yes, derived classes inherit friends automatically.", "No, friendship is neither inherited nor transitive.", "Yes, friends of friends are friends.", "Only in C++20."],
                "correct": 1,
                "explanation": "Friendship is strictly non-inherited and non-transitive; each class must explicitly grant access."
            }
        ]
    },
    {
        "id": "language_translator_project",
        "name": "LanguageTranslatorProject",
        "title": "Multi-Key Lookup & Static Flash Tables",
        "headline": "Dictionary Lookups: Heap Maps vs Compile-Time Flash Tables",
        "emb_class": "emb-med",
        "emb_badge": "⚡ Embedded Relevance: Medium",
        "tags": ["Dictionary", "std::map", "Flash ROM", "constexpr"],
        "summary": "Building dictionary lookups and evaluating Flash ROM <code>constexpr</code> lookup tables for embedded systems.",
        "files": [
            "section_11/LanguageTranslatorProject/LanguageTranslatorProject/LanguageTranslator.h",
            "section_11/LanguageTranslatorProject/LanguageTranslatorProject/LanguageTranslator.cpp",
            "section_11/LanguageTranslatorProject/LanguageTranslatorProject/main.cpp"
        ],
        "concepts_html": "<h3>Multi-Element Map Queries</h3><p>Managing string-to-string associations and handling missing key lookups.</p>",
        "embedded_html": "<h3>Diagnostic Trouble Codes (DTC)</h3><p>In automotive firmware, fault code string tables are stored entirely in Flash ROM to save SRAM.</p>",
        "refactor_html": "<pre class=\"code-block\" style=\"background:#0d1117; padding:16px; border-radius:8px;\">constexpr const char* getDtcDescription(uint16_t code) {\n    return (code == 0x0100) ? \"Mass Air Flow Fault\" : \"Unknown\";\n}</pre>",
        "quiz": [
            {
                "question": "Where should static lookup tables be stored in embedded systems to conserve SRAM?",
                "options": ["On the heap via malloc.", "In Flash ROM using `constexpr` or `const` in `.rodata` section.", "On the stack.", "In the CPU interrupt vector table."],
                "correct": 1,
                "explanation": "Marking tables <code>constexpr</code> places them in read-only Flash ROM (.rodata), consuming 0 bytes of SRAM."
            }
        ]
    },
    {
        "id": "overloading_fun",
        "name": "OverloadingFun",
        "title": "Operator Overloading & Fixed-Point Arithmetic",
        "headline": "Creating Type-Safe Physical Units & Fixed-Point Math Wrappers",
        "emb_class": "emb-high",
        "emb_badge": "⚡ Embedded Relevance: High",
        "tags": ["Operator Overloading", "Fixed-Point", "Type Safety", "Physical Units"],
        "summary": "Exploring operator overloading (<code>+</code>, <code>==</code>, <code>&lt;&lt;</code>). We show how embedded systems use operator overloading to build type-safe physical unit types (Volts, Amperes) and fixed-point math wrappers avoiding FPU overhead.",
        "files": [
            "section_11/OverloadingFun/OverloadingFun/Rectangle.h",
            "section_11/OverloadingFun/OverloadingFun/Rectangle.cpp",
            "section_11/OverloadingFun/OverloadingFun/main.cpp"
        ],
        "concepts_html": "<h3>Operator Overloading Syntax</h3><p>Custom classes can overload arithmetic and comparison operators to act like fundamental types.</p>",
        "embedded_html": "<h3>Fixed-Point Math for Cortex-M0/M3 (No FPU)</h3><p>Microcontrollers without hardware Floating Point Units emulate floats in software, taking dozens of cycles. Overloading operators on fixed-point integer types enables fast arithmetic with clean mathematical syntax.</p>",
        "refactor_html": "<pre class=\"code-block\" style=\"background:#0d1117; padding:16px; border-radius:8px;\">struct Millivolts {\n    int32_t val;\n    constexpr Millivolts operator+(Millivolts o) const { return {val + o.val}; }\n    constexpr bool operator==(Millivolts o) const { return val == o.val; }\n};</pre>",
        "quiz": [
            {
                "question": "Why is operator overloading beneficial for physical units in embedded systems?",
                "options": ["It guarantees unit compatibility at compile-time (e.g. preventing adding Volts to Amperes) with zero runtime cost.", "It automatically converts floats to doubles.", "It allocates units on the heap.", "It bypasses the compiler."],
                "correct": 0,
                "explanation": "Type-safe unit wrappers catch physical calculation mistakes at compile time with zero runtime overhead."
            }
        ]
    },
    {
        "id": "stack_fun",
        "name": "StackFun",
        "title": "LIFO Stacks: Container Adapters vs MCU Call Stacks",
        "headline": "std::stack Mechanics, Stack Overflow Hazards, and MPU Guards",
        "emb_class": "emb-high",
        "emb_badge": "⚡ Embedded Relevance: High",
        "tags": ["std::stack", "LIFO", "Call Stack", "Stack Overflow", "MPU"],
        "summary": "Understanding LIFO stack adapters. We compare data structure stacks with the hardware MCU execution stack, explore stack overflow risks, and examine memory protection unit (MPU) stack watermarking.",
        "files": ["section_11/StackFun/StackFun/main.cpp"],
        "concepts_html": "<h3>LIFO Stack Operations</h3><p><code>std::stack</code> provides <code>push()</code>, <code>pop()</code>, <code>top()</code>, and <code>empty()</code> using LIFO semantics.</p>",
        "embedded_html": "<h3>Hardware Call Stack Constraints</h3><p>On microcontrollers, stack memory is shared between local variables and interrupt context saving. Stack overflow corrupts global variables silently unless MPU guards are enabled.</p>",
        "refactor_html": "<pre class=\"code-block\" style=\"background:#0d1117; padding:16px; border-radius:8px;\">template &lt;typename T, size_t MaxDepth&gt;\nclass StaticStack {\npublic:\n    bool push(T val) { if (top_ &gt;= MaxDepth) return false; data_[top_++] = val; return true; }\n    T pop() { return data_[--top_]; }\nprivate:\n    std::array&lt;T, MaxDepth&gt; data_; size_t top_ = 0;\n};</pre>",
        "quiz": [
            {
                "question": "What is a primary danger of deeply nested recursive functions on microcontrollers?",
                "options": ["Exhausting the fixed MCU hardware call stack and corrupting RAM (Stack Overflow).", "Disabling compiler optimization.", "Destroying flash memory permanently.", "Causing a division by zero."],
                "correct": 0,
                "explanation": "Microcontrollers have limited stack memory (often 1KB-8KB); recursion risks overflowing into heap/static RAM."
            }
        ]
    },
    {
        "id": "swapper_test",
        "name": "SwapperTest",
        "title": "Generic Template Swapping",
        "headline": "Pass-by-Reference & Zero-Copy Value Exchanges",
        "emb_class": "emb-core",
        "emb_badge": "⚡ Embedded Relevance: Core",
        "tags": ["Templates", "std::swap", "Pass-by-Reference"],
        "summary": "Implementing generic swap templates using reference passing without heap allocations.",
        "files": [
            "section_11/SwapperTest/SwapperTest/Swapper.h",
            "section_11/SwapperTest/SwapperTest/main.cpp"
        ],
        "concepts_html": "<h3>Generic Reference Swapping</h3><p>Using template references <code>T&amp;</code> allows modifying caller variables directly without copies.</p>",
        "embedded_html": "<h3>Register Swaps</h3><p>Compilers optimize reference swaps directly into CPU register instructions (e.g. <code>MOV</code>/<code>REV</code>).</p>",
        "refactor_html": "<pre class=\"code-block\" style=\"background:#0d1117; padding:16px; border-radius:8px;\">template &lt;typename T&gt;\nvoid fastSwap(T&amp; a, T&amp; b) noexcept {\n    T tmp = std::move(a); a = std::move(b); b = std::move(tmp);\n}</pre>",
        "quiz": [
            {
                "question": "Why is pass-by-reference essential in template swap functions?",
                "options": ["To avoid expensive copies and modify the original variables in-place.", "To allocate pointers dynamically.", "To enable runtime polymorphism.", "To store values in ROM."],
                "correct": 0,
                "explanation": "Pass-by-reference enables in-place modification and avoids copying large payloads."
            }
        ]
    }
]

# ==============================================================================
# SECTION 12 PROJECT DEFINITIONS (Data Structures)
# ==============================================================================
SECTION_12_PROJECTS = [
    {
        "id": "array_queue_app",
        "name": "ArrayQueueApp",
        "title": "Circular Array Queue: The Core Embedded Ring Buffer",
        "headline": "Implementing Bounded FIFO Queues with Modulo Arithmetic for Non-Blocking ISRs",
        "emb_class": "emb-high",
        "emb_badge": "⚡ Embedded Relevance: Critical",
        "tags": ["ArrayQueue", "Ring Buffer", "Modulo Arithmetic", "Bounded Memory", "ISR Safety"],
        "summary": "Deep dive into circular array queue data structures. We examine index wrapping using modulo arithmetic, full/empty state disambiguation, and why array-backed ring buffers are the foundational communication pipeline for embedded UART, CAN, and SPI drivers.",
        "files": [
            "section_12/ArrayQueueApp/ArrayQueueApp/Queue.h",
            "section_12/ArrayQueueApp/ArrayQueueApp/ArrayQueue.h",
            "section_12/ArrayQueueApp/ArrayQueueApp/main.cpp"
        ],
        "concepts_html": """
        <h3>1. Abstract Interface & Array Implementation</h3>
        <p>The <code>Queue&lt;T&gt;</code> interface defines <code>enqueue</code>, <code>dequeue</code>, <code>peek</code>, and <code>isEmpty</code>. <code>ArrayQueue&lt;T&gt;</code> implements these operations in fixed contiguous memory using circular indexing.</p>

        <div class="diagram-container">
          <h4>🔄 Circular Ring Buffer FIFO Architecture</h4>
          <svg class="svg-diagram" width="540" height="170" viewBox="0 0 540 170" xmlns="http://www.w3.org/2000/svg">
            <rect x="20" y="45" width="55" height="55" rx="6" fill="#1e293b" stroke="#10b981" stroke-width="2"/>
            <text x="47" y="77" fill="#f0fdf4" font-family="monospace" font-size="13" text-anchor="middle">Slot 0</text>
            <rect x="85" y="45" width="55" height="55" rx="6" fill="#1e293b" stroke="#10b981" stroke-width="2"/>
            <text x="112" y="77" fill="#f0fdf4" font-family="monospace" font-size="13" text-anchor="middle">Slot 1</text>
            <rect x="150" y="45" width="55" height="55" rx="6" fill="#1e293b" stroke="#38bdf8" stroke-width="2"/>
            <text x="177" y="77" fill="#f0fdf4" font-family="monospace" font-size="13" text-anchor="middle">Slot 2</text>
            <rect x="215" y="45" width="55" height="55" rx="6" fill="#1e293b" stroke="#38bdf8" stroke-width="2"/>
            <text x="242" y="77" fill="#f0fdf4" font-family="monospace" font-size="13" text-anchor="middle">Slot 3</text>
            <rect x="280" y="45" width="55" height="55" rx="6" fill="#0f172a" stroke="#475569" stroke-width="1.5" stroke-dasharray="4"/>
            <text x="307" y="77" fill="#64748b" font-family="monospace" font-size="13" text-anchor="middle">Empty</text>
            <rect x="345" y="45" width="55" height="55" rx="6" fill="#0f172a" stroke="#475569" stroke-width="1.5" stroke-dasharray="4"/>
            <text x="372" y="77" fill="#64748b" font-family="monospace" font-size="13" text-anchor="middle">Empty</text>
            <!-- Pointer Arrows -->
            <path d="M 47 130 L 47 110" stroke="#10b981" stroke-width="2"/>
            <polygon points="47,105 42,112 52,112" fill="#10b981"/>
            <text x="47" y="148" fill="#10b981" font-family="sans-serif" font-weight="bold" font-size="12" text-anchor="middle">TAIL (Dequeue)</text>
            <path d="M 307 20 L 307 38" stroke="#38bdf8" stroke-width="2"/>
            <polygon points="307,43 302,36 312,36" fill="#38bdf8"/>
            <text x="307" y="14" fill="#38bdf8" font-family="sans-serif" font-weight="bold" font-size="12" text-anchor="middle">HEAD (Enqueue Next)</text>
          </svg>
        </div>

        <h3>2. Modulo Arithmetic Index Wrapping</h3>
        <p>Instead of shifting elements on dequeue ($O(N)$), the queue simply advances its <code>front</code> and <code>rear</code> indices using modulo arithmetic: <code>(rear + 1) % capacity</code>, achieving constant $O(1)$ enqueue and dequeue.</p>
        """,
        "embedded_html": """
        <h3>1. Power-of-Two Bitmask Optimization</h3>
        <p>In high-frequency ISRs, the hardware division instruction (or software division routine on Cortex-M0) required for <code>% capacity</code> takes multiple clock cycles. Embedded engineers dimension ring buffers to powers of two (e.g. 64, 128, 256), replacing expensive modulo with a single-cycle bitwise AND: <code>(index + 1) &amp; (CAPACITY - 1)</code>!</p>

        <div class="callout callout-embedded">
          <h4>⚡ Hard Real-Time Advantage</h4>
          <p>Zero dynamic memory allocation, zero pointer chasing, and bounded memory consumption ensure predictable WCET (Worst-Case Execution Time).</p>
        </div>
        """,
        "refactor_html": """
        <pre class="code-block" style="background:#0d1117; padding:16px; border-radius:8px; border:1px solid #30363d;">#include &lt;array&gt;
#include &lt;cstdint&gt;

template &lt;typename T, size_t PowerOfTwoCap = 64&gt;
class FastRingBuffer {
    static_assert((PowerOfTwoCap &amp; (PowerOfTwoCap - 1)) == 0, "Capacity must be power of 2!");
public:
    bool enqueue(T val) {
        size_t nextHead = (head_ + 1) &amp; MASK;
        if (nextHead == tail_) return false; // Full
        buffer_[head_] = val;
        head_ = nextHead;
        return true;
    }
    bool dequeue(T&amp; out) {
        if (head_ == tail_) return false; // Empty
        out = buffer_[tail_];
        tail_ = (tail_ + 1) &amp; MASK;
        return true;
    }
private:
    static constexpr size_t MASK = PowerOfTwoCap - 1;
    std::array&lt;T, PowerOfTwoCap&gt; buffer_;
    size_t head_ = 0, tail_ = 0;
};</pre>
        """,
        "quiz": [
            {
                "question": "Why is the modulo operation `% capacity` often replaced with `& (capacity - 1)` in high-speed embedded ring buffers?",
                "options": [
                    "Bitwise AND executes in a single clock cycle, whereas integer division/modulo takes significantly more CPU cycles.",
                    "Bitwise AND automatically detects hardware parity errors.",
                    "Modulo cannot be compiled on ARM Cortex microcontrollers.",
                    "Bitwise AND converts numbers to floating point."
                ],
                "correct": 0,
                "explanation": "When capacity is a power of 2, <code>index & (capacity - 1)</code> produces identical results to <code>index % capacity</code> in a single fast clock cycle."
            },
            {
                "question": "What is the algorithmic time complexity of enqueue and dequeue in an ArrayQueue?",
                "options": ["O(1) constant time", "O(N) linear time", "O(log N)", "O(N^2)"],
                "correct": 0,
                "explanation": "Circular array queues achieve true $O(1)$ constant time for both enqueue and dequeue because no element shifting is performed."
            }
        ]
    },
    {
        "id": "array_list_app",
        "name": "ArrayListApp",
        "title": "ArrayList: Dynamic Array Resizing & Amortized Complexity",
        "headline": "Implementing Custom Dynamic Arrays, Resize Policies, and Bounded Alternatives",
        "emb_class": "emb-high",
        "emb_badge": "⚡ Embedded Relevance: High",
        "tags": ["ArrayList", "Dynamic Array", "Amortized O(1)", "Memory Relocation"],
        "summary": "Building a custom dynamic array list implementing an abstract List<T> interface. We analyze growth factors, amortized complexity, and contiguous memory access benefits.",
        "files": [
            "section_12/ArrayListApp/ArrayListApp/List.h",
            "section_12/ArrayListApp/ArrayListApp/ArrayList.h",
            "section_12/ArrayListApp/ArrayListApp/main.cpp"
        ],
        "concepts_html": "<h3>Dynamic Array Fundamentals</h3><p>Implements indexable random access ($O(1)$) with dynamic growth when capacity is reached.</p>",
        "embedded_html": "<h3>Heap Relocation Hazards</h3><p>Resizing an ArrayList requires allocating a new memory block and copying all data, causing latency spikes in real-time loops.</p>",
        "refactor_html": "<pre class=\"code-block\" style=\"background:#0d1117; padding:16px; border-radius:8px;\">// Bounded ArrayList with zero dynamic allocation\ntemplate &lt;typename T, size_t MaxSize&gt;\nclass BoundedList {\n    std::array&lt;T, MaxSize&gt; data_; size_t size_ = 0;\n};</pre>",
        "quiz": [
            {
                "question": "What is the random access lookup complexity of an ArrayList?",
                "options": ["O(1) constant time", "O(N)", "O(log N)", "O(N^2)"],
                "correct": 0,
                "explanation": "Contiguous array storage enables direct address computation in $O(1)$ time."
            }
        ]
    },
    {
        "id": "array_stack_app",
        "name": "ArrayStackApp",
        "title": "ArrayStack: Bounded LIFO Structures",
        "headline": "Implementing Array-Based Stacks for Deterministic Execution",
        "emb_class": "emb-high",
        "emb_badge": "⚡ Embedded Relevance: High",
        "tags": ["ArrayStack", "LIFO", "Bounded Memory", "Deterministic"],
        "summary": "Implementing a bounded array stack. We explore top index manipulation, push/pop mechanics, and deterministic execution.",
        "files": [
            "section_12/ArrayStackApp/ArrayStackApp/Stack.h",
            "section_12/ArrayStackApp/ArrayStackApp/ArrayStack.h",
            "section_12/ArrayStackApp/ArrayStackApp/main.cpp"
        ],
        "concepts_html": """
        <h3>Stack Operations</h3>
        <p>Push and pop operate on the top index in $O(1)$ time.</p>

        <div class="diagram-container">
          <h4>🥞 LIFO Stack Memory Layout (Push / Pop)</h4>
          <svg class="svg-diagram" width="460" height="190" viewBox="0 0 460 190" xmlns="http://www.w3.org/2000/svg">
            <rect x="130" y="130" width="200" height="34" rx="4" fill="#1e293b" stroke="#10b981" stroke-width="2"/>
            <text x="230" y="152" fill="#f0fdf4" font-family="monospace" font-size="13" text-anchor="middle">data[0] (Bottom)</text>
            <rect x="130" y="90" width="200" height="34" rx="4" fill="#1e293b" stroke="#10b981" stroke-width="2"/>
            <text x="230" y="112" fill="#f0fdf4" font-family="monospace" font-size="13" text-anchor="middle">data[1]</text>
            <rect x="130" y="50" width="200" height="34" rx="4" fill="#1e293b" stroke="#38bdf8" stroke-width="2"/>
            <text x="230" y="72" fill="#38bdf8" font-family="monospace" font-size="13" text-anchor="middle">data[top-1] (Top Element)</text>
            <rect x="130" y="10" width="200" height="34" rx="4" fill="#0f172a" stroke="#475569" stroke-width="1" stroke-dasharray="4"/>
            <text x="230" y="32" fill="#64748b" font-family="monospace" font-size="13" text-anchor="middle">Free Space (Capacity)</text>
            <path d="M 360 67 L 340 67" stroke="#00ff88" stroke-width="2"/>
            <polygon points="335,67 342,63 342,71" fill="#00ff88"/>
            <text x="400" y="71" fill="#00ff88" font-family="sans-serif" font-weight="bold" font-size="12" text-anchor="middle">top_ index</text>
          </svg>
        </div>
        """,
        "embedded_html": "<h3>Deterministic LIFO Buffering</h3><p>Array-backed stacks have bounded memory and execute in guaranteed single-cycle operations.</p>",
        "refactor_html": "<pre class=\"code-block\" style=\"background:#0d1117; padding:16px; border-radius:8px;\">template &lt;typename T, size_t Cap&gt;\nclass SafeArrayStack {\n    std::array&lt;T, Cap&gt; data_; size_t top_ = 0;\n};</pre>",
        "quiz": [
            {
                "question": "Why is an ArrayStack preferred over a LinkedStack in embedded systems?",
                "options": ["It uses contiguous memory, requires zero per-node heap allocations, and exhibits superior cache locality.", "It can store infinite items.", "It is non-deterministic.", "It disables interrupts."],
                "correct": 0,
                "explanation": "Array stacks avoid heap fragmentation and node pointer overhead while maximizing CPU cache performance."
            }
        ]
    },
    {
        "id": "linked_chain_fun",
        "name": "LinkedChainFun",
        "title": "Linked Node Chaining & Pointer Traversal",
        "headline": "Manual Node Linking, Memory Layout, and Pointer Overhead",
        "emb_class": "emb-med",
        "emb_badge": "⚡ Embedded Relevance: Medium",
        "tags": ["Node", "Pointers", "Memory Layout", "Heap"],
        "summary": "Exploring explicit node pointer linking and traversing heap-allocated structures.",
        "files": [
            "section_12/LinkedChainFun/LinkedChainFun/Node.h",
            "section_12/LinkedChainFun/LinkedChainFun/main.cpp"
        ],
        "concepts_html": """
        <h3>Node Anatomy & Pointer Chaining</h3>
        <p>Each node encapsulates a data payload and a pointer to the next node.</p>

        <div class="diagram-container">
          <h4>🔗 Singly Linked Node Pointer Chain</h4>
          <svg class="svg-diagram" width="520" height="110" viewBox="0 0 520 110" xmlns="http://www.w3.org/2000/svg">
            <rect x="20" y="25" width="75" height="45" rx="4" fill="#1e293b" stroke="#10b981" stroke-width="2"/>
            <text x="57" y="52" fill="#f0fdf4" font-family="monospace" font-size="12" text-anchor="middle">Data (4B)</text>
            <rect x="95" y="25" width="45" height="45" rx="4" fill="#0f172a" stroke="#38bdf8" stroke-width="2"/>
            <text x="117" y="52" fill="#38bdf8" font-family="monospace" font-size="11" text-anchor="middle">next*</text>
            <path d="M 140 47 L 195 47" stroke="#38bdf8" stroke-width="2"/>
            <polygon points="195,43 203,47 195,51" fill="#38bdf8"/>
            <rect x="205" y="25" width="75" height="45" rx="4" fill="#1e293b" stroke="#10b981" stroke-width="2"/>
            <text x="242" y="52" fill="#f0fdf4" font-family="monospace" font-size="12" text-anchor="middle">Data (4B)</text>
            <rect x="280" y="25" width="45" height="45" rx="4" fill="#0f172a" stroke="#38bdf8" stroke-width="2"/>
            <text x="302" y="52" fill="#38bdf8" font-family="monospace" font-size="11" text-anchor="middle">next*</text>
            <path d="M 325 47 L 380 47" stroke="#38bdf8" stroke-width="2"/>
            <polygon points="380,43 388,47 380,51" fill="#38bdf8"/>
            <rect x="390" y="25" width="75" height="45" rx="4" fill="#1e293b" stroke="#10b981" stroke-width="2"/>
            <text x="427" y="52" fill="#f0fdf4" font-family="monospace" font-size="12" text-anchor="middle">Data (4B)</text>
            <rect x="465" y="25" width="45" height="45" rx="4" fill="#0f172a" stroke="#f43f5e" stroke-width="2"/>
            <text x="487" y="52" fill="#f43f5e" font-family="monospace" font-size="10" text-anchor="middle">null</text>
          </svg>
        </div>
        """,
        "embedded_html": "<h3>Pointer Memory Tax</h3><p>On 64-bit systems, storing a 4-byte <code>int</code> with an 8-byte <code>next</code> pointer incurs 200% memory overhead plus allocator metadata.</p>",
        "refactor_html": "<pre class=\"code-block\" style=\"background:#0d1117; padding:16px; border-radius:8px;\">// Intrusive Node pattern to save memory\nstruct IntrusiveNode { IntrusiveNode* next = nullptr; };</pre>",
        "quiz": [
            {
                "question": "What is a major downside of singly linked chains on memory-constrained systems?",
                "options": ["Pointer overhead per node and heap fragmentation from individual node allocations.", "They cannot store characters.", "Traversal is O(1).", "They require an FPU."],
                "correct": 0,
                "explanation": "Every node incurs pointer storage overhead and separate heap allocation metadata."
            }
        ]
    },
    {
        "id": "linked_list_app",
        "name": "LinkedListApp",
        "title": "LinkedList: Dynamic Insertion vs Memory Fragmentation",
        "headline": "Implementing Singly Linked Lists & Evaluating Intrusive Alternatives",
        "emb_class": "emb-high",
        "emb_badge": "⚡ Embedded Relevance: High",
        "tags": ["LinkedList", "Dynamic Allocation", "Heap Fragmentation", "Intrusive List"],
        "summary": "Building a full linked list data structure implementing <code>List&lt;T&gt;</code>. We examine insertion/deletion at arbitrary positions, pointer manipulation, and intrusive list alternatives.",
        "files": [
            "section_12/LinkedListApp/LinkedListApp/List.h",
            "section_12/LinkedListApp/LinkedListApp/LinkedList.h",
            "section_12/LinkedListApp/LinkedListApp/main.cpp"
        ],
        "concepts_html": "<h3>List Traversal and Modification</h3><p>Inserting at the head is $O(1)$, while arbitrary index access requires $O(N)$ linear traversal.</p>",
        "embedded_html": "<h3>Intrusive Linked Lists (Embedded Gold Standard)</h3><p>In operating systems (FreeRTOS, Linux Kernel), nodes are embedded directly inside existing structures (intrusive lists), eliminating extra heap allocations entirely!</p>",
        "refactor_html": "<pre class=\"code-block\" style=\"background:#0d1117; padding:16px; border-radius:8px;\">struct TaskControlBlock {\n    TaskControlBlock* nextReadyTask;\n    uint32_t taskId;\n}; // Zero heap overhead intrusive node!</pre>",
        "quiz": [
            {
                "question": "Why do embedded kernels (like FreeRTOS) use intrusive linked lists instead of standard std::list?",
                "options": ["Intrusive lists embed links directly into objects, eliminating separate heap allocations for node wrappers.", "Standard lists do not work in C++.", "Intrusive lists are sorted automatically.", "They require more RAM."],
                "correct": 0,
                "explanation": "Intrusive lists avoid dynamic node wrapper allocation by placing pointer hooks inside the data structure itself."
            }
        ]
    },
    {
        "id": "linked_queue_project",
        "name": "LinkedQueueProject",
        "title": "LinkedQueue: Pointer-Based FIFO Queues",
        "headline": "Front & Rear Pointer Manipulation vs Cache Inefficiencies",
        "emb_class": "emb-med",
        "emb_badge": "⚡ Embedded Relevance: Medium",
        "tags": ["LinkedQueue", "FIFO", "Pointer Chasing"],
        "summary": "Implementing a node-based FIFO queue with front and rear pointers, contrasting its memory footprint with array ring buffers.",
        "files": [
            "section_12/LinkedQueueProject/LinkedQueueProject/Queue.h",
            "section_12/LinkedQueueProject/LinkedQueueProject/LinkedQueue.h",
            "section_12/LinkedQueueProject/LinkedQueueProject/main.cpp"
        ],
        "concepts_html": "<h3>Two-Pointer Queue Mechanics</h3><p>Maintains head and tail pointers for $O(1)$ push and pop.</p>",
        "embedded_html": "<h3>Heap Allocation Overhead</h3><p>Every enqueue calls <code>new Node</code>, creating dynamic allocation jitter in embedded environments.</p>",
        "refactor_html": "<pre class=\"code-block\" style=\"background:#0d1117; padding:16px; border-radius:8px;\">// Prefer ArrayQueue / RingBuffer for embedded queues</pre>",
        "quiz": [
            {
                "question": "What is the main drawback of LinkedQueue in interrupt handlers?",
                "options": ["Enqueuing requires dynamic memory allocation (new), which is unsafe in ISRs.", "It is too fast.", "It cannot store structures.", "It uses too few registers."],
                "correct": 0,
                "explanation": "Dynamic memory allocation inside an interrupt service routine is non-reentrant and causes system crashes."
            }
        ]
    },
    {
        "id": "linked_stack_app",
        "name": "LinkedStackApp",
        "title": "LinkedStack: Dynamic Node-Based LIFO",
        "headline": "Dynamic Node Allocation in Stack Implementations",
        "emb_class": "emb-med",
        "emb_badge": "⚡ Embedded Relevance: Medium",
        "tags": ["LinkedStack", "LIFO", "Dynamic Nodes"],
        "summary": "Implementing a node-based dynamic stack, analyzing push/pop pointer manipulation and cleanup.",
        "files": [
            "section_12/LinkedStackApp/LinkedStackApp/Stack.h",
            "section_12/LinkedStackApp/LinkedStackApp/LinkedStack.h",
            "section_12/LinkedStackApp/LinkedStackApp/main.cpp"
        ],
        "concepts_html": "<h3>Node Stack Mechanics</h3><p>Pushing creates a node and prepends it to the top pointer; popping frees the head node.</p>",
        "embedded_html": "<h3>Memory Comparison</h3><p>Array stacks use contiguous static memory and outperform linked stacks across all embedded metrics.</p>",
        "refactor_html": "<pre class=\"code-block\" style=\"background:#0d1117; padding:16px; border-radius:8px;\">// Static array stack is universally preferred in microcontrollers</pre>",
        "quiz": [
            {
                "question": "What operation is required on every pop() in a LinkedStack?",
                "options": ["Deallocating the popped node to prevent memory leaks.", "Rehashing the table.", "Disabling interrupts.", "Reallocating the array."],
                "correct": 0,
                "explanation": "Popping removes the head node, requiring explicit deallocation to avoid memory leakage."
            }
        ]
    },
    {
        "id": "list_stack_project",
        "name": "ListStackProject",
        "title": "ListStack: Container Adapter Pattern",
        "headline": "Composition vs Inheritance: Wrapping List Primitives in Stack Interfaces",
        "emb_class": "emb-high",
        "emb_badge": "⚡ Embedded Relevance: High",
        "tags": ["Adapter Pattern", "Composition", "ListStack", "Layering"],
        "summary": "Demonstrating the Adapter design pattern by implementing a <code>Stack</code> interface over an underlying <code>LinkedList</code>.",
        "files": [
            "section_12/ListStackProject/ListStackProject/List.h",
            "section_12/ListStackProject/ListStackProject/LinkedList.h",
            "section_12/ListStackProject/ListStackProject/Stack.h",
            "section_12/ListStackProject/ListStackProject/ListStack.h",
            "section_12/ListStackProject/ListStackProject/main.cpp"
        ],
        "concepts_html": "<h3>The Adapter Pattern</h3><p>Adapting an existing interface (<code>List</code>) to satisfy a target interface (<code>Stack</code>) using composition.</p>",
        "embedded_html": "<h3>Abstraction Cost</h3><p>Inlined adapter wrappers have zero runtime cost under compiler optimization (<code>-O2</code>).</p>",
        "refactor_html": "<pre class=\"code-block\" style=\"background:#0d1117; padding:16px; border-radius:8px;\">template &lt;typename Container&gt;\nclass StackAdapter {\n    Container c_;\npublic:\n    void push(typename Container::value_type v) { c_.push_back(v); }\n};</pre>",
        "quiz": [
            {
                "question": "What design pattern does ListStack implement?",
                "options": ["Adapter (Wrapper) Pattern", "Singleton Pattern", "Observer Pattern", "Visitor Pattern"],
                "correct": 0,
                "explanation": "ListStack adapts the general <code>List</code> interface into a restricted LIFO <code>Stack</code> interface."
            }
        ]
    },
    {
        "id": "templated_array_stack_app",
        "name": "TemplatedArrayStackApp",
        "title": "Templated ArrayStack: The Gold Standard Embedded Container",
        "headline": "Generic Bounded LIFO Structures with Zero Runtime Heap Allocation",
        "emb_class": "emb-high",
        "emb_badge": "⚡ Embedded Relevance: Critical",
        "tags": ["Templates", "ArrayStack", "Zero-Heap", "Type-Safe", "AUTOSAR Compliant"],
        "summary": "Implementing a generic templated array stack. We explore type-safe compile-time instantiations, bounded memory guarantees, and why templated bounded arrays represent the gold standard container in safety-critical embedded systems.",
        "files": [
            "section_12/TemplatedArrayStackApp/TemplatedArrayStackApp/Stack.h",
            "section_12/TemplatedArrayStackApp/TemplatedArrayStackApp/ArrayStack.h",
            "section_12/TemplatedArrayStackApp/TemplatedArrayStackApp/main.cpp"
        ],
        "concepts_html": """
        <h3>1. Generic Template Containers</h3>
        <p>Combining templates with static arrays provides type safety for arbitrary data payloads while avoiding <code>void*</code> casts.</p>
        """,
        "embedded_html": """
        <h3>1. Safety-Critical Compliance (AUTOSAR / MISRA)</h3>
        <p>Templated bounded array stacks allocate storage at compile time, guaranteeing zero dynamic memory operations after system initialization.</p>
        """,
        "refactor_html": """
        <pre class="code-block" style="background:#0d1117; padding:16px; border-radius:8px; border:1px solid #30363d;">#include &lt;array&gt;
#include &lt;optional&gt;

template &lt;typename T, size_t MaxCapacity&gt;
class EmbeddedStack {
public:
    bool push(const T&amp; item) {
        if (top_ &gt;= MaxCapacity) return false;
        data_[top_++] = item;
        return true;
    }
    std::optional&lt;T&gt; pop() {
        if (top_ == 0) return std::nullopt;
        return data_[--top_];
    }
private:
    std::array&lt;T, MaxCapacity&gt; data_;
    size_t top_ = 0;
};</pre>
        """,
        "quiz": [
            {
                "question": "Why is a templated bounded array stack considered the gold standard in AUTOSAR C++ embedded software?",
                "options": [
                    "It combines strong compile-time type safety with guaranteed fixed SRAM allocation and zero heap fragmentation.",
                    "It can grow infinitely.",
                    "It automatically creates threads.",
                    "It bypasses all memory checks."
                ],
                "correct": 0,
                "explanation": "It provides full generic type safety while bounding memory consumption strictly at compile time."
            }
        ]
    },
    {
        "id": "for_proj12_2_files",
        "name": "_for-proj12-2-files",
        "title": "Reference Solutions & Comparative Analysis",
        "headline": "Comparative Data Structure Evaluation for Real-Time Firmware",
        "emb_class": "emb-core",
        "emb_badge": "⚡ Embedded Relevance: Core",
        "tags": ["Reference Architecture", "Data Structures", "Comparative Analysis"],
        "summary": "Comparative architectural review of custom data structure implementations across performance, footprint, and deterministic timing metrics.",
        "files": [
            "section_12/_for-proj12-2-files/List.h",
            "section_12/_for-proj12-2-files/LinkedList.h",
            "section_12/_for-proj12-2-files/Stack.h",
            "section_12/_for-proj12-2-files/main.cpp"
        ],
        "concepts_html": "<h3>Architectural Synthesis</h3><p>Reviewing interface contracts and polymorphism across container implementations.</p>",
        "embedded_html": "<h3>Metric Synthesis</h3><p>Comparing contiguous array performance vs linked node overhead in microcontroller systems.</p>",
        "refactor_html": "<pre class=\"code-block\" style=\"background:#0d1117; padding:16px; border-radius:8px;\">// Architectural summary: Prefer contiguous static structures in microcontrollers</pre>",
        "quiz": [
            {
                "question": "In general, which container category is best suited for real-time microcontrollers?",
                "options": ["Contiguous bounded static containers (std::array, ring buffers, flat maps).", "Dynamic node-based containers (std::list, std::map).", "Deeply nested heap trees.", "Global void* pointers."],
                "correct": 0,
                "explanation": "Contiguous bounded containers provide deterministic execution, zero heap fragmentation, and maximum CPU cache efficiency."
            }
        ]
    }
]

# ==============================================================================
# MASTER LANDING PAGE BUILDER
# ==============================================================================
def build_index():
    all_projects = []

    # All Sections in Order
    sections_data = [
        ("1", SECTION_1_PROJECTS),
        ("2", SECTION_2_PROJECTS),
        ("3", SECTION_3_PROJECTS),
        ("4", SECTION_4_PROJECTS),
        ("5", SECTION_5_PROJECTS),
        ("6", SECTION_6_PROJECTS),
        ("7", SECTION_7_PROJECTS),
        ("8", SECTION_8_PROJECTS),
        ("9", SECTION_9_PROJECTS),
        ("10", SECTION_10_PROJECTS),
    ]

    for sec_num, proj_list in sections_data:
        for p in proj_list:
            rel = "high" if "Critical" in p['emb_badge'] or "High" in p['emb_badge'] else ("med" if "Medium" in p['emb_badge'] else "core")
            track = "foundations" if int(sec_num) <= 6 else "advanced"
            all_projects.append({
                "sec": sec_num,
                "track": track,
                "id": p['id'],
                "name": p['name'],
                "title": p['title'],
                "desc": sanitize_card_desc(p['summary']),
                "tags": p['tags'][:3],
                "rel": "high" if rel == "high" else "core",
                "rel_text": p['emb_badge'].replace("⚡ Embedded Relevance: ", ""),
                "rel_cls": p['emb_class'],
                "link": f"section_{sec_num}/{p['id']}.html"
            })

    # Section 11 Projects
    for p in SECTION_11_PROJECTS:
        rel = "high" if "Critical" in p['emb_badge'] or "High" in p['emb_badge'] else ("med" if "Medium" in p['emb_badge'] else "core")
        all_projects.append({
            "sec": "11",
            "track": "advanced",
            "id": p['id'],
            "name": p['name'],
            "title": p['title'],
            "desc": sanitize_card_desc(p['summary']),
            "tags": p['tags'][:3],
            "rel": "high" if rel == "high" else "core",
            "rel_text": p['emb_badge'].replace("⚡ Embedded Relevance: ", ""),
            "rel_cls": p['emb_class'],
            "link": f"section_11/{p['id']}.html"
        })

    # Section 12 Projects
    for p in SECTION_12_PROJECTS:
        rel = "high" if "Critical" in p['emb_badge'] or "High" in p['emb_badge'] else ("med" if "Medium" in p['emb_badge'] else "core")
        all_projects.append({
            "sec": "12",
            "track": "advanced",
            "id": p['id'],
            "name": p['name'],
            "title": p['title'],
            "desc": sanitize_card_desc(p['summary']),
            "tags": p['tags'][:3],
            "rel": "high" if rel == "high" else "core",
            "rel_text": p['emb_badge'].replace("⚡ Embedded Relevance: ", ""),
            "rel_cls": p['emb_class'],
            "link": f"section_12/{p['id']}.html"
        })

    foundations_cards = []
    advanced_cards = []

    for p in all_projects:
        tags_rendered = " ".join([f'<span class="tag">{t}</span>' for t in p['tags']])
        card_html = f'''
        <a href="{p['link']}" class="project-card" data-section="{p['sec']}" data-track="{p['track']}" data-relevance="{p['rel']}">
          <div class="card-top">
            <span class="section-pill section-{p['sec']}">Section {p['sec']}</span>
            <span class="embedded-badge {p['rel_cls']}">⚡ {p['rel_text']}</span>
          </div>
          <h3 class="card-title">{p['name']}</h3>
          <p class="card-desc">{p['desc']}</p>
          <div class="card-tags">
            {tags_rendered}
          </div>
        </a>'''
        if p['track'] == "foundations":
            foundations_cards.append(card_html)
        else:
            advanced_cards.append(card_html)

    foundations_grid_rendered = "\n".join(foundations_cards)
    advanced_grid_rendered = "\n".join(advanced_cards)

    index_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Embedded Modern C++: From Bare-Metal to STL</title>
  <link rel="stylesheet" href="assets/style.css">
</head>
<body>
  <header class="site-header">
    <div class="container nav-bar">
      <a href="index.html" class="nav-brand">
        ⚡ Embedded Modern C++
        <span class="badge-tag">Complete Curriculum (116 Projects)</span>
      </a>
      <ul class="nav-links">
        <li><a href="index.html" class="active">🏠 Home</a></li>
        <li><a href="glossary.html">📖 Glossary</a></li>
        <li><a href="section_1/hello.html">Sec 1</a></li>
        <li><a href="section_2/hello_world.html">Sec 2</a></li>
        <li><a href="section_3/control_statements_intro.html">Sec 3</a></li>
        <li><a href="section_4/array_fun.html">Sec 4</a></li>
        <li><a href="section_5/function_fun_1.html">Sec 5</a></li>
        <li><a href="section_6/book_fun.html">Sec 6</a></li>
        <li><a href="section_7/bug_fun.html">Sec 7</a></li>
        <li><a href="section_8/pointer_fun.html">Sec 8</a></li>
        <li><a href="section_9/file_input_fun.html">Sec 9</a></li>
        <li><a href="section_10/enum_fun.html">Sec 10</a></li>
        <li><a href="section_11/smart_pointer_fun.html">Sec 11</a></li>
        <li><a href="section_12/array_queue_app.html">Sec 12</a></li>
        <li>
          <button id="themeToggle" class="theme-toggle-btn" aria-label="Toggle theme" title="Toggle Light/Dark Theme">
            <span class="theme-icon">☀️</span>
            <span class="theme-text">Light</span>
          </button>
        </li>
        <li><a href="https://github.com/mohamed-soubhi/Embedded-Modern-Cpp-From-Bare-Metal-to-STL" target="_blank" rel="noopener noreferrer" class="nav-github-link">📦 GitHub</a></li>
      </ul>
    </div>
  </header>

  <main class="container">
    <section class="hero">
      <h1>Embedded Modern C++: From Bare-Metal to STL</h1>
      <p>Comprehensive, deep-dive architectural analysis of all 116 course projects across Sections 1 through 12. Complete with fully annotated source code, ARM Cortex-M hardware realities, zero-overhead refactors, and interactive self-checking quizzes.</p>
      
      <!-- Upstream Curriculum & Repository Attribution Card -->
      <div class="reference-banner">
        <div class="reference-badge">🎓 Upstream Curriculum &amp; Repository Attribution</div>
        <p class="reference-text">
          Built upon the curriculum and project code of <strong>The Complete C++ Developer Course</strong> by Packt Publishing (Dr. John P. Baugh). 
          This portal serves as an advanced companion resource—expanding foundational C++ code into production-grade embedded systems architectures, deterministic real-time patterns, ARM Cortex-M hardware analyses, and interactive quizzes.
        </p>
        <div class="reference-links">
          <a href="glossary.html" class="btn-ref" style="background: rgba(16, 185, 129, 0.15); border-color: var(--accent-primary); color: var(--accent-neon);">
            <span>📖</span> Technical Glossary (68+ Terms)
          </a>
          <a href="https://github.com/mohamed-soubhi/Embedded-Modern-Cpp-From-Bare-Metal-to-STL" target="_blank" rel="noopener noreferrer" class="btn-ref">
            <span>📂</span> GitHub Repository
          </a>
          <a href="https://github.com/mohamed-soubhi/Embedded-Modern-Cpp-From-Bare-Metal-to-STL/blob/main/README.md" target="_blank" rel="noopener noreferrer" class="btn-ref">
            <span>📖</span> Course Syllabus &amp; Setup Guide
          </a>
          <span class="ref-pill">⚡ ARM Cortex-M &amp; MISRA C++ Focus</span>
        </div>
      </div>
    </section>

    <!-- Category Tracks Navigation Switcher -->
    <div class="track-switcher">
      <button class="track-btn active" data-track="all">
        <span>🌟 All Curriculum</span>
        <span class="track-badge">116 Projects</span>
      </button>
      <button class="track-btn" data-track="foundations">
        <span>📘 Foundations Track (Sec 1–6)</span>
        <span class="track-badge">61 Projects</span>
      </button>
      <button class="track-btn" data-track="advanced">
        <span>🚀 Advanced Systems Track (Sec 7–12)</span>
        <span class="track-badge">55 Projects</span>
      </button>
      <button class="track-btn" data-track="emb-high">
        <span>⚡ High / Critical Relevance</span>
        <span class="track-badge">50+ Projects</span>
      </button>
    </div>

    <!-- Search and Filters Panel -->
    <section class="filter-panel">
      <div class="search-box">
        <span class="search-icon">🔍</span>
        <input type="text" id="projectSearch" class="search-input" placeholder="Search 116 projects by concept (e.g. AAPCS, vtable, MMIO, DMA, LittleFS, heap, alignas), name, or tag...">
      </div>
      <div class="filter-chips">
        <span class="filter-label">Filter by Section:</span>
        <button class="chip active" data-filter="all">All Sections (116)</button>
        <button class="chip" data-filter="sec-1">Sec 1: Toolchains (2)</button>
        <button class="chip" data-filter="sec-2">Sec 2: Types &amp; Vars (14)</button>
        <button class="chip" data-filter="sec-3">Sec 3: Control Flow (13)</button>
        <button class="chip" data-filter="sec-4">Sec 4: Arrays &amp; Locality (11)</button>
        <button class="chip" data-filter="sec-5">Sec 5: Functions &amp; AAPCS (15)</button>
        <button class="chip" data-filter="sec-6">Sec 6: OOP Foundations (6)</button>
        <button class="chip" data-filter="sec-7">Sec 7: Exceptions &amp; Faults (9)</button>
        <button class="chip" data-filter="sec-8">Sec 8: Pointers &amp; Memory (7)</button>
        <button class="chip" data-filter="sec-9">Sec 9: Streams &amp; Flash FS (7)</button>
        <button class="chip" data-filter="sec-10">Sec 10: OOP &amp; Enums (3)</button>
        <button class="chip" data-filter="sec-11">Sec 11: Templates &amp; STL (19)</button>
        <button class="chip" data-filter="sec-12">Sec 12: Data Structures (10)</button>
      </div>
    </section>

    <!-- Dynamic Live Result Counter -->
    <div class="results-counter" id="resultsCounter">
      Showing <strong>116</strong> of <strong>116</strong> Projects
    </div>

    <!-- Track 1: Foundations & Core Language Architecture (Sections 1-6) -->
    <div class="track-header" id="header-foundations" data-track-header="foundations">
      <div class="track-title-wrap">
        <span class="track-icon">📘</span>
        <div>
          <h2>Track 1: Foundations &amp; Core Language Architecture</h2>
          <p>Sections 1 through 6 &bull; Cross-Compilers, Data Types, Control Flow, Memory Locality, Calling Conventions &amp; OOP Foundations</p>
        </div>
      </div>
      <span class="track-count-badge">61 Projects</span>
    </div>

    <section class="cards-grid" id="grid-foundations">
      {foundations_grid_rendered}
    </section>

    <!-- Track 2: Advanced Systems, Real-Time Hardware & Memory (Sections 7-12) -->
    <div class="track-header advanced-header" id="header-advanced" data-track-header="advanced">
      <div class="track-title-wrap">
        <span class="track-icon">🚀</span>
        <div>
          <h2>Track 2: Advanced Systems, Real-Time Hardware &amp; Memory</h2>
          <p>Sections 7 through 12 &bull; Fault Handlers, Memory-Mapped I/O, Flash File Systems, Polymorphism &amp; CRTP, Modern STL &amp; Data Structures</p>
        </div>
      </div>
      <span class="track-count-badge">55 Projects</span>
    </div>

    <section class="cards-grid" id="grid-advanced">
      {advanced_grid_rendered}
    </section>
  </main>

  <footer class="site-footer">
    <div class="container footer-content">
      <div class="footer-brand">
        <h4>⚡ Embedded Modern C++: From Bare-Metal to STL</h4>
        <p>An interactive companion for mastering Modern C++ (C++11/14/17/20), zero-overhead abstractions, and bare-metal microcontroller firmware design.</p>
      </div>
      <div class="footer-links-group">
        <div class="footer-col">
          <h5>Course Curriculum (Foundations)</h5>
          <ul>
            <li><a href="section_1/hello.html">Section 1: Toolchains &amp; Linkers</a></li>
            <li><a href="section_2/hello_world.html">Section 2: Types &amp; Variables</a></li>
            <li><a href="section_3/control_statements_intro.html">Section 3: Control Flow</a></li>
            <li><a href="section_4/array_fun.html">Section 4: Arrays &amp; Locality</a></li>
            <li><a href="section_5/function_fun_1.html">Section 5: Functions &amp; Scope</a></li>
            <li><a href="section_6/book_fun.html">Section 6: OOP Foundations</a></li>
          </ul>
        </div>
        <div class="footer-col">
          <h5>Course Curriculum (Advanced)</h5>
          <ul>
            <li><a href="section_7/bug_fun.html">Section 7: Exceptions &amp; Faults</a></li>
            <li><a href="section_8/pointer_fun.html">Section 8: Pointers &amp; Memory</a></li>
            <li><a href="section_9/file_input_fun.html">Section 9: Streams &amp; Flash FS</a></li>
            <li><a href="section_10/enum_fun.html">Section 10: OOP &amp; Enums</a></li>
            <li><a href="section_11/smart_pointer_fun.html">Section 11: Templates &amp; STL</a></li>
            <li><a href="section_12/array_queue_app.html">Section 12: Data Structures</a></li>
          </ul>
        </div>
        <div class="footer-col">
          <h5>Attribution &amp; Source</h5>
          <ul>
            <li><a href="glossary.html">📖 Technical Glossary &amp; Reference</a></li>
            <li><a href="https://github.com/mohamed-soubhi/Embedded-Modern-Cpp-From-Bare-Metal-to-STL" target="_blank" rel="noopener noreferrer">GitHub Repository</a></li>
            <li><a href="https://github.com/mohamed-soubhi/Embedded-Modern-Cpp-From-Bare-Metal-to-STL/blob/main/README.md" target="_blank" rel="noopener noreferrer">Course Syllabus &amp; Setup</a></li>
            <li><span>Author: Mohamed Soubhi</span></li>
          </ul>
        </div>
      </div>
    </div>
    <div class="footer-bottom">
      <p>Original Course &copy; Packt Publishing / Dr. John P. Baugh. Extended Architectural Analysis &amp; Interactive Study Portal by Mohamed Soubhi.</p>
    </div>
  </footer>

  <script src="assets/app.js"></script>
</body>
</html>'''

    with open(os.path.join(PORTAL_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(index_content)
    print("✓ Master index.html created successfully!")

# ==============================================================================
# MAIN GENERATION RUNNER
# ==============================================================================
def main():
    sections_to_build = [
        (1, SECTION_1_PROJECTS),
        (2, SECTION_2_PROJECTS),
        (3, SECTION_3_PROJECTS),
        (4, SECTION_4_PROJECTS),
        (5, SECTION_5_PROJECTS),
        (6, SECTION_6_PROJECTS),
        (7, SECTION_7_PROJECTS),
        (8, SECTION_8_PROJECTS),
        (9, SECTION_9_PROJECTS),
        (10, SECTION_10_PROJECTS),
        (11, SECTION_11_PROJECTS),
        (12, SECTION_12_PROJECTS),
    ]

    for sec_num, proj_list in sections_to_build:
        print(f"Generating Section {sec_num} HTML pages...")
        for idx, p in enumerate(proj_list):
            if 'uml_diagram' not in p and p['id'] in UML_DEFINITIONS:
                p['uml_diagram'] = UML_DEFINITIONS[p['id']]
            
            prev_p = proj_list[idx - 1] if idx > 0 else proj_list[-1]
            next_p = proj_list[idx + 1] if idx < len(proj_list) - 1 else proj_list[0]
            
            prev_link = f"{prev_p['id']}.html"
            next_link = f"{next_p['id']}.html"
            
            html_out = generate_page(p, prev_link, next_link, section_num=sec_num)
            out_path = os.path.join(PORTAL_DIR, f"section_{sec_num}", f"{p['id']}.html")
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(html_out)
            print(f"  ✓ [{idx+1}/{len(proj_list)}] section_{sec_num}/{p['id']}.html")

    print("Building Technical Glossary Page...")
    generate_glossary_page()

    print("Building Master Index Landing Page...")
    build_index()
    print("All 116 portal pages & Technical Glossary generated successfully!")

if __name__ == "__main__":
    main()
