# Chapter 16: Hands-On Practice (Attack It, Then Fix It)

> **Goal.** After this chapter you can: find the classic web bugs yourself in a deliberately vulnerable app, explain each as "how I found it, why it works, how I'd fix it", and write a short finding report. This is the same loop a penetration tester follows, so it also builds the first step toward pentesting.
>
> **Who:** frontend and backend. **Time:** about 6-8 hours (spread over Weeks 2-4). **Needs:** Docker (or Node 24), a browser, curl.

---

## 0. Ground rules (read first)

Testing a system you do not own, or have no written permission to test, is illegal in most countries. Practise **only** on:

- apps running **on your own machine** (Juice Shop in Docker, the labs in `labs/`),
- training sites that invite attacks (PortSwigger Web Security Academy, TryHackMe, Hack The Box),
- your employer's systems **only with written permission**.

Bind lab apps to `127.0.0.1` so nobody else on your network can reach them.

---

## 1. Setup (20 minutes)

```bash
# A deliberately vulnerable web app, reachable only from your machine
docker run -d --name juice -p 127.0.0.1:3000:3000 bkimminich/juice-shop
# open http://127.0.0.1:3000

# Your own labs from this book
cd labs && npm install
```

Tools (all free):

| Tool | Use |
| --- | --- |
| **Browser DevTools** (Network tab) | See every request; right-click a request, **Copy as cURL** or **Copy as fetch** to replay it |
| **curl** | Replay and modify requests from the terminal |
| **Burp Suite Community** | Intercepting proxy: Proxy (see and edit requests), Repeater (resend one request with changes). Learn only these two for now |

---

## 2. The method (the pentester's loop)

Every exercise below follows five steps. Say them in interviews.

1. **Map**: click through the app, record the requests, note every input and every ID.
2. **Hypothesize**: "this ID is in the URL; maybe the server doesn't check ownership."
3. **Test**: change one thing, resend, compare responses.
4. **Prove**: write the smallest reproduction (one request, one screenshot).
5. **Fix and retest**: say what code change closes it, and what test keeps it closed.

---

## 3. Practice sessions

Each session: **Goal, Steps, What you should see, The fix, Say it in the interview.**

### Practice 1: Map the app and read the security signals (45 min)

**Goal:** learn to read what the browser and server are telling you.

**Steps**
1. Open Juice Shop, press F12, open the **Network** tab, register an account and log in.
2. Find the login request. Note: method, URL, body, and the response.
3. Open **Application → Cookies / Local Storage**. Where is the token stored?
4. Run `curl -I http://127.0.0.1:3000` and read the response headers.

**What you should see:** a JWT stored in the browser (readable by scripts), and few or no security headers on the response.

**Checklist to write down:** Is the token in `localStorage` or an `HttpOnly` cookie? Are `Content-Security-Policy`, `Strict-Transport-Security`, `X-Content-Type-Options` present? Any `Access-Control-Allow-Origin: *`?

**The fix:** HttpOnly cookie or BFF (Chapter 4), headers via `helmet` (Chapter 3).
**Say it:** "First I map the app and read where tokens live and which headers are set."

### Practice 2: BOLA / IDOR with two accounts (60 min)

**Goal:** prove broken object-level authorization by hand.

**Steps**
1. Register **two** users, A and B. As each, add a different item to the basket.
2. As A, find the request that loads A's basket (look for `/rest/basket/<number>`). Copy it as cURL.
3. Resend it with B's basket number but **A's token**.
4. Compare: did you get B's basket?

**What you should see:** A can read B's basket. Same bug as Snippet 1 in Chapter 11.

**The fix:** scope every query to the caller (`where: { id, ownerId: req.user.id }`), return 404 otherwise. Prove the fix on your own code: run `labs/lab1_bola.mjs` and read the vulnerable vs fixed handler.
**Test to write:** user A requests user B's resource and expects 404 (Chapter 11, section 3).
**Say it:** "I log in as two users and replay A's request with B's ID. If it works, authorization isn't checked per object."

### Practice 3: Reflected XSS and why encoding fixes it (45 min)

**Goal:** see the difference between text and live HTML.

