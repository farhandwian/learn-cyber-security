#!/usr/bin/env python3
"""Generate the book's diagrams (SVG) into ../images.   Usage: python3 make_diagrams.py"""
import os, textwrap, hashlib
from xml.sax.saxutils import escape

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "images")
NAVY = "#12304a"; TEAL = "#1b8a9a"; RED = "#c0392b"; GREEN = "#2e8b57"; AMBER = "#c77d0a"
INK = "#1a1a1a"; MUTE = "#5b6b79"; GREY = "#eef2f5"; WHITE = "#ffffff"
PINK = "#fbeaea"; MINT = "#e7f5ec"; SKY = "#e6f3f7"; SAND = "#fdf3e0"
ORANGE = "#d9622b"; DARKRED = "#8e1b12"
FONT = "DejaVu Sans, Verdana, Arial, sans-serif"
MONO = "DejaVu Sans Mono, Consolas, monospace"


def wrap(line, width, size, mono=False):
    n = max(4, int(width / (size * (0.62 if mono else 0.6))))
    return textwrap.wrap(line, n) or [""]


class S:
    def __init__(s, w, h, title=None, sub=None):
        s.w, s.h, s.p, s.marks = w, h, [], set()
        if title:
            s.text(w / 2, 32, title, 19, NAVY, "bold", "middle")
        if sub:
            s.text(w / 2, 54, sub, 12.5, MUTE, "normal", "middle")

    def text(s, x, y, t, size=14, fill=INK, weight="normal", anchor="start", font=FONT, lh=1.3, width=None):
        lines = []
        for l in str(t).split("\n"):
            lines += wrap(l, width, size, font == MONO) if width else [l]
        tsp = "".join(
            f'<tspan x="{x}" dy="{0 if i == 0 else round(size * lh, 1)}">{escape(l)}</tspan>'
            for i, l in enumerate(lines))
        s.p.append(f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" fill="{fill}" '
                   f'font-weight="{weight}" text-anchor="{anchor}">{tsp}</text>')

    def ctext(s, cx, cy, t, size=14, fill=INK, weight="normal", font=FONT, lh=1.3, width=None):
        lines = []
        for l in str(t).split("\n"):
            lines += wrap(l, width, size, font == MONO) if width else [l]
        y0 = cy - (len(lines) - 1) * size * lh / 2 + size * 0.35
        s.text(cx, round(y0, 1), "\n".join(lines), size, fill, weight, "middle", font, lh)

    def rect(s, x, y, w, h, fill=WHITE, stroke=NAVY, rx=10, sw=1.6, dash=False):
        d = ' stroke-dasharray="6 4"' if dash else ""
        s.p.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" '
                   f'stroke="{stroke}" stroke-width="{sw}"{d}/>')

    def box(s, x, y, w, h, label, fill=SKY, stroke=TEAL, tc=INK, size=14, weight="normal", font=FONT, dash=False):
        s.rect(x, y, w, h, fill, stroke, 10, dash=dash)
        s.ctext(x + w / 2, y + h / 2, label, size, tc, weight, font, width=w - 14)

    def card(s, x, y, w, h, title, body, color=TEAL, hh=34, size=12.5, tc=INK):
        s.rect(x, y, w, h, WHITE, color, 10)
        s.p.append(f'<path d="M{x},{y+hh} L{x},{y+10} Q{x},{y} {x+10},{y} L{x+w-10},{y} Q{x+w},{y} {x+w},{y+10} '
                   f'L{x+w},{y+hh} Z" fill="{color}"/>')
        s.ctext(x + w / 2, y + hh / 2, title, 14, WHITE, "bold", width=w - 12)
        s.text(x + 12, y + hh + 21, body, size, tc, width=w - 24, lh=1.35)

    def cell(s, x, y, w, h, head, body, fill, stroke, hc, size=11.5):
        s.rect(x, y, w, h, fill, stroke, 8)
        s.text(x + 10, y + 17, head, 9.5, hc, "bold")
        s.text(x + 10, y + 35, body, size, INK, width=w - 20, lh=1.28)

    def line(s, x1, y1, x2, y2, color=MUTE, sw=1.6, dash=False):
        d = ' stroke-dasharray="6 4"' if dash else ""
        s.p.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{sw}"{d}/>')

    def arrow(s, x1, y1, x2, y2, color=MUTE, dash=False, sw=2, head=True, tail=False):
        s.marks.add(color)
        d = ' stroke-dasharray="7 4"' if dash else ""
        m = f' marker-end="url(#a{color[1:]})"' if head else ""
        t = f' marker-start="url(#a{color[1:]})"' if tail else ""
        s.p.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{sw}"{d}{m}{t}/>')

    def path(s, d, color=MUTE, sw=2, dash=False, head=True):
        s.marks.add(color)
        dd = ' stroke-dasharray="7 4"' if dash else ""
        m = f' marker-end="url(#a{color[1:]})"' if head else ""
        s.p.append(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{sw}"{dd}{m}/>')

    def tag(s, cx, cy, t, size=12, fill=INK, weight="normal", bg=WHITE, font=FONT):
        w = len(t) * size * (0.62 if font == MONO else 0.6) + 10
        h = size + 8
        s.p.append(f'<rect x="{cx-w/2}" y="{cy-h/2}" width="{w}" height="{h}" rx="4" fill="{bg}"/>')
        s.text(cx, round(cy + size * 0.35, 1), t, size, fill, weight, "middle", font)

    def pill(s, cx, cy, t, fill, tc=WHITE, size=11):
        w = len(t) * size * 0.64 + 18
        h = size + 10
        s.p.append(f'<rect x="{cx-w/2}" y="{cy-h/2}" width="{w}" height="{h}" rx="{h/2}" fill="{fill}"/>')
        s.text(cx, round(cy + size * 0.35, 1), t, size, tc, "bold", "middle")

    def lifelines(s, actors, top=80, bottom=470):
        for nm, x, c in actors:
            s.box(x - 72, top, 144, 40, nm, c, c, WHITE, 13.5, "bold")
            s.line(x, top + 40, x, bottom, MUTE, 1.5, True)

    def msg(s, y, x1, x2, t, color=NAVY, both=False, dash=False):
        sx = 3 if x2 > x1 else -3
        s.arrow(x1 + sx, y, x2 - sx, y, color, dash, head=True, tail=both)
        s.text((x1 + x2) / 2, y - 9, t, 12, INK, anchor="middle")

    def save(s, name):
        defs = "".join(
            f'<marker id="a{c[1:]}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
            f'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{c}"/></marker>' for c in sorted(s.marks))
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {s.w} {s.h}" width="{s.w}" height="{s.h}">'
               f'<rect width="100%" height="100%" fill="#ffffff"/><defs>{defs}</defs>{"".join(s.p)}</svg>')
        open(os.path.join(OUT, name + ".svg"), "w", encoding="utf-8").write(svg)


