# MASTER RESTRUCTURE PLAN — JS & Node.js Elite Vault
## For Antigravity IDE Agents (Opus 4.6)
### READ THIS ENTIRE DOCUMENT BEFORE WRITING A SINGLE LINE OF CODE

---

## PART 0: DIAGNOSIS — WHAT'S BROKEN RIGHT NOW

### Bug #1: Content Bleeding into Wrong Sections
The Python conversion script dumped content from `JS_Internals_Masterclass.md`
into the wrong sections:

- **Lines ~677–976 in section-0** contain `Memory Model العميق` 
  → This does NOT belong in Module 1 & 2. Move it to new section-2.

- **Lines ~1857–2038 in section-1** contain `WeakRef & FinalizationRegistry`
  → This does NOT belong in Module 3 & 4. Move it to new section-2.

### Bug #2: Missing Content (6 Files Never Converted)
These files exist in `Resources/` but are completely absent from index.html:
1. `Resources/Nodejs/NodeJS_Internals_Masterclass.md` — 0% converted
2. `Resources/Nodejs/commom modules.md` — 0% converted  
3. `Resources/Nodejs/esm modules.md` — 0% converted
4. `Resources/Nodejs/ENV Variables.md` — 0% converted
5. `Resources/Nodejs/Node.js_Interview_Prep_Arabic.md` — 0% converted
6. `Resources/JavaScript/Day-4 lecture  codes.md` — 0% converted

### Bug #3: JS_Engine_Internals.md Partially Missing
`Resources/JavaScript/JS_Engine_Internals.md` has 11 sections.
Only sections 1 (LE), 3 (EC), 4 (Call Stack), 5 (Scope), 6 (Closures) made it in.
MISSING from HTML: Section 2 (VE vs LE), Section 10 (eval), Section 11 (Currying).

### Bug #4: Incoherent Module Numbering
- Modules 1–7 follow one numbering system
- Then suddenly "Module 8, 9, 10" appear with no logical connection
- The Q&A is labeled "25 سؤال" but has 30 questions

### Bug #5: Duplicate/Redundant Content
- Module Pattern appears in BOTH section-0 (Module 2.1) and section-1 (Module 3.2)
- Closures appear in BOTH section-0 (1.3) and section-1 (3.1) with heavy overlap
- Pure Functions + HOF in section-1 AND referenced again in FP Masterclass

---

## PART 1: THE NEW STRUCTURE — 10 SECTIONS

The new site has sections 0–9. Delete all current sections and rebuild from scratch.

```
SECTION 0: JS Engine Foundation
SECTION 1: OOP, Prototypes & Memory  
SECTION 2: V8 Deep Internals
SECTION 3: Functional Programming (Full)
SECTION 4: Node.js Foundations
SECTION 5: Node.js Internals
SECTION 6: Async Architecture
SECTION 7: Module System: CJS & ESM
SECTION 8: Design Patterns & Browser APIs
SECTION 9: Q&A Gauntlet (30 Questions)
```

---

## PART 2: SECTION-BY-SECTION CONTENT SPECIFICATION

---

### SECTION 0 — "JS Engine Foundation"
**Nav title:** "JS Engine Foundation"  
**Nav subtitle:** "Execution Context · Scope · Closures"

**Source files (USE IN THIS ORDER):**
1. `JS_Mastery_Module1_Module2.md` — Module 1 only (1.1 + 1.2 + 1.3)
2. `JS_Engine_Internals.md` — Sections 1, 2, 3, 4, 5 only

**Content order inside section:**
```
1. Module 1: The Execution Engine (heading-1)
   1.1 Execution Context & Call Stack
   1.2 Hoisting & Scope Chain (with TDZ)
   1.3 Closures — شنطة الذكريات

2. Going Deeper — Engine Internals (heading-1)
   2.1 Lexical Environment — المكونات الأساسية
   2.2 Variable Environment (VE) vs Lexical Environment (LE)
       → Why var uses VE, let/const use LE, TDZ explanation
   2.3 Execution Context — غرفة العمليات (مراحل الحياة)
   2.4 Call Stack — منظم المرور
   2.5 Scope Chain — رحلة البحث + Shadowing
```