**Steps**
1. In Juice Shop's search box, enter the payload documented in Juice Shop's own "DOM XSS" challenge (see its Score Board / companion guide): an `<iframe>` with a `javascript:` URL that shows `alert`. The only effect is an alert box.
2. Open `labs/lab2_dom.html` in the browser, paste `<img src=x onerror="alert('xss ran')">`, and click **innerHTML (UNSAFE)** versus **textContent (SAFE)**.
3. Run `npm run lab2` and look at the CSP header the fixed version sends.

**What you should see:** an alert on the unsafe path, literal text on the safe path.

**The fix:** render as text (React does this by default), sanitize with DOMPurify when HTML is required, add a nonce-based CSP (Chapter 7).
**Say it:** "XSS happens when untrusted text is parsed as HTML or script. I fix the sink, then CSP limits the damage."

### Practice 4: SQL injection and parameterized queries (45 min)

**Goal:** understand why string-built SQL is dangerous, then fix it.

**Steps**
1. On Juice Shop's login page, follow its documented "Login Admin" challenge (an injection in the email field using `'` and a SQL comment). Note how an error or odd behaviour reveals that input reaches a query.
2. Write a tiny vulnerable function on your own machine (SQLite in memory, string concatenation) and call it with a quote character. Then rewrite it with placeholders and call it again.

```ts
// vulnerable: input becomes part of the SQL
db.prepare(`SELECT * FROM users WHERE email = '${email}'`).get();
// fixed: input is data, never SQL
db.prepare("SELECT * FROM users WHERE email = ?").get(email);
```

**What you should see:** the first accepts a quote and changes the query's meaning; the second treats the same text as plain data.

**The fix:** placeholders everywhere; allowlist dynamic identifiers like column names (Chapter 6).
**Say it:** "I never build SQL with strings; the driver sends the query and the data separately."

### Practice 5: Tokens: read, verify, tamper (30 min)

**Steps**
1. Copy the JWT from Practice 1. Split it on `.`, base64url-decode the first two parts (`node -e` is enough). Note the claims.
2. Run `npm run lab3` and read how `decode` accepts a forged claim while `verify` with a pinned algorithm rejects it.

**What you should see:** the payload is readable by anyone; only the signature protects it.

**The fix:** `verify` with pinned `algorithms`, `iss`, `aud`, short expiry (Chapter 4).
**Say it:** "A JWT is signed, not secret. Never trust claims you haven't verified."

### Practice 6: Headers and CORS check with curl (30 min)

**Steps**
1. Against Juice Shop and then your own `lab2` server (fixed version), run:
   ```bash
   curl -sI http://127.0.0.1:3000 | grep -iE "content-security|strict-transport|x-content-type|referrer|x-powered"
   curl -sI -H "Origin: https://evil.example" http://127.0.0.1:3000/rest/products/search?q=a | grep -i access-control
   ```
2. Compare which protections each one sends; note any `Access-Control-Allow-Origin` that reflects the evil origin or uses `*`.

**The fix:** `helmet`, exact-origin CORS allowlist (Chapter 3).
**Say it:** "I check headers with curl in seconds; reflected origins with credentials are the dangerous CORS bug."

### Practice 7: Brute force and rate limiting (30 min)

**Steps**
1. Run `npm run lab6`. It starts a server on a random port, sends 7 login attempts and one oversized body, then exits. Read the output: attempts 1-5 return `401`, attempts 6-7 return `429`, the 5 KB body returns `413`.
2. Open `lab6_ratelimit.mjs`, change `limit: 5` to `limit: 2`, and rerun. The lab now prints FAIL, because attempt 3 is throttled earlier than the check expects. That shows the limit is what makes the difference.
3. Change it back to `5`.
4. Think about the gap: the limit is per IP. An attacker with many IPs, or one targeting a single account, needs a per-account limit too.

**The fix:** limits per IP and per account, lockout or backoff, body-size limits (Chapters 4 and 8).
**Say it:** "Login endpoints need per-account and per-IP limits, plus alerts on spikes."

### Practice 8: SSRF validator test (30 min)

**Steps**
1. Run `npm run lab7` and read the 12 test URLs: loopback, private ranges, `169.254.169.254`, IPv6, decimal (`2130706433`) and hex (`0x7f.0.0.1`) forms, and `file:` and `ftp:` schemes are blocked; two public IPs are allowed.
2. Add two cases of your own to the `cases` list in `lab7_ssrf.mjs`, for example `http://localhost/` (blocked after DNS resolution) and `http://0177.0.0.1/` (octal form). Run again and see whether each is blocked. If one slips through, fix `assertSafeUrl`.

