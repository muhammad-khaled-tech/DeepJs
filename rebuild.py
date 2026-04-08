#!/usr/bin/env python3
"""
JS & Node.js Elite Vault — Master Rebuilder
Builds a clean 10-section index.html following the master restructure plan.

Run from inside the project directory:
    python3 rebuild.py

Output: index.html (overwrites existing)
"""
import os, re

from convert_md import parse_md, wrap_section, build_toc, extract_between, read_md

# ── Paths ─────────────────────────────────────────────────────────────
HERE     = os.path.dirname(os.path.abspath(__file__))
JS_DIR   = os.path.join(HERE, "Resources", "JavaScript")
NODE_DIR = os.path.join(HERE, "Resources", "Nodejs")
BASELINE = os.path.join(HERE, "baseline.html")
OUTPUT   = os.path.join(HERE, "index.html")

def js(name):   return read_md(os.path.join(JS_DIR, name))
def node(name): return read_md(os.path.join(NODE_DIR, name))

DIV = '\n<div class="spacer"></div>\n<hr class="divider">\n<div class="spacer"></div>\n'

# ═══════════════════════════════════════════════════════════════════════
print("📚 Loading source files…")
# ═══════════════════════════════════════════════════════════════════════
m1m2       = js("JS_Mastery_Module1_Module2.md")
m3m4       = js("JS_NodeJS_Elite_Vault_Part2_Modules3_4.md")
m5m6       = js("JS_NodeJS_Elite_Vault_Part3_Modules5_6.md")
m7         = js("JS_NodeJS_Elite_Vault_Part4_Module7.md")
qa_vault   = js("JS_NodeJS_Elite_Vault_Part5_QA_Gauntlet.md")
qa_prep    = js("JavaScript interview preparation.md")
engine     = js("JS_Engine_Internals.md")
internals  = js("JS_Internals_Masterclass.md")
fp_master  = js("JS_Functional_Programming_Masterclass.md")
day4       = js("Day-4 lecture  codes.md")
node_int   = node("NodeJS_Internals_Masterclass.md")
node_deep  = node("nodejs-internals-deep-dive (1).md")
node_prep  = node("Node.js_Interview_Prep_Arabic.md")
node_qa    = node("nodejs-interview-questions.md")
cjs        = node("commom modules.md")
esm        = node("esm modules.md")
env_v      = node("ENV Variables.md")
print("   ✅ All 17 files loaded")


# ═══════════════════════════════════════════════════════════════════════
print("✂️  Extracting chunks…")
# ═══════════════════════════════════════════════════════════════════════

# ── Section 0: JS Engine Foundation ──────────────────────────────────
# Module 1 only from m1m2 (stop before Module 2)
s0_mod1     = extract_between(m1m2,
                  r'^# 📦 Module 1',
                  r'^# 📦 Module 2')

# Engine Internals sections 1–5 (LE, VE vs LE, EC, Call Stack, Scope Chain)
# Stop before section 6 (Closures – already covered in Module 1)
s0_engine   = extract_between(engine,
                  r'^## 1\. 📚 Lexical Environment',
                  r'^## 6\. 🔒 Closures')

s0_md = s0_mod1 + DIV + s0_engine

# ── Section 1: OOP, Prototypes & Memory ──────────────────────────────
# Module 2 from m1m2
s1_mod2     = extract_between(m1m2,
                  r'^# 📦 Module 2')

# Module 3 from m3m4 (stop before Module 4)
s1_mod3     = extract_between(m3m4,
                  r'^# 🎒 Module 3',
                  r'^# ⚗️ Module 4')

# Arrow Functions & Lexical this (section 9 of engine)
s1_arrow    = extract_between(engine,
                  r'^## 9\. ➡️ Arrow Functions',
                  r'^## 10\.')

s1_md = s1_mod2 + DIV + s1_mod3 + DIV + s1_arrow

# ── Section 2: V8 Deep Internals ─────────────────────────────────────
# All of JS_Internals_Masterclass (sections 1-5, skip Interview Kit)
s2_internals = extract_between(internals,
                   r'^## 1\. Memory Model',
                   r'^## 6\. Interview Survival Kit')

# eval section from engine (section 10)
s2_eval      = extract_between(engine,
                   r'^## 10\. ⚠️ Eval Execution Context',
                   r'^## 11\.')

s2_md = s2_internals + DIV + s2_eval

# ── Section 3: Functional Programming (Full) ─────────────────────────
# Module 4 from m3m4
s3_mod4     = extract_between(m3m4,
                  r'^# ⚗️ Module 4')

# Pure Functions + Immutability + Currying from engine
s3_pure     = extract_between(engine,
                  r'^## 7\. 🧼 Pure Functions',
                  r'^## 8\.')
s3_immut    = extract_between(engine,
                  r'^## 8\. 🧊 Immutability',
                  r'^## 9\.')
s3_curry    = extract_between(engine,
                  r'^## 11\. 🍛 Currying Functions',
                  r'^## 🗺️')

# FP Masterclass (sections 1-7 including Interview Survival Kit)
s3_fp_main  = extract_between(fp_master,
                  r'^## 1\. Compose vs Pipe')

s3_md = s3_mod4 + DIV + s3_pure + DIV + s3_immut + DIV + s3_curry + DIV + s3_fp_main

# ── Section 4: Node.js Foundations ───────────────────────────────────
s4_md = node_prep   # entire file

# ── Section 5: Node.js Internals ─────────────────────────────────────
s5_md = node_int + DIV + node_deep