**DO NOT include** from JS_Engine_Internals.md: sections 6 (Closures — already covered), 7 (Pure Functions — goes to Section 3), 8 (Immutability — goes to Section 3), 9 (Arrow Functions — goes to Section 1), 10 (eval — goes to Section 2), 11 (Currying — goes to Section 3).

---

### SECTION 1 — "OOP, Prototypes & Memory"
**Nav title:** "OOP & Memory"  
**Nav subtitle:** "Prototypes · this · Module Pattern"

**Source files (USE IN THIS ORDER):**
1. `JS_Mastery_Module1_Module2.md` — Module 2 only (2.1 + 2.2)
2. `JS_NodeJS_Elite_Vault_Part2_Modules3_4.md` — Module 3 only (3.1 through 3.6)
3. `JS_Engine_Internals.md` — Section 9 only (Arrow Functions & Lexical this)

**Content order:**
```
1. Module 2: Encapsulation & Memory Architecture (heading-1)
   2.1 The Module Pattern (Private Variables & Encapsulation)
   2.2 Memory Leaks & Closures (The Hidden Heap Killer)

2. Module 3: OOP Deep Dive (heading-1)
   3.1 Closures — The Live Link & Snapshot Trap
       NOTE: Keep this brief, reference Section 0 for foundation
   3.2 The Module Pattern (ADVANCED — Revealing Module, IIFE internals)
       NOTE: This is deeper than Module 2.1, not duplicate — show advanced patterns
   3.3 Closures & Memory Leaks — Reachability Trap in Node.js
   3.4 Prototypal Inheritance vs Classical — The Prototype Chain
   3.5 The 'this' Keyword — The 4 Rules (Implicit, Explicit, New, Default)
   3.6 Arrow Functions as Class Methods — The Anti-Pattern That Destroys Memory
   3.7 Arrow Functions & Lexical this — Deep Mechanics
       (from JS_Engine_Internals Section 9)
```

**REMOVE** from this section: the WeakRef content that was wrongly injected (lines ~1857–2038 of current index.html).

---

### SECTION 2 — "V8 Deep Internals"
**Nav title:** "V8 Deep Internals"  
**Nav subtitle:** "Memory Model · Hidden Classes · GC · WeakRef · Symbols"

**Source files (USE IN THIS ORDER):**
1. `JS_Internals_Masterclass.md` — ALL sections (1 through 6)
2. `JS_Engine_Internals.md` — Section 10 (eval) only

**Content order:**
```
1. Memory Model العميق (heading-1)
   - The 3 Memory Regions (Stack, Heap, Static/Global)
   - Stack Frame بالتفصيل
   - V8 Heap من جوه (Young/Old Generation, Map Space, Large Object Space)
   - Value vs Reference Semantics
   - الجدول النهائي: مين يروح Stack ومين يروح Heap

2. V8 Hidden Classes & Inline Caching (heading-1)
   - Dynamic Lookup المشكلة
   - Hidden Class — النسخة الخفية
   - Transition Chain
   - Inline Caching (IC) — الخدعة الأسرع
   - قواعد الـ Architect (العواقب العملية)

3. Garbage Collection Algorithms (heading-1)
   - Reachability المفهوم
   - Mark & Sweep
   - Generational GC (Young/Old)
   - Minor GC — The Scavenger
   - Major GC — Mark-Sweep-Compact
   - Incremental & Concurrent Marking
   - Write Barrier & Tri-Color Marking

4. WeakRef & FinalizationRegistry (heading-1)
   - المشكلة التي ES2021 جاء يحلها
   - WeakRef — الـ Reference الضعيفة
   - Smart Cache بـ WeakRef
   - FinalizationRegistry — خبّرني لما تمسحه
   - WeakRef vs WeakMap — إمتى تستخدم إيه؟

5. Symbols — البروتوكولات الخفية للغة (heading-1)
   - Symbol الأساسي + Global Registry
   - Well-Known Symbols (iterator, toPrimitive, hasInstance, asyncIterator, toStringTag, species)
   - بناء Protocol كامل

6. eval Execution Context (heading-1)
   (from JS_Engine_Internals.md Section 10)
   - ليه "eval is evil"؟
   - eval vs new Function()
```

