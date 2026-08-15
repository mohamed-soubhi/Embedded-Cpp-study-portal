---
name: study-portal-generator
description: >-
  Systematic workflow and architecture guide for building, scaling, and maintaining
  an interactive, high-performance static engineering study portal (with annotated code viewers,
  systems architecture deep-dives, hardware realities, production refactors, self-checking MCQ quiz engines,
  and Cyber Matrix UI) from any code repository or multi-section programming curriculum.
---

# ⚡ Interactive Engineering Study Portal Generator Skill

This skill provides a complete, repeatable, production-tested blueprint for transforming any programming course, code repository, or technical curriculum into an **interactive, high-performance static Study Portal** hosted on GitHub Pages or any static host.

---

## 🎯 When to Use This Skill

Activate this skill when you need to:
- Transform a multi-section code repository into an interactive, browser-accessible documentation and learning portal.
- Translate software constructs into **bare-metal systems realities** (CPU registers, memory alignment, cache locality, calling conventions, assembly mappings).
- Add interactive multi-file code viewers with 1-click clipboard copying and syntax highlighting.
- Embed interactive self-checking MCQ quizzes with immediate feedback and technical explanations.
- Deploy a zero-dependency static web application via GitHub Pages.

---

## 🏗️ 1. Architecture & Directory Blueprint

```
repo-root/
├── study_portal/                       # Static portal root (GitHub Pages target)
│   ├── index.html                     # Master landing page with filters & search
│   ├── assets/
│   │   ├── style.css                  # Cyber Matrix / Terminal theme & CSS grid
│   │   └── app.js                     # Dynamic search, filtering & quiz interactivity
│   ├── section_1/ ... section_N/      # Generated project deep-dive HTML pages
│   ├── builder.py                     # Core HTML template generator & component builder
│   ├── generate_all.py                # Master build orchestrator & index assembler
│   ├── section_1_data.py              # Section 1 project metadata & quizzes
│   └── section_N_data.py              # Modular data definition files
```

---

## 📚 2. The 4-Pillar Pedagogical Framework

Every project page in the portal must follow this 4-pillar structure:

### Pillar 1: Annotated Multi-File Source Code
- Display full working source code with semantic syntax token highlighting.
- Support multi-file tab switching (e.g., `main.cpp`, `Header.h`, `Implementation.cpp`).
- Include 1-click clipboard copy button with visual confirmation.

### Pillar 2: Core Language & Architectural Concepts
- Deep-dive into standard rules, idioms, type systems, and contract invariants.
- Comparison tables contrasting legacy approaches vs modern idiomatic alternatives.

### Pillar 3: Systems & Hardware Reality (Bare-Metal Grounding)
- **Calling Conventions:** Register usage (e.g. ARM AAPCS R0–R3 vs stack spills).
- **Memory Footprint:** SRAM allocation, struct padding, natural alignment (`alignas`).
- **Instruction Pipeline:** Branch prediction penalties, table branch jumps (`TBB`/`TBH`).
- **Storage Realities:** Flash ROM placement (`.rodata`), wear leveling, EEPROM ring buffers.

### Pillar 4: Production-Ready Refactoring
- Concrete, copy-pasteable code examples demonstrating zero-cost abstractions, MISRA/AUTOSAR compliance, and deterministic memory patterns.

---

## 🧩 3. Data-Driven Project Schema

Store each section's project definitions in modular Python files (`section_X_data.py`):

```python
SECTION_X_PROJECTS = [
    {
        "id": "unique_project_id",
        "name": "ProjectName",
        "title": "Conceptual Project Title",
        "headline": "One-line Architectural Subtitle",
        "emb_class": "emb-high",                 # "emb-high" | "emb-med" | "emb-core"
        "emb_badge": "⚡ Embedded Relevance: Critical",
        "tags": ["Tag1", "Tag2", "Tag3"],
        "summary": "Plain text summary without raw unclosed HTML tags.",
        "files": [
            "path/to/main.cpp",
            "path/to/Header.h"
        ],
        "concepts_html": """
        <h3>1. Conceptual Heading</h3>
        <p>Architectural breakdown...</p>
        """,
        "embedded_html": """
        <h3>1. Hardware & System Realities</h3>
        <p>Memory, registers, and clock cycles...</p>
        """,
        "refactor_html": """
        <p>Production refactoring pattern:</p>
        <pre class="code-block"><code>// Refactored code</code></pre>
        """,
        "quiz": [
            {
                "question": "Clear, technically rigorous question?",
                "options": [
                    "Correct technical answer",
                    "Plausible distractor 1",
                    "Plausible distractor 2",
                    "Plausible distractor 3"
                ],
                "correct": 0,                    # 0-indexed integer (0 to 3)
                "explanation": "Detailed explanation of why option is correct."
            }
        ]
    }
]
```

---

## 🎨 4. Design System & CSS Rules (Cyber Matrix Theme)

