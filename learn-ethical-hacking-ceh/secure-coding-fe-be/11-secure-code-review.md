# Chapter 11: Secure Code Review and Security Testing

> **Goal.** After this chapter you can: review a pull request with a security checklist; spot the 15 most common vulnerabilities in short code snippets; write the tests that prove authorization and validation work; and use ASVS as a verification checklist.
>
> **Who:** frontend and backend. **Time:** about 2 hours. **Lab:** [Lab 11](13-labs.md) (the timed review drill).

Reading a diff and saying "this is wrong because..." is the skill interviewers test most directly: they hand you a snippet and ask what is wrong.

---

## 1. A 5-question review checklist

For every change that touches a request, a query, a render or a dependency, ask:

1. **Who is calling?** Is the caller authenticated, and is the identity taken from the session or token (not the request)?
2. **Are they allowed?** Is access checked **per object and per action**, on the server?
3. **What can they control?** Every input (body, query, headers, files, URLs, model output): is it validated against a strict schema?
4. **Where does it go?** Into a query, shell, file path, URL fetch, HTML, redirect or log: is it parameterized, encoded or allowlisted for that destination?
5. **What if it fails or repeats?** Does it fail closed, return a generic error, respect limits, and behave under concurrency?

Add: **Does this add a dependency, a secret, a permission or a third-party script?**

---

## 2. Spot the vulnerability (15 snippets)

Cover the answers, spend about 2 minutes on each, then check. Aim for 12 of 15. Each snippet has *one main* flaw (some have extras).

**Snippet 1**
```ts
app.get("/api/invoices/:id", requireLogin, async (req, res) => {
  res.json(await db.invoice.findUnique({ where: { id: req.params.id } }));
});
```

**Snippet 2**
```tsx
function Comment({ html }: { html: string }) {
  return <div dangerouslySetInnerHTML={{ __html: html }} />;
}
```

**Snippet 3**
```python
cur.execute(f"SELECT * FROM users WHERE email = '{email}' AND active = 1")
```

**Snippet 4**
```ts
const claims = jwt.decode(token) as any;
if (claims?.role === "admin") return next();
```

**Snippet 5**
```ts
app.use(cors({ origin: true, credentials: true }));
```

**Snippet 6**
```ts
const user = await users.findOne({ email: req.body.email, password: req.body.password });
```

**Snippet 7**
```ts
exec(`ffmpeg -i ${req.body.filename} -vn out.mp3`);
```

**Snippet 8**
```ts
app.get("/login/done", (req, res) => res.redirect(req.query.next as string));
```

**Snippet 9**
```ts
app.post("/payments-webhook", express.json(), (req, res) => {
  if (req.body.type === "payment.succeeded") markOrderPaid(req.body.data.orderId);
  res.sendStatus(200);
});
```

**Snippet 10**
```ts
await db.user.update({ where: { id: req.user.id }, data: req.body });
```

**Snippet 11**
```yaml
on: pull_request_target
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with: { ref: "${{ github.event.pull_request.head.sha }}" }
      - run: npm ci && npm test
        env: { DEPLOY_KEY: "${{ secrets.DEPLOY_KEY }}" }
```

**Snippet 12**
```ts
"use server";
export async function deleteUser(id: string) {
  await db.user.delete({ where: { id } });
}
```

**Snippet 13**
```ts
app.get("/preview", async (req, res) => {
  const r = await fetch(req.query.url as string);
  res.send(await r.text());
});
```

