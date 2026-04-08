# Node.js Internals — أسئلة الإنترفيو (Junior / Mid-level)

> 20 سؤال من الأكتر تكراراً في الإنترفيوهات — مرتّبين من السهل للصعب.

---

## 🟢 Junior Level (12 سؤال)

---

### س١ — إيه هو الـ Event Loop في Node.js وليه هو مهم؟

> الـ Event Loop هو الـ control structure الوحيد اللي بيشتغل في الـ single thread بتاع Node.js. مهمته إنه يراقب 3 حاجات: الـ pending timers (setTimeout/setInterval)، الـ OS tasks (HTTP servers)، والـ Thread Pool operations (fs, crypto). لما أي operation منهم تخلص، هو اللي بيشغّل الـ callback الخاص بيها. مهم لأن فهمه بيساعدك تعرف ليه الكود بيتسلسل بشكل معين وازاي تتجنب الـ blocking.

---

### س٢ — إيه الفرق بين Synchronous وAsynchronous في Node.js؟

> الـ Synchronous code بيتشغّل سطر بسطر وبيحجب الـ Event Loop — يعني لو عندك `while` loop بتاخد 5 ثواني، السيرفر مش هيرد على أي request تاني في الـ 5 ثواني دول. الـ Asynchronous code بيبدأ operation (زي قراءة ملف)، وبدل ما ينتظر، بيكمّل الشغل ولما الـ operation تخلص بيشغّل الـ callback. ده اللي بيخلي Node.js يقدر يخدم requests كتيرة في نفس الوقت.

---

### س٣ — إيه الفرق بين `setTimeout` و`setImmediate`؟

> `setTimeout(fn, 0)` بيضيف الـ callback في الـ Step 1 من الـ Event Loop (بعد ما الـ timers تخلص). `setImmediate(fn)` بيشتغل في الـ Step 4 — بعد الـ I/O callbacks وقبل الـ timers في الـ iteration الجاية. عملياً لو استخدمتهم برّه أي I/O callback، الـ order مش مضمون. بس لو جوّه I/O callback، `setImmediate` دايماً هيشتغل قبل `setTimeout`.

```javascript
const fs = require('fs');

fs.readFile(__filename, () => {
  setTimeout(() => console.log('setTimeout'), 0);
  setImmediate(() => console.log('setImmediate'));
  // setImmediate دايماً أول جوّه I/O callback ✅
});
```

---

### س٤ — إيه الفرق بين `fs.readFile` و`fs.readFileSync`؟

> `fs.readFileSync` بتحجب الـ Event Loop كاملاً لحد ما الملف يتقرأ — يعني لو الملف كبير، السيرفر واقف مش بيعمل أي حاجة تانية. `fs.readFile` async بتبعت الطلب للـ Thread Pool وترجع فوراً للـ Event Loop. لما الملف يتقرأ، بتشغّل الـ callback. في production servers، دايماً استخدم الـ async version إلا في حالات startup زي قراءة config file.

```javascript
// ❌ بتحجب الـ Event Loop — متستخدمهاش في servers
const data = fs.readFileSync('file.txt', 'utf8');

// ✅ async — مش بتحجب حاجة
fs.readFile('file.txt', 'utf8', (err, data) => {
  console.log(data);
});
```

---

### س٥ — ليه لما بتعمل `app.listen(3000)` البرنامج مش بيخرج تلقائياً؟

> لأن `app.listen()` بتضيف entry في الـ `pendingOSTasks` array داخل الـ Event Loop. الـ `shouldContinue()` function بتشوف إن فيه OS task نشط (الـ HTTP server بيستنّى connections)، فبيفضل الـ Event Loop شغّال. البرنامج بيخرج بس لما الـ arrays التلاتة تبقى فاضية — pending timers, OS tasks, وThread Pool operations.

---

### س٦ — إيه هو الـ Callback وإيه مشكلته؟

> الـ Callback هو function بتبعته كـ argument لـ function تانية، وبيتشغّل لما operation تخلص. المشكلة هي "Callback Hell" — لما بتعمل nested callbacks كتيرة الكود بيبقى شبه مثلث وصعب القراءة والـ error handling.