---

### SECTION 3 — "Functional Programming (Full)"
**Nav title:** "Functional Programming"  
**Nav subtitle:** "Pure Functions · Compose · Memoization · Railway"

**Source files (USE IN THIS ORDER):**
1. `JS_NodeJS_Elite_Vault_Part2_Modules3_4.md` — Module 4 only (4.1 + 4.3)
2. `JS_Engine_Internals.md` — Sections 7, 8, 11 only (Pure Functions, Immutability, Currying)
3. `JS_Functional_Programming_Masterclass.md` — ALL sections (1 through 7)

**Content order:**
```
1. FP Foundations (heading-1)
   - Pure Functions & Side Effects: The Foundation of FP (from Module 4.1)
   - Immutability — الداتا المقدسة (from JS_Engine_Internals Section 8)
     → Object.freeze deep vs shallow, spread patterns
   - Higher-Order Functions (HOF): Passing Functions as Data (from Module 4.3)
   - Currying Functions — التقسيط البرمجي (from JS_Engine_Internals Section 11)
     → Mechanics, Currying vs Partial Application, Use Cases

2. FP Masterclass (heading-1)
   - Compose vs Pipe
   - Memoization Deep Dive
   - Transducers
   - Railway-Oriented Programming (Either Monad)
   - Lazy Evaluation & Infinite Sequences
   - Point-Free Style
   - Interview Survival Kit for FP
```

---

### SECTION 4 — "Node.js Foundations"
**Nav title:** "Node.js Foundations"  
**Nav subtitle:** "npm · V8 · Debugging · Security"

**Source file:** `Node.js_Interview_Prep_Arabic.md` — ALL sections

**Content order (exact from file):**
```
1. ما هو Node.js؟ (heading-1)
   - ليه Node.js سريع جداً؟
   - Single Process وعدم الـ Blocking
   - Hello World Server

2. الفرق بين Node.js والـ Browser (heading-1)
   - Ecosystem مختلف
   - التحكم في البيئة
   - CommonJS vs ES Modules (overview — details in Section 7)

3. الـ V8 JavaScript Engine في Node.js (heading-1)
   - ما هو الـ V8؟
   - V8 مش الـ DOM
   - JavaScript مش Interpreted بس!

4. npm — مدير الحزم (heading-1)
   - npm إيه؟
   - dependencies vs devDependencies
   - Versioning والـ Semver
   - الـ npm Scripts

5. ECMAScript 2015+ في Node.js (heading-1)
   - تصنيف الـ Features
   - ليه ده مهم في الإنترفيو؟

6. Debugging في Node.js (heading-1)
   - Inspector
   - Flags المهمة
   - تحذير أمني

7. Fetch API مع Undici + WebSocket (heading-1)

8. الفرق بين Development وProduction (heading-1)
   - NODE_ENV
   - ليه NODE_ENV antipattern؟

9. Profiling + WebAssembly (heading-1)

10. Security Best Practices (heading-1)
    - DoS, DNS Rebinding, HTTP Smuggling
    - Prototype Pollution, Supply Chain Attacks
    - Permission Model
```

---

### SECTION 5 — "Node.js Internals"
**Nav title:** "Node.js Internals"  
**Nav subtitle:** "C10K · libuv · Thread Pool · Buffers"

**Source file:** `NodeJS_Internals_Masterclass.md` — ALL sections

