# Interview Q&A Bank: 40 Questions

> **Goal.** Be able to answer each question in about 30-60 seconds, out loud, using the four-step shape (what, how it's exploited, how to prevent it, a real case).
>
> **How to drill (this is the whole method):**
> 1. **Round 1:** read a question, cover the answer, **speak your answer out loud**, then compare. Mark it green (nailed), yellow (shaky) or red (blank).
> 2. **Round 2 (two days later):** only the yellow and red ones.
> 3. **Round 3 (mock interview):** use [Lab 12](11-labs.md#lab-12-mock-interview-record-yourself). Random order, because real interviews are never in chapter order (this is *interleaving*, and it feels harder precisely because it works).

---

## A. Fundamentals

**1. What is the CIA triad?**
*Answer:* Confidentiality (only the right people can read it), integrity (it hasn't been altered), availability (it works when needed). Any attack can be classified by which leg it breaks: a leaked database breaks confidentiality, tampering breaks integrity, ransomware or DDoS breaks availability.
*Follow-up:* "What would you add?" Authenticity and non-repudiation.

**2. Vulnerability vs threat vs risk?**
*Answer:* A vulnerability is a weakness; a threat is something that could exploit it; risk is the likelihood times the impact. An easy-to-reach bug that exposes all customers is high risk; a hard-to-reach bug exposing nothing is low risk even though it is technically a vulnerability.

**3. Vulnerability assessment vs penetration test?**
*Answer:* An assessment is broad and mostly automated and produces a ranked list of weaknesses. A pentest is narrow and manual and proves real impact by exploiting weaknesses, within an agreed scope and with written permission.

**4. Walk me through how an attacker compromises a system.**
*Answer:* Recon (gather public info), scanning (find hosts, ports, versions), gaining access (exploit a flaw or a stolen credential), maintaining access (backdoor, new account), covering tracks (alter logs). I'd give one concrete example per phase and end with how a defender breaks the chain early.

**5. Red team vs blue team vs purple team?**
*Answer:* Red simulates real attackers; blue defends, monitors and responds; purple is red and blue sharing findings in real time so detection and defences improve faster.

**6. What is defense in depth?**
*Answer:* Multiple overlapping controls so one failure isn't fatal. For a web app: parameterized queries, input validation, least-privilege database account, WAF, logging and alerting, all together.

**7. What is least privilege?**
*Answer:* Every user, process and service gets only the access it needs. The web app's database user shouldn't be able to drop tables; if the app is compromised, damage is limited.

**8. What is zero trust?**
*Answer:* Never trust a request just because it comes from inside the network. Authenticate and authorize every request, and assume the network may already be hostile.

---

## B. Cryptography and networking

**9. Hashing vs encryption vs encoding?**
*Answer:* Hashing is one-way, used for integrity and passwords. Encryption is reversible *with a key*, used for confidentiality. Encoding is reversible with *no* key, such as Base64, and provides no security at all.

**10. Symmetric vs asymmetric encryption?**
*Answer:* Symmetric (AES) uses one shared key: fast, but the key must be shared safely. Asymmetric (RSA/ECC) uses a public/private pair: solves key sharing but is slow. TLS uses asymmetric crypto to agree on a key and symmetric crypto to encrypt the traffic.

**11. How does HTTPS work?**
*Answer:* TCP handshake, then a TLS handshake: the client sends supported ciphers and a key share, the server replies with its certificate and key share, the client validates the certificate chain against trusted CAs, both sides derive the same session key, and all traffic is then encrypted symmetrically. A man-in-the-middle fails because they can't present a valid certificate for the domain.
*Follow-up:* "What is forward secrecy?" Session keys are temporary, so stealing the server's long-term key later can't decrypt past recorded traffic.

**12. How should passwords be stored?**
*Answer:* Hashed with a slow, salted algorithm (Argon2id, bcrypt, scrypt). Never plaintext, never encrypted (keys get stolen), never MD5 or SHA-1. Slowness makes each guess expensive; the per-user salt defeats precomputed tables and makes identical passwords hash differently. LinkedIn's unsalted SHA-1 leak is the classic example.

**13. Salt vs pepper?**
*Answer:* A salt is random, per user, stored beside the hash. A pepper is a secret shared across users and stored *outside* the database, so a stolen database alone isn't enough.

**14. 401 vs 403?**
*Answer:* 401: not authenticated, we don't know who you are. 403: authenticated but not authorized, we know you and the answer is still no.

**15. What happens when you type https://example.com into a browser?**
*Answer:* DNS lookup, TCP handshake, TLS handshake, HTTP request, server processing, response and render. I'd add one risk per step: DNS spoofing, SYN flood, MITM, cookie theft/CSRF, injection and broken access control, XSS.

**16. TCP vs UDP?**
*Answer:* TCP is connection-oriented with ordered, guaranteed delivery (after a three-way handshake). UDP is connectionless and faster with no guarantees; used by DNS, video and games.

**17. What is a certificate and a certificate authority?**
*Answer:* A certificate is a signed statement that a public key belongs to a domain. A CA is a trusted organization that signs it. Browsers trust a built-in list of root CAs, and validate a chain from the site's certificate up to one of them.

**18. What is a digital signature?**
*Answer:* The sender hashes the message and signs the hash with their private key; anyone verifies it with the public key. It proves integrity and authenticity, and provides non-repudiation.

---

## C. Web security

**19. What is SQL injection and how do you prevent it?**
*Answer:* Untrusted input is interpreted as part of a SQL query, so an attacker can change its meaning, for example making a login condition always true. Prevent it with parameterized queries (prepared statements), plus a least-privilege database account. Escaping and WAFs are not the primary defence. Heartland Payment Systems (about 130 million cards) is the classic case.

**20. XSS: types and prevention?**
*Answer:* The attacker's script runs in another user's browser under your site's origin. Stored (saved on the server), reflected (bounced from a URL), DOM-based (client-side). Primary fix: context-aware output encoding, which frameworks do by default, so watch for escape hatches such as `dangerouslySetInnerHTML`. Layers: CSP and HttpOnly cookies.

**21. CSRF, and how is it different from XSS?**
*Answer:* CSRF abuses the browser's automatic cookie sending to make the victim's browser perform an action they didn't intend; no attacker code runs on your site. XSS runs attacker code in your page. Prevent CSRF with SameSite cookies and anti-CSRF tokens. And an XSS flaw defeats CSRF tokens.

**22. What is IDOR?**
*Answer:* Changing an identifier (`/orders/1002`) to reach someone else's object because the server checked "logged in?" but not "allowed to see this object?". Fix: scope every lookup to the current user and deny by default. Unguessable IDs are a bonus, not a control.

**23. What is SSRF?**
*Answer:* Making the server fetch an attacker-chosen URL, so it reaches internal services the attacker can't, such as the cloud metadata service. Fix: allowlist destinations, block private and link-local IPs, use the hardened metadata service (IMDSv2), and give the server's cloud role least privilege. Capital One (2019) is the commonly cited case.

**24. Same-origin policy and CORS?**
*Answer:* The same-origin policy stops one origin's scripts reading another origin's responses. CORS is how a server selectively relaxes that with headers. CORS doesn't add security; careless CORS (`*` with credentials) removes it.

**25. Name the OWASP Top 10 (2025).**
*Answer:* A01 Broken Access Control, A02 Security Misconfiguration, A03 Software Supply Chain Failures (new), A04 Cryptographic Failures, A05 Injection, A06 Insecure Design, A07 Authentication Failures, A08 Software or Data Integrity Failures, A09 Security Logging and Alerting Failures, A10 Mishandling of Exceptional Conditions (new). SSRF was folded into A01.

**26. What should you watch for with JWTs?**
*Answer:* Verify the signature and pin the algorithm server-side; use a strong secret; keep tokens short-lived and plan revocation; don't store them in `localStorage` (XSS can read it), prefer an HttpOnly cookie; remember the payload is only encoded, so no secrets inside.

**27. How would you secure a REST API?**
*Answer:* HTTPS everywhere; authenticate every call; authorize per object (prevents IDOR); validate input and use parameterized queries; rate limit; return only needed fields and no stack traces; no secrets in code or URLs; restrictive CORS; log auth and access failures; keep dependencies updated.

**28. What do HttpOnly, Secure and SameSite do on a cookie?**
*Answer:* HttpOnly hides it from JavaScript (limits XSS cookie theft). Secure sends it only over HTTPS (limits sniffing). SameSite restricts sending on cross-site requests (limits CSRF).

**29. What is session fixation?**
*Answer:* The attacker plants a known session ID in the victim's browser before login; after the victim logs in, the attacker uses that same ID. Fix: issue a new session ID at login.

**30. What is command injection and its fix?**
*Answer:* User input reaches an operating-system shell. Avoid the shell; pass arguments as a list (`subprocess.run(["ping", host])`) and validate against an allowlist.

---

## D. Network and systems

**31. Firewall vs IDS vs IPS vs WAF?**
*Answer:* A firewall filters by IP, port and state. An IDS watches a copy of traffic and alerts. An IPS sits inline and blocks. A WAF understands HTTP and blocks web-attack patterns like SQLi and XSS.

**32. What is a man-in-the-middle attack?**
*Answer:* An attacker relays and possibly alters traffic between two parties, for instance via a rogue Wi-Fi point or ARP spoofing. Defence: TLS with certificate validation plus HSTS, so interception yields only ciphertext and a forged certificate is rejected.

**33. DoS vs DDoS, and how do you defend?**
*Answer:* DoS exhausts a resource from one source; DDoS does it from many, typically a botnet. Types: volumetric, state exhaustion (SYN flood), application layer. Defend with upstream scrubbing or a CDN, rate limiting, SYN cookies and caching.

**34. What does nmap tell you?**
*Answer:* Live hosts, open/closed/filtered ports, service versions and OS guesses: the map of the attack surface. Versions lead to CVE lookups. Only run it with permission.

**35. CVE vs CWE vs CVSS?**
*Answer:* CVE is one specific numbered flaw in a product; CWE is the category of weakness (CWE-89 is SQL injection); CVSS is the 0-10 severity score. CVSS measures potential severity, not likelihood of exploitation, so I'd also check whether it's being exploited now.

---

## E. Engineering practice and scenarios

**36. How do you build security into development?**
*Answer:* Threat-model new features early (STRIDE); follow secure-coding defaults (parameterized queries, output encoding, authorization checks); code review with a security eye; SAST, dependency scanning and secret scanning in CI; DAST on staging; secrets in a manager; least privilege everywhere; logging and alerting.

**37. What is a software supply-chain attack?**
*Answer:* Compromising something you depend on (a package, a build system, an update channel) to compromise you. SolarWinds (2020) is the classic case. Defences: lockfiles and pinned versions, dependency scanning, an SBOM, signature verification and hardened CI/CD.

**38. How do you manage secrets?**
*Answer:* Never in source code, config committed to Git, or front-end bundles. Use a secrets manager or KMS, inject at runtime, give each service its own least-privilege credentials, rotate regularly, scan repos for leaked secrets, and rotate immediately if one leaks.

**39. You find a critical vulnerability in production. What do you do?**
*Answer:* Don't probe further than needed. Document what I saw, report it immediately through the proper channel, help assess impact, support a fix and deployment, verify the fix, and run a blameless post-mortem. They're testing process and ethics, not heroics.

**40. You suspect a breach. First steps?**
*Answer:* Follow incident response: identify and scope, contain (isolate systems, revoke credentials), eradicate the cause, recover from clean backups, then a blameless post-mortem. Preserve evidence and don't just reboot everything, which destroys evidence and may tip off the attacker.

---

## Bonus: three behavioural questions that always come up

- **"Tell me about a security issue you found or fixed."** Use your prepared war story: situation, what you did, outcome, what changed afterwards.
- **"How do you stay current?"** Name two real sources (for example the OWASP Top 10, CISA advisories, a security newsletter, hands-on labs on PortSwigger) and one recent thing you learned.
- **"A teammate says security slows us down. How do you respond?"** Security is cheaper early (design and code review) than late (incident and rewrite); automate checks in CI so they cost minutes; start with the highest-risk paths; and make the secure way the easy way.
