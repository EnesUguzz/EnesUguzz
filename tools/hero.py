"""GitHub profil hero SVG'lerini uretir: A (olculu), B (gosterisli).

Kullanim: python hero.py ascii.txt <cikti_klasoru>
"""
import sys
from html import escape
from pathlib import Path

W, H = 1200, 420
MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, 'Liberation Mono', monospace"

PAL = {
    "dark": dict(bg="#0d1117", panel="#0b1018", border="#30363d", fg="#e6edf3", dim="#8b949e",
                 green="#3fb950", blue="#58a6ff", violet="#bc8cff", cyan="#39c5cf", bar="#161b22"),
    "light": dict(bg="#ffffff", panel="#f6f8fa", border="#d0d7de", fg="#1f2328", dim="#59636e",
                  green="#1a7f37", blue="#0969da", violet="#8250df", cyan="#1b7c83", bar="#eaeef2"),
}

TERM = [
    ("cmd", "whoami"),
    ("name", "Enes Uğuz · AI / ML Engineer · Istanbul"),
    ("cmd", "cat interests.txt"),
    ("out", "▸ Computer vision — training models on images"),
    ("out", "▸ Agentic AI — LLM agents, tool use, MCP"),
    ("out", "▸ New AI tech — try it, build with it, learn it"),
    ("cmd", "ls projects/"),
    ("dir", "image-to-3d-lrm/  masa-oyunlari/"),
    ("cursor", ""),
]


def nb(s):
    # SVG bastaki/ardisik bosluklari yutar; bolunmez bosluk hizayi korur
    return escape(s).replace(" ", " ")


def portrait(lines, p, fancy):
    fs, lh, cw = 11, 13, 6.62
    width = max(len(l) for l in lines) * cw
    x0 = (456 - width) / 2 + 8
    y0 = (H - len(lines) * lh) / 2 + 10
    move = ""
    if fancy:
        move = ('<animate attributeName="x1" values="0;300;0" dur="8s" repeatCount="indefinite"/>'
                '<animate attributeName="x2" values="456;756;456" dur="8s" repeatCount="indefinite"/>')
    out = [f'<linearGradient id="pg" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="456" y2="{H}">'
           f'<stop offset="0" stop-color="{p["cyan"]}"/><stop offset=".55" stop-color="{p["blue"]}"/>'
           f'<stop offset="1" stop-color="{p["violet"]}"/>{move}</linearGradient>']
    out.append(f'<g font-family="{MONO}" font-size="{fs}" fill="url(#pg)" xml:space="preserve">')
    for i, l in enumerate(lines):
        y = y0 + i * lh
        b = 0.15 + i * 0.035
        out.append(f'<text x="{x0:.1f}" y="{y:.1f}" opacity="0">{nb(l)}'
                   f'<animate attributeName="opacity" from="0" to="1" begin="{b:.2f}s" dur=".35s" fill="freeze"/></text>')
    out.append("</g>")
    if fancy:  # tarama cizgisi
        out.append(f'<rect x="0" y="-40" width="456" height="40" fill="url(#scan)" opacity=".55">'
                   f'<animate attributeName="y" values="-40;{H}" dur="4.5s" begin="1.4s" repeatCount="indefinite"/></rect>')
    return "\n".join(out)


def terminal(p, fancy):
    x, y, w, h = 492, 36, 672, 348
    fs, step, cw = 16, 28, 9.65
    o = []
    stroke = 'url(#shimmer)' if fancy else p["border"]
    o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{p["panel"]}" '
             f'stroke="{stroke}" stroke-width="{1.6 if fancy else 1}"/>')
    o.append(f'<path d="M{x} {y+14}a14 14 0 0 1 14-14h{w-28}a14 14 0 0 1 14 14v22h-{w}z" fill="{p["bar"]}"/>')
    for k, c in enumerate(("#ff5f57", "#febc2e", "#28c840")):
        o.append(f'<circle cx="{x+22+k*20}" cy="{y+18}" r="6" fill="{c}"/>')
    o.append(f'<text x="{x+w/2}" y="{y+23}" text-anchor="middle" font-family="{MONO}" font-size="13" '
             f'fill="{p["dim"]}">enes@istanbul: ~</text>')
    t = 0.5
    ty = y + 74
    o.append(f'<g font-family="{MONO}" font-size="{fs}" xml:space="preserve">')
    for i, (kind, txt) in enumerate(TERM):
        yy = ty + i * step
        tx = x + 28
        if kind in ("cmd", "cursor"):
            o.append(f'<text x="{tx}" y="{yy}" fill="{p["green"]}" opacity="0">❯'
                     f'<animate attributeName="opacity" to="1" begin="{t:.2f}s" dur=".01s" fill="freeze"/></text>')
            cx = tx + 2 * cw
            if kind == "cursor":
                o.append(f'<rect x="{cx}" y="{yy-14}" width="9" height="18" fill="{p["fg"]}" opacity="0">'
                         f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;.01;.5;.51" dur="1s" '
                         f'begin="{t:.2f}s" repeatCount="indefinite"/></rect>')
                break
            dur = max(0.25, len(txt) * 0.055)
            o.append(f'<clipPath id="c{i}"><rect x="{cx}" y="{yy-18}" width="0" height="24">'
                     f'<animate attributeName="width" from="0" to="{len(txt)*cw+2:.0f}" begin="{t:.2f}s" '
                     f'dur="{dur:.2f}s" fill="freeze" calcMode="discrete" '
                     f'values="{";".join(f"{k*cw:.0f}" for k in range(len(txt)+1))}"/></rect></clipPath>')
            o.append(f'<text x="{cx}" y="{yy}" fill="{p["fg"]}" clip-path="url(#c{i})">{nb(txt)}</text>')
            t += dur + 0.25
        else:
            col = {"name": p["fg"], "out": p["dim"], "dir": p["blue"]}[kind]
            weight = ' font-weight="700"' if kind == "name" else ""
            filt = ' filter="url(#glow)"' if (fancy and kind == "name" and p is PAL["dark"]) else ""
            o.append(f'<text x="{tx}" y="{yy}" fill="{col}"{weight}{filt} opacity="0">{nb(txt)}'
                     f'<animate attributeName="opacity" to="1" begin="{t:.2f}s" dur=".3s" fill="freeze"/></text>')
            t += 0.22
    o.append("</g>")
    return "\n".join(o)