**Content order (exact from file):**
```
1. المشكلة الأصلية: C10K Problem (heading-1)
   - الكارثة اللي أنجبت نود
   - Context Switching: العدو الصامت
   - Blocking: المشكلة الجوهرية
   - الحل المقترح

2. ليه JavaScript؟ قرار Ryan Dahl (heading-1)
   - 2009: الرجل والفكرة
   - ليه JavaScript تحديدًا؟

3. تشريح المفاعل: هيكل Node.js من جوه (heading-1)
   - الثالوث المقدس (V8 + libuv + C++ Bindings)
   - Folder Structure في Source Code

4. V8 Engine في Node: الجينيوس الأعمى (heading-1)
   - JIT: Ignition → TurboFan
   - Isolates والـ Contexts
   - Garbage Collector في Node context

5. C++ Bindings: طبقة التهكير (heading-1)
   - internalBinding: بوابة النفق
   - Syscall: الطلب الرسمي للـ Kernel
   - Context Switch بين اللغتين
   - Bootstrap: إزاي Node بيحقن كل حاجة في V8

6. libuv والـ Event Loop: المدير والعمال (heading-1)
   - libuv: المصنع اللي ورا الستارة
   - Event Loop مش Loop عادي
   - Phase 1: Timers ⏱️
   - Phase 4: Poll 📡 (أهم Phase)
   - Phase 5: Check ✅
   - Microtasks: البلطجية اللي بيقاطعوا كل حاجة

7. Thread Pool vs OS Kernel (heading-1)
   - مين بيقرأ الملف فعلًا؟
   - Thread Pool: العمال الـ 4
   - OS Kernel: الجبار الشبكي

8. Buffers والـ Streams: سباكة الداتا (heading-1)
   - المشكلة: V8 Heap صغير والداتا كبيرة
   - Buffer: الميموري خارج V8
   - Zero-Copy: السحر الحقيقي
   - Streams: الماسورة اللي بتنقذ الرام
   - Backpressure: التنظيم الذاتي
   - أنواع الـ Streams الأربعة

9. الصورة الكاملة: ليه Node.js سريع؟ (heading-1)
   - الـ 5 أسباب الجوهرية

10. Interview Survival Kit — Node.js Internals (heading-1)
    - جدول المراجعة السريعة
```

---

### SECTION 6 — "Async Architecture"
**Nav title:** "Async Architecture"  
**Nav subtitle:** "Event Loop · Generators · Streams"

**Source file:** `JS_NodeJS_Elite_Vault_Part3_Modules5_6.md` — ALL of Module 5 + ALL of Module 6

**Content order:**
```
1. Module 5: The Asynchronous Brain (heading-1)
   - المايسترو الوحيد — إزاي Node.js بيخدم 10,000 مستخدم
   5.1 The Reactor Pattern: libuv & Non-Blocking I/O
   5.2 Async/Await Under the Hood: Generators, Suspend & Resume

2. Module 6: Node.js Core Architecture (heading-1)
   - قلب Node.js — EventEmitter, Streams & Backpressure
   6.1 The EventEmitter: Observer Pattern & The Zalgo Anti-Pattern
   6.3 Piping & Backpressure: Connecting Streams Without Crashing the Server
```

---

### SECTION 7 — "Module System: CJS & ESM"
**Nav title:** "Module System"  
**Nav subtitle:** "CommonJS · ESM · ENV Variables"

**Source files (USE IN THIS ORDER):**
1. `commom modules.md` — ALL sections
2. `esm modules.md` — ALL sections
3. `ENV Variables.md` — ALL sections

