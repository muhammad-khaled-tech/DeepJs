---
tags:
  - javascript
  - interview-prep
  - nodejs
  - functional-programming
  - ITI
aliases:
  - JS Engine Internals
  - محرك الجافاسكريبت
created: 2026-03-21
status: complete
---

# 🧠 JS Engine Internals — محرك الجافاسكريبت من الجذور

> [!abstract] الخريطة الكاملة
> هذه النوتة تغطي الطبقات الداخلية لمحرك الجافاسكريبت من الأسفل للأعلى:
> **LE → VE → EC → Scope Chain → Closures → Pure Functions → Immutability → Arrow Functions → Eval → Currying**

---

## 1. 📚 Lexical Environment (LE)

> [!info] التعريف
> **Data Structure داخلية** بيعملها المحرك عشان يخزن فيها المتغيرات والفانكشنز المتعرفة في "مكان" معين في الكود.
> كلمة **Lexical** = "مكاني/ترتيبي" — يعني بيتحدد بناءً على **أنت كاتب الكود فين بالظبط**.

### المكونان الأساسيان

```mermaid
graph TD
    LE["🗂️ Lexical Environment"]
    ER["📋 Environment Record\n(الجدول الحقيقي)\nx: 10\nuser: {name: 'Ali'}"]
    OR["🔗 Outer Reference\n(السلك الواصل بالـ Parent LE)"]

    LE --> ER
    LE --> OR
    OR -->|"يشاور على"| ParentLE["Lexical Environment\nالـ Parent"]
```

| المكوّن | الدور |
|---|---|
| **Environment Record** | الجدول الحقيقي اللي فيه أسماء المتغيرات وقيمها |
| **Outer LE Reference** | السلك اللي بيوصل اللي بالـ Parent — أساس الـ Scope Chain |

---

## 2. ⚙️ Variable Environment (VE) vs Lexical Environment (LE)

> [!tip] ليه فيه اتنين؟
> مع ظهور **ES6** و `let` و `const`، المحرك بقى يقسم البيئات جوه الـ Execution Context لنوعين عشان يطبق **Block Scope**.

```mermaid
graph LR
    EC["🏗️ Execution Context"]
    VE["📦 Variable Environment\nللـ var فقط\n(لا يحترم الـ Block)"]
    LE["📚 Lexical Environment\nللـ let / const / class\n(يحترم الـ Block)"]
    THIS["🎯 This Binding"]

    EC --> VE
    EC --> LE
    EC --> THIS
```

| | `var` | `let` / `const` |
|---|---|---|
| **المخزن** | Variable Environment | Lexical Environment |
| **Block Scope** | ❌ لا يعرف الـ `{}` | ✅ يحترم الـ `{}` |
| **Hoisting** | `undefined` | TDZ (Temporal Dead Zone) |

> [!example] مثال البلوك سكوب
> ```js
> {
>   var x = 1;   // يعيش في الـ VE — مرئي بره الـ Block
>   let y = 2;   // يعيش في LE جديد خاص بالـ Block ده بس
> }
> console.log(x); // 1 ✅
> console.log(y); // ReferenceError ❌
> ```

---

## 3. 🏗️ Execution Context (EC) — غرفة العمليات

> [!info] التعريف
> "الحاوية" الكبيرة اللي بتشغل الكود. **مفيش سطر كود واحد بيشتغل بره Execution Context.**

### أنواع الـ Execution Context

```mermaid
graph TD
    Types["أنواع الـ Execution Context"]
    GEC["🌍 Global EC\nبيتخلق أول ما تشغل الملف\nواحد بس طول البرنامج\nبيعمل window/global\nبيربط this بيهم"]
    FEC["🔧 Function EC\nبيتخلق كل ما تنادي فانكشن\n10 نداءات = 10 contexts"]
    EEC["⚠️ Eval EC\nنادر — لما تستخدم eval()"]

    Types --> GEC
    Types --> FEC
    Types --> EEC
```

### مراحل حياة الـ Execution Context

