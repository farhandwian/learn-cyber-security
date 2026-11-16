# Glossary

One line each. If a term feels fuzzy, the chapter named at the end explains it.

| Term | Meaning | Chapter |
| --- | --- | --- |
| **AES** | A fast, widely used symmetric encryption algorithm | 4 |
| **AiTM** | Adversary-in-the-middle: a phishing proxy that relays a real login and steals the session | 9 |
| **Agent (AI)** | An AI system that plans and takes actions with tools, not just answers | 13 |
| **APT** | Advanced Persistent Threat: a patient, well-resourced attacker, often state-backed | 3 |
| **Asymmetric encryption** | Encryption with a public/private key pair (RSA, ECC) | 4 |
| **Attack surface** | Everything an attacker can reach: endpoints, ports, inputs, dependencies, vendors | 3 |
| **Authentication** | Proving who you are | 8 |
| **Authorization** | Deciding what you are allowed to do | 8 |
| **Availability** | The system works when needed (the "A" in CIA) | 3 |
| **BFLA** | Broken Function Level Authorization: calling a function you shouldn't | 8 |
| **BOLA** | Broken Object Level Authorization: reaching another user's object (API name for IDOR) | 8 |
| **Botnet** | Many infected devices under one attacker's control | 10, 11 |
| **CA (Certificate Authority)** | A trusted organization that signs certificates | 4 |
| **CIA triad** | Confidentiality, Integrity, Availability | 3 |
| **Confidentiality** | Only the right people can read the data | 3 |
| **Cookie** | A small value the browser sends with each request to a site; often holds the session ID | 5 |
| **CORS** | A mechanism that selectively *relaxes* the same-origin policy | 5 |
| **Credential stuffing** | Replaying leaked username and password pairs on other sites | 9 |
| **CSP** | Content-Security-Policy: a header limiting where scripts and content may load from | 5 |
| **CSRF** | Tricking a victim's browser into sending an unintended authenticated request | 8 |
| **CVE** | A numbered identifier for one specific known vulnerability | 6 |
| **CVSS** | A 0-10 severity score for a vulnerability | 6 |
| **CWE** | A category of weakness (for example CWE-89, SQL injection) | 6 |
| **DAST** | Dynamic testing of a running application from the outside | 12 |
| **DDoS** | Denial of service from many machines at once | 10 |
| **Defense in depth** | Layering overlapping controls so one failure is not fatal | 3 |
| **DMZ** | A separated network zone for public-facing servers | 10 |
| **DNS** | The system that maps names to IP addresses | 5 |
| **Double extortion** | Stealing data *and* encrypting systems, then threatening to leak | 11 |
| **EDR** | Endpoint Detection and Response: software that monitors devices for attacks | 10 |
| **Encoding** | Changing data's format (Base64); reversible by anyone, not security | 4 |
| **Encryption** | Scrambling data so only a key holder can read it | 4 |
| **Exploit** | The technique or code that uses a vulnerability | 3 |
| **FIDO2 / WebAuthn** | The standards behind passkeys and hardware security keys | 9 |
| **Firewall** | Filters network traffic by address, port and state | 10 |
| **Hash** | A fixed-size one-way fingerprint of data | 4 |
| **Harvest now, decrypt later** | Recording encrypted data today to decrypt with a future quantum computer | 4 |
| **HSTS** | A header telling browsers to always use HTTPS for a site | 5 |
| **IDOR** | Reaching another user's object by changing an identifier; missing authorization check | 8 |
| **IDS** | Intrusion Detection System: watches traffic and alerts | 10 |
| **Infostealer** | Malware that copies saved passwords, cookies and tokens from a device | 9, 11 |
| **Integrity** | Data has not been altered | 3 |
| **IPS** | Intrusion Prevention System: inline, detects and blocks | 10 |
| **JWT** | JSON Web Token: a signed token carrying identity claims | 9 |
| **KEV** | CISA's catalogue of Known Exploited Vulnerabilities | 6 |
| **Least privilege** | Give only the access that is needed, nothing more | 3 |
| **MFA** | Multi-factor authentication: more than one proof of identity | 9 |
| **MITM** | Man-in-the-middle: an attacker relaying and possibly altering traffic | 10 |
| **MITRE ATT&CK** | A public catalogue of attacker tactics and techniques | 2 |
| **ML-KEM / ML-DSA / SLH-DSA** | NIST's post-quantum key-establishment and signature standards (FIPS 203/204/205) | 4 |
| **nmap** | The standard network and port scanner | 6 |
| **OAuth / OIDC** | Delegated access with tokens / login built on top of it | 9 |
| **OSINT** | Open-source intelligence: gathering information from public sources | 6 |
| **OWASP** | The Open Worldwide Application Security Project; publisher of the Top 10 lists | 7 |
| **Passkey** | A phishing-resistant public-key login tied to the real website | 9 |
| **Payload** | What runs after an exploit succeeds | 3 |
| **Penetration test** | Authorized, manual attack simulation that proves impact | 3 |
| **Pepper** | A secret added to password hashing and stored outside the database | 4 |
| **Phishing** | Fraudulent messages that trick people into revealing information | 9 |
| **Pretexting** | An invented scenario used to extract access or information | 9 |
| **Prompt injection** | Text an AI reads is obeyed as instructions | 13 |
| **Ransomware** | Malware that encrypts data and demands payment | 11 |
| **Red team / Blue team** | The simulated attackers / the defenders | 3 |
| **Risk** | Likelihood × impact | 3 |
| **Salt** | Random per-user data mixed into a password hash | 4 |
| **SAST** | Static analysis of source code | 12 |
| **SBOM** | Software Bill of Materials: a list of what is inside your software | 12 |
| **SCA** | Software composition analysis: scanning dependencies for known flaws | 12 |
| **SIEM** | A system that collects and correlates logs across an organization | 10, 11 |
| **SQL injection** | Untrusted input interpreted as part of a database query | 7 |
| **SSRF** | Making a server fetch attacker-chosen URLs, reaching internal resources | 8 |
| **STRIDE** | Six threat types: Spoofing, Tampering, Repudiation, Information disclosure, DoS, Elevation of privilege | 12 |
| **Supply-chain attack** | Compromising something you depend on to compromise you | 12 |
| **Symmetric encryption** | Encryption using one shared secret key (AES) | 4 |
| **Threat** | Something that could exploit a vulnerability | 3 |
| **TLS** | The protocol that encrypts and authenticates web traffic (HTTPS = HTTP over TLS) | 4 |
| **Vulnerability** | A weakness that could be exploited | 3 |
| **WAF** | Web Application Firewall: understands HTTP and blocks web-attack patterns | 10 |
| **XSS** | Cross-site scripting: attacker's script runs in another user's browser | 7 |
| **Zero-day** | A flaw unknown to the vendor, with no patch yet | 3 |
| **Zero trust** | Never trust by network location; verify every request | 3, 10 |
