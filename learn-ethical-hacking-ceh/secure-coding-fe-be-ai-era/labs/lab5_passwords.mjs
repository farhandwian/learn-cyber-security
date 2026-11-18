// Lab 5: password hashing with scrypt (Node stdlib), stored params, and upgrade-on-login.   Run: node lab5_passwords.mjs
// OWASP's current minimum for scrypt (when Argon2id is unavailable): N=2^17, r=8, p=1.
// In production prefer Argon2id (m=19 MiB, t=2, p=1 minimum) via a maintained library.
import crypto from "node:crypto";
import { promisify } from "node:util";

const scrypt = promisify(crypto.scrypt);
const CURRENT = { N: 2 ** 17, r: 8, p: 1 };
const KEYLEN = 32;

const run = (password, salt, { N, r, p }) =>
  scrypt(password.normalize("NFKC"), salt, KEYLEN, { N, r, p, maxmem: 256 * 1024 * 1024 });

// Stored format records the parameters, so you can raise them later: scrypt$N$r$p$salt$hash
export async function hashPassword(password, params = CURRENT) {
  const salt = crypto.randomBytes(16);
  const hash = await run(password, salt, params);
  return ["scrypt", params.N, params.r, params.p, salt.toString("base64"), hash.toString("base64")].join("$");
}

export async function verifyPassword(password, stored) {
  const [, N, r, p, saltB64, hashB64] = stored.split("$");
  const params = { N: Number(N), r: Number(r), p: Number(p) };
  const expected = Buffer.from(hashB64, "base64");
  const actual = await run(password, Buffer.from(saltB64, "base64"), params);
  const ok = actual.length === expected.length && crypto.timingSafeEqual(actual, expected);
  const needsRehash = ok && params.N < CURRENT.N; // upgrade the hash the next time the user logs in
  return { ok, needsRehash };
}

if (import.meta.url === `file://${process.argv[1]}`) {
  const t0 = performance.now();
  const a = await hashPassword("correct horse battery staple");
  const ms = Math.round(performance.now() - t0);
  const b = await hashPassword("correct horse battery staple");

  const legacy = await hashPassword("hunter2", { N: 2 ** 14, r: 8, p: 1 }); // an older, weaker setting

  const checks = {
    [`hash takes under 1 second (took ${ms} ms)`]: ms < 1000,
    "same password gives different hashes (random salt)": a !== b,
    "right password verifies": (await verifyPassword("correct horse battery staple", a)).ok,
    "wrong password is rejected": !(await verifyPassword("wrong", a)).ok,
    "current-strength hash does not need a rehash": !(await verifyPassword("correct horse battery staple", a)).needsRehash,
    "weak legacy hash verifies AND is flagged for rehash": (await verifyPassword("hunter2", legacy)).needsRehash === true,
  };
  let ok = true;
  for (const [name, pass] of Object.entries(checks)) {
    ok &&= pass;
    console.log(`${pass ? "PASS" : "FAIL"}  ${name}`);
  }
  console.log("\nStored value looks like:", a.slice(0, 48) + "...");
  console.log(ok ? "\nPASS" : "\nFAIL");
  process.exit(ok ? 0 : 1);
}
