# Hands-On Labs

> **Why labs?** Reading builds recognition; running a vulnerable app next to its fixed twin builds the instinct to spot the bug in review. Seven labs below are **runnable code in [labs/](labs/)** with self-checking output. Each has a goal, the command, what you should see, ways to extend it, and a **reflection** question.
>
> **Legal rule:** run everything on your own machine, on your own code and accounts, or on practice platforms. Never aim these techniques at systems you don't have permission to test.

| Lab | Week | Time | Track | What you will see |
| --- | --- | --- | --- | --- |
| 1. BOLA and mass assignment | 1 | 40 min | BE (FE: read) | A leaking API and its fix |
| 2. XSS encoding, CSP, and a DOM sinks page | 1, 3 | 45 min | FE + BE | Raw payloads vs encoded; a real CSP header; innerHTML vs textContent |
| 3. JWT: verify, don't decode | 1 | 25 min | both | A forged token accepted by `decode`, rejected by `verify` |
| 4. Webhook signature verification | 2 | 30 min | BE | Tampered and replayed requests rejected |
| 5. Password hashing with parameters and rehash | 1 | 25 min | BE | OWASP-minimum scrypt, upgrade on login |
| 6. Rate limiting and body limits | 2 | 20 min | BE | The 6th attempt throttled; a big body refused |
| 7. An SSRF-safe URL validator | 3 | 30 min | BE | 12 URLs: tricks blocked, public IPs allowed |
| 8. Audit your own project | 4 | 40 min | both | Your real dependency, secret and CI exposure |
| 9. CSP report-only on your own app | 3 | 60 min | FE | Real violations from your own pages |
| 10. PortSwigger Web Security Academy | 2-3 | 6 h | both | Real vulnerable apps, legally |
| 11. The 15-snippet code-review drill | 4 | 45 min | both | Your review hit rate |
| 12. Mock interview | 4 | 3 h | both | Your weak spots |

---

## Setup (once)

You need **Node.js 20 or newer** (the labs were tested on Node 24).

```bash
cd labs
npm install          # express, helmet, express-rate-limit, jsonwebtoken
npm run all          # runs labs 1-7; every lab prints PASS or FAIL and exits non-zero on failure
```

Each lab file contains both the **vulnerable** and **fixed** version side by side and a small self-test, so you can read the diff between them.

---

## Lab 1: BOLA and mass assignment

**Goal:** see an API leak another user's data and let a user make themselves admin, then see the fix. **Chapter:** [5](05-authorization-and-api-design.md).

```bash
node lab1_bola.mjs
```

**What you should see:**

```
VULNERABLE app
  Alice reads Bob's order : LEAK (200)
  Alice makes herself admin: SUCCEEDED
FIXED app
  Alice reads Bob's order : blocked (404)
  Alice makes herself admin: blocked
PASS: vulnerable app leaks, fixed app does not.
```

**Extend it:**
1. Add a `DELETE /orders/:id` route and make it vulnerable, then fix it. Does your fix cover it too?
2. Add a **property-level** leak: return a `costPriceCents` field only admins should see, then shape the response.
3. Write a test table: for each route, user A vs user B vs anonymous, expecting 200/404/401.

**Reflect:** Where in your own project is the equivalent of `orders.find(...)`, and does it take the owner from the session?

---

## Lab 2: XSS encoding, CSP, and the DOM sinks page

**Goal:** see output encoding remove the hole, see the CSP header helmet produces, and feel the difference between `innerHTML` and `textContent`. **Chapters:** [3](03-browser-and-http-security.md) and [7](07-frontend-security.md).

**Part A (server):**

```bash
node lab2_xss_csp.mjs
```

**What you should see (abridged):**

```
VULNERABLE: payload reflected as live HTML: true | CSP header: none
FIXED     : payload reflected as live HTML: false | encoded as text: true
FIXED CSP : default-src 'self';base-uri 'self';...;frame-ancestors 'none';...;script-src 'self' 'nonce-...';script-src-attr 'none';style-src 'self' https: 'unsafe-inline';...
PASS: encoding removes the hole; CSP is the second layer.
```

Notice what `helmet`'s default policy still allows (`style-src ... 'unsafe-inline'`): a good baseline, not a finished policy.

**Part B (browser):** open `labs/lab2_dom.html` in your browser. Paste `<img src=x onerror="alert('xss ran')">`, click **innerHTML (UNSAFE)** then **textContent (SAFE)**. Then paste `javascript:alert('xss ran')` and compare the unsafe link with the allowlisted one.