**Content order:**
```
PART 1: CommonJS Deep Dive (heading-1)

1. الـ Module Wrapper — الغلاف الخفي لكودك (heading-2)
   - إيه هو الـ Wrapper كـ Textual Transformation؟
   - تشريح الـ Arguments الخمسة (exports, module, require, __filename, __dirname)
   - سحر الـ .call() والـ this
   - Execution Flow: إزاي الـ String بيبقى كود؟
   - Interview Scenarios: Global Leak + Reference Break

2. رحلة الـ require(X) — خوارزمية البحث (heading-2)
   - Core Modules (أصحاب الحصانة)
   - File Modules
   - Directory as a Module
   - node_modules — رحلة الصعود للجبل
   - Interview Scenarios: Singleton Pattern + Case-Sensitivity Nightmare

3. الـ Caching — السر الكبير (heading-2)
   - ليه نود سريع وذكي؟

4. تشريح الـ module Object — هوية الموديول (heading-2)
   - module.id, module.filename, module.loaded, module.children, module.paths
   - require.main === module — الضربة القاضية
   - Interview Scenarios: Memory Leak Trace + Private Module Logic

5. خناقة الـ exports والـ module.exports (heading-2)
   - الحقيقة الصادمة (The Memory Link)
   - متى تحدث الكارثة؟ (Reassignment Trap)
   - القاعدة الذهبية
   - Interview Scenarios: Mixed Exports + Exports as a Function

6. مختبر نود — التجارب العملية (heading-2)
   - التجربة 1: كشف الـ Wrapper
   - التجربة 2: جريمة قتل الـ Reference
   - التجربة 3: إثبات الـ Singleton (الـ Cache)
   - التجربة 4: الـ Script vs Module
   - التجربة 5: الـ Circular Dependency

---

PART 2: ESM Deep Dive (heading-1)

1. Identity Crisis — إزاي نود بيعرف إنه ESM؟ (heading-2)
   - Extension (.mjs / .cjs / .js)
   - "type": "module" في package.json
   - --input-type Flag

2. الـ Parsing Phase — 3 مراحل (heading-2)
   - Construction (Fetching)
   - Instantiation (Linking)
   - Evaluation (Execution)
   - ليه import لازم في الـ Top-level

3. Live Bindings — السحر اللي بيبهر الكل (heading-2)
   - الفرق الجوهري: CJS Copy vs ESM Live Binding

4. Mandatory Extensions (heading-2)

5. import.meta — وريث العرش (heading-2)
   - إزاي نرجع __dirname و __filename

6. Top-level await — التحرر من العبودية (heading-2)
   - القوة والخطورة

7. Interoperability — خناقة الإخوة الأعداء (heading-2)
   - ESM ينادي CJS (سهلة بس غدارة)
   - CJS ينادي ESM (المهمة المستحيلة — Dynamic Import)

8. ESM Cache vs require.cache (heading-2)

9. أسئلة الإنترفيو لليفل وحش الـ ESM (heading-2)

---

PART 3: Environment Variables (heading-1)

1. الفلسفة العميقة لمتغيرات البيئة (heading-2)
   - ليه بنقسم الدنيا "Environments"؟
   - إيه هي الـ ENV Variables؟
   - الفرق بين الـ Env في Node والـ Env في Express

2. السيطرة على المتغيرات (heading-2)
   - process.env (الخزنة العالمية)
   - الحقن عبر Terminal
   - ملف .env (الاحترافية)
   - مكتبة dotenv

3. التفاصيل التقنية العميقة (heading-2)
   - Shell Variables vs Process Variables
   - ليه process متاح من غير require؟
   - الأمان في الـ Production

4. الـ Traps والاحترافية (heading-2)
   - فخ "مين ركب الأول؟" (Execution Order)
   - الـ Scripts في package.json
   - Conditional Logic
   - Cheat Sheet
```

---

### SECTION 8 — "Design Patterns & Browser APIs"
**Nav title:** "Design Patterns"  
**Nav subtitle:** "Node.js Patterns · Browser APIs"

**Source files (USE IN THIS ORDER):**
1. `JS_NodeJS_Elite_Vault_Part4_Module7.md` — ALL of Module 7
2. `Day-4 lecture  codes.md` — ALL sections

**Content order:**
```
PART 1: Node.js Design Patterns (heading-1)
(Module 7 — from JS_NodeJS_Elite_Vault_Part4_Module7.md)

7.1 Factory, Builder & Revealing Constructor
7.2 Singleton Pattern & Circular Dependencies (CommonJS vs ESM)
7.3 Structural Patterns: Proxy & Decorator
7.4 State & Command Patterns (The Mongoose Secret)
7.5 Asynchronous Request Batching (Piggybacking Pattern)
7.6 Canceling Async Operations: Generators as Supervisors
7.7 Taming the CPU: Worker Threads & Thread Pool Pattern

---

PART 2: Browser APIs (heading-1)
(from Day-4 lecture  codes.md)

1. DOM Collections (heading-2)
   - Live Collection vs Static Collection
   - متى بنستخدم دي ومتى بنستخدم دي
   - Interview Traps

2. Event Life Cycle (heading-2)
   - إيه هو الـ Event Life Cycle؟
   - Capture → Target → Bubble phases
   - e.target vs e.currentTarget vs this
   - stopPropagation()
   - مثال عملي + Mermaid Diagram
   - Interview Questions للتنانين

3. BOM: Browser Object Model (heading-2)
   - Window Object (كبير العيلة)
   - التحكم في النوافذ (open & close)
   - History Object — رحلة عبر الزمن
   - Location Object — التحكم في المكان
   - Mermaid Diagram
   - Interview Questions

4. URL API (heading-2)
   - تشريح الـ URL (Properties)
   - أهم الـ Methods
   - Mermaid Diagram
   - Interview Questions

5. Modern History API (heading-2)
   - history.pushState() + history.replaceState()
   - popstate Event
   - مثال SPA Navigation
   - Interview Questions للتنانين

6. Web Storage (heading-2)
   - Cookies (القديم المحنك)
   - localStorage (المخزن الدائم)
   - sessionStorage (خزنة التابة الواحدة)
   - مقارنة سريعة (الجدول اللي بيبهر في الإنترفيو)
   - أمثلة بالكود
   - Interview Traps
```

