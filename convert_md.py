#!/usr/bin/env python3
"""
JS & Node.js Elite Vault — Markdown → HTML Converter
Handles: headings, fenced code blocks (with copy button), callouts,
mermaid diagrams, tables, ordered/unordered lists, inline code,
bold, italic, horizontal rules.
"""
import re, sys, os

CALLOUT_MAP = {
    "فخ":        ("callout-bug",      "🕵️", "فخ الانترفيو"),
    "انترفيو":   ("callout-bug",      "🕵️", "سؤال الإنترفيو"),
    "interview": ("callout-bug",      "🕵️", "Interview Trap"),
    "trap":      ("callout-bug",      "🕵️", "Interview Trap"),
    "danger":    ("callout-bug",      "🕵️", "خطر"),
    "bug":       ("callout-bug",      "🕵️", "Bug"),
    "abstract":  ("callout-abstract", "🧠", "المفهوم"),
    "مفهوم":     ("callout-abstract", "🧠", "المفهوم المعماري"),
    "concept":   ("callout-abstract", "🧠", "المفهوم"),
    "معمار":     ("callout-abstract", "🧠", "المفهوم المعماري"),
    "under the hood": ("callout-abstract", "🧠", "Under the Hood"),
    "✅":         ("callout-success",  "✅", "Checkpoint"),
    "checkpoint": ("callout-success",  "✅", "Checkpoint"),
    "الإجابة":   ("callout-success",  "✅", "الإجابة النموذجية"),
    "answer":    ("callout-success",  "✅", "الإجابة"),
    "صح":        ("callout-success",  "✅", "الطريقة الصح"),
    "success":   ("callout-success",  "✅", "Success"),
    "مثال":      ("callout-example",  "💻", "مثال عملي"),
    "example":   ("callout-example",  "💻", "Example"),
    "كود":       ("callout-example",  "💻", "كود"),
    "scenario":  ("callout-example",  "💻", "Scenario"),
    "سيناريو":   ("callout-example",  "💻", "سيناريو"),
    "tip":       ("callout-tip",      "⚡", "Tip"),
    "نصيحة":     ("callout-tip",      "⚡", "نصيحة السينيور"),
    "قاعدة":     ("callout-tip",      "⚡", "القاعدة الذهبية"),
    "زتونة":     ("callout-tip",      "⚡", "زتونة الإنترفيو"),
    "note":      ("callout-tip",      "⚡", "ملاحظة"),
    "info":      ("callout-tip",      "⚡", "معلومة"),
    "warning":   ("callout-tip",      "⚡", "تحذير"),
    "تحذير":     ("callout-tip",      "⚡", "تحذير"),
}

def detect_callout(first_line):
    low = first_line.lower()
    for kw, val in CALLOUT_MAP.items():
        if kw in low:
            return val
    return ("callout-abstract", "🧠", "ملاحظة")

def slugify(text):
    text = re.sub(r'[`*_]', '', text)
    text = re.sub(r'[^\w\s\u0600-\u06FF-]', '', text)
    text = re.sub(r'\s+', '-', text.strip().lower())
    return text or 'section'

def process_inline(line):
    parts, codes = [], {}
    def stash_code(m):
        k = f"\x00CODE{len(codes)}\x00"
        content = m.group(1).replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
        codes[k] = f'<code class="inline-code">{content}</code>'
        return k
    line = re.sub(r'`([^`]+)`', stash_code, line)
    line = re.sub(r'\*\*\*(.+?)\*\*\*', r'<strong><em>\1</em></strong>', line)
    line = re.sub(r'\*\*(.+?)\*\*',     r'<strong>\1</strong>', line)
    line = re.sub(r'(?<!\*)\*([^*\n]+?)\*(?!\*)', r'<em>\1</em>', line)
    for k, v in codes.items():
        line = line.replace(k, v)
    return line

