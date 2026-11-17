#!/usr/bin/env python3
"""Generate this book's own diagrams (SVG) into ../images.  Usage: python3 make_diagrams.py
Reused diagrams (SQL injection, XSS, CSRF, ...) are copied from the first book by hand and are not regenerated here."""
import os
from diagram_lib import *  # noqa: F401,F403  (S, colours, wrap, MONO, ...)
from diagram_lib import S, wrap, OUT, NAVY, TEAL, RED, GREEN, AMBER, INK, MUTE, GREY, WHITE, PINK, MINT, SKY, SAND, ORANGE, DARKRED, MONO, FONT

PURPLE = "#6b4fa0"


def bullets(s, x, y, items, width, size=11.5, color=INK, dot=MUTE, gap=8, mono=False):
    for it in items:
        lines = wrap(it, width, size, mono)
        s.text(x, y, "•", size, dot, "bold")
        s.text(x + 14, y, "\n".join(lines), size, color, font=MONO if mono else FONT, lh=1.28)
        y += len(lines) * size * 1.28 + gap
    return y


def trust_boundaries():
    s = S(860, 450, "Trust boundaries: the browser is outside your control", "Everything that crosses the line must be checked again on the server")
    s.rect(20, 75, 262, 265, PINK, RED, 12, dash=True); s.text(151, 98, "BROWSER (untrusted)", 13.5, RED, "bold", "middle")
    bullets(s, 36, 124, ["JavaScript checks and disabled buttons", "Hidden form fields and URL parameters", "localStorage and cookies it holds",
                         "The payload inside a JWT", "Request headers and uploaded files", "Any request, from any tool, not just your UI"], 232, 11.5, INK, RED)
    s.line(311, 75, 311, 340, AMBER, 2, True); s.text(311, 70, "TRUST BOUNDARY", 10.5, AMBER, "bold", "middle")
    s.rect(340, 75, 300, 265, MINT, GREEN, 12); s.text(490, 98, "YOUR BACKEND (trusted)", 13.5, GREEN, "bold", "middle")
    s.box(362, 125, 120, 54, "API handlers", WHITE, GREEN, INK, 12.5, "bold"); s.box(498, 125, 120, 54, "Auth + policy\nlayer", WHITE, GREEN, INK, 12, "bold")
    s.box(362, 235, 120, 54, "Database\n(least privilege)", WHITE, GREEN, INK, 12, "bold"); s.box(498, 235, 120, 54, "Secrets +\nconfig", WHITE, GREEN, INK, 12, "bold")
    s.arrow(284, 152, 360, 152, RED); s.text(322, 142, "hostile", 10.5, RED, "bold", "middle")
    s.arrow(422, 181, 422, 233, GREEN)
    s.rect(668, 75, 172, 265, SAND, AMBER, 12, dash=True); s.text(754, 98, "THIRD PARTIES", 13, AMBER, "bold", "middle")
    bullets(s, 682, 124, ["Payments", "Analytics and tag managers", "Identity provider", "CDN-hosted scripts", "SaaS integrations"], 140, 11.5, INK, AMBER)
    s.text(754, 296, "Partly trusted:\nlimit what they can reach", 11, MUTE, anchor="middle")
    s.arrow(642, 152, 666, 152, AMBER)
    s.rect(20, 360, 820, 70, SKY, TEAL, 10)
    s.ctext(430, 395, "Frontend validation is user experience. Backend validation is security. You need both, but only the second one counts against an attacker.", 13, INK, "bold", width=780)
    s.save("trust-boundaries")


