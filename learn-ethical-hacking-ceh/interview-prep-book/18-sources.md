# Sources and Further Reading

> **A note on accuracy.** This edition was written on **16 November 2026**. Incident figures (people affected, organizations hit, dates) are *reported estimates* that differ between sources and change as investigations continue; the book rounds them and says "about", "reported" or "confirmed". Statistics come from **news coverage and vendor summaries of reports**, not always from the reports themselves. Check the primary source before quoting a number in an interview, and say "according to..." when you do.

## Standards and reference

- **OWASP Top 10:2025**: https://top10.owasp.org/2025 (the ten categories, the 2025 changes, SSRF merged into A01).
- **OWASP API Security Top 10 (2023)**: https://owasp.org/API-Security/ (BOLA is API1). Names of API1, API3 and API5 were confirmed from several summaries; the full list is from OWASP.
- **OWASP Top 10 for LLM Applications (2025)**: https://genai.owasp.org/llm-top-10/ (the ten entries were read from this page).
- **OWASP Top 10 for Agentic Applications (for 2026)**, published 9 December 2025: https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/ (the ten entries ASI01-ASI10 were read from OWASP's PDF).
- **OWASP Cheat Sheet Series**: https://cheatsheetseries.owasp.org (SQL injection, XSS, CSRF, password storage, authentication and more).
- **MITRE CWE** https://cwe.mitre.org and **MITRE ATT&CK** https://attack.mitre.org
- **NVD** https://nvd.nist.gov and **FIRST CVSS** https://www.first.org/cvss
- **CISA Known Exploited Vulnerabilities catalog**: https://www.cisa.gov/known-exploited-vulnerabilities-catalog
- **NIST post-quantum cryptography**: https://csrc.nist.gov/projects/post-quantum-cryptography (FIPS 203, 204, 205 published 13 August 2024); **NIST IR 8547** final, 27 October 2026: https://csrc.nist.gov/pubs/ir/8547/final (deprecate quantum-vulnerable public-key algorithms after 2030, disallow after 2035; read from the report text). NIST's explainer on "harvest now, decrypt later": https://www.nist.gov/cybersecurity/what-post-quantum-cryptography
- **NIST SP 800-61** (incident handling): the lifecycle Chapter 11 summarizes.

## Threat-landscape data (2026)

- **Verizon 2026 Data Breach Investigations Report** (released May 2026), as reported by [TechTarget](https://www.techtarget.com/cybersecurity/news/366643420/Verizon-2026-DBIR-6-key-takeaways-for-CISOs) and [Help Net Security](https://www.helpnetsecurity.com/2026/05/20/verizon-2026-dbir-findings/). Used for: exploitation 31% (from 20%), credential abuse 13% (from 22%), pretexting 6%, third-party involvement 48% (from 30%), ransomware in 48% of breaches, 69% of ransomware victims did not pay, median payment about $140,000, only 26% of known-exploited flaws fully fixed, median 43 days to fix. The two articles agree on these; they differ on a few other details (for example how fast "shadow AI" grew), which the book omits. Neither article reports a phishing percentage. The full report is at verizon.com/business/resources/reports/dbir/.
- **Cloudflare DDoS Threat Report H1 2026**, published 11 August 2026: https://blog.cloudflare.com/ddos-threat-report-2026-h1/ (23.2 million network-layer attacks, 29.64 trillion HTTP requests, 935 attacks above 1 Tbps with 805 in Q2, DNS-based 34.3%, 96.62% under 500 Mbps, 90.60% ended within 10 minutes; SYN floods not named).
- **TechCrunch, "The worst hacks and breaches of 2026 so far"** (15 September 2026 version): https://techcrunch.com/2026/09/15/the-worst-hacks-and-breaches-of-2026-so-far/ (Klue, the 2026 developer-tool supply-chain wave, the Instagram/Meta AI chatbot case, exposed document stores, ShinyHunters incidents). A roundup based on other outlets' reporting, so each case is labelled confirmed or reported in the text.

## Incident case studies used in this book

- **MOVEit Transfer (2023):** CVE-2023-34362 SQL injection exploited by Cl0p. [Wikipedia summary with Emsisoft's August 2024 tally](https://en.wikipedia.org/wiki/2023_MOVEit_data_breach); [Help Net Security](https://www.helpnetsecurity.com/2023/09/26/moveit-victim-number/). Counts differ by date (about 2,773 organizations and nearly 96 million people in the latest tally found).
- **Snowflake customers (2024):** compromised credentials, mostly from infostealers, no MFA; at least 165 organizations. [Dark Reading](https://darkreading.com/threat-intelligence/snowflake-account-attacks-driven-by-exposed-legitimate-credentials), [Infosecurity Magazine](https://infosecurity-magazine.com/news/threat-actor-breaches-snowflake), [CIO Dive](https://www.ciodive.com/news/snowflake-customers-attacked-mandiant/718507/). The "100 million people" figure comes mainly from secondary sites.
- **Change Healthcare (2024):** a Citrix portal without MFA, stolen credentials, nine days of movement. [TechTarget](https://www.techtarget.com/cybersecurity/news/366582824/Change-Healthcare-breached-via-Citrix-portal-with-no-MFA), [SecurityWeek](https://www.securityweek.com/change-healthcare-ransomware-attack-impacts-100-million-people/). The affected count was revised upward over time (about 100 million at first, later reported as about 192.7 million).
- **XZ Utils (2024):** CVE-2024-3094. [Akamai](https://www.akamai.com/blog/security-research/critical-linux-backdoor-xz-utils-discovered-what-to-know), [Dark Reading](https://www.darkreading.com/cyber-risk/xz-utils-backdoor-implanted-in-intricate-multi-year-supply-chain-attack).
- **Marks & Spencer (2025) and MGM Resorts (2023):** help-desk social engineering linked to Scattered Spider. [BleepingComputer](https://www.bleepingcomputer.com/news/security/marks-and-spencer-breach-linked-to-scattered-spider-ransomware-attack/). Public reporting; details of the calls are not fully confirmed.
- **Salesloft Drift (2025):** stolen OAuth tokens. [The Hacker News](https://thehackernews.com/2025/08/salesloft-oauth-breach-via-drift-ai.html), [Security Boulevard](https://securityboulevard.com/2025/09/breach-of-salesloft-drift-oauth-tokens-leads-to-salesforce-data-theft/). The 700+ figure is Google's early estimate; scope details were still being revised.
- **Shai-Hulud npm worm (2025):** [Help Net Security (September wave)](https://www.helpnetsecurity.com/2025/09/16/self-replicating-worm-hits-180-npm-packages-in-largely-automated-supply-chain-attack/), [CyberScoop](https://cyberscoop.com/supply-chain-attack-shai-hulud-npm/) (November wave).
- **EchoLeak (2025):** CVE-2025-32711, Microsoft 365 Copilot. [The Hacker News](https://thehackernews.com/2025/06/zero-click-ai-vulnerability-exposes.html), [arXiv paper](https://arxiv.org/html/2509.10540v1).
- **HTTP/2 Rapid Reset (2023):** CVE-2023-44487. [TechTarget](https://www.techtarget.com/cybersecurity/news/366554941/Rapid-Reset-DDoS-attacks-exploiting-HTTP-2-vulnerability) (Google's reported peak of about 398 million requests per second).
- **Capital One (2019):** the SSRF "textbook case". [Krebs on Security](https://krebsonsecurity.com/2019/08/what-we-can-learn-from-the-capital-one-hack/); the exact technical path is partly reconstructed from court filings.
- **SolarWinds (2020):** mentioned only as the classic ancestor of supply-chain attacks.

**Not re-verified for this edition:** the claim that Log4Shell's CVSS is 10.0 (Lab 5 has you confirm it on the NVD), and general statements such as "SameSite=Lax is the default in Chrome and Edge", "WPA3 is the current Wi-Fi standard" and details of AWS IMDSv2, which come from general knowledge.

## Practice platforms (all free to start)

- **PortSwigger Web Security Academy**: https://portswigger.net/web-security (including the *Web LLM attacks* topic)
- **TryHackMe**: https://tryhackme.com
- **OWASP Juice Shop**: https://owasp.org/www-project-juice-shop/
- **Wireshark documentation**: https://www.wireshark.org/docs/ · **Nmap**: https://nmap.org (practice target https://scanme.nmap.org)
- **Have I Been Pwned**: https://haveibeenpwned.com · **WebAuthn demo**: https://webauthn.io

## Your Indonesian book

*Ethical Hacking dari Nol: Buku Ajar* is a full CEH-oriented course. Use it as a deeper companion for the older fundamentals (the chapter map is in [00-start-here.md](00-start-here.md)); it predates this edition's focus on identity, supply chain and AI, and skipping its Linux, Bash, Python and exam-simulation chapters suits this one-month goal.
