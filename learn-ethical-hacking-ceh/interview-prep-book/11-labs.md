# Hands-On Labs

> **Why labs?** Reading builds recognition; doing builds recall. A concept you have *seen happen on your own screen* survives interview pressure. Each lab has a goal, the time it takes, steps, what you should see, and a **reflection** question. Answer the reflection in writing: that is the active-recall step.
>
> **Legal rule for every lab:** only use your own machine, your own code, practice platforms, and `scanme.nmap.org`. Never aim these techniques at systems you don't have permission to test.

| Lab | Week | Time | What you will see |
| --- | --- | --- | --- |
| 1. Encoding vs hashing vs salting (Python) | 1 | 25 min | Why hashes differ and encodings don't |
| 2. Wireshark: TCP handshake and TLS hello | 1 | 45 min | The handshake from the book on your own screen |
| 3. Read a site's security headers | 1 | 15 min | HSTS, CSP, cookie flags in real life |
| 4. nmap on scanme.nmap.org | 2 | 60 min | Open ports and versions |
| 5. Read a real CVE and CVSS vector | 2 | 30 min | Severity translated to English |
| 6. TryHackMe rooms | 2 | 3 h | Guided practice |
| 7. SQL injection and its fix (your own toy DB) | 3 | 25 min | The vulnerability and the fix in code |
| 8. XSS and its fix (local HTML file) | 3 | 20 min | The alert box and the encoding fix |
| 9. PortSwigger Web Security Academy | 3 | 3 h | Real lab environments |
| 10. Juice Shop (optional) | 3-4 | 2 h | A whole vulnerable app, locally |
| 11. Threat-model a feature with STRIDE | 4 | 45 min | Security thinking on your own code |
| 12. Mock interview: record yourself | 4 | 3 h | Your real weak spots |

---

## Lab 1: Encoding vs hashing vs salted hashing in Python

**Goal:** see with your own eyes why Base64 is not security and why salts matter. **Time:** 25 minutes. **Chapter:** [3](03-cryptography.md).

Save this as `lab1_crypto.py` and run `python3 lab1_crypto.py` (standard library only):

```python
import base64, hashlib, os

secret = b"hello"

# 1. Encoding: reversible by anyone, no key
encoded = base64.b64encode(secret)
print("base64 :", encoded, "->", base64.b64decode(encoded))

# 2. Hashing: one-way, deterministic
print("sha256 :", hashlib.sha256(secret).hexdigest())

# 3. A fast, unsalted hash: same password gives the SAME hash every time
pw = b"password123"
print("md5 #1 :", hashlib.md5(pw).hexdigest())
print("md5 #2 :", hashlib.md5(pw).hexdigest())

# 4. Salted, slow hash (scrypt, from the standard library): DIFFERENT every time
def hash_password(password: bytes) -> str:
    salt = os.urandom(16)
    digest = hashlib.scrypt(password, salt=salt, n=2**14, r=8, p=1)
    return salt.hex() + ":" + digest.hex()

def verify(password: bytes, stored: str) -> bool:
    salt_hex, digest_hex = stored.split(":")
    digest = hashlib.scrypt(password, salt=bytes.fromhex(salt_hex), n=2**14, r=8, p=1)
    return digest.hex() == digest_hex

a, b = hash_password(pw), hash_password(pw)
print("scrypt #1:", a[:48], "...")
print("scrypt #2:", b[:48], "...")
print("hashes differ:", a != b)
print("right password verifies:", verify(pw, a))
print("wrong password verifies:", verify(b"nope", a))
```

**What you should see:** Base64 decodes straight back; the two MD5 lines are identical; the two scrypt lines differ even for the same password, yet `verify` still works. (In real systems use a maintained library such as `argon2-cffi` or `bcrypt`; this lab uses the standard library only so nothing needs installing.)

**Reflect:** (1) If a database of MD5 hashes leaks, why can an attacker crack both users who share a password in one go? (2) Why does the salt not need to be secret?

---

## Lab 2: Watch a TCP handshake and a TLS hello in Wireshark

