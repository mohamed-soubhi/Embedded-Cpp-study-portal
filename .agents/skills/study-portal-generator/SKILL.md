---
name: study-portal-generator
description: >-
  Systematic workflow and architecture guide for building, scaling, and maintaining
  an interactive, high-performance static engineering study portal (with internal X.YY project numbering,
  interactive technical glossary, annotated code viewers, C++ syntax tokenizers, day/night themes,
  responsive SVG/UML diagrams, systems architecture deep-dives, hardware realities, production refactors,
  self-checking MCQ quiz engines, and Cyber Matrix UI) from any code repository or multi-section programming curriculum.
---

# ⚡ Interactive Engineering Study Portal Generator Skill

This skill provides a complete, repeatable, production-tested blueprint for transforming any programming course, code repository, or technical curriculum into an **interactive, high-performance static Study Portal** hosted on GitHub Pages or any static host.

---

## 🎯 When to Use This Skill

Activate this skill when you need to:
- Transform a multi-section code repository into an interactive, browser-accessible documentation and learning portal.
- Translate software constructs into **bare-metal systems realities** (CPU registers, memory alignment, cache locality, calling conventions, assembly mappings, MMIO, AUTOSAR/MISRA).
- Implement systematic **internal project numbering (`X.YY`)** across portal index cards, navigation headers, breadcrumbs, and footer controls.
- Generate an interactive, searchable **Technical Glossary & Architecture Reference** (`glossary.html`) cross-linking terms directly to curriculum projects.
- Add interactive multi-file code viewers with **pure-Python C++ syntax highlighting tokenizers** and 1-click clipboard copying.
- Support **Day & Night theme toggling** (Cyber Matrix Dark / Clean Slate Light) with `localStorage` persistence.
- Render **responsive inline SVG diagrams** (FIFO queues, LIFO stacks, memory maps) and **UML class hierarchy cards**.
- Embed interactive self-checking MCQ quizzes with immediate feedback and technical explanations.
- Deploy a zero-dependency static web application via GitHub Pages.

---

## 🏗️ 1. Architecture & Directory Blueprint

```
repo-root/
├── README.md                                  # Complete course roadmap & embedded realities table
├── complete-cpp-developer-course-2025-main/
│   └── embedded_cpp_study_portal/             # Static portal root (GitHub Pages target)
│       ├── index.html                         # Master landing page (Track 1 & 2 grids, live search)
│       ├── glossary.html                      # Interactive 68-term Technical Glossary & Reference
│       ├── assets/
│       │   ├── style.css                      # Cyber Matrix & Light Theme tokens, layout, UML, pills
│       │   └── app.js                         # Theme toggle, search, category filter & quiz engine
│       ├── section_1/ ... section_12/         # 116 generated project deep-dive HTML pages
│       ├── builder.py                         # C++ syntax tokenizer, tab builder, and page assembler
│       ├── generate_all.py                    # Master build orchestrator & index generator
│       ├── build_glossary.py                  # Standalone glossary page builder
│       ├── glossary_data.py                   # 68-term structured engineering dictionary
│       ├── uml_data_definitions.py            # SVG and UML class models
│       ├── section_1_data.py ... section_10_data.py # Modular data definitions & quizzes
│       └── generate_uml_diagrams.py           # UML generator utilities
```

---

## 🏷️ 2. Internal Project Numbering Standard (`X.YY`)

To maintain clean traceability across large curriculum sets (e.g. 116 projects), every project receives a deterministic two-part identifier: `X.YY` where `X` is the Section Number (1–12) and `YY` is the zero-padded 2-digit project index (`01`, `02`, ...).

### Numbering Scheme Example:
- **Section 1 (Toolchains):** `1.01` (`hello`), `1.02` (`vsc_hello`)
- **Section 2 (Memory & Types):** `2.01` (`hello_world`) &rarr; `2.14` (`secret_agent_id`)
- **Section 5 (Functions & AAPCS):** `5.01` (`function_fun_1`) &rarr; `5.15` (`tic_tac_toe`)
- **Section 11 (Templates & STL):** `11.01` (`smart_pointer_fun`) &rarr; `11.19` (`swapper_test`)
- **Section 12 (Data Structures):** `12.01` (`array_queue_app`) &rarr; `12.10` (`for_proj12_2_files`)

