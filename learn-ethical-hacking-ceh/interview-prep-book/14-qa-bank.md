# Interview Q&A Bank: 45 Questions

> **Goal.** Be able to answer each question in about 30-60 seconds, out loud, using the four-step shape (what, how it's exploited, how to prevent it, a recent real case).
>
> **How to drill (this is the whole method):**
> 1. **Round 1:** read a question, cover the answer, **speak your answer out loud**, then compare. Mark it green (nailed), yellow (shaky) or red (blank).
> 2. **Round 2 (two days later):** only the yellow and red ones.
> 3. **Round 3 (mock interview):** use [Lab 13](15-labs.md#lab-13-mock-interview-record-yourself). Random order, because real interviews are never in chapter order (this is *interleaving*, and it feels harder precisely because it works).

---

## A. The landscape and fundamentals

**1. What are the biggest security threats right now?**
*Answer:* Three doors dominate: **exploited known vulnerabilities** (especially in internet-facing devices), **stolen or phished credentials** (including phishing that defeats ordinary MFA), and **third parties** (vendor tokens, poisoned dependencies). Ransomware monetizes that access. AI adds scaled phishing and a new attack surface (prompt injection). Most of it is preventable with fast patching, phishing-resistant MFA, least privilege and vendor hygiene.

**2. How do breaches usually start, with numbers?**
*Answer:* In Verizon's 2026 report, exploiting a vulnerability was the top initial access vector (about 31%, up from 20%), stolen credentials about 13%, pretexting about 6%; third parties were involved in about 48% of breaches and ransomware in about 48%. I'd say "according to Verizon" and round the numbers.

**3. What is the CIA triad?**
*Answer:* Confidentiality, integrity, availability. Classify any attack by which leg it breaks: a leak breaks confidentiality, tampering breaks integrity, ransomware or DDoS breaks availability.

**4. Vulnerability vs threat vs risk?**
*Answer:* A vulnerability is a weakness; a threat is something that could exploit it; risk is likelihood times impact. An easy-to-reach bug exposing all customers is high risk; a hard-to-reach bug exposing nothing is low.

**5. Vulnerability assessment vs penetration test?**
*Answer:* An assessment is broad and mostly automated and gives a ranked list. A pentest is narrow and manual and proves real impact by exploiting under an agreed scope and written permission.

**6. Walk me through how an attacker compromises a system.**
*Answer:* Recon, scanning, gaining access, maintaining access, covering tracks, each with an example. Today "gaining access" is usually a known flaw, a stolen login or a phone call. The detailed industry version is MITRE ATT&CK, a catalogue of tactics and techniques.

**7. What are least privilege and defense in depth?**
*Answer:* Least privilege: each user and service gets only the access it needs, so a compromise is contained. Defense in depth: overlapping controls so one failure isn't fatal. For a web app: parameterized queries, a least-privilege database account, a WAF, and logging, together.

**8. What is zero trust?**
*Answer:* Never trust a request because of where it comes from. Authenticate and authorize every request, assume the network may already be hostile, and limit blast radius with segmentation.

---

## B. Cryptography and web basics

**9. Hashing vs encryption vs encoding?**
*Answer:* Hashing is one-way (integrity, passwords). Encryption is reversible with a key (confidentiality). Encoding is reversible with no key, such as Base64: no security at all.

**10. Symmetric vs asymmetric encryption?**
*Answer:* Symmetric (AES) uses one shared key: fast, but the key must be shared safely. Asymmetric (RSA/ECC) uses a public/private pair: solves sharing but is slow. TLS uses asymmetric crypto to establish a key and symmetric crypto for the traffic.

**11. How does HTTPS work?**
*Answer:* TCP handshake, then TLS: the client sends supported ciphers and a key share, the server sends its certificate and key share, the client validates the certificate chain, both derive session keys, and traffic is encrypted symmetrically. A man-in-the-middle fails because they can't present a valid certificate for the domain.
*Follow-up:* "Forward secrecy?" Session keys are temporary, so stealing the server's long-term key later can't decrypt past traffic.

**12. How should passwords be stored?**
*Answer:* Hashed with a slow, salted algorithm (Argon2id, bcrypt, scrypt). Never plaintext, never encrypted, never MD5/SHA-1. Slowness makes each guess expensive; the per-user salt defeats precomputed tables. Better still, move users to passkeys.

**13. What is a passkey and why is it better than a password?**
*Answer:* A passkey is a public-key credential (WebAuthn/FIDO2). Your device keeps a private key; the site stores only the public key and sends a challenge your device signs. It is tied to the real domain, so it resists phishing, it can't be reused or guessed, and a server leak gives attackers nothing to replay. The weak spot is account recovery.

**14. What is "harvest now, decrypt later", and what is the post-quantum timeline?**
*Answer:* Attackers can record encrypted traffic today and decrypt it once a powerful quantum computer exists, so long-lived secrets are at risk now. NIST published ML-KEM, ML-DSA and SLH-DSA in August 2024, and its transition plan (IR 8547, final October 2026) deprecates RSA/ECC after 2030 and disallows them after 2035. Practical steps: inventory RSA/ECC use, be crypto-agile, prefer TLS 1.3, adopt hybrid post-quantum key exchange as libraries support it.

**15. What happens when you type https://example.com into a browser?**
*Answer:* DNS lookup, TCP handshake, TLS handshake, HTTP request, server processing, response and render. I add one risk per step: DNS spoofing, floods, MITM, session theft/CSRF, injection and broken access control, XSS.

**16. 401 vs 403, and what do HttpOnly, Secure and SameSite do?**
*Answer:* 401 means not authenticated; 403 means authenticated but not allowed. HttpOnly hides a cookie from JavaScript (limits XSS theft), Secure sends it only over HTTPS, SameSite limits cross-site sending (limits CSRF).

---

## C. Web, API and vulnerability management

**17. What is SQL injection and how do you prevent it?**
*Answer:* Untrusted input is interpreted as part of a SQL query, so an attacker changes its meaning. Prevent with parameterized queries and a least-privilege database account; escaping and WAFs are not the primary fix. The 2023 MOVEit campaign used a SQL injection flaw to steal data from thousands of organizations.

**18. XSS: types and prevention?**
*Answer:* The attacker's script runs in another user's browser under your origin: stored, reflected or DOM-based. Primary fix: context-aware output encoding (frameworks do it by default, so watch escape hatches like `dangerouslySetInnerHTML`). Layers: CSP and HttpOnly cookies.

**19. CSRF, and how is it different from XSS?**
*Answer:* CSRF abuses the browser's automatic cookie sending to make the victim's browser perform an action; no attacker code runs on your site. XSS runs attacker code in your page. Prevent CSRF with SameSite cookies and anti-CSRF tokens. An XSS flaw defeats CSRF tokens.

**20. What are IDOR and BOLA?**
*Answer:* The same flaw: changing an identifier (`/orders/1002`) to reach someone else's object because the server checked "logged in?" but not "allowed to see this object?". BOLA is #1 on the OWASP API Security Top 10. Fix: scope every lookup to the current user and deny by default. Unguessable IDs are a bonus, not a control.

**21. How would you secure a REST API?**
*Answer:* HTTPS; strong authentication with short-lived tokens; per-object and per-function authorization (BOLA and BFLA); validate input and use parameterized queries; return only needed fields; rate limiting; no secrets in code or URLs; restrictive CORS; keep an inventory of endpoints and retire old ones; log auth and access failures; scan dependencies.

**22. What is SSRF?**
*Answer:* Making the server fetch an attacker-chosen URL so it reaches internal services, such as the cloud metadata service. Fix: allowlist destinations, block private and link-local IPs, use the hardened metadata service (IMDSv2), and give the server's cloud role least privilege. OWASP merged it into A01 in 2025.

**23. Same-origin policy and CORS?**
*Answer:* The same-origin policy stops one origin's scripts reading another origin's responses. CORS is the server selectively relaxing that with headers. It doesn't add security; careless CORS (`*` with credentials) removes it.

**24. Name the OWASP Top 10 (2025).**
*Answer:* A01 Broken Access Control, A02 Security Misconfiguration, A03 Software Supply Chain Failures (new), A04 Cryptographic Failures, A05 Injection, A06 Insecure Design, A07 Authentication Failures, A08 Software or Data Integrity Failures, A09 Security Logging and Alerting Failures, A10 Mishandling of Exceptional Conditions (new). SSRF folded into A01.

**25. What should you watch for with JWTs?**
*Answer:* Verify the signature and pin the algorithm server-side; use a strong secret; keep tokens short-lived with a revocation plan; don't store them in `localStorage` (XSS can read it), prefer an HttpOnly cookie; the payload is only encoded, so no secrets inside.

**26. What is session hijacking and session fixation?**
*Answer:* Hijacking steals or predicts a valid session ID or token (via XSS, malware, or a phishing proxy). Fixation plants a known ID before login. Defend with HttpOnly/Secure/SameSite cookies, a new session ID at login, short sessions, and server-side invalidation on logout or compromise.

**27. How can OAuth be abused?**
*Answer:* Through consent phishing (a malicious app gets broad scopes) and stolen tokens. In the Salesloft Drift incident (2025), stolen OAuth tokens for an integration let attackers pull data from many customers' Salesforce accounts. Defend with least-privilege scopes, an inventory of connected apps, short-lived tokens, and the ability to revoke fast.

**28. CVE vs CWE vs CVSS vs KEV, and how do you prioritize patches?**
*Answer:* CVE is one specific flaw; CWE is the weakness category; CVSS is a 0-10 severity; KEV is CISA's list of flaws exploited in the wild. Prioritize known-exploited first, then internet-facing assets, then CVSS and business impact. Verizon found only about 26% of known-exploited flaws were fully fixed, with a median of 43 days.

---

## D. Identity and people

**29. How can MFA be bypassed?**
*Answer:* By adversary-in-the-middle phishing: a look-alike site proxies the real login, the victim enters password and MFA code, and the proxy steals the session cookie. Also by prompt bombing (fatigue), SIM swapping and help-desk resets. Phishing-resistant MFA (passkeys/FIDO2) defeats the proxy because the credential is bound to the real domain.

**30. How would you reduce account takeover?**
*Answer:* Passkeys where possible; MFA everywhere, preferring number matching or hardware keys over SMS; rate limiting and breached-password checks; short sessions with revocation; monitoring for impossible travel and new devices; and hardened recovery and help-desk procedures, since attackers go around strong login through weak recovery.

**31. How do you defend against help-desk social engineering?**
*Answer:* Strong identity verification before any reset or MFA change, call-back to a known number, extra approval for privileged accounts, no resets under time pressure, and logging. The help desk is part of the perimeter: MGM (2023) and Marks & Spencer (2025) were linked to this technique in public reporting.

**32. Credential stuffing vs password spraying?**
*Answer:* Stuffing replays leaked username and password pairs from other breaches because people reuse passwords. Spraying tries a few common passwords across many accounts to avoid lockouts. Both are blunted by MFA, passkeys, rate limiting and monitoring.

**33. What is an infostealer and why does it matter?**
*Answer:* Malware that copies saved passwords, cookies and tokens from a device and sells them. It feeds credential stuffing and session theft. In the 2024 Snowflake incidents, credentials stolen by infostealers (some years earlier) still worked on accounts without MFA.

---

## E. Infrastructure and operations

**34. Firewall vs IDS vs IPS vs WAF?**
*Answer:* A firewall filters by IP, port and state. An IDS watches a copy of traffic and alerts. An IPS sits inline and blocks. A WAF understands HTTP and blocks web-attack patterns. EDR watches the endpoint itself.

**35. How do you defend against DDoS?**
*Answer:* Put a CDN or scrubbing service in front so volume is absorbed at the edge, rate-limit per client, cache and make expensive endpoints cheap, hide the origin IP, and have a runbook. Cloudflare's H1 2026 data showed DNS and reflection floods leading, 1+ Tbps attacks surging, but most attacks being under 500 Mbps and over within 10 minutes.

**36. What is a man-in-the-middle attack?**
*Answer:* An attacker relays and possibly alters traffic between two parties, for example via a rogue Wi-Fi point. Defence: TLS with certificate validation plus HSTS, so interception yields only ciphertext and a forged certificate is rejected.

**37. How does ransomware work and how do you defend?**
*Answer:* Initial access (an edge-device flaw, a stolen login, phishing or a help-desk call), taking control, spreading, stealing data, then encrypting and extorting. Defend the chain: patch edge devices, phishing-resistant MFA, least privilege, segmentation, EDR, outbound monitoring, tested offline backups and a practised incident plan.

**38. What is a software supply-chain attack and how do you defend?**
*Answer:* Compromising something you depend on (a package, maintainer, build system or tool) to compromise you. Recent examples: the Shai-Hulud npm worm (2025), the XZ Utils backdoor (2024) and the 2026 developer-tool compromises. Defend with lockfiles and exact versions, a cooldown on new versions, scanning, an SBOM, short-lived tokens with MFA, hardened CI/CD and fewer dependencies.

**39. How do you manage secrets and avoid cloud misconfiguration?**
*Answer:* Never in code, Git or front-end bundles. Use a secrets manager, inject at runtime, give each service least-privilege short-lived credentials, rotate on any exposure, run secret scanning, and keep storage private by default with account-level public-access blocks.

**40. How do you manage third-party risk?**
*Answer:* Inventory vendors and integrations, grant least-privilege scopes, minimize the data they hold, be able to revoke tokens fast, and review their security evidence. Third parties were involved in about 48% of breaches in Verizon's 2026 report.

---

## F. AI and scenarios

**41. What is prompt injection and how do you defend against it?**
*Answer:* An LLM can't reliably separate instructions from data, so text it reads (an email, a web page) can steer it. Indirect injection is the dangerous kind. There is no complete fix, so layer defences: least-privilege tools, human approval for sensitive actions, treating output as untrusted, no secrets in prompts, and breaking the combination of private data, untrusted content and an outbound channel. EchoLeak (Microsoft 365 Copilot, 2025) was a zero-click example.

**42. How would you secure an AI feature or agent with access to customer data?**
*Answer:* It acts with the *user's* permissions, never a super-account; per-user authorization on every retrieval and tool call; minimal tools with confirmation for risky actions; validate and encode its output; rate limits and spending caps; logging and monitoring; and red-teaming for injection before launch.

**43. You find a critical vulnerability in production. What do you do?**
*Answer:* Don't probe further than needed. Document what I saw, report it immediately through the proper channel, help assess impact, support the fix and deployment, verify, and run a blameless post-mortem. They are testing process and ethics, not heroics.

**44. You suspect a breach. First steps?**
*Answer:* Incident response: identify and scope; contain (isolate systems, revoke credentials **and sessions**); eradicate the cause; recover from clean backups; learn. Preserve evidence and don't just reboot everything, which destroys evidence and may tip off the attacker.

**45. How do you build security into development?**
*Answer:* Threat-model new features (STRIDE); secure defaults (parameterized queries, output encoding, per-object authorization); secret scanning, SAST and dependency scanning in CI plus DAST on staging; pinned dependencies and an SBOM; secrets in a manager; least privilege everywhere; and review AI-generated code like a stranger's.

---

## Bonus: three behavioural questions that always come up

- **"Tell me about a security issue you found or fixed."** Use your prepared war story: situation, what you did, outcome, what changed afterwards.
- **"How do you stay current?"** Name two real sources (for example the OWASP lists, CISA advisories, the Verizon DBIR, a security newsletter, hands-on labs on PortSwigger) and one recent thing you learned.
- **"A teammate says security slows us down. How do you respond?"** Security is cheaper early (design, code review) than late (incident and rewrite); automate checks in CI so they cost minutes; start with the highest-risk paths; make the secure way the easy way.