**Goal:** see the handshake and TLS setup from Chapters 3 and 4 on real traffic. **Time:** 45 minutes. **Chapter:** [4](04-networking-and-web.md).

1. Install **Wireshark** from wireshark.org (or `sudo apt install wireshark` on Ubuntu). On WSL, run Wireshark on the Windows side, because WSL has no direct access to your network interface.
2. Open Wireshark, pick your active network interface (Wi-Fi or Ethernet) and **start capturing**. Capture only **your own** traffic on a network you are allowed to use.
3. In a browser, visit a plain-HTTP page (for example `http://neverssl.com`, a site that exists to stay on plain HTTP) and an HTTPS page (any site). Then **stop** the capture.
4. **Find a handshake.** In the display-filter bar enter: `tcp.flags.syn == 1`. Click a SYN packet, then right-click it and choose *Conversation Filter → TCP*. You should see three packets: SYN, SYN/ACK, ACK.
5. **Read plain HTTP.** Filter `http`. Click a request, then *Follow → HTTP Stream*. Notice that everything, including cookies and headers, is readable plain text.
6. **Find the TLS hello.** Filter `tls.handshake.type == 1` (Client Hello). Expand *Transport Layer Security → Handshake Protocol → Extension: server_name*. You will see which site you were contacting, even though the rest is encrypted.
7. **Look at DNS.** Filter `dns` and see the name lookups that preceded each connection.

**What you should see:** a three-packet handshake; readable plain HTTP; unreadable HTTPS; and a visible site name (SNI) in the TLS hello.

**Reflect:** (1) What exactly did the plain-HTTP capture reveal that the HTTPS one did not? (2) Which parts of an HTTPS connection are still visible to someone on the network?

---

## Lab 3: Read the security headers of a website

**Goal:** recognize good and missing protections in real responses. **Time:** 15 minutes. **Chapter:** [4](04-networking-and-web.md).

```bash
curl -sI https://example.com
curl -sI https://github.com
```

`-I` fetches only the response headers (a normal request, just like a browser makes). For each site, look for:

- `Strict-Transport-Security` (HSTS)
- `Content-Security-Policy`
- `X-Content-Type-Options: nosniff`
- `Set-Cookie` (if present): are `HttpOnly`, `Secure` and `SameSite` set?

Then try one of **your own** projects, and optionally paste a URL into securityheaders.com for a graded report.

**What you should see:** well-run sites send several of these headers; simple pages often send none.

**Reflect:** Pick one missing header on your own project and write the one-line risk it leaves open and the one-line fix.

---

## Lab 4: Scan the one server that invites you to (scanme.nmap.org)

**Goal:** run a real scan and read the output like a professional. **Time:** 60 minutes. **Chapter:** [5](05-recon-and-scanning.md).

> The nmap project provides `scanme.nmap.org` for people to practise scanning, with the request not to hammer it (a few scans a day is fine). **Do not scan any other target without written permission.**

1. Install nmap: `sudo apt install nmap` (Windows/macOS: nmap.org/download).
2. **Scan your own machine first:** `nmap localhost`. Which ports are open on your own computer, and do you recognize all of them?
3. **Scan the practice target:** `nmap -sV scanme.nmap.org`. This sends a SYN to common ports and then identifies the software versions.
4. **Annotate the output:** for each open port write the port, the service, the version, and "is this version old enough to have known CVEs?"
5. **Compare scan types:** run `sudo nmap -sS scanme.nmap.org` (SYN scan) and `nmap -sT scanme.nmap.org` (connect scan). Same results? Think about which one completes the handshake.
6. **Your own home network (only devices you own):** find your range with `ip addr` (or `ipconfig`), then run a ping sweep such as `nmap -sn 192.168.1.0/24`. How many devices do you find? Do you recognize every one?

**What you should see:** a handful of open ports with versions on scanme; a list of your own devices on the home scan.

**Reflect:** (1) Which open port on your own machine surprised you? (2) For one open port you found, what would you check next, and what is the defender's fix?