```javascript
// ❌ Callback Hell
fs.readFile('a.txt', (err, a) => {
  fs.readFile('b.txt', (err, b) => {
    fs.readFile('c.txt', (err, c) => {
      // الكود بقى مثلث وصعب يتقرأ 😵
    });
  });
});

// ✅ async/await — أوضح بكتير
async function readAll() {
  const a = await fs.promises.readFile('a.txt', 'utf8');
  const b = await fs.promises.readFile('b.txt', 'utf8');
  const c = await fs.promises.readFile('c.txt', 'utf8');
}
```

---

### س٧ — إيه الفرق بين Promise و`async/await`؟

> `async/await` مبنية فوق Promises — مش بديل مختلف، هي syntax sugar. الـ `async` function دايماً بترجع Promise. الـ `await` بتوقّف execution الـ function (مش الـ Event Loop!) لحد ما الـ Promise تخلص. الميزة إن الكود بيبقى أسهل في القراءة وبتقدر تستخدم `try/catch` عادي بدل `.catch()`.

```javascript
// Promise style
fetchUser(id)
  .then(user => fetchPosts(user.id))
  .then(posts => console.log(posts))
  .catch(err => console.error(err));

// async/await style — نفس الحاجة، أوضح
async function getUserPosts(id) {
  try {
    const user  = await fetchUser(id);
    const posts = await fetchPosts(user.id);
    console.log(posts);
  } catch (err) {
    console.error(err);
  }
}
```

---

### س٨ — هل Node.js single-threaded فعلاً؟

> الإجابة: صح وغلط في نفس الوقت. الـ Event Loop نفسه single-threaded — كل الـ JavaScript code بتاعك بيشتغل في thread واحد. بس libuv بتعمل Thread Pool بـ 4 threads افتراضياً للـ I/O الـ expensive زي `fs` وـ `crypto`. وكمان الـ OS نفسه بيتولّى الـ network operations. يعني الـ Node.js process كلها فيها multiple threads، بس الـ JS execution نفسه single-threaded.

```
Node.js Process:
┌──────────────────────────────────────────────────┐
│  Event Loop Thread (JS code runs here — 1 only)  │
├──────────────────────────────────────────────────┤
│  Thread Pool (libuv — 4 threads by default)      │
│   T1: fs.readFile    T2: crypto.pbkdf2           │
│   T3: dns.lookup     T4: available               │
└──────────────────────────────────────────────────┘
```

---

### س٩ — إيه هو `process.nextTick()` وامتى تستخدمه؟

> `process.nextTick()` بيشغّل الـ callback في آخر الـ current operation، قبل ما الـ Event Loop يكمل للـ tick الجاي. ده بيخليه أسرع من `setImmediate` و`setTimeout`. بتستخدمه لما تحتاج حاجة تتشغّل async بس في أسرع وقت ممكن — زي مثلاً في constructors لما تعمل emit لـ event بعد ما الـ user يقدر يعمل listen ليه.

```javascript
// ← ترتيب التشغيل:
process.nextTick(() => console.log('1 — nextTick'));     // أول حاجة
Promise.resolve().then(() => console.log('2 — promise')); // تاني
setImmediate(() => console.log('3 — setImmediate'));      // تالت
setTimeout(() => console.log('4 — setTimeout'), 0);      // رابع
```

> ⚠️ **انتبه:** لو استخدمت `process.nextTick()` في loop ممكن تحجب الـ Event Loop كاملاً، لأنه بيشتغل قبل أي I/O.

---

### س١٠ — إيه هو الـ Thread Pool في Node.js ومين بيستخدمه؟

> الـ Thread Pool هو مجموعة من الـ threads (4 افتراضياً) اللي libuv بتعملها لتشغيل الـ expensive operations بعيداً عن الـ Event Loop. تقدر تغيّر الحجم بـ environment variable.

```javascript
// ← غيّر حجم الـ Thread Pool (لازم يكون أول سطر في البرنامج)
process.env.UV_THREADPOOL_SIZE = 8;

// Functions بتستخدم Thread Pool ✅
const fs     = require('fs');      // كل fs operations
const crypto = require('crypto');  // pbkdf2, randomBytes
const dns    = require('dns');     // dns.lookup (مش dns.resolve)

// Functions مش بتستخدمه ❌ (بتتعامل مع OS مباشرة)
const https = require('https');   // network → OS يتولّاها
const net   = require('net');     // TCP → OS يتولّاها
```