**Extend it:** in Part A, change the page to put `q` inside an HTML **attribute** (`<input value="...">`). Does `escapeHtml` still protect it? (Yes, because it also escapes quotes; try removing the quote escapes to see why they matter.)

**Reflect:** Which of these would a React app have prevented automatically, and which would it have *allowed*?

---

## Lab 3: JWT: verify, don't decode

**Goal:** see that `decode` trusts forged claims while `verify` doesn't. **Chapter:** [4](04-authentication-and-sessions.md).

```bash
node lab3_jwt.mjs
```

**What you should see:** five `PASS` lines: `decode()` trusts the forged `role: admin` (the wrong way); `verify()` accepts the genuine token and rejects the forged payload, an `alg: none` token and an expired token.

**Extend it:** add checks for `iss` and `aud` in `verify`, and show a token for the wrong audience being rejected. Then write the one-line rule you'd put in your team's guidelines.

**Reflect:** Search your code for `jwt.decode(` or `atob(token.split(".")[1])`. Is any of it used for a security decision?

---

## Lab 4: Webhook signature verification

**Goal:** verify a signed webhook with the raw body, a timestamp window and a constant-time comparison. **Chapter:** [8](08-backend-security.md).

```bash
node lab4_webhook.mjs
```

**What you should see:** `PASS` for a valid request (200) and rejections (401) for a tampered body, a replay from an hour ago, a missing signature and a wrong secret.

**Extend it:** (1) switch the route to `express.json()` and see why the signature check breaks (the bytes changed). (2) Add **idempotency**: store processed event IDs and ignore duplicates.

**Reflect:** Which webhooks does your project receive today, and does each verify a signature?

---

## Lab 5: Password hashing with parameters and rehash-on-login

**Goal:** hash with OWASP's minimum scrypt parameters, store the parameters with the hash, and flag weak legacy hashes for upgrade. **Chapter:** [4](04-authentication-and-sessions.md).

```bash
node lab5_passwords.mjs
```

**What you should see:** six `PASS` lines (hash under 1 second, different hashes for the same password, correct/incorrect verification, current hash needs no rehash, a weak legacy hash verifies **and** is flagged `needsRehash`), plus a stored value like `scrypt$131072$8$1$<salt>$<hash>`.

**Extend it:** in production use **Argon2id** with a maintained library (OWASP minimum: 19 MiB memory, 2 iterations, 1 parallelism). Rewrite the lab with `argon2` (Node) or `argon2-cffi` (Python) and keep the rehash logic (`needsRehash` / `check_needs_rehash`).

**Reflect:** How are passwords hashed in your project today, and are the parameters stored with the hash so you can raise them?

---

## Lab 6: Rate limiting and body limits

**Goal:** throttle a login route and cap request size. **Chapters:** [5](05-authorization-and-api-design.md) and [8](08-backend-security.md).

```bash
node lab6_ratelimit.mjs
```

**What you should see:**

```
login attempts 1..7 -> 401 401 401 401 401 429 429
oversized body       -> 413
PASS: attempts 6 and 7 are throttled (429); a 5 KB body is refused (413).
```

**Extend it:** add a **per-account** limiter (key by the username in the body) in addition to the per-IP limiter, and explain what attack each one stops. Then set `trust proxy` and test with an `X-Forwarded-For` header.

**Reflect:** What happens to your login endpoint if 10,000 attempts arrive in a minute?

---

## Lab 7: An SSRF-safe URL validator

**Goal:** block internal addresses (and the encoding tricks) in a "fetch this URL" feature. **Chapter:** [8](08-backend-security.md).

```bash
node lab7_ssrf.mjs
```

**What you should see:** twelve `PASS` lines: loopback, the cloud metadata address, private ranges, IPv6 loopback, IPv4-mapped IPv6, decimal and hex IP tricks, and non-HTTP schemes **blocked**; public IPs allowed.

**Extend it:** (1) add a **host allowlist** mode (`api.partner.com` only) and compare how much simpler and safer it is. (2) Write down the three things this validator does *not* do (DNS rebinding, redirects, response limits) and how you'd handle each.

**Reflect:** Does any feature in your project fetch a URL a user supplied (link previews, webhooks, image import, PDF generation)?

---

## Lab 8: Audit your own project

**Goal:** find your real supply-chain exposure. **Chapter:** [9](09-supply-chain-and-ci-cd.md). Pick a repository **you own**.