# --------------------------------------------------------------------------- study skills
def d01():
    s = S(865, 365, "Your 4-week path", "About 10 hours a week: weekday evenings plus the weekend")
    items = [("WEEK 1\nFoundations", NAVY, "• Security basics: CIA, attack phases\n• Cryptography and TLS\n• Networking and how the web works"),
             ("WEEK 2\nRecon and scanning", TEAL, "• OSINT (passive recon)\n• nmap and port states\n• CVE, CWE, CVSS"),
             ("WEEK 3\nWeb attacks", RED, "• OWASP Top 10 (2025)\n• SQLi, XSS, CSRF\n• IDOR, SSRF, auth\n★ highest interview value"),
             ("WEEK 4\nSystems and review", GREEN, "• Network attacks and defenses\n• Malware, people, incident response\n• Q&A drill and mock interview")]
    for i, (t, c, b) in enumerate(items):
        x = 20 + i * 212
        s.card(x, 80, 185, 205, t, b, c, hh=50)
        if i < 3:
            s.arrow(x + 188, 180, x + 209, 180, MUTE)
    s.rect(20, 303, 825, 44, SAND, AMBER, 10)
    s.ctext(432, 325, "Every week:  read 40%  ·  hands-on lab 40%  ·  say answers out loud 20%", 14, INK, "bold")
    s.save("01-roadmap")


def d02():
    s = S(870, 300, "A realistic week", "Ten hours: short weekday sessions, one longer lab block, one rest day")
    days = [("MON", "1.5 h", "Read the\nchapter", SKY, TEAL), ("TUE", "1.5 h", "Read, type\nthe commands", SKY, TEAL),
            ("WED", "1.5 h", "Mini-lab\n(hands-on)", SAND, AMBER), ("THU", "1.5 h", "Quiz and\nrecall", MINT, GREEN),
            ("FRI", "rest", "No study.\nSleep helps\nmemory.", GREY, MUTE), ("SAT", "3 h", "Big lab\n(PortSwigger,\nTryHackMe)", SAND, AMBER),
            ("SUN", "1 h", "Teach-back:\nanswer out loud", MINT, GREEN)]
    for i, (d, h, a, f, c) in enumerate(days):
        x = 20 + i * 120
        s.rect(x, 80, 108, 135, f, c, 10)
        s.ctext(x + 54, 102, d, 13, c, "bold")
        s.ctext(x + 54, 136, h, 22, INK, "bold")
        s.ctext(x + 54, 183, a, 12, INK)
    s.rect(20, 235, 830, 44, WHITE, TEAL, 10)
    s.ctext(435, 257, "Start every session with 5 minutes of recall: write what you remember from last time, no notes.", 13, INK)
    s.save("02-weekly-rhythm")


def d03():
    s = S(865, 360, "The 4-step answer for any security question", "Memorize this shape; it works for almost every interview question")
    steps = [("1  WHAT is it?", "One plain sentence."), ("2  HOW is it exploited?", "One concrete example."),
             ("3  HOW do you prevent it?", "The fix in code or config."), ("4  WHEN did it happen?", "One real incident (bonus).")]
    ex = ["Untrusted input is run as part of a database query.",
          "Typing ' OR '1'='1 into a login form makes the condition always true.",
          "Parameterized queries, plus a database account with minimal rights.",
          "Heartland Payment Systems: SQL injection led to about 130 million card numbers stolen."]
    for i, (t, b) in enumerate(steps):
        x = 20 + i * 212
        s.card(x, 75, 185, 95, t, b, NAVY, hh=40)
        s.cell(x, 190, 185, 120, "EXAMPLE: SQL INJECTION", ex[i], SKY, TEAL, TEAL, 12)
        if i < 3:
            s.arrow(x + 188, 122, x + 209, 122, MUTE)
    s.ctext(432, 335, "The third step is where a software engineer stands out: always finish with the fix.", 13, GREEN, "bold")
    s.save("03-answer-framework")


# --------------------------------------------------------------------------- week 1
def d04():
    s = S(820, 430, "The CIA triad", "The three things security protects. Every attack breaks at least one.")
    s.box(295, 75, 230, 64, "CONFIDENTIALITY\nonly the right people can read it", NAVY, NAVY, WHITE, 12.5, "bold")
    s.box(50, 285, 230, 64, "INTEGRITY\ndata is not changed behind your back", TEAL, TEAL, WHITE, 12.5, "bold")
    s.box(540, 285, 230, 64, "AVAILABILITY\nthe system works when needed", GREEN, GREEN, WHITE, 12.5, "bold")
    s.line(350, 139, 200, 285, MUTE, 2); s.line(470, 139, 620, 285, MUTE, 2); s.line(280, 317, 540, 317, MUTE, 2)
    s.p.append(f'<circle cx="410" cy="225" r="42" fill="{SAND}" stroke="{AMBER}" stroke-width="2"/>')
    s.ctext(410, 225, "DATA", 15, AMBER, "bold")
    s.text(545, 100, "Broken when: a database leaks\nto strangers.", 12, RED, width=240)
    s.text(50, 375, "Broken when: someone silently\nedits a bank balance.", 12, RED, width=300)
    s.text(540, 375, "Broken when: ransomware or a DDoS\ntakes the site down.", 12, RED, width=240)
    s.save("04-cia-triad")


