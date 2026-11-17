# Cheat Sheets

> Copy-paste starting points and facts to recall fast. Adapt every snippet to your stack and **test it**; a cheat sheet is a starting point, not a guarantee.

---

## 1. The answer shape

**Threat → control (with a one-line example) → a backup layer → how you'd test it.**

---

## 2. The secure request pipeline

1. TLS + HSTS · 2. Limits (rate, size) · 3. Authenticate · 4. **Authorize per object** · 5. Validate (schema) · 6. Do the work (parameterized, least privilege) · 7. Respond (minimal fields, encoded, generic errors) · 8. Log (no secrets)

---

## 3. Cookies

```ts
res.cookie("__Host-sid", sessionId, { httpOnly: true, secure: true, sameSite: "lax", path: "/", maxAge: 8 * 3600 * 1000 });
```

`HttpOnly` blocks script reads · `Secure` HTTPS only · `SameSite` limits cross-site sending (set it explicitly) · `__Host-` prefix forces Secure, `Path=/`, no `Domain`.

---

## 4. Security headers (starting point)

| Header | Value |
| --- | --- |
| `Strict-Transport-Security` | `max-age=63072000; includeSubDomains` |
| `X-Content-Type-Options` | `nosniff` |
| `Referrer-Policy` | `strict-origin-when-cross-origin` |
| `Permissions-Policy` | `camera=(), microphone=(), geolocation=()` |
| `Cache-Control` (sensitive responses) | `no-store` |
| `Content-Security-Policy` | see section 5 |

```ts
app.disable("x-powered-by"); app.use(helmet());   // then review helmet's defaults against your app
```

---

## 5. CSP starter (nonce-based; deploy as `-Report-Only` first)

```
default-src 'self';
script-src 'self' 'nonce-{RANDOM_PER_RESPONSE}' 'strict-dynamic';
style-src 'self' 'unsafe-inline';
img-src 'self' data: https:;
connect-src 'self' https://api.example.com;
object-src 'none'; base-uri 'self'; frame-ancestors 'none'; form-action 'self'
```

Avoid `'unsafe-inline'` and `'unsafe-eval'` for scripts. CSP reduces XSS impact; it does not replace encoding.

---

## 6. CORS rules

- Allowlist **exact origins**; never reflect `Origin` with credentials (`cors({ origin: true, credentials: true })` is the bug).
- Don't allow `null`; anchor any regex (`^https://app\.example\.com$`).
- CORS only governs what a **browser page may read**. It is not authentication, authorization or CSRF protection.

---

## 7. CSRF

SameSite cookies + CSRF token (or Origin check, or custom header for JSON APIs) · never change state on `GET` · re-authenticate for sensitive actions.

---

## 8. Passwords (OWASP minimums)

| Algorithm | Minimum |
| --- | --- |
| **Argon2id** | `m=19456 KiB (19 MiB), t=2, p=1` |
| scrypt | `N=2^17, r=8, p=1` |
| bcrypt (legacy) | work factor ≥ 10; 72-byte limit |
| PBKDF2-HMAC-SHA256 | 600,000 iterations |

Store the algorithm and parameters with the hash; rehash on login; check breached lists; rate-limit; never encrypt or use fast hashes.

---

## 9. JWT checklist

☐ **verify**, never `decode` · ☐ pin `algorithms` · ☐ check `iss`, `aud`, `exp` · ☐ strong secret or asymmetric keys · ☐ short-lived + refresh rotation · ☐ not in `localStorage` · ☐ no secrets in the payload

```ts
await jwtVerify(token, JWKS, { issuer, audience, algorithms: ["RS256"] });
```

---

## 10. Authorization checklist

☐ identity from session, not request · ☐ every query scoped to owner/tenant · ☐ role middleware, deny by default · ☐ strict input schema (no mass assignment) · ☐ response DTO (no extra fields) · ☐ cross-user test per route · ☐ UI hiding is not enforcement

---

## 11. Injection quick table

| Risk | Unsafe | Safe |
| --- | --- | --- |
| SQL | string-built SQL, `$queryRawUnsafe`, `.raw(f"...")` | placeholders, `$queryRaw` tagged template, allowlisted identifiers |
| NoSQL | pass `req.body` into a query | schema that requires strings |
| Shell | `exec(string)`, `shell=True` | `execFile(cmd, [args])`, `shell=False` |
| Path | `path.join(base, userInput)` | `resolve` + prefix check, or random IDs |
| HTML | `innerHTML`, `dangerouslySetInnerHTML` | text rendering, DOMPurify, CSP |
| URL | raw user `href`, `?next=` | scheme allowlist, internal-path allowlist |
| Deserialize | `pickle.loads`, `yaml.load` | JSON + schema, `yaml.safe_load` |

---

## 12. SSRF, uploads, webhooks (one line each)

