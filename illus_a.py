"""Story illustrations, part A: the four LEAD pictures (21 Nov 2026 edition).

ILLUS_A maps story id -> fn(w, h) -> one self-contained inline <svg> string.
All leads use a fixed 243x116 viewBox (xMidYMid slice). The bottom 16 units are
covered by build.py's caption band, so key content stays above y=100.
Standard library only, fully deterministic.
"""
import math

INK = "#1d1a22"
FONT = 'font-family="Barlow Condensed, Arial Narrow, sans-serif" font-weight="700"'
VW, VH = 243, 116


# ------------------------------------------------------------------ helpers
def _svg(w, h, defs, body):
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d" '
            'preserveAspectRatio="xMidYMid slice"><defs>%s</defs>%s</svg>'
            % (w, h, VW, VH, defs, body))


def _lg(gid, stops, x2=0, y2=1):
    s = "".join('<stop offset="%s" stop-color="%s"/>' % (o, c) for o, c in stops)
    return '<linearGradient id="%s" x1="0" y1="0" x2="%s" y2="%s">%s</linearGradient>' % (gid, x2, y2, s)


def _rg(gid, stops):
    s = "".join('<stop offset="%s" stop-color="%s" stop-opacity="%s"/>' % (o, c, a) for o, c, a in stops)
    return '<radialGradient id="%s">%s</radialGradient>' % (gid, s)


def _label(x, y, text, size=13, fill="#fff", bg=INK, anchor="start"):
    """Caps label on a solid tag so it stays legible over any art."""
    wpx = len(text) * size * 0.5 + 9
    bx = x - 4 if anchor == "start" else (x - wpx / 2 if anchor == "middle" else x - wpx + 4)
    return ('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="2" fill="%s"/>'
            '<text x="%.1f" y="%.1f" %s font-size="%d" fill="%s" text-anchor="%s" '
            'letter-spacing="0.4">%s</text>'
            % (bx, y - size + 1, wpx, size + 3, bg, x, y, FONT, size, fill, anchor, text))


def _smoke(cx, cy, puffs, col="#5a5560", op=0.85):
    out = []
    for i, (dx, dy, r) in enumerate(puffs):
        out.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" opacity="%.2f"/>'
                   % (cx + dx, cy + dy, r, col, op - i * 0.06))
    return "".join(out)


def _flames(x, y, s=1.0):
    return ('<path d="M%.1f %.1f q%.1f %.1f %.1f %.1f q%.1f %.1f %.1f %.1f q%.1f %.1f %.1f %.1f '
            'q%.1f %.1f %.1f %.1f z" fill="#e8562a"/>'
            '<path d="M%.1f %.1f q%.1f %.1f %.1f %.1f q%.1f %.1f %.1f %.1f q%.1f %.1f %.1f %.1f z" fill="#ffc23a"/>'
            % (x, y, -2 * s, -6 * s, 1 * s, -12 * s, 1 * s, 4 * s, 3 * s, 3 * s,
               0, -5 * s, 3 * s, -9 * s, 3 * s, 7 * s, 0, 12 * s,
               x + 1.5 * s, y, -1 * s, -4 * s, 1 * s, -7 * s, 1 * s, 3 * s, 2 * s, 2 * s, 1 * s, 3 * s, 0, 5 * s))


def _drone(x, y, s=1.0):
    """Small delta-wing loitering-drone silhouette heading right/down."""
    return ('<g transform="translate(%.1f %.1f) scale(%.2f) rotate(14)">'
            '<path d="M9 0 L-5 -1.6 L-8 -1.2 L-8 1.2 L-5 1.6 Z" fill="%s"/>'
            '<path d="M4 -1 L-4 -10 L-6 -10 L-3 -1 Z M4 1 L-4 10 L-6 10 L-3 1 Z" fill="%s"/>'
            '<path d="M-6 -1 L-9 -4 M-6 1 L-9 4" stroke="%s" stroke-width="1.2"/></g>' % (x, y, s, INK, INK, INK))