```mermaid
sequenceDiagram
    participant Engine as 🔧 V8 Engine
    participant Creation as 📐 Creation Phase
    participant Execution as ▶️ Execution Phase

    Engine->>Creation: بيبدأ قبل ما ينفذ أول سطر
    Creation->>Creation: 1. ينشئ LE و VE
    Creation->>Creation: 2. Hoisting (function ↑ كاملة / var ↑ undefined)
    Creation->>Creation: 3. يحدد الـ Outer Reference
    Creation->>Creation: 4. يحدد قيمة this

    Engine->>Execution: بعد الـ Creation Phase
    Execution->>Execution: يمشي سطر بسطر
    Execution->>Execution: يعطي المتغيرات قيمها الحقيقية
    Execution->>Execution: ينفذ الـ Logic والنداءات
```

---

## 4. 📚 Call Stack — منظم المرور

> [!info] الهدف
> بما إن الجافا سكريبت **Single-Threaded** (إيد واحدة بس)، الـ Call Stack هو اللي بيعرف المحرك "أنا دلوقتي في أنهي غرفة عمليات؟"
> نوعه: **LIFO — Last In, First Out**

```mermaid
graph BT
    Global["🌍 Global EC\n(دايماً في القاع)"]
    A["🔧 Function A EC"]
    B["🔧 Function B EC\n(دخلت الأخيرة، بتخرج الأول)"]

    Global --> A --> B

    style B fill:#ff6b6b,color:#fff
    style A fill:#ffa94d,color:#fff
    style Global fill:#51cf66,color:#fff
```

> [!example] الـ Stack في العمل
> ```js
> function b() { console.log("B"); }
> function a() { b(); }
> 
> // Stack:
> // [Global] → [a EC] → [b EC]  ← b تنفذ وتتشال
> //          → [a EC]            ← a تكمل وتتشال
> // [Global]                     ← يفضل لحد ما البرنامج يخلص
> ```

---

## 5. ⛓️ Scope Chain — السلم الواصل

> [!info] التعريف
> الـ **Scope Chain** هي النتيجة المنطقية للـ **Outer References** المتسلسلة. كل LE بيشاور على اللي فوقيه، وده بيعمل "سلم" يقدر المحرك يتسلقه عشان يلاقي المتغيرات.

### كيف تتبنى السلسلة؟

```mermaid
graph TD
    GlobalLE["🌍 Global LE\nouter → null\n[x: 10, a: fn]"]
    ALE["🔧 Function A LE\nouter → Global LE\n[y: 20, b: fn]"]
    BLE["🔧 Function B LE\nouter → A LE\n[z: 30]"]

    BLE -->|"outer ref"| ALE
    ALE -->|"outer ref"| GlobalLE
    GlobalLE -->|"outer ref"| NULL["null 🔚"]

    style NULL fill:#dee2e6
```

> [!warning] مبني على **مكان الكتابة** مش مكان النداء!
> الـ Outer Reference بيتحدد وقت **Definition** (لما كتبت الكود)، مش وقت **Execution** (لما ناديت الفانكشن).
> ده اللي بنسميه **Static / Lexical Scoping**.

### رحلة البحث (Identifier Resolution)

```mermaid
flowchart LR
    Start(["🔍 بحث عن x"]) --> Local{"في الـ Local LE؟"}
    Local -->|"✅ نعم"| Found(["✅ خلاص!"])
    Local -->|"❌ لا"| Outer{"في الـ Outer LE؟"}
    Outer -->|"✅ نعم"| Found
    Outer -->|"❌ لا"| Global{"في الـ Global LE؟"}
    Global -->|"✅ نعم"| Found
    Global -->|"❌ لا"| Error(["💥 ReferenceError:\nx is not defined"])
```

### ⚔️ Scope Chain vs Call Stack

| | Call Stack | Scope Chain |
|---|---|---|
| **يحدد** | ترتيب التنفيذ (مين نادى مين؟) | الوصول للبيانات (مين يشوف مين؟) |
| **مبني على** | وقت النداء (Runtime) | وقت الكتابة (Lexical/Static) |
| **مثال** | `a()` → `b()` → Stack | `b` كُتبت جوه `a` → يرث Scope |