---

### SECTION 9 — "Q&A Gauntlet"
**Nav title:** "Q&A Gauntlet"  
**Nav subtitle:** "30 Interview Questions"

**Source file:** `JS_NodeJS_Elite_Vault_Part5_QA_Gauntlet.md` — ALL sections
**Supplement with:** `JavaScript interview preparation.md` for any questions not already in the vault file

**Content:**
```
⚔️ Module 9: The Ultimate Core JS & Async Gauntlet

🔴 Part 1: Type Coercion, JS Quirks, Truthy/Falsy & Memory Traps
   Questions 1 → 10

🟡 Part 2: ES6+ Traps, Lexical Environments & Memory
   Questions 11 → 20

🔵 Part 3: Async, Event Loop, Microtasks & Macrotasks
   Questions 21 → 30
   (Make sure 30 questions exist — add from JavaScript interview preparation.md if needed)
```

---

## PART 3: TECHNICAL EXECUTION INSTRUCTIONS

### Step 1: Read existing CSS patterns first
Before writing any HTML, read `css/styles.css` and `js/app.js` fully.
Note all these class names that you MUST use:
- `callout callout-bug` → for interview traps and questions
- `callout callout-success` → for answers
- `callout callout-abstract` → for deep concept explanations
- `callout callout-example` → for code scenarios
- `callout callout-tip` → for senior notes / professor tips
- `callout callout-question` → for bridge questions between sections
- `code-block-wrap` → wrapper for code blocks (with copy button)
- `inline-code` → for inline code
- `mermaid-wrap` → wrapper for Mermaid diagrams
- `heading-1`, `heading-2`, `heading-3` → headings
- `spacer` → spacing element `<div class="spacer"></div>`
- `divider` → horizontal rule `<hr class="divider">`
- `content-section` → each section wrapper
- `section-header` → section title area
- `section-body` → section content area

### Step 2: Update the navigation buttons
The new nav must have exactly 10 buttons (0–9):
```html
<button class="nav-btn" id="nav-0" onclick="showSection(0)">
  <span class="nav-title">JS Engine Foundation</span>
  <span class="nav-sub">Execution Context · Scope · Closures</span>
</button>
<button class="nav-btn" id="nav-1" onclick="showSection(1)">
  <span class="nav-title">OOP & Memory</span>
  <span class="nav-sub">Prototypes · this · Module Pattern</span>
</button>
<button class="nav-btn" id="nav-2" onclick="showSection(2)">
  <span class="nav-title">V8 Deep Internals</span>
  <span class="nav-sub">Memory Model · Hidden Classes · GC</span>
</button>
<button class="nav-btn" id="nav-3" onclick="showSection(3)">
  <span class="nav-title">Functional Programming</span>
  <span class="nav-sub">Pure Functions · Compose · Railway</span>
</button>
<button class="nav-btn" id="nav-4" onclick="showSection(4)">
  <span class="nav-title">Node.js Foundations</span>
  <span class="nav-sub">npm · V8 · Debugging · Security</span>
</button>
<button class="nav-btn" id="nav-5" onclick="showSection(5)">
  <span class="nav-title">Node.js Internals</span>
  <span class="nav-sub">C10K · libuv · Thread Pool · Buffers</span>
</button>
<button class="nav-btn" id="nav-6" onclick="showSection(6)">
  <span class="nav-title">Async Architecture</span>
  <span class="nav-sub">Event Loop · Generators · Streams</span>
</button>
<button class="nav-btn" id="nav-7" onclick="showSection(7)">
  <span class="nav-title">Module System</span>
  <span class="nav-sub">CommonJS · ESM · ENV Variables</span>
</button>
<button class="nav-btn" id="nav-8" onclick="showSection(8)">
  <span class="nav-title">Design Patterns</span>
  <span class="nav-sub">Node.js Patterns · Browser APIs</span>
</button>
<button class="nav-btn" id="nav-9" onclick="showSection(9)">
  <span class="nav-title">Q&A Gauntlet</span>
  <span class="nav-sub">30 Interview Questions</span>
</button>
```

