#!/usr/bin/env python3
"""Shared helpers for drawing the book diagrams (SVG)."""
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


