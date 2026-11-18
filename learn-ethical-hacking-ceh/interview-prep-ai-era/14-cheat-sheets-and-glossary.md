# Chapter 14: Cheat Sheets and Glossary

> **Goal.** Hold the facts interviewers expect instantly. If you cannot explain a row out loud, go back to its chapter.
>
> **Time:** about 30 minutes to review the evening before the interview.

---

## 1. The answer shape

**What is it? → How is it exploited? → How do you prevent it (a control, a backup layer, a test)? → A recent real case.** Always end with the fix.

## 2. Latest numbers (say "according to" and round)

| Fact | Number | Source |
| --- | --- | --- |
| Top way breaches start | Exploiting a vulnerability, about **31%** (was 20%) | Verizon DBIR 2026, as reported |
| Stolen credentials / pretexting | about **13%** / about **6%** | Verizon DBIR 2026, as reported |
| Third-party involvement | about **48%** (was 30%) | Verizon DBIR 2026, as reported |
| Ransomware in breaches | about **48%**; **69%** of victims did not pay | Verizon DBIR 2026, as reported |
| Known-exploited flaws fully fixed | about **26%**; median **43 days** | Verizon DBIR 2026, as reported |
| DDoS, H1 2026 | **23.2 million** network-layer; **935** above 1 Tbps; **96.62%** under 500 Mbps; **90.60%** over within 10 minutes | Cloudflare H1 2026 |
| Post-quantum standards | FIPS **203** (ML-KEM), **204** (ML-DSA), **205** (SLH-DSA), Aug 2024 | NIST |
| RSA/ECC timeline | deprecated after **2030**, disallowed after **2035** | NIST IR 8547 (final, Oct 2026) |
| Log4Shell CVSS | **10.0** (CVE-2021-44228); verify in NVD | NVD |
| AI-hallucinated packages | at least **5.2%** (commercial), **21.7%** (open-source models) | USENIX Security 2025 study |
| AI-orchestrated espionage | **80-90%** AI-executed, about **30** targets | Anthropic, 13 Nov 2025 |

## 3. OWASP lists

**Web Top 10 (2025):** A01 Broken Access Control · A02 Security Misconfiguration · A03 Software Supply Chain Failures *(new)* · A04 Cryptographic Failures · A05 Injection · A06 Insecure Design · A07 Authentication Failures · A08 Software or Data Integrity Failures · A09 Security Logging and Alerting Failures · A10 Mishandling of Exceptional Conditions *(new)*. SSRF merged into A01.

**API Top 10 (2023), the ones to know:** API1 **BOLA** · API3 Broken Object Property Level Authorization · API4 Unrestricted Resource Consumption · API5 **BFLA**.

**LLM Top 10 (2025):** LLM01 Prompt Injection · 02 Sensitive Information Disclosure · 03 Supply Chain · 04 Data and Model Poisoning · 05 Improper Output Handling · 06 Excessive Agency · 07 System Prompt Leakage · 08 Vector and Embedding Weaknesses · 09 Misinformation · 10 Unbounded Consumption.

**Agentic Top 10 (for 2026, published 9 Dec 2025):** the first three are Agent Goal Hijack, Tool Misuse and Exploitation, Identity and Privilege Abuse.

## 4. Quick tables

**MFA ladder:** password only < SMS < app code < push < number-matching push < **passkey / FIDO2 key** (only the last resists AiTM phishing; weak spot: recovery).

**Ports:** 22 SSH · 53 DNS · 80 HTTP · 443 HTTPS · 445 SMB (never expose) · 3306/5432 databases (never expose) · 3389 RDP (top ransomware entry). 65,535 ports; nmap scans the top 1,000 by default.

**Status codes:** 200 OK · 301/302 redirect (open-redirect abuse) · **401 not authenticated** · **403 not authorized** · 404 not found · 429 too many requests · 500 server error (verbose errors leak internals).

**Cookie flags and headers:** `HttpOnly` blocks script reads · `Secure` HTTPS only · `SameSite` limits CSRF · HSTS blocks downgrade · CSP limits XSS impact · `nosniff` stops MIME confusion · `frame-ancestors` stops clickjacking.

**Password minimums (OWASP):** Argon2id m=19 MiB, t=2, p=1 · scrypt N=2^17, r=8, p=1 · bcrypt cost 10+ (72-byte limit) · PBKDF2-HMAC-SHA256 600,000.

**STRIDE:** Spoofing (authentication) · Tampering (integrity) · Repudiation (non-repudiation) · Information disclosure (confidentiality) · Denial of service (availability) · Elevation of privilege (authorization).

**CVSS bands:** 0.1-3.9 Low · 4.0-6.9 Medium · 7.0-8.9 High · 9.0-10.0 Critical. **Patch order:** known-exploited (KEV) first, then internet-facing, then CVSS and business impact.

**Incident response:** Identify → Contain (revoke credentials **and sessions**) → Eradicate → Recover (clean backups) → Learn (blameless). **Ransomware chain:** initial access → control → spread → steal data → encrypt and extort.

**Useful commands (permitted targets only):** `nmap -sV <target>` · `nmap -sn <range>` · `dig example.com` · `curl -sI https://example.com` · Wireshark `tcp.flags.syn == 1`, `tls.handshake.type == 1`.

**Agent controls in one line:** sandbox · scoped short-lived tokens · no prod credentials · approvals for risky actions · reviewed rules/MCP config · human check of every new dependency · small reviewed PRs.

## 5. Pairs people confuse

