# Chapter 10: Cheat Sheets

> **Goal.** Copy-paste starting points and facts to recall fast. Adapt every snippet to your stack and **test it**; a cheat sheet is a starting point, not a guarantee.
>
> **Time:** about 30 minutes to skim, then keep open while you review code.

---

## 1. Answer shape and request pipeline

**Threat, then control (one-line example), then a backup layer, then how you would test it.**

**Pipeline:** TLS + HSTS · limits (rate, size) · authenticate · **authorize per object** · validate (schema) · do the work (parameterized, least privilege) · respond (minimal fields, encoded, generic errors) · log (no secrets).

---

## 2. Cookies and headers

```ts
res.cookie("__Host-sid", sessionId, { httpOnly: true, secure: true, sameSite: "lax", path: "/", maxAge: 8 * 3600 * 1000 });
app.disable("x-powered-by"); app.use(helmet());   // then review helmet's defaults for your app
```

`HttpOnly` blocks script reads · `Secure` HTTPS only · `SameSite` limits cross-site sending · `__Host-` forces Secure, `Path=/`, no `Domain`.

| Header | Value |
| --- | --- |
| `Strict-Transport-Security` | `max-age=63072000; includeSubDomains` |
| `X-Content-Type-Options` | `nosniff` |
| `Referrer-Policy` | `strict-origin-when-cross-origin` |
| `Permissions-Policy` | `camera=(), microphone=(), geolocation=()` |
| `Cache-Control` (sensitive) | `no-store` |

**CSP starter** (nonce-based; deploy as `Content-Security-Policy-Report-Only` first):

```
default-src 'self';
script-src 'self' 'nonce-{RANDOM_PER_RESPONSE}' 'strict-dynamic';
style-src 'self' 'unsafe-inline'; img-src 'self' data: https:;
connect-src 'self' https://api.example.com;
object-src 'none'; base-uri 'self'; frame-ancestors 'none'; form-action 'self'
```

CSP reduces XSS impact; it does not replace encoding.

---

## 3. CORS, CSRF

- **CORS:** allowlist exact origins; never reflect `Origin` with credentials (`cors({ origin: true, credentials: true })` is the bug); do not allow `null`; anchor any regex. CORS is not authentication or CSRF protection.
- **CSRF:** SameSite cookies + token (or Origin check, or a custom header for JSON APIs); never change state on `GET`; re-authenticate for sensitive actions.

---

## 4. Passwords and JWT

| Algorithm | OWASP minimum |
| --- | --- |
| **Argon2id** | `m=19456 KiB (19 MiB), t=2, p=1` |
| scrypt | `N=2^17, r=8, p=1` |
| bcrypt (legacy) | work factor ≥ 10; 72-byte limit |
| PBKDF2-HMAC-SHA256 | 600,000 iterations |

Store algorithm and parameters with the hash; rehash on login; check breached lists; rate-limit; never encrypt or use fast hashes.

**JWT:** ☐ **verify**, never `decode` · ☐ pin `algorithms` · ☐ check `iss`, `aud`, `exp` · ☐ strong secret or asymmetric keys · ☐ short-lived + refresh rotation · ☐ not in `localStorage` · ☐ no secrets in payload.

**Authorization:** ☐ identity from session, not request · ☐ every query scoped to owner/tenant · ☐ deny-by-default roles · ☐ strict input schema · ☐ response DTO · ☐ cross-user test per route · ☐ UI hiding is not enforcement.

---

## 5. Injection quick table

| Risk | Unsafe | Safe |
| --- | --- | --- |
| SQL | string-built SQL, `$queryRawUnsafe` | placeholders, tagged templates, allowlisted identifiers |
| NoSQL | pass `req.body` into a query | schema requiring strings |
| Shell | `exec(string)`, `shell=True` | `execFile(cmd, [args])`, `shell=False` |
| Path | `path.join(base, userInput)` | `resolve` + prefix check, or random IDs |
| HTML | `innerHTML`, `dangerouslySetInnerHTML` | text rendering, DOMPurify, CSP |
| URL | raw user `href`, `?next=` | scheme allowlist, internal-path allowlist |
| Deserialize | `pickle.loads`, `yaml.load` | JSON + schema, `yaml.safe_load` |

