# Study Recommendation

Written 19 November 2026. This is my advice for using `Interview_Prep_AI_Agent_Era.pdf`. It is not part of the PDF.

## Your situation

- You are interviewing for a **cybersecurity job**, and the interview is mostly a **formality**.
- You are a software engineer, but you are **not yet comfortable with networking and the web**.
- In the job you expect to **operate an app, do a little security, and ask AI a lot**.
- Time: about 10 hours a week for 4 weeks (about 40 hours).
- Goals: **minimum** = pass the formal interview; **best case** = also be able to pass CEH.

## What to prioritise

**1. Foundations first (about 12 h).** Everything else builds on these.
- Chapter 2 Basics: CIA triad, risk, least privilege, defence in depth, CVE and CVSS.
- Chapter 4 Networking and web: what happens when you open a URL (DNS, TCP handshake, TLS, HTTP).
- Chapter 3 Cryptography: hash vs encrypt vs encode, symmetric vs asymmetric, TLS in two sentences.

**2. Core interview topics (about 18 h).**
- Chapter 5 Recon and scanning: passive vs active, what `nmap` shows, port states, legal rules.
- Chapter 6 Appsec core: SQL injection, XSS, CSRF, IDOR, with the fix for each.
- Chapter 7 Identity and phishing: phishing, MFA, passwords, social engineering.
- Chapter 9 Ransomware and incident response: know the IR phases.

**3. Key points (about 12 h).**
- Chapter 11 AI and agent security: prompt injection, the OWASP LLM list, agent-safety rules. Most relevant to your job.
- Chapters 15 and 16: CEH gap terms (IDS vs IPS vs WAF, malware types, enumeration, wireless, IoT) and working with AI.
- Chapters 1, 8, 10: skim for the main points and one or two numbers, said with "according to".

**4. Practise and recall (about 10 h).**
- Chapter 12 Q&A: pick about 25 of the 48 questions and say each aloud twice.
- Chapter 14 Glossary: read it twice; interviewers test vocabulary.
- Chapter 13 Labs: do three only: Juice Shop, `nmap` on your own machine, one agent lab.

The total is about 50 hours. To fit 40, read Chapter 10 once, skip Chapter 1 beyond its numbers, and do three labs. Keep Weeks 1 and 2 intact.

## Week by week

| Week | Chapters | Check |
| --- | --- | --- |
| 1 | 2, 4, 3 | Explain aloud what happens when you open a URL |
| 2 | 5, 6, 7 | Find two bugs in Juice Shop; run `nmap` on your own machine |
| 3 | 9, 8, 10, 1 | Walk through a ransomware timeline and the IR phases aloud |
| 4 | 11, 15, 16, then 12 and 14 | About 25 questions aloud twice; two mock interviews |

## How to study

- Weekday (about 90 minutes): 30 read, 30 lab, 20 saying answers aloud, 10 writing what you got wrong.
- If a foundation chapter feels hard, stay on it an extra day. A weak base makes later chapters feel like memorising.
- Cover the answers in each "Check yourself" and try first.
- Use AI to explain things you do not understand, then check against the book or the vendor documentation.

## For your job, not just the interview

Learn to explain an alert, an IP address, a CVE and a command in plain words, and to say how you would check an AI answer (Chapter 16). That matters more than memorising tools.

## What you can skip

- The cheat-sheet tables beyond the glossary.
- Detailed code in Chapter 6 (understand the idea, not the syntax).
- Deep protocol detail in Chapter 4 beyond the URL journey and the TCP and TLS handshakes.

## What the book does not give you

- **Tool practice.** To use Nmap, Wireshark or Burp for real, use TryHackMe or PortSwigger Web Security Academy.
- **CEH exam detail.** The CEH v13 brochure lists 20 modules and a 125-question, 4-hour knowledge exam (passing score given as 60%-85%). Chapter 15 covers the gap topics at definition level only. Passing CEH would need the courseware and lab time on top.
- **Verified AI-tool incident details.** AI-agent incidents and CVEs in Chapter 11 are labelled "reported"; check the vendor advisory before quoting one.

## Levels

| Goal | What is enough |
| --- | --- |
| **Minimum:** formal interview | Steps 1 and 2, Chapter 11, and the Q&A and glossary |
| **Good:** confident interview | All four steps |
| **Best case:** CEH | All four steps, then the CEH courseware, plus lab time on enumeration, system hacking, malware, wireless and mobile |
