# Cheat Sheets

> Rapid-fire material: things interviewers expect instantly, with no thinking pause. Review this the evening before. **If you can't explain a row out loud, go back to its chapter.**

---

## 1. The answer shape

**What is it? → How is it exploited? → How do you prevent it? → When did it happen (a recent real case)?**

Always end with the fix.

---

## 2. Latest numbers (and where they come from)

| Fact | Number | Source |
| --- | --- | --- |
| Top way breaches start | Exploiting a vulnerability, about **31%** (was 20%) | Verizon DBIR 2026, as reported |
| Stolen credentials / pretexting | about **13%** / about **6%** | Verizon DBIR 2026, as reported |
| Third-party involvement in breaches | about **48%** (was 30%) | Verizon DBIR 2026, as reported |
| Ransomware in breaches | about **48%**; **69%** of victims did not pay | Verizon DBIR 2026, as reported |
| Known-exploited flaws fully fixed | about **26%**; median **43 days** to fix | Verizon DBIR 2026, as reported |
| DDoS attacks, first half 2026 | **23.2 million** network-layer; **935** above 1 Tbps | Cloudflare H1 2026 report |
| Share of DDoS that is small and short | **96.62%** under 500 Mbps; **90.60%** over within 10 minutes | Cloudflare H1 2026 report |
| Post-quantum standards | FIPS **203** (ML-KEM), **204** (ML-DSA), **205** (SLH-DSA), Aug 2024 | NIST |
| RSA/ECC timeline | deprecated after **2030**, disallowed after **2035** | NIST IR 8547 (final, Oct 2026) |
| Log4Shell CVSS | **10.0** (CVE-2021-44228) | NVD |

Say "according to" and round. Numbers change each year.

---

## 3. OWASP lists in one place

**Web Top 10 (2025):** A01 Broken Access Control · A02 Security Misconfiguration · A03 Software Supply Chain Failures *(new)* · A04 Cryptographic Failures · A05 Injection · A06 Insecure Design · A07 Authentication Failures · A08 Software or Data Integrity Failures · A09 Security Logging and Alerting Failures · A10 Mishandling of Exceptional Conditions *(new)*. SSRF merged into A01.

**API Security Top 10 (2023), the ones to know:** API1 **BOLA** · API3 Broken Object Property Level Authorization · API4 Unrestricted Resource Consumption · API5 **BFLA** (function level). Also exist: Broken Authentication, Sensitive Business Flows, SSRF, Misconfiguration, Improper Inventory, Unsafe Consumption of APIs.

**LLM Top 10 (2025):** LLM01 Prompt Injection · 02 Sensitive Information Disclosure · 03 Supply Chain · 04 Data and Model Poisoning · 05 Improper Output Handling · 06 Excessive Agency · 07 System Prompt Leakage · 08 Vector and Embedding Weaknesses · 09 Misinformation · 10 Unbounded Consumption.

**Agentic Top 10 (for 2026, published Dec 2025):** the first three are Agent Goal Hijack, Tool Misuse and Exploitation, Identity and Privilege Abuse.

---

## 4. The MFA ladder

Password only < SMS code < app code (TOTP) < push approval < number-matching push < **passkey / FIDO2 key**.
Only the last resists phishing proxies (AiTM). Its weak spot: account recovery.

---

## 5. Ports to know

| Port | Service | Worth saying |
| --- | --- | --- |
| 22 | SSH | Encrypted remote shell |
| 53 | DNS | UDP for queries, TCP for larger answers |
| 80 | HTTP | Unencrypted web |
| 443 | HTTPS | Web over TLS |
| 445 | SMB | Windows file sharing; never expose to the internet |
| 3306 / 5432 | MySQL / PostgreSQL | Databases: never face the internet |
| 3389 | RDP | Windows remote desktop; a top ransomware entry point |

(Telnet 23, FTP 21 and similar: "cleartext legacy, should be off".) There are **65,535** ports; nmap scans the top **1,000** by default.

---

## 6. HTTP status codes