def flush_list(buf, kind):
    tag = 'ol' if kind == 'ol' else 'ul'
    items = '\n'.join(f'<li>{process_inline(t)}</li>' for t in buf)
    return f'<{tag} class="content-list">\n{items}\n</{tag}>\n<div class="spacer"></div>'

def parse_md(md_text):
    lines = md_text.split('\n')
    out   = []
    in_code = False; code_lang = ''; code_lines = []
    in_callout = False; co_cls = co_icon = co_title = ''; co_lines = []
    list_buf = []; list_kind = None

    def flush_callout():
        nonlocal in_callout, co_lines
        if not in_callout: return
        body_parts = []
        in_sub = False; sub_lang = ''; sub_lines = []
        for ln in co_lines:
            ln = ln.strip()
            if ln.startswith('```'):
                if in_sub:
                    cs = '\n'.join(sub_lines).replace('<','&lt;').replace('>','&gt;')
                    body_parts.append(f'<pre><code class="language-{sub_lang}">{cs}</code></pre>')
                    in_sub = False; sub_lines = []
                else:
                    in_sub = True; sub_lang = ln[3:].strip() or 'javascript'
                continue
            if in_sub: sub_lines.append(ln); continue
            if not ln: continue
            if re.match(r'^\d+\.\s', ln):
                body_parts.append(f'<p class="callout-list-item">{process_inline(ln)}</p>')
            elif re.match(r'^[-*]\s', ln):
                body_parts.append(f'<p class="callout-list-item">{process_inline(ln[2:])}</p>')
            else:
                body_parts.append(f'<p>{process_inline(ln)}</p>')
        if in_sub and sub_lines:
            cs = '\n'.join(sub_lines).replace('<','&lt;').replace('>','&gt;')
            body_parts.append(f'<pre><code class="language-{sub_lang}">{cs}</code></pre>')
        body = '\n'.join(body_parts)
        out.append(f'<div class="{co_cls} callout"><div class="callout-title"><span class="callout-icon">{co_icon}</span><span>{co_title}</span></div><div class="callout-body">{body}</div></div>')
        out.append('<div class="spacer"></div>')
        in_callout = False; co_lines.clear()

    def flush_list_now():
        nonlocal list_buf, list_kind
        if list_buf:
            out.append(flush_list(list_buf, list_kind))
            list_buf[:] = []; list_kind = None

    def close_code():
        nonlocal in_code, code_lines, code_lang
        if not in_code: return
        if code_lang == 'mermaid':
            diagram = '\n'.join(code_lines)
            out.append(f'<div class="mermaid-wrap"><div class="mermaid">{diagram}\n</div></div>')
        else:
            cs = '\n'.join(code_lines).replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
            lang = code_lang or 'javascript'
            out.append(
                f'<div class="code-block-wrap"><span class="code-lang">{lang}</span>'
                f'<pre><code class="language-{lang}">{cs}</code></pre>'
                f'<button class="copy-btn" onclick="copyCode(this)" title="نسخ">📋</button></div>'
            )
        out.append('<div class="spacer"></div>')
        in_code = False; code_lines[:] = []

    i = 0
    while i < len(lines):
        raw = lines[i]; line = raw.rstrip()

        if line.lstrip().startswith('```'):
            if in_code:
                close_code()
            else:
                flush_callout(); flush_list_now()
                in_code = True; code_lang = line.lstrip('`').strip(); code_lines = []
            i += 1; continue

        if in_code:
            code_lines.append(raw.rstrip()); i += 1; continue

        if line.startswith('>'):
            content = line[1:].strip()
            if not in_callout:
                flush_list_now(); in_callout = True
                co_cls, co_icon, co_title = detect_callout(content)
            if content: co_lines.append(content)
            i += 1; continue

        if in_callout:
            if line.strip() == '':
                flush_callout(); i += 1; continue
            else:
                flush_callout()

        hm = re.match(r'^(#{1,4})\s+(.+)$', line)
        if hm:
            flush_list_now()
            level = len(hm.group(1)); text = process_inline(hm.group(2)); hid = slugify(hm.group(2))
            out.append(f'<h{level} id="{hid}" class="heading-{level}">{text}</h{level}>')
            out.append('<div class="spacer"></div>'); i += 1; continue

        if re.match(r'^---+$', line.strip()):
            flush_list_now()
            out.append('<hr class="divider">'); out.append('<div class="spacer"></div>'); i += 1; continue

        if line.startswith('|') and i + 1 < len(lines) and re.match(r'^\|[\s\-|:]+\|', lines[i+1]):
            flush_list_now()
            table_rows = []
            while i < len(lines) and lines[i].strip().startswith('|'):
                table_rows.append(lines[i].strip()); i += 1
            if len(table_rows) >= 3:
                headers = [c.strip() for c in table_rows[0].split('|')[1:-1]]
                t  = '<div class="table-wrap"><table class="content-table"><thead><tr>'
                t += ''.join(f'<th>{process_inline(h)}</th>' for h in headers)
                t += '</tr></thead><tbody>'
                for row in table_rows[2:]:
                    cells = [c.strip() for c in row.split('|')[1:-1]]
                    t += '<tr>' + ''.join(f'<td>{process_inline(c)}</td>' for c in cells) + '</tr>'
                t += '</tbody></table></div><div class="spacer"></div>'
                out.append(t)
            continue

        ul_m = re.match(r'^(\s*)[-*+]\s+(.+)$', line)
        if ul_m:
            if list_kind == 'ol': flush_list_now()
            list_kind = 'ul'; list_buf.append(ul_m.group(2)); i += 1; continue

        ol_m = re.match(r'^(\s*)\d+\.\s+(.+)$', line)
        if ol_m:
            if list_kind == 'ul': flush_list_now()
            list_kind = 'ol'; list_buf.append(ol_m.group(2)); i += 1; continue

        if not line.strip():
            flush_list_now(); i += 1; continue

        flush_list_now()
        out.append(f'<p>{process_inline(line)}</p>')
        i += 1

    flush_callout(); flush_list_now(); close_code()
    return '\n'.join(out)

