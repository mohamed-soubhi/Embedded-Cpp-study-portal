#!/usr/bin/env python3
"""
Generator script for glossary.html in the Modern C++ & Embedded Systems Study Portal.
Produces a standalone, high-performance, searchable glossary reference page.
"""

import os
import html
from glossary_data import GLOSSARY_TERMS, GLOSSARY_CATEGORIES

PORTAL_DIR = os.path.dirname(os.path.abspath(__file__))

def build_glossary_cards():
    # Sort terms alphabetically by term name (ignoring special symbols like . or - or [)
    sorted_terms = sorted(GLOSSARY_TERMS, key=lambda x: x['term'].lstrip('.-[').lower())
    
    cards_html = []
    current_letter = ""
    
    for item in sorted_terms:
        first_char = item['term'].lstrip('.-[').upper()[0]
        if first_char != current_letter:
            current_letter = first_char
            cards_html.append(f'''
            <div class="glossary-letter-group" id="letter-{current_letter}" data-letter="{current_letter}">
              <div class="glossary-letter-header">
                <span class="letter-badge">{current_letter}</span>
                <span class="letter-line"></span>
              </div>
            </div>
            ''')
            
        tags_rendered = " ".join([f'<span class="tag">{html.escape(t)}</span>' for t in item.get('tags', [])])
        
        rel_links = []
        for rel in item.get('related_sections', []):
            rel_links.append(f'<a href="{rel["url"]}" class="glossary-project-link">📌 {html.escape(rel["title"])}</a>')
        rel_links_rendered = " ".join(rel_links)
        
        category_label = GLOSSARY_CATEGORIES.get(item['category'], item['category'])
        
        cards_html.append(f'''
        <article class="glossary-card" id="{item['id']}" data-category="{item['category']}" data-letter="{first_char}">
          <div class="glossary-card-top">
            <div class="glossary-term-wrap">
              <h3 class="glossary-term-title">
                <a href="#{item['id']}" class="term-anchor" title="Direct link to {html.escape(item['term'])}">{html.escape(item['term'])}</a>
              </h3>
              <div class="glossary-expansion">{html.escape(item['expansion'])}</div>
            </div>
            <div class="glossary-card-meta">
              <span class="glossary-cat-badge cat-{item['category']}">{html.escape(category_label)}</span>
              <button class="btn-copy-term" data-anchor="{item['id']}" title="Copy direct anchor link">🔗 Copy Link</button>
            </div>
          </div>
          
          <div class="glossary-tags">
            {tags_rendered}
          </div>
          
          <div class="glossary-body">
            <div class="glossary-def">
              <strong>Definition &amp; Concept:</strong>
              <p>{item['definition']}</p>
            </div>
            
            <div class="glossary-hw-box">
              <div class="hw-box-title">⚡ Embedded Systems &amp; Low-Level Reality</div>
              <p>{item['hardware_relevance']}</p>
            </div>
          </div>
          
          <div class="glossary-footer">
            <span class="rel-label">Related Curriculum Projects:</span>
            <div class="rel-links-list">
              {rel_links_rendered}
            </div>
          </div>
        </article>
        ''')
        
    return "\n".join(cards_html)

def build_alphabet_nav():
    letters = sorted(list(set(item['term'].lstrip('.-[').upper()[0] for item in GLOSSARY_TERMS)))
    nav_items = []
    for l in letters:
        nav_items.append(f'<a href="#letter-{l}" class="alpha-jump-btn" data-letter="{l}">{l}</a>')
    return "".join(nav_items)

def generate_glossary_page():
    cards_rendered = build_glossary_cards()
    alpha_nav_rendered = build_alphabet_nav()
    total_count = len(GLOSSARY_TERMS)
    
    # Calculate category counts
    cat_counts = {"all": total_count}
    for item in GLOSSARY_TERMS:
        c = item['category']
        cat_counts[c] = cat_counts.get(c, 0) + 1
        
    page_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Technical Glossary &amp; Architecture Reference - Embedded Modern C++: From Bare-Metal to STL</title>
  <link rel="stylesheet" href="assets/style.css">
