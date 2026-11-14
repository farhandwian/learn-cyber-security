# Glossary

One line each. If a term feels fuzzy, the chapter named at the end explains it.

| Term | Meaning | Chapter |
| --- | --- | --- |
| **AES** | A fast, widely used symmetric encryption algorithm | 3 |
| **APT** | Advanced Persistent Threat: a patient, well-resourced attacker, often state-backed | 2 |
| **ARP spoofing** | Forging local-network address replies so traffic is sent to the attacker | 8 |
| **Asymmetric encryption** | Encryption with a public/private key pair (RSA, ECC) | 3 |
| **Attack surface** | Everything an attacker can reach: endpoints, ports, inputs, dependencies | 2 |
| **Authentication** | Proving who you are | 7 |
| **Authorization** | Deciding what you are allowed to do | 7 |
| **Availability** | The system works when needed (the "A" in CIA) | 2 |
| **Backdoor** | A hidden way back into a system | 2 |
| **Banner grabbing** | Reading the name and version a service announces | 5 |
| **Blue team** | The defenders | 2 |
| **Botnet** | Many infected machines under one attacker's control | 8, 9 |
| **Brute force** | Trying many passwords or keys until one works | 7 |
| **CA (Certificate Authority)** | A trusted organization that signs certificates | 3 |
| **CIA triad** | Confidentiality, Integrity, Availability | 2 |
| **Confidentiality** | Only the right people can read the data | 2 |
| **Cookie** | A small value the browser sends with each request to a site; often holds the session ID | 4 |
| **CORS** | A mechanism that selectively *relaxes* the same-origin policy | 4 |
| **CSP** | Content-Security-Policy: a header limiting where scripts and content may load from | 4 |
| **CSRF** | Tricking a victim's browser into sending an unintended authenticated request | 7 |
| **CVE** | A numbered identifier for one specific known vulnerability | 5 |
| **CVSS** | A 0-10 severity score for a vulnerability | 5 |
| **CWE** | A category of weakness (for example CWE-89, SQL injection) | 5 |
| **DDoS** | Denial of service from many machines at once | 8 |
| **Defense in depth** | Layering overlapping controls so one failure is not fatal | 2 |
| **DMZ** | A separated network zone for public-facing servers | 8 |
| **DNS** | The system that maps names to IP addresses | 4 |
| **EDR** | Endpoint Detection and Response: security software that monitors devices | 9 |
| **Encoding** | Changing data's format (Base64); reversible by anyone, not security | 3 |
| **Encryption** | Scrambling data so only a key holder can read it | 3 |
| **Exploit** | The technique or code that uses a vulnerability | 2 |
| **Firewall** | Filters network traffic by address, port and state | 8 |
| **Hash** | A fixed-size one-way fingerprint of data | 3 |
| **HSTS** | A header telling browsers to always use HTTPS for a site | 4 |
| **IDOR** | Reaching another user's object by changing an identifier; missing authorization check | 7 |
| **IDS** | Intrusion Detection System: watches traffic and alerts | 8 |
| **Integrity** | Data has not been altered | 2 |
| **IPS** | Intrusion Prevention System: inline, detects and blocks | 8 |
| **JWT** | JSON Web Token: a signed token carrying identity claims | 7 |
| **Least privilege** | Give only the access that is needed, nothing more | 2 |
| **MFA** | Multi-factor authentication: more than one proof of identity | 7 |
| **MITM** | Man-in-the-middle: an attacker relaying and possibly altering traffic | 8 |
| **nmap** | The standard network and port scanner | 5 |
| **OSINT** | Open-source intelligence: gathering information from public sources | 5 |
| **OWASP** | The Open Worldwide Application Security Project; publisher of the Top 10 | 6 |
| **Payload** | What runs after an exploit succeeds | 2 |
| **Penetration test** | Authorized, manual attack simulation that proves impact | 2 |
| **Pepper** | A secret added to password hashing and stored outside the database | 3 |
| **Phishing** | Fraudulent messages that trick people into revealing information | 9 |
| **Ransomware** | Malware that encrypts data and demands payment | 9 |
| **Red team** | The simulated attackers | 2 |
| **Risk** | Likelihood × impact | 2 |
| **Salt** | Random per-user data mixed into a password hash | 3 |
| **SAST / DAST / SCA** | Scan source code / test the running app / scan dependencies | 9 |
| **SBOM** | Software Bill of Materials: a list of what is inside your software | 9 |
| **SIEM** | A system that collects and correlates logs across an organization | 8, 9 |
| **SQL injection** | Untrusted input interpreted as part of a database query | 6 |
| **SSRF** | Making a server fetch attacker-chosen URLs, reaching internal resources | 7 |
| **STRIDE** | Six threat types: Spoofing, Tampering, Repudiation, Information disclosure, DoS, Elevation of privilege | 9 |
| **Supply-chain attack** | Compromising something you depend on to compromise you | 9 |
| **Symmetric encryption** | Encryption using one shared secret key (AES) | 3 |
| **Threat** | Something that could exploit a vulnerability | 2 |
| **TLS** | The protocol that encrypts and authenticates web traffic (HTTPS = HTTP over TLS) | 3 |
| **Vulnerability** | A weakness that could be exploited | 2 |
| **WAF** | Web Application Firewall: understands HTTP and blocks web-attack patterns | 8 |
| **XSS** | Cross-site scripting: attacker's script runs in another user's browser | 6 |
| **Zero-day** | A flaw unknown to the vendor, with no patch yet | 2 |
| **Zero trust** | Never trust by network location; verify every request | 2, 8 |