def d05():
    s = S(860, 420, "The 5 phases of an attack", "Also a great structure for 'walk me through how an attacker would...' answers")
    ph = [("1  RECON", "Watches the house from the street", "whois, DNS, LinkedIn, Shodan", "Share less publicly"),
          ("2  SCANNING", "Tries which doors and windows are unlocked", "nmap: open ports and service versions", "Close unused ports; firewall"),
          ("3  GAIN ACCESS", "Picks the lock and walks in", "SQL injection, stolen password, unpatched bug", "Patch, validate input, MFA"),
          ("4  MAINTAIN", "Copies a key to get back in later", "Backdoor, new admin account, scheduled task", "Monitor new accounts and tasks"),
          ("5  COVER TRACKS", "Wipes fingerprints, cuts the camera", "Deleting or editing log files", "Ship logs to a separate server")]
    for i, (n, b, t, d) in enumerate(ph):
        x = 20 + i * 167
        s.box(x, 75, 152, 48, n, NAVY, NAVY, WHITE, 13, "bold")
        if i < 4:
            s.arrow(x + 154, 99, x + 165, 99, MUTE)
        s.cell(x, 133, 152, 88, "LIKE A BURGLAR", b, SAND, AMBER, AMBER)
        s.cell(x, 229, 152, 88, "IN THE IT WORLD", t, SKY, TEAL, TEAL)
        s.cell(x, 325, 152, 78, "DEFENDER'S MOVE", d, MINT, GREEN, GREEN)
    s.save("05-five-phases")


def d06():
    s = S(860, 405, "Encoding vs encryption vs hashing", "Three different tools. Mixing them up is the classic beginner mistake.")
    lanes = [("ENCODING", "changes the format", SAND, AMBER, "Base64", "aGVsbG8=", "decode (no key needed)", GREEN,
              "Anyone can reverse it.\nNot security."),
             ("ENCRYPTION", "hides the content", SKY, TEAL, "AES + secret key", "9f3a7c…e1", "decrypt (key required)", GREEN,
              "Only the key holder can reverse it.\nUse for confidentiality."),
             ("HASHING", "fingerprints the content", MINT, GREEN, "SHA-256", "2cf24dba5fb0…", "✗ cannot be reversed", RED,
              "One-way. Same input, same output.\nUse for integrity and passwords.")]
    for i, (nm, sub, f, c, op, out, back, bc, verdict) in enumerate(lanes):
        y = 80 + i * 106
        s.rect(15, y, 830, 94, f, c, 10)
        s.text(30, y + 36, nm, 15, c, "bold")
        s.text(30, y + 56, sub, 11.5, MUTE)
        s.box(185, y + 14, 80, 42, "hello", WHITE, c, INK, 13, font=MONO)
        s.arrow(267, y + 35, 303, y + 35, c)
        s.box(305, y + 14, 130, 42, op, WHITE, c, INK, 12, "bold")
        s.arrow(437, y + 35, 473, y + 35, c)
        s.box(475, y + 14, 150, 42, out, WHITE, c, INK, 11.5, font=MONO)
        s.arrow(475, y + 77, 225, y + 77, bc, dash=True)
        s.tag(350, y + 77, back, 11.5, bc, "bold", bg=f)
        s.text(645, y + 30, verdict, 12, INK, "bold", width=190)
    s.save("06-hash-encrypt-encode")


def d07():
    s = S(860, 425, "Symmetric vs asymmetric encryption", "Symmetric is fast but has a key-sharing problem. Asymmetric solves sharing but is slower.")
    s.rect(15, 70, 410, 270, SKY, TEAL, 12); s.text(220, 97, "SYMMETRIC  (e.g. AES)", 15, TEAL, "bold", "middle")
    s.box(40, 150, 100, 50, "Alice", WHITE, NAVY, INK, 14, "bold"); s.box(300, 150, 100, 50, "Bob", WHITE, NAVY, INK, 14, "bold")
    s.arrow(142, 175, 298, 175, NAVY); s.text(220, 163, "encrypted message", 12, INK, anchor="middle")
    s.pill(90, 128, "KEY K", AMBER); s.pill(350, 128, "KEY K", AMBER); s.line(130, 128, 310, 128, AMBER, 1.5, True)
    s.text(220, 232, "Both sides use the SAME key.", 13, INK, "bold", "middle")
    s.text(220, 262, "✔ very fast", 12.5, GREEN, "bold", "middle")
    s.text(220, 284, "✘ how do you share K safely in the first place?", 12.5, RED, "bold", "middle")
    s.rect(435, 70, 410, 270, MINT, GREEN, 12); s.text(640, 97, "ASYMMETRIC  (e.g. RSA, ECC)", 15, GREEN, "bold", "middle")
    s.box(455, 150, 90, 50, "Alice", WHITE, NAVY, INK, 14, "bold"); s.box(745, 150, 90, 50, "Bob", WHITE, NAVY, INK, 14, "bold")
    s.arrow(547, 175, 743, 175, NAVY); s.text(645, 163, "locked with the PUBLIC key", 11.5, INK, anchor="middle")
    s.pill(500, 128, "Bob's PUBLIC key", GREEN, size=10.5)
    s.pill(768, 128, "Bob's PRIVATE key", RED, size=10.5)
    s.text(640, 232, "Anyone can lock; only Bob can unlock.", 13, INK, "bold", "middle")
    s.text(640, 262, "✔ no secret has to be shared", 12.5, GREEN, "bold", "middle")
    s.text(640, 284, "✘ much slower", 12.5, RED, "bold", "middle")
    s.rect(15, 358, 830, 48, SAND, AMBER, 10)
    s.ctext(430, 382, "TLS uses BOTH: asymmetric crypto to agree on a secret, then fast symmetric encryption for the real traffic.", 12.5, INK, "bold", width=800)
    s.save("07-symmetric-asymmetric")


def d08():
    s = S(860, 495, "TLS handshake (simplified)", "What happens between 'connect' and the first encrypted byte")
    s.lifelines([("Browser", 190, NAVY), ("Server", 670, NAVY)], 75, 480)
    s.msg(150, 190, 670, "1  ClientHello: TLS versions, ciphers, key share")
    s.msg(205, 670, 190, "2  ServerHello + certificate + key share")
    s.box(25, 228, 345, 58, "3  Browser verifies the certificate: signed by a trusted CA? Right domain? Not expired?", SAND, AMBER, INK, 12)
    s.box(480, 228, 355, 58, "A man-in-the-middle cannot present a valid certificate for the domain, so step 3 fails.", PINK, RED, INK, 12)
    s.box(110, 315, 640, 40, "4  Both sides now compute the same secret session key (it is never sent over the wire)", MINT, GREEN, INK, 12.5)
    s.msg(410, 190, 670, "5  Encrypted HTTP traffic (fast symmetric encryption)", GREEN, both=True)
    s.save("08-tls-handshake")