- **SSRF:** allowlist hosts; block private/loopback/link-local (incl. `169.254.169.254`); pin the validated IP; check redirects; timeouts and size caps; IMDSv2.
- **Uploads:** limit size, check real content, random name, store outside web root, serve from a separate domain with `nosniff`.
- **Webhooks:** raw body, HMAC, timestamp window, constant-time compare, idempotent handler.

---

## 13. Supply chain commands and settings

```bash
npm ci --ignore-scripts          # exact lockfile, no install scripts
npm audit && npm audit signatures
osv-scanner --lockfile package-lock.json     # or pip-audit for Python
gitleaks detect                              # scan for committed secrets
npm sbom --sbom-format cyclonedx > sbom.json
pip install --require-hashes -r requirements.txt
```

Cooldown on new releases: Dependabot `cooldown`, Renovate `minimumReleaseAge`, pnpm `minimumReleaseAge`.

---

## 14. GitHub Actions hardening

```yaml
permissions: { contents: read }
steps:
  - uses: actions/checkout@<FULL-40-CHAR-COMMIT-SHA>      # pin by SHA, not a tag
  - env: { TITLE: "${{ github.event.pull_request.title }}" }   # never inline untrusted input in run:
    run: echo "$TITLE"
```

Avoid `pull_request_target` with untrusted code · no secrets for forks · OIDC to the cloud · protected branches · CODEOWNERS on `.github/`.

---

## 15. Secure Dockerfile in six lines

Multi-stage build · `npm ci --ignore-scripts` · minimal/distroless runtime pinned by digest · `USER nonroot` · no secrets in the image · read-only filesystem and dropped capabilities at runtime.

---

## 16. Fast facts (with sources in [15-sources.md](15-sources.md))

| Fact | Detail |
| --- | --- |
| Verizon DBIR 2026 (as reported) | Exploited vulnerabilities about 31% of breach starts; stolen credentials about 13%; third parties in about 48% of breaches; known-exploited flaws median 43 days to fix |
| **React2Shell** | CVE-2025-55182, CVSS 10; RCE in React Server Components; affected `react-server-dom-*` 19.0 to 19.2.0; fixed 19.0.1, 19.1.2, 19.2.1 (and matching Next.js releases); on CISA KEV 5 Dec 2025 |
| **Next.js middleware bypass** | CVE-2025-29927, CVSS 9.1; `x-middleware-subrequest` header; fixed 12.3.5, 13.5.9, 14.2.25, 15.2.3 |
| **npm token changes** | Trusted publishing (OIDC) GA 31 Jul 2025; classic tokens revoked 9 Dec 2025; granular write tokens 90-day max with 2FA by default |
| **tj-actions** (Mar 2025) | CVE-2025-30066; version tags rewritten; 23,000+ repos' secrets at risk; pin Actions to a SHA |
| **chalk/debug** (8 Sep 2025) | Maintainer phished; about 18 packages, 2B+ weekly downloads; crypto-stealer; live for hours |
| **OWASP Top 10 (2025)** | A01 Broken Access Control, A02 Security Misconfiguration, A03 Software Supply Chain Failures *(new)*, A04 Cryptographic Failures, A05 Injection, A06 Insecure Design, A07 Authentication Failures, A08 Software or Data Integrity Failures, A09 Logging and Alerting Failures, A10 Mishandling of Exceptional Conditions *(new)* |
| **OWASP API Top 10 (2023)** | API1 BOLA, API2 Broken Authentication, API3 Broken Object Property Level Authorization, API4 Unrestricted Resource Consumption, API5 BFLA, API6 Sensitive Business Flows, API7 SSRF, API8 Misconfiguration, API9 Improper Inventory, API10 Unsafe Consumption of APIs |
| **OWASP LLM Top 10 (2025)** | LLM01 Prompt Injection · 02 Sensitive Information Disclosure · 03 Supply Chain · 04 Data and Model Poisoning · 05 Improper Output Handling · 06 Excessive Agency · 07 System Prompt Leakage · 08 Vector and Embedding Weaknesses · 09 Misinformation · 10 Unbounded Consumption |
| **ASVS 5.0** | Released May 2025; use Level 1 as the baseline checklist |

---

## 17. Grep your own repo for red flags

```bash
grep -rnE "dangerouslySetInnerHTML|innerHTML|eval\(|new Function|\\\$queryRawUnsafe|origin: true|jwt\.decode|Math\.random|rejectUnauthorized: false|verify=False|pull_request_target|NEXT_PUBLIC_.*(KEY|SECRET|TOKEN)" \
  --include=*.ts --include=*.tsx --include=*.js --include=*.jsx --include=*.py --include=*.yml --include=*.yaml .
```

Each hit is a *question*, not necessarily a bug. Ask the five review questions about it.

---

## 18. The 60-second self-test

Say these five aloud, without notes:

1. The secure request pipeline, in order.
2. How to fix BOLA in one line of code, and the test that proves it.
3. Where a SPA keeps its login, and why not `localStorage`.
4. What React2Shell and the Next.js middleware bypass each teach you.
5. How to harden a GitHub Actions workflow in three changes.
