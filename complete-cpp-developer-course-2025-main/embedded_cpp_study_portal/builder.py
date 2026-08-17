#!/usr/bin/env python3
import os
import html
import re

PORTAL_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(PORTAL_DIR)

CPP_KEYWORDS = {
    "alignas", "alignof", "auto", "bool", "break", "case", "catch", "class",
    "concept", "const", "consteval", "constexpr", "constinit", "const_cast",
    "continue", "decltype", "default", "delete", "do", "dynamic_cast", "else",
    "enum", "explicit", "export", "extern", "false", "final", "for", "friend",
    "goto", "if", "inline", "mutable", "namespace", "new", "noexcept", "nullptr",
    "operator", "override", "private", "protected", "public", "register",
    "reinterpret_cast", "requires", "return", "sizeof", "static", "static_assert",
    "static_cast", "struct", "switch", "template", "this", "thread_local", "throw",
    "true", "try", "typedef", "typeid", "typename", "union", "using", "virtual",
    "volatile", "while"
}

CPP_TYPES = {
    "int", "double", "float", "char", "void", "short", "long", "unsigned", "signed",
    "size_t", "uint8_t", "uint16_t", "uint32_t", "uint64_t", "int8_t", "int16_t",
    "int32_t", "int64_t", "uintptr_t", "intptr_t", "string", "string_view", "vector",
    "array", "unique_ptr", "shared_ptr", "weak_ptr", "make_unique", "make_shared",
    "queue", "deque", "list", "stack", "map", "unordered_map", "set", "unordered_set",
    "pair", "tuple", "span", "optional", "variant", "expected", "move", "forward",
    "cout", "cin", "endl", "cerr", "ifstream", "ofstream", "fstream", "stringstream",
    "std", "Animal", "Dog", "Cat", "Player", "Warrior", "Mage", "Priest", "House",
    "Rectangle", "Book", "LibraryCard", "IceCreamSundae", "Triangle", "Drone", "Exhibit"
}

def read_file(rel_path):
    full_path = os.path.join(ROOT_DIR, rel_path)
    if not os.path.exists(full_path):
        return f"// File not found: {rel_path}"
    with open(full_path, "r", encoding="utf-8", errors="replace") as f:
        return f.read()

def highlight_cpp(code_str):
    lines = code_str.splitlines()
    highlighted_lines = []
    in_multiline = False

    for raw_line in lines:
        escaped_line = html.escape(raw_line)

        if in_multiline:
            if "*/" in escaped_line:
                idx = escaped_line.find("*/") + 2
                c_part = escaped_line[:idx]
                rest = escaped_line[idx:]
                in_multiline = False
                highlighted_lines.append(f'<span class="tok-com">{c_part}</span>' + tokenize_line(rest))
            else:
                highlighted_lines.append(f'<span class="tok-com">{escaped_line}</span>')
            continue

        if "/*" in escaped_line and "*/" not in escaped_line:
            idx = escaped_line.find("/*")
            code_part = escaped_line[:idx]
            c_part = escaped_line[idx:]
            in_multiline = True
            highlighted_lines.append(tokenize_line(code_part) + f'<span class="tok-com">{c_part}</span>')
            continue

        stripped = escaped_line.lstrip()
        if stripped.startswith('#'):
            highlighted_lines.append(f'<span class="tok-pre">{escaped_line}</span>')
            continue

        if "//" in escaped_line:
            idx = escaped_line.find("//")
            code_part = escaped_line[:idx]
            c_part = escaped_line[idx:]
            if any(k in c_part for k in ["[EMBEDDED", "[HARDWARE", "[AAPCS", "[MISRA", "[AUTOSAR", "NOTE", "CRITICAL", "STEP", "INVARIANT"]):
                c_span = f'<span class="tok-emb-com">{c_part}</span>'
            else:
                c_span = f'<span class="tok-com">{c_part}</span>'
            highlighted_lines.append(tokenize_line(code_part) + c_span)
            continue

        highlighted_lines.append(tokenize_line(escaped_line))

    return "\n".join(highlighted_lines)