def build_toc(html_body, section_id):
    links = []
    for m in re.finditer(r'<h([123])\s+id="([^"]+)"[^>]*>(.*?)</h\1>', html_body):
        level = int(m.group(1)); hid = m.group(2)
        label = re.sub(r'<[^>]+>', '', m.group(3)).strip()
        indent = (level - 1) * 14
        links.append(f'<a href="#{hid}" class="toc-link toc-level-{level}" style="padding-right:{indent}px" onclick="showSection({section_id})">{label}</a>')
    display = 'block' if section_id == 0 else 'none'
    inner = '\n'.join(links) if links else f'<a href="#" class="toc-link toc-level-1" onclick="showSection({section_id})">Section {section_id}</a>'
    return f'<div id="toc-{section_id}" class="toc-section" style="display:{display}">{inner}\n</div>'

def wrap_section(html_body, section_id, title, subtitle):
    display = 'block' if section_id == 0 else 'none'
    return (
        f'<section id="section-{section_id}" class="content-section" style="display:{display}">'
        f'<div class="section-header"><h1 class="section-title">{title}</h1>'
        f'<p class="section-subtitle">{subtitle}</p></div>'
        f'<div class="section-body">\n{html_body}\n<div class="spacer"></div></div></section>'
    )

def extract_between(text, start_pat, end_pat=None):
    lines = text.split('\n'); out = []; capturing = False
    for line in lines:
        if not capturing:
            if re.match(start_pat, line): capturing = True; out.append(line)
        else:
            if end_pat and re.match(end_pat, line): break
            out.append(line)
    return '\n'.join(out).strip()

def read_md(path):
    with open(path, 'r', encoding='utf-8') as f: return f.read()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 convert_md.py <file.md>"); sys.exit(0)
    print(parse_md(read_md(sys.argv[1])))