**One-liners:** *SSRF:* allowlist hosts, block private/loopback/link-local (incl. `169.254.169.254`), pin the validated IP, check redirects, timeouts, IMDSv2. *Uploads:* limit size, check real content, random name, outside web root, separate domain with `nosniff`. *Webhooks:* raw body, HMAC, timestamp window, constant-time compare, idempotent.

---

## 6. Supply chain and CI

```bash
npm ci --ignore-scripts                  # exact lockfile, no install scripts
npm audit && npm audit signatures
osv-scanner --lockfile package-lock.json # or pip-audit for Python
gitleaks detect                          # committed secrets
```

Cooldown on new releases: Dependabot `cooldown`, Renovate `minimumReleaseAge`, pnpm `minimumReleaseAge`.

```yaml
permissions: { contents: read }
steps:
  - uses: actions/checkout@<FULL-40-CHAR-COMMIT-SHA>        # pin by SHA, not a tag
  - env: { TITLE: "${{ github.event.pull_request.title }}" }  # never inline untrusted input in run:
    run: echo "$TITLE"
```

Avoid `pull_request_target` with untrusted code · no secrets for forks · OIDC to the cloud · branch protection · CODEOWNERS on `.github/`.

---

## 7. Glossary (25 terms)

| Term | Meaning |
| --- | --- |
| **AiTM** | A phishing proxy that relays a real login and steals the session |
| **Attack surface** | Everything an attacker can reach |
| **BFLA / BOLA** | Calling a function you should not / reaching another user's object |
| **CIA triad** | Confidentiality, integrity, availability |
| **CORS** | A mechanism that selectively *relaxes* the same-origin policy |
| **Credential stuffing** | Replaying leaked username/password pairs on other sites |
| **CSP** | A header limiting where scripts and content may load from |
| **CSRF** | Tricking a victim's browser into an unintended authenticated request |
| **CVE / CWE / CVSS / KEV** | One flaw / a weakness type / a 0-10 severity / CISA's exploited-now list |
| **Defence in depth** | Overlapping controls so one failure is not fatal |
| **Double extortion** | Steal data *and* encrypt systems, then threaten to leak |
| **EDR** | Software that monitors endpoints for attacks |
| **HSTS** | Header telling browsers to always use HTTPS for a site |
| **IDOR** | Reaching another user's object by changing an identifier |
| **Infostealer** | Malware that copies saved passwords, cookies and tokens |
| **JWT** | A signed token carrying identity claims |
| **Least privilege** | Only the access that is needed |
| **MITM** | An attacker relaying and possibly altering traffic |
| **OAuth / OIDC** | Delegated access with tokens / login built on it |
| **OSINT** | Information gathered from public sources |
| **Passkey** | A WebAuthn/FIDO2 public-key credential tied to a domain |
| **Prompt injection** | Text the model reads that steers it against its instructions |
| **SBOM** | A list of the components in your software |
| **SSRF** | Making the server fetch a URL the attacker chooses |
| **Zero trust** | Never trust a request because of where it comes from |

---

## 8. Grep your own repo for red flags

```bash
grep -rnE "dangerouslySetInnerHTML|innerHTML|eval\(|new Function|\\\$queryRawUnsafe|origin: true|jwt\.decode|Math\.random|rejectUnauthorized: false|verify=False|pull_request_target|NEXT_PUBLIC_.*(KEY|SECRET|TOKEN)" \
  --include=*.ts --include=*.tsx --include=*.js --include=*.jsx --include=*.py --include=*.yml --include=*.yaml .
```

Each hit is a *question*, not necessarily a bug. Ask the five review questions about it. Use it on AI-generated code too.

---

## 9. The 60-second self-test

Say these aloud, without notes:

1. The secure request pipeline, in order.
2. How to fix BOLA in one line of code, and the test that proves it.
3. Where a single-page app keeps its login, and why not `localStorage`.
4. What React2Shell and the Next.js middleware bypass each teach you.
5. How to harden a GitHub Actions workflow in three changes.