1. **Lockfile:** committed? CI uses `npm ci` (or equivalent)? If not, that's finding #1.
2. **Known-vulnerable dependencies:** run `npm audit`, `pip-audit` or `osv-scanner`. Pick the one finding most likely to matter (internet-facing code, exploitable) and say why.
3. **Provenance and install scripts:** `npm audit signatures`. Which dependencies run install scripts? Could you use `--ignore-scripts`?
4. **Secrets:** scan the repository **and its history** with `gitleaks` (or your host's secret scanning). Any key ever committed? **Rotate it**; deleting the file is not enough.
5. **CI review:** open each workflow. Are third-party Actions pinned to a full SHA? Is `permissions:` set? Any `pull_request_target`? Any `${{ github.event... }}` inside `run:`? Do forks get secrets?
6. **SBOM (optional):** `npm sbom --sbom-format cyclonedx > sbom.json` and confirm you could search it for a package name.
7. **Write three lines:** biggest risk, easiest fix, what you'd automate.

**Reflect:** If a package you use were poisoned tomorrow, which of your credentials could it reach, and how fast could you rotate them?

---

## Lab 9: CSP report-only on your own app

**Goal:** discover what a real CSP would break in your own pages. **Chapters:** [3](03-browser-and-http-security.md) and [7](07-frontend-security.md).

1. Add a **report-only** policy to your app (a header or `<meta>`-free server config):
   `Content-Security-Policy-Report-Only: default-src 'self'; script-src 'self' 'nonce-...'; object-src 'none'; base-uri 'self'; frame-ancestors 'none'; report-to csp-endpoint`
2. Browse the app with DevTools open; the Console lists every **violation**.
3. Group them: your inline scripts (add nonces or move to files), third-party scripts (decide: keep, SRI, remove), `eval` (remove).
4. Check headers with `curl -sI https://your-app` and a header-grading site.
5. When violations are quiet for a week, switch to enforcing.

**Reflect:** Which third-party script surprised you most, and what could it read on your page?

---

## Lab 10: PortSwigger Web Security Academy

**Goal:** practise on real, deliberately vulnerable applications, legally. The Academy (portswigger.net/web-security) is free and runs in your browser. Do the **Apprentice** labs first (titles may change; search each topic page).

| Topic | Why it matters to you |
| --- | --- |
| **SQL injection**, **NoSQL injection** | Chapter 6 |
| **Access control** (IDOR, privilege escalation), **API testing** | Chapter 5 |
| **Cross-site scripting**, **DOM-based vulnerabilities** | Chapter 7 |
| **CORS**, **CSRF** | Chapter 3 |
| **JWT attacks**, **OAuth authentication** | Chapter 4 |
| **SSRF**, **File upload vulnerabilities**, **OS command injection**, **Path traversal** | Chapters 6 and 8 |
| **Prototype pollution**, **GraphQL API vulnerabilities**, **Race conditions** | Chapters 5 and 6 |
| **Web LLM attacks** | Chapter 10 |

**Method (more important than speed):** read the topic page first; try for about 10 minutes before a hint; use hints freely but don't copy a full solution; finish each lab by writing **three sentences**: *what was the flaw, how was it exploited, how would I fix it in code.* That third sentence is your interview answer.

---

## Lab 11: The 15-snippet code-review drill

**Goal:** measure your review hit rate under time pressure. **Chapter:** [11](11-secure-code-review.md).

1. Set a **30-minute** timer. Read the 15 snippets in section 2 of Chapter 11 and write one line for each: *the flaw and the fix.* Don't peek at the answers.
2. Score yourself against the answers. **12 of 15 or better** is the goal.
3. For each miss, note which review question (who, allowed, controlled, destination, failure) would have caught it.
4. **Repeat on your own code:** pick one real pull request or a file from your project and find five issues using the five questions.

**Reflect:** Which category do you miss most (authorization, injection, CI, crypto)? That is tomorrow's reading.

---

## Lab 12: Mock interview

**Goal:** find weak spots under mild pressure. **Time:** 3 hours (Saturday of Week 4).

1. Pick 15 random questions: `python3 -c "import random; print(sorted(random.sample(range(1,51),15)))"`, plus **one design question** from section D.
2. Record yourself (phone voice or video). Answer each in **under 90 seconds** using *threat, control, backup layer, test*; for the design question, talk through it for 5 minutes.
3. Watch back and score:

| Check | Yes / No |
| --- | --- |
| Started with the threat in one sentence | |
| Named a concrete control, ideally with a one-line code or config example | |
| Added a second layer of defence | |
| Said how I'd test it | |
| Used a recent, correctly hedged real case ("according to", "reported") | |
| Under 90 seconds, no rambling | |

4. List your three most common problems and redo your five worst answers.
5. If you can, repeat it live with a colleague who asks one follow-up per answer.

**Reflect:** Which topics did you freeze on? Add them to tomorrow's five-minute recall.
