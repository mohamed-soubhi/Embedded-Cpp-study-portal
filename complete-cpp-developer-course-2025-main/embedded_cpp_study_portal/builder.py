#!/usr/bin/env python3
import os
import html

PORTAL_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(PORTAL_DIR)

def read_file(rel_path):
    full_path = os.path.join(ROOT_DIR, rel_path)
    if not os.path.exists(full_path):
        return f"// File not found: {rel_path}"
    with open(full_path, "r", encoding="utf-8", errors="replace") as f:
        return f.read()

def syntax_highlight(code_str):
    escaped = html.escape(code_str)
    # Basic highlighting markers can be added or simple styled text
    return escaped

def build_tabs(files_dict):
    tab_headers = []
    tab_panels = []
    
    first = True
    for idx, (filename, content) in enumerate(files_dict.items()):
        active_class = " active" if first else ""
        target_id = f"file-tab-{idx}"
        tab_headers.append(f'<button class="code-tab{active_class}" data-target="{target_id}">{html.escape(filename)}</button>')
        tab_panels.append(f'''
        <div class="code-panel{active_class}" id="{target_id}">
          <pre class="code-block">{html.escape(content)}</pre>
        </div>''')
        first = False
        
    headers_html = "\n            ".join(tab_headers)
    panels_html = "\n".join(tab_panels)
    
    return f'''
      <div class="code-viewer">
        <div class="code-header">
          <div class="code-tabs">
            {headers_html}
          </div>
          <div class="code-actions">
            <button class="btn-copy">📋 Copy Active File</button>
          </div>
        </div>
        {panels_html}
      </div>
    '''

def build_mcq(quiz_list):
    cards_html = []
    for idx, q in enumerate(quiz_list):
        opts_html = []
        for opt_idx, opt_text in enumerate(q['options']):
            letter = chr(ord('A') + opt_idx)
            opts_html.append(f'<div class="quiz-option"><span class="opt-letter">{letter}</span> {html.escape(opt_text)}</div>')
        
        options_rendered = "\n            ".join(opts_html)
        cards_html.append(f'''
        <div class="quiz-card" data-correct="{q['correct']}">
          <div class="quiz-question">
            <span class="q-num">Q{idx+1}.</span> {html.escape(q['question'])}
          </div>
          <div class="quiz-options">
            {options_rendered}
          </div>
          <div class="quiz-explanation">
            <strong>Detailed Explanation:</strong>
            {q['explanation']}
          </div>
        </div>''')
    
    all_cards = "\n".join(cards_html)
    return f'''
    <section class="study-section">
      <div class="quiz-container">
        <div class="quiz-header">
          <h3><span class="icon">📝</span> Knowledge Verification Quiz</h3>
          <p>Test your understanding of the C++ concepts and embedded microcontroller trade-offs covered in this guide. Click any option for instant feedback.</p>
        </div>
        {all_cards}
      </div>
    </section>
    '''

def generate_page(data, prev_link, next_link, section_num):
    files_dict = {}
    for fpath in data['files']:
        fname = os.path.basename(fpath)
        files_dict[fname] = read_file(fpath)
        
    code_viewer_html = build_tabs(files_dict)
    quiz_html = build_mcq(data['quiz'])
    
    tags_html = " ".join([f'<span class="tag">{html.escape(t)}</span>' for t in data['tags']])
    
    html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{html.escape(data['title'])} - C++ & Embedded Systems Guide</title>
  <link rel="stylesheet" href="../assets/style.css">
