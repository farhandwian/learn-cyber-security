# Plan: 28 Days

Each weekday session is about 1.5 hours, Saturday is a 3-hour block, Sunday is 1 hour, and Friday is rest. About 10 hours a week.

**Start every session (5 minutes):** close everything and write down what you remember from the last session. **End every session (2 minutes):** write one sentence: "Today I learned ___, and I'd catch it in review by looking for ___."

> **Definition of done.** Each row has an *output*. If you can produce it without the book, the day counts.

---

## Week 1: Shared core (≈10 h)

| Day | Time | Do | Output |
| --- | --- | --- | --- |
| Mon | 1.5 h | Read [02-threat-model-for-developers.md](02-threat-model-for-developers.md); start [03-browser-and-http-security.md](03-browser-and-http-security.md) §1-2 (origin, cookies) | Draw the trust-boundary diagram from memory |
| Tue | 1.5 h | Finish chapter 3 (CSRF, CORS, headers). Quiz. | Explain CORS vs CSRF in 60 seconds |
| Wed | 1.5 h | Read [04-authentication-and-sessions.md](04-authentication-and-sessions.md) §1-4 (passwords, sessions, JWT) | State OWASP's Argon2id minimum and the JWT checklist |
| Thu | 1.5 h | Finish chapter 4 (OAuth + PKCE, passkeys, token storage). Quiz. **Lab 3** (JWT) and **Lab 5** (passwords). | Both labs show `PASS` |
| Fri | rest | - | - |
| Sat | 3 h | Set up the labs (`cd labs && npm install`). **Lab 1** (BOLA) and **Lab 2** (XSS + CSP). Re-read chapters 3-4 headings. | Break and fix the BOLA lab yourself |
| Sun | 1 h | Teach-back: "Where do you store a login token in a SPA, and why?" | A 2-minute spoken answer |

## Week 2: Authorization, APIs and input (≈10 h)

| Day | Time | Do | Output |
| --- | --- | --- | --- |
| Mon | 1.5 h | Read [05-authorization-and-api-design.md](05-authorization-and-api-design.md) §1-5 | Explain BOLA, BFLA and mass assignment with one fix each |
| Tue | 1.5 h | Finish chapter 5. Quiz. **Lab 6** (rate limiting). | Throttled attempts 6 and 7 |
| Wed | 1.5 h | Read [06-input-handling-and-injection.md](06-input-handling-and-injection.md) §1-4 (validation, SQLi, NoSQLi, commands) | Show a safe query in your own ORM |
| Thu | 1.5 h | Finish chapter 6 (deserialization, React2Shell, prototype pollution). Quiz. **Lab 4** (webhook HMAC). | Lab 4 shows `PASS` |
| Fri | rest | - | - |
| Sat | 3 h | **Lab 10** part 1: PortSwigger Academy (SQL injection, access control, API testing). Redo Week 1 quizzes. | 4+ labs solved, a 3-sentence summary each |
| Sun | 1 h | Teach-back: "Walk me through securing one API endpoint end to end." Use the request pipeline. | A 3-minute spoken answer |

## Week 3: Your track (≈10 h)

Do **both** chapters if you are full-stack; otherwise do your track deeply and skim the other.

| Day | Time | Do | Output |
| --- | --- | --- | --- |
| Mon | 1.5 h | **FE:** [07-frontend-security.md](07-frontend-security.md) §1-3 (XSS sinks, CSP, tokens). **BE:** [08-backend-security.md](08-backend-security.md) §1-3 (defaults, SSRF, uploads) | List the XSS sinks (FE) or the upload steps (BE) |
| Tue | 1.5 h | **FE:** §4-7 (secrets in bundles, third-party scripts, postMessage, redirects). **BE:** §4-6 (webhooks, secrets, errors) | One bug you'd flag in a PR |
| Wed | 1.5 h | **FE:** §8-9 (Next.js and RSC: Server Actions, middleware, React2Shell). **BE:** §7-9 (database, containers, cloud) | Explain CVE-2025-29927 and CVE-2025-55182 in one sentence each |
| Thu | 1.5 h | The other track's chapter, skim; **Lab 7** (SSRF). Quiz. | Lab 7 shows `PASS` |
| Fri | rest | - | - |
| Sat | 3 h | **Lab 10** part 2 (XSS, DOM-based, CORS, JWT labs). **Lab 2** DOM page in a browser. | 6+ Academy labs total |
| Sun | 1 h | Teach-back all of Weeks 1-3 as "bug, exploit, fix, test" | Say 10 of them without notes |

## Week 4: Delivery, AI and the interview (≈10 h)

| Day | Time | Do | Output |
| --- | --- | --- | --- |
| Mon | 1.5 h | Read [09-supply-chain-and-ci-cd.md](09-supply-chain-and-ci-cd.md). **Lab 8** (audit your own project). | A 3-line audit summary |
| Tue | 1.5 h | Read [10-ai-features-for-developers.md](10-ai-features-for-developers.md); [11-secure-code-review.md](11-secure-code-review.md) §1-2 | Say the AI "risky combination" |
| Wed | 1.5 h | **Lab 11**: the 15-snippet code-review drill, timed (30 min). Then §3-4 of chapter 11. | At least 12 of 15 found |
| Thu | 1.5 h | [12-interview-qa.md](12-interview-qa.md) round 1: answer out loud, mark green / yellow / red | Coloured list of 50 questions |
| Fri | rest | - | - |
| Sat | 3 h | **Lab 12**: mock interview. Record 15 random questions plus one design question. Watch it back. | Three things to fix |
| Sun | 1 h | Final pass on [14-cheat-sheets.md](14-cheat-sheets.md). Prepare your own **war story**. Early night. | Your 2-minute war story |

> **Your war story.** Pick one real example from your work: a bug you caught in review, a dependency you patched, an auth flaw you fixed. Say it as situation, what you did, outcome, what changed afterwards.

---

## If you fall behind

1. Drop Lab 9 and the second half of the PortSwigger labs first.
2. Never skip Lab 1, Lab 3, Lab 11 or the Sunday teach-backs.
3. If you only have an hour: run one lab and answer five questions from the bank out loud.