### الـ Shadowing

> [!example] لو عندك `x` local و`x` global
> ```js
> let x = "global";
> function test() {
>   let x = "local"; // عمل Shadow على الـ Global x
>   console.log(x);  // "local" — المحرك وقف هنا ومكملش
> }
> test();
> ```

---

## 6. 🔒 Closures — الذاكرة الممتدة

> [!abstract] التعريف الدقيق
> **Closure** = دالة + الـ Lexical Environment اللي اتولدت فيه.
> هي قدرة الدالة الداخلية على **تذكر** والوصول لمتغيرات الـ Parent Scope حتى بعد ما الـ Parent خلص تنفيذه.

### الميكانيكا

```mermaid
sequenceDiagram
    participant Outer as 🏭 Outer Function
    participant LE as 📚 Lexical Environment
    participant Inner as 🔒 Inner Function (Closure)
    participant GC as 🗑️ Garbage Collector

    Outer->>LE: تنشئ الـ LE وتخزن فيه المتغيرات
    Outer->>Inner: تنشئ وترجع الـ Inner Function
    Outer-->>Outer: الـ EC بتاعها بيتشال من الـ Call Stack
    GC->>LE: "هحذفك!"
    Inner->>LE: أنا لسه شايله بالـ Outer Reference!
    GC-->>LE: ماقدرش أحذفه 😤

    Note over LE,Inner: الـ LE بيفضل حي في الميموري\nطالما الـ Closure موجودة
```

> [!example] مصنع العدادات
> ```js
> function makeCounter() {
>   let count = 0; // هيفضل محبوس في الـ LE
>
>   return function() {
>     count++;
>     return count;
>   };
> }
>
> const counter1 = makeCounter(); // LE خاص بـ counter1
> const counter2 = makeCounter(); // LE خاص بـ counter2 (منفصل!)
>
> counter1(); // 1
> counter1(); // 2
> counter2(); // 1 ← بيبدأ من الأول لأن LE منفصل
> ```

### فوائد الـ Closures

| الفائدة | الشرح |
|---|---|
| **Data Privacy** | متغيرات مش يقدر حد يوصلها من بره (زي الـ private fields) |
| **State Management** | ذاكرة خاصة للفانكشن من غير متغيرات Global |
| **Function Factories** | توليد دوال متخصصة (زي الـ Currying) |

> [!caution] الثمن: Memory Leaks
> الـ Closures بتمنع الـ Garbage Collector من مسح الـ LE القديمة. عمل آلاف الـ Closures من غير داعٍ = استهلاك ذاكرة كبير.

---

## 7. 🧼 Pure Functions والـ Side Effects

### شروط الـ Pure Function

```mermaid
graph LR
    Pure["✅ Pure Function"]
    D["1️⃣ Determinism\nنفس المدخلات → نفس النتيجة\nدايماً وأبداً"]
    NS["2️⃣ No Side Effects\nمش بتغير أي حاجة بره نفسها"]

    Pure --> D
    Pure --> NS
```

### إيه هو الـ Side Effect؟

> [!warning] أي تغيير بيحصل **بره** حدود الفانكشن
> - تعديل متغير Global
> - `console.log()` ← نعم، حتى دي!
> - الكتابة في ملف أو Database
> - الـ HTTP Requests
> - نداء فانكشن تانية Impure

> [!example] Pure vs Impure
> ```js
> // ❌ Impure — بتعدل في حاجة بره
> let total = 0;
> function addToTotal(n) {
>   total += n; // Side Effect!
> }
>
> // ✅ Pure — بترجع قيمة جديدة بس
> function add(a, b) {
>   return a + b;
> }
> ```

### استراتيجية العزل (الحل الواقعي)