</head>
<body>
  <header class="site-header">
    <div class="container nav-bar">
      <a href="../index.html" class="nav-brand">
        ⚡ C++ Embedded Deep-Dive
        <span class="badge-tag">Section {section_num}</span>
      </a>
      <ul class="nav-links">
        <li><a href="../index.html">🏠 Home Portal</a></li>
        <li><a href="../section_10/enum_fun.html">Section 10</a></li>
        <li><a href="../section_11/smart_pointer_fun.html">Section 11</a></li>
        <li><a href="../section_12/array_queue_app.html">Section 12</a></li>
        <li><a href="https://github.com/mohamed-soubhi/The-Complete-Cpp-Developer-Course" target="_blank" rel="noopener noreferrer" class="nav-github-link">📦 GitHub Repo</a></li>
      </ul>
    </div>
  </header>

  <main class="container">
    <div class="breadcrumb">
      <a href="../index.html">Portal Home</a>
      <span class="sep">/</span>
      <a href="../index.html">Section {section_num}</a>
      <span class="sep">/</span>
      <span class="current">{html.escape(data['name'])}</span>
    </div>

    <header class="project-header">
      <div class="project-meta">
        <span class="section-pill section-{section_num}">Section {section_num}</span>
        <span class="embedded-badge {data['emb_class']}">{data['emb_badge']}</span>
        {tags_html}
      </div>
      <h1 class="project-title">{html.escape(data['headline'])}</h1>
      <div class="project-summary-box">
        <strong>Executive Summary:</strong> {data['summary']}
      </div>
    </header>

    <section class="study-section">
      <h2 class="section-heading">
        <span class="icon">💻</span> 1. Annotated Source Code
      </h2>
      {code_viewer_html}
    </section>

    <section class="study-section">
      <h2 class="section-heading">
        <span class="icon">📚</span> 2. Core C++ Concepts Deep-Dive
      </h2>
      <div class="content-card">
        {data['concepts_html']}
      </div>
    </section>

    <section class="study-section">
      <h2 class="section-heading">
        <span class="icon">⚡</span> 3. Embedded Systems & Hardware Reality
      </h2>
      <div class="content-card">
        {data['embedded_html']}
      </div>
    </section>

    <section class="study-section">
      <h2 class="section-heading">
        <span class="icon">💡</span> 4. Production-Ready Embedded Refactoring
      </h2>
      <div class="content-card">
        {data['refactor_html']}
      </div>
    </section>

    {quiz_html}

    <footer class="page-nav-footer">
      <a href="{prev_link}" class="btn-nav">← Previous Project</a>
      <a href="../index.html" class="btn-nav">🏠 Portal Index</a>
      <a href="{next_link}" class="btn-nav">Next Project →</a>
    </footer>
  </main>

  <footer class="site-footer">
    <div class="container footer-content">
      <div class="footer-brand">
        <h4>⚡ Modern C++ &amp; Embedded Systems Study Portal</h4>
        <p>An interactive companion for mastering Modern C++ (C++11/14/17/20), zero-overhead abstractions, and bare-metal microcontroller firmware design.</p>
      </div>
      <div class="footer-links-group">
        <div class="footer-col">
          <h5>Course Curriculum</h5>
          <ul>
            <li><a href="../section_10/enum_fun.html">Section 10: OOP &amp; Enums</a></li>
            <li><a href="../section_11/smart_pointer_fun.html">Section 11: Templates &amp; STL</a></li>
            <li><a href="../section_12/array_queue_app.html">Section 12: Data Structures</a></li>
          </ul>
        </div>
        <div class="footer-col">
          <h5>Attribution &amp; Source</h5>
          <ul>
            <li><a href="https://github.com/mohamed-soubhi/The-Complete-Cpp-Developer-Course" target="_blank" rel="noopener noreferrer">GitHub Repository</a></li>
            <li><a href="https://github.com/mohamed-soubhi/The-Complete-Cpp-Developer-Course/blob/main/README.md" target="_blank" rel="noopener noreferrer">Original Course README</a></li>
            <li><span>Author: Mohamed Soubhi</span></li>
          </ul>
        </div>
      </div>
    </div>
    <div class="footer-bottom">
      <p>Original Course &copy; Packt Publishing / Dr. John P. Baugh. Extended Architectural Analysis &amp; Interactive Study Portal by Mohamed Soubhi.</p>
    </div>
  </footer>

  <script src="../assets/app.js"></script>
</body>
</html>'''
    return html_content

print("Template builder initialized")
