// Lab 7: a URL validator for "fetch this URL for me" features (SSRF defence).   Run: node lab7_ssrf.mjs
import net from "node:net";
import dns from "node:dns/promises";

const blocked = new net.BlockList();
for (const [addr, prefix] of [
  ["0.0.0.0", 8], ["10.0.0.0", 8], ["100.64.0.0", 10], ["127.0.0.0", 8], ["169.254.0.0", 16], // 169.254.169.254 = cloud metadata
  ["172.16.0.0", 12], ["192.0.0.0", 24], ["192.168.0.0", 16], ["198.18.0.0", 15],
]) blocked.addSubnet(addr, prefix, "ipv4");
for (const [addr, prefix] of [["::1", 128], ["fc00::", 7], ["fe80::", 10]]) blocked.addSubnet(addr, prefix, "ipv6");

export async function assertSafeUrl(input) {
  const url = new URL(input); // the URL parser also normalizes tricks like http://2130706433/ and http://0x7f.0.0.1/
  if (!["http:", "https:"].includes(url.protocol)) throw new Error(`scheme not allowed: ${url.protocol}`);

  const host = url.hostname.replace(/^\[|\]$/g, ""); // strip IPv6 brackets
  const addresses = net.isIP(host) ? [{ address: host, family: net.isIP(host) }] : await dns.lookup(host, { all: true });

  for (const { address, family } of addresses) {
    if (blocked.check(address, family === 6 ? "ipv6" : "ipv4")) throw new Error(`blocked address: ${address}`);
  }
  // Real systems must ALSO: connect to the address you just checked (not re-resolve; DNS rebinding),
  // re-check every redirect hop, set short timeouts and size limits, and prefer an allowlist of hosts.
  return url;
}

if (import.meta.url === `file://${process.argv[1]}`) {
  const cases = [
    ["http://127.0.0.1/admin", false],
    ["http://169.254.169.254/latest/meta-data/", false],
    ["http://10.1.2.3/", false],
    ["http://192.168.0.10:8080/", false],
    ["http://[::1]/", false],
    ["http://[::ffff:127.0.0.1]/", false],
    ["http://2130706433/", false], // decimal form of 127.0.0.1
    ["http://0x7f.0.0.1/", false], // hex form
    ["file:///etc/passwd", false],
    ["ftp://example.com/x", false],
    ["http://93.184.216.34/", true],
    ["https://1.1.1.1/", true],
  ];
  let ok = true;
  for (const [u, shouldPass] of cases) {
    let passed;
    try { await assertSafeUrl(u); passed = true; } catch { passed = false; }
    const good = passed === shouldPass;
    ok &&= good;
    console.log(`${good ? "PASS" : "FAIL"}  ${shouldPass ? "allowed" : "blocked"}  ${u}`);
  }
  console.log(ok ? "\nPASS" : "\nFAIL");
  process.exit(ok ? 0 : 1);
}
