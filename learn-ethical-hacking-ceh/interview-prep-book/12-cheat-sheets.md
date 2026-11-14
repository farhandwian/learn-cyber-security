# Cheat Sheets

> Rapid-fire material: things interviewers expect instantly, with no thinking pause. Review this the evening before. **If you can't explain a row out loud, go back to its chapter.**

---

## 1. The answer shape

**What is it? → How is it exploited? → How do you prevent it? → When did it happen (real case)?**

Always end with the fix.

---

## 2. Ports to know cold

| Port | Service | Worth saying |
| --- | --- | --- |
| 21 | FTP | Cleartext; legacy, replaced by SFTP |
| 22 | SSH | Encrypted remote shell (also SFTP/SCP) |
| 23 | Telnet | Cleartext remote shell; should never be open |
| 25 | SMTP | Mail transfer |
| 53 | DNS | UDP for queries, TCP for zone transfers |
| 80 | HTTP | Unencrypted web |
| 110 / 143 | POP3 / IMAP | Mail retrieval |
| 161 | SNMP | Device management; weak "community strings" are a classic finding |
| 389 | LDAP | Directory service (Active Directory) |
| 443 | HTTPS | Web over TLS |
| 445 | SMB | Windows file sharing; WannaCry spread through it |
| 3306 | MySQL | Should never face the internet |
| 3389 | RDP | Windows remote desktop; a top ransomware entry point |
| 5432 | PostgreSQL | Same rule as MySQL |

There are **65,535** ports; nmap scans the top **1,000** by default.

---

## 3. OWASP Top 10 (2025) in one line each

| # | Name | One line | Fix |
| --- | --- | --- | --- |
| A01 | Broken Access Control | Users do or see what they shouldn't (IDOR); includes SSRF | Server-side check on every request; deny by default |
| A02 | Security Misconfiguration | Defaults, open buckets, debug on | Hardened, repeatable configuration |
| A03 | Software Supply Chain Failures *(new)* | Compromised dependency, build or update | Pin, scan, SBOM, verify |
| A04 | Cryptographic Failures | Weak or missing crypto, bad key handling | TLS, strong algorithms, key management |
| A05 | Injection | Untrusted input runs as code (SQLi, XSS, command) | Parameterized queries, output encoding |
| A06 | Insecure Design | Flawed by design | Threat model early |
| A07 | Authentication Failures | Weak login, stuffing, bad sessions | MFA, rate limit, slow salted hashes |
| A08 | Software or Data Integrity Failures | Trusting unsigned code or data | Verify signatures and integrity |
| A09 | Security Logging and Alerting Failures | Attacks go unseen | Log security events; alert |
| A10 | Mishandling of Exceptional Conditions *(new)* | Errors handled badly; fails open | Fail closed; handle every error path |

Five groups: **who can do what** (A01, A07), **setup and build** (A02, A03, A08), **data protection** (A04), **code and design** (A05, A06, A10), **detection** (A09).

---

## 4. HTTP status codes

| Code | Meaning | Security note |
| --- | --- | --- |
| 200 | OK | n/a |
| 301 / 302 | Redirect | Open-redirect abuse in phishing |
| 400 | Bad request | n/a |
| **401** | **Not authenticated** ("who are you?") | Login needed |
| **403** | **Not authorized** ("I know you, still no") | Authorization failure |
| 404 | Not found | Sometimes used to avoid revealing a resource exists |
| 429 | Too many requests | Rate limiting |
| 500 | Server error | Verbose errors leak internals |

---

## 5. Cookie flags and security headers

| Item | Protects against |
| --- | --- |
| `HttpOnly` | Script reading the cookie (XSS cookie theft) |
| `Secure` | Sending over plain HTTP (sniffing) |
| `SameSite=Lax/Strict` | CSRF |
| `Strict-Transport-Security` (HSTS) | Downgrade to HTTP |
| `Content-Security-Policy` | XSS impact; restricts script sources |
| `X-Content-Type-Options: nosniff` | MIME-type confusion |
| `frame-ancestors` / `X-Frame-Options` | Clickjacking |

---

## 6. STRIDE

| Letter | Threat | Property violated |
| --- | --- | --- |
| S | Spoofing | Authentication |
| T | Tampering | Integrity |
| R | Repudiation | Non-repudiation |
| I | Information disclosure | Confidentiality |
| D | Denial of service | Availability |
| E | Elevation of privilege | Authorization |

---

## 7. Useful numbers

| Item | Value |
| --- | --- |
| CVSS bands | 0.1-3.9 Low, 4.0-6.9 Medium, 7.0-8.9 High, 9.0-10.0 Critical |
| Log4Shell CVSS | 10.0 (CVE-2021-44228) |
| TLS | Use 1.3 (1.2 acceptable); SSL and TLS 1.0/1.1 are deprecated |
| Password hash | Argon2id, bcrypt or scrypt; never MD5/SHA-1/plain SHA-256 |
| Incident response | Identify, Contain, Eradicate, Recover, Learn |

---

## 8. Commands

| Command | Purpose |
| --- | --- |
| `nmap -sV <target>` | Scan and detect service versions (**permitted targets only**) |
| `nmap -sn <range>` | Which hosts are alive |
| `nmap -sS` / `-sT` | SYN scan vs full connect scan |
| `dig example.com` / `dig MX example.com` | DNS records |
| `whois example.com` | Domain registration |
| `curl -sI https://example.com` | Response headers (HSTS, CSP, cookie flags) |
| Wireshark filter `tcp.flags.syn == 1` | Handshake starts |
| Wireshark filter `tls.handshake.type == 1` | TLS Client Hello |

---

## 9. Pairs people confuse (favourite trap questions)

| Pair | One-line difference |
| --- | --- |
| Authentication vs authorization | Who you are vs what you may do |
| 401 vs 403 | Not logged in vs logged in but forbidden |
| Encryption vs hashing | Reversible with a key vs one-way |
| Encoding vs encryption | No key at all (Base64) vs key required |
| Salt vs pepper | Per user, stored beside the hash vs shared secret stored elsewhere |
| Symmetric vs asymmetric | One shared key vs public/private pair |
| IDS vs IPS | Alerts vs blocks |
| Firewall vs WAF | Network rules vs understands HTTP attacks |
| CVE vs CWE vs CVSS | One flaw vs a weakness type vs a severity score |
| XSS vs CSRF | Attacker's code runs vs the victim's browser is driven |
| Virus vs worm | Needs a host and a user vs spreads by itself |
| Vulnerability assessment vs pentest | Broad automated list vs manual proof of impact |
| Passive vs active recon | Doesn't touch the target vs does (needs permission) |
| SSL vs TLS | SSL is the deprecated ancestor; people still say "SSL certificate" |
| SAST vs DAST vs SCA | Scan source vs test the running app vs scan dependencies |

---

## 10. The 60-second self-test

Say these five aloud, no notes, before the interview:

1. CIA triad, with an attack for each letter.
2. How HTTPS works, from DNS to encrypted traffic.
3. How to prevent SQLi and XSS in code.
4. 401 vs 403, and what IDOR is.
5. The first three items of the OWASP Top 10 (2025) and what changed this edition.

If all five flow, you're ready.