```mermaid
graph TD
    App["🏗️ التطبيق"]
    Pure["🧼 Pure Core\nكل الـ Logic والحسابات\nسهل الـ Testing\nمفيش DB / Side Effects"]
    Impure["🪣 Impure Shell\nالـ Controllers\nالـ DB Calls\nالـ HTTP Requests"]

    App --> Pure
    App --> Impure
    Pure <-->|"Data فقط"| Impure
```

### فوائد الـ Pure Functions

| الفائدة | الشرح |
|---|---|
| **Predictability** | `add(2,2)` = 4 دايماً |
| **Testability** | مش محتاج Mock للـ DB |
| **Parallelism** | مفيش Race Conditions |
| **Memoization** | تقدر تـ Cache النتيجة |

---

## 8. 🧊 Immutability — الداتا المقدسة

> [!abstract] المبدأ
> بمجرد ما الـ Data Structure تتخلق، **ممنوع تعدلها**. لو محتاج تغيير، خد **نسخة جديدة** وعدل فيها.

### التشبيه: السبورة ضد الكراسة

```mermaid
graph LR
    Mutable["🖊️ Mutable\n(السبورة)\nبتكتب وتمسح\nفي نفس المكان\n⚠️ Race Conditions"]
    Immutable["📓 Immutable\n(الكراسة)\nبتقلب صفحة\nوتكتب نسخة جديدة\n✅ الأصل محفوظ"]
```

> [!caution] فخ الـ Reference في الجافاسكريبت
> ```js
> const user = { name: "Ali" };
> const admin = user; // مش نسخة — نفس الـ Reference!
>
> admin.name = "Mohamed";
> console.log(user.name); // "Mohamed" 😱
> // الاتنين بيشاوروا على نفس المكان في الميموري!
> ```

### الطريقة الصح (Modern Immutability)

```js
// ✅ تعديل Object — نسخة جديدة
const user = { id: 1, name: "Ali" };
const updatedUser = { ...user, name: "Mohamed" };

// ✅ إضافة لـ Array — array جديدة
const list = [1, 2, 3];
const newList = [...list, 4];

// ✅ حذف من Array
const withoutFirst = list.filter(item => item !== 1);

// ✅ تعديل عنصر في Array
const updated = list.map(item => item === 2 ? 99 : item);
```

> [!warning] Methods بتغير الأصل — تجنبها في الـ FP
> `push`, `pop`, `splice`, `sort`, `reverse`, `shift`, `unshift`

### فوائد الـ Immutability

| الفائدة | الشرح |
|---|---|
| **Predictability** | مفيش فانكشن بتغير داتا من وراك |
| **Time Travel Debugging** | كل نسخة محفوظة = تقدر ترجع لأي حالة سابقة (Redux DevTools) |
| **Change Detection** | المحرك بيقارن الـ Reference بس، مش بيلف جوه الـ Object كله (React) |

> [!quote] زتونة الإنترفيو
> "الـ Immutability هي المبدأ اللي بيمنع الـ Side Effects الناتجة عن تعديل الـ State بشكل مباشر. بدلاً من الـ Mutation، دايماً بننشئ New Copies من البيانات، وده بيضمن إن البيانات تفضل Predictable ويسهل تتبع الـ Bugs."

---

## 9. ➡️ Arrow Functions والـ Lexical `this`

> [!info] مش بس اختصار في الكتابة!
> الـ Arrow Functions فيها ميكانيكا داخلية **مختلفة تماماً** عن الـ Regular Functions فيما يخص `this`.

### المقارنة الجوهرية

```mermaid
graph TD
    Regular["🔧 Regular Function"]
    Arrow["➡️ Arrow Function"]

    Regular -->|"this binding"| Dynamic["Dynamic this\nبيتحدد وقت الـ Call\nبناءً على مين نادى"]
    Arrow -->|"this binding"| Lexical["Lexical this\nبيتحدد وقت الـ Definition\nبيبص في الـ Outer Scope"]
```

### الميكانيكا