</head>
<body>
  <header class="site-header">
    <div class="container nav-bar">
      <a href="index.html" class="nav-brand">
        ⚡ Embedded Modern C++
        <span class="badge-tag">Glossary Reference</span>
      </a>
      <ul class="nav-links">
        <li><a href="index.html">🏠 Home</a></li>
        <li><a href="glossary.html" class="active">📖 Glossary</a></li>
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
    <div class="breadcrumb">
      <a href="index.html">Portal Home</a>
      <span class="sep">/</span>
      <span class="current">Technical Glossary &amp; Architecture Reference</span>
    </div>

    <section class="hero glossary-hero">
      <div class="hero-badge">📖 Authoritative Engineering Reference</div>
      <h1>Technical Glossary &amp; Hardware Concepts</h1>
      <p>A comprehensive architectural reference defining the acronyms, CPU registers, low-level idioms, memory layouts, toolchain concepts, and safety standards explored across all 116 curriculum projects.</p>
      
      <div class="glossary-stats-grid">
        <div class="stat-card">
          <span class="stat-num">{total_count}</span>
          <span class="stat-lbl">Technical Terms</span>
        </div>
        <div class="stat-card">
          <span class="stat-num">5</span>
          <span class="stat-lbl">Core Engineering Domains</span>
        </div>
        <div class="stat-card">
          <span class="stat-num">116</span>
          <span class="stat-lbl">Cross-Referenced Projects</span>
        </div>
        <div class="stat-card">
          <span class="stat-num">100%</span>
          <span class="stat-lbl">Zero-Cost &amp; Bare-Metal Focus</span>
        </div>
      </div>
    </section>

    <!-- Search & Filter Controls -->
    <section class="filter-panel glossary-controls">
      <div class="search-box">
        <span class="search-icon">🔍</span>
        <input type="text" id="glossarySearch" class="search-input" placeholder="Search {total_count} terms (e.g. AAPCS, MMIO, DMA, LittleFS, CRTP, VTable, alignas, SRAM, MISRA, DWARF)...">
      </div>
      
      <div class="filter-chips glossary-chips">
        <span class="filter-label">Filter Domain:</span>
        <button class="chip active" data-filter="all">All Domains ({cat_counts.get('all', total_count)})</button>
        <button class="chip" data-filter="embedded-hw">⚡ Embedded &amp; CPU ({cat_counts.get('embedded-hw', 0)})</button>
        <button class="chip" data-filter="cpp-idiom">📚 Modern C++ ({cat_counts.get('cpp-idiom', 0)})</button>
        <button class="chip" data-filter="memory-storage">💾 Memory &amp; Storage ({cat_counts.get('memory-storage', 0)})</button>
        <button class="chip" data-filter="toolchain-standards">🛡️ Toolchains &amp; Standards ({cat_counts.get('toolchain-standards', 0)})</button>
        <button class="chip" data-filter="data-structures">📐 Data Structures ({cat_counts.get('data-structures', 0)})</button>
      </div>

      <!-- Quick Alphabetical Jump Index -->
      <div class="alphabet-nav-bar">
        <span class="alpha-label">Alphabetical Jump:</span>
        <div class="alpha-links">
          {alpha_nav_rendered}
        </div>
      </div>
    </section>

    <!-- Dynamic Result Counter -->
    <div class="results-counter" id="glossaryCounter">
      Showing <strong>{total_count}</strong> of <strong>{total_count}</strong> Technical Terms
    </div>

    <!-- Glossary List Grid -->
    <section class="glossary-container" id="glossaryList">
      {cards_rendered}
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
          <h5>Curriculum &amp; Navigation</h5>
          <ul>
            <li><a href="index.html">🏠 Home Portal (116 Projects)</a></li>
            <li><a href="glossary.html" class="active">📖 Technical Glossary &amp; Reference</a></li>
            <li><a href="section_1/hello.html">Section 1: Toolchains &amp; Linkers</a></li>
            <li><a href="section_5/function_fun_1.html">Section 5: Functions &amp; AAPCS</a></li>
            <li><a href="section_8/pointer_fun.html">Section 8: Pointers &amp; MMIO</a></li>
            <li><a href="section_11/smart_pointer_fun.html">Section 11: Templates &amp; STL</a></li>
          </ul>
        </div>
        <div class="footer-col">
          <h5>Core Embedded Concepts</h5>
          <ul>
            <li><a href="glossary.html#aapcs">ARM AAPCS Standard</a></li>
            <li><a href="glossary.html#mmio">Memory-Mapped I/O (MMIO)</a></li>
            <li><a href="glossary.html#crtp">CRTP Static Polymorphism</a></li>
            <li><a href="glossary.html#littlefs">LittleFS Flash Storage</a></li>
            <li><a href="glossary.html#dma">Direct Memory Access (DMA)</a></li>
            <li><a href="glossary.html#misra-cpp">MISRA C++ Guidelines</a></li>
          </ul>
        </div>
        <div class="footer-col">
          <h5>Attribution &amp; Source</h5>
          <ul>
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

    out_file = os.path.join(PORTAL_DIR, "glossary.html")
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(page_html)
    print(f"✓ Glossary page successfully generated: {out_file}")

if __name__ == "__main__":
    generate_glossary_page()