def request_pipeline():
    s = S(900, 440, "The secure request pipeline (backend)", "Eight checks every request should pass, in this order")
    st = [("1  TLS + HSTS", "Stops sniffing and downgrade attacks."), ("2  LIMITS", "Rate limits, body and upload size caps. Stops brute force and resource abuse."),
          ("3  AUTHENTICATE", "Verify the session or token: signature, expiry, audience. Stops impersonation."), ("4  AUTHORIZE", "Is THIS user allowed THIS action on THIS object? Stops BOLA and BFLA."),
          ("5  VALIDATE", "Schema-check types, lengths and allowed fields. Stops injection and mass assignment."), ("6  DO THE WORK", "Parameterized queries; least-privilege database user. Stops SQL injection."),
          ("7  RESPOND", "Return only needed fields; encode output; generic errors. Stops data leaks."), ("8  LOG", "Record security events, never secrets. Makes attacks visible.")]
    for i, (t, b) in enumerate(st):
        x = 20 + (i % 4) * 220; y = 72 + (i // 4) * 170
        s.card(x, y, 205, 145, t, b, [NAVY, TEAL, TEAL, RED, TEAL, GREEN, GREEN, AMBER][i], hh=34, size=12)
        if i % 4 < 3:
            s.arrow(x + 208, y + 72, x + 217, y + 72, MUTE)
    s.path("M862,220 V232 H122 V240", MUTE)
    s.rect(20, 395, 860, 34, SAND, AMBER, 10)
    s.ctext(450, 412, "Cheap checks first. Authorization before any data access. Every layer assumes the one before it can fail.", 12, INK, "bold", width=830)
    s.save("request-pipeline")


def cors_preflight():
    s = S(860, 470, "CORS in one picture: the browser enforces it, not your server", "Preflight happens for non-simple requests (custom headers, JSON, PUT/DELETE)")
    s.lifelines([("app.example.com", 170, TEAL), ("api.example.com", 690, NAVY)], 75, 330)
    s.msg(140, 170, 690, "1  OPTIONS /orders (preflight)  Origin: https://app.example.com", NAVY)
    s.msg(185, 690, 170, "2  Allow-Origin: app.example.com, Allow-Methods, Allow-Headers", GREEN)
    s.msg(235, 170, 690, "3  The real request (cookies sent only if credentials are enabled)", NAVY)
    s.msg(280, 690, 170, "4  Response: the browser lets the page's JavaScript read it only if allowed", GREEN)
    s.box(20, 350, 405, 64, "CORS is enforced by the BROWSER. curl, Postman and an attacker's own server ignore it. It protects users' browsers; it is not authentication or access control.", SKY, TEAL, INK, 11.5)
    s.box(435, 350, 405, 64, "Never reflect any Origin back while allowing credentials. Browsers refuse the * wildcard together with cookies, so people \"fix\" it by reflecting. That is the bug.", PINK, RED, INK, 11.5)
    s.rect(20, 425, 820, 36, SAND, AMBER, 10)
    s.ctext(430, 443, "A request can reach your server even when CORS blocks the response. Simple form POSTs skip the preflight entirely.", 12, INK, "bold", width=800)
    s.save("cors-preflight")


def spa_token_storage():
    s = S(900, 450, "Where should a single-page app keep its login?", "Four options, from weakest to strongest")
    cards = [("localStorage /\nsessionStorage", RED, "Readable by any script on the page, so one XSS flaw hands over the token to be used anywhere.", "XSS can steal it: YES", "Avoid for real tokens"),
             ("Short-lived token in memory + HttpOnly refresh cookie", AMBER, "The access token lives only in JS memory. The refresh token sits in a cookie scripts cannot read. Rotate it.", "XSS can steal it: NO (can still use it while the page is open)", "A good SPA default"),
             ("HttpOnly session cookie (same site)", GREEN, "A server-side session. The browser sends the cookie automatically. Needs SameSite and CSRF defences.", "XSS can steal it: NO (can still act as the user)", "Simple and robust"),
             ("BFF: tokens never reach the browser", TEAL, "A small backend holds the OAuth tokens. The browser has only a session cookie to the BFF.", "XSS can steal tokens: there are none to steal", "Best for high-value apps")]
    for i, (t, c, b, x_, v) in enumerate(cards):
        x = 20 + i * 220
        s.card(x, 75, 205, 270, t, b, c, hh=54, size=11.5)
        s.rect(x + 8, 245, 189, 52, PINK if i == 0 else MINT, RED if i == 0 else GREEN, 6); s.text(x + 16, 262, x_, 10.5, INK, "bold", width=173, lh=1.25)
        s.rect(x + 8, 305, 189, 32, c, c, 6); s.ctext(x + 102, 321, v, 11.5, WHITE, "bold", width=180)
    s.rect(20, 362, 860, 62, SAND, AMBER, 10)
    s.ctext(450, 393, "No storage choice is safe if XSS exists: an attacker script can still USE the session while the page is open. Fix XSS first, then choose storage so that a foothold is worth as little as possible.", 12, INK, "bold", width=830)
    s.save("spa-token-storage")


def bff_architecture():
    s = S(860, 420, "The BFF pattern: keep OAuth tokens out of the browser", "BFF = Backend For Frontend, a small server that fronts your single-page app")
    s.box(20, 140, 170, 100, "Browser SPA\nholds only a session cookie\n(HttpOnly, Secure, SameSite)", SKY, TEAL, INK, 12)
    s.box(290, 120, 230, 140, "BFF (your server)\nholds access + refresh tokens\nchecks CSRF and Origin\nattaches the token to API calls", MINT, GREEN, INK, 12, "bold")
    s.box(630, 85, 210, 70, "Your APIs\n(resource servers)", WHITE, NAVY, INK, 12.5, "bold")
    s.box(630, 225, 210, 70, "Identity provider\n(OAuth / OIDC)", WHITE, AMBER, INK, 12.5, "bold")
    s.arrow(192, 190, 288, 190, TEAL); s.text(240, 178, "cookie", 11, anchor="middle")
    s.arrow(522, 120, 628, 120, GREEN); s.text(575, 108, "access token", 11, anchor="middle")
    s.arrow(522, 250, 628, 250, AMBER); s.text(575, 238, "code + refresh", 11, anchor="middle")
    s.rect(20, 320, 820, 70, SAND, AMBER, 10)
    s.ctext(430, 355, "XSS cannot steal a token the browser never had. You pay for it with one extra server to run, but you remove the single most valuable thing an injected script could take.", 12.5, INK, "bold", width=790)
    s.save("bff-architecture")


def oauth_pkce():
    s = S(860, 500, "OAuth authorization code flow with PKCE", "The safe way for single-page apps, mobile apps and 'Sign in with...'")
    s.lifelines([("Your app", 130, TEAL), ("Browser", 430, MUTE), ("Auth server", 730, NAVY)], 72, 400)
    s.msg(135, 130, 430, "1  app makes code_verifier + code_challenge", TEAL)
    s.msg(175, 430, 730, "2  /authorize?client_id&code_challenge&state", NAVY)
    s.box(480, 192, 365, 36, "3  user signs in (ideally with a passkey) and consents", SAND, AMBER, INK, 12)
    s.msg(262, 730, 430, "4  redirect back with ?code=...&state=...", NAVY)
    s.msg(302, 430, 130, "5  app receives the code", TEAL)
    s.msg(342, 130, 730, "6  POST /token: code + code_verifier", GREEN)
    s.msg(382, 730, 130, "7  access token (+ refresh token)", GREEN)
    s.box(20, 412, 405, 70, "A stolen code is useless without the code_verifier that only your app knows. That is what PKCE adds.", MINT, GREEN, INK, 12)
    s.box(435, 412, 405, 70, "Also: check the state value, register exact redirect URIs, keep scopes minimal, and keep tokens short-lived.", SKY, TEAL, INK, 12)
    s.save("oauth-pkce")


def passkey_flow():
    s = S(860, 510, "Passkey (WebAuthn) login, step by step")
    s.lifelines([("Browser + device", 170, TEAL), ("Your server", 690, NAVY)], 48, 395)
    s.msg(135, 690, 170, "1  challenge (random) + your domain", NAVY)
    s.box(20, 160, 340, 66, "2  The device checks the domain, asks for fingerprint / face / PIN, and signs the challenge with the PRIVATE key", SAND, AMBER, INK, 11.5)
    s.msg(275, 170, 690, "3  signed response (credential id + signature)", GREEN)
    s.box(430, 295, 410, 62, "4  Server verifies with the stored PUBLIC key, and checks the challenge, the origin and the signature counter", MINT, GREEN, INK, 11.5)
    s.msg(385, 690, 170, "5  session created (rotate the session id)", NAVY)
    s.box(20, 415, 405, 80, "A look-alike domain gets nothing usable: the key is scoped to the real domain. That is why passkeys resist phishing.", MINT, GREEN, INK, 12)
    s.box(435, 415, 405, 80, "Registration has the same shape, but the server stores only the public key. Use a maintained library (for example SimpleWebAuthn) and plan account recovery.", SKY, TEAL, INK, 12)
    s.save("passkey-flow")


def csp_effect():
    s = S(860, 410, "How a Content-Security-Policy limits an injected script", "The second layer: it helps when output encoding has failed somewhere")
    s.box(20, 85, 270, 190, "", WHITE, NAVY)
    s.text(34, 108, "Server response", 12, NAVY, "bold")
    s.text(34, 126, "Content-Security-Policy:\n  script-src 'nonce-R4nd0m'\n  object-src 'none'\n  frame-ancestors 'none'", 10.5, INK, font=MONO, lh=1.35)
    s.text(34, 205, "<script nonce=\"R4nd0m\">app()</script>\n<script>steal()</script>   <- injected\n<img src=x onerror=steal()>  <- injected", 9.8, RED, font=MONO, lh=1.4)
    s.box(345, 150, 150, 74, "Browser checks every script against the policy", SKY, TEAL, INK, 12, "bold")
    s.arrow(292, 187, 343, 187, MUTE)
    s.box(560, 85, 280, 54, "ALLOWED: has the right nonce (your own app script)", MINT, GREEN, INK, 11.5, "bold")
    s.box(560, 160, 280, 54, "BLOCKED: inline script with no nonce", PINK, RED, INK, 11.5, "bold")
    s.box(560, 235, 280, 54, "BLOCKED: inline event handler (script-src-attr)", PINK, RED, INK, 11.5, "bold")
    s.arrow(497, 175, 558, 112, GREEN); s.arrow(497, 187, 558, 187, RED); s.arrow(497, 199, 558, 262, RED)
    s.rect(20, 315, 820, 70, SAND, AMBER, 10)
    s.ctext(430, 350, "CSP reduces the blast radius; it does not replace encoding. Roll it out in report-only mode first, use nonces with 'strict-dynamic' instead of long host allowlists, and avoid 'unsafe-inline' for scripts.", 12, INK, "bold", width=790)
    s.save("csp-effect")


def fe_be_split():
    s = S(890, 480, "Who owns what: frontend, backend and shared security work", "Security fails in the gaps. Know your side, and the seam between the sides.")
    cols = [("FRONTEND OWNS", TEAL, SKY, ["Safe rendering: JSX escaping, no raw innerHTML", "CSP and Trusted Types rollout", "Where tokens live (never plain localStorage)", "No secrets in the bundle (NEXT_PUBLIC_, VITE_)",
                                       "Third-party scripts: fewer, with SRI", "Safe URLs, redirects and postMessage origin checks", "Security UX: passkeys, no leaky error text"]),
            ("BACKEND OWNS", NAVY, GREY, ["Authentication and per-object authorization", "Schema validation of every input", "Parameterized queries, least-privilege database", "Rate limits, body and upload limits",
                                         "SSRF-safe outbound requests and file handling", "Secrets management; logging without secrets", "Generic errors and failing closed"]),
            ("BOTH OWN", GREEN, MINT, ["HTTPS, HSTS and cookie flags (server sets, browser enforces)", "CORS and CSRF design", "Dependencies, lockfiles and CI/CD hardening", "Threat-modelling each feature together",
                                       "Reviewing AI-generated code", "Incident response: rotate, revoke, patch"])]
    for i, (h, c, f, items) in enumerate(cols):
        x = 20 + i * 285
        s.rect(x, 75, 270, 385, f, c, 12)
        s.p.append(f'<path d="M{x},109 L{x},87 Q{x},75 {x+12},75 L{x+258},75 Q{x+270},75 {x+270},87 L{x+270},109 Z" fill="{c}"/>')
        s.ctext(x + 135, 92, h, 13.5, WHITE, "bold")
        bullets(s, x + 14, 138, items, 232, 11.5, INK, c, 9)
    s.save("fe-be-split")


def ci_gates():
    s = S(900, 440, "A delivery pipeline with security gates", "Each gate catches a different kind of mistake before it reaches production")
    row1 = [("Pull request", "Review + branch protection"), ("Secret scan", "Block keys before merge"), ("Install", "npm ci / lockfile / no install scripts"), ("Dependency scan", "Known-vulnerable packages (SCA)")]
    row2 = [("Static analysis", "Code patterns (SAST)"), ("Tests", "Include authorization tests"), ("Build + image scan", "Minimal, non-root image"), ("Sign + deploy", "Provenance, then monitor")]
    for r, row in enumerate((row1, row2)):
        for i, (t, b) in enumerate(row):
            x = 20 + i * 220; y = 72 + r * 92
            s.rect(x, y, 205, 76, [SKY, MINT][r], [TEAL, GREEN][r], 10)
            s.text(x + 12, y + 24, f"{r*4+i+1}  {t}", 12.5, NAVY, "bold"); s.text(x + 12, y + 46, b, 11, INK, width=182, lh=1.25)
            if i < 3:
                s.arrow(x + 207, y + 38, x + 218, y + 38, MUTE)
    s.path("M862,148 V160 H122 V164", MUTE)
    s.rect(20, 262, 860, 160, SAND, AMBER, 12); s.text(36, 286, "Harden the pipeline itself (it holds your most powerful secrets)", 13, AMBER, "bold")
    bullets(s, 36, 312, ["Pin third-party Actions to a full commit SHA (the 2025 tj-actions compromise rewrote version tags)", "Set workflow permissions to read-only by default", "Give no secrets to pull requests from forks"], 390, 11.5, INK, AMBER)
    bullets(s, 450, 312, ["Use OIDC to your cloud instead of long-lived keys", "Protected branches, required reviews, signed commits where you can", "Short-lived registry tokens and trusted publishing"], 400, 11.5, INK, AMBER)
    s.save("ci-security-gates")


def webhook_hmac():
    s = S(860, 480, "Webhook verification: trust the signature, not the URL", "Anyone who finds your webhook URL can send a fake 'payment succeeded' unless you check")
    s.lifelines([("Provider", 170, TEAL), ("Your server", 690, NAVY)], 75, 345)
    s.box(20, 130, 345, 48, "signature = HMAC-SHA256(secret, timestamp + \".\" + rawBody)", SKY, TEAL, INK, 11.5, "bold", font=MONO)
    s.msg(215, 170, 690, "POST /webhook  body + X-Timestamp + X-Signature", NAVY)
    s.box(430, 240, 410, 78, "1  Use the RAW body (not re-serialized JSON)\n2  Recompute the HMAC\n3  Compare in constant time\n4  Reject old timestamps (replay)", MINT, GREEN, INK, 11.5)
    s.msg(345, 690, 170, "200 if valid, 401 if not (and do not run the handler)", GREEN)
    s.box(20, 372, 405, 90, "Also: make the handler idempotent (providers retry, so the same event can arrive twice) and acknowledge quickly; do slow work in a queue.", SAND, AMBER, INK, 12)
    s.box(435, 372, 405, 90, "Keep the signing secret in your secrets manager and rotate it. If you cannot verify a signature, fetch the event from the provider's API instead of trusting the payload.", SKY, TEAL, INK, 12)
    s.save("webhook-hmac")


def upload_flow():
    s = S(860, 420, "Handling file uploads safely", "Five steps, each stopping a different attack")
    st = [("1  LIMIT + AUTH", "Require login; cap file size and count.", "Anonymous abuse, disk filling"), ("2  CHECK CONTENT", "Allowlist types; check the real content (magic bytes), not just name or Content-Type.", "Disguised scripts"),
          ("3  RENAME", "Store under a random ID. Never use the user's filename or path.", "Path traversal, overwriting files"), ("4  STORE SAFELY", "Object storage or a folder outside the web root, never executable.", "Direct execution"),
          ("5  SERVE SAFELY", "Separate domain, Content-Disposition: attachment, nosniff.", "Stored XSS through uploads")]
    for i, (h, do, stops) in enumerate(st):
        x = 20 + i * 167
        s.box(x, 75, 152, 46, h, NAVY, NAVY, WHITE, 12, "bold")
        if i < 4:
            s.arrow(x + 154, 98, x + 165, 98, MUTE)
        s.cell(x, 131, 152, 120, "DO THIS", do, SKY, TEAL, TEAL)
        s.cell(x, 259, 152, 70, "STOPS", stops, MINT, GREEN, GREEN)
    s.rect(20, 345, 820, 56, SAND, AMBER, 10)
    s.ctext(430, 373, "Treat SVG and PDF as active content (they can contain script). Process images in a sandbox. Scan files that other users will download.", 12, INK, "bold", width=790)
    s.save("upload-flow")


def study_tracks():
    s = S(880, 400, "Your four weeks: shared core, then both tracks, then delivery", "About 10 hours a week, evenings plus the weekend")
    s.card(20, 80, 200, 250, "WEEK 1\nShared core", "• Threat model for developers\n• Browser and HTTP security\n• Authentication and sessions", NAVY, hh=50, size=12)
    s.card(235, 80, 200, 250, "WEEK 2\nAuthZ and input", "• Authorization and API design\n• Injection and input handling\n• Labs 1, 3, 4, 5", TEAL, hh=50, size=12)
    s.card(450, 80, 200, 115, "WEEK 3a  Frontend", "• XSS, CSP, tokens\n• Next.js / RSC risks", RED, hh=34, size=12)
    s.card(450, 215, 200, 115, "WEEK 3b  Backend", "• SSRF, uploads, webhooks\n• Secrets, errors, containers", AMBER, hh=34, size=12)
    s.card(665, 80, 195, 250, "WEEK 4\nDelivery + interview", "• Supply chain and CI/CD\n• AI features\n• Code review drill\n• 50-question mock", GREEN, hh=50, size=12)
    for x in (222, 437, 652):
        s.arrow(x, 205, x + 11, 205, MUTE)
    s.rect(20, 345, 840, 40, SAND, AMBER, 10)
    s.ctext(440, 365, "Frontend engineer? Do 3a deeply and skim 3b. Backend engineer? The reverse. Full-stack? Do both and skip nothing in Week 2.", 12.5, INK, "bold", width=810)
    s.save("study-tracks")


def nextjs_trust():
    s = S(880, 510, "Where Next.js and React Server Components code runs, and what to distrust", "The same lessons apply to Remix, React Router, Nuxt and SvelteKit: server code reachable over HTTP is an API")
    boxes = [("Browser\n(client components)", SKY, TEAL), ("CDN / edge\nmiddleware", GREY, MUTE), ("Server\n(server components, route handlers, server actions)", MINT, GREEN), ("Database +\ninternal services", WHITE, NAVY)]
    xs = [20, 235, 450, 665]
    for (t, f, c), x in zip(boxes, xs):
        s.box(x, 82, 190, 84, t, f, c, INK, 12, "bold")
    for x in (212, 427, 642):
        s.arrow(x, 124, x + 21, 124, MUTE)
    notes = [("Everything here is public: client code, source maps, and any NEXT_PUBLIC_* / VITE_* variable. Never put secrets here.", PINK, RED),
             ("Middleware is a convenience, not the only gate. In 2025 a single request header could skip it (CVE-2025-29927). Authorize again where data is read.", PINK, RED),
             ("Server Actions and route handlers are public HTTP endpoints. Authenticate, authorize and validate INSIDE each one. Request parsing is attack surface: React2Shell (CVE-2025-55182, CVSS 10) was remote code execution.", PINK, RED),
             ("Least-privilege credentials, parameterized queries, and no direct reachability from the internet.", MINT, GREEN)]
    for (t, f, c), x in zip(notes, xs):
        s.rect(x, 190, 190, 185, f, c, 10); s.text(x + 10, 210, t, 11, INK, width=170, lh=1.3)
    s.rect(20, 395, 840, 100, SAND, AMBER, 12)
    s.text(34, 418, "Developer habits that follow", 13, AMBER, "bold")
    bullets(s, 34, 440, ["Keep React, Next.js and other framework packages patched; critical framework bugs are mass-exploited within days.", "Treat each server function like a REST endpoint: same checks, same tests."], 800, 11.5, INK, AMBER, 6)
    s.save("nextjs-trust-model")


def xss_sinks():
    s = S(880, 410, "XSS sinks every frontend developer should recognise", "Frameworks escape by default. These are the doors that switch it off.")
    s.rect(20, 75, 300, 270, MINT, GREEN, 12); s.text(170, 98, "SAFE BY DEFAULT", 13.5, GREEN, "bold", "middle")
    bullets(s, 36, 124, ["React / JSX:  {value}", "Vue:  {{ value }}", "Angular:  {{ value }} interpolation", "DOM:  element.textContent = value", "Template engines with autoescape on"], 270, 12, INK, GREEN, 10, mono=True)
    s.rect(345, 75, 515, 270, PINK, RED, 12); s.text(602, 98, "DANGEROUS SINKS (review every use)", 13.5, RED, "bold", "middle")
    bullets(s, 361, 124, ["dangerouslySetInnerHTML  (React)", "innerHTML, outerHTML, insertAdjacentHTML", "v-html (Vue),  [innerHTML] (Angular)", "document.write(...)", "eval(...), new Function(...), setTimeout(\"string\")",
                          "href / src set from user input  (javascript: URLs)", "location = userInput, window.open(userInput)  (open redirect)", "onclick=... attributes built from data", "message handlers with no event.origin check"], 480, 11.5, INK, RED, 8, mono=True)
    s.rect(20, 360, 840, 40, SAND, AMBER, 10)
    s.ctext(440, 380, "If you must render HTML, sanitize it with DOMPurify. If you accept URLs, allowlist http, https and mailto. If you listen to postMessage, check the origin.", 12, INK, "bold", width=810)
    s.save("xss-sinks")


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for f in (trust_boundaries, request_pipeline, cors_preflight, spa_token_storage, bff_architecture, oauth_pkce, passkey_flow, csp_effect,
              fe_be_split, ci_gates, webhook_hmac, upload_flow, study_tracks, nextjs_trust, xss_sinks):
        f()
    print("wrote", len([n for n in os.listdir(OUT) if n.endswith(".svg")]), "svg files in", os.path.abspath(OUT))
