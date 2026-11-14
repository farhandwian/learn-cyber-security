# Daily Plan: 28 Days

Each weekday session is about 1.5 hours, Saturday is a 3-hour lab block, Sunday is 1 hour, and Friday is rest. Total: roughly 10 hours a week.

**Every session starts the same way (5 minutes):** close everything, write down what you remember from the previous session, then check against your notes. This is spaced repetition; it is the cheapest memory boost there is.

**Every session ends the same way (2 minutes):** write one sentence: "Today I learned ___, and the interview question it answers is ___."

> **Definition of done.** Each row has an *output*. If you can produce it without looking at the book, the day counts.

---

## Week 1: Foundations (≈10 h)

| Day | Time | Do | Output (proof you're done) |
| --- | --- | --- | --- |
| Mon | 1.5 h | Read [02-security-basics.md](02-security-basics.md) sections 1-4 (CIA, vocabulary, phases) | Draw the CIA triangle and the 5 phases from memory |
| Tue | 1.5 h | Finish chapter 02 (who's who, assessment vs pentest). Take the quiz. | Quiz 5 of 6 or better |
| Wed | 1.5 h | Read [03-cryptography.md](03-cryptography.md) sections 1-3 (hashing, password storage). Do **Lab 1** (code). | Explain "why not MD5 for passwords" in 30 seconds |
| Thu | 1.5 h | Finish chapter 03 (sym/asym, certificates, TLS). Take the quiz. | Draw the TLS handshake on paper |
| Fri | rest | Nothing. Sleep is part of memory. | - |
| Sat | 3 h | Read [04-networking-and-web.md](04-networking-and-web.md). Do **Lab 2** (Wireshark) and **Lab 3** (headers). | Screenshot of a TCP handshake you captured |
| Sun | 1 h | Teach-back: narrate "what happens when you type https://bank.com" out loud, with one risk per step. Quiz chapter 04. | A 2-minute spoken answer, no notes |

## Week 2: Recon and scanning (≈10 h)

Reading is lighter this week; the extra time goes into hands-on work and reviewing Week 1.

| Day | Time | Do | Output |
| --- | --- | --- | --- |
| Mon | 1.5 h | Read [05-recon-and-scanning.md](05-recon-and-scanning.md) sections 1-2 (legal, passive vs active, OSINT) | Name 5 passive sources and what each reveals |
| Tue | 1.5 h | Sections 3-4 (nmap, port states, enumeration) | Explain open / closed / filtered with the handshake |
| Wed | 1.5 h | **Lab 4**: nmap on scanme.nmap.org | Annotated output: what is exposed and why it matters |
| Thu | 1.5 h | Sections 5-6 (CWE/CVE/CVSS, real cases). **Lab 5**: look up Log4Shell. Quiz. | Translate a CVSS vector into plain English |
| Fri | rest | - | - |
| Sat | 3 h | TryHackMe: complete a Nmap room and one network fundamentals room. Then redo the Week 1 quizzes. | Both quizzes at 80% or better |
| Sun | 1 h | Teach-back: "Walk me through how an attacker would find a way into a company." Use the five phases. | A spoken answer with one example per phase |

## Week 3: Web attacks, the most valuable week (≈10 h)

| Day | Time | Do | Output |
| --- | --- | --- | --- |
| Mon | 1.5 h | Read [06-injection-and-xss.md](06-injection-and-xss.md) sections 1-3 (OWASP map, injection idea, SQLi) | Recite the OWASP Top 10 in 5 groups |
| Tue | 1.5 h | Sections 4-6 (other injections, XSS, interview). Quiz. | Explain SQLi and XSS and their fixes in 90 seconds each |
| Wed | 1.5 h | **Lab 7** and **Lab 8** (your own code: SQL injection and XSS, then the fix) | Before/after code on screen |
| Thu | 1.5 h | Read [07-access-auth-requests.md](07-access-auth-requests.md) sections 1-3 (IDOR, auth, sessions) | Explain 401 vs 403 and why IDOR is #1 |
| Fri | rest | - | - |
| Sat | 3 h | **Lab 9**: PortSwigger Web Security Academy (SQL injection, XSS, access control, CSRF apprentice labs) | 6+ labs solved; one 3-sentence summary each |
| Sun | 1 h | Read chapter 07 sections 4-6 (CSRF, SSRF, API checklist). Teach-back all six attacks. | Say what / how / fix for each of the six |

## Week 4: Systems, people, review (≈10 h)

| Day | Time | Do | Output |
| --- | --- | --- | --- |
| Mon | 1.5 h | Read [08-network-attacks-defenses.md](08-network-attacks-defenses.md) | Place firewall, IDS, IPS, WAF on a network sketch |
| Tue | 1.5 h | Read [09-people-malware-incident-response.md](09-people-malware-incident-response.md) | Name the 5 incident-response steps and 6 STRIDE letters |
| Wed | 1.5 h | [10-qa-bank.md](10-qa-bank.md) round 1: read each question, answer **out loud**, then compare | Mark each question green / yellow / red |
| Thu | 1.5 h | **Lab 11**: threat-model a feature you built (STRIDE). Review red and yellow questions. | One STRIDE table |
| Fri | rest | - | - |
| Sat | 3 h | **Lab 12**: mock interview. Record yourself answering 15 random questions. Watch it back. | A list of three things to fix |
| Sun | 1 h | Final pass on [12-cheat-sheets.md](12-cheat-sheets.md). Prepare your own "war story" (see below). Early night. | Your 2-minute war story |

> **Your war story.** Interviewers remember stories, not definitions. Prepare one real example from your own work: a security bug you caught in code review, a dependency CVE you patched, an auth flaw you fixed. Structure: situation, what you did, outcome, what changed afterwards.

---

## If you fall behind

1. Drop optional labs first (Juice Shop, extra TryHackMe rooms).
2. Merge Week 2's lighter days into Week 1 or 3, but **never shorten Week 3**.
3. Keep the Sunday teach-backs: they are the highest-value hour of the week.
4. If you have only one hour tonight: do one lab and answer five questions from the Q&A bank out loud.