---

### س١١ — إيه اللي بيحصل لو عملت blocking code في الـ Event Loop؟

> الـ Event Loop بيتجمّد كاملاً. يعني لو عندك `while` loop بتدور لـ 5 ثواني في route handler، السيرفر مش هيقدر يرد على أي request تاني في الـ 5 ثواني دول.

```javascript
// ❌ Blocking — بيوقّف الـ server كامل!
app.get('/bad', (req, res) => {
  const start = Date.now();
  while (Date.now() - start < 5000) {} // ← 5 ثواني blocking
  res.send('done');
});

// ✅ Non-blocking — الـ Event Loop فاضي يشتغل على requests تانية
app.get('/good', (req, res) => {
  crypto.pbkdf2('a', 'b', 100_000, 512, 'sha512', () => {
    // ← بيتعمل في Thread Pool، مش في الـ Event Loop
    res.send('done');
  });
});
```

---

### س١٢ — إيه الفرق بين `require` و`import`؟

> `require` هو نظام CommonJS — synchronous، بيشتغل في أي مكان في الكود، وبتقدر تعمله conditionally. `import` هو ES Modules — static (الـ imports بيتحلوا وقت الـ parsing مش الـ runtime)، وبيدعم الـ tree-shaking. في Node.js الحديثة، الاتنين شغّالين.

| | `require` (CommonJS) | `import` (ES Modules) |
|---|---|---|
| التوقيت | Runtime (synchronous) | Parse time (static) |
| Conditional | ✅ ممكن | ❌ مش ممكن |
| Tree-shaking | ❌ | ✅ |
| الـ Extension | `.js` / `.cjs` | `.mjs` أو `"type": "module"` |
| مناسب لـ | معظم الـ Node.js projects | Modern ESM projects |

---

## 🔵 Mid-level (8 أسئلة)

---

### س١٣ — اشرح الفرق بين `pendingOSTasks` والـ `pendingOperations` في الـ Event Loop.

> `pendingOSTasks` بتتبّع الـ tasks اللي الـ OS بيعملها مباشرة — زي HTTP servers اللي بتستنّى connections أو TCP connections. الـ OS نفسه بيتولّى الشغل ومفيش thread من الـ pool بيتحجز. `pendingOperations` بتتبّع الـ tasks اللي شغّالة في الـ Thread Pool بتاع libuv — زي قراءة ملف أو حساب hash. الفرق الجوهري: الـ OS tasks مش ليها limit (الـ OS بيقرر)، أما الـ Thread Pool فـ limited بعدد الـ threads.

```javascript
// pendingOSTasks — الـ OS يتولّى، مش Thread Pool
https.request('https://google.com', cb).end(); // ← OS handles it

// pendingOperations — Thread Pool
fs.readFile('file.txt', cb);       // ← Thread Pool
crypto.pbkdf2('a','b',100000,512,'sha512', cb); // ← Thread Pool
```

---

### س١٤ — ليه تشغيل 6 `pbkdf2` calls في نفس الوقت على Dual-Core machine بياخد ~2s بدل 1s؟

> لأن الـ default Thread Pool عنده 4 threads. الـ 4 threads بتتوزّع على الـ 2 cores — كل core بيشتغل على 2 threads في نفس الوقت (multi-threading/hyperthreading). كل core بيعمل ضعف الشغل في نفس الوقت، فبياخد ضعف الوقت. الـ 4 calls الأوائل بياخدوا ~2s، وبعدين الـ 2 المتبقيين بياخدوا ~1s لأن عندهم threads لوحدهم.

```
Dual-Core + 4 Threads:

Core 1: [Thread 1 (hash)] [Thread 2 (hash)]  ← اتنين في نفس الوقت = double time
Core 2: [Thread 3 (hash)] [Thread 4 (hash)]  ← اتنين في نفس الوقت = double time

النتيجة:
  Call 1-4: ~2000ms  (كل core عمل ضعف الشغل)
  Call 5-6: ~3000ms  (استنّوا thread يفضى)

لو UV_THREADPOOL_SIZE = 2:
  Call 1-2: ~1000ms  ✅ (thread واحد لكل core)
  Call 3-4: ~2000ms
  Call 5-6: ~3000ms
```