# ------------------------------------------------------------- gulf-finland-ship
def gulf_finland_ship(w, h):
    p = "gfs"
    defs = (_lg(p + "sky", [("0", "#8d97a3"), ("0.6", "#c9c3b8"), ("1", "#e4d6c0")])
            + _lg(p + "sea", [("0", "#6b7883"), ("1", "#3f4b56")])
            + _rg(p + "glow", [("0", "#ffb347", "0.75"), ("1", "#ffb347", "0")]))
    b = ['<rect width="243" height="116" fill="url(#%ssky)"/>' % p,
         # distant Finnish shore with pines
         '<path d="M0 66 L30 62 L60 64 L95 60 L120 63 L120 67 L0 67 Z" fill="#5d6a62"/>']
    for i in range(9):
        x = 6 + i * 12
        b.append('<path d="M%d 63 l3 -8 l3 8 z" fill="#46544b"/>' % x)
    b.append('<rect y="66" width="243" height="50" fill="url(#%ssea)"/>' % p)
    for y, x0 in ((74, 10), (82, 150), (90, 40), (96, 190), (86, 100)):
        b.append('<path d="M%d %d h22" stroke="#8a97a0" stroke-width="1" opacity="0.6"/>' % (x0, y))
    # smoke column drifting left/up from ship
    b.append(_smoke(150, 48, [(0, 0, 9), (-8, -10, 11), (-20, -18, 12), (-36, -24, 13), (-54, -28, 12),
                              (-72, -30, 10)], "#4a4650", 0.9))
    b.append('<circle cx="150" cy="60" r="26" fill="url(#%sglow)"/>' % p)
    # cargo ship hull (bow to the right)
    b.append('<path d="M108 70 L208 70 L200 86 L114 86 Z" fill="#7b2e2a" stroke="%s" stroke-width="1.6"/>' % INK)
    b.append('<path d="M110 74 L206 74" stroke="#d9d2c4" stroke-width="1.2"/>')
    # containers
    cols = ["#b5532d", "#4f6b8a", "#c9a23a", "#5f7f5a", "#8a4a3a"]
    for i in range(5):
        b.append('<rect x="%d" y="62" width="13" height="8" fill="%s" stroke="%s" stroke-width="0.8"/>'
                 % (140 + i * 13, cols[i], INK))
    for i in range(3):
        b.append('<rect x="%d" y="54" width="13" height="8" fill="%s" stroke="%s" stroke-width="0.8"/>'
                 % (153 + i * 13, cols[(i + 2) % 5], INK))
    # superstructure at stern
    b.append('<rect x="114" y="52" width="20" height="18" fill="#e6e0d4" stroke="%s" stroke-width="1.4"/>' % INK)
    b.append('<rect x="117" y="56" width="14" height="3" fill="%s"/>' % INK)
    b.append('<rect x="122" y="44" width="5" height="8" fill="#3a3a40" stroke="%s" stroke-width="1"/>' % INK)
    # fire on deck
    b.append(_flames(146, 62, 1.1))
    b.append(_flames(160, 54, 0.9))
    b.append('<path d="M108 86 Q160 90 208 86" stroke="#c8d0d6" stroke-width="1" fill="none" opacity="0.6"/>')
    # Finnish coast guard patrol boat (left foreground)
    b.append('<path d="M22 84 L82 84 L76 95 L28 95 Z" fill="#eeeae2" stroke="%s" stroke-width="1.6"/>' % INK)
    b.append('<path d="M28 89 L80 89" stroke="#c0392b" stroke-width="2.2"/>')
    b.append('<path d="M32 89 L37 89" stroke="#1f4e9c" stroke-width="2.2"/>')
    b.append('<rect x="40" y="75" width="22" height="9" fill="#eeeae2" stroke="%s" stroke-width="1.4"/>' % INK)
    b.append('<rect x="43" y="77" width="16" height="3" fill="%s"/>' % INK)
    b.append('<path d="M52 75 V66" stroke="%s" stroke-width="1.2"/>' % INK)
    # Finnish flag on stern staff
    b.append('<path d="M27 84 V70" stroke="%s" stroke-width="1"/>' % INK)
    b.append('<g transform="translate(27 70)"><rect width="14" height="9" fill="#fff" stroke="%s" stroke-width="0.6"/>'
             '<rect x="4" width="2.6" height="9" fill="#18458f"/><rect y="3.2" width="14" height="2.6" fill="#18458f"/></g>'
             % INK)
    b.append('<path d="M84 90 Q95 92 104 90" stroke="#dfe5ea" stroke-width="1" fill="none"/>')
    # two drones
    b.append(_drone(194, 18, 1.2))
    b.append(_drone(218, 32, 1.1))
    b.append('<path d="M188 14 l-12 -3 M206 26 l-12 -3" stroke="#fff" stroke-width="0.8" opacity="0.7"/>')
    b.append(_label(10, 20, "SPARTA II", 14))
    return _svg(w, h, defs, "".join(b))