| Code | Meaning | Security note |
| --- | --- | --- |
| 200 | OK | n/a |
| 301 / 302 | Redirect | Open-redirect abuse in phishing |
| **401** | **Not authenticated** ("who are you?") | Login needed |
| **403** | **Not authorized** ("I know you, still no") | Authorization failure |
| 404 | Not found | Sometimes used to avoid revealing a resource exists |
| 429 | Too many requests | Rate limiting |
| 500 | Server error | Verbose errors leak internals |

---

## 7. Cookie flags and security headers

| Item | Protects against |
| --- | --- |
| `HttpOnly` | Script reading the cookie (XSS cookie theft) |
| `Secure` | Sending over plain HTTP |
| `SameSite=Lax/Strict` | CSRF |
| `Strict-Transport-Security` (HSTS) | Downgrade to HTTP |
| `Content-Security-Policy` | Limits XSS impact |
| `X-Content-Type-Options: nosniff` | MIME-type confusion |
| `frame-ancestors` (CSP) | Clickjacking |

---

## 8. STRIDE

| Letter | Threat | Property violated |
| --- | --- | --- |
| S | Spoofing | Authentication |
| T | Tampering | Integrity |
| R | Repudiation | Non-repudiation |
| I | Information disclosure | Confidentiality |
| D | Denial of service | Availability |
| E | Elevation of privilege | Authorization |

---

## 9. CVSS bands and the patch order

CVSS: 0.1-3.9 Low · 4.0-6.9 Medium · 7.0-8.9 High · 9.0-10.0 Critical.
**Patch order:** known-exploited (KEV) first → internet-facing assets → then CVSS and business impact.

---

## 10. Incident response and ransomware

**IR:** Identify → Contain (revoke credentials **and sessions**) → Eradicate → Recover (clean backups) → Learn (blameless).
**Ransomware chain:** initial access → take control → spread → steal data → encrypt and extort.

---

## 11. Commands

| Command | Purpose |
| --- | --- |
| `nmap -sV <target>` | Scan and detect service versions (**permitted targets only**) |
| `nmap -sn <range>` | Which hosts are alive |
| `nmap -sS` / `-sT` | SYN scan vs full connect scan |
| `dig example.com` / `dig MX example.com` | DNS records |
| `curl -sI https://example.com` | Response headers (HSTS, CSP, cookie flags) |
| Wireshark filter `tcp.flags.syn == 1` | Handshake starts |
| Wireshark filter `tls.handshake.type == 1` | TLS Client Hello |

---

## 12. Pairs people confuse (favourite trap questions)

| Pair | One-line difference |
| --- | --- |
| Authentication vs authorization | Who you are vs what you may do |
| 401 vs 403 | Not logged in vs logged in but forbidden |
| IDOR vs BOLA | Same flaw: web name vs API name |
| BOLA vs BFLA | Reach another's object vs call a forbidden function |
| Encryption vs hashing | Reversible with key vs one-way |
| Encoding vs encryption | No key at all (Base64) vs key required |
| Salt vs pepper | Per user, stored beside the hash vs shared secret stored elsewhere |
| Symmetric vs asymmetric | One shared key vs public/private pair |
| MFA vs passkey | Extra proof (relayable) vs domain-bound public-key login (phishing-resistant) |
| IDS vs IPS | Alerts vs blocks |
| Firewall vs WAF | Network rules vs understands HTTP attacks |
| CVE vs CWE vs CVSS vs KEV | One flaw vs weakness type vs severity vs "exploited now" |
| XSS vs CSRF | Attacker's code runs vs victim's browser is driven |
| Direct vs indirect prompt injection | User types it vs hidden in content the AI reads |
| Virus vs worm | Needs a host and a user vs spreads by itself |
| SAST vs DAST vs SCA | Scan source vs test the running app vs scan dependencies |
| Vulnerability assessment vs pentest | Broad automated list vs manual proof of impact |

---

## 13. The 60-second self-test

Say these five aloud, no notes, before the interview:

1. The three doors breaches use today, with one number.
2. How HTTPS works, from DNS to encrypted traffic.
3. How to prevent SQLi and XSS in code, and one recent case.
4. Why ordinary MFA fails against AiTM phishing, and what doesn't.
5. What prompt injection is and the three-part risky combination.

If all five flow, you're ready.