---

### س١٥ — إيه هو الـ Clustering وامتى تستخدمه؟

> الـ Clustering بيشغّل multiple instances من الـ Node.js application — كل instance في process منفصلة بـ Event Loop منفصل. بتستخدمه لما عندك CPU-intensive operations في request handlers وعايز تخدم multiple requests بشكل concurrent. الـ Rule of Thumb: عدد الـ children = عدد الـ CPU cores.

```javascript
const cluster = require('cluster');
const os      = require('os');
const express = require('express');

if (cluster.isMaster) {
  // ← Master: مهمته بس يعمل children
  const numCPUs = os.cpus().length; // ← الرقم الأمثل
  for (let i = 0; i < numCPUs; i++) {
    cluster.fork(); // ← كل fork = instance جديدة من السيرفر
  }

  cluster.on('exit', () => cluster.fork()); // ← auto-restart لو مات

} else {
  // ← Children: دول اللي بيشتغلوا كـ HTTP servers فعلاً
  const app = express();
  app.get('/', (req, res) => res.send(`Worker ${process.pid}`));
  app.listen(3000);
}
```

---

### س١٦ — ليه زيادة عدد الـ Cluster workers أكتر من عدد الـ CPU cores بتبطّئ التطبيق؟

> الـ CPU عنده طاقة معالجة ثابتة. لو عندك 4 cores وعملت 8 workers، الـ OS بيضطر يعمل context switching بين الـ 8 processes على الـ 4 cores. الـ context switching نفسه بياخد وقت وموارد. النتيجة إن كل request بياخد وقت أطول لأن الـ CPU بيشتّت تركيزه.

```
Benchmark على Dual-Core:

2 concurrent requests:
  2 Workers  → ~1000ms ✅  (كل core شغّال على worker واحد)
  6 Workers  → ~3500ms ❌  (الـ OS بيبدّل بين 3 workers على كل core)

6 concurrent requests:
  2 Workers  → ~3000ms (batch processing — 2 في المرة)
  6 Workers  → ~3500ms (كلهم مع بعض بس بطيئين بسبب context switching)
```

---

### س١٧ — إيه الفرق بين Clustering وWorker Threads؟ وامتى تختار أي منهم؟

> الـ Clustering بيعمل multiple processes — كل process معزولة وليها memory منفصلة وEvent Loop منفصل. الـ Worker Threads بتعمل multiple threads في نفس الـ process — بيشاركوا الـ memory وبيتواصلوا بشكل أسرع.

| | Clustering | Worker Threads |
|---|---|---|
| الـ Isolation | Process منفصلة كاملة ✅ | Thread في نفس الـ Process |
| الـ Memory | منفصلة لكل process | مشتركة (SharedArrayBuffer) |
| الـ Crash | مش بيأثر على غيره ✅ | ممكن يأثر على الـ process |
| الـ Stability | Production-ready ✅ | Newer, less battle-tested |
| مناسب لـ | HTTP servers, I/O | CPU-intensive pure JS |

```javascript
// Worker Threads — للـ pure JS heavy computation
const { Worker, isMainThread, parentPort } = require('worker_threads');

if (isMainThread) {
  const worker = new Worker(__filename); // ← شغّل نفس الملف كـ worker
  worker.on('message', result => console.log('Result:', result));
  worker.postMessage({ task: 'compute' }); // ← ابعت شغل للـ worker
} else {
  parentPort.on('message', (data) => {
    let count = 0;
    for (let i = 0; i < 1_000_000_000; i++) count++; // ← heavy computation
    parentPort.postMessage(count); // ← ابعت النتيجة للـ main thread
  });
}
```

---

### س١٨ — إيه اللي بيحصل خطوة بخطوة لما تكتب `https.request('https://google.com', cb)`؟

> ١) الـ Node.js بتمرر الـ request لـ libuv. ٢) libuv بتشوف إن ده network operation وبتتواصل مع الـ OS مباشرة. ٣) الـ OS بيعمل الـ TCP connection وبيبعت الـ HTTP request في الـ background بدون ما تمسّ الـ Thread Pool. ٤) الـ Event Loop بيضيف الـ operation في الـ `pendingOSTasks`. ٥) لما الـ response يجي، الـ OS بيخبر libuv. ٦) الـ callback بيتشغّل في الـ Step 2 من الـ Event Loop tick.

