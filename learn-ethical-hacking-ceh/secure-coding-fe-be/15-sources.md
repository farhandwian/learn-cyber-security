# Sources and Accuracy Notes

> **Written on 17 November 2026.** Security facts change quickly. Incident numbers (organizations affected, downloads, dates) are *reported estimates* that vary by source; this book rounds them and says "about" or "reported". Statistics from the Verizon report come from **news coverage of the report**, not the report itself. **Check the primary source before quoting a number in an interview, and say "according to".**

## Standards and guidance

- **OWASP Top 10:2025**: https://top10.owasp.org/2025
- **OWASP API Security Top 10 (2023)**: https://owasp.org/API-Security/ (BOLA is API1; names of API1, API3 and API5 were confirmed across several summaries)
- **OWASP Top 10 for LLM Applications (2025)**: https://genai.owasp.org/llm-top-10/ (read from the page)
- **OWASP Top 10 for Agentic Applications (for 2026)**, 9 December 2025: https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/
- **OWASP Cheat Sheet Series**: https://cheatsheetseries.owasp.org. The password-storage numbers (Argon2id 19 MiB / t=2 / p=1; scrypt N=2^17, r=8, p=1; bcrypt work factor 10+ and 72-byte limit; PBKDF2-HMAC-SHA256 600,000) were read from the [Password Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html).
- **OWASP ASVS 5.0** (released May 2025): https://github.com/OWASP/ASVS. The "about 17 chapters, about 350 requirements" description comes from secondary summaries ([SoftwareMill](https://softwaremill.com/whats-new-in-asvs-5-0/)); confirm in the standard itself.
- **CISA Known Exploited Vulnerabilities catalog**: https://www.cisa.gov/known-exploited-vulnerabilities-catalog

## Incidents and advisories used