def d09():
    s = S(860, 450, "TCP handshake, and how a SYN flood abuses it")
    s.rect(15, 50, 410, 345, SKY, TEAL, 12); s.text(220, 76, "Normal 3-way handshake", 15, TEAL, "bold", "middle")
    s.rect(435, 50, 410, 345, PINK, RED, 12); s.text(640, 76, "SYN flood (denial of service)", 15, RED, "bold", "middle")
    for nm, x in (("Client", 95), ("Server", 345)):
        s.box(x - 50, 90, 100, 34, nm, NAVY, NAVY, WHITE, 13, "bold"); s.line(x, 124, x, 290, MUTE, 1.5, True)
    for y, a, b, t in ((160, 95, 345, 'SYN  ("can we talk?")'), (215, 345, 95, 'SYN/ACK  ("yes, can you?")'), (270, 95, 345, 'ACK  ("yes")')):
        s.arrow(a + (3 if b > a else -3), y, b - (3 if b > a else -3), y, NAVY); s.text((a + b) / 2, y - 9, t, 11.5, anchor="middle")
    s.box(40, 322, 350, 44, "Connection established: data flows", MINT, GREEN, INK, 12.5)
    for nm, x, c in (("Attacker", 520, RED), ("Server", 780, NAVY)):
        s.box(x - 50, 90, 100, 34, nm, c, c, WHITE, 13, "bold"); s.line(x, 124, x, 240, MUTE, 1.5, True)
    for i, y in enumerate((150, 183, 216)):
        s.arrow(524, y, 776, y, RED); s.text(650, y - 7, "SYN  (fake source address)" if i == 0 else "SYN", 11.5, anchor="middle")
    s.text(640, 262, "The server answers each SYN and waits for an ACK that never comes.", 12, INK, anchor="middle", width=380)
    s.text(455, 313, "Waiting queue:", 12, MUTE, "bold")
    for i in range(8):
        s.rect(580 + i * 28, 299, 22, 18, RED, DARKRED, 3)
    s.ctext(640, 345, "FULL: real users are refused (availability lost)", 12.5, RED, "bold", width=380)
    s.rect(15, 408, 830, 34, MINT, GREEN, 10)
    s.ctext(430, 425, "Defenses: SYN cookies  ·  rate limiting  ·  upstream DDoS protection (CDN / scrubbing)", 12.5, INK, "bold")
    s.save("09-tcp-synflood")