```
https.request('https://google.com', cb)
         ↓
      libuv (C++)
         ↓
   Operating System      ← مش Thread Pool!
         ↓
   TCP Connection
         ↓
   HTTP Request sent
         ↓
   [waiting... waiting...]    ← Event Loop فاضي يشتغل على حاجات تانية
         ↓
   Response arrives
         ↓
   OS notifies libuv
         ↓
   callback → Event Loop Step 2
         ↓
   cb() runs ✅
```

---

### س١٩ — إزاي pm2 بتساعد في الـ production وإيه مميزاتها عن الـ Clustering اليدوي؟

> pm2 بتوفّر: Auto-restart لو أي child process انهار، Load balancing تلقائي، Zero-downtime reloads، Log management مركزي، وMonitoring dashboard.

```bash
# ← تشغيل مع clustering (0 = عدد الـ CPUs تلقائياً)
pm2 start index.js -i 0

# ← شوف الـ processes الشغّالة
pm2 list

# ← Dashboard حي مع metrics
pm2 monit

# ← Logs لكل الـ workers مع بعض
pm2 logs

# ← Zero-downtime restart (بيبدّل workers واحدة واحدة)
pm2 reload index

# ← وقّف كل حاجة
pm2 delete index
```

> **نصيحة الخبراء:** في الـ production، استخدم `pm2 start index.js -i 0` على server بـ 8 cores وهيعمل 8 workers تلقائياً. أحسن بكتير من إنك تكتب الـ Clustering logic بإيدك.

---

### س٢٠ — لو عندك route بيستقبل صورة ويعمل image processing ثقيل، إيه أحسن approach؟

> الـ image processing هي pure CPU computation — مش I/O. الـ options من الأبسط للأكثر scalability:

```
Option 1: Worker Threads (نفس الـ process)
  └── أسرع في التواصل، بيشاركوا memory
  └── مناسب لو الـ processing بسيط

Option 2: Clustering (multiple processes)
  └── أكثر stability — crash مش بيأثر على الكل
  └── مناسب للـ medium complexity

Option 3: Microservice منفصل ✅ (الـ Production Answer)
  └── service منفصلة بلغة تانية (Python/Go أسرع للـ images)
  └── بتـ scale بشكل مستقل
  └── الـ main server بيبعت task للـ queue (Redis/RabbitMQ)
  └── الـ image service بتاخد الـ task وترجع النتيجة
```

```javascript
// ❌ الغلط — blocking في الـ Event Loop
app.post('/process-image', (req, res) => {
  const result = heavyImageProcessing(req.body.image); // ← بيوقّف الـ server!
  res.json({ result });
});

// ✅ الصح — Worker Thread
app.post('/process-image', (req, res) => {
  const worker = new Worker('./image-worker.js', {
    workerData: { image: req.body.image }
  });
  worker.on('message', result => res.json({ result }));
  worker.on('error',   err    => res.status(500).json({ error: err.message }));
});
```

---

## 🫒 زتونة الإنترفيو

> **"Node.js مبنية على V8 للـ JS execution وlibuv للـ Async I/O. الـ Event Loop هو الـ single thread اللي بيشغّل كل الـ JS code بتاعك، وبيراقب 3 arrays: pending timers، OS tasks، وThread Pool operations. الـ blocking code في الـ Event Loop هو أخطر حاجة ممكن تعملها — بيوقّف الـ server كامل. الحل هو إنك تستخدم دايماً الـ async APIs الموجودة (fs, crypto, https) اللي بتشتغل بعيداً عن الـ Event Loop. لو محتاج performance أحسن مع requests كتيرة، استخدم Clustering بعدد workers = عدد CPU cores، وpm2 في الـ production عشان تتولّى الـ process management. Worker Threads للـ حالات الخاصة جداً اللي فيها pure JS heavy computation."**

---

*المصدر: مبني على محاضرة Advanced Node.js وتجارب إنترفيوهات حقيقية*