- **Verizon 2026 DBIR (May 2026)**, as reported by [TechTarget](https://www.techtarget.com/cybersecurity/news/366643420/Verizon-2026-DBIR-6-key-takeaways-for-CISOs) and [Help Net Security](https://www.helpnetsecurity.com/2026/05/20/verizon-2026-dbir-findings/): exploitation about 31% (from 20%), credential abuse about 13%, third parties about 48% of breaches, 26% of known-exploited flaws fully fixed, median 43 days.
- **React2Shell, CVE-2025-55182 (CVSS 10)**: [React's advisory](https://react.dev/blog/2025/12/03/critical-security-vulnerability-in-react-server-components) (affected packages and versions, fixed versions, the "even without Server Functions" note; read from the page). CISA KEV addition on 5 December 2025 and the active exploitation are from news and vendor reporting, e.g. [The Hacker News](https://thehackernews.com/2025/12/critical-react2shell-flaw-added-to-cisa.html) and [The Register](https://www.theregister.com/2025/12/12/vulnerable_react_instances_unpatched/). The advisory's Next.js fixed-version list differs slightly between its text and its commands; check the Next.js advisory before pinning.
- **Next.js middleware bypass, CVE-2025-29927 (CVSS 9.1)**: [Fastly](https://fastly.com/blog/cve-2025-29927-authorization-bypass-in-next-js), [Snyk](https://snyk.io/blog/cve-2025-29927-authorization-bypass-in-next-js-middleware). I could not read the primary Vercel/GitHub advisory in this session, so the **affected-version range varies between sources**; the fixed versions (12.3.5, 13.5.9, 14.2.25, 15.2.3) agree. Verify at the Next.js advisory (GHSA-f82v-jwr5-mffw).
- **npm supply-chain changes**, from GitHub's posts: [Our plan for a more secure npm supply chain (Sep 2025)](https://github.blog/security/supply-chain-security/our-plan-for-a-more-secure-npm-supply-chain/), [trusted publishing GA (31 Jul 2025)](https://github.blog/changelog/2025-07-31-npm-trusted-publishing-with-oidc-is-generally-available/), [classic tokens disabled (5 Nov 2025)](https://github.blog/changelog/2025-11-05-npm-security-update-classic-token-creation-disabled-and-granular-token-changes/), [classic tokens revoked (9 Dec 2025)](https://github.blog/changelog/2025-12-09-npm-classic-tokens-revoked-session-based-auth-and-cli-token-management-now-available). The September plan mentioned 7-day token lifetimes; the implemented limit was 90 days.
- **chalk/debug compromise (8 Sep 2025)**: [Check Point](https://blog.checkpoint.com/crypto/the-great-npm-heist-september-2025/), [Endor Labs](https://endorlabs.com/learn/major-supply-chain-attack-compromises-popular-npm-packages-including-chalk-and-debug), [Kaspersky](https://www.kaspersky.co.in/blog/npm-packages-trojanized/29528/). Sources disagree on the package count (18 to 25) and the exposure window; the book says "about 18" and "hours".
- **Shai-Hulud npm worm (Sep and Nov 2025)**: [Help Net Security](https://www.helpnetsecurity.com/2025/09/16/self-replicating-worm-hits-180-npm-packages-in-largely-automated-supply-chain-attack/), [CyberScoop](https://cyberscoop.com/supply-chain-attack-shai-hulud-npm/).
- **tj-actions/changed-files, CVE-2025-30066 (Mar 2025)**: [Wiz](https://www.wiz.io/blog/github-action-tj-actions-changed-files-supply-chain-attack-cve-2025-30066), [The Hacker News](https://thehackernews.com/2025/03/github-action-compromise-puts-cicd.html), [Checkmarx](https://checkmarx.com/zero-post/compromised-github-actions-leading-to-credential-leaks/). The "23,000+ repositories" figure is reported; sources differ on exact start times.
- **XZ Utils backdoor, CVE-2024-3094**: [Akamai](https://www.akamai.com/blog/security-research/critical-linux-backdoor-xz-utils-discovered-what-to-know).
- **MOVEit Transfer, CVE-2023-34362**: [Wikipedia summary with Emsisoft's August 2024 tally](https://en.wikipedia.org/wiki/2023_MOVEit_data_breach), [Help Net Security](https://www.helpnetsecurity.com/2023/09/26/moveit-victim-number/).
- **Salesloft Drift (Aug 2025)**: [The Hacker News](https://thehackernews.com/2025/08/salesloft-oauth-breach-via-drift-ai.html).
- **EchoLeak, CVE-2025-32711 (CVSS 9.3)**: [The Hacker News](https://thehackernews.com/2025/06/zero-click-ai-vulnerability-exposes.html), [arXiv paper](https://arxiv.org/html/2509.10540v1).
- **2026 developer-tool compromises, the Instagram/Meta AI chatbot case, exposed document stores, Klue**: [TechCrunch, "The worst hacks and breaches of 2026 so far"](https://techcrunch.com/2026/09/15/the-worst-hacks-and-breaches-of-2026-so-far/), a roundup built on other outlets' reporting. Treat them as *reported* unless the text says "confirmed".
- **MGM (2023) and Marks & Spencer (2025) help-desk attacks**: [BleepingComputer](https://www.bleepingcomputer.com/news/security/marks-and-spencer-breach-linked-to-scattered-spider-ransomware-attack/); public reporting, details not fully confirmed.
- **Capital One (2019), the SSRF textbook case**: [Krebs on Security](https://krebsonsecurity.com/2019/08/what-we-can-learn-from-the-capital-one-hack/).

## Not independently verified for this edition (general knowledge)

`SameSite=Lax` as Chrome and Edge's default; `__Host-` cookie prefix rules; Trusted Types browser support; Dependabot `cooldown`, Renovate and pnpm `minimumReleaseAge`; `npm sbom`; `connect-redis`, `jose`, `@simplewebauthn/server`, `file-type`, `multer` and `zod` API details; AWS IMDSv2; the OWASP API Security Top 10 entries other than API1, API3 and API5. The **runnable labs were executed and pass** on Node 24; the other snippets are illustrative and should be tested in your stack.

## Practice platforms

- **PortSwigger Web Security Academy**: https://portswigger.net/web-security (topics listed in Lab 10, including Web LLM attacks)
- **OWASP Juice Shop**: https://owasp.org/www-project-juice-shop/
- **WebAuthn demo**: https://webauthn.io

## The companion book

*Interview Prep: 4-Week Crash Course* (the `interview-prep-book/` folder) covers the broader cybersecurity topics this edition leaves out: scanning with nmap, malware, networks, ransomware and incident response, and the CVE/CVSS vocabulary.
