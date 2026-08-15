#!/usr/bin/env python3
"""
Section 9 Project Definitions: Streams, Flash File Systems & Data Serialization
Contains 7 comprehensive project definitions covering std::ifstream / std::ofstream,
LittleFS & FATFS on SPI NOR/NAND Flash, wear leveling, struct binary serialization, and CRC32 integrity.
"""

SECTION_9_PROJECTS = [
    {
        "id": "file_input_fun",
        "name": "FileInputFun",
        "title": "File Input Streams, LittleFS & SPI Flash Memory",
        "headline": "std::ifstream Mechanics vs LittleFS / FatFS on SPI NOR Flash Microcontrollers",
        "emb_class": "emb-high",
        "emb_badge": "⚡ Embedded Relevance: Critical",
        "tags": ["std::ifstream", "LittleFS", "FatFS", "SPI Flash", "NOR Flash"],
        "summary": "Exploring file reading via std::ifstream. We analyze file stream opening, buffer extraction, EOF detection, and contrast hosted POSIX file systems with embedded Flash file systems (LittleFS / FatFS) running on Quad-SPI NOR Flash memory chips with dynamic wear leveling.",
        "files": [
            "section_9/FileInputFun/FileInputFun/main.cpp",
            "section_9/FileInputFun/FileInputFun/input.txt"
        ],
        "concepts_html": """
        <h3>1. <code>std::ifstream</code> Stream Mechanics</h3>
        <p><code>std::ifstream</code> manages file stream handles, buffering file blocks from storage and converting text tokens to target data types using formatted extraction (<code>&gt;&gt;</code>).</p>

        <h3>2. Stream Lifecycle (RAII)</h3>
        <p>When an <code>ifstream</code> object exits scope, its destructor automatically flushes buffers and closes the underlying OS file descriptor (RAII).</p>
        """,
        "embedded_html": """
        <h3>1. LittleFS on External SPI NOR Flash</h3>
        <p>In microcontrollers lacking POSIX operating systems, <strong>LittleFS</strong> provides a power-resilient, fail-safe file system designed specifically for microcontrollers. It features <strong>dynamic wear leveling</strong> (preventing Flash sector burnout) and power-cut resilience.</p>
        """,
        "refactor_html": """
        <p>Embedded LittleFS file read operation:</p>
        <pre class="code-block" style="background:#0d1117; padding:16px; border-radius:8px; border:1px solid #30363d;">#include &lt;cstdint&gt;
#include &lt;array&gt;

// Conceptually equivalent to lfs_file_read
struct EmbeddedConfig {
    uint32_t baud_rate{115200};
    uint16_t sensor_interval_ms{1000};
    uint8_t  device_id{1};
};

bool readConfigFile(EmbeddedConfig&amp; out_cfg) noexcept {
    // Read raw binary struct directly from LittleFS SPI Flash block...
    return true;
}</pre>
        """,
        "quiz": [
            {
                "question": "What is 'LittleFS' in the embedded microcontroller ecosystem?",
                "options": ["A lightweight, power-fail-resilient file system designed for microcontrollers with bounded RAM and dynamic wear leveling for SPI Flash memory", "A cloud storage driver for AWS", "A file system only for Windows 11", "A tool that compiles C++ code on SD cards"],
                "correct": 0,
                "explanation": "LittleFS is an open-source embedded file system engineered specifically for NOR/NAND flash on microcontrollers, featuring wear leveling and power-cut safety."
            },
            {
                "question": "Why can raw NOR Flash memory NOT be overwritten without performing a sector erase first?",
                "options": ["Flash memory bits can be programmed from 1 to 0 individually, but can only be reset from 0 back to 1 in entire sectors (e.g. 4KB blocks)", "Flash chips require 120V AC voltage to write", "Flash memory is permanently read-only", "Writing requires an internet connection"],
                "correct": 0,
                "explanation": "NOR flash physics allows clearing bits from 1 to 0 on a byte level, but flipping 0s back to 1s requires an electrical block erase cycle (typically 4KB sectors)."
            },
            {
                "question": "What is 'Flash Wear Leveling'?",
                "options": ["An algorithm that distributes erase/write cycles evenly across all physical Flash sectors to prevent premature silicon cell failure (typical 100k cycle limit)", "A tool that measures chip temperature", "A mechanical polishing process for silicon chips", "A technique to increase RAM clock speeds"],
                "correct": 0,
                "explanation": "Flash sectors degrade after ~10,000–100,000 erase cycles. Wear leveling remaps logical sectors across physical blocks to maximize chip longevity."
            },
            {
                "question": "What check must be performed immediately after attempting to open a file with std::ifstream?",
                "options": ["Verify stream validity via 'if (!file.is_open())' to handle missing or inaccessible files safely", "Check if the CPU is running at 100MHz", "Reboot the microcontroller", "Call cin.clear()"],
                "correct": 0,
                "explanation": "Always verify <code>file.is_open()</code> or <code>if (!file)</code> before reading to prevent undefined behavior when accessing nonexistent files."
            }
        ]
    },
    {
        "id": "file_output_fun",
        "name": "FileOutputFun",
        "title": "File Output Streams, Buffering & Flush Mechanics",
        "headline": "std::ofstream Buffering, Power-Loss Corruption & Atomic Flash Commits",
        "emb_class": "emb-high",
        "emb_badge": "⚡ Embedded Relevance: High",
        "tags": ["std::ofstream", "Buffering", "Power Loss", "Atomic Writes", "Data Logging"],
        "summary": "Exploring file writing via std::ofstream. We analyze write buffering, explicit stream flushing, the severe hazard of power loss during file writes causing metadata corruption, and implementing atomic write transactions on embedded telemetry loggers.",
        "files": [
            "section_9/FileOutputFun/FileOutputFun/main.cpp",
            "section_9/FileOutputFun/FileOutputFun/output.txt"
        ],
        "concepts_html": """
        <h3>1. <code>std::ofstream</code> Write Buffering</h3>
        <p>Output streams buffer writes in memory before committing chunks to disk. Writing with <code>&lt;&lt;</code> writes to the stream buffer; data reaches disk only when the buffer fills, <code>flush()</code> is called, or the file is closed.</p>
        """,
        "embedded_html": """
        <h3>1. Power-Loss File System Corruption</h3>
        <p>If battery power fails while writing a file, uncommitted RAM buffers are lost and partially written FAT/directory tables will <strong>corrupt the entire file system</strong>. Embedded systems use <strong>journaling or copy-on-write atomic transactions</strong>.</p>
        """,
        "refactor_html": """
        <p>Power-fail safe atomic log writer:</p>
        <pre class="code-block" style="background:#0d1117; padding:16px; border-radius:8px; border:1px solid #30363d;">#include &lt;cstdint&gt;

struct TelemetryLogEntry {
    uint32_t timestamp_s;
    int16_t  temperature_c;
    uint16_t voltage_mv;
    uint32_t crc32;
};

// Write with explicit hardware flush to guarantee persistence
bool appendLogRecord(const TelemetryLogEntry&amp; entry) noexcept {
    // 1. Write binary entry to Flash buffer...
    // 2. Force hardware SPI Flash write transaction...
    // 3. Update non-volatile commit pointer in Flash header...
    return true;
}</pre>
        """,
        "quiz": [
            {
                "question": "What happens if a battery is disconnected while an embedded data logger is writing to a standard FATFS SD card?",
                "options": ["Unflushed cache buffers are lost and file allocation tables may be left in an inconsistent state, corrupting the SD card file system", "The SD card converts to an encrypted partition", "The data is automatically recovered from ROM", "The microcontroller clock frequency is reduced"],
                "correct": 0,
                "explanation": "Power interruption during FAT table updates corrupts directory chains, rendering files unreadable without specialized recovery tools."
            },
            {
                "question": "What does calling 'out_file.flush()' or 'out_file << std::flush' do?",
                "options": ["Forces all buffered output data in memory to be physically committed to the underlying storage device immediately", "Clears all text from the file", "Deletes the file from disk", "Closes the file permanently"],
                "correct": 0,
                "explanation": "<code>flush()</code> pushes all pending characters from RAM stream buffers into physical storage without closing the file handle."
            },
            {
                "question": "Which open mode flag appends new data to the end of an existing file rather than overwriting it?",
                "options": ["std::ios::app", "std::ios::trunc", "std::ios::in", "std::ios::binary"],
                "correct": 0,
                "explanation": "<code>std::ios::app</code> (append mode) positions write operations at the end of the file, preserving existing content."
            },
            {
                "question": "Why is binary file serialization (writing raw structs) faster and more compact than text serialization (ASCII numbers) in IoT loggers?",
                "options": ["Binary format writes raw bytes directly without CPU-intensive ASCII formatting, consuming 40-70% less Flash storage and write energy", "Binary files cannot be corrupted by power loss", "Text files can only hold 256 bytes", "Binary files run in RAM only"],
                "correct": 0,
                "explanation": "Binary serialization stores numbers in their native byte layout (e.g. 4 bytes for float), avoiding expensive integer-to-string formatting."
            }
        ]
    },
    {
        "id": "twice_file",
        "name": "TwiceFile",
        "title": "Stream Transformation, Data Pipelines & Circular EEPROM Rings",
        "headline": "Input-to-Output Stream Transformations & Circular Ring Logging in EEPROM",
        "emb_class": "emb-core",
        "emb_badge": "⚡ Embedded Relevance: Core",
        "tags": ["Streams", "Data Pipeline", "EEPROM", "Circular Logging", "Transformation"],
        "summary": "Building read-transform-write file pipelines. We analyze streaming mathematical transformation of files and compare file-based streams with circular logging queues stored in non-volatile I2C/SPI EEPROM memory.",
        "files": [
            "section_9/TwiceFile/TwiceFile/main.cpp",
            "section_9/TwiceFile/TwiceFile/input.txt",
            "section_9/TwiceFile/TwiceFile/output.txt"
        ],
        "concepts_html": """
        <h3>1. Streaming Data Pipelines</h3>
        <p>Reading elements sequentially from an input stream, applying a transformation function, and writing directly to an output stream in $O(1)$ memory space.</p>
        """,
        "embedded_html": """
        <h3>1. Non-Volatile EEPROM Circular Buffers</h3>
        <p>In industrial sensors, small <strong>I2C EEPROMs (e.g. 24LC256 - 32KB)</strong> store error event logs. Because EEPROM allows byte-level writes with 1,000,000+ erase endurance, circular ring structures log telemetry indefinitely.</p>
        """,
        "refactor_html": """
        <p>Streaming data transformer:</p>
        <pre class="code-block" style="background:#0d1117; padding:16px; border-radius:8px; border:1px solid #30363d;">#include &lt;cstdint&gt;
#include &lt;cstddef&gt;

// In-place streaming sensor sample scaler
void scaleSensorStream(const int16_t* in_samples, int16_t* out_samples, size_t count, int16_t multiplier) noexcept {
    for (size_t i = 0; i &lt; count; ++i) {
        out_samples[i] = in_samples[i] * multiplier;
    }
}</pre>
        """,
        "quiz": [
            {
                "question": "How does I2C/SPI EEPROM differ from NOR Flash memory in embedded hardware?",
                "options": ["EEPROM allows true byte-level overwriting without requiring full sector erases, and provides higher endurance (1,000,000+ cycles)", "EEPROM is read-only", "EEPROM requires 64-bit microcontrollers", "Flash memory is faster for single byte writes"],
                "correct": 0,
                "explanation": "EEPROM allows erasing and writing individual bytes independently, making it ideal for parameter storage and high-frequency event logging."
            },
            {
                "question": "What is the memory complexity of a streaming data transformation pipeline that processes items one at a time?",
                "options": ["O(1) constant auxiliary RAM space", "O(N) memory space", "O(N^2) memory space", "O(log N) memory space"],
                "correct": 0,
                "explanation": "Processing items one by one in a stream pipeline requires only a single element buffer, operating in $O(1)$ RAM."
            },
            {
                "question": "What happens if a stream extraction 'in_file >> val' reaches End-Of-File (EOF)?",
                "options": ["The stream sets its eofbit flag and the extraction expression evaluates to false in a boolean context", "The CPU reboots", "A HardFault is generated", "The file is deleted"],
                "correct": 0,
                "explanation": "Upon reaching EOF, <code>eofbit</code> is set, causing <code>while (in_file &gt;&gt; val)</code> loops to terminate cleanly."
            },
            {
                "question": "Why is closing file streams explicitly (or via RAII scope exit) critical before reading the destination file?",
                "options": ["To ensure all pending data buffered in memory is flushed and written to disk before the subsequent reader accesses it", "To reduce RAM clock speed", "To encrypt the file", "To prevent compiler syntax errors"],
                "correct": 0,
                "explanation": "Closing a file flushes all remaining cached buffer data to physical media, ensuring readers see complete files."
            }
        ]
    },
    {
        "id": "names_ages",
        "name": "NamesAges",
        "title": "Parallel File Streams, Synchronization & Correlation Records",
        "headline": "Parallel File Stream Synchronization, Record Alignment & Relational Records in Flash",
        "emb_class": "emb-core",
        "emb_badge": "⚡ Embedded Relevance: Core",
        "tags": ["Parallel Streams", "Record Synchronization", "Relational Data", "Validation"],
        "summary": "Synchronizing parallel file streams (names.txt and ages.txt). We analyze stream synchronization, detecting mismatched record lengths, and unifying multi-file tabular data into coherent C++ aggregate structures.",
        "files": [
            "section_9/NamesAges/NamesAges/main.cpp",
            "section_9/NamesAges/NamesAges/names.txt",
            "section_9/NamesAges/NamesAges/ages.txt",
            "section_9/NamesAges/NamesAges/output.txt"
        ],
        "concepts_html": """
        <h3>1. Parallel Stream Synchronization</h3>
        <p>Reading from multiple files simultaneously and correlating line $N$ of file 1 with line $N$ of file 2. If one file has fewer entries, stream state checks must handle record mismatch.</p>
        """,
        "embedded_html": """
        <h3>1. Multi-Channel Sensor Log Synchronization</h3>
        <p>In aerospace telemetry loggers (e.g. flight data recorders), separate streams (IMU accelerometers, GPS coordinates, Pitot tube airspeed) are synchronized by matching timestamps into unified frame packets.</p>
        """,
        "refactor_html": """
        <p>Unified synchronized telemetry record:</p>
        <pre class="code-block" style="background:#0d1117; padding:16px; border-radius:8px; border:1px solid #30363d;">#include &lt;cstdint&gt;

struct SynchronizedFlightFrame {
    uint32_t timestamp_ms;
    int16_t  accel_z_mg;
    int32_t  gps_latitude_scaled;
    uint16_t airspeed_knots;
};</pre>
        """,
        "quiz": [
            {
                "question": "What is the primary risk of storing relational data across two separate parallel files (e.g. names.txt and ages.txt)?",
                "options": ["Desynchronization: if one file is modified, corrupted, or has missing lines, all subsequent paired records become misaligned and invalid", "Files cannot be opened simultaneously in C++", "It doubles CPU voltage", "It requires dynamic heap allocation"],
                "correct": 0,
                "explanation": "Parallel separate files lack referential integrity; a single missing line offsets all subsequent paired records."
            },
            {
                "question": "How should structured multi-field records be stored in embedded systems to avoid desynchronization?",
                "options": ["Encapsulated into a single unified struct or JSON/binary record written to a single unified log stream", "Stored across 10 separate text files", "Stored in CPU registers only", "Transmitted over I2C without storage"],
                "correct": 0,
                "explanation": "Consolidating related fields into a single struct guarantees atomicity and alignment for every record."
            },
            {
                "question": "In the loop 'while (file1 >> name && file2 >> age)', when does the loop terminate?",
                "options": ["As soon as EITHER file reaches End-Of-File or encounters an extraction error", "Only when both files reach EOF simultaneously", "After exactly 10 iterations", "When the CPU resets"],
                "correct": 0,
                "explanation": "Logical AND (<code>&amp;&amp;</code>) stops looping as soon as either stream read fails or encounters EOF."
            },
            {
                "question": "What check verifies that both parallel files contained the exact same number of lines after loop termination?",
                "options": ["Check that both 'file1.eof()' and 'file2.eof()' are true", "Check if sizeof(file1) == sizeof(file2)", "Check the file names", "Check the compile date"],
                "correct": 0,
                "explanation": "Verifying that both files reached EOF simultaneously confirms that neither file contained trailing unmatched records."
            }
        ]
    },
    {
        "id": "movie_genres",
        "name": "MovieGenres",
        "title": "Data Aggregation, Frequency Histograms & Category Grouping",
        "headline": "Stream Categorization, Frequency Tables & Static Fixed-Capacity Bins in RAM",
        "emb_class": "emb-core",
        "emb_badge": "⚡ Embedded Relevance: Core",
        "tags": ["Histograms", "Categorization", "Frequency Table", "Static Bins", "Data Analysis"],
        "summary": "Analyzing category frequency distributions and histograms from file streams. We explore fixed-size category binning, counting algorithm complexity, and replacing dynamic associative maps with static fixed-array frequency tables in embedded telemetry analyzers.",
        "files": [
            "section_9/MovieGenres/MovieGenres/main.cpp",
            "section_9/MovieGenres/MovieGenres/genres.txt"
        ],
        "concepts_html": """
        <h3>1. Frequency Binning & Histograms</h3>
        <p>Counting occurrences of categorical items across a dataset to compute statistical distributions.</p>
        """,
        "embedded_html": """
        <h3>1. Hardware Event Diagnostic Bins</h3>
        <p>In automotive ECUs, Diagnostic Trouble Codes (DTCs) and CAN bus message counters use static integer histogram bins in battery-backed SRAM to log fault occurrences across vehicle operational lifetimes.</p>
        """,
        "refactor_html": """
        <p>Fixed-array event diagnostic histogram:</p>
        <pre class="code-block" style="background:#0d1117; padding:16px; border-radius:8px; border:1px solid #30363d;">#include &lt;cstdint&gt;
#include &lt;array&gt;

enum class FaultCategory : uint8_t {
    OverVoltage = 0,
    UnderVoltage,
    OverTemperature,
    CanBusTimeout,
    SensorMismatch,
    Count // 5 categories
};

class DiagnosticHistogram {
private:
    std::array&lt;uint32_t, static_cast&lt;size_t&gt;(FaultCategory::Count)&gt; counts_{};

public:
    void record_fault(FaultCategory fault) noexcept {
        size_t idx = static_cast&lt;size_t&gt;(fault);
        if (idx &lt; counts_.size()) {
            ++counts_[idx]; // O(1) single-instruction increment!
        }
    }

    uint32_t get_count(FaultCategory fault) const noexcept {
        return counts_[static_cast&lt;size_t&gt;(fault)];
    }
};</pre>
        """,
        "quiz": [
            {
                "question": "What is the time complexity of incrementing a histogram bin indexed by an enum value in a static array?",
                "options": ["O(1) constant time (direct array index access)", "O(N) linear search time", "O(log N) tree search time", "O(N^2) quadratic time"],
                "correct": 0,
                "explanation": "Indexing an array directly by enum value compiles to a single load/add/store instruction sequence in $O(1)$ time."
            },
            {
                "question": "Why is 'std::map<string, int>' suboptimal for histogram counting on microcontrollers?",
                "options": ["std::map dynamically allocates 32-48 byte Red-Black tree nodes on the heap for every unique entry, causing RAM exhaustion and heap fragmentation", "std::map only supports floating point keys", "std::map cannot store numbers", "std::map is deprecated"],
                "correct": 0,
                "explanation": "<code>std::map</code> allocates node objects on the heap, consuming excessive RAM and fragmenting heap memory on microcontrollers."
            },
            {
                "question": "What is the standard idiom for tracking the total number of enum values in an enum class?",
                "options": ["Add a final 'Count' element to the enum: enum class Cat { A=0, B, C, Count };", "Use sizeof(Enum)", "Query the compiler version", "Count lines in the header"],
                "correct": 0,
                "explanation": "Appending a <code>Count</code> element automatically sets its value equal to the total number of preceding items."
            },
            {
                "question": "Where should diagnostic fault counters in an automotive ECU be stored so they persist across engine restarts?",
                "options": ["In Non-Volatile RAM (NVRAM / battery-backed SRAM / EEPROM)", "On the CPU stack frame", "In the CPU instruction cache", "In .bss section RAM"],
                "correct": 0,
                "explanation": "Diagnostic Trouble Code (DTC) histograms are stored in non-volatile memory (EEPROM / NVRAM) to survive vehicle power-down."
            }
        ]
    },
    {
        "id": "employee_salary_report",
        "name": "EmployeeSalaryReport",
        "title": "Tabular Formatting, Stream Manipulators & Statistical Aggregation",
        "headline": "Formatted Stream Manipulators (<iomanip>), Fixed-Width Alignments & Sensor Summary Reports",
        "emb_class": "emb-core",
        "emb_badge": "⚡ Embedded Relevance: Core",
        "tags": ["<iomanip>", "setw", "setprecision", "Formatting", "Statistical Reports"],
        "summary": "Generating formatted tabular text reports using <iomanip> (std::setw, std::setprecision, std::fixed). We analyze table column alignment, computing running averages/min/max statistics, and generating ASCII telemetry summary logs for embedded serial terminals.",
        "files": [
            "section_9/EmployeeSalaryReport/EmployeeSalaryReport/main.cpp",
            "section_9/EmployeeSalaryReport/EmployeeSalaryReport/salaries.txt"
        ],
        "concepts_html": """
        <h3>1. Formatted Stream Manipulators (<code>&lt;iomanip&gt;</code>)</h3>
        <ul>
          <li><code>std::setw(N)</code>: Sets field width for the next item.</li>
          <li><code>std::setprecision(N)</code>: Sets decimal precision.</li>
          <li><code>std::fixed</code>: Formats floating-point numbers with fixed decimal notation.</li>
        </ul>
        """,
        "embedded_html": """
        <h3>1. Embedded ASCII Telemetry Tables</h3>
        <p>In satellite and drone serial consoles, formatted ASCII tables provide human-readable sensor health summaries over radio telemetry links.</p>
        """,
        "refactor_html": """
        <p>Lightweight string buffer table formatter:</p>
        <pre class="code-block" style="background:#0d1117; padding:16px; border-radius:8px; border:1px solid #30363d;">#include &lt;cstdint&gt;
#include &lt;cstdio&gt;

struct SensorReport {
    uint8_t  id;
    int16_t  temp_c;
    uint16_t voltage_mv;
};

// Compact snprintf formatting: 0 <iomanip> Flash bloat!
void formatReportLine(const SensorReport&amp; r, char* out_buf, size_t buf_len) noexcept {
    snprintf(out_buf, buf_len, "| ID: %02u | Temp: %+03d C | V: %04u mV |\\r\\n",
             r.id, r.temp_c, r.voltage_mv);
}</pre>
        """,
        "quiz": [
            {
                "question": "Which header file provides stream manipulators like std::setw, std::setprecision, and std::setfill?",
                "options": ["<iomanip>", "<iostream>", "<stdlib.h>", "<sstream>"],
                "correct": 0,
                "explanation": "<code>&lt;iomanip&gt;</code> contains formatting manipulators for parameterized stream formatting."
            },
            {
                "question": "Why is 'snprintf()' often preferred over '<iomanip>' for formatting text in small microcontroller firmware?",
                "options": ["'snprintf()' is extremely compact in Flash ROM, avoids linking heavy C++ locale machinery, and prevents buffer overflows with explicit length bounds", "'snprintf()' is faster than CPU clock speed", "'snprintf()' only works on 8-bit AVR", "'<iomanip>' cannot output numbers"],
                "correct": 0,
                "explanation": "<code>snprintf()</code> provides bounded, format-string-based output with minimal Flash footprint compared to heavy C++ streams."
            },
            {
                "question": "What is the scope of 'std::setw(10)' when applied to a stream (cout << setw(10) << a << b;)?",
                "options": ["It applies ONLY to the very next single item ('a'); subsequent items ('b') revert to default formatting", "It applies permanently to all future items", "It formats the entire line", "It sets width for the next 10 items"],
                "correct": 0,
                "explanation": "<code>std::setw</code> is non-sticky: it affects only the immediately following output token."
            },
            {
                "question": "How do you calculate running minimum and maximum values across a stream of numbers in $O(1)$ memory?",
                "options": ["Initialize min = +INFINITY, max = -INFINITY, and update with std::min() / std::max() on each element", "Store all elements in a sorted array", "Use a hash table", "Re-read the file from the start on every item"],
                "correct": 0,
                "explanation": "Tracking running min/max requires only two scalar variables updated on each iteration ($O(1)$ space)."
            }
        ]
    },
    {
        "id": "student_roster",
        "name": "StudentRoster",
        "title": "Object Serialization, Binary Structs & CRC32 Integrity",
        "headline": "Class Object File Serialization, Binary Record Streaming & CRC32 Checksums",
        "emb_class": "emb-high",
        "emb_badge": "⚡ Embedded Relevance: Critical",
        "tags": ["Serialization", "Binary Structs", "CRC32", "Data Integrity", "Non-Volatile Storage"],
        "summary": "Building class object serialization and roster persistence. We compare text-based serialization with raw binary struct serialization (write/read), analyze endianness and struct padding issues across different CPU architectures, and implement CRC32 checksum verification to detect Flash corruption.",
        "files": [
            "section_9/StudentRoster/StudentRoster/main.cpp",
            "section_9/StudentRoster/StudentRoster/Student.h",
            "section_9/StudentRoster/StudentRoster/Student.cpp",
            "section_9/StudentRoster/StudentRoster/students.txt"
        ],
        "concepts_html": """
        <h3>1. Object Serialization & Deserialization</h3>
        <p>Converting in-memory C++ objects into a linear stream of bytes for persistent storage, and reconstructing objects from byte streams.</p>

        <h3>2. Text vs Binary Serialization</h3>
        <ul>
          <li><strong>Text (JSON / CSV / ASCII):</strong> Human-readable; large storage footprint; CPU parsing overhead.</li>
          <li><strong>Binary:</strong> Direct memory image; compact; fast $O(1)$ copy; sensitive to padding and endianness.</li>
        </ul>
        """,
        "embedded_html": """
        <h3>1. CRC32 Hardware Checksum Verification</h3>
        <p>In safety-critical avionics and automotive ECUs, serialized Flash data records must include a <strong>CRC32 (Cyclic Redundancy Check)</strong> checksum. Microcontrollers feature on-chip <strong>Hardware CRC calculation units</strong> that verify data integrity in single-digit clock cycles.</p>
        """,
        "refactor_html": """
        <p>Binary record serialization with CRC32 integrity verification:</p>
        <pre class="code-block" style="background:#0d1117; padding:16px; border-radius:8px; border:1px solid #30363d;">#include &lt;cstdint&gt;
#include &lt;array&gt;

#pragma pack(push, 1) // Packed: 0 padding bytes across network / Flash
struct CalibrationRecord {
    uint32_t magic_header; // 0x55AA55AA
    uint32_t serial_number;
    int16_t  zero_offset;
    uint16_t scale_gain;
    uint32_t crc32;        // Checksum over payload bytes
};
#pragma pack(pop)

uint32_t computeHardwareCrc32(const void* data, size_t len) noexcept {
    // Feed bytes into STM32 Hardware CRC Peripheral (CRC->DR)...
    return 0x12345678;
}</pre>
        """,
        "quiz": [
            {
                "question": "What is the primary role of a CRC32 checksum appended to serialized Flash configuration records?",
                "options": ["To detect bit flips, incomplete writes, and memory corruption upon reading data from non-volatile storage", "To compress the data by 50%", "To encrypt user passwords", "To speed up Flash read speeds"],
                "correct": 0,
                "explanation": "CRC32 verifies data integrity, detecting corruptions caused by power interruptions, bit rot, or transmission noise."
            },
            {
                "question": "Why can directly serializing raw structs via 'file.write(reinterpret_cast<char*>(&obj), sizeof(obj))' fail when ported across different CPU architectures?",
                "options": ["Different CPU architectures may have different Endianness (Little-Endian vs Big-Endian) and different compiler struct alignment padding", "Structs cannot be converted to pointers", "C++ forbids binary file writes", "sizeof returns different numbers every time"],
                "correct": 0,
                "explanation": "Raw memory images depend on host CPU endianness and compiler padding rules. Cross-platform formats require explicit endian packing (e.g. Protocol Buffers / packed structs)."
            },
            {
                "question": "What is 'Endianness' in computer architecture?",
                "options": ["The order in which multi-byte integers are stored in memory addresses (Little-Endian: Least Significant Byte first; Big-Endian: Most Significant Byte first)", "The total size of the CPU cache", "The speed of the system clock", "The direction of the stack pointer"],
                "correct": 0,
                "explanation": "Endianness defines byte ordering in memory: Little-Endian (standard on ARM Cortex-M and x86) stores least-significant bytes at lower addresses."
            },
            {
                "question": "What is the purpose of a 'Magic Number Header' (e.g. 0x55AA55AA) at the beginning of an EEPROM configuration block?",
                "options": ["To quickly verify that the memory region has been formatted and initialized with valid firmware data, rather than containing uninitialized 0xFF Flash bytes", "To overclock the EEPROM chip", "To set the baud rate", "To reset the microcontroller"],
                "correct": 0,
                "explanation": "Magic headers allow firmware to distinguish initialized valid data from blank/erased Flash memory (which reads 0xFFFFFFFF)."
            }
        ]
    }
]