def tokenize_line(line):
    if not line:
        return ""
    pattern = re.compile(r'(&quot;.*?&quot;|\'.*?\'|0x[0-9a-fA-F]+|0b[01]+|\b\d+(?:\.\d+)?f?\b|\b[a-zA-Z_]\w*\b|[^\s\w]+)')
    pos = 0
    result = []
    for m in pattern.finditer(line):
        start, end = m.span()
        if start > pos:
            result.append(line[pos:start])
        tok = m.group(0)
        if tok.startswith('&quot;') or (tok.startswith("'") and tok.endswith("'")):
            result.append(f'<span class="tok-str">{tok}</span>')
        elif re.match(r'^(0x[0-9a-fA-F]+|0b[01]+|\d+(?:\.\d+)?f?)$', tok):
            result.append(f'<span class="tok-num">{tok}</span>')
        elif tok in CPP_KEYWORDS:
            result.append(f'<span class="tok-kw">{tok}</span>')
        elif tok in CPP_TYPES or tok.startswith('std::'):
            result.append(f'<span class="tok-type">{tok}</span>')
        elif end < len(line) and line[end:end+1] == '(':
            result.append(f'<span class="tok-fn">{tok}</span>')
        else:
            result.append(tok)
        pos = end
    if pos < len(line):
        result.append(line[pos:])
    return "".join(result)

