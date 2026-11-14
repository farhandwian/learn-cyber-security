# Security Interview Prep: 4-Week Crash Course

*Illustrated edition. Written for a working software engineer who has one month, about 10 hours a week, and one goal: pass a security-flavoured technical interview.*

> **Goal.** After four weeks you can (1) explain core security ideas in plain English, (2) narrate how HTTPS, hashing and the OWASP Top 10 work, (3) answer any "what is X?" question in four steps (what, how it is exploited, how to prevent it, a real incident), and (4) run basic scans and web labs on legal targets.
>
> **Not a goal.** Becoming a penetration tester or passing the CEH exam. That is why this book skips the terminal basics, Python and Bash, which you already know.

---

## 1. How this book teaches

Good courses are built on a few well-tested learning techniques. This book uses all of them, so use them too:

| Technique | Why it works | How you apply it here |
| --- | --- | --- |
| **Dual coding** (picture + words) | You remember a diagram plus a sentence far better than text alone | Every chapter shows the idea as a diagram first. Look at the picture, *then* read. |
| **Chunking** | Working memory holds only a few items | Chapters are split into short sections with one idea each. |
| **Worked examples** | Seeing a full example beats abstract rules | Each attack has one concrete walkthrough and a before/after code fix. |
| **Active recall** | Pulling facts out of memory builds memory; re-reading does not | Close the book at the end of a section and write what you remember. Then do the *Check yourself* quiz. |
| **Spaced repetition** | Reviewing at growing intervals beats cramming | The [daily plan](01-daily-plan.md) starts every session with 5 minutes of recall from the last session. |
| **Teach-back** (Feynman technique) | If you can't explain it simply, you don't know it yet | Every Sunday you explain the week's topics out loud, as if to a junior developer. |
| **Real cases** | A story gives an abstract idea a place to live in your head | Each topic is tied to a real incident (Equifax, Capital One, SolarWinds and others). |
| **Interleaving** | Mixing topics trains you to *pick* the right idea | Week 4's question bank mixes everything on purpose. |

![Four-week roadmap](images/01-roadmap.svg)

![A realistic weekly rhythm](images/02-weekly-rhythm.svg)

---

## 2. The one answer shape to memorize

Almost every interview question has the same skeleton. Practise it until it is automatic.

![The 4-step answer for any security question](images/03-answer-framework.svg)

1. **What is it?** One plain sentence.
2. **How is it exploited?** One concrete example.
3. **How do you prevent it?** The fix in code or configuration. *This is where an engineer stands out.*
4. **When did it happen?** One real incident (a bonus that signals real knowledge).

> **Interview angle.** If you freeze, say the four steps silently in order. You will always have something sensible to say.

---

## 3. The chapters

| File | Topic | Week | Time | Matching chapters in your Indonesian book |
| --- | --- | --- | --- | --- |
| [01-daily-plan.md](01-daily-plan.md) | Day-by-day schedule for 28 days | all | - | - |
| [02-security-basics.md](02-security-basics.md) | CIA, vocabulary, attack phases, who's who | 1 | 2 h | Bab 0 |
| [03-cryptography.md](03-cryptography.md) | Hashing, encryption, TLS, password storage | 1 | 3 h | Bab 6, Tabel 13.4 |
| [04-networking-and-web.md](04-networking-and-web.md) | Layers, TCP, DNS, HTTP, cookies | 1 | 4 h | Bab 3, 4 |
| [05-recon-and-scanning.md](05-recon-and-scanning.md) | OSINT, nmap, CVE/CVSS | 2 | 10 h | Bab 7, 8 |
| [06-injection-and-xss.md](06-injection-and-xss.md) | OWASP Top 10, SQL injection, XSS | 3 | 5 h | Bab 11, 12 |
| [07-access-auth-requests.md](07-access-auth-requests.md) | IDOR, auth, sessions, CSRF, SSRF | 3 | 5 h | Bab 11, 12 |
| [08-network-attacks-defenses.md](08-network-attacks-defenses.md) | MITM, DoS, firewalls, IDS/IPS, WAF | 4 | 3 h | Bab 10, 11 |
| [09-people-malware-incident-response.md](09-people-malware-incident-response.md) | Social engineering, malware, supply chain, IR, STRIDE | 4 | 3 h | Bab 9, 10 |
| [10-qa-bank.md](10-qa-bank.md) | 40 interview questions with model answers | 4 | 4 h | Bab 14, 15 |
| [11-labs.md](11-labs.md) | Step-by-step hands-on labs | 1-4 | - | - |
| [12-cheat-sheets.md](12-cheat-sheets.md) | One-page revision tables | 4 | - | - |
| [13-glossary.md](13-glossary.md) | 68 terms in one line each | all | - | - |
| [14-sources.md](14-sources.md) | Sources, further reading, accuracy notes | all | - | - |

---

## 4. How every chapter is built

Every chapter has the same anatomy, so you always know where you are:

1. **Goal box** at the top: what you will be able to do afterwards.
2. **Big picture and analogy**, so the idea has a place to sit.
3. **Diagrams** with a one-line caption.
4. **Short sections**, one idea each, with a worked example.
5. **Common mistakes** and **interview angle** boxes.
6. **Check yourself**: a short quiz. The answers sit directly below, so cover them first.
7. **Summary**: five lines for the night before the interview.

Box labels you will see:

> **Analogy.** An everyday comparison to make the idea stick.

> **Real case.** A real incident that shows the idea in the wild.

> **Common mistake.** What beginners (and some interviewers' traps) get wrong.

> **Interview angle.** How to turn this topic into a strong answer.

> **Try it.** A short hands-on step. Longer labs live in [11-labs.md](11-labs.md).

---

## 5. Ground rules

1. **Legal first.** Test only systems you own, practice platforms (PortSwigger Web Security Academy, TryHackMe) or targets that explicitly invite scanning (scanme.nmap.org). "Just trying" on someone else's site is a crime in most countries, including under Indonesia's UU ITE.
2. **Type, don't paste.** Typing a command builds recall that reading cannot.
3. **Understand, don't memorize.** Interviewers follow up on *why*. A memorized list collapses at the first follow-up; an understood idea does not.
4. **Fall-behind rule.** If you lose a day, skip optional labs first. Never skip the Sunday teach-back or Week 3.

Start with [02-security-basics.md](02-security-basics.md), or open the [daily plan](01-daily-plan.md) to see exactly what to do tonight.