# ---------------------------------------------------------- hormuz-tanker-strikes
def _tanker(x, y, s, hull="#3c4a5a"):
    t = ('<g transform="translate(%.1f %.1f) scale(%.2f)">'
         '<path d="M0 0 L70 0 L64 10 L4 10 Z" fill="%s" stroke="%s" stroke-width="1.6"/>'
         '<path d="M2 3 H68" stroke="#a33a2a" stroke-width="2"/>'
         '<rect x="16" y="-2" width="44" height="2" fill="#7d8790"/>'
         '<path d="M22 -2 V-5 M32 -2 V-5 M42 -2 V-5 M52 -2 V-5" stroke="%s" stroke-width="1"/>'
         '<rect x="3" y="-11" width="11" height="11" fill="#ece6da" stroke="%s" stroke-width="1.3"/>'
         '<rect x="5" y="-8" width="7" height="2" fill="%s"/>'
         '<rect x="7" y="-16" width="3.5" height="5" fill="#b8862b" stroke="%s" stroke-width="0.8"/>'
         '</g>') % (x, y, s, hull, INK, INK, INK, INK, INK)
    return t


def hormuz_tanker_strikes(w, h):
    p = "hts"
    defs = (_lg(p + "sky", [("0", "#5b5a7d"), ("0.45", "#d98a6a"), ("0.8", "#f3c27f"), ("1", "#f7dca5")])
            + _lg(p + "sea", [("0", "#c68a6a"), ("0.25", "#4d6f86"), ("1", "#2c4659")])
            + _rg(p + "sun", [("0", "#fff2c4", "1"), ("0.5", "#ffd27a", "0.8"), ("1", "#ffd27a", "0")]))
    b = ['<rect width="243" height="116" fill="url(#%ssky)"/>' % p,
         '<circle cx="128" cy="56" r="20" fill="url(#%ssun)"/>' % p,
         '<circle cx="128" cy="57" r="6" fill="#fff0c0"/>',
         '<rect y="56" width="243" height="60" fill="url(#%ssea)"/>' % p]
    # Iranian coast top-left/back, Omani Musandam rocky coast right-front
    b.append('<path d="M0 56 L0 34 L14 30 L26 36 L40 28 L58 38 L76 40 L96 50 L112 56 Z" '
             'fill="#7a5a4a" stroke="%s" stroke-width="1.2"/>' % INK)
    b.append('<path d="M14 30 L22 40 M40 28 L46 42 M58 38 L64 48" stroke="#5c4236" stroke-width="1"/>')
    b.append('<path d="M243 100 L243 44 L230 40 L214 50 L200 48 L186 60 L174 66 L166 76 L176 86 L196 92 L220 100 Z" '
             'fill="#8b6a52" stroke="%s" stroke-width="1.4"/>' % INK)
    b.append('<path d="M230 40 L222 60 M200 48 L204 66 M186 60 L194 76" stroke="#684c3a" stroke-width="1"/>')
    for x0, y0 in ((60, 64), (20, 78), (120, 90), (90, 72)):
        b.append('<path d="M%d %d h18" stroke="#f3c890" stroke-width="0.9" opacity="0.5"/>' % (x0, y0))
    # far tanker (hit at stern, smoke)
    b.append(_smoke(98, 58, [(0, 0, 5), (-5, -7, 6), (-12, -13, 7), (-21, -17, 7), (-31, -19, 6)], "#3a3438", 0.9))
    b.append(_tanker(96, 64, 0.8, "#3c4a5a"))
    b.append(_flames(99, 64, 0.7))
    # near tanker
    b.append(_tanker(20, 86, 1.25, "#2f3c4c"))
    for x0, y0 in ((18, 97), (96, 73)):
        b.append('<path d="M%d %d q-10 2 -20 0" stroke="#e8eef2" stroke-width="1" fill="none" opacity="0.7"/>'
                 % (x0, y0))
    # target ring on the struck tanker
    b.append('<circle cx="102" cy="60" r="13" fill="none" stroke="#a3271d" stroke-width="1.4" stroke-dasharray="3 2"/>')
    b.append(_label(8, 18, "STRAIT OF HORMUZ", 13))
    b.append(_label(122, 44, "2 HITS", 13, bg="#a3271d"))
    return _svg(w, h, defs, "".join(b))


