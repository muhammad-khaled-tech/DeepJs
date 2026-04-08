# 🟢 Node.js — مذاكرة الإنترفيو بالعامية المصرية

> **ملاحظة:** الملف ده بيغطي كل الـ topics اللي في النوتس بتاعتك بالتفصيل الممل — متحتاجش ترجع للـ docs يوم الإنترفيو.

---

## 📌 الفهرس

1. [[#ما هو Node.js؟]]
2. [[#الفرق بين Node.js والـ Browser]]
3. [[#الـ V8 JavaScript Engine]]
4. [[#الـ npm — مدير الحزم]]
5. [[#ECMAScript 2015 وما بعده في Node.js]]
6. [[#Debugging في Node.js]]
7. [[#الـ Fetch API مع Undici]]
8. [[#الـ WebSocket Client في Node.js]]
9. [[#الفرق بين Development وProduction في Node.js]]
10. [[#Profiling — قياس أداء التطبيق]]
11. [[#Node.js مع WebAssembly]]
12. [[#Security Best Practices]]

---

## ما هو Node.js؟

تخيل إنك شغال على مشروع ويب، وعندك JavaScript بتشتغل في الـ browser عشان تتحكم في الصفحة. طب ما كان جميل لو نفس اللغة دي تشتغل كمان على السيرفر؟ ده بالظبط اللي جه Node.js عشانه.

**Node.js** هو **runtime environment** — يعني بيئة تشغيل — بتخليك تشغّل كود JavaScript **بره البراوزر** على السيرفر أو على جهازك مباشرةً.

### ليه Node.js بيُعدّ سريع جداً؟

**Node.js بيشغّل الـ V8 engine** — ده نفس المحرك اللي بيشغّل Google Chrome. فبما إن Chrome سريع ومحسّن بشكل رهيب، Node.js بيورث السرعة دي.

### نقطة مهمة جداً — الـ Single Process وعدم الـ Blocking

كتير من السيرفرات التانية زي Apache كانت بتعمل **thread جديد لكل request**. الـ Thread ده بياخد ذاكرة، وبياخد وقت عشان ينشأ، وبيخلي السيرفر مثقّل. Node.js اتخلى عن الفكرة دي خالص.

Node.js بيشتغل في **single process** — process واحدة بس — وبيعتمد على **asynchronous I/O** بدل ما يستنى. يعني إيه ده عملياً؟

تخيل عندك طلب من يوزر يجيب له بيانات من الـ database. في السيرفر العادي، الـ thread بيقف واقف ومستنيّ رد الـ database — ده اسمه **blocking**. Node.js بيعمل إيه؟ بيبعت الطلب للـ database، وبدل ما يوقف مستنيّ، بيروح يشتغل على طلبات تانية. لما الرد يجي من الـ database، Node.js بيرجع يكمّل الشغل.

بالطريقة دي، Node.js قادر يتعامل مع **آلاف الـ connections في نفس الوقت** باستخدام process واحدة بس، من غير ما يتعب من إدارة الـ threads.

### الكود المشهور — Hello World Server

```javascript
const { createServer } = require('node:http');
const hostname = '127.0.0.1';
const port = 3000;

const server = createServer((req, res) => {
  res.statusCode = 200;
  res.setHeader('Content-Type', 'text/plain');
  res.end('Hello World');
});

server.listen(port, hostname, () => {
  console.log(`Server running at http://${hostname}:${port}/`);
});
```

**تحليل الكود بالتفصيل:**

- `require('node:http')` — بنجيب الـ **http module** اللي جوّا Node.js. ده اللي بيخليك تعمل servers وتبعت requests.
- `createServer()` — بتعمل سيرفر HTTP جديد. الـ callback اللي بيتعدّي لها بتتنادى على كل **request** جديد بييجي.
- الـ callback بتاخد `req` و`res`:
  - `req` — الـ **IncomingMessage** — بيمثّل الطلب الجاي من اليوزر. فيه headers، البيانات، الـ URL، إلخ.
  - `res` — الـ **ServerResponse** — ده اللي بتبعت بيه الرد للعميل.
- `res.statusCode = 200` — بنقول للـ client إن الطلب نجح.
- `res.setHeader('Content-Type', 'text/plain')` — بنحدد إن الرد بتاعنا نص عادي.
- `res.end('Hello World')` — بنبعت الرد ونقفل الـ connection.
- `server.listen(port, hostname, callback)` — بنبدأ السيرفر يستمع على البورت 3000.

**عشان تشغّل الكود:**
```bash
node server.js
```
لو بتستخدم الـ ESM version، احفظ الملف كـ `server.mjs` وشغّله بـ `node server.mjs`.

---

## الفرق بين Node.js والـ Browser

حاجة كتير من الناس بتتلخبط فيها. الاتنين بيشغّلوا JavaScript، بس البيئة مختلفة خالص.

### الـ Ecosystem مختلف

في الـ **Browser**، أنت طول الوقت بتتعامل مع حاجات زي:
- الـ **DOM** — `document`, `window`, `getElementById`, إلخ.
- الـ **Web APIs** — زي `localStorage`, `fetch`, `Cookies`, إلخ.

دي كلها **مش موجودة في Node.js**. لو كتبت `document.getElementById('btn')` جوّا Node.js هيطلع لك error.

في المقابل، في **Node.js**، أنت بتتعامل مع حاجات زي:
- الـ **File System** — قراءة وكتابة ملفات على السيرفر.
- الـ **Network** — عمل HTTP servers وclients.
- الـ **Process** — التحكم في الـ process نفسه.

دي كلها **مش موجودة في البراوزر**.

### التحكم في البيئة

في البراوزر، أنت مش بتتحكم إيه browser بيستخدم اليوزر — ممكن Chrome، ممكن Firefox، ممكن واحد لسه شايل IE قديم. فمضطر تكتب كود متوافق مع كل الإصدارات.

في Node.js، **أنت اللي بتحدد الإصدار**. عارف بالظبط هتشغّل التطبيق على إيه Node version، فممكن تستخدم أحدث features في JavaScript براحتك.

### الـ CommonJS vs ES Modules

ده فرق تقني مهم:
- في Node.js، ممكن تستخدم الاتنين: `require()` (CommonJS) و`import` (ES Modules). Node.js دعم الاتنين من الـ v12.
- في البراوزر، بدأنا نشوف دعم لـ ES Modules بس. مش كل حاجة بتعرف `require`.

---

## الـ V8 JavaScript Engine

### ما هو الـ V8؟

**V8** هو المحرك اللي بيفهم JavaScript ويشغّلها. كتبه Google وهو اللي جوّا Chrome. لما فتحت Chrome وروحت على موقع فيه JavaScript، V8 هو اللي بيقرأها وينفّذها.

لما Ryan Dahl أنشأ Node.js سنة 2009، اختار V8 كـ engine. النتيجة؟ Node.js ورث كل سرعة وتطوير V8.

### الـ V8 مش الـ DOM

ده غلطة شايعة. V8 مش هو اللي بيعمل `document.getElementById` ولا الـ DOM. V8 بيفهم JavaScript فقط. الـ DOM والـ Web APIs دي بتيجي من البراوزر نفسه اللي بيحتضن الـ V8.

### كل Browser عنده Engine

| المتصفح | المحرك |
|---------|--------|
| Chrome / Edge | V8 |
| Firefox | SpiderMonkey |
| Safari | JavaScriptCore (Nitro) |

كل المحركات دي بتطبّق معيار واحد: **ECMA ES-262** — ده المعيار الرسمي للـ JavaScript.

### JavaScript مش Interpreted بس!

فكرة قديمة كانت إن JavaScript لغة **interpreted** — يعني بتتقرأ سطر بسطر وتتنفّذ. ده كان صح في الأول.

دلوقتي، V8 بيعمل حاجة اسمها **JIT Compilation — Just-In-Time Compilation**. يعني بدل ما يفسّر الكود على طول، بيـ**compile** أجزاء منه للـ machine code وهو شغّال، عشان يكون أسرع بكتير في المرات الجاية. ده ممكن يتسأل في الإنترفيو!

الـ JIT اتبدأ فعلياً سنة 2009 لما Firefox 3.5 أضاف SpiderMonkey compiler، وبعدين V8 كمّل على نفس الفكرة.

---

## الـ npm — مدير الحزم

### npm إيه؟

**npm** اختصار **Node Package Manager**. هو أداة بتيجي مع Node.js وبتخليك:
- تنزّل مكتبات جاهزة (packages/dependencies) عشان تستخدمها في مشروعك.
- تشارك كودك مع الناس التانية.
- تشغّل scripts محددة في مشروعك.

في سبتمبر 2022، كان في **أكتر من 2.1 مليون package** على الـ npm registry. ده أكبر repository بلغة واحدة في العالم!

البدائل لـ npm هما **Yarn** و**pnpm**.

### تنزيل الـ Dependencies

```bash
# تنزيل كل الـ dependencies اللي في package.json
npm install

# تنزيل package معين
npm install <package-name>

# تنزيل package وإضافته لـ devDependencies
npm install --save-dev <package-name>

# تنزيل package بدون إضافته لـ package.json
npm install --no-save <package-name>
```

### الفرق بين dependencies وdevDependencies

**ده سؤال بيتسأل كتير في الإنترفيو!**

- **`dependencies`**: الحاجات اللي مشروعك محتاجها عشان يشتغل في الـ **production**. مثلاً: Express, Mongoose, إلخ.
- **`devDependencies`**: الحاجات اللي بتحتاجها **وقت التطوير بس** — زي testing libraries (Jest مثلاً), Webpack, TypeScript compiler. الـ production server مش محتاجها.
- **`optionalDependencies`**: لو فشل تنزيلها، التطبيق مش هيبوظ، بس لازم كودك يتعامل مع غيابها.

### Versioning والـ Semver

npm بيتبع معيار **Semantic Versioning (semver)**:

الـ version بتتكوّن من 3 أرقام: `MAJOR.MINOR.PATCH` — مثلاً `1.4.2`

- **PATCH** (آخر رقم): bug fixes بسيطة، مفيش حاجة اتكسرت.
- **MINOR** (الوسط): features جديدة أُضيفت بشكل backward-compatible.
- **MAJOR** (الأول): تغييرات جذرية ممكن تكسر الكود القديم.

```bash
# تنزيل version معين
npm install express@4.18.0

# تحديث كل الـ packages
npm update
```

### الـ npm Scripts

في الـ `package.json` ممكن تعرّف commands مختصرة:

```json
{
  "scripts": {
    "start": "node lib/server-production",
    "start-dev": "node lib/server-development",
    "watch": "webpack --watch --config webpack.conf.js",
    "prod": "NODE_ENV=production webpack -p --config webpack.conf.js"
  }
}
```

بعدين بدل ما تكتب الكوماند الطويلة، بتكتب:
```bash
npm run start-dev
npm run watch
npm run prod
```

---

## ECMAScript 2015 وما بعده في Node.js

### الموضوع إيه؟

JavaScript اللغة بتتطور باستمرار. بتيجي features جديدة زي arrow functions, classes, async/await, إلخ. المعيار الرسمي اللي بيحدد الـ features دي اسمه **ECMAScript** أو **ECMA-262**. إصدار 2015 (الـ ES6) كان نقلة كبيرة.

Node.js بيحاول يستخدم أحدث إصدارات V8، فمع كل إصدار جديد من Node.js بتجي features جديدة من JavaScript.

### تصنيف الـ Features

الـ features في Node.js بتنقسم لـ 3 أنواع:

1. **Shipping (مستقرة)**: متاحة بشكل افتراضي، V8 اعتبرها stable. مش محتاج أي flag.
2. **Staged (شبه جاهزة)**: جاهزة بس V8 لسه مش معتبراها stable. تحتاج flag: `--harmony`
3. **In Progress (تحت التطوير)**: مش جاهزة، ممكن تتغير، مش ينصح تستخدمها في production. كل feature عندها flag خاص بيها.

### تعرف V8 version عندك

```bash
node -p process.versions.v8
```

### ليه ده مهم في الإنترفيو؟

لأن في البراوزر، لو محتاج تستخدم ES6+، ممكن تحتاج تـ**transpile** الكود بأداة زي **Babel** عشان يشتغل على المتصفحات القديمة. في Node.js، مش محتاج Babel لأنك بتتحكم في الإصدار اللي شغّال عليه. ده ميزة كبيرة.

---

## Debugging في Node.js

### الـ Inspector

لما بتشغّل Node.js بالـ flag `--inspect`، بيفتح **debugging server** على البورت `9229` بشكل افتراضي على الـ address `127.0.0.1`.

```bash
node --inspect server.js
```

أي debugging client يعرف يتواصل مع الـ Inspector بروتوكول خاص بيقدر يتوصل ويبدأ debugging.

### الـ Flags المهمة

| Flag | الوظيفة |
|------|---------|
| `--inspect` | تفعيل الـ inspector على `127.0.0.1:9229` |
| `--inspect=[host:port]` | تفعيله على عنوان أو بورت مخصص |
| `--inspect-brk` | تفعيل الـ inspector، والوقوف عند أول سطر كود قبل التنفيذ |
| `--inspect-wait` | تفعيل الـ inspector، والانتظار لحد ما debugger يتوصّل |

### الأدوات اللي بتستخدم الـ Inspector

- **Chrome DevTools**: افتح `chrome://inspect` في Chrome، هتلاقي تطبيق Node.js بتاعك ظاهر في الـ Remote Target list. اضغط inspect وهتاخد debugging بالـ GUI الجميل.
- **VS Code**: بيدعم debugging بشكل native، بس افتح settings من الـ Debug panel.
- **VS 2017+**: من قايمة Debug اختار Start Debugging أو F5.
- **WebStorm**: عمل Node.js debug configuration وشغّله.

### تحذير أمني مهم

**لازم تعرف الكلام ده للإنترفيو:**

الـ Inspector بيدي صلاحية **كاملة** لتنفيذ كود على السيرفر. لو حد تاني اتوصّل بيه يقدر يعمل أي حاجة. لذلك:

- ✅ الـ default: `--inspect` بيستمع على `127.0.0.1` بس — يعني الجهاز المحلي فقط.
- ❌ **ممنوع** تبعت `--inspect` مع IP عام أو `0.0.0.0` على سيرفر production، غير كده أي حد على الإنترنت يقدر يتحكم في السيرفر.

**لو عايز تعمل Remote Debugging بأمان؟** استخدم **SSH Tunnel**:

```bash
# على السيرفر البعيد
node --inspect server.js

# من جهازك المحلي
ssh -L 9221:localhost:9229 user@remote.example.com
```

بكده بتوصّل الـ port 9221 على جهازك لـ 9229 على السيرفر عبر قناة SSH مشفّرة. وبعدين تفتح Chrome DevTools على `localhost:9221`.

---

## الـ Fetch API مع Undici

### ما هي Undici؟

**Undici** هي مكتبة HTTP client متبنياها من الصفر لـ Node.js. اسمها "undici" يعني "أحد عشر" بالإيطالي — إشارة للـ HTTP/1.1. هي دي اللي بتشغّل الـ `fetch` API الـ built-in في Node.js من الـ v18+.

مميزاتها: سريعة جداً وملاءمة للتطبيقات high-performance.

### Basic GET Request

```javascript
async function main() {
  const response = await fetch('https://jsonplaceholder.typicode.com/posts');
  const data = await response.json();
  console.log(data);
}
main().catch(console.error);
```

ده نفس الـ `fetch` اللي بتستخدمه في البراوزر. الـ default method هي GET.

### Basic POST Request

```javascript
const body = {
  title: 'foo',
  body: 'bar',
  userId: 1,
};

async function main() {
  const response = await fetch('https://jsonplaceholder.typicode.com/posts', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(body),
  });
  const data = await response.json();
  console.log(data);
}
main().catch(console.error);
```

### الـ Pool — إعادة استخدام الـ Connections

لو بتبعت requests كتير لنفس السيرفر، بدل ما تفتح connection جديد في كل مرة، ممكن تستخدم **Pool** عشان تعيد استخدام نفس الـ connections:

```javascript
import { Pool } from 'undici';

const pool = new Pool('http://localhost:11434', {
  connections: 10, // أقصى عدد connections
});

const { statusCode, body } = await pool.request({
  path: '/api/generate',
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ prompt: 'hello', model: 'mistral' }),
});
```

ده بيحسّن الأداء بشكل ملحوظ.

### الـ Streaming Responses

ممكن كمان تـ**stream** الـ response بدل ما تستنّاه كله:

```javascript
import { Writable } from 'node:stream';
import { stream } from 'undici';

await stream(
  'https://api.github.com/users/nodejs/repos',
  { method: 'GET', headers: { 'User-Agent': 'myapp' } },
  res => {
    let buffer = '';
    return new Writable({
      write(chunk, encoding, callback) {
        buffer += chunk.toString();
        callback();
      },
      final(callback) {
        const json = JSON.parse(buffer);
        console.log(json.map(repo => repo.name));
        callback();
      },
    });
  }
);
```

---

## الـ WebSocket Client في Node.js

### WebSocket إيه؟

HTTP العادي يشتغل بنظام **request-response**: اليوزر بيبعت request، السيرفر بيرد، والـ connection بيتقفل. لو اليوزر عايز يعرف في حاجة اتغيرت على السيرفر؟ محتاج يبعت request تاني.

**WebSocket** بيحل المشكلة دي. بيفتح **connection** **دائم** بين الـ client والسيرفر، وكل منهم يقدر يبعت للتاني في أي وقت من غير ما ينتظر. ده اللي بيسموه **full-duplex** أو **bi-directional** communication.

المواقف اللي WebSocket مفيد فيها: chat apps, live notifications, real-time games, live prices في البورصة، إلخ.

- WebSocket بيشتغل على البورت **443** (مشفّر) أو **80** (غير مشفّر).
- الـ URI schemes بتاعته: `ws://` للاتصال غير المشفّر، و`wss://` للمشفّر.

### Native WebSocket Client في Node.js

من **Node.js v21** متاح الـ WebSocket client built-in، واتعلن عنه stable في **v22.4.0**. قبل كده كنت محتاج مكتبة تالتة زي `ws` أو `socket.io`.

### كود عملي

**الاتصال الأساسي وتبادل رسائل:**

```javascript
const socket = new WebSocket('ws://localhost:8080');

// لما الـ connection يتفتح
socket.addEventListener('open', event => {
  console.log('Connection established!');
  socket.send('Hello Server!');
});

// لما تيجي رسالة من السيرفر
socket.addEventListener('message', event => {
  console.log('Message from server: ', event.data);
});

// لما الـ connection يتقفل
socket.addEventListener('close', event => {
  console.log('Connection closed:', event.code, event.reason);
});

// لما يحصل error
socket.addEventListener('error', error => {
  console.error('WebSocket error:', error);
});
```

**إرسال واستقبال JSON:**

```javascript
const socket = new WebSocket('ws://localhost:8080');

socket.addEventListener('open', () => {
  const data = { type: 'message', content: 'Hello from Node.js!' };
  socket.send(JSON.stringify(data)); // حوّل الـ object لـ string قبل الإرسال
});

socket.addEventListener('message', event => {
  try {
    const receivedData = JSON.parse(event.data); // حوّل الـ string لـ object بعد الاستقبال
    console.log('Received JSON:', receivedData);
  } catch (error) {
    console.error('Error parsing JSON:', error);
  }
});
```

### نقطة مهمة جداً للإنترفيو!

Node.js v22 عنده **WebSocket client** built-in — يعني Node.js يقدر **يتوصّل** لـ WebSocket server.

لكن Node.js **مش عنده WebSocket server** built-in. لو عايز تعمل WebSocket server (يعني تـ**accept** connections من browsers أو clients تانيين)، لسه محتاج مكتبة زي `ws` أو `socket.io`.

---

## الفرق بين Development وProduction في Node.js

### مفيش فرق في الـ Core!

كتير بيسألوا في الإنترفيو: "إيه الفرق بين Node.js في development وproduction؟"

الإجابة الصح: **في Node.js نفسه مفيش settings خاصة للإنتاج**. بس في مكتبات كتير بتتعامل مع متغير البيئة `NODE_ENV` وبتغيّر سلوكها بناءً عليه.

### الـ NODE_ENV

```bash
NODE_ENV=production node app.js
```

ممكن تحدد قيمته لـ: `development`, `testing`, `staging`, `production`.

كتير من الـ libraries زي Express بتعمل optimizations تلقائياً لما `NODE_ENV=production`.

### ليه NODE_ENV يُعدّ antipattern؟

**ده سؤال سبق وتسألوه في إنترفيوز كتير!**

المشكلة لما بتعمل كود زي كده:

```javascript
if (process.env.NODE_ENV === 'development') {
  // كود معين
}
if (process.env.NODE_ENV === 'production') {
  // كود تاني
}
```

إيه المشكلة؟ إنك بتعمل سلوك مختلف للتطبيق حسب البيئة. يعني لو اتعمل تيست في development ونجح، مش معناه إنه هينجح في production. بتفقد القدرة على التيست الموثوق!

الأفضل هو إنك تفصل بين الـ **optimizations** والـ **behavior**. مثلاً: debug logging ممكن يتحكم فيه بـ flag منفصل مش مرتبط بـ NODE_ENV.

---

## Profiling — قياس أداء التطبيق

### الـ Profiling إيه؟

**Profiling** يعني إنك تـ**راقب** تطبيقك وهو شغّال عشان تعرف:
- أنهي functions بتاخد أكتر وقت CPU؟
- في memory leaks؟
- في bottlenecks بتعطّل الأداء؟

### الـ Built-in Profiler

Node.js عنده profiler built-in جوّا الـ V8. بيـ**sample** الـ stack بشكل منتظم (بيسمّوا الـ samples دي **ticks**) ويسجّل نتايجها.

**عشان تشغّل الـ profiler:**

```bash
NODE_ENV=production node --prof app.js
```

ده بيعمل ملف اسمه `isolate-0xnnnnnnnnnnnn-v8.log`.

**عشان تقرأ الملف:**

```bash
node --prof-process isolate-0xnnnnnnnnnnnn-v8.log > processed.txt
```

### مثال عملي

كان في تطبيق Express فيه endpoint بيعمل encryption للباسورد:

```javascript
// الإصدار البطيء — Synchronous
const hash = crypto.pbkdf2Sync(password, salt, 10000, 512, 'sha512');
```

النتايج كانت كارثية: **5 requests بس في الثانية** ومعدل استجابة 4 ثواني!

لما اشتغلوا على الـ profiler، طلع إن **51.8% من وقت الـ CPU** كان بيتاكل من `pbkdf2Sync`. المشكلة إن الدالة دي **synchronous** — يعني بتـ**block** الـ event loop وتمنع Node.js من التعامل مع طلبات تانية.

**الحل: استخدام الـ Async version:**

```javascript
// الإصدار السريع — Asynchronous
crypto.pbkdf2(password, salt, 10000, 512, 'sha512', (err, hash) => {
  // الكود هيشتغل لما الـ hash يتعمل، بدون blocking
});
```

النتيجة: **20 request في الثانية** ومعدل استجابة 1 ثانية بس. تحسّن بمقدار 4 مرات!

**الدرس المستفاد:** أي عملية heavy زي encryption أو قراءة ملف — دايماً استخدم الـ async version عشان ما تـ**block**ش الـ event loop.

---

## Node.js مع WebAssembly

### WebAssembly إيه؟

**WebAssembly (Wasm)** هو format قريب من الـ machine code. بتـ**compile** كود C, C++, Rust أو غيرهم لـ .wasm file، وبعدين تشغّل الملف ده في البراوزر أو في Node.js بسرعة عالية جداً.

مناسب للعمليات الحسابية الثقيلة زي تشغيل games engines, video/image processing, ML models, إلخ.

### المصطلحات الأساسية

| المصطلح | المعنى |
|---------|--------|
| **Module** | الـ .wasm file المـcompiled |
| **Memory** | ArrayBuffer قابل للتمدد بيستخدمه الـ Wasm code |
| **Table** | Array من references مش محفوظة في الـ Memory |
| **Instance** | نسخة شغّالة من الـ Module مع Memory وTable والـ variables |

### طرق إنشاء Wasm modules

- **Emscripten**: لتحويل كود C/C++ لـ .wasm
- **wasm-pack**: لتحويل كود Rust لـ .wasm
- **AssemblyScript**: لو بتحب TypeScript
- كتابة Wasm Text format (.wat) يدوياً وتحويله

### استخدام Wasm في Node.js

```javascript
const fs = require('node:fs');

// اقرأ الـ .wasm file
const wasmBuffer = fs.readFileSync('/path/to/add.wasm');

// شغّله
WebAssembly.instantiate(wasmBuffer).then(wasmModule => {
  const { add } = wasmModule.instance.exports;
  console.log(add(5, 6)); // 11
});
```

Node.js بيدي الـ `WebAssembly` object كـ global — مفيش حاجة تـimport.

### ملاحظة مهمة

Wasm modules **مش تقدر توصل** لنظام الملفات أو الشبكة مباشرةً. لو محتاج ده، بتستخدم أداة زي **Wasmtime** اللي بتتيح الوصول ده عبر **WASI API**.

---

## Security Best Practices

الباب ده مهم جداً في الإنترفيو. هنتكلم عن أشهر هجمات على Node.js وازاي تتحمى.

### 1. Denial of Service — DoS (CWE-400)

**الفكرة:** المهاجم بيبعت requests بطريقة بتخلي السيرفر مشغول ومش قادر يرد على أي حد تاني.

مثال كلاسيكي: **Slowloris attack** — بيبعت HTTP requests ببطء شديد، fragment بعد fragment. السيرفر بيفضل حاجز resources للـ request ده. لو بعت كتير زيه في نفس الوقت، السيرفر بيتملّى ويوقف.

**الحلول:**
- استخدام **reverse proxy** (زي Nginx) قبل السيرفر بتاعك — بيتحمل هو الضغط.
- ضبط **timeouts** مناسبة على السيرفر: `headersTimeout`, `requestTimeout`, `keepAliveTimeout`.
- تحديد عدد **open sockets** المسموح بيهم.
- تأكد إنك معملتش server من غير error handler — غير كده request واحد غلط يقدر يـcrash السيرفر كله.

### 2. DNS Rebinding (CWE-346)

**الفكرة:** هجوم بيستهدف الـ debugging inspector (`--inspect`). المهاجم يعمل website خبيثة، وعن طريق التحكم في DNS يخلّي الـ browser يتصل بالـ inspector اللي شغّال على جهازك.

**الحلول:**
- **مبدأياً مش تشغّل الـ inspector في production**.
- لو محتاجه، استخدم SSH tunnel بدل ما تفتح البورت للعالم.
- أضف `process.on('SIGUSR1', ...)` listener عشان تتحكم في تشغيل الـ inspector.

### 3. كشف ملفات حساسة (CWE-552)

**الفكرة:** لما بتـ**publish** package على npm، بيُرفع **كل محتوى الـ folder** تلقائياً إلا لو قلتله ما يرفعش.

خطير جداً لو عندك ملفات زي `.env` فيها passwords أو API keys!

**الحلول:**
- استخدم `.npmignore` أو `.gitignore` عشان تحدد الملفات المُستثناة.
- استخدم `files` في `package.json` عشان تحدد بالظبط إيه اللي يتنشر (allowlist).
- **قبل ما تنشر**: شغّل `npm publish --dry-run` عشان تشوف هيتنشر إيه.

### 4. HTTP Request Smuggling (CWE-444)

**الفكرة:** هجوم بيحصل لما يكون في **proxy** قدام Node.js. المهاجم بيبعت HTTP request مبهم، الـ proxy يفهمه بطريقة، وNode.js يفهمه بطريقة تانية. النتيجة: request خبيث "يتهرّب" من الـ proxy ويوصل للـ app.

**الحلول:**
- ما تستخدمش الـ `insecureHTTPParser` option.
- اضبط الـ proxy عشان **يُنظّف** الـ requests الغامضة.
- استخدم **HTTP/2** end-to-end.

### 5. Timing Attacks (CWE-208)

**الفكرة:** المهاجم بيبعت requests ويقيس الفارق في وقت الرد عشان يخمّن معلومات سرية. مثلاً: لو بتقارن password بـ string comparison عادية، المقارنة للكلمات المتطابقة بتاخد وقت أطول. ده بيفضح طول وتركيب الباسورد.

**الحلول:**
- **دايماً** استخدم `crypto.timingSafeEqual()` لمقارنة بيانات حساسة.
- استخدم `crypto.scrypt()` لـ password hashing.

### 6. Prototype Pollution (CWE-1321)

**الفكرة:** في JavaScript، كل object بيرث من `Object.prototype`. لو المهاجم قدر يعدّل الـ `__proto__` بيخلي properties خبيثة تظهر في **كل الـ objects** في التطبيق.

**مثال:**
```javascript
const data = JSON.parse('{"__proto__": { "polluted": true}}');
const c = Object.assign({}, {}, data);
console.log(c.polluted); // true — الـ pollution اتنشر!
```

**الحلول:**
- **ما تعملش** deep merge على بيانات جاية من اليوزر بدون validation.
- استخدم JSON Schema validation على كل input.
- استخدم `Object.create(null)` لو عايز object من غير prototype.
- استخدم `Object.freeze(MyObject.prototype)` تجميد الـ prototype.
- استخدم الـ flag `--disable-proto`.

### 7. Malicious Third-Party Packages (CWE-1357) وSupply Chain Attacks

**الفكرة:** مكتبة استخدمتها فيها كود خبيث — إما إنها اتعملت عشان كده (typosquatting)، أو إن حساب الـ maintainer اتاخد والمهاجم نشر version خبيث.

**Typosquatting**: مهاجم ينشر package باسم قريب من package مشهور زي `expres` بدل `express`. لو غلطت في الكتابة، هتنزّل الخبيث.

**Supply Chain Attack**: لو مكتبة بتستخدمها اعتمدت على مكتبة تالتة اتعملها كود خبيث — حتى لو أنت ما نزّلتهاش مباشرةً.

**الحلول:**
- **Pin** الـ versions بالظبط في `package.json`.
- استخدم **lockfiles** (`package-lock.json`) وتأكد إنها لم تتعدّل.
- استخدم `npm ci` بدل `npm install` — بيجبر استخدام الـ lockfile.
- شغّل `npm audit` بشكل منتظم عشان تكشف vulnerabilities.
- استخدم `--ignore-scripts` عشان تمنع npm scripts من الاشتغال تلقائياً عند التنزيل.
- دايماً اتحقق من الـ package.json عشان ما فيش typos في أسماء الـ packages.

### 8. Memory Access Violations (CWE-284)

**الفكرة:** هجمات بتستغل أخطاء في إدارة الذاكرة.

**الحل:** استخدم الـ flag `--secure-heap=n` عشان تحجز heap آمن ذو حجم محدد.

ملاحظة: `--secure-heap` مش متاح على Windows.

### 9. Monkey Patching (CWE-349)

**الفكرة:** تعديل خصائص built-in objects في الـ runtime — زي overriding الـ `Array.prototype.push`:

```javascript
Array.prototype.push = function (item) {
  // سلوك خبيث هنا!
};
```

**الحل:** استخدم الـ flag `--frozen-intrinsics` (تجريبي) — بيجمّد كل الـ built-in objects وما يخليش حد يعدّل عليهم.

ملاحظة: لسا ممكن تعدّل `globalThis`، فلو عايز تأمن من ده كمان: `Object.freeze(globalThis)`.

### 10. الـ Node.js Permission Model

من Node.js الإصدارات الحديثة، في نظام permissions بتقدر تقيّد فيه إيه اللي Process بتاعتك مسموحالها تعمله:

```bash
node --permission app.js
```

تقدر تحدد: هل مسموح بالـ file system access؟ الـ network access؟ إنشاء child processes؟ إلخ.

ده بيحمي من المكتبات الخبيثة — حتى لو مكتبة اتحلّت فيها exploit، الـ Permission Model بيمنعها من إنها تعمل حاجات برّا الصلاحيات المسموح بيها.

---

## 🎯 ملخص سريع للإنترفيو

| الموضوع | النقطة الجوهرية |
|---------|----------------|
| Node.js ما هو | Runtime لـ JavaScript على السيرفر، بيشغّل V8 |
| الـ Single Process | مش بيعمل thread جديد لكل request، بيعتمد على async I/O |
| V8 | محرك JavaScript بتاع Chrome، بيستخدم JIT Compilation |
| npm | أكبر package registry في العالم، بيدير dependencies |
| dependencies vs devDependencies | production vs development tools |
| Semver | MAJOR.MINOR.PATCH — لو MAJOR اتغيرت يبقى في breaking changes |
| --inspect | بيفتح debugging server على port 9229، متفتحوش publicaly! |
| Fetch/Undici | built-in HTTP client من v18، Undici بتوفر Pool وStreaming |
| WebSocket | من v21 Node.js يقدر يكون WebSocket client، بس مش server |
| NODE_ENV antipattern | بيعمل سلوك مختلف بين environments وبيعطّل الـ testing الموثوق |
| Profiling | `node --prof` لتوليد ticks، `node --prof-process` لقراءتها |
| Prototype Pollution | تعديل `__proto__` يلوّث كل الـ objects، استخدم `Object.create(null)` |
| Supply Chain Attack | مكتبة تالتة فيها كود خبيث، pin versions واستخدم lockfiles |
| Timing Attack | استخدم `crypto.timingSafeEqual` دايماً في مقارنة بيانات حساسة |

---

> 💡 **نصيحة أخيرة:** الإنترفيو في الغالب بيركّز على الـ event loop، الـ async/await، الفرق بين blocking وnon-blocking، والـ npm ecosystem. خليهم واضحين في ذهنك كويس!
