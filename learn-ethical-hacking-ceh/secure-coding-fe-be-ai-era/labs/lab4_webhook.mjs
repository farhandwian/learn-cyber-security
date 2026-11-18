// Lab 4: verifying webhook signatures (HMAC + timestamp + constant-time compare).   Run: node lab4_webhook.mjs
import express from "express";
import crypto from "node:crypto";

const SECRET = "whsec_demo_only";

// The provider signs "timestamp.rawBody" with a shared secret.
export const sign = (rawBody, ts, secret = SECRET) =>
  crypto.createHmac("sha256", secret).update(`${ts}.${rawBody}`).digest("hex");

export function verify(rawBody, ts, signatureHex, { now = Date.now() / 1000, toleranceSeconds = 300 } = {}) {
  if (!Number.isFinite(ts) || Math.abs(now - ts) > toleranceSeconds) return false; // stops replay of old requests
  const expected = Buffer.from(sign(rawBody, ts), "hex");
  const given = Buffer.from(signatureHex ?? "", "hex");
  // timingSafeEqual throws on different lengths, so compare lengths first.
  return given.length === expected.length && crypto.timingSafeEqual(given, expected);
}

export function makeApp() {
  const app = express();
  // IMPORTANT: use the RAW bytes. If express.json() parses first, re-serializing changes the bytes and the signature breaks.
  app.post("/webhook", express.raw({ type: "application/json" }), (req, res) => {
    const ok = verify(req.body.toString("utf8"), Number(req.header("x-timestamp")), req.header("x-signature"));
    if (!ok) return res.status(401).json({ error: "bad signature" });
    res.json({ received: true });
  });
  return app;
}

if (import.meta.url === `file://${process.argv[1]}`) {
  const server = makeApp().listen(0);
  const url = `http://127.0.0.1:${server.address().port}/webhook`;
  const send = (body, ts, sig) =>
    fetch(url, { method: "POST", headers: { "content-type": "application/json", "x-timestamp": String(ts), "x-signature": sig ?? "" }, body });

  const body = JSON.stringify({ event: "payment.succeeded", amount: 100 });
  const now = Math.floor(Date.now() / 1000);
  const old = now - 3600;

  const cases = {
    "valid request is accepted": [await send(body, now, sign(body, now)), 200],
    "tampered body is rejected": [await send(body.replace("100", "1"), now, sign(body, now)), 401],
    "replayed (1 hour old) request is rejected": [await send(body, old, sign(body, old)), 401],
    "missing signature is rejected": [await send(body, now, ""), 401],
    "signature made with the wrong secret is rejected": [await send(body, now, sign(body, now, "other-secret")), 401],
  };
  server.close();

  let ok = true;
  for (const [name, [res, expected]] of Object.entries(cases)) {
    const pass = res.status === expected;
    ok &&= pass;
    console.log(`${pass ? "PASS" : "FAIL"}  ${name} (status ${res.status})`);
  }
  console.log(ok ? "\nPASS: signature, freshness and constant-time comparison all enforced." : "\nFAIL");
  process.exit(ok ? 0 : 1);
}
