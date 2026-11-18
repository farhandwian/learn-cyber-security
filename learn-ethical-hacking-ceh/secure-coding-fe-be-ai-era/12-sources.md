# Sources and Accuracy Notes

> **Written on 18 November 2026.** Security facts change quickly. Incident figures are *reported estimates*. Statistics from the Verizon report come from **news coverage of the report**, not the report itself. **Check the primary source before quoting a number in an interview and say "according to".** Labels: **read** = a page was read during writing; **reported** = taken from news or vendor summaries.

## Standards and guidance
- **OWASP Top 10:2025**: https://top10.owasp.org/2025 · **API Security Top 10 (2023)**: https://owasp.org/API-Security/ · **LLM Top 10 (2025)**: https://genai.owasp.org/llm-top-10/ (read in the earlier books) · **Agentic Applications Top 10**, published 9 Dec 2025: https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/ (published 9 Dec 2025; the ten entries ASI01-ASI10 were read from OWASP's PDF while writing the earlier book).
- **OWASP Cheat Sheet Series**: password-storage numbers (Argon2id 19 MiB, t=2, p=1; scrypt N=2^17, r=8, p=1; bcrypt cost 10+ and 72-byte limit; PBKDF2-HMAC-SHA256 600,000) read from https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html
- **OWASP ASVS 5.0** (May 2025): https://github.com/OWASP/ASVS (the "about 17 chapters, about 350 requirements" description is from secondary summaries).
- **MCP security best practices** (draft specification, read): https://modelcontextprotocol.io/specification/draft/basic/security_best_practices
- **Claude Code security documentation** (read; used as an example of documented controls): https://code.claude.com/docs/en/security
- **Joint government guidance "Careful Adoption of Agentic AI Services"** (NSA, CISA and partner agencies, around 30 Apr-1 May 2026): known from an agency press listing; the PDF was **not read**.
- **NIST** FIPS 203/204/205 (Aug 2024) and IR 8547 (as summarized in the earlier books).

## AI-agent era evidence
- **Package hallucination**: Spracklen et al., "We Have a Package for You!", USENIX Security 2025, https://arxiv.org/abs/2406.10279 (abstract read: 16 models, 576,000 samples, at least 5.2% commercial and 21.7% open-source, 205,474 unique names). The 19.7% overall average and newer-model figures are **reported**. Real-world slopsquatting cases are **reported**; details conflict.
- **AI code quality**: Veracode 2026 GenAI Code Security Report (28 Jul 2026, press release read: 56% pass rate, vendor research on raw models). The 2025 report's 45% figure is **reported** by several outlets.
- **Tool vulnerabilities** (all **reported** from security-vendor and news write-ups; the advisories were not read, so verify CVE IDs, scores and fixed versions at NVD or the vendor): GitHub Copilot CVE-2025-53773 (7.8 per NVD-derived sources; a "9.6" figure seen online is unverified); Cursor CVE-2025-54135 and CVE-2025-54136 (scores conflict between sources); several Claude Code CVEs (2025-26); Amazon Q Developer extension v1.84.0 (AWS bulletin AWS-2025-015); Pillar Security "Rules File Backdoor". Further 2026 CVEs mentioned in search results were not used.
- **MCP tool poisoning**: Invariant Labs, 1 Apr 2025, https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks (read). mcp-remote CVE-2025-6514 and MCP Inspector CVE-2025-49596 are **reported** only and are not used in the text.
- **Nx "s1ngularity" (Aug 2025)**: InfoQ, https://www.infoq.com/news/2025/10/npm-s1ngularity-shai-hulud (read: over 400 users or organizations, more than 5,500 repositories, more than 1,000 valid GitHub tokens) and Socket's write-up. Its relation to Shai-Hulud is described by sources as "related"; the book does not say they are the same.
- **AI-orchestrated espionage**: Anthropic, 13 Nov 2025, https://www.anthropic.com/news/disrupting-AI-espionage (read: 80-90% AI-executed, about 30 targets, a small number of successes, hallucinated credentials).
- **Exploit-speed claims**: vendor figures (Synack, Cogent, VulnCheck) use different metrics; the book says only that vendors report days or hours.
- **Agent incidents**: Replit (July 2025) reported by Fortune and others; PocketOS (Apr 2026) rests on the founder's own account. Other 2026 incident claims found in search results were **not used**.
- **Surveys**: SOUPS 2026 interview study (15 engineers) and vendor-sponsored surveys are **reported**; the book uses only the SOUPS point, labelled reported.

## Incidents carried over from the earlier books
- **Verizon 2026 DBIR (May 2026)**, as reported by TechTarget and Help Net Security; **React2Shell CVE-2025-55182** (React's advisory, read; CISA KEV 5 Dec 2025 from news); **Next.js CVE-2025-29927** (affected range varies by source; fixed versions 12.3.5, 13.5.9, 14.2.25, 15.2.3 agree; verify at GHSA-f82v-jwr5-mffw); **npm trusted publishing and token changes** (GitHub's posts); **chalk/debug (8 Sep 2025)**; **Shai-Hulud**; **tj-actions CVE-2025-30066**; **XZ Utils CVE-2024-3094**; **EchoLeak CVE-2025-32711**; **Cloudflare H1 2026 DDoS report**. The full source list is in the first two books' source chapters.
- Log4Shell's CVSS 10.0 and the ransomware median payment come from the first book and were not re-verified.

## Not independently verified (general knowledge)
`SameSite=Lax` defaults; `__Host-` cookie rules; Trusted Types support; Dependabot `cooldown`, Renovate and pnpm release-age settings; `connect-redis`, `jose`, `@simplewebauthn/server`, `file-type`, `multer`, `zod` API details; AWS IMDSv2. The seven **runnable labs were executed and pass** on Node 24 (in the earlier edition); the other snippets are illustrative. Test them in your stack.

## Practice platforms
PortSwigger Web Security Academy (https://portswigger.net/web-security), OWASP Juice Shop (https://owasp.org/www-project-juice-shop/), TryHackMe, Hack The Box Academy, webauthn.io.
