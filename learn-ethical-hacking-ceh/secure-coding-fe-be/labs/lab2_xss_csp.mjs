// Lab 2: reflected XSS and a nonce-based Content-Security-Policy.   Run: node lab2_xss_csp.mjs
import express from "express";
import helmet from "helmet";
import crypto from "node:crypto";

const escapeHtml = (s) =>
  String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c]);

export function makeApp({ safe }) {
  const app = express();

  if (safe) {
    // A fresh nonce per response. Only <script nonce="..."> blocks with this value may run.
    app.use((req, res, next) => {
      res.locals.nonce = crypto.randomBytes(16).toString("base64");
      next();
    });
    app.use((req, res, next) =>
      helmet({
        contentSecurityPolicy: {
          directives: {
            defaultSrc: ["'self'"],
            scriptSrc: ["'self'", `'nonce-${res.locals.nonce}'`],
            objectSrc: ["'none'"],
            baseUri: ["'self'"],
            frameAncestors: ["'none'"], // also stops clickjacking
          },
        },
      })(req, res, next),
    );
  }

  app.get("/search", (req, res) => {
    const q = String(req.query.q ?? "");
    const shown = safe ? escapeHtml(q) : q; // FIX #1: encode output for the HTML context
    res
      .type("html")
      .send(`<h1>Results for ${shown}</h1><script nonce="${res.locals.nonce ?? ""}">/* the app's own script */</script>`);
  });

  return app;
}

async function probe(safe) {
  const server = makeApp({ safe }).listen(0);
  const payload = `<img src=x onerror=alert(1)>`;
  const res = await fetch(`http://127.0.0.1:${server.address().port}/search?q=${encodeURIComponent(payload)}`);
  const body = await res.text();
  const csp = res.headers.get("content-security-policy");
  server.close();
  return { rawPayloadInPage: body.includes(payload), encoded: body.includes("&lt;img"), csp };
}

if (import.meta.url === `file://${process.argv[1]}`) {
  const vuln = await probe(false);
  const fixed = await probe(true);
  console.log("VULNERABLE: payload reflected as live HTML:", vuln.rawPayloadInPage, "| CSP header:", vuln.csp ?? "none");
  console.log("FIXED     : payload reflected as live HTML:", fixed.rawPayloadInPage, "| encoded as text:", fixed.encoded);
  console.log("FIXED CSP : ", fixed.csp);
  const ok =
    vuln.rawPayloadInPage && !vuln.csp &&
    !fixed.rawPayloadInPage && fixed.encoded &&
    /script-src[^;]*'nonce-/.test(fixed.csp) && /frame-ancestors 'none'/.test(fixed.csp);
  console.log(ok ? "\nPASS: encoding removes the hole; CSP is the second layer." : "\nFAIL: unexpected result");
  process.exit(ok ? 0 : 1);
}
