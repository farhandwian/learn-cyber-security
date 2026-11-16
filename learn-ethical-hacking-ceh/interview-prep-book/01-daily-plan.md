# Daily Plan: 28 Days

Each weekday session is about 1.5 hours, Saturday is a 3-hour lab block, Sunday is 1 hour, and Friday is rest. Total: roughly 10 hours a week.

**Every session starts the same way (5 minutes):** close everything, write down what you remember from the previous session, then check against your notes. This is spaced repetition; it is the cheapest memory boost there is.

**Every session ends the same way (2 minutes):** write one sentence: "Today I learned ___, and the interview question it answers is ___."

> **Definition of done.** Each row has an *output*. If you can produce it without looking at the book, the day counts.

---

## Week 1: Foundations (≈10 h)

| Day | Time | Do | Output (proof you're done) |
| --- | --- | --- | --- |
| Mon | 1.5 h | Read [02-threat-landscape-2026.md](02-threat-landscape-2026.md) in full | Say the three "doors" breaches use today, with one number |
| Tue | 1.5 h | Read [03-security-basics.md](03-security-basics.md); take the quiz | Draw the CIA triangle and the 5 phases from memory |
| Wed | 1.5 h | Read [04-cryptography.md](04-cryptography.md) sections 1-4 (hashing, passwords, sym/asym). Do **Lab 1** (code). | Explain "why not MD5 for passwords" in 30 seconds |
| Thu | 1.5 h | Finish chapter 4 (certificates, TLS, post-quantum). Take the quiz. | Draw the TLS handshake on paper |
| Fri | rest | Nothing. Sleep is part of memory. | - |
| Sat | 3 h | Read [05-networking-and-web.md](05-networking-and-web.md). Do **Lab 2** (Wireshark) and **Lab 3** (headers). | Screenshot of a TCP handshake you captured |
| Sun | 1 h | Teach-back: narrate "what happens when you type https://bank.com" out loud, one risk per step. Quiz chapter 5. | A 2-minute spoken answer, no notes |

## Week 2: Recon, vulnerabilities and web flaws (≈10 h)

| Day | Time | Do | Output |
| --- | --- | --- | --- |
| Mon | 1.5 h | Read [06-recon-and-scanning.md](06-recon-and-scanning.md) sections 1-3 (legal, passive vs active, nmap) | Explain open / closed / filtered with the handshake |
| Tue | 1.5 h | Finish chapter 6 (CVE/CVSS/KEV, patching). **Lab 4** (nmap on scanme) and **Lab 5** (read a CVE). | Translate a CVSS vector into plain English |
| Wed | 1.5 h | Read [07-injection-and-xss.md](07-injection-and-xss.md) sections 1-3 (OWASP map, injection idea, SQLi) | Recite the OWASP Top 10 in 5 groups |
| Thu | 1.5 h | Finish chapter 7 (XSS). Quiz. **Lab 7** and **Lab 8** (your own code: SQLi and XSS, then the fix). | Before/after code on screen |
| Fri | rest | - | - |
| Sat | 3 h | **Lab 9** part 1: PortSwigger Web Security Academy (SQL injection and XSS apprentice labs). Redo Week 1 quizzes. | 4+ labs solved; one 3-sentence summary each |
| Sun | 1 h | Teach-back: "How would an attacker get into a company, and how would you stop them?" Use the five phases and the Verizon numbers. | A spoken answer with one example per phase |

## Week 3: Access, identity and phishing: the most valuable week (≈10 h)

| Day | Time | Do | Output |
| --- | --- | --- | --- |
| Mon | 1.5 h | Read [08-access-control-and-apis.md](08-access-control-and-apis.md) sections 1-3 (AuthN vs AuthZ, BOLA/IDOR, API Top 10) | Explain 401 vs 403 and why BOLA is #1 for APIs |
| Tue | 1.5 h | Finish chapter 8 (CSRF, SSRF, API checklist). Quiz. | Say what / how / fix for CSRF and SSRF |
| Wed | 1.5 h | Read [09-identity-and-phishing.md](09-identity-and-phishing.md) sections 1-3 (stolen logins, infostealers, the MFA ladder) | Draw the MFA ladder and name what beats each rung |
| Thu | 1.5 h | Finish chapter 9 (AiTM, passkeys, OAuth tokens, help-desk attacks). Quiz. **Lab 6** (check your own accounts, try a passkey). | Explain why a passkey stops an AiTM phish |
| Fri | rest | - | - |
| Sat | 3 h | **Lab 9** part 2: PortSwigger access-control and CSRF labs, then the Web LLM attacks intro | 6+ labs total solved; one 3-sentence summary each |
| Sun | 1 h | Teach-back all of Weeks 2-3 attacks: what / how / fix / recent case. | Say all of them without notes |

## Week 4: Defence, new risks, review (≈10 h)

| Day | Time | Do | Output |
| --- | --- | --- | --- |
| Mon | 1.5 h | Read [10-network-attacks-and-ddos.md](10-network-attacks-and-ddos.md) (1 h) and start [11-ransomware-and-incident-response.md](11-ransomware-and-incident-response.md) | Place firewall, IDS, IPS, WAF on a sketch |
| Tue | 1.5 h | Finish chapter 11. Read [12-supply-chain-cloud-devsecops.md](12-supply-chain-cloud-devsecops.md). **Lab 10** (audit your own project's dependencies). | The 5 incident-response steps and the 6 STRIDE letters |
| Wed | 1.5 h | Read [13-ai-and-llm-security.md](13-ai-and-llm-security.md). **Lab 11** (prompt-injection toy). | Explain prompt injection and "excessive agency" in 60 seconds |
| Thu | 1.5 h | [14-qa-bank.md](14-qa-bank.md) round 1: answer **out loud**, then compare. Mark green / yellow / red. If you have 20 spare minutes, sketch **Lab 12** (STRIDE). | A coloured list of 45 questions |
| Fri | rest | - | - |
| Sat | 3 h | **Lab 13**: mock interview. Record yourself answering 15 random questions. Watch it back. Redo the red ones. | A list of three things to fix |
| Sun | 1 h | Final pass on [16-cheat-sheets.md](16-cheat-sheets.md). Prepare your own "war story" (see below). Early night. | Your 2-minute war story |

> **Your war story.** Interviewers remember stories, not definitions. Prepare one real example from your own work: a security bug you caught in code review, a dependency CVE you patched, an auth flaw you fixed. Structure: situation, what you did, outcome, what changed afterwards.

---

## If you fall behind

1. Drop optional labs first (Lab 14 Juice Shop, extra TryHackMe rooms).
2. Merge Week 2's lighter days into Week 1 or 3, but **never shorten Week 3**.
3. Keep the Sunday teach-backs: they are the highest-value hour of the week.
4. If you have only one hour tonight: do one lab and answer five questions from the Q&A bank out loud.