### Numbering Placement Rules:
1. **Master Index Cards (`index.html`)**:
   - Render `#X.YY` pill in `.card-pills`: `<span class="project-num-badge">#{p['num']}</span>`.
   - Prepend title prefix: `<h3 class="card-title"><span class="card-num-prefix">{p['num']}</span> {p['name']}</h3>`.
2. **Individual Project Pages (`section_X/id.html`)**:
   - `<title>[X.YY] Title - Embedded Modern C++: From Bare-Metal to STL</title>`
   - Top Header brand badge: `Section X • #X.YY`
   - Breadcrumbs: `Portal Home / Section X / Project X.YY: Name`
   - Project Meta Header: `<span class="project-num-pill">Project X.YY</span>`
   - Project Headline: `<h1 class="project-title"><span class="title-num">X.YY</span> Headline</h1>`
   - Footer Navigation: `← Previous (X.YY)` / `Next (X.YY) →`

---

## 📖 3. Interactive Technical Glossary Engine (`build_glossary.py` & `glossary_data.py`)

A comprehensive architectural reference linking core concepts to specific projects:

### Architecture:
- **Data Definition (`glossary_data.py`)**: Structured array of term dictionaries containing:
  - `term`: Official technical name (e.g., `AAPCS`, `MMIO`, `Placement-New`, `CRTP`, `Strict Aliasing`, `Erase-Remove Idiom`).
  - `category`: Category slug (`memory`, `hardware`, `concurrency`, `autosar`, `modern_cpp`, `data_structures`).
  - `badge`: Display category badge with distinct color styling.
  - `definition`: Precise technical definition with inline code and embedded hardware implications.
  - `related_projects`: List of internal links with project numbers (e.g., `[{"id": "5.01", "name": "FunctionFun1", "url": "section_5/function_fun_1.html"}]`).
- **Glossary Page Builder (`build_glossary.py`)**:
  - Standalone generator script rendering category filter pills, real-time live search filter, and responsive glossary cards.
  - Callable directly or orchestrated within `generate_all.py`.

---

## 📚 4. The 4-Pillar Pedagogical Framework

Every project page in the portal must follow this 4-pillar structure:

### Pillar 1: Annotated Multi-File Source Code
- Display full working source code with semantic C++ syntax token highlighting.
- Support multi-file tab switching (e.g., `main.cpp`, `Header.h`, `Implementation.cpp`).
- Include 1-click clipboard copy button with visual confirmation.

### Pillar 2: Core Language & Architectural Concepts
- Deep-dive into standard rules, idioms, type systems, and contract invariants.
- **UML Class Diagrams & Visual SVGs:** Class inheritance cards, interface contracts, and data structure layouts.

### Pillar 3: Systems & Hardware Reality (Bare-Metal Grounding)
- **Calling Conventions:** Register usage (e.g. ARM AAPCS R0–R3 vs stack spills).
- **Memory Footprint:** SRAM allocation, struct padding, natural alignment (`alignas`), Flash ROM (`.text`/`.rodata`).
- **Instruction Pipeline:** Branch prediction penalties, table branch jumps (`TBB`/`TBH`), VTable dereferencing overhead.

### Pillar 4: Production-Ready Refactoring
- Concrete, copy-pasteable code examples demonstrating zero-cost abstractions, MISRA/AUTOSAR compliance, and deterministic memory patterns.

---

## 🎨 5. Design System & Theming (Cyber Matrix + Light Mode)

### CSS Variables & Dual-Theme Tokens (`style.css`)
```css
:root {
  --bg-primary: #0a0e14;         /* Deep Obsidian */
  --bg-secondary: #111822;       /* Cyber Slate */
  --bg-card: #121a24;            /* Card Surface */
  --bg-code: #06090d;            /* Terminal Black */
  --text-main: #f0fdf4;          /* Mint White */
  --text-muted: #94a3b8;         /* Slate Gray */
  --text-dim: #64748b;           /* Dim Gray */
  --accent-primary: #10b981;     /* Terminal Emerald */
  --accent-neon: #00ff88;        /* Neon Green */
  --accent-mint: #34d399;        /* Light Mint */
  --border-color: #1e293b;
  --border-glow: rgba(16, 185, 129, 0.35);
}

[data-theme="light"] {
  --bg-primary: #f8fafc;
  --bg-secondary: #ffffff;
  --bg-card: #ffffff;
  --bg-code: #0b1120;
  --text-main: #0f172a;
  --text-muted: #475569;
  --text-dim: #64748b;
  --accent-primary: #059669;
  --accent-neon: #047857;
  --accent-mint: #059669;
  --border-color: #e2e8f0;
  --border-glow: rgba(5, 150, 105, 0.25);
}
```