# ------------------------------------------------------------ meza-flores-confirm
def _soldier(x, y, s=1.0, face=1):
    """Olive-uniformed soldier, simple silhouette; face=1 walks right."""
    return ('<g transform="translate(%.1f %.1f) scale(%.2f %.2f)">'
            '<path d="M-3 0 L-4 -11 L4 -11 L3 0 Z" fill="#4f5a32" stroke="%s" stroke-width="1"/>'
            '<path d="M-3 0 L-5 9 M3 0 L5 9" stroke="#4f5a32" stroke-width="3" stroke-linecap="round"/>'
            '<path d="M-5 9 h3 M5 9 h-3" stroke="%s" stroke-width="2"/>'
            '<path d="M-5 -24 L-6 -11 L6 -11 L5 -24 Z" fill="#5c6a3a" stroke="%s" stroke-width="1.2"/>'
            '<circle cx="0" cy="-28" r="3.6" fill="#b07a55" stroke="%s" stroke-width="0.8"/>'
            '<path d="M-4.4 -29 Q0 -35 4.4 -29 Z" fill="#3d4628" stroke="%s" stroke-width="0.8"/>'
            '<path d="M4 -21 L12 -17" stroke="%s" stroke-width="2.2"/>'
            '</g>') % (x, y, face * s, s, INK, INK, INK, INK, INK, INK)