def d10():
    s = S(880, 485, "What happens when you type https://bank.com", "Interview favourite: narrate the six steps and add one security note to each")
    st = [("1  DNS lookup", "The browser asks a DNS server: which IP address is bank.com?", "DNS spoofing sends you to a fake IP."),
          ("2  TCP handshake", "SYN, SYN/ACK, ACK opens a connection to port 443.", "A SYN flood can exhaust the server."),
          ("3  TLS handshake", "The server proves its identity with a certificate; both sides agree on a key.", "MITM or downgrade: certificates stop it."),
          ("4  HTTP request", "The browser sends GET /account plus cookies, now encrypted.", "Cookie theft (XSS), CSRF."),
          ("5  Server work", "Checks login, runs business logic, queries the database.", "SQL injection, IDOR, broken access control."),
          ("6  Response and render", "HTML and JS arrive; the browser enforces same-origin policy and CSP.", "XSS if output is not encoded.")]
    for i, (t, b, r) in enumerate(st):
        x = 20 + (i % 3) * 285; y = 75 + (i // 3) * 205
        s.card(x, y, 270, 185, t, b, NAVY, hh=34)
        s.rect(x + 8, y + 122, 254, 54, PINK, RED, 6)
        s.text(x + 16, y + 141, "RISK: " + r, 11.5, RED, width=238)
        if i % 3 < 2:
            s.arrow(x + 273, y + 92, x + 282, y + 92, MUTE)
    s.path("M725,260 V268 H155 V277", MUTE)
    s.save("10-url-journey")


def d11():
    s = S(860, 488, "Where attacks live in the network stack", "Interview trick: name one attack per layer")
    s.text(30, 82, "LAYER", 11, MUTE, "bold"); s.text(250, 82, "PROTOCOLS YOU KNOW", 11, MUTE, "bold"); s.text(520, 82, "TYPICAL ATTACKS", 11, MUTE, "bold")
    rows = [("Application", NAVY, "HTTP, HTTPS, DNS, SSH, SMTP", "SQL injection, XSS, CSRF, credential stuffing, phishing links"),
            ("Transport", TEAL, "TCP, UDP (ports)", "SYN flood, port scanning, session hijacking"),
            ("Internet", GREEN, "IP, ICMP", "IP spoofing, ping flood, routing attacks"),
            ("Link", AMBER, "Ethernet, Wi-Fi, ARP", "ARP spoofing, rogue Wi-Fi access point, sniffing")]
    for i, (n, c, p, a) in enumerate(rows):
        y = 92 + i * 92
        s.box(20, y, 200, 78, n, c, c, WHITE, 15, "bold")
        s.box(235, y, 260, 78, p, GREY, MUTE, INK, 13)
        s.box(510, y, 330, 78, a, PINK, RED, INK, 13)
        s.arrow(221, y + 39, 233, y + 39, MUTE); s.arrow(496, y + 39, 508, y + 39, MUTE)
    s.text(20, 472, "Higher layers are closer to your code, so developers influence the top layer the most.", 12, MUTE)
    s.save("11-layers-attacks")


# --------------------------------------------------------------------------- week 2
def d12():
    s = S(860, 420, "Passive vs active reconnaissance", "Passive never touches the target. Active sends the target packets, so it needs permission.")
    s.rect(15, 70, 830, 155, SKY, TEAL, 12); s.pill(95, 88, "PASSIVE", TEAL)
    s.box(35, 125, 110, 60, "Attacker", NAVY, NAVY, WHITE, 13, "bold")
    s.rect(230, 105, 390, 100, WHITE, TEAL, 10, dash=True); s.text(425, 124, "Public sources", 11.5, MUTE, "bold", "middle")
    for i, n in enumerate(["WHOIS", "Google", "Shodan", "crt.sh", "LinkedIn"]):
        s.box(240 + i * 76, 142, 70, 36, n, SKY, TEAL, INK, 11)
    s.arrow(228, 158, 147, 158, TEAL)
    s.box(725, 125, 110, 60, "Target", GREY, MUTE, INK, 13, "bold")
    s.arrow(723, 158, 622, 158, MUTE, dash=True); s.text(672, 149, "public info", 10.5, MUTE, anchor="middle")
    s.text(780, 203, "never sees you", 11.5, MUTE, anchor="middle")
    s.rect(15, 238, 830, 160, PINK, RED, 12); s.pill(90, 256, "ACTIVE", RED)
    s.box(35, 290, 110, 60, "Attacker", NAVY, NAVY, WHITE, 13, "bold")
    s.box(725, 290, 110, 60, "Target", WHITE, RED, INK, 13, "bold")
    s.arrow(147, 308, 723, 308, RED, sw=2.5); s.text(435, 299, "probes: ping, port scan, banner grab", 12, anchor="middle")
    s.arrow(723, 336, 147, 336, RED, dash=True); s.text(435, 356, "replies reveal open ports and software versions", 12, anchor="middle")
    s.text(835, 372, "may log it or raise an alert", 11, RED, anchor="end")
    s.save("12-passive-vs-active")


def d13():
    s = S(860, 440, "The three port states nmap reports", "nmap sends a SYN to each port and reads the reply, or the silence")
    rows = [("OPEN", GREEN, "Port 443\nweb server listening", "SYN/ACK", "A service is listening and answers.\nThis is the attack surface.", False),
            ("CLOSED", AMBER, "Port 81\nnothing listening", "RST (reset)", "The host is reachable but no service uses this port.\nUseful: proves the host is alive.", False),
            ("FILTERED", RED, "Port 23\nbehind a firewall", "(silence)", "A firewall silently drops the probe.\nnmap cannot tell open from closed.", True)]
    for i, (st, c, host, reply, exp, blocked) in enumerate(rows):
        y = 75 + i * 118
        s.rect(15, y, 830, 106, WHITE, c, 10)
        s.box(30, y + 22, 110, 60, "Scanner\n(nmap)", NAVY, NAVY, WHITE, 12.5, "bold")
        if blocked:
            s.arrow(142, y + 40, 283, y + 40, NAVY); s.text(212, y + 32, "SYN", 12, anchor="middle")
            s.rect(286, y + 12, 12, 82, RED, RED, 2); s.text(292, y + 104, "firewall", 10, RED, anchor="middle")
            s.tag(215, y + 70, "no reply at all", 11.5, c, "bold")
        else:
            s.arrow(142, y + 40, 330, y + 40, NAVY); s.text(236, y + 32, "SYN", 12, anchor="middle")
            s.arrow(330, y + 68, 142, y + 68, c, dash=True); s.tag(236, y + 68, reply, 11.5, c, "bold")
        s.box(332, y + 22, 150, 60, host, GREY, MUTE, INK, 12)
        s.pill(540, y + 22, st, c)
        s.text(500, y + 50, exp, 11.5, INK, width=335)
    s.save("13-port-states")


def d14():
    s = S(860, 385, "CWE → CVE → CVSS: three names, three jobs")
    cards = [("CWE: the type of weakness", "CWE-89  SQL injection\nCWE-79  Cross-site scripting", "Like: \"brakes can fail\"", NAVY),
             ("CVE: one specific bug", "CVE-2021-44228, \"Log4Shell\", a flaw in Apache Log4j", "Like: \"the 2019 brake recall for Model X\"", TEAL),
             ("CVSS: how bad it is (0–10)", "Log4Shell scored 10.0, which means Critical", "Like: the safety rating on the box", RED)]
    for i, (t, b, a, c) in enumerate(cards):
        x = 20 + i * 285
        s.card(x, 60, 250, 150, t, b + "\n\n" + a, c, hh=38)
        if i < 2:
            s.arrow(x + 253, 135, x + 282, 135, MUTE)
    s.text(60, 247, "CVSS severity scale", 12, MUTE, "bold")
    segs = [(0.1, 3.9, "LOW", "0.1–3.9", GREEN), (4.0, 6.9, "MEDIUM", "4.0–6.9", AMBER), (7.0, 8.9, "HIGH", "7.0–8.9", ORANGE), (9.0, 10.0, "CRITICAL", "9.0–10", DARKRED)]
    for lo, hi, n, r, c in segs:
        x0 = 60 + lo * 74; x1 = 60 + hi * 74
        s.rect(x0, 258, x1 - x0, 48, c, c, 4)
        s.ctext((x0 + x1) / 2, 276, n, 11.5, WHITE, "bold"); s.ctext((x0 + x1) / 2, 293, r, 10.5, WHITE)
    s.text(60, 330, "0.0 = none", 10.5, MUTE)
    s.line(800, 310, 800, 322, DARKRED, 2); s.text(800, 340, "Log4Shell: 10.0", 11.5, DARKRED, "bold", "end")
    s.text(430, 372, "CVE is an instance, CWE is the category, CVSS is the severity.", 12.5, INK, "bold", "middle")
    s.save("14-cwe-cve-cvss")


# --------------------------------------------------------------------------- week 3
def d15():
    s = S(905, 502, "OWASP Top 10 (2025) at a glance", "Memorize the names; know one fix for each")
    t = [("A01", "Broken Access Control", "Users do or see what they should not (IDOR, SSRF).", "Check permissions on the server, every request.", False),
         ("A02", "Security Misconfiguration", "Default passwords, open cloud buckets, debug mode on.", "Hardened, repeatable configuration.", False),
         ("A03", "Software Supply Chain Failures", "A poisoned dependency, build system or update.", "Pin, scan and verify what you depend on.", True),
         ("A04", "Cryptographic Failures", "No or weak encryption, leaked keys, weak hashing.", "TLS, strong algorithms, key management.", False),
         ("A05", "Injection", "Untrusted input runs as code (SQLi, XSS, command).", "Parameterized queries, output encoding.", False),
         ("A06", "Insecure Design", "The design itself is flawed, not a coding slip.", "Threat-model before you build.", False),
         ("A07", "Authentication Failures", "Weak login, credential stuffing, bad sessions.", "MFA, rate limiting, slow salted hashes.", False),
         ("A08", "Software or Data Integrity Failures", "Trusting unsigned code or data.", "Verify signatures and integrity.", False),
         ("A09", "Security Logging and Alerting Failures", "Attacks happen and nobody notices.", "Log security events, alert on anomalies.", False),
         ("A10", "Mishandling of Exceptional Conditions", "Errors handled badly; the system fails open.", "Fail closed; handle every error path.", True)]
    for i, (n, nm, what, fix, new) in enumerate(t):
        x = 20 + (i % 5) * 175; y = 70 + (i // 5) * 205
        s.rect(x, y, 165, 195, WHITE, NAVY, 10)
        s.p.append(f'<path d="M{x},{y+68} L{x},{y+10} Q{x},{y} {x+10},{y} L{x+155},{y} Q{x+165},{y} {x+165},{y+10} L{x+165},{y+68} Z" fill="{NAVY}"/>')
        s.text(x + 10, y + 17, n, 12, "#9fd3dc", "bold")
        s.text(x + 10, y + 34, nm, 11.5, WHITE, "bold", width=145, lh=1.2)
        if new:
            s.pill(x + 135, y + 12, "NEW", AMBER, size=9)
        s.text(x + 10, y + 90, what, 11, INK, width=145, lh=1.3)
        s.rect(x + 6, y + 138, 153, 51, MINT, GREEN, 6)
        s.text(x + 12, y + 153, "FIX: " + fix, 10.5, GREEN, "bold", width=141, lh=1.25)
    s.text(20, 494, "2025 edition: SSRF was merged into A01. Source: top10.owasp.org/2025", 11, MUTE)
    s.save("15-owasp-top10")


def d16():
    s = S(860, 458, "SQL injection: why parameterized queries fix it")
    s.rect(15, 45, 830, 190, PINK, RED, 12); s.pill(150, 62, "UNSAFE: gluing strings together", RED, size=11)
    s.text(30, 100, "User types", 11.5, MUTE, "bold"); s.box(30, 108, 215, 46, "' OR '1'='1", WHITE, RED, INK, 13, font=MONO)
    s.arrow(247, 131, 277, 131, RED)
    s.text(280, 100, "Code builds the query", 11.5, MUTE, "bold")
    s.box(280, 108, 265, 66, '"SELECT * FROM users WHERE name = \'" + input + "\'"', WHITE, RED, INK, 11, font=MONO)
    s.arrow(547, 141, 577, 141, RED)
    s.text(580, 100, "Database receives", 11.5, MUTE, "bold")
    s.box(580, 108, 250, 66, "... WHERE name = ''\n    OR '1'='1'", WHITE, RED, INK, 11.5, font=MONO)
    s.text(30, 208, "The input changed the STRUCTURE of the query. '1'='1' is always true, so the database returns every row.", 12.5, RED, "bold", width=800)
    s.rect(15, 248, 830, 195, MINT, GREEN, 12); s.pill(150, 265, "SAFE: parameterized query", GREEN, size=11)
    s.text(30, 303, "User types", 11.5, MUTE, "bold"); s.box(30, 311, 215, 46, "' OR '1'='1", WHITE, GREEN, INK, 13, font=MONO)
    s.arrow(247, 334, 277, 334, GREEN)
    s.text(280, 303, "Code sends query and value separately", 11.5, MUTE, "bold")
    s.box(280, 311, 265, 66, "query: \"SELECT * FROM users WHERE name = ?\"\nvalue: input", WHITE, GREEN, INK, 11, font=MONO)
    s.arrow(547, 344, 577, 344, GREEN)
    s.text(580, 303, "Database receives", 11.5, MUTE, "bold")
    s.box(580, 311, 250, 66, "Query shape is FIXED.\nInput is only a value.", WHITE, GREEN, INK, 12, "bold")
    s.text(30, 411, "The database never parses the input as SQL. It looks for a user literally named ' OR '1'='1 and finds none.", 12.5, GREEN, "bold", width=800)
    s.save("16-sql-injection")


def d17():
    s = S(860, 530, "Stored XSS: the attacker's script runs in your visitors' browsers")
    s.lifelines([("Attacker", 130, RED), ("Website + database", 430, NAVY), ("Victim's browser", 730, TEAL)], 55, 435)
    s.msg(130, 130, 430, "1  posts a comment that contains a script", RED)
    s.box(310, 160, 240, 44, "2  Site stores it as-is (no output encoding)", SAND, AMBER, INK, 12)
    s.msg(245, 730, 430, "3  opens the page with the comments", NAVY)
    s.msg(295, 430, 730, "4  sends the page, including the attacker's script", RED)
    s.box(520, 325, 330, 56, "5  The browser runs the script as if the site itself wrote it. It can act as the victim on this site.", PINK, RED, INK, 12)
    s.rect(15, 452, 830, 62, MINT, GREEN, 10)
    s.ctext(430, 483, "Defenses:  encode output  ·  Content-Security-Policy  ·  HttpOnly cookies  ·  framework auto-escaping", 12.5, INK, "bold", width=800)
    s.save("17-xss-stored")


def d18():
    s = S(860, 530, "CSRF: the browser sends your cookie, even when you did not mean to")
    s.lifelines([("Victim's browser", 130, TEAL), ("Malicious page", 430, RED), ("Bank", 730, NAVY)], 55, 435)
    s.box(20, 112, 330, 44, "0  Victim is already logged in to the bank (cookie stored)", SKY, TEAL, INK, 12)
    s.msg(195, 130, 430, "1  visits a malicious page", NAVY)
    s.msg(245, 430, 130, "2  page holds a hidden request to bank.com", RED)
    s.msg(305, 130, 730, "3  browser sends it AND attaches the bank cookie automatically", RED)
    s.box(520, 325, 330, 50, "4  Bank sees a valid session and performs the action.", PINK, RED, INK, 12)
    s.tag(430, 405, "The victim never clicked anything on the bank's site.", 12, MUTE)
    s.rect(15, 452, 830, 62, MINT, GREEN, 10)
    s.ctext(430, 483, "Defenses:  anti-CSRF token  ·  SameSite cookies  ·  re-authenticate for sensitive actions", 12.5, INK, "bold", width=800)
    s.save("18-csrf")


def d19():
    s = S(860, 440, "IDOR: logged in does not mean allowed")
    s.rect(15, 45, 830, 190, PINK, RED, 12); s.pill(110, 62, "VULNERABLE", RED, size=11)
    s.box(30, 90, 130, 64, "Alice\n(user 1001)", NAVY, NAVY, WHITE, 13, "bold")
    s.arrow(162, 112, 328, 112, RED); s.text(245, 103, "GET /orders/1002", 12, INK, anchor="middle", font=MONO)
    s.text(245, 133, "(she edited the number)", 11, MUTE, anchor="middle")
    s.box(330, 86, 200, 76, "Server asks only:\n\"is the user logged in?\"\nYES", WHITE, RED, INK, 12)
    s.arrow(532, 124, 628, 124, RED)
    s.box(630, 90, 200, 68, "Returns Bob's order\n(private data leaked)", RED, RED, WHITE, 12.5, "bold")
    s.text(30, 205, "Authentication passed, but authorization was never checked.", 12.5, RED, "bold")
    s.rect(15, 250, 830, 180, MINT, GREEN, 12); s.pill(90, 267, "FIXED", GREEN, size=11)
    s.box(30, 295, 130, 64, "Alice\n(user 1001)", NAVY, NAVY, WHITE, 13, "bold")
    s.arrow(162, 317, 328, 317, GREEN); s.text(245, 308, "GET /orders/1002", 12, INK, anchor="middle", font=MONO)
    s.box(330, 288, 200, 78, "Server also asks:\n\"does order 1002 belong\nto Alice?\"  NO", WHITE, GREEN, INK, 12)
    s.arrow(532, 327, 628, 327, GREEN)
    s.box(630, 295, 200, 64, "403 Forbidden", GREEN, GREEN, WHITE, 13, "bold")
    s.text(30, 400, "Check ownership on the server for every object and every request. Hard-to-guess IDs are not a fix.", 12.5, GREEN, "bold", width=800)
    s.save("19-idor")


def d20():
    s = S(860, 478, "SSRF: tricking the server into making requests for you")
    s.rect(15, 60, 250, 290, GREY, MUTE, 12, dash=True); s.text(140, 82, "Internet", 12, MUTE, "bold", "middle")
    s.rect(285, 60, 270, 290, SKY, TEAL, 12, dash=True); s.text(420, 82, "Your public web app", 12, TEAL, "bold", "middle")
    s.rect(575, 60, 270, 290, SAND, AMBER, 12, dash=True); s.text(710, 82, "Internal network (unreachable from outside)", 11, AMBER, "bold", "middle", width=250)
    s.box(40, 175, 200, 70, "Attacker", RED, RED, WHITE, 14, "bold")
    s.box(305, 150, 230, 120, "Feature: \"give me a URL and I will fetch a preview\"\n(the SERVER makes the request)", WHITE, TEAL, INK, 12)
    s.box(595, 150, 230, 120, "Internal admin panel or\ncloud metadata service\n(169.254.169.254)", WHITE, AMBER, INK, 12)
    s.path("M140,173 V112 H710 V148", RED, dash=True); s.tag(425, 112, "✗ direct access blocked by the firewall", 11.5, RED, "bold")
    s.arrow(242, 195, 303, 195, RED); s.pill(272, 180, "1", RED)
    s.arrow(537, 205, 593, 205, RED); s.pill(565, 190, "2", RED)
    s.arrow(593, 235, 537, 235, RED, dash=True); s.arrow(303, 235, 242, 235, RED, dash=True); s.pill(272, 252, "3", RED)
    s.text(20, 374, "1  The attacker submits an internal URL.\n2  The server, which IS trusted inside, fetches it.\n3  The answer comes back to the attacker.", 11.5, INK, lh=1.35)
    s.rect(15, 425, 830, 40, MINT, GREEN, 10)
    s.ctext(430, 445, "Defenses:  allowlist destinations  ·  block private and link-local IPs  ·  never fetch raw user URLs  ·  protect the metadata service", 11.5, INK, "bold", width=810)
    s.save("20-ssrf")


# --------------------------------------------------------------------------- week 4
def d21():
    s = S(880, 435, "Defense in depth: who sits where", "Each layer catches what the previous one cannot")
    it = [(20, "Internet", GREY, MUTE, "Anyone, including attackers."),
          (190, "Firewall", MINT, GREEN, "Allows or blocks by IP address and port. Cannot read HTTP content."),
          (360, "IPS", MINT, GREEN, "Sits in the path. Detects attacks AND blocks them."),
          (530, "WAF", MINT, GREEN, "Understands HTTP. Blocks SQLi and XSS patterns."),
          (700, "Web server", SKY, TEAL, "")]
    for x, nm, f, c, d in it:
        s.box(x, 90, 150, 60, nm, f, c, INK, 14, "bold")
        s.text(x + 75, 172, d, 11, MUTE, anchor="middle", width=146)
    for a, b in ((170, 190), (340, 360), (510, 530), (680, 700)):
        s.arrow(a + 1, 120, b - 1, 120, NAVY)
    s.text(765, 172, "Your code.\nIt must be\nsecure too!", 11, MUTE, anchor="end")
    s.line(350, 120, 350, 262, AMBER, 2, True)
    s.box(275, 262, 150, 56, "IDS", MINT, GREEN, INK, 14, "bold")
    s.text(350, 338, "Watches a COPY of the traffic.\nAlerts only; does not block.", 11, MUTE, anchor="middle")
    s.box(40, 262, 150, 56, "Security team\n(gets the alert)", SAND, AMBER, INK, 12)
    s.arrow(273, 290, 192, 290, AMBER, dash=True)
    s.arrow(775, 152, 775, 262, NAVY)
    s.box(700, 262, 150, 56, "Database\n(private network only)", SKY, TEAL, INK, 12)
    s.rect(15, 378, 850, 42, SAND, AMBER, 10)
    s.ctext(440, 399, "Layers overlap on purpose: if one fails, the next still protects you. That is defense in depth.", 12.5, INK, "bold")
    s.save("21-defense-in-depth")


def d22():
    s = S(860, 430, "Man-in-the-middle (MITM)", "How the attacker gets in the middle: rogue Wi-Fi, ARP spoofing, DNS spoofing")
    s.rect(15, 70, 830, 165, PINK, RED, 12); s.pill(110, 88, "WITHOUT TLS", RED)
    s.box(35, 120, 130, 60, "Victim", NAVY, NAVY, WHITE, 13, "bold")
    s.box(365, 120, 130, 60, "Attacker", RED, RED, WHITE, 13, "bold")
    s.box(695, 120, 130, 60, "Server", NAVY, NAVY, WHITE, 13, "bold")
    s.arrow(167, 138, 363, 138, RED); s.arrow(497, 138, 693, 138, RED)
    s.arrow(363, 166, 167, 166, RED, dash=True); s.arrow(693, 166, 497, 166, RED, dash=True)
    s.text(265, 128, "password=hunter2", 11, RED, anchor="middle", font=MONO); s.text(595, 128, "password=hunter2", 11, RED, anchor="middle", font=MONO)
    s.text(430, 214, "The attacker reads and can change everything, in plain text.", 12.5, RED, "bold", "middle")
    s.rect(15, 250, 830, 165, MINT, GREEN, 12); s.pill(95, 268, "WITH TLS", GREEN)
    s.box(35, 300, 130, 60, "Victim", NAVY, NAVY, WHITE, 13, "bold")
    s.box(365, 300, 130, 60, "Attacker", GREY, MUTE, INK, 13, "bold")
    s.box(695, 300, 130, 60, "Server", NAVY, NAVY, WHITE, 13, "bold")
    s.arrow(167, 330, 363, 330, GREEN, tail=True); s.arrow(497, 330, 693, 330, GREEN, tail=True)
    s.text(265, 320, "x9f#a1…", 11.5, GREEN, anchor="middle", font=MONO); s.text(595, 320, "x9f#a1…", 11.5, GREEN, anchor="middle", font=MONO)
    s.text(430, 385, "The attacker sees only scrambled bytes. A fake certificate makes the browser show a warning.", 12.5, GREEN, "bold", "middle", width=800)
    s.save("22-mitm")


def d23():
    md5 = hashlib.md5(b"password123").hexdigest()
    s = S(860, 495, "How to store passwords (and how not to)")
    rows = [("1  Plaintext", RED, PINK, "password123", "password123", "A leak is instant disaster. Anyone with database access reads every password."),
            ("2  Fast hash, no salt\n(MD5, SHA-1)", ORANGE, SAND, md5[:20] + "…", md5[:20] + "…", "Same password gives the same hash. Rainbow tables and GPUs crack billions per second."),
            ("3  Salted slow hash\n(bcrypt, scrypt, Argon2)", GREEN, MINT, "$2b$12$Qk7Lm…9aXe", "$2b$12$Zp1Rt…m4Tu", "Different hash for the same password, and every guess is deliberately expensive.")]
    for i, (lab, c, f, a, b, v) in enumerate(rows):
        y = 50 + i * 128
        s.rect(15, y, 830, 116, f, c, 10)
        s.box(28, y + 18, 190, 80, lab, c, c, WHITE, 12.5, "bold")
        s.text(240, y + 30, "user", 10.5, MUTE, "bold"); s.text(320, y + 30, "stored in the database", 10.5, MUTE, "bold")
        s.text(240, y + 55, "alice", 12, INK, font=MONO); s.text(320, y + 55, a, 11.5, INK, font=MONO)
        s.text(240, y + 80, "bob", 12, INK, font=MONO); s.text(320, y + 80, b, 11.5, INK, font=MONO)
        s.text(560, y + 28, "both chose \"password123\"" if i != 0 else "both chose the same password", 10.5, MUTE, "bold")
        s.text(560, y + 50, v, 12, c, "bold", width=270)
    s.text(20, 440, "Real case: LinkedIn (2012) stored unsalted SHA-1 hashes. About 117 million credentials surfaced in 2016, and many were cracked quickly.", 11.5, INK, width=820)
    s.text(20, 480, "Rule: never encrypt passwords (keys get stolen) and never use a fast hash. Use a slow, salted password hash.", 12, GREEN, "bold", width=820)
    s.save("23-password-storage")


def d24():
    s = S(860, 330, "Incident response in five steps", "If you suspect a breach, say these out loud in this order")
    st = [("1  IDENTIFY", "Is it real? How big is it? What is affected?", NAVY), ("2  CONTAIN", "Isolate systems, revoke credentials, stop the spread.", RED),
          ("3  ERADICATE", "Remove the cause: malware, rogue account, vulnerable code.", AMBER), ("4  RECOVER", "Restore from clean backups; monitor closely.", GREEN),
          ("5  LEARN", "Blameless post-mortem; fix the root cause.", TEAL)]
    for i, (t, b, c) in enumerate(st):
        x = 20 + i * 167
        s.card(x, 75, 152, 130, t, b, c, hh=34, size=12)
        if i < 4:
            s.arrow(x + 154, 140, x + 165, 140, MUTE)
    s.path("M772,207 V240 H96 V209", TEAL, dash=True)
    s.tag(434, 240, "what you learn improves the next response", 11.5, TEAL, "bold")
    s.rect(20, 268, 825, 42, SAND, AMBER, 10)
    s.ctext(432, 289, "Before anything happens: logging, backups, runbooks, and a named person on call. Preserve evidence; do not just reboot everything.", 12, INK, "bold", width=800)
    s.save("24-incident-response")


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for f in (d01, d02, d03, d04, d05, d06, d07, d08, d09, d10, d11, d12, d13, d14, d15, d16, d17, d18, d19, d20, d21, d22, d23, d24):
        f()
    print("wrote", len([n for n in os.listdir(OUT) if n.endswith(".svg")]), "diagrams to", os.path.abspath(OUT))
