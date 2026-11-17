// Lab 6: rate limiting a login route and capping request body size.   Run: node lab6_ratelimit.mjs
import express from "express";
import { rateLimit } from "express-rate-limit";

export function makeApp() {
  const app = express();
  // Behind a reverse proxy/CDN, set this correctly or every user shares the proxy's IP: app.set("trust proxy", 1)

  app.use(express.json({ limit: "1kb" })); // reject oversized bodies early (413)

  const loginLimiter = rateLimit({
    windowMs: 60_000,
    limit: 5, // 5 attempts per IP per minute (real systems also limit per ACCOUNT, not just per IP)
    standardHeaders: true,
    legacyHeaders: false,
    message: { error: "too many attempts, try again later" },
  });

  app.post("/login", loginLimiter, (req, res) => res.status(401).json({ error: "invalid username or password" })); // same message for any failure

  // Central error handler: a short generic message, never a stack trace (and don't log request bodies).
  app.use((err, req, res, next) => res.status(err.status ?? 500).json({ error: err.status === 413 ? "payload too large" : "request failed" }));
  return app;
}

if (import.meta.url === `file://${process.argv[1]}`) {
  const server = makeApp().listen(0);
  const base = `http://127.0.0.1:${server.address().port}`;
  const post = (body) => fetch(base + "/login", { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify(body) });

  const statuses = [];
  for (let i = 0; i < 7; i++) statuses.push((await post({ user: "alice", pass: "guess" + i })).status);
  const big = await post({ blob: "x".repeat(5000) });
  server.close();

  console.log("login attempts 1..7 ->", statuses.join(" "));
  console.log("oversized body       ->", big.status);
  const ok = statuses.slice(0, 5).every((s) => s === 401) && statuses.slice(5).every((s) => s === 429) && big.status === 413;
  console.log(ok ? "\nPASS: attempts 6 and 7 are throttled (429); a 5 KB body is refused (413)." : "\nFAIL");
  process.exit(ok ? 0 : 1);
}