```mermaid
flowchart LR
    ArrowFn["➡️ Arrow Function\nطلبت this"] --> HasOwn{"عندها this\nخاصة؟"}
    HasOwn -->|"❌ لا"| Lookup["تعاملها كأي متغير\nوتدور عليها في\nالـ Outer Lexical Scope"]
    Lookup --> Found["✅ وجدت this\nبتاعة الـ Parent"]
```

> [!example] المشكلة الكلاسيكية وحلها
> ```js
> const obj = {
>   name: "Ali",
>
>   // ❌ Regular Function — this بتتغير حسب الـ Call
>   greetRegular: function() {
>     setTimeout(function() {
>       console.log(this.name); // undefined! this هنا = window/undefined
>     }, 100);
>   },
>
>   // ✅ Arrow Function — this بتجيب من الـ Parent (obj)
>   greetArrow: function() {
>     setTimeout(() => {
>       console.log(this.name); // "Ali" ✅
>     }, 100);
>   }
> };
> ```

> [!warning] الـ Arrow Functions لا تملك
> - `this` خاصة بيها
> - `arguments` object
> - `super`
> - لا تصلح كـ Constructor (مش تقدر تعمل `new ArrowFn()`)

---

## 10. ⚠️ Eval Execution Context — الخيمة الدخيلة

> [!danger] eval is evil
> `eval()` بتاخد **String** وبتنفذه كأنه كود JS حقيقي. خطير جداً.

### ليه بيقولوا "eval is evil"؟

```mermaid
graph TD
    Eval["⚠️ eval()"]
    Perf["🐢 Performance Loss\nالـ V8 بيوقف كل الـ Optimizations\nلأنه مش عارف الـ eval هيضيف إيه\nقبل ما يشغله"]
    Sec["🔓 Security Risks\nلو الـ input جاي من اليوزر\nيقدر يبعت كود خبيث\n(XSS / Code Injection)"]
    Scope["🌀 Scope Violation\nبيقدر يضيف / يعدل متغيرات\nفي الـ Local Scope اللي جوه فيه\nويكسر الـ Lexical Scope الثابت"]

    Eval --> Perf
    Eval --> Sec
    Eval --> Scope
```

> [!tip] الـ Strict Mode بيحسن الموضوع شوية
> ```js
> 'use strict';
> eval("var secret = 42"); // في الـ Strict Mode بيعمل LE منفصل
> console.log(secret);     // ReferenceError ✅ — مش هيظهر بره
> ```

### الـ eval vs new Function()

| | `eval()` | `new Function()` |
|---|---|---|
| **الـ Outer Reference** | بيشاور على الـ Local Scope اللي جواه | دايماً بيشاور على الـ Global LE |
| **الخطورة** | أعلى — يقدر يعدل في المتغيرات المحلية | أأمن — معزول عن الـ Local |
| **الاستخدام** | تجنب تماماً | مقبول في أدوات محددة جداً |

> [!quote] القاعدة الذهبية
> "Never use eval unless you are building a compiler or a very specific dev tool."

---

## 11. 🍛 Currying Functions — التقسيط البرمجي

> [!abstract] التعريف
> تحويل فانكشن بتاخد كذا Parameter: `f(a, b, c)`
> لسلسلة من الفانكشنز كل واحدة بتاخد **Parameter واحد بس**: `f(a)(b)(c)`

### الميكانيكا (مبنية على Closures)

```mermaid
sequenceDiagram
    participant Call1 as f(a)
    participant LE1 as LE1: {a: قيمة}
    participant Call2 as f(a)(b)
    participant LE2 as LE2: {b: قيمة}
    participant Call3 as f(a)(b)(c)

    Call1->>LE1: تخزن a وترجع fn2
    Note over LE1: Closure على a
    Call2->>LE2: تخزن b (بتشوف a من LE1)
    Note over LE2: Closure على a و b
    Call3->>Call3: بتشوف a و b عبر الـ Scope Chain\nوبترجع النتيجة النهائية
```