### Step 3: Update app.js
In `js/app.js`, find where the total section count is defined.
Change it to 10 (sections 0–9).
Update `showSection()` to handle 10 sections.
Update TOC rendering to handle 10 sections.

### Step 4: Section HTML Template
Every section follows this EXACT structure:
```html
<section id="section-N" class="content-section" style="display:none">
  <div class="section-header">
    <h1 class="section-title">SECTION TITLE</h1>
    <p class="section-subtitle">Subtitle here</p>
  </div>
  <div class="section-body">
    <!-- content goes here -->
    <div class="spacer"></div>
    <hr class="divider">
    <div class="spacer"></div>
    <!-- ... -->
  </div>
</section>
```

Section 0 has `style="display:block"`, all others have `style="display:none"`.

### Step 5: TOC structure
Each section needs a TOC div:
```html
<div id="toc-N" class="toc-section" style="display:none">
  <a href="#heading-anchor" class="toc-link toc-level-1" style="padding-right:0px" onclick="showSection(N)">Title</a>
  <a href="#heading-anchor" class="toc-link toc-level-2" style="padding-right:14px" onclick="showSection(N)">Subtitle</a>
  <a href="#heading-anchor" class="toc-link toc-level-3" style="padding-right:28px" onclick="showSection(N)">Sub-subtitle</a>
</div>
```

TOC section 0 has `style="display:block"`, all others have `style="display:none"`.

---

## PART 4: EXECUTION STRATEGY FOR AGENTS

### Do it in this exact order (don't skip steps):

**PHASE A: Restructure existing content**
1. Fix section-0: REMOVE Memory Model content (lines ~677–976). That block starts at `<h2 id="1-memory-model-العميق"` and ends before `</section>`. DELETE it.
2. Fix section-1: REMOVE WeakRef content (lines ~1857–2038). That block starts at `<h2 id="4-weakref-finalizationregistry"` and ends before `</section>`. DELETE it.
3. Renumber sections: what was section-0 stays 0, but add new sections 2–9 and renumber old sections accordingly.

**PHASE B: Convert missing files**

**IMPORTANT for Antigravity agents:** Read each source `.md` file completely before converting it. The files are in:
- `/Resources/Nodejs/NodeJS_Internals_Masterclass.md`
- `/Resources/Nodejs/commom modules.md`
- `/Resources/Nodejs/esm modules.md`
- `/Resources/Nodejs/ENV Variables.md`
- `/Resources/Nodejs/Node.js_Interview_Prep_Arabic.md`
- `/Resources/JavaScript/Day-4 lecture  codes.md`
- `/Resources/JavaScript/JS_Engine_Internals.md` (for missing sections: 2, 7, 8, 10, 11)
- `/Resources/JavaScript/JS_Functional_Programming_Masterclass.md` (already in HTML as section-7, move it)

**PHASE C: Update navigation and app.js**
Update nav buttons to 10 sections.
Update app.js to handle 10 sections.
Update all TOC entries.

**PHASE D: Verify**
- All 10 sections exist (id="section-0" through id="section-9")
- All nav buttons work (id="nav-0" through id="nav-9")
- No broken Mermaid syntax (every mermaid block has proper opening/closing)
- No duplicate section IDs in the HTML
- TOC entries match their sections

---

## PART 5: CONVERSION RULES FOR MARKDOWN → HTML

When converting `.md` content to HTML, follow these rules:

**Headings:**
- `# Title` → `<h1 id="slug" class="heading-1">Title</h1>`
- `## Title` → `<h2 id="slug" class="heading-2">Title</h2>`
- `### Title` → `<h3 id="slug" class="heading-3">Title</h3>`
- Slug = lowercase, Arabic chars kept, spaces→hyphens, remove symbols