### Theme Switcher Engine (`app.js`)
```javascript
function initTheme() {
  const savedTheme = localStorage.getItem('study-portal-theme') || 'dark';
  applyTheme(savedTheme);

  document.querySelectorAll('#themeToggle, .theme-toggle-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const current = document.documentElement.getAttribute('data-theme') || 'dark';
      const next = (current === 'dark') ? 'light' : 'dark';
      applyTheme(next);
    });
  });
}

function applyTheme(theme) {
  document.documentElement.setAttribute('data-theme', theme);
  localStorage.setItem('study-portal-theme', theme);
  document.querySelectorAll('#themeToggle, .theme-toggle-btn').forEach(btn => {
    const icon = btn.querySelector('.theme-icon');
    const text = btn.querySelector('.theme-text');
    if (theme === 'light') {
      if (icon) icon.textContent = '🌙';
      if (text) text.textContent = 'Dark';
    } else {
      if (icon) icon.textContent = '☀️';
      if (text) text.textContent = 'Light';
    }
  });
}
```

---

## 💻 6. High-Performance C++ Syntax Tokenizer (`builder.py`)

A pure-Python regex-based tokenizer that emits high-contrast semantic syntax spans without heavy JavaScript runtime dependencies:

```python
import html, re

CPP_KEYWORDS = {
    "auto", "bool", "break", "case", "catch", "class", "concept", "const", "constexpr",
    "continue", "default", "delete", "do", "else", "enum", "explicit", "extern", "false",
    "final", "for", "friend", "if", "inline", "mutable", "namespace", "new", "noexcept",
    "nullptr", "operator", "override", "private", "protected", "public", "return", "sizeof",
    "static", "static_assert", "struct", "switch", "template", "this", "throw", "true",
    "try", "typedef", "typename", "using", "virtual", "volatile", "while"
}

CPP_TYPES = {
    "int", "double", "float", "char", "void", "short", "long", "unsigned", "signed",
    "size_t", "uint8_t", "uint16_t", "uint32_t", "uint64_t", "int8_t", "int16_t",
    "int32_t", "int64_t", "string", "string_view", "vector", "array", "unique_ptr",
    "shared_ptr", "queue", "deque", "list", "stack", "map", "unordered_map", "span", "std"
}

def highlight_cpp(code_str):
    lines = code_str.splitlines()
    highlighted = []
    in_multiline = False

    for raw_line in lines:
        escaped = html.escape(raw_line)
        if in_multiline:
            if "*/" in escaped:
                idx = escaped.find("*/") + 2
                in_multiline = False
                highlighted.append(f'<span class="tok-com">{escaped[:idx]}</span>' + tokenize_line(escaped[idx:]))
            else:
                highlighted.append(f'<span class="tok-com">{escaped}</span>')
            continue

        if "/*" in escaped and "*/" not in escaped:
            idx = escaped.find("/*")
            in_multiline = True
            highlighted.append(tokenize_line(escaped[:idx]) + f'<span class="tok-com">{escaped[idx:]}</span>')
            continue

        if escaped.lstrip().startswith('#'):
            highlighted.append(f'<span class="tok-pre">{escaped}</span>')
            continue

        if "//" in escaped:
            idx = escaped.find("//")
            code_part = escaped[:idx]
            com_part = escaped[idx:]
            com_class = "tok-emb-com" if any(k in com_part for k in ["[EMBEDDED", "HARDWARE", "MISRA", "NOTE"]) else "tok-com"
            highlighted.append(tokenize_line(code_part) + f'<span class="{com_class}">{com_part}</span>')
            continue

        highlighted.append(tokenize_line(escaped))

    return "\n".join(highlighted)

def colorize_code_blocks(html_str):
    """Automatically extracts and applies semantic C++ syntax highlighting to any <pre> blocks in HTML content cards."""
    if not html_str:
        return ""
    def replacer(match):
        inner = match.group(2)
        cleaned = re.sub(r'</?(?:code|span)[^>]*>', '', inner)
        raw_code = html.unescape(cleaned).strip('\r\n')
        highlighted = highlight_cpp(raw_code)
        return f'<pre class="code-block">{highlighted}</pre>'
    return re.sub(r'(<pre[^>]*>)(.*?)(</pre>)', replacer, html_str, flags=re.DOTALL)
```