> [!example] مثال عملي — حساب الضرائب
> ```js
> // Curried Function
> const calculateTax = rate => price => price + (price * rate);
>
> // Partial Application — نثبت الـ rate
> const egyptTax = calculateTax(0.14); // Closure قفشت في 0.14
> const vatTax   = calculateTax(0.05); // Closure قفشت في 0.05
>
> // نستخدمهم بعدين براحتنا
> egyptTax(100); // 114
> vatTax(100);   // 105
> egyptTax(500); // 570
> ```

### Currying vs Partial Application

| | Currying | Partial Application |
|---|---|---|
| **التعريف** | كل فانكشن بتاخد **1** parameter بالظبط | بتثبت **أي عدد** من الـ parameters |
| **الشكل** | `f(a)(b)(c)` | `f(a, b)(c)` أو `f(a)(b, c)` |
| **الأصل** | مفهوم رياضي صارم | تطبيق عملي مرن |

### فوائد الـ Currying

| الفائدة | الشرح |
|---|---|
| **Code Reusability** | فانكشن عامة → دوال متخصصة |
| **Composition** | قطع ليغو تتركب مع بعض |
| **Declarative Code** | بتقول "إيه" مش "إزاي" |

> [!quote] زتونة الإنترفيو
> "الـ Currying هو تحويل دالة متعددة الوسائط لسلسلة من الدوال أحادية الوسيط. يعتمد كلياً على الـ Closures للحفاظ على الوسائط السابقة. فائدته في الـ Code Reusability وخلق دوال متخصصة من دوال عامة."

---

## 🗺️ الخريطة الكاملة — كل المفاهيم مع بعض

```mermaid
graph TD
    EC["🏗️ Execution Context\n(غرفة العمليات)"]
    LE["📚 Lexical Environment\n(القاموس الحديث)"]
    VE["📦 Variable Environment\n(القاموس القديم)"]
    THIS["🎯 This Binding"]
    CHAIN["⛓️ Scope Chain\n(السلم الواصل)"]
    CLOSURE["🔒 Closure\n(الذاكرة الممتدة)"]
    PURE["🧼 Pure Functions"]
    IMMUT["🧊 Immutability"]
    CURRY["🍛 Currying"]
    ARROW["➡️ Arrow Functions"]
    STACK["📚 Call Stack"]

    EC --> LE
    EC --> VE
    EC --> THIS
    LE -->|"Outer References"| CHAIN
    CHAIN -->|"السر الأعظم"| CLOSURE
    CLOSURE -->|"تمكّن"| CURRY
    PURE -->|"مبدأ مكمل"| IMMUT
    ARROW -->|"بتستخدم"| CHAIN
    STACK -->|"بيدير"| EC

    style EC fill:#4263eb,color:#fff
    style CLOSURE fill:#e64980,color:#fff
    style CHAIN fill:#0ca678,color:#fff
    style CURRY fill:#f76707,color:#fff
```

---

## 📋 ملخص الإنترفيو السريع

| المفهوم | الجملة السحرية |
|---|---|
| **LE** | قاموس المتغيرات = Environment Record + Outer Reference |
| **EC** | الحاوية = LE + VE + This Binding، بمرحلتين: Creation ثم Execution |
| **Scope Chain** | سلم الـ Outer References، مبني على مكان الكتابة مش النداء |
| **Closure** | الدالة الداخلية تحافظ على الـ LE بتاع الـ Parent حتى بعد موته |
| **Pure Functions** | نفس Input → نفس Output، من غير Side Effects |
| **Immutability** | بدل الـ Mutation، خد نسخة جديدة بالـ Spread Operator |
| **Arrow + this** | مفيش this خاصة — بتجيبها من الـ Outer Scope |
| **eval** | بيكسر الـ Lexical Scope ويوقف الـ Optimizations — تجنبه |
| **Currying** | `f(a,b,c)` → `f(a)(b)(c)` بالاعتماد على الـ Closures |

---

*📌 لينكات ذات صلة:*
- [[Node.js Interview Prep]]
- [[AWS CLF-C02 Notes]]
- [[DSA Roadmap]]