def particles(p):
    import random
    rnd = random.Random(7)
    o = []
    for _ in range(26):
        cx, cy = rnd.uniform(10, W - 10), rnd.uniform(10, H - 10)
        r = rnd.uniform(0.8, 2.2)
        d = rnd.uniform(6, 14)
        c = rnd.choice([p["cyan"], p["blue"], p["violet"]])
        o.append(f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{r:.1f}" fill="{c}" opacity="0">'
                 f'<animate attributeName="cy" values="{cy:.0f};{cy-40:.0f}" dur="{d:.1f}s" repeatCount="indefinite"/>'
                 f'<animate attributeName="opacity" values="0;.7;0" dur="{d:.1f}s" repeatCount="indefinite"/></circle>')
    return "\n".join(o)


def build(lines, theme, fancy):
    p = PAL[theme]
    defs = [f'<linearGradient id="scan" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{p["cyan"]}" stop-opacity="0"/>'
            f'<stop offset="1" stop-color="{p["cyan"]}" stop-opacity=".25"/></linearGradient>',
            f'<linearGradient id="shimmer" gradientUnits="userSpaceOnUse" x1="492" y1="0" x2="1164" y2="0">'
            f'<stop offset="0" stop-color="{p["border"]}"/><stop offset=".5" stop-color="{p["blue"]}"/>'
            f'<stop offset="1" stop-color="{p["border"]}"/>'
            f'<animate attributeName="x1" values="-200;1200" dur="3.5s" repeatCount="indefinite"/>'
            f'<animate attributeName="x2" values="400;1800" dur="3.5s" repeatCount="indefinite"/></linearGradient>',
            '<filter id="glow" x="-10%" y="-50%" width="120%" height="200%"><feGaussianBlur stdDeviation="2.5" result="b">'
            '<animate attributeName="stdDeviation" values="1.2;3.5;1.2" dur="3s" repeatCount="indefinite"/></feGaussianBlur>'
            '<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>',
            f'<radialGradient id="aura" cx=".22" cy=".5" r=".5"><stop offset="0" stop-color="{p["blue"]}" stop-opacity=".16"/>'
            f'<stop offset="1" stop-color="{p["blue"]}" stop-opacity="0"/>'
            + ('<animate attributeName="r" values=".42;.55;.42" dur="6s" repeatCount="indefinite"/>' if fancy else '')
            + '</radialGradient>']
    body = [f'<rect width="{W}" height="{H}" rx="18" fill="{p["bg"]}"/>',
            f'<rect width="{W}" height="{H}" rx="18" fill="url(#aura)"/>']
    if fancy:
        body.append(particles(p))
    body.append(portrait(lines, p, fancy))
    body.append(terminal(p, fancy))
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
            f'role="img" aria-label="Enes Uğuz — AI / ML Engineer">\n<defs>{"".join(defs)}</defs>\n'
            + "\n".join(body) + "\n</svg>\n")


if __name__ == "__main__":
    rd = lambda f: Path(f).read_text(encoding="utf-8").rstrip("\n").split("\n")
    lines = {"dark": rd(sys.argv[1]), "light": rd(sys.argv[1].replace(".txt", "_light.txt"))}
    out = Path(sys.argv[2]); out.mkdir(exist_ok=True)
    for theme in ("dark", "light"):
        (out / f"hero-calm-{theme}.svg").write_text(build(lines[theme], theme, False), encoding="utf-8")
        (out / f"hero-bold-{theme}.svg").write_text(build(lines[theme], theme, True), encoding="utf-8")
    print("ok")
