# Interview Q&A: 50 Questions

> **Goal.** Answer each question in 45-90 seconds, out loud, in the shape **threat, control, backup layer, how you'd test it** (see [00-start-here.md](00-start-here.md)).
>
> **How to drill:**
> 1. **Round 1:** read the question, cover the answer, **say your answer out loud**, compare. Mark green / yellow / red.
> 2. **Round 2 (two days later):** only yellow and red.
> 3. **Round 3:** [Lab 12](13-labs.md), a recorded mock interview in random order with one design question.
>
> Frontend engineers: spend extra time on sections A, B and D. Backend engineers: A, C and D. Everyone: E.

---

## A. Shared core

**1. What are the biggest risks for web applications right now?**
Exploited known vulnerabilities (the top breach start in Verizon's 2026 report, about 31%), stolen or phished credentials, and third parties (about 48% of breaches), including dependencies and CI. At the application level, broken access control is #1 on OWASP's 2025 list. React2Shell (CVSS 10, December 2025) is the example of how fast a framework flaw gets exploited.

**2. Where is the trust boundary, and where do you validate?**
The browser is untrusted: anything the client sends can be forged. Frontend validation is UX; the server validates and authorizes every request. I take identity from the session or token, never from request fields.

**3. Walk me through the secure request pipeline.**
TLS and HSTS; limits (rate, size); authenticate; authorize per object; validate against a schema; do the work with parameterized queries and a least-privilege DB user; respond with minimal fields, encoded, generic errors; log security events without secrets.

**4. Authentication vs authorization, and 401 vs 403 vs 404?**
Authentication is who you are; authorization is what you may do, checked on every request for every object. 401 means not authenticated; 403 means authenticated but not allowed; I sometimes return 404 for "not yours" so existence isn't revealed.

**5. What are BOLA and IDOR, and how do you prevent them?**
The same flaw: changing an ID to reach someone else's object because the server checked "logged in" but not "owns this". I scope the query to the owner or tenant (`findFirst({ where: { id, ownerId } })`), return 404 otherwise, and add a test that logs in as A and requests B's resource. Unguessable IDs are a bonus, not a control.

**6. BOLA vs BFLA vs mass assignment?**
BOLA: reaching another user's object. BFLA: calling a function you shouldn't, like an admin endpoint. Mass assignment (BOPLA): setting fields you shouldn't by copying a request body into a model. Fixes: owner-scoped queries, role middleware with deny-by-default, and strict schemas with response DTOs.

**7. Sessions or JWTs?**
For a normal web app, server-side sessions in an HttpOnly cookie: easy to revoke, nothing for scripts to steal. JWTs suit stateless service-to-service calls and must be short-lived. In both cases I keep revocation and rotation in mind.

**8. How do you verify a JWT correctly?**
Verify the signature (never `decode`), pin the algorithm, check issuer, audience and expiry, use a strong secret or asymmetric keys, keep tokens short-lived, and don't put secrets in the payload since it's only encoded.

**9. How should passwords be stored?**
Argon2id with at least 19 MiB memory, 2 iterations, 1 parallelism (OWASP's minimum), parameters stored with the hash so I can rehash on login; scrypt (N=2^17, r=8, p=1) if Argon2id isn't available; bcrypt (work factor 10+, 72-byte limit) for legacy. Plus breached-password checks and rate limiting. Better still: passkeys.

**10. Explain the OAuth authorization code flow with PKCE.**
The app sends the user to the authorization server with a hashed `code_challenge`; after login the app receives a code and redeems it with the original `code_verifier`. A stolen code is useless without the verifier. I also use exact redirect URIs, a `state` check, minimal scopes and short-lived tokens, and a maintained library.

**11. What are passkeys, and what are their limits?**
Public-key credentials (WebAuthn/FIDO2): the device signs a server challenge with a private key scoped to the real domain, so phishing sites get nothing usable and a database leak exposes only public keys. Limits: account recovery becomes the weak link, and passwords and MFA fallbacks persist during adoption.

**12. Same-origin policy, CORS and CSRF: how do they relate?**
The same-origin policy stops a page *reading* other origins' responses, not *sending* requests. CORS is a server's way to relax that for chosen origins; it isn't authentication. CSRF abuses automatic cookie sending, defended by SameSite cookies, tokens or Origin checks. CORS settings don't fix CSRF.

---

## B. Frontend

**13. How does XSS happen in a React app, and how do you fix it?**
React escapes `{value}`, so XSS comes from escape hatches: `dangerouslySetInnerHTML`, raw `innerHTML`, user-supplied `href` (`javascript:` URLs), `eval`. Fixes: render text, sanitize with DOMPurify when HTML is required, allowlist URL schemes, and add a CSP as a second layer.

**14. What is a CSP and how would you roll it out?**
A header telling the browser which scripts may run. I'd use a nonce-based policy with `'strict-dynamic'`, `object-src 'none'`, `base-uri 'self'`, `frame-ancestors`, deploy it in report-only mode first, fix violations, then enforce and keep reporting. It reduces XSS impact; it doesn't replace encoding.

**15. Where do you store tokens in a single-page app?**
Not in `localStorage` (any XSS reads it). Best: a server-set HttpOnly session cookie with SameSite and CSRF protection, or a short-lived in-memory access token with an HttpOnly refresh cookie, or a BFF that keeps OAuth tokens off the browser. And fix XSS: HttpOnly limits what a foothold is worth, but scripts can still use the session while the page is open.

**16. Why are secrets in `NEXT_PUBLIC_` or `VITE_` variables a problem?**
Those prefixes inline values into the browser bundle, so they are public to anyone. Secrets belong on the server; the browser calls a backend endpoint instead. Public keys are fine only when the provider enforces domain and quota restrictions.

**17. Is a client-side route guard a security control?**
No, it's UX. Attackers call the API directly. Every action must be authorized on the server; the guard just hides things from honest users.

**18. How do you handle user-supplied URLs and redirects?**
Allowlist schemes (`http`, `https`, `mailto`) for links, `rel="noopener noreferrer"` for external links, and allowlist internal paths for `?next=` redirects to prevent open redirects used for phishing.

**19. What are the risks of third-party scripts, and how do you reduce them?**
They run with your page's privileges. Use fewer, pin versions, add Subresource Integrity for CDN files, sandbox iframes, restrict `connect-src` to limit exfiltration, and treat tag managers as a trust decision.

**20. How do you make `postMessage` safe?**
Check `event.origin` against an exact allowlist, validate the message shape with a schema, and use a specific target origin (never `"*"`) when sending sensitive data.

**21. What was the Next.js middleware bypass (CVE-2025-29927), and what is the lesson?**
In March 2025 (CVSS 9.1), a crafted `x-middleware-subrequest` header made Next.js skip middleware, bypassing authorization that lived only there. The lesson: authorize where the data is read, not only in middleware, and keep the framework patched (fixed in 12.3.5, 13.5.9, 14.2.25, 15.2.3).

**22. What is React2Shell and how do you respond to a framework CVE like it?**
CVE-2025-55182 (CVSS 10): unauthenticated remote code execution in React Server Components via crafted requests to Server Function endpoints; exploited within days and on CISA's KEV list from 5 December 2025. Response: identify affected packages from the lockfile or SBOM, upgrade to the fixed versions (React 19.0.1, 19.1.2, 19.2.1 and matching Next.js releases), consider temporary WAF rules, check logs, rotate secrets if exposed, and add this to the patching process.

---

## C. Backend

**23. How do you prevent SQL injection, including with an ORM?**
Parameterized queries everywhere; ORMs are safe until the raw escape hatch (`$queryRawUnsafe`, string-built `raw()`/`text()`). Allowlist identifiers like `ORDER BY` columns, use a least-privilege DB user, and add a WAF only as a backup. MOVEit (2023) shows SQL injection can still cause a mass breach.

**24. What is NoSQL injection?**
Supplying an object where a string was expected (`{"password": {"$ne": null}}`) so a Mongo query matches anything. Fix: strict schemas that reject objects, hash-compare passwords, never pass raw request objects into a query.

**25. How do you prevent command injection and path traversal?**
Avoid shells: `execFile`/`subprocess.run([...], shell=False)` with an allowlisted program and validated arguments, or use a library. For paths, resolve and check the prefix, or better, store files under random IDs. Beware zip-slip when extracting archives.

**26. How do you defend against SSRF?**
Allowlist hosts where possible; otherwise validate scheme and resolved IP against private, loopback and link-local ranges (including the cloud metadata address), connect to the validated address to avoid DNS rebinding, re-check redirects, add timeouts and size caps, don't return raw responses, use IMDSv2 and least-privilege cloud roles, and restrict egress.

**27. How do you handle file uploads securely?**
Require auth, cap size, check the real content (magic bytes) against an allowlist, rename to a random ID, store outside the web root or in object storage, serve from a separate domain with `nosniff` and download disposition, treat SVG and PDF as active content, and sandbox processing.

**28. How would you build a secure webhook receiver?**
Verify an HMAC signature over the raw body plus timestamp using a constant-time comparison, reject old timestamps to stop replays, keep the secret in a secrets manager, make the handler idempotent because providers retry, and respond quickly while processing in a queue.

**29. How do you design rate limiting against brute force and abuse?**
Per account *and* per IP, stricter on login, reset and signup; the same error for any failure; progressive delays or lockout with care to avoid denial of service by lockout; cap body, page and file sizes; budgets on endpoints that cost money. Correct `trust proxy` settings so the real client IP is used.

**30. What does "fail closed" mean and why does it matter?**
When something errors, deny rather than allow. A policy check that throws and leaves `allowed = true` is fail-open. OWASP added "Mishandling of Exceptional Conditions" (A10) in 2025. Pair it with generic client errors and detailed server logs without secrets.

**31. How do you manage secrets and rotate them?**
A secrets manager, injected at runtime; never in code, Git, images, bundles or logs; separate per environment and service; short-lived credentials (OIDC, cloud roles) where possible; secret scanning and push protection; and a rehearsed response: revoke, rotate, find what it touched, check logs.

**32. How do you isolate tenants in a multi-tenant app?**
Take the tenant from the authenticated session, enforce `tenant_id` in a repository layer, add database row-level security as a second layer, set per-tenant limits, and test isolation on every endpoint with two tenants.

**33. How do you prevent race conditions and business-logic abuse?**
Do the check and the update atomically (`UPDATE ... WHERE balance >= amount` and check rows affected, or transactions with locks), use unique constraints (one coupon use), recompute prices server-side, enforce a server-side state machine, and add idempotency keys.

**34. How do you harden a container and its runtime?**
Minimal base image pinned by digest, multi-stage build, non-root user, read-only filesystem and dropped capabilities, no secrets in the image, `npm ci --ignore-scripts`, image scanning, resource limits, and in Kubernetes network policies and no privileged pods.

---

## D. Design scenarios

**35. Design secure login for a SPA plus an API.**
Offer passkeys and/or OIDC with authorization code + PKCE through a maintained library or IdP. Keep the login in an HttpOnly, Secure, SameSite session cookie (or use a BFF so OAuth tokens never reach the browser), add CSRF protection, rate limiting, breached-password checks if passwords exist, regenerate the session at login, short sessions with revocation, and a hardened recovery flow. Test: login throttling, fixation, cross-user access.

**36. Design password reset.**
Same response whether or not the email exists; a random 128-bit+ token stored as a hash, single-use, expiring in minutes, sent only to the registered address; rate limits; after reset invalidate all sessions and notify the user; require re-auth for sensitive changes; make help-desk resets as strict as the web flow.

**37. Design authorization for a multi-tenant SaaS API.**
Identity and tenant from the session; a policy layer with deny-by-default; owner- and tenant-scoped queries; role checks for functions; strict input schemas and response DTOs; Postgres RLS as a second layer; per-tenant rate limits; authorization tests for every route; an API inventory so old endpoints don't linger.

**38. Design a file-sharing or upload feature.**
Authenticated, size-limited uploads; content checks; random names in object storage; signed, expiring download URLs; serve from a separate domain; per-object authorization on download; malware scanning for shared files; sandboxed previews; audit logs; quotas.

**39. Design a payment webhook handler.**
Raw-body HMAC verification with timestamp and constant-time compare; idempotency by event ID; process asynchronously; confirm state with the provider's API for critical transitions; secret in a manager with rotation; alert on signature failures.

**40. Design a "paste a URL to get a preview" feature.**
This is SSRF territory: allowlist or strictly validate scheme and resolved IP, pin the connection to the validated address, handle redirects explicitly, cap time and size, fetch from an isolated worker with restricted egress, never return raw bodies or error details, and sanitize anything rendered.

**41. How do you security-review a pull request or a new feature?**
Run the five questions: who is calling, are they allowed, what can they control, where does it go, what if it fails or repeats. Check new dependencies, secrets and permissions. Verify authorization tests exist, scanners pass, and for larger features do a short STRIDE pass.

**42. Design API keys for third-party developers.**
Generate long random keys, show them once, store only a hash, prefix them to identify the owner and allow leak scanning, scope each key narrowly, support rotation and expiry, rate-limit per key, log usage, and let users revoke instantly.

---

## E. Delivery, AI and incidents

**43. What is a software supply-chain attack and how do you defend against it?**
Compromising something you depend on. Recent examples: the Shai-Hulud npm worm (Sep and Nov 2025), the chalk/debug maintainer phish (Sep 2025), the tj-actions tag rewrite (Mar 2025), XZ Utils (2024). Defences: lockfiles and `npm ci`, a cooldown on new versions, blocking install scripts where possible, scanning, an SBOM, short-lived publish tokens and trusted publishing, SHA-pinned Actions, least-privilege CI.

**44. How would you harden a CI/CD pipeline?**
Pin third-party Actions to full commit SHAs, read-only default token permissions, never interpolate untrusted input into `run:` (use environment variables), avoid `pull_request_target` with untrusted code, no secrets for forks, OIDC to the cloud, branch protection and required reviews, and secret scanning.

**45. A secret was committed to Git. What do you do?**
Revoke or rotate it immediately (deleting the commit isn't enough), find what it could access and review provider logs, replace it with a narrower or short-lived credential, then fix the root cause: secret scanning, push protection, and a secrets manager.

**46. A critical CVE in a core dependency just dropped. What is your process?**
Determine exposure from the lockfile and SBOM, check whether it's exploited (CISA KEV) and internet-facing, patch or apply a mitigation, verify with tests, rotate secrets if exploitation is plausible, check logs, and communicate. Then shorten the time-to-patch for next time.

**47. What is prompt injection and how do you defend against it?**
The model can't separate instructions from data, so text it reads can steer it; indirect injection is the dangerous kind (EchoLeak, 2025). No complete fix, so contain it: the AI acts with the user's permissions, minimal tools that authorize inside, human approval for risky actions, output treated as untrusted, no secrets in prompts, and avoid combining private data, untrusted content and an outbound channel.

**48. How do you handle AI-generated code in your team?**
Review it like a stranger's PR: authorization, unsafe sinks, secrets, crypto, and invented or outdated packages. Run the same scanners and tests, don't paste secrets or customer data into unapproved tools, and keep humans accountable for what ships.

**49. How do you test for security?**
Authorization tests for every route, unit tests for validation and helpers (SSRF checker, path joiner), mass-assignment and rate-limit tests, plus SAST, SCA, secret scanning in CI and DAST on staging; headers and CSP checked in integration tests; ASVS Level 1 as the checklist.

**50. Tell me about a security issue you found or fixed. How do you stay current?**
Use your prepared war story: situation, what you did, outcome, what changed afterwards. For staying current, name real sources (OWASP lists, CISA advisories, the Verizon DBIR, framework security advisories, hands-on labs) and one recent thing you learned, such as React2Shell or the npm token changes.