### Color Palette Tokens
```css
:root {
  --bg-primary: #0a0e14;         /* Deep Obsidian */
  --bg-secondary: #111822;       /* Cyber Slate */
  --bg-card: #121a24;            /* Container Surface */
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
```

### Critical Layout Rules
1. **Prevent Card Stretching:**
   - Always strip HTML tags (`re.sub(r'<[^>]+>', '', text)`) before slicing strings for card descriptions. Slicing raw HTML cuts tags in half (e.g. `<code>` &rarr; `<c...`), breaking DOM containers.
   - Use CSS clamp:
     ```css
     .card-desc {
       display: -webkit-box;
       -webkit-line-clamp: 3;
       -webkit-box-orient: vertical;
       overflow: hidden;
       min-height: 3.95rem;
     }
     ```
2. **Equal Height Grid:**
   - Set `.cards-grid { align-items: stretch; }` and `.project-card { height: 100%; display: flex; flex-direction: column; justify-content: space-between; }`.

---

## ⚡ 5. Client-Side Interactivity (`app.js`)

### Instant Search & Dual-Track Filtering
```javascript
function filterProjects() {
  const query = document.getElementById('searchInput').value.toLowerCase();
  const activeTrack = document.querySelector('.track-btn.active')?.dataset.track || 'all';
  const activeSection = document.querySelector('.chip.active')?.dataset.section || 'all';
  
  const cards = document.querySelectorAll('.project-card');
  let visibleCount = 0;

  cards.forEach(card => {
    const title = card.querySelector('.card-title').textContent.toLowerCase();
    const desc = card.querySelector('.card-desc').textContent.toLowerCase();
    const tags = Array.from(card.querySelectorAll('.tag')).map(t => t.textContent.toLowerCase()).join(' ');
    
    const matchesSearch = !query || title.includes(query) || desc.includes(query) || tags.includes(query);
    const matchesTrack = activeTrack === 'all' || card.dataset.track === activeTrack;
    const matchesSection = activeSection === 'all' || card.dataset.section === activeSection;

    if (matchesSearch && matchesTrack && matchesSection) {
      card.style.display = 'flex';
      visibleCount++;
    } else {
      card.style.display = 'none';
    }
  });

  const counter = document.getElementById('resultsCounter');
  if (counter) counter.innerHTML = `Showing <strong>${visibleCount}</strong> matching projects`;
}
```

### Self-Checking MCQ Quiz Handler
```javascript
function initQuizzes() {
  document.querySelectorAll('.quiz-card').forEach(card => {
    const correctIdx = parseInt(card.dataset.correct, 10);
    const options = card.querySelectorAll('.quiz-option');
    const explanation = card.querySelector('.quiz-explanation');

    options.forEach((opt, idx) => {
      opt.addEventListener('click', () => {
        if (card.dataset.answered === 'true') return;
        card.dataset.answered = 'true';

        options.forEach(o => o.classList.add('disabled'));

        if (idx === correctIdx) {
          opt.classList.add('correct');
        } else {
          opt.classList.add('incorrect');
          options[correctIdx].classList.add('correct');
        }

        if (explanation) explanation.classList.add('show');
      });
    });
  });
}
```

---

## 🛠️ 6. Automated Pre-Flight Audit Checklist

Before publishing, run this automated Python verification script across all generated HTML files:

```python
import os, glob, re

portal_dir = "./embedded_cpp_study_portal"
html_files = glob.glob(f"{portal_dir}/**/*.html", recursive=True)
errors = []

for fpath in html_files:
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()
    
    # 1. Check for unclosed tags
    for tag in ["code", "pre", "span", "div", "a"]:
        opens = len(re.findall(rf"<{tag}(\s+[^>]*)?>", content))
        closes = len(re.findall(rf"</{tag}>", content))
        if opens != closes:
            errors.append(f"Tag mismatch <{tag}> in {fpath}")

    # 2. Check internal links
    for link in re.findall(r'href=["\']([^"\']+)["\']', content):
        if not link.startswith(('http', '#', 'mailto:')):
            target = os.path.normpath(os.path.join(os.path.dirname(fpath), link.split('?')[0].split('#')[0]))
            if not os.path.exists(target):
                errors.append(f"Broken link in {fpath}: {link}")

if not errors:
    print("✅ All pages passed structural and link validation perfectly!")
else:
    print(f"❌ Found {len(errors)} validation errors:")
    for e in errors: print(" -", e)
```

---

## 🚀 7. GitHub Pages Deployment Steps

1. Commit and push the `embedded_cpp_study_portal/` directory to GitHub `main` branch.
2. In GitHub repository settings:
   - Navigate to **Settings** &rarr; **Pages**.
   - Set **Source** to `Deploy from a branch`.
   - Set **Branch** to `main` and **Folder** to `/complete-cpp-developer-course-2025-main/embedded_cpp_study_portal` (or root `/` if located at top level).
3. Tag release: `git tag -a v1.0 -m "Release v1.0" && git push origin v1.0`.