**Snippet 14**
```ts
const token = Math.random().toString(36).slice(2);
await db.passwordReset.create({ data: { userId: user.id, token } });
await sendMail(user.email, `https://app.example.com/reset?token=${token}`);
```

**Snippet 15**
```ts
app.post("/upload", upload.single("file"), async (req, res) => {
  await fs.writeFile(path.join("/var/www/uploads", req.file.originalname), req.file.buffer);
  res.sendStatus(201);
});
```

---

<div style="break-before: page"></div>

### Answers

1. **BOLA/IDOR.** Any logged-in user can read any invoice. Scope the query to the owner or tenant: `findFirst({ where: { id, ownerId: req.user.id } })`, return 404 otherwise. *Test:* user A requests user B's invoice and expects 404.
2. **Stored XSS.** User-supplied HTML rendered raw. Render text (`<p>{text}</p>`), or sanitize with DOMPurify, and add a CSP.
3. **SQL injection.** String-built query. Use placeholders: `cur.execute("... WHERE email = %s AND active = 1", (email,))` (the placeholder style depends on the driver).
4. **Trusting an unverified token.** `decode` does **not** check the signature, so anyone can forge `role: admin`. Use `verify` with a pinned algorithm, issuer and audience (Lab 3).
5. **Over-permissive CORS.** `origin: true` reflects *any* origin and `credentials: true` lets that site read authenticated responses. Use an exact allowlist.
6. **NoSQL operator injection** (and plaintext passwords). An object like `{"$ne": null}` as the password matches anything; validate types with a schema, and compare a *password hash* with a verify function, never the raw password in the query.
7. **Command injection.** The filename goes through a shell. Use `execFile("ffmpeg", ["-i", safeName, ...])`, validate the file against an allowlist, and ideally use a library or stored file ID.
8. **Open redirect.** An attacker crafts a login link that bounces users to a phishing site. Allowlist internal paths (`/^\/[\w\/-]*$/`) or a fixed set of destinations.
9. **Unverified webhook.** Anyone who finds the URL can fake "payment succeeded". Verify an HMAC signature on the **raw** body with a constant-time comparison and a timestamp window (Lab 4); make the handler idempotent.
10. **Mass assignment.** The client can send `{"isAdmin": true}`. Validate with a strict schema listing only changeable fields.
11. **Dangerous workflow.** `pull_request_target` runs with secrets and write access, and this job **checks out and runs the untrusted PR code** with `DEPLOY_KEY` exposed. Use `pull_request` (no secrets) for untrusted code, never mix; also pin `checkout` to a full SHA and set `permissions: contents: read`.
12. **Unauthenticated, unauthorized, unvalidated server action.** Server Actions are public HTTP endpoints: anyone can call this and delete any user. Authenticate, authorize (is the caller allowed to delete *this* user?), and validate the input inside the function.
13. **SSRF**, and it **returns the raw response**. The server will fetch internal addresses such as the cloud metadata service. Allowlist hosts, validate the resolved IP (Lab 7), restrict redirects, add timeouts and size caps, and don't return raw bodies.
14. **Predictable, plaintext, non-expiring reset token.** `Math.random()` is not cryptographically secure. Use `crypto.randomBytes(32)`, store only a **hash**, make it single-use with a short expiry, and invalidate sessions after reset.
15. **Path traversal and unsafe upload.** `originalname` is attacker-controlled (`../../x.js`), and files go into a web-served folder. Use a random server-generated name, check the real content type, limit size, and store outside the web root or in object storage (Chapter 8).

**Score:** 13-15 excellent; 10-12 solid; below 10, re-read Chapters 4-8 and retry in two days.

---

## 3. Security tests worth writing

You can't review your way to safety; **tests keep fixes fixed.**

**Authorization tests** are the highest-value security tests. For every resource route:

```ts
describe("GET /orders/:id", () => {
  it("requires authentication", async () => {
    expect((await api.get(`/orders/${aliceOrder.id}`)).status).toBe(401);
  });
  it("returns 404 for another user's order (no BOLA)", async () => {
    const res = await api.get(`/orders/${bobOrder.id}`).set("Cookie", aliceSession);
    expect(res.status).toBe(404);
  });
  it("lets the owner read it", async () => {
    expect((await api.get(`/orders/${aliceOrder.id}`).set("Cookie", aliceSession)).status).toBe(200);
  });
});
```

**Other tests and tools:**

| Layer | What | Examples |
| --- | --- | --- |
| **Unit tests** | Validation and security helpers: safe-URL checker, path joiner, permission policy, schema rejects extra fields | The test table in Lab 7 |
| **Mass-assignment tests** | PATCH with `isAdmin: true` is ignored or rejected | Lab 1 |
| **SAST** (static analysis) | Finds dangerous patterns in source | Semgrep, CodeQL |
| **SCA / secret scanning** | Vulnerable dependencies; leaked keys | `npm audit`, `osv-scanner`, `gitleaks` |
| **DAST** | Probes the running app | OWASP ZAP |
| **Headers and CSP** | Assert expected headers in an integration test; use report-only first | Lab 2 |
| **Rate-limit tests** | The Nth request returns 429 | Lab 6 |

---

## 4. ASVS: a ready-made checklist

The **OWASP Application Security Verification Standard (ASVS)** is a catalogue of testable security requirements for web apps and APIs. **ASVS 5.0** was released in **May 2025**, reorganized into roughly 17 chapters (secondary sources count about 350 requirements) with new chapters on topics such as tokens and OAuth, and a lower-barrier **Level 1**.

**How to use it:** don't read it cover to cover. Pick **Level 1** as your baseline for any production app, turn the chapters that match your stack (authentication, sessions, access control, validation, API, configuration) into your pull-request checklist, and treat "Level 2" as the target for apps handling sensitive data. In an interview, saying *"I'd use ASVS Level 1 as our baseline checklist and automate what we can in CI"* shows maturity.

---

## Check yourself

1. List the five review questions.
2. Which single test gives the most security value per line?
3. What's wrong with `jwt.decode(token)` used for access control?
4. Why is `pull_request_target` plus a checkout of the PR head dangerous?
5. Why are Server Actions in "needs review" territory in any code review?
6. What is ASVS and how would you use Level 1?

**Answers** *(cover this until you have tried)*

1. Who is calling? Are they allowed (per object and action)? What can they control (validated)? Where does it go (parameterized/encoded/allowlisted)? What if it fails or repeats (fail closed, limits, concurrency)?
2. An authorization test: log in as user A and assert user B's resource returns 404 (and that unauthenticated access returns 401).
3. `decode` doesn't verify the signature, so attackers can forge any claim. Use `verify` with a pinned algorithm, issuer and audience.
4. That workflow runs with secrets and write permissions, and checking out the PR head runs attacker-controlled code with them.
5. They are public HTTP endpoints that anyone can call directly; each must authenticate, authorize and validate on its own.
6. OWASP's catalogue of verification requirements; use Level 1 as the baseline checklist for production apps, and automate what you can in CI.

---

## Summary

- Review with five questions: who, allowed, controlled, destination, failure.
- The 15 classics: BOLA, stored XSS, SQLi, `decode`-as-auth, reflective CORS, NoSQL operators, command injection, open redirect, unverified webhook, mass assignment, `pull_request_target`, unprotected server action, SSRF, weak reset token, upload path traversal.
- Write authorization tests for every resource route; add unit tests for security helpers; run SAST, SCA, secret scanning and DAST.
- ASVS 5.0 (May 2025): use Level 1 as your baseline checklist.