| Pair | One-line difference |
| --- | --- |
| Authentication vs authorization | Who you are vs what you may do |
| IDOR vs BOLA | Same flaw: web name vs API name |
| BOLA vs BFLA | Reach another's object vs call a forbidden function |
| Encryption vs hashing vs encoding | Reversible with key vs one-way vs reversible with no key |
| Salt vs pepper | Per user, stored beside the hash vs shared secret stored elsewhere |
| MFA vs passkey | Extra proof (relayable) vs domain-bound public-key login |
| IDS vs IPS; firewall vs WAF | Alerts vs blocks; network rules vs HTTP-aware |
| CVE / CWE / CVSS / KEV | One flaw / weakness type / severity / "exploited now" |
| XSS vs CSRF | Attacker's code runs vs victim's browser is driven |
| Direct vs indirect prompt injection | User types it vs hidden in content the AI reads |
| SAST / DAST / SCA | Scan source / test running app / scan dependencies |

## 6. The 60-second self-test

Say aloud, no notes: (1) the three doors breaches use today, with one number; (2) how HTTPS works from DNS to encrypted traffic; (3) how to prevent SQLi and XSS in code, with a recent case; (4) why ordinary MFA fails against AiTM phishing and what does not; (5) what prompt injection is, the three-part risky combination, and three controls for a coding agent.

---

## Glossary

| Term | Meaning | Ch. |
| --- | --- | --- |
| **Agent (AI)** | An AI system that plans and takes actions with tools, not just answers | 11 |
| **Agentic** | Describes systems or risks involving such agents (OWASP has an Agentic Top 10) | 11 |
| **AiTM** | Adversary-in-the-middle: a phishing proxy that relays a real login and steals the session | 7 |
| **Attack surface** | Everything an attacker can reach: endpoints, ports, inputs, dependencies, vendors | 2 |
| **BFLA / BOLA** | Calling a function you should not / reaching another user's object (API name for IDOR) | 6 |
| **CIA triad** | Confidentiality, Integrity, Availability | 2 |
| **CORS** | Mechanism that selectively *relaxes* the same-origin policy | 4 |
| **Credential stuffing** | Replaying leaked username and password pairs on other sites | 7 |
| **CSP** | Header limiting where scripts and content may load from | 4 |
| **CSRF** | Tricking a victim's browser into sending an unintended authenticated request | 6 |
| **CVE / CWE / CVSS / KEV** | One known flaw / a weakness category / 0-10 severity / CISA's known-exploited list | 5 |
| **DAST / SAST / SCA** | Test the running app / scan source / scan dependencies | 10 |
| **Defense in depth** | Overlapping controls so one failure is not fatal | 2 |
| **DDoS** | Denial of service from many machines at once | 8 |
| **Double extortion** | Stealing data *and* encrypting systems, then threatening to leak | 9 |
| **EDR** | Endpoint Detection and Response: monitors devices for attacks | 8 |
| **Encoding / encryption / hash** | Reversible by anyone / reversible with a key / one-way fingerprint | 3 |
| **FIDO2 / WebAuthn** | Standards behind passkeys and hardware security keys | 7 |
| **HSTS** | Header telling browsers to always use HTTPS for a site | 4 |
| **Harvest now, decrypt later** | Recording encrypted data today to decrypt with a future quantum computer | 3 |
| **IDS / IPS / WAF** | Alerts / blocks inline / understands HTTP attacks | 8 |
| **Infostealer** | Malware that copies saved passwords, cookies and tokens | 7 |
| **JWT** | Signed token carrying identity claims; verify, never just decode | 7 |
| **Least privilege** | Give only the access that is needed | 2 |
| **MCP** | Model Context Protocol: a standard for letting an AI agent call external tools and data sources | 11 |
| **MITM** | Man-in-the-middle: relaying and possibly altering traffic | 8 |
| **MITRE ATT&CK** | Public catalogue of attacker tactics and techniques | 1 |
| **ML-KEM / ML-DSA / SLH-DSA** | NIST post-quantum standards (FIPS 203/204/205) | 3 |
| **nmap** | The standard network and port scanner | 5 |
| **OAuth / OIDC** | Delegated access with tokens / login built on it | 7 |
| **OSINT** | Information gathered from public sources | 5 |
| **Passkey** | Phishing-resistant public-key login tied to the real website | 7 |
| **Penetration test** | Authorized, manual attack simulation that proves impact | 2 |
| **Phishing / pretexting** | Fraudulent messages / an invented scenario to extract access | 7 |
| **Prompt injection** | Text an AI reads is obeyed as instructions | 11 |
| **Ransomware** | Malware that encrypts data and demands payment | 9 |
| **Risk** | Likelihood × impact | 2 |
| **Salt / pepper** | Random per-user data in a hash / a secret kept outside the database | 3 |
| **SBOM** | Software Bill of Materials: a list of what is inside your software | 10 |
| **SIEM** | Collects and correlates logs across an organization | 8 |
| **Slopsquatting** | Registering a package name an AI model tends to invent, so that developers who install the suggestion get malware | 10, 11 |
| **SQL injection / XSS** | Untrusted input interpreted as a query / as script in another user's browser | 6 |
| **SSRF** | Making a server fetch attacker-chosen URLs, reaching internal resources | 6 |
| **STRIDE** | Six threat types (see section 4) | 2 |
| **Supply-chain attack** | Compromising something you depend on to compromise you | 10 |
| **Tool poisoning** | Hostile instructions hidden in an AI tool's description; can change after approval | 11 |
| **Zero-day / zero trust** | A flaw with no patch yet / never trust by network location | 2 |
