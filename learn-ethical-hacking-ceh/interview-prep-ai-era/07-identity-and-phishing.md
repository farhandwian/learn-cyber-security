# Chapter 7: Identity, Phishing and Modern Authentication

> **Goal.** After this chapter you can: explain why identity is the main battlefield; list how logins get stolen; rank MFA methods and explain why ordinary MFA fails against adversary-in-the-middle (AiTM) phishing; explain passkeys; handle sessions, JWTs and OAuth correctly; and describe help-desk social engineering.
>
> **Time:** about 60 minutes. This is the most current chapter: stolen access and phishing sit behind most major incidents of 2024-2026.

---

## 1. Identity is the perimeter

Staff, vendors and apps log in from anywhere, so **the login is the perimeter**. In Verizon's 2026 data (as reported), stolen credentials and pretexting were about 13% and 6% of breach starts, and most ransomware stories begin with someone's valid access.

## 2. How logins get stolen

| Method | How | Main defence |
| --- | --- | --- |
| **Credential stuffing** | Replay leaked pairs from other sites | MFA, passkeys, breached-password checks, rate limits |
| **Password spraying** | A few common passwords against many accounts | MFA, monitoring spread-out failures |
| **Infostealer malware** | Copies saved passwords, cookies, tokens from a device | Endpoint protection, short-lived sessions |
| **Phishing** | Fake page or prompt | Phishing-resistant MFA, training |
| **Help-desk calls** | Impersonate an employee to get a reset | Strong verification, call-back |
| **MFA fatigue** | Spam push prompts until "yes" | Number matching, passkeys |

> **Real case: Snowflake customers (2024).** Mandiant traced the incidents to compromised customer credentials, mostly from infostealers. The accounts had no MFA, credentials were still valid (some from infections back to 2020) and there was no network allow-list. At least 165 organizations were hit; Snowflake's own platform was not breached. Lessons: enforce MFA, rotate old credentials, restrict login origins.

---

## 3. The MFA ladder

![Not all MFA is equal](images/27-mfa-ladder.svg)

Each rung beats more attacks, but **only passkeys/FIDO2 resist phishing proxies**, and even they have a weak spot in account recovery. "We have MFA, so we're safe" is a common mistake: codes and push approvals can be relayed.

## 4. AiTM phishing and session theft

The attacker runs a look-alike login page that is a **live proxy** to the real site. The victim enters the password and approves MFA, and the proxy captures the **session cookie** the real site issues. The attacker replays it without breaking MFA.

![Adversary-in-the-middle phishing](images/26-aitm-phishing.svg)

**Changing the password does not end the access**: the stolen session stays valid until it expires or is revoked. Defences: passkeys (bound to the real domain), shorter sessions and risk-based re-checks, **revoking all sessions** when phishing is suspected, and monitoring for new mailbox rules, devices and impossible travel.

## 5. Passkeys

A passkey is public-key login (WebAuthn/FIDO2): at registration the device makes a key pair for the site and gives it the public key; at login it signs the site's random challenge with the private key (after you unlock it), and the signature is tied to the real domain. Benefits: phishing-resistant, nothing reusable on the server, no stuffing or spraying. **Honest limits:** account recovery becomes the weakest link, adoption is partial, and passkeys do not help if malware already runs on the device.

![Password storage](images/23-password-storage.svg)

**Passwords you still store (OWASP minimums):** Argon2id (m=19 MiB, t=2, p=1), scrypt (N=2^17, r=8, p=1), bcrypt (work factor 10+, 72-byte limit) or PBKDF2-HMAC-SHA256 (600,000 iterations). Store parameters with the hash, rehash on login, rate-limit, never use fast hashes or reversible encryption.

---

## 6. Sessions, JWTs and OAuth

**Sessions:** long random ID from a secure generator; rotate at login (stops fixation); `HttpOnly`, `Secure`, `SameSite`; expire; logout invalidates server-side.

| JWT pitfall | Fix |
| --- | --- |
| Signature or algorithm not verified (`alg: none`, or `decode` used for access) | `verify`, pin the algorithm, check issuer, audience, expiry |
| Weak secret | Long random secret or asymmetric keys |
| Long-lived, no revocation | Short expiry plus refresh rotation |
| Stored in `localStorage` | `HttpOnly` cookie (or a BFF) |
| Secrets in the payload | The payload is encoded, not encrypted |

**OAuth 2.0** lets an app act for you without your password (scopes, access token); **OIDC** adds login. Use the **authorization code flow with PKCE**. Risks: consent phishing and stolen or over-broad tokens.

> **Real case: Salesloft Drift (August 2025).** Attackers obtained OAuth tokens for the Drift integration and used them to pull data from many customers' Salesforce accounts; Google's threat team said it knew of 700+ potentially impacted organizations. Lessons: a vendor's token is your data; least-privilege scopes, an inventory of connected apps, fast revocation.

---

## 7. Social engineering today

Verizon's 2026 report (as reported) splits out **pretexting** at about 6%. Attackers moved to **voice calls and chats**.

| Technique | Defence |
| --- | --- |
| **Vishing** (voice phishing) | Call back a known number; never act on inbound calls |
| **Help-desk impersonation** | Strong verification before any reset; manager approval for privileged accounts |
| **Business email compromise** | Two-person approval for payments; verify bank-detail changes by phone |
| **AI-assisted fraud** (better text, cloned voices) | Process checks that do not depend on "it sounded right" |

> **Real case: help-desk attacks (2023, 2025).** Public reporting links MGM Resorts (2023) and Marks & Spencer (2025) to attackers who impersonated employees to the IT help desk (attributed to Scattered Spider; details of the M&S call are reported, not formally confirmed). The help desk is part of your perimeter.

**Mindset:** assume someone will be fooled, and make sure one fooled person cannot do catastrophic damage.

> **AI-agent era.** Agents are "phished" the way users are: hostile text in a web page, issue or tool description can steer them (prompt injection, Chapter 11), and they act with your tokens. Give agents their own scoped, short-lived credentials, never your personal admin session, and never leave long-lived tokens in files or the environment an agent can read: the 2025 Nx "s1ngularity" attack made installed AI tools hunt for secrets on developer machines (over 400 users or organizations affected, as reported by InfoQ).

---

## Check yourself

1. Name four ways a login is stolen.
2. Why does ordinary MFA fail against an AiTM proxy and passkeys do not?
3. Why does changing the password not end access after session theft?
4. List three JWT mistakes and their fixes.

**Answers** *(cover this until you have tried)*

1. Any four of: credential stuffing, password spraying, infostealers, phishing, help-desk impersonation, MFA fatigue.
2. The proxy relays the code or approval and captures the session cookie; a passkey is bound to the real domain, so a look-alike cannot obtain a valid response.
3. The stolen session cookie stays valid until it expires or is revoked; revoke sessions.
4. For example: `decode` instead of `verify` (verify with a pinned algorithm); long-lived tokens (short expiry plus refresh rotation); `localStorage` storage (HttpOnly cookie or BFF).

---

## Summary

- Identity is the perimeter: stuffing, spraying, infostealers, phishing, help-desk calls, prompt bombing.
- Only passkeys/FIDO2 resist AiTM; AiTM steals the session, so revoke sessions and shorten them.
- Verify tokens properly; OAuth tokens are access (Drift, 2025); store passwords with OWASP-minimum hashing.
- The help desk and phone are attack surfaces; verify before you reset.
- Agents need their own scoped credentials, and can be steered by hostile content.