# ── Section 6: Async Architecture ────────────────────────────────────
s6_md = m5m6        # Module 5 + Module 6 entire file

# ── Section 7: Module System: CJS & ESM & ENV ────────────────────────
s7_md = cjs + DIV + esm + DIV + env_v

# ── Section 8: Design Patterns + Browser APIs ────────────────────────
s8_md = m7 + DIV + day4

# ── Section 9: Q&A Gauntlet ──────────────────────────────────────────
# Use vault Q&A as base; append supplement from prep file
qa_supplement = extract_between(qa_prep,
                    r'^# Module 9')   # grab Module 9 Q&A block

s9_md = qa_vault
if qa_supplement.strip():
    s9_md += DIV + qa_supplement
s9_md += DIV + node_qa

for name, chunk in [("s0",s0_md),("s1",s1_md),("s2",s2_md),("s3",s3_md),
                     ("s4",s4_md),("s5",s5_md),("s6",s6_md),("s7",s7_md),
                     ("s8",s8_md),("s9",s9_md)]:
    status = "✅" if chunk.strip() else "❌ EMPTY"
    print(f"   {name}: {status} ({len(chunk):,} chars)")


# ═══════════════════════════════════════════════════════════════════════
print("🔄 Converting Markdown → HTML…")
# ═══════════════════════════════════════════════════════════════════════

SECTIONS = [
    (0, "JS Engine Foundation",    "Execution Context · Scope · Closures",   s0_md),
    (1, "OOP & Memory",            "Prototypes · this · Module Pattern",      s1_md),
    (2, "V8 Deep Internals",       "Memory Model · Hidden Classes · GC",      s2_md),
    (3, "Functional Programming",  "Pure Functions · Compose · Railway",      s3_md),
    (4, "Node.js Foundations",     "npm · V8 · Debugging · Security",         s4_md),
    (5, "Node.js Internals",       "C10K · libuv · Thread Pool · Clustering", s5_md),
    (6, "Async Architecture",      "Event Loop · Generators · Streams",       s6_md),
    (7, "Module System",           "CommonJS · ESM · ENV Variables",          s7_md),
    (8, "Design Patterns",         "Node.js Patterns · Browser APIs",         s8_md),
    (9, "Q&A Gauntlet",            "Elite Interview Questions",               s9_md),
]

sections_html = []
tocs_html     = []
nav_html      = []

for sid, title, sub, md_content in SECTIONS:
    body = parse_md(md_content)
    sections_html.append(wrap_section(body, sid, title, sub))
    tocs_html.append(build_toc(body, sid))
    nav_html.append(
        f'<button class="nav-btn" id="nav-{sid}" onclick="showSection({sid})">'
        f'<span class="nav-title">{title}</span>'
        f'<span class="nav-sub">{sub}</span>'
        f'</button>'
    )
    print(f"   ✅ Section {sid}: {title} ({len(body):,} chars)")


# ═══════════════════════════════════════════════════════════════════════
print("📄 Reading baseline shell…")
# ═══════════════════════════════════════════════════════════════════════
with open(BASELINE, 'r', encoding='utf-8') as f:
    shell = f.read()

# ── Strip existing nav buttons (keep label div) ───────────────────────
shell = re.sub(
    r'(<div class="sidebar-label">[^<]*</div>\s*).*?(\s*</nav>)',
    lambda m: m.group(1) + '\n' + '\n'.join(nav_html) + '\n' + m.group(2),
    shell, flags=re.DOTALL
)

# ── Replace all content sections inside <main> ────────────────────────
shell = re.sub(
    r'(<main[^>]*>).*?(</main>)',
    lambda m: m.group(1) + '\n' + '\n'.join(sections_html) + '\n' + m.group(2),
    shell, flags=re.DOTALL
)

# ── Replace TOC inside <aside> ────────────────────────────────────────
shell = re.sub(
    r'(<aside[^>]*>\s*<span[^>]*>[^<]*</span>).*?(</aside>)',
    lambda m: m.group(1) + '\n' + '\n'.join(tocs_html) + '\n' + m.group(2),
    shell, flags=re.DOTALL
)

# ── Fix app.js section count ──────────────────────────────────────────
# Update TOTAL_SECTIONS or any hardcoded count in the inline/linked JS
# The app.js uses a loop up to the total — patch the number
shell = re.sub(r'(totalSections\s*=\s*)\d+', r'\g<1>10', shell)
shell = re.sub(r'(TOTAL_SECTIONS\s*=\s*)\d+', r'\g<1>10', shell)


# ═══════════════════════════════════════════════════════════════════════
print("💾 Writing index.html…")
# ═══════════════════════════════════════════════════════════════════════
with open(OUTPUT, 'w', encoding='utf-8') as f:
    f.write(shell)

# ── Sanity check ─────────────────────────────────────────────────────
ns = len(re.findall(r'id="section-\d+"', shell))
nn = len(re.findall(r'id="nav-\d+"',     shell))
nt = len(re.findall(r'id="toc-\d+"',     shell))
sz = os.path.getsize(OUTPUT)

print()
print("═" * 50)
print(f"  ✅ DONE")
print(f"  Sections : {ns}  (expect 10)")
print(f"  Nav btns : {nn}  (expect 10)")
print(f"  TOC divs : {nt}  (expect 10)")
print(f"  File size: {sz:,} bytes  ({sz//1024} KB)")
print("═" * 50)

if ns != 10 or nn != 10 or nt != 10:
    print("  ⚠️  Count mismatch — check output!")