def meza_flores_confirm(w, h):
    p = "mfc"
    defs = (_lg(p + "sky", [("0", "#9cc3d6"), ("1", "#efdcb3")])
            + _lg(p + "gnd", [("0", "#d8b37c"), ("1", "#b98c55")]))
    b = ['<rect width="243" height="116" fill="url(#%ssky)"/>' % p,
         '<path d="M0 64 L30 54 L60 60 L92 50 L130 58 L170 48 L210 56 L243 52 L243 68 L0 68 Z" fill="#a8a07a"/>',
         '<rect y="66" width="243" height="50" fill="url(#%sgnd)"/>' % p]
    # dust
    for cx, cy, r in ((170, 92, 10), (190, 88, 8), (205, 94, 9), (150, 95, 6)):
        b.append('<ellipse cx="%d" cy="%d" rx="%d" ry="%.1f" fill="#e9d3a6" opacity="0.7"/>' % (cx, cy, r, r * 0.45))
    # helicopter (right)
    hx, hy = 186, 70
    b.append('<g transform="translate(%d %d)">' % (hx, hy)
             + '<path d="M-28 -4 Q-28 -18 -10 -18 L14 -18 Q22 -18 22 -8 L22 4 L-24 4 Q-28 4 -28 -4 Z" '
               'fill="#56603a" stroke="%s" stroke-width="1.6"/>' % INK
             + '<path d="M-26 -8 Q-25 -15 -14 -15 L-14 -6 Z" fill="#a9c6d4" stroke="%s" stroke-width="1"/>' % INK
             + '<rect x="-8" y="-14" width="14" height="14" fill="#2b2f22" stroke="%s" stroke-width="1"/>' % INK
             + '<path d="M22 -12 L52 -16 L52 -11 L22 -4 Z" fill="#56603a" stroke="%s" stroke-width="1.4"/>' % INK
             + '<path d="M50 -24 L54 -8" stroke="%s" stroke-width="1.6"/>' % INK
             + '<path d="M0 -18 V-23" stroke="%s" stroke-width="2"/>' % INK
             + '<path d="M-44 -24 L46 -22" stroke="%s" stroke-width="2.2"/>' % INK
             + '<path d="M-22 10 H18 M-16 4 V10 M12 4 V10" stroke="%s" stroke-width="1.6"/>' % INK
             + '</g>')
    # small Mexican flag on helicopter tail boom
    b.append('<g transform="translate(212 58)"><rect width="15" height="9" fill="#fff" stroke="%s" stroke-width="0.6"/>'
             '<rect width="5" height="9" fill="#006847"/><rect x="10" width="5" height="9" fill="#ce1126"/>'
             '<circle cx="7.5" cy="4.5" r="1.4" fill="#8a5a2b"/></g>' % INK)
    # escort group walking right toward helicopter
    b.append(_soldier(70, 88, 1.15))
    b.append(_soldier(130, 88, 1.15))
    # handcuffed detainee (white shirt, dark trousers, hands behind)
    b.append('<g transform="translate(100 88) scale(1.15)">'
             '<path d="M-3 0 L-5 9 M3 0 L5 9" stroke="#2c2c34" stroke-width="3" stroke-linecap="round"/>'
             '<path d="M-3 0 L-4 -11 L4 -11 L3 0 Z" fill="#2c2c34" stroke="%s" stroke-width="1"/>'
             '<path d="M-5 -24 L-6 -11 L6 -11 L5 -24 Z" fill="#f2efe8" stroke="%s" stroke-width="1.2"/>'
             '<circle cx="0" cy="-28" r="3.6" fill="#b07a55" stroke="%s" stroke-width="0.8"/>'
             '<path d="M-3.6 -29.5 Q0 -33.5 3.6 -29.5" fill="#2a2018"/>'
             '<path d="M-5 -21 L-8 -14" stroke="#f2efe8" stroke-width="2.6"/>'
             '<circle cx="-8" cy="-13" r="1.8" fill="none" stroke="#8a929a" stroke-width="1.2"/>'
             '<circle cx="-5.6" cy="-13" r="1.8" fill="none" stroke="#8a929a" stroke-width="1.2"/>'
             '</g>' % (INK, INK, INK))
    # soldiers' hands on detainee
    b.append('<path d="M84 64 L92 66 M116 66 L124 64" stroke="#5c6a3a" stroke-width="2.2"/>')
    # dust tracks
    b.append('<path d="M20 100 Q90 96 160 98" stroke="#c9a46a" stroke-width="1" fill="none" opacity="0.7"/>')
    b.append(_label(10, 22, "ARRESTED", 15, bg="#8e1b1b"))
    return _svg(w, h, defs, "".join(b))