---

## 📊 7. Visual Architecture & UML Component Design

### Inline Responsive SVG Diagram (e.g. Ring Buffer Queue)
```html
<div class="diagram-container">
  <h4>🔄 Circular Ring Buffer FIFO Architecture</h4>
  <svg class="svg-diagram" width="540" height="170" viewBox="0 0 540 170" xmlns="http://www.w3.org/2000/svg">
    <rect x="20" y="45" width="55" height="55" rx="6" fill="#1e293b" stroke="#10b981" stroke-width="2"/>
    <text x="47" y="77" fill="#f0fdf4" font-family="monospace" font-size="13" text-anchor="middle">Slot 0</text>
    <rect x="85" y="45" width="55" height="55" rx="6" fill="#1e293b" stroke="#10b981" stroke-width="2"/>
    <text x="112" y="77" fill="#f0fdf4" font-family="monospace" font-size="13" text-anchor="middle">Slot 1</text>
    <!-- Pointer Markers -->
    <path d="M 47 130 L 47 110" stroke="#10b981" stroke-width="2"/>
    <polygon points="47,105 42,112 52,112" fill="#10b981"/>
    <text x="47" y="148" fill="#10b981" font-family="sans-serif" font-weight="bold" font-size="12" text-anchor="middle">TAIL (Dequeue)</text>
  </svg>
</div>
```

### UML Class Hierarchy Card
```html
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
  </div>
</div>
```

---

## 🛠️ 8. Automated Pre-Flight Verification Script

Run this verification routine before every release to guarantee zero broken links, zero tag mismatches, and accurate quiz structures:

```python
import os, glob, re

html_files = glob.glob("**/*.html", recursive=True)
errors = 0

for fpath in html_files:
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()
    
    # 1. Check title and links
    if '<title>' not in content or '</title>' not in content:
        print(f"Missing title: {fpath}"); errors += 1
    if 'style.css' not in content:
        print(f"Missing style.css: {fpath}"); errors += 1
    if 'app.js' not in content:
        print(f"Missing app.js: {fpath}"); errors += 1
    if 'themeToggle' not in content:
        print(f"Missing themeToggle: {fpath}"); errors += 1

    # 2. Check tab balance
    if 'index.html' not in fpath and 'glossary.html' not in fpath:
        tabs = len(re.findall(r'\bclass=[\"\']code-tab\b', content))
        panels = len(re.findall(r'\bclass=[\"\']code-panel\b', content))
        if tabs != panels:
            print(f"Tab mismatch in {fpath}: {tabs} tabs vs {panels} panels"); errors += 1

    # 3. Check internal links
    for link in re.findall(r'href=["\']([^"\']+)["\']', content):
        if not link.startswith(('http', '#', 'mailto:')):
            target = os.path.normpath(os.path.join(os.path.dirname(fpath), link.split('?')[0].split('#')[0]))
            if not os.path.exists(target):
                print(f"Broken link in {fpath} -> {link}"); errors += 1

if errors == 0:
    print("✅ All pages passed 100% verification with 0 errors!")
```

---

## 🚀 9. Build, Test & Deployment Workflow

1. **Regenerate Entire Portal:**
   ```bash
   cd complete-cpp-developer-course-2025-main/embedded_cpp_study_portal
   python3 generate_all.py
   ```
2. **Commit & Push:**
   ```bash
   git add -A
   git commit -m "feat: add interactive features and project updates"
   git push origin main
   ```
3. **GitHub Pages URL Configuration:**
   - Repository: `https://github.com/mohamed-soubhi/Embedded-Cpp-study-portal`
   - Portal Home: `https://mohamed-soubhi.github.io/Embedded-Cpp-study-portal/`
   - Technical Glossary: `https://mohamed-soubhi.github.io/Embedded-Cpp-study-portal/glossary.html`