**The fix:** resolve DNS, check the resulting IP against a block list, pin it, limit redirects (Chapter 8).
**Say it:** "I validate the resolved IP, not the hostname string."

### Practice 9: Write a one-page finding report (30 min)

A report is how pentesters and AppSec engineers communicate. Write one for Practice 2 using this template:

```
Title:        Broken object-level authorization on basket endpoint
Severity:     High (any user can read any user's basket)
Where:        GET /rest/basket/{id}
Steps:        1) Log in as user A. 2) Request B's basket id with A's token.
Evidence:     Response body contains B's items (screenshot / curl output).
Impact:       Data exposure across accounts; at scale, a full data leak.
Fix:          Scope the query to the authenticated user; return 404 otherwise.
Test:         Integration test: A requests B's basket, expect 404.
```

---

## 4. Continue on real training platforms

| Platform | Why | Start with |
| --- | --- | --- |
| **PortSwigger Web Security Academy** (free) | The best guided web-security course; labs in the browser | Access control, SQL injection, XSS, authentication, SSRF, JWT |
| **OWASP Juice Shop** | Gamified, covers most of the OWASP Top 10 | Score Board; try the 1-2 star challenges |
| **TryHackMe** (free tier) | Guided paths for beginners | "Pre Security", "Web Fundamentals" |
| **Hack The Box Academy** | Deeper, more pentest-oriented | "Web Requests", "Introduction to Web Applications" |

---

## 5. Is this related to pentesting?

**Partly.** Practices 1, 2, 3, 4, 6 and 9 are pentest-style: you attack an app you did not write, using map, hypothesize, test, prove, report. Practices 5, 7 and 8 are developer-side: you run this book's labs and check that your fix works. Together they are **web-application security testing**, the entry-level slice of pentesting. They are not a full pentest, which has a written scope and permission, covers a whole system, and ends in a professional report. The difference is the goal.

| | Software engineer with security skills | Web pentester |
| --- | --- | --- |
| **Question** | "How do I prevent this bug in my code?" | "Where are the bugs in someone else's system?" |
| **Output** | Fix, test, review checklist | Written report with evidence and risk rating |
| **Breadth** | The bugs in your stack | Web, APIs, networks, infrastructure, sometimes physical and social engineering |

What a pentester also needs, which this book does **not** teach in depth: Burp Suite mastery, network scanning (nmap) and service enumeration, privilege escalation, Active Directory, cloud misconfigurations, scoping and rules of engagement, and report writing at professional quality. The first book (`interview-prep-book/`) touches scanning and networks; practising on TryHackMe/Hack The Box fills the rest.

**A realistic path if you want pentesting later:** PortSwigger Academy (web) → Juice Shop → TryHackMe/HTB paths → an entry certification such as eJPT or PNPT, then OSCP later (check each provider's current syllabus and prices).

**For your one-month interview goal:** the nine practices above are enough to say "I've found and fixed these myself", which is much stronger than theory alone.

---

## 6. Where it fits in your 4-week plan

| Week | Add this (about 2 h per week) |
| --- | --- |
| 1 | Setup, Practice 1 |
| 2 | Practices 2 and 5 (authorization and tokens) |
| 3 | Practices 3, 4, 6 (XSS, SQL, headers), plus your track |
| 4 | Practices 7, 8, 9 (limits, SSRF, report); then the mock interview |

---

## Check yourself

1. List the five steps of the pentester's loop.
2. How do you prove a BOLA bug with two accounts?
3. What does a good finding report contain?
4. Where may you legally practise?

**Answers** *(cover this until you have tried)*

1. Map, hypothesize, test, prove, fix and retest.
2. Log in as A, replay A's request with B's object ID, and show the response contains B's data; then fix the query and show it returns 404.
3. Title, severity, location, steps, evidence, impact, fix, and the test that keeps it fixed.
4. Your own machine, training sites that invite attacks, or systems you have written permission to test.

---

## Summary

- Practise attacks **only on legal targets**; the loop is map, hypothesize, test, prove, fix.
- Nine practices cover BOLA, XSS, SQL injection, tokens, headers/CORS, rate limits, SSRF, and a report.
- This is the web-testing core of pentesting; real pentest roles add networks, Active Directory, cloud and report craft.
