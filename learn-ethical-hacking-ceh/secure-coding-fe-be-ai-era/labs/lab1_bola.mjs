// Lab 1: BOLA/IDOR and mass assignment, vulnerable vs fixed.   Run: node lab1_bola.mjs
import express from "express";

export function makeApp({ safe }) {
  // Fresh data per app so the vulnerable PATCH can't pollute the fixed run.
  const users = {
    1: { id: 1, name: "alice", isAdmin: false },
    2: { id: 2, name: "bob", isAdmin: false },
  };
  const orders = [
    { id: 1001, ownerId: 1, item: "Alice's laptop" },
    { id: 1002, ownerId: 2, item: "Bob's private gift" },
  ];

  const app = express();
  app.use(express.json());

  // Authentication is faked with a header so the lab stays small.
  // In real life this is a session cookie or a VERIFIED token (see Lab 3).
  app.use((req, res, next) => {
    const user = users[req.header("x-user-id")];
    if (!user) return res.status(401).json({ error: "not authenticated" });
    req.user = user;
    next();
  });

  app.get("/orders/:id", (req, res) => {
    const order = orders.find((o) => o.id === Number(req.params.id));
    if (!order) return res.status(404).json({ error: "not found" });
    // FIX (BOLA): authorize this user for THIS object. 404 hides that it exists.
    if (safe && order.ownerId !== req.user.id) return res.status(404).json({ error: "not found" });
    res.json(order);
  });

  app.patch("/profile", (req, res) => {
    if (safe) {
      // FIX (mass assignment): copy only the fields a user may change.
      if (typeof req.body?.name === "string") req.user.name = req.body.name.slice(0, 50);
    } else {
      Object.assign(req.user, req.body); // VULNERABLE: client can send {"isAdmin": true}
    }
    res.json(req.user);
  });

  return app;
}

async function run(label, safe) {
  const server = makeApp({ safe }).listen(0);
  const base = `http://127.0.0.1:${server.address().port}`;
  const call = (path, userId, init = {}) =>
    fetch(base + path, { ...init, headers: { "x-user-id": userId, "content-type": "application/json" } });

  const other = await call("/orders/1002", "1"); // Alice asks for BOB's order
  const bolaLeak = other.status === 200;
  const patch = await call("/profile", "1", { method: "PATCH", body: JSON.stringify({ name: "alice", isAdmin: true }) });
  const escalated = (await patch.json()).isAdmin === true;
  server.close();

  console.log(`${label}`);
  console.log(`  Alice reads Bob's order : ${bolaLeak ? "LEAK (200)" : `blocked (${other.status})`}`);
  console.log(`  Alice makes herself admin: ${escalated ? "SUCCEEDED" : "blocked"}`);
  return { bolaLeak, escalated };
}

if (import.meta.url === `file://${process.argv[1]}`) {
  const vuln = await run("VULNERABLE app", false);
  const fixed = await run("FIXED app", true);
  const ok = vuln.bolaLeak && vuln.escalated && !fixed.bolaLeak && !fixed.escalated;
  console.log(ok ? "\nPASS: vulnerable app leaks, fixed app does not." : "\nFAIL: unexpected result");
  process.exit(ok ? 0 : 1);
}