---

## Lab 5: Read a real CVE and its CVSS vector

**Goal:** turn a severity score into plain English. **Time:** 30 minutes. **Chapter:** [5](05-recon-and-scanning.md).

1. Open nvd.nist.gov and search for **CVE-2021-44228** (Log4Shell).
2. Find the **CVSS 3.x base score** (10.0) and the **vector string**.
3. Translate each metric (AV, AC, PR, UI, S, C, I, A) into a plain English phrase using the table in Chapter 5.
4. Open the FIRST CVSS calculator (first.org/cvss/calculator/3.1), enter the same vector, then **change one metric** (for example set *Privileges Required* to High) and watch the score fall.
5. Search CISA's *Known Exploited Vulnerabilities Catalog* (cisa.gov) for the same CVE.

**Reflect:** (1) Which single metric change dropped the score most? (2) Why might a team treat a CVE that is on the KEV list as more urgent than a higher-scored one that is not?

---

## Lab 6: TryHackMe rooms

**Goal:** guided practice with built-in virtual machines. **Time:** about 3 hours (Saturday of Week 2).

1. Create a free account at tryhackme.com.
2. Do the introductory networking rooms from the beginner learning path.
3. Search for a room on **Nmap** and complete it.
4. After each room, write three sentences: what it taught, what surprised you, which interview question it answers.

---

## Lab 7: SQL injection and its fix (on your own toy database)

**Goal:** make the vulnerability and the fix real, on a database you created five seconds ago. **Time:** 25 minutes. **Chapter:** [6](06-injection-and-xss.md).

Save as `lab7_sqli.py` and run it (standard library only):

```python
import sqlite3

db = sqlite3.connect(":memory:")          # a throwaway database in RAM
db.execute("CREATE TABLE users(name TEXT, secret TEXT)")
db.executemany("INSERT INTO users VALUES (?, ?)",
               [("alice", "alice-secret"), ("bob", "bob-secret")])

def unsafe(name):
    # VULNERABLE: builds the query by concatenating strings
    return db.execute("SELECT * FROM users WHERE name = '" + name + "'").fetchall()

def safe(name):
    # SAFE: the value is passed separately from the query
    return db.execute("SELECT * FROM users WHERE name = ?", (name,)).fetchall()

print("unsafe, normal input :", unsafe("alice"))
print("unsafe, attack input :", unsafe("' OR '1'='1"))
print("safe,   attack input :", safe("' OR '1'='1"))
```

**What you should see:** the normal lookup returns one row; the attack input returns *every* row through the unsafe function and **nothing** through the safe one.

**Then extend it (this is where learning happens):**

1. Add a test: `assert safe("' OR '1'='1") == []` and make sure it passes.
2. Print the exact query string the unsafe function builds for the attack input, and compare it to Figure "SQL injection" in Chapter 6.
3. Try to make the `safe` function parameterize a **table name**. It can't. Write down how you would handle a user-chosen sort column safely (hint: an allowlist).

**Reflect:** In one sentence, why does the `?` placeholder make the attack harmless?

---

## Lab 8: XSS and its fix in a local HTML file

**Goal:** see a script run and then see encoding stop it. **Time:** 20 minutes. **Chapter:** [6](06-injection-and-xss.md).

Save as `lab8_xss.py`, run it, then open both generated files in your browser:

```python
import html, pathlib

# Pretend this came from a user comment stored in a database
comment = '<script>alert("this script ran")</script>Nice post!'

pathlib.Path("unsafe.html").write_text("<h1>Comments</h1><p>" + comment + "</p>")
pathlib.Path("safe.html").write_text("<h1>Comments</h1><p>" + html.escape(comment) + "</p>")
print("Now open unsafe.html and safe.html in your browser.")
```

**What you should see:** `unsafe.html` pops an alert box (the "comment" executed as code); `safe.html` simply *displays* the text of the tag. Use "View source" on `safe.html` and find `&lt;script&gt;`: that is the encoding at work.

