// Lab 3: JWT mistakes. decode() is NOT verify(). Always pin the algorithm.   Run: node lab3_jwt.mjs
import jwt from "jsonwebtoken";

const SECRET = "demo-only-secret-use-32-plus-random-bytes-in-real-life";
const b64 = (obj) => Buffer.from(JSON.stringify(obj)).toString("base64url");

// A legitimate token for a normal user.
const good = jwt.sign({ sub: "alice", role: "user" }, SECRET, { algorithm: "HS256", expiresIn: "15m" });
const [header, , signature] = good.split(".");

// Attacker edits the payload (role: admin) but cannot recompute the signature.
const exp = Math.floor(Date.now() / 1000) + 3600;
const forged = [header, b64({ sub: "alice", role: "admin", exp }), signature].join(".");

// An "alg: none" token: no signature at all.
const none = [b64({ alg: "none", typ: "JWT" }), b64({ sub: "alice", role: "admin", exp }), ""].join(".");

const expired = jwt.sign({ sub: "alice" }, SECRET, { algorithm: "HS256", expiresIn: -10 });

const rejects = (token) => {
  try {
    jwt.verify(token, SECRET, { algorithms: ["HS256"] }); // pinned algorithm
    return false;
  } catch {
    return true;
  }
};

const results = {
  "decode() trusts the forged role (WRONG way)": jwt.decode(forged).role === "admin",
  "verify() accepts the genuine token": !rejects(good),
  "verify() rejects the forged payload": rejects(forged),
  "verify() rejects alg:none": rejects(none),
  "verify() rejects the expired token": rejects(expired),
};

for (const [name, value] of Object.entries(results)) console.log(`${value ? "PASS" : "FAIL"}  ${name}`);
const ok = Object.values(results).every(Boolean);
console.log(ok ? "\nPASS: verify with a pinned algorithm; never trust decode()." : "\nFAIL");
process.exit(ok ? 0 : 1);