**Code blocks:**
```html
<div class="code-block-wrap">
  <span class="code-lang">javascript</span>
  <pre><code class="language-javascript">YOUR CODE HERE</code></pre>
  <button class="copy-btn" onclick="copyCode(this)" title="نسخ">📋</button>
</div>
```

**Inline code:** `<code class="inline-code">text</code>`

**Callouts:**
- Interview trap/question → `<div class="callout-bug callout"><div class="callout-title"><span class="callout-icon">🕵️</span><span>TITLE</span></div><div class="callout-body">CONTENT</div></div>`
- Answer → `<div class="callout-success callout"><div class="callout-title"><span class="callout-icon">✅</span><span>TITLE</span></div><div class="callout-body">CONTENT</div></div>`
- Deep concept → `<div class="callout-abstract callout"><div class="callout-title"><span class="callout-icon">🧠</span><span>TITLE</span></div><div class="callout-body">CONTENT</div></div>`
- Code example scenario → `<div class="callout-example callout"><div class="callout-title"><span class="callout-icon">💡</span><span>TITLE</span></div><div class="callout-body">CONTENT</div></div>`
- Senior tip → `<div class="callout-tip callout"><div class="callout-title"><span class="callout-icon">⚡</span><span>TITLE</span></div><div class="callout-body">CONTENT</div></div>`

**Mermaid diagrams:**
```html
<div class="mermaid-wrap">
  <div class="mermaid">
    YOUR MERMAID CODE HERE
  </div>
</div>
```

**Tables:**
```html
<div class="table-wrap">
  <table class="content-table">
    <thead><tr><th>Header</th></tr></thead>
    <tbody><tr><td>Cell</td></tr></tbody>
  </table>
</div>
```

**Between major topics, always add:**
```html
<div class="spacer"></div>
<hr class="divider">
<div class="spacer"></div>
```

**Between minor topics:**
```html
<div class="spacer"></div>
```

---

## PART 6: CONTENT TONE & STYLE RULES

1. **Language:** Egyptian Arabic mixed with English technical terms. Same voice as existing content. Not formal Arabic. Not pure English.
2. **Interview questions:** Always use `callout-bug` for the question, `callout-success` for the answer.
3. **Senior tips:** Use `callout-tip` with ⚡ icon.
4. **Every section** must start with a brief intro paragraph (2-3 lines Arabic) explaining what this section covers and why it matters.
5. **Keep existing content** exactly as-is when restructuring — don't rewrite content that's already converted correctly, just move it.

---

## SUMMARY CHECKLIST FOR AGENT

Before finishing, verify ALL of these:

- [ ] section-0: Has Module 1 (1.1, 1.2, 1.3) + Engine Internals (sections 1-5). Memory Model is REMOVED.
- [ ] section-1: Has Module 2 (2.1, 2.2) + Module 3 (3.1–3.6) + Arrow Functions deep. WeakRef is REMOVED.
- [ ] section-2: Has ALL of JS_Internals_Masterclass (Memory Model, Hidden Classes, GC, WeakRef, Symbols) + eval
- [ ] section-3: Has Module 4 FP basics + Immutability + Currying + ALL of FP Masterclass
- [ ] section-4: Has ALL of Node.js_Interview_Prep_Arabic.md
- [ ] section-5: Has ALL of NodeJS_Internals_Masterclass.md
- [ ] section-6: Has ALL of Module 5 + Module 6 (Async, EventEmitter, Streams)
- [ ] section-7: Has ALL of commom_modules.md + esm_modules.md + ENV_Variables.md
- [ ] section-8: Has ALL of Module 7 + ALL of Day-4 lecture codes.md
- [ ] section-9: Has 30 Q&A questions
- [ ] Nav has exactly 10 buttons (nav-0 through nav-9)
- [ ] TOC has exactly 10 divs (toc-0 through toc-9)
- [ ] app.js handles 10 sections
- [ ] No Memory Model content in section-0
- [ ] No WeakRef content in section-1
- [ ] All code blocks have copy buttons
- [ ] All Mermaid diagrams are wrapped in mermaid-wrap div