**Extend it:** in a browser console, compare `div.innerHTML = comment` with `div.textContent = comment` and note which one is dangerous.

**Reflect:** Which line in a real web application corresponds to `comment`? (Hint: where does your app receive text from users?) Where is the right place to encode?

---

## Lab 9: PortSwigger Web Security Academy

**Goal:** practise on real, deliberately vulnerable applications, legally. **Time:** 3 hours. **Chapters:** [6](06-injection-and-xss.md) and [7](07-access-auth-requests.md).

The **Web Security Academy** (portswigger.net/web-security) is free, runs in your browser, and is designed for learning. Create a free account and work through these **Apprentice** labs:

| Topic | Lab to look for |
| --- | --- |
| SQL injection | "SQL injection vulnerability in WHERE clause allowing retrieval of hidden data"; "SQL injection vulnerability allowing login bypass" |
| XSS | "Reflected XSS into HTML context with nothing encoded"; "Stored XSS into HTML context with nothing encoded" |
| Access control | "Unprotected admin functionality"; "User ID controlled by request parameter" |
| CSRF | "CSRF vulnerability with no defenses" |

**How to use each lab (the method matters more than the speed):**

1. **Read the topic page first.** The Academy's explanations are excellent.
2. **Try for about 10 minutes before using any hint.** Struggling productively is what makes the lesson stick.
3. **Use hints freely, but don't copy a full solution.** Finish by understanding *why* it worked.
4. **Write three sentences:** what was the flaw, how was it exploited, how would *you* fix it in code. That third sentence is your interview answer.

**Reflect:** Which of the labs would a framework's default settings have prevented, and which setting was it?

---

## Lab 10 (optional): OWASP Juice Shop

**Goal:** explore a whole vulnerable web app that runs only on your machine. **Time:** 2 hours.

```bash
docker run --rm -p 3000:3000 bkimminich/juice-shop
```

Open `http://localhost:3000`. It is a deliberately insecure shop with a built-in scoreboard of challenges. Keep it **local only**, never exposed to the internet. Pick two challenges that match chapters you have read (injection, broken access control) and write the fix for each.

---

## Lab 11: Threat-model a feature you built with STRIDE

**Goal:** practise security thinking on your own code. **Time:** 45 minutes. **Chapter:** [9](09-people-malware-incident-response.md).

1. Pick a feature you know well (login, password reset, file upload, payments).
2. Draw it as boxes and arrows: user, browser, API, database, any third party.
3. For each arrow and box, fill in a table like this one:

| Element | S | T | R | I | D | E |
| --- | --- | --- | --- | --- | --- | --- |
| e.g. Password-reset endpoint | Attacker requests resets for others | Token edited in link | No audit log of resets | Reset email reveals if account exists | Mass reset requests flood email | Reset flow reused to reach admin |

4. For each realistic threat, write **one mitigation**. Circle the top three by risk (likelihood × impact).

**Reflect:** Which of your top three is *not yet* mitigated in the real system? Would you raise it with your team?

---

## Lab 12: Mock interview, record yourself

**Goal:** find your real weak spots under mild pressure. **Time:** 3 hours (Saturday of Week 4).

1. Pick 15 random questions from [10-qa-bank.md](10-qa-bank.md): `python3 -c "import random; print(sorted(random.sample(range(1,41),15)))"`.
2. Use your phone's voice or video recorder. For each question, answer **out loud in under 90 seconds**, using the four-step shape (what, how exploited, how prevented, real case).
3. **Watch or listen back** at normal speed. Score each answer on this rubric:

| Check | Yes / No |
| --- | --- |
| Started with a one-sentence definition | |
| Gave one concrete example | |
| **Ended with the fix** | |
| Explained any jargon in plain words | |
| Under 90 seconds, no rambling | |
| Few filler words ("um", "basically") | |

4. List the **three** most common problems and redo the five worst answers.
5. If you can, repeat it live with a friend or colleague playing the interviewer, and let them ask one follow-up per answer.

**Reflect:** Which topics did you freeze on? Add them to tomorrow's five-minute recall.