# ---------------------------------------------------------------- banda-sea-quake
def banda_sea_quake(w, h):
    p = "bsq"
    defs = (_lg(p + "sea", [("0", "#bcd6dc"), ("1", "#8fb7c2")])
            + '<clipPath id="%sclip"><rect x="0" y="22" width="243" height="94"/></clipPath>' % p)
    b = ['<rect width="243" height="116" fill="url(#%ssea)"/>' % p]
    land = "#d9c79c"
    g = ['<g clip-path="url(#%sclip)">' % p]
    # epicentre in the Banda Sea (upper middle)
    ex, ey = 118, 40
    for i, r in enumerate((10, 22, 36, 52, 70)):
        g.append('<circle cx="%d" cy="%d" r="%d" fill="none" stroke="#a3271d" stroke-width="%.1f" opacity="%.2f"/>'
                 % (ex, ey, r, 1.8 - i * 0.2, 0.9 - i * 0.14))
    # Timor (long island, SW-NE)
    g.append('<path d="M40 70 Q60 62 86 58 Q104 54 118 52 Q124 53 120 57 Q100 64 80 68 Q60 74 44 76 Q36 74 40 70 Z" '
             'fill="%s" stroke="%s" stroke-width="1.4"/>' % (land, INK))
    # Banda arc islands to the north
    g.append('<path d="M150 30 q8 -3 14 0 q-6 4 -14 0 Z M30 36 q16 -4 30 -2 q-14 5 -30 2 Z" '
             'fill="%s" stroke="%s" stroke-width="1"/>' % (land, INK))
    # northern Australian coast (bottom)
    g.append('<path d="M0 116 L0 90 Q30 86 54 88 L70 80 Q84 74 98 80 L112 78 Q124 72 136 80 L150 84 '
             'Q170 80 186 86 L200 80 Q214 74 226 82 L243 84 L243 116 Z" '
             'fill="%s" stroke="%s" stroke-width="1.4"/>' % (land, INK))
    g.append('</g>')
    b.extend(g)
    # Darwin dot
    dx, dy = 112, 82
    b.append('<circle cx="%d" cy="%d" r="3.2" fill="%s" stroke="#fff" stroke-width="1"/>' % (dx, dy, INK))
    # epicentre star
    pts = []
    for k in range(10):
        r = 7 if k % 2 == 0 else 3
        a = -math.pi / 2 + k * math.pi / 5
        pts.append("%.1f,%.1f" % (ex + r * math.cos(a), ey + r * math.sin(a)))
    b.append('<polygon points="%s" fill="#e8562a" stroke="%s" stroke-width="1.2"/>' % (" ".join(pts), INK))
    # seismograph strip along top
    b.append('<rect x="0" y="0" width="243" height="20" fill="#f4efe4"/>')
    b.append('<path d="M0 20 H243" stroke="%s" stroke-width="1.2"/>' % INK)
    for x in range(0, 243, 20):
        b.append('<path d="M%d 0 V20" stroke="#d8cfbf" stroke-width="0.6"/>' % x)
    tr = []
    for i in range(0, 244, 2):
        d = abs(i - 140)
        amp = 8.5 * math.exp(-((i - 140) / 22.0) ** 2) if i >= 112 else 0.0
        amp = max(amp, 0.8) if i < 112 else max(amp, 0.8 + 3 * math.exp(-max(i - 140, 0) / 40.0))
        y = 10 + amp * (1 if (i // 2) % 2 == 0 else -1) * (0.6 + 0.4 * math.cos(d * 0.9))
        tr.append("%s%d %.1f" % ("M" if i == 0 else "L", i, y))
    b.append('<path d="%s" stroke="#a3271d" stroke-width="1.1" fill="none"/>' % " ".join(tr))
    b.append(_label(6, 16, "M6.8", 13, bg="#a3271d"))
    b.append(_label(dx + 8, dy + 13, "DARWIN", 12))
    return _svg(w, h, defs, "".join(b))


ILLUS_A = {
    "gulf-finland-ship": gulf_finland_ship,
    "hormuz-tanker-strikes": hormuz_tanker_strikes,
    "meza-flores-confirm": meza_flores_confirm,
    "banda-sea-quake": banda_sea_quake,
}