def build_tabs(files_dict):
    tab_headers = []
    tab_panels = []
    
    first = True
    for idx, (filename, content) in enumerate(files_dict.items()):
        active_class = " active" if first else ""
        target_id = f"file-tab-{idx}"
        tab_headers.append(f'<button class="code-tab{active_class}" data-target="{target_id}">{html.escape(filename)}</button>')
        highlighted_code = highlight_cpp(content)
        tab_panels.append(f'''
        <div class="code-panel{active_class}" id="{target_id}">
          <pre class="code-block">{highlighted_code}</pre>
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

def format_uml_item(raw_item):
    if isinstance(raw_item, dict):
        vis = raw_item.get("vis", "+")
        name = raw_item.get("name", "")
        itype = raw_item.get("type", "")
        spec = raw_item.get("spec", "")
    else:
        raw_str = str(raw_item).strip()
        vis = "+"
        if raw_str.startswith("-"):
            vis = "-"
            raw_str = raw_str[1:].strip()
        elif raw_str.startswith("+"):
            vis = "+"
            raw_str = raw_str[1:].strip()
        elif raw_str.startswith("#"):
            vis = "#"
            raw_str = raw_str[1:].strip()
        elif raw_str.startswith("~"):
            vis = "~"
            raw_str = raw_str[1:].strip()

        spec = ""
        spec_match = re.search(r'\[(.*?)\]$', raw_str)
        if spec_match:
            spec = spec_match.group(1)
            raw_str = raw_str[:spec_match.start()].strip()

        if ")" in raw_str:
            close_idx = raw_str.rfind(")")
            after_paren = raw_str[close_idx+1:].strip()
            if after_paren.startswith(":"):
                name = raw_str[:close_idx+1].strip()
                itype = after_paren
            else:
                name = raw_str[:close_idx+1].strip() + ((" " + after_paren) if after_paren else "")
                itype = ""
        elif ":" in raw_str:
            parts = raw_str.split(":", 1)
            name = parts[0].strip()
            itype = ": " + parts[1].strip()
        else:
            name = raw_str
            itype = ""

    vis_class = "public"
    if vis == "-":
        vis_class = "private"
    elif vis == "#":
        vis_class = "protected"
    elif vis == "~":
        vis_class = "internal"

    spec_html = f'<span class="method-spec">[{html.escape(spec)}]</span>' if spec else ""
    type_html = f' <span class="field-type">{html.escape(itype)}</span>' if itype else ""
    name_html = f'<span class="field-name">{html.escape(name)}</span>'

    return f'<div class="uml-item {vis_class}"><span class="vis">{vis}</span>{name_html}{type_html}{spec_html}</div>'

def build_uml_section(uml_data, default_title="UML Architecture & Class Model"):
    if not uml_data:
        return ""
    if isinstance(uml_data, str):
        if "<div" in uml_data or "<svg" in uml_data:
            return uml_data
        else:
            return f'<p>{html.escape(uml_data)}</p>'

    if isinstance(uml_data, list):
        classes_list = uml_data
        title = default_title
        relationships = []
        notes = ""
    else:
        classes_list = uml_data.get("classes", [])
        title = uml_data.get("title", default_title)
        relationships = uml_data.get("relationships", [])
        notes = uml_data.get("notes", "")

    cards_html = []
    for cls in classes_list:
        cname = cls.get("name", "Unnamed")
        cstereo = cls.get("stereotype", "<<class>>")
        cbadge = cls.get("badge", "")
        ctype = cls.get("type", "")
        card_class = "uml-class-card"
        if "abstract" in cstereo.lower() or ctype == "abstract":
            card_class += " abstract-class"
        elif "struct" in cstereo.lower() or ctype == "struct":
            card_class += " struct-card"
        elif "unit" in cstereo.lower() or "module" in cstereo.lower() or ctype == "module":
            card_class += " module-card"

        badge_html = f'<span class="uml-badge-tag">{html.escape(cbadge)}</span>' if cbadge else ""
        
        attrs = cls.get("attributes", [])
        attrs_rendered = [format_uml_item(a) for a in attrs]
        
        if attrs_rendered:
            attrs_section_html = f'''
            <div class="uml-section">
              <div class="uml-section-label">Attributes / Data Members</div>
              {''.join(attrs_rendered)}
            </div>
            '''
        else:
            attrs_section_html = f'''
            <div class="uml-section">
              <div class="uml-section-label">Attributes / Data Members</div>
              <div class="uml-item public" style="color:var(--text-dim); font-style:italic;">(none / stateless)</div>
            </div>
            '''

        methods = cls.get("methods", [])
        methods_rendered = [format_uml_item(m) for m in methods]
        
        methods_section_html = ""
        if methods_rendered:
            methods_section_html = f'''
            <div class="uml-section">
              <div class="uml-section-label">Operations / Methods</div>
              {''.join(methods_rendered)}
            </div>
            '''

        cards_html.append(f'''
        <div class="{card_class}">
          <div class="uml-class-header">
            <span class="uml-stereotype">{html.escape(cstereo)}</span>
            <span class="uml-class-name">{html.escape(cname)}</span>
            {badge_html}
          </div>
          {attrs_section_html}
          {methods_section_html}
        </div>
        ''')

    rel_html = ""
    if relationships:
        rows = []
        for r in relationships:
            r_from = html.escape(r.get("from", ""))
            r_to = html.escape(r.get("to", ""))
            r_type = r.get("type", "inherits")
            r_label = html.escape(r.get("label", r_type))
            arrow = "──▷"
            if r_type == "composes":
                arrow = "◆──"
            elif r_type == "aggregates":
                arrow = "◇──"
            elif r_type == "uses":
                arrow = "─ ─ >"
            elif r_type == "implements":
                arrow = "- - ▷"
            
            rows.append(f'''
            <div class="uml-rel-row">
              <strong>{r_from}</strong>
              <span>{arrow}</span>
              <span class="uml-rel-badge {r_type}">{r_label}</span>
              <span>{arrow}</span>
              <strong>{r_to}</strong>
            </div>
            ''')
        rel_html = f'''
        <div class="uml-relationships">
          <div class="uml-rel-title">🔗 Architectural Relationships &amp; Hierarchy</div>
          <div class="uml-rel-list">
            {''.join(rows)}
          </div>
        </div>
        '''

    notes_html = f'<p style="margin-top:12px; font-size:0.88rem; color:var(--text-muted);">{notes}</p>' if notes else ""

    return f'''
    <div class="uml-diagram-wrapper">
      <div class="uml-header-bar">
        <div class="uml-header-title">
          <span>📐</span> {html.escape(title)}
        </div>
        <div class="uml-legend">
          <span class="uml-legend-item"><span class="uml-legend-badge pub">+</span> Public</span>
          <span class="uml-legend-item"><span class="uml-legend-badge priv">-</span> Private</span>
          <span class="uml-legend-item"><span class="uml-legend-badge prot">#</span> Protected</span>
        </div>
      </div>
      <div class="uml-grid">
        {''.join(cards_html)}
      </div>
      {rel_html}
      {notes_html}
    </div>
    '''

def generate_page(data, prev_link, next_link, section_num):
    files_dict = {}
    for fpath in data['files']:
        fname = os.path.basename(fpath)
        files_dict[fname] = read_file(fpath)
        
    code_viewer_html = build_tabs(files_dict)
    quiz_html = build_mcq(data['quiz'])
    uml_content_html = build_uml_section(data.get('uml_diagram') or data.get('uml_html', ''))
    
    tags_html = " ".join([f'<span class="tag">{html.escape(t)}</span>' for t in data['tags']])
    
    html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{html.escape(data['title'])} - Embedded Modern C++: From Bare-Metal to STL</title>
  <link rel="stylesheet" href="../assets/style.css">
</head>
<body>
  <header class="site-header">
    <div class="container nav-bar">
      <a href="../index.html" class="nav-brand">
        ⚡ Embedded Modern C++
        <span class="badge-tag">Section {section_num}</span>
      </a>
      <ul class="nav-links">
        <li><a href="../index.html">🏠 Home Portal</a></li>
        <li><a href="../glossary.html">📖 Glossary</a></li>
        <li><a href="../section_1/hello.html">Sec 1</a></li>
        <li><a href="../section_2/hello_world.html">Sec 2</a></li>
        <li><a href="../section_3/control_statements_intro.html">Sec 3</a></li>
        <li><a href="../section_4/array_fun.html">Sec 4</a></li>
        <li><a href="../section_5/function_fun_1.html">Sec 5</a></li>
        <li><a href="../section_6/book_fun.html">Sec 6</a></li>
        <li><a href="../section_7/bug_fun.html">Sec 7</a></li>
        <li><a href="../section_8/pointer_fun.html">Sec 8</a></li>
        <li><a href="../section_9/file_input_fun.html">Sec 9</a></li>
        <li><a href="../section_10/enum_fun.html">Sec 10</a></li>
        <li><a href="../section_11/smart_pointer_fun.html">Sec 11</a></li>
        <li><a href="../section_12/array_queue_app.html">Sec 12</a></li>
        <li>
          <button id="themeToggle" class="theme-toggle-btn" aria-label="Toggle theme" title="Toggle Light/Dark Theme">
            <span class="theme-icon">☀️</span>
            <span class="theme-text">Light</span>
          </button>
        </li>
        <li><a href="https://github.com/mohamed-soubhi/Embedded-Cpp-study-portal" target="_blank" rel="noopener noreferrer" class="nav-github-link">📦 GitHub</a></li>
      </ul>
    </div>
  </header>

  <main class="container">
    <div class="breadcrumb">
      <a href="../index.html">Portal Home</a>
      <span class="sep">/</span>
      <a href="../index.html#grid-{'foundations' if int(section_num) <= 6 else 'advanced'}">Section {section_num}</a>
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
        <span class="icon">📐</span> 2. Architecture &amp; UML Class Model
      </h2>
      <div class="content-card">
        {uml_content_html}
      </div>
    </section>

    <section class="study-section">
      <h2 class="section-heading">
        <span class="icon">📚</span> 3. Core C++ Concepts Deep-Dive
      </h2>
      <div class="content-card">
        {data['concepts_html']}
      </div>
    </section>

    <section class="study-section">
      <h2 class="section-heading">
        <span class="icon">⚡</span> 4. Embedded Systems &amp; Hardware Reality
      </h2>
      <div class="content-card">
        {data['embedded_html']}
      </div>
    </section>

    <section class="study-section">
      <h2 class="section-heading">
        <span class="icon">💡</span> 5. Production-Ready Embedded Refactoring
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
        <h4>⚡ Embedded Modern C++: From Bare-Metal to STL</h4>
        <p>An interactive companion for mastering Modern C++ (C++11/14/17/20), zero-overhead abstractions, and bare-metal microcontroller firmware design.</p>
      </div>
      <div class="footer-links-group">
        <div class="footer-col">
          <h5>Course Curriculum (Foundations)</h5>
          <ul>
            <li><a href="../section_1/hello.html">Section 1: Toolchains &amp; Linkers</a></li>
            <li><a href="../section_2/hello_world.html">Section 2: Types &amp; Variables</a></li>
            <li><a href="../section_3/control_statements_intro.html">Section 3: Control Flow</a></li>
            <li><a href="../section_4/array_fun.html">Section 4: Arrays &amp; Locality</a></li>
            <li><a href="../section_5/function_fun_1.html">Section 5: Functions &amp; Scope</a></li>
            <li><a href="../section_6/book_fun.html">Section 6: OOP Foundations</a></li>
          </ul>
        </div>
        <div class="footer-col">
          <h5>Course Curriculum (Advanced)</h5>
          <ul>
            <li><a href="../section_7/bug_fun.html">Section 7: Exceptions &amp; Faults</a></li>
            <li><a href="../section_8/pointer_fun.html">Section 8: Pointers &amp; Memory</a></li>
            <li><a href="../section_9/file_input_fun.html">Section 9: Streams &amp; Flash FS</a></li>
            <li><a href="../section_10/enum_fun.html">Section 10: OOP &amp; Enums</a></li>
            <li><a href="../section_11/smart_pointer_fun.html">Section 11: Templates &amp; STL</a></li>
            <li><a href="../section_12/array_queue_app.html">Section 12: Data Structures</a></li>
          </ul>
        </div>
        <div class="footer-col">
          <h5>Attribution &amp; Source</h5>
          <ul>
            <li><a href="../glossary.html">📖 Technical Glossary &amp; Reference</a></li>
            <li><a href="https://github.com/mohamed-soubhi/Embedded-Cpp-study-portal" target="_blank" rel="noopener noreferrer">GitHub Repository</a></li>
            <li><a href="https://github.com/mohamed-soubhi/Embedded-Cpp-study-portal/blob/main/README.md" target="_blank" rel="noopener noreferrer">Course Syllabus &amp; Setup</a></li>
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
