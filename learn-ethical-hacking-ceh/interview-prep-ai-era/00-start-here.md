# Start Here

> **Goal.** After four weeks you can talk about security at a broad technical-interview level: the vocabulary, the common attacks and defences, how a breach and its response unfold, and how AI agents change the picture. You do not need to become a security professional.
>
> **Time:** one month at about 10 hours a week (evenings plus weekends). Reading all chapters takes about 12 hours; the rest is labs and speaking practice.

---

## What this book is

This is the **AI-agent-era edition of *Interview Prep: 4-Week Crash Course***. It keeps the original's breadth (basics, crypto, networks, scanning, web attacks, identity, DDoS, ransomware and incident response, supply chain, AI) and compacts it from about 35,000 to about 21,000 words (110 to about 77 pages). Every chapter from 1 to 11 has an **AI-agent era** callout, and Chapter 11 is rebuilt around AI features *and* AI coding agents. Rare and legacy cases were cut.

For the developer-focused deep dive (code, labs, secure code review), use the companion book, *Secure Coding for FE and BE Engineers: AI-Agent-Era Edition*.

## The one idea

> **Security is mostly a small set of ideas applied everywhere: least privilege, validate at trust boundaries, defence in depth, patch fast, prepare to respond.** AI agents add a fast, confident new participant that reads untrusted content and acts with your permissions; the same ideas apply.

## The four-week plan

| Week | Chapters | Practice |
| --- | --- | --- |
| **1** | 1 Landscape and AI era, 2 Basics, 3 Cryptography, 4 Networking and web | Set up your lab (Ch 13); say the CIA triad and TLS handshake aloud |
| **2** | 5 Recon and scanning, 6 Application security core, 7 Identity and phishing | Juice Shop: two web bugs; `nmap` your own machine |
| **3** | 8 Network attacks and DDoS, 9 Ransomware and incident response, 10 Supply chain and cloud | Walk through a ransomware timeline aloud; audit one repo's dependencies |
| **4** | 11 AI and agent security, 12 Q&A, 14 Cheat sheets | Agent labs A1-A4; two mock interviews |

**Weekday rhythm (about 90 minutes):** 30 minutes read, 30 lab, 20 saying answers aloud, 10 writing what you got wrong. **Two-week version:** Chapters 1, 2, 6, 7, 9 and 11, plus Q&A.

## How to answer

![Answer framework](images/03-answer-framework.svg)

Use one shape: **threat, control (with a one-line example), a backup layer, how you would test it.**

## What to study first if time is short

![Study priority](images/34-study-priority.svg)

## Rules for practice

Test only systems you own, deliberately vulnerable training apps, training sites that invite attacks, or systems you have written permission to test. Scanning or attacking anything else is illegal in most countries.

## Accuracy

Security facts change quickly. Incident figures are reported estimates, and Verizon figures come from news coverage of the report. The last chapter says what was read and what is only reported. Say "according to" when you quote a number.
