# Chapter 3: Cryptography You Actually Need

> **Goal.** After this chapter you can: explain encoding vs encryption vs hashing and pick the right one; explain symmetric vs asymmetric encryption and why TLS uses both; describe how certificates and digital signatures work; narrate the TLS handshake; and say exactly how passwords should be stored and why.
>
> **Time:** about 3 hours. **Companion reading:** Bab 6 and Tabel 13.4 of your Indonesian book. **Lab:** [Lab 1](11-labs.md#lab-1-encoding-vs-hashing-vs-salted-hashing-in-python).

---

## 1. The big picture: three tools, three jobs

Most beginner confusion in cryptography comes from mixing up three different tools. Fix this first and everything else is easier.

![Encoding vs encryption vs hashing](images/06-hash-encrypt-encode.svg)

| You need to... | Use | Example |
| --- | --- | --- |
| Put data in a format another system can read | **Encoding** | Base64 for binary in JSON, URL-encoding |
| Keep data secret, but get it back later | **Encryption** | AES for files, TLS for traffic |
| Check data was not changed, or store a password | **Hashing** | SHA-256 checksum, bcrypt password hash |

> **Common mistake #1.** "Base64 is encryption." It is not. Anyone can decode it, no key needed. Seeing a password or token in Base64 is not protection; it is the same as plain text.
>
> **Common mistake #2.** "We *decrypt* the hash to verify the password." A hash cannot be reversed. To verify a password you hash the *attempt* and compare hashes.
>
> **Common mistake #3.** "We encrypt passwords." If you can decrypt them, so can an attacker who steals the key. Passwords should be hashed, never encrypted.

---

## 2. Hashing in depth

A **hash function** turns any input into a fixed-size fingerprint.

Properties to remember:

- **Deterministic:** the same input always gives the same output.
- **Fixed size:** a one-word input and a one-gigabyte file both give, say, 256 bits.
- **One-way:** you cannot compute the input from the output.
- **Avalanche effect:** change one character and the whole output changes.
- **Collision resistant:** it should be practically impossible to find two inputs with the same hash.

Where you already meet hashes as a developer: **Git** names every commit by its hash; **download checksums** prove a file is intact; **digital signatures** sign a hash, not the whole message; **HMACs** prove a message came from someone who knows a secret.

| Algorithm | Status | Use for |
| --- | --- | --- |
| MD5, SHA-1 | **Broken** for security (collisions found) | Nothing security-related. Legacy checksums only. |
| SHA-256 / SHA-3 | Good | Integrity checks, signatures, fingerprints |
| bcrypt, scrypt, **Argon2id** | Good, and *deliberately slow* | **Passwords** |

> **Why "fast" is bad for passwords.** SHA-256 is designed to be fast, so a graphics card can try billions of guesses per second against a stolen database. Password hashes (bcrypt, scrypt, Argon2) are designed to be slow and memory-hungry, which makes each guess expensive for the attacker while costing a login only a fraction of a second.

---

## 3. Storing passwords correctly

![How to store passwords](images/23-password-storage.svg)

The safe recipe has two ingredients:

1. **A slow, purpose-built password hash** (Argon2id, bcrypt, scrypt). Never MD5, SHA-1 or plain SHA-256.
2. **A unique random salt per user.** A **salt** is random data stored next to the hash and mixed in before hashing. Two consequences: identical passwords produce different hashes, and precomputed lookup tables ("rainbow tables") become useless because the attacker would need a separate table for every salt.

(Good libraries do both for you: the salt is generated and stored inside the output string. Never write this yourself.)

A **pepper** is an extra secret added to all passwords but stored *outside* the database (for example in a secrets manager), so a stolen database alone is not enough. **Salt is per-user and stored beside the hash; pepper is shared and stored elsewhere.**

**Verification flow:** user submits password → look up that user's stored salt and hash → hash the submitted password with the same salt and settings → compare. No decryption anywhere.

> **Real case: LinkedIn (2012).** LinkedIn stored passwords as **unsalted SHA-1** hashes. After a breach, about **117 million** email and password records surfaced for sale in 2016, and many of the passwords were cracked quickly. Salted slow hashing would have made that dramatically harder.

> **Interview angle.** "How should passwords be stored?" Model answer: *"Hashed with a slow, salted algorithm such as Argon2id or bcrypt, never encrypted and never a fast hash like MD5. The slowness means each guess is expensive, and the per-user salt means identical passwords get different hashes and precomputed tables don't work."*

---

## 4. Symmetric vs asymmetric encryption

![Symmetric vs asymmetric encryption](images/07-symmetric-asymmetric.svg)

| | Symmetric (AES) | Asymmetric (RSA, ECC) |
| --- | --- | --- |
| Keys | One shared secret key | A public/private key pair |
| Speed | Very fast | Much slower |
| Main problem | How do both sides get the key safely? | Slowness |
| Typical use | Encrypting the actual data | Agreeing on a key, signing, identity |

**The key idea:** the two types fix each other's weaknesses. Asymmetric crypto solves *key distribution* ("how do two strangers agree on a secret over a hostile network?"), and symmetric crypto solves *speed*. Real systems, including TLS, use **both**.

> **Analogy.** Asymmetric is a **padlock you hand out for free**: anyone can snap it shut (encrypt with the public key), but only you hold the key that opens it (the private key). Symmetric is a **shared safe combination**: fast to use, but you must get the combination to your friend without anyone overhearing.

One more term you may hear: **Diffie-Hellman** (and its elliptic-curve version) is a way for two parties to *agree on a shared secret* over an open channel without ever sending it. Modern TLS uses it to create fresh session keys.

---

## 5. Digital signatures and certificates

**Digital signature:** the sender hashes the message and *signs* the hash with their **private key**. Anyone can *verify* it with the sender's **public key**. If verification succeeds you know two things: the message was not altered (**integrity**) and it came from the key holder (**authenticity**, plus **non-repudiation**).

> Notice the reversal: **encryption uses the public key to lock and the private key to unlock; signing uses the private key to sign and the public key to verify.**

**Certificate:** a public key on its own proves nothing. Anyone can generate a key pair and claim to be bank.com. A **certificate** is a signed statement from a trusted **Certificate Authority (CA)**: *"this public key belongs to bank.com."*

**Chain of trust:** your operating system and browser ship with a list of trusted **root CAs**. A site's certificate is signed by an *intermediate* CA, which is signed by a *root* CA. The browser walks up the chain until it reaches a root it already trusts.

> **Analogy.** A certificate is a **passport**. You trust it because a government you already trust issued it, not because the person holding it says so.

The browser checks four things: is it signed by a trusted CA? Is it for *this* domain? Is it within its validity dates? Has it been revoked?

---

## 6. The TLS handshake

HTTPS is simply HTTP carried inside TLS. The handshake happens before any HTTP is sent.

![TLS handshake](images/08-tls-handshake.svg)

1. **ClientHello.** The browser offers the TLS versions and cipher suites it supports and sends its half of a key exchange.
2. **ServerHello + certificate.** The server picks the options, sends its certificate and its half of the key exchange.
3. **Verification.** The browser checks the certificate (chain, domain, dates).
4. **Session key.** Both sides independently compute the *same* secret key from the exchanged values. The key itself is never transmitted.
5. **Encrypted traffic.** Everything from here on is encrypted with the fast symmetric session key.

**Why a man-in-the-middle fails:** to impersonate bank.com, the attacker needs a certificate for bank.com signed by a trusted CA, which they cannot get. A forged certificate makes the browser show a warning.

**Follow-ups you should expect:**

- *What is forward secrecy?* Session keys are temporary. If the server's long-term private key is stolen later, **past** recorded traffic still cannot be decrypted. TLS 1.3 requires it.
- *TLS 1.3 vs 1.2?* 1.3 is faster (fewer round trips) and removed old, weak options.
- *What does the padlock mean?* Only that the connection is encrypted **and** the server really owns that domain. It does **not** mean the site is trustworthy: a phishing site can have a perfectly valid certificate.
- *What is a downgrade attack?* Tricking both sides into using an older, weaker protocol. **HSTS** (an HTTP header) tells browsers to always use HTTPS for a site, which blocks it.

---

## 7. Encryption at rest, in transit, in use

| State | Meaning | Protection |
| --- | --- | --- |
| **In transit** | Moving across a network | TLS |
| **At rest** | Stored on disk or in a database | Disk or column encryption (AES) |
| **In use** | Being processed in memory | Hard; specialized hardware ("confidential computing") |

The hard part of encryption is almost never the algorithm; it is **key management**: where keys live, who can read them, and how they are rotated. Keys belong in a secrets manager or KMS, never in source code or a repository.

---

## 8. Crypto mistakes developers actually make

- **Rolling your own crypto.** Always use a vetted library. ("Don't invent your own cipher" is the first rule.)
- **Hard-coded keys and secrets** in source code, config files committed to Git, or front-end bundles.
- **Weak or fast password hashing** (MD5, SHA-1, plain SHA-256).
- **ECB mode** for block ciphers (it leaks patterns). Prefer an authenticated mode such as **AES-GCM**.
- **Predictable "random" values.** `Math.random()` is not for tokens. Use a cryptographically secure generator (`secrets` in Python, `crypto.randomBytes` in Node).
- **Turning off certificate verification** (`verify=False`, "trust all certificates") to make an error go away. This quietly removes the protection TLS gives.

---

## Check yourself

1. Is Base64 encryption? Why or why not?
2. Why can't you "decrypt" a password hash, and how do you check a login instead?
3. What does a salt do, and how is it different from a pepper?
4. Why does TLS use both asymmetric and symmetric encryption?
5. A signature uses which key to *sign* and which to *verify*?
6. What does the browser padlock guarantee, and what does it *not* guarantee?

**Answers** *(cover this until you have tried)*

1. No. It is encoding: reversible by anyone with no key, so it provides no secrecy.
2. Hashing is one-way. To check a login, hash the submitted password with the stored salt and compare the two hashes.
3. A salt is random, per user and stored beside the hash; it makes identical passwords hash differently and defeats precomputed tables. A pepper is a shared secret kept *outside* the database so a stolen database alone is not enough.
4. Asymmetric crypto lets two parties agree on a secret over an open network but is slow; symmetric crypto is fast for bulk data. TLS uses the first to set up a key and the second to encrypt the traffic.
5. Sign with the **private** key; verify with the **public** key.
6. It guarantees the connection is encrypted and the server controls that domain. It does not guarantee the site is honest or safe.

---

## Summary

- Encoding = format, encryption = secrecy (reversible with a key), hashing = fingerprint (one-way).
- Passwords: Argon2id/bcrypt, salted, never encrypted, never fast hashes.
- Asymmetric agrees on a key; symmetric encrypts the data. TLS uses both.
- Certificates are signed statements from trusted CAs; that is why a man-in-the-middle fails.
- The usual real-world failure is key management and misuse, not the algorithm.
