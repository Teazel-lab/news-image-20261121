"""Story illustrations, part A (v2 layout, 21 Nov 2026 edition).

ILLUS_A maps story id -> fn(w, h) -> one self-contained inline <svg> string.
LEAD pictures use a fixed 325x132 viewBox (bottom 16 units sit under build.py's
caption band); SMALL pictures use 191x66 (bottom 15 units covered).
Labels are drawn at >= 13 viewBox units and are never scaled down.
Standard library only, fully deterministic.
"""
import math

INK = "#1d1a22"
FONT = 'font-family="Barlow Condensed, Arial Narrow, sans-serif" font-weight="700"'
LEAD = (325, 132)
SMALL = (191, 66)


# ------------------------------------------------------------------ helpers
def _svg(w, h, vb, defs, body):
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d" '
            'preserveAspectRatio="xMidYMid slice"><defs>%s</defs>%s</svg>'
            % (w, h, vb[0], vb[1], defs, body))


def _lg(gid, stops, x2=0, y2=1):
    s = "".join('<stop offset="%s" stop-color="%s"/>' % (o, c) for o, c in stops)
    return '<linearGradient id="%s" x1="0" y1="0" x2="%s" y2="%s">%s</linearGradient>' % (gid, x2, y2, s)


def _rg(gid, stops):
    s = "".join('<stop offset="%s" stop-color="%s" stop-opacity="%s"/>' % (o, c, a) for o, c, a in stops)
    return '<radialGradient id="%s">%s</radialGradient>' % (gid, s)


def _label(x, y, text, size=14, fill="#fff", bg=INK):
    """Caps label on a solid tag (left-aligned at x, baseline y)."""
    wpx = len(text) * size * 0.47 + 9
    return ('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="2" fill="%s"/>'
            '<text x="%.1f" y="%.1f" %s font-size="%d" fill="%s" letter-spacing="0.4">%s</text>'
            % (x - 4, y - size + 1, wpx, size + 3, bg, x, y, FONT, size, fill, text))


def _smoke(cx, cy, puffs, col="#4a4650", op=0.9):
    return "".join('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" opacity="%.2f"/>'
                   % (cx + dx, cy + dy, r, col, max(op - i * 0.05, 0.35))
                   for i, (dx, dy, r) in enumerate(puffs))


def _flames(x, y, s=1.0):
    """Flame tongue standing on point (x, y)."""
    return ('<g transform="translate(%.1f %.1f) scale(%.2f)">'
            '<path d="M-7 0 Q-9 -8 -4 -13 Q-4 -7 -1 -6 Q-2 -14 3 -20 Q3 -11 7 -8 Q9 -4 7 0 Z" '
            'fill="#e8562a" stroke="#8e2a14" stroke-width="0.8"/>'
            '<path d="M-4 0 Q-5 -5 -2 -8 Q-1 -4 1 -4 Q1 -9 3 -12 Q4 -6 5 -3 Q5 -1 4 0 Z" fill="#ffc23a"/>'
            '</g>') % (x, y, s)


def _drone(x, y, s=1.0):
    """Delta-wing loitering-drone silhouette heading right/down."""
    return ('<g transform="translate(%.1f %.1f) scale(%.2f) rotate(14)">'
            '<path d="M9 0 L-5 -1.6 L-8 -1.2 L-8 1.2 L-5 1.6 Z" fill="%s"/>'
            '<path d="M4 -1 L-4 -10 L-6 -10 L-3 -1 Z M4 1 L-4 10 L-6 10 L-3 1 Z" fill="%s"/>'
            '<path d="M-6 -1 L-9 -4 M-6 1 L-9 4" stroke="%s" stroke-width="1.2"/></g>' % (x, y, s, INK, INK, INK))


def _star(cx, cy, ro, ri, fill="#e8562a"):
    pts = []
    for k in range(10):
        r = ro if k % 2 == 0 else ri
        a = -math.pi / 2 + k * math.pi / 5
        pts.append("%.1f,%.1f" % (cx + r * math.cos(a), cy + r * math.sin(a)))
    return '<polygon points="%s" fill="%s" stroke="%s" stroke-width="1.2"/>' % (" ".join(pts), fill, INK)


# ------------------------------------------------------------- gulf-finland-ship
def gulf_finland_ship(w, h):
    p = "gfs"
    defs = (_lg(p + "sky", [("0", "#8a94a1"), ("0.6", "#c9c3b8"), ("1", "#e6d8c2")])
            + _lg(p + "sea", [("0", "#6b7883"), ("1", "#3c4853")])
            + _rg(p + "glow", [("0", "#ffb347", "0.8"), ("1", "#ffb347", "0")]))
    b = ['<rect width="325" height="132" fill="url(#%ssky)"/>' % p,
         '<path d="M0 70 L40 65 L80 67 L120 63 L150 66 L150 72 L0 72 Z" fill="#5d6a62"/>']
    for i in range(12):
        b.append('<path d="M%d 67 l3.5 -9 l3.5 9 z" fill="#46544b"/>' % (4 + i * 12))
    b.append('<rect y="71" width="325" height="61" fill="url(#%ssea)"/>' % p)
    for y, x0 in ((80, 12), (90, 250), (100, 60), (108, 280), (96, 150), (112, 120)):
        b.append('<path d="M%d %d h26" stroke="#8a97a0" stroke-width="1" opacity="0.6"/>' % (x0, y))
    # smoke column drifting up/left
    b.append(_smoke(206, 50, [(0, 0, 11), (-10, -12, 13), (-24, -22, 14), (-42, -30, 15), (-62, -35, 14),
                              (-84, -38, 12), (-104, -40, 10)], "#4a4650", 0.92))
    b.append('<circle cx="206" cy="66" r="34" fill="url(#%sglow)"/>' % p)
    # cargo ship (bow right)
    b.append('<path d="M150 78 L290 78 L279 98 L158 98 Z" fill="#7b2e2a" stroke="%s" stroke-width="1.8"/>' % INK)
    b.append('<path d="M153 83 H287" stroke="#d9d2c4" stroke-width="1.4"/>')
    cols = ["#b5532d", "#4f6b8a", "#c9a23a", "#5f7f5a", "#8a4a3a", "#4f6b8a"]
    for i in range(6):
        b.append('<rect x="%d" y="68" width="16" height="10" fill="%s" stroke="%s" stroke-width="0.9"/>'
                 % (188 + i * 16, cols[i], INK))
    for i in range(3):
        b.append('<rect x="%d" y="58" width="16" height="10" fill="%s" stroke="%s" stroke-width="0.9"/>'
                 % (220 + i * 16, cols[(i + 2) % 6], INK))
    b.append('<rect x="158" y="56" width="25" height="22" fill="#e6e0d4" stroke="%s" stroke-width="1.5"/>' % INK)
    b.append('<rect x="161" y="61" width="19" height="4" fill="%s"/>' % INK)
    b.append('<rect x="167" y="46" width="6" height="10" fill="#3a3a40" stroke="%s" stroke-width="1"/>' % INK)
    b.append(_flames(200, 69, 1.25))
    b.append(_flames(214, 59, 1.0))
    b.append('<path d="M150 98 Q220 103 290 98" stroke="#c8d0d6" stroke-width="1" fill="none" opacity="0.6"/>')
    # Finnish coast-guard boat, left foreground
    b.append('<path d="M28 98 L112 98 L104 112 L36 112 Z" fill="#eeeae2" stroke="%s" stroke-width="1.8"/>' % INK)
    b.append('<path d="M34 105 H108" stroke="#c0392b" stroke-width="2.6"/>')
    b.append('<path d="M40 105 H47" stroke="#1f4e9c" stroke-width="2.6"/>')
    b.append('<rect x="56" y="86" width="30" height="12" fill="#eeeae2" stroke="%s" stroke-width="1.5"/>' % INK)
    b.append('<rect x="60" y="89" width="22" height="4" fill="%s"/>' % INK)
    b.append('<path d="M72 86 V74" stroke="%s" stroke-width="1.4"/>' % INK)
    b.append('<path d="M34 98 V78" stroke="%s" stroke-width="1.2"/>' % INK)
    b.append('<g transform="translate(34 78)"><rect width="18" height="11" fill="#fff" stroke="%s" stroke-width="0.7"/>'
             '<rect x="5" width="3.2" height="11" fill="#18458f"/><rect y="3.9" width="18" height="3.2" fill="#18458f"/></g>'
             % INK)
    b.append('<path d="M115 106 Q130 108 144 106" stroke="#dfe5ea" stroke-width="1" fill="none"/>')
    # two drones closing from upper right
    b.append(_drone(262, 20, 1.45))
    b.append(_drone(296, 38, 1.3))
    b.append('<path d="M252 15 l-16 -4 M285 33 l-16 -4" stroke="#fff" stroke-width="0.9" opacity="0.75"/>')
    b.append(_label(10, 22, "SPARTA II", 16))
    return _svg(w, h, LEAD, defs, "".join(b))


# ------------------------------------------------------------- bahrain-sitra-fire
def _bahrain_flag(x, y):
    """Red flag, white hoist band with 5 white serration points."""
    fw, fh, band, depth = 28, 18, 8, 5
    pts = ["%d,%d" % (x, y), "%d,%d" % (x + band, y)]
    step = fh / 5.0
    for k in range(5):
        pts.append("%.1f,%.1f" % (x + band + depth, y + step * (k + 0.5)))
        pts.append("%.1f,%.1f" % (x + band, y + step * (k + 1)))
    pts.append("%d,%d" % (x, y + fh))
    return ('<rect x="%d" y="%d" width="%d" height="%d" fill="#ce1126" stroke="%s" stroke-width="0.8"/>'
            '<polygon points="%s" fill="#fff"/>'
            '<rect x="%d" y="%d" width="%d" height="%d" fill="none" stroke="%s" stroke-width="0.8"/>'
            % (x, y, fw, fh, INK, " ".join(pts), x, y, fw, fh, INK))


def bahrain_sitra_fire(w, h):
    p = "bsf"
    defs = (_lg(p + "sky", [("0", "#6d6a86"), ("0.5", "#d39276"), ("1", "#f2cf98")])
            + _lg(p + "sea", [("0", "#4f7a8c"), ("1", "#2b4a5a")])
            + _lg(p + "tank", [("0", "#f1ece2"), ("1", "#b9b2a4")], x2=1, y2=0)
            + _rg(p + "glow", [("0", "#ffb347", "0.85"), ("1", "#ffb347", "0")]))
    b = ['<rect width="325" height="132" fill="url(#%ssky)"/>' % p,
         '<rect y="82" width="325" height="50" fill="url(#%ssea)"/>' % p]
    for y, x0 in ((104, 20), (112, 230), (120, 90), (108, 280)):
        b.append('<path d="M%d %d h24" stroke="#9cbccb" stroke-width="1" opacity="0.6"/>' % (x0, y))
    # tall smoke column from the burning tank
    b.append(_smoke(150, 52, [(0, 0, 12), (-4, -14, 14), (-2, -28, 15), (-8, -42, 16), (-4, -56, 17),
                              (-12, -66, 17), (8, -66, 14)], "#3d3a42", 0.93))
    b.append('<circle cx="150" cy="68" r="34" fill="url(#%sglow)"/>' % p)
    # island platform
    b.append('<path d="M36 90 L60 80 L262 80 L290 90 L276 96 L50 96 Z" fill="#b9a47e" stroke="%s" stroke-width="1.6"/>'
             % INK)
    b.append('<path d="M50 96 L276 96 L272 100 L54 100 Z" fill="#8c7a5c"/>')
    # pipework rack
    for yy in (77, 74):
        b.append('<path d="M66 %d H262" stroke="#6b6458" stroke-width="2"/>' % yy)
    for xx in range(70, 262, 16):
        b.append('<path d="M%d 80 V72" stroke="%s" stroke-width="1"/>' % (xx, INK))
    # storage tanks
    for tx, tw, th in ((76, 34, 20), (128, 40, 24), (188, 34, 20)):
        b.append('<rect x="%d" y="%d" width="%d" height="%d" fill="url(#%stank)" stroke="%s" stroke-width="1.6"/>'
                 % (tx, 80 - th, tw, th, p, INK))
        b.append('<ellipse cx="%.1f" cy="%d" rx="%.1f" ry="3" fill="#ddd6c8" stroke="%s" stroke-width="1.2"/>'
                 % (tx + tw / 2.0, 80 - th, tw / 2.0, INK))
        b.append('<path d="M%d %d H%d" stroke="#9b9384" stroke-width="1"/>' % (tx, 80 - th / 2, tx + tw))
    # refinery stacks + cracking tower
    b.append('<rect x="234" y="34" width="7" height="46" fill="#cfc6b6" stroke="%s" stroke-width="1.4"/>' % INK)
    b.append('<path d="M234 42 h7 M234 50 h7" stroke="#b5332a" stroke-width="2"/>')
    b.append('<rect x="248" y="44" width="6" height="36" fill="#cfc6b6" stroke="%s" stroke-width="1.4"/>' % INK)
    b.append('<path d="M248 52 h6" stroke="#b5332a" stroke-width="2"/>')
    b.append('<rect x="222" y="54" width="8" height="26" rx="3" fill="#9c958a" stroke="%s" stroke-width="1.3"/>' % INK)
    b.append(_smoke(238, 30, [(0, 0, 3), (-4, -4, 4)], "#d7d1c6", 0.7))
    # fire on the middle tank
    b.append(_flames(140, 58, 1.2))
    b.append(_flames(156, 58, 1.0))
    # missile trail arriving from the north-east (upper right)
    b.append('<path d="M322 4 Q260 10 196 36" stroke="#f7f1e6" stroke-width="3" fill="none" opacity="0.75" '
             'stroke-linecap="round"/>')
    b.append('<path d="M322 4 Q260 10 196 36" stroke="#a99f92" stroke-width="1" fill="none" stroke-dasharray="3 3"/>')
    b.append('<g transform="translate(196 36) rotate(158)"><path d="M-6 -2 H6 L10 0 L6 2 H-6 Z M-6 -2 L-9 -5 M-6 2 L-9 5" '
             'fill="%s" stroke="%s" stroke-width="1.2"/></g>' % (INK, INK))
    # Bahrain flag on a pole at the west end of the island
    b.append('<path d="M50 88 V46" stroke="%s" stroke-width="1.6"/>' % INK)
    b.append(_bahrain_flag(51, 46))
    b.append(_label(10, 20, "SITRA, BAHRAIN", 15))
    b.append(_label(174, 70, "FIRE", 15, bg="#a3271d"))
    return _svg(w, h, LEAD, defs, "".join(b))


# ------------------------------------------------------------ meza-flores-confirm
def _soldier(x, y, s=1.0, face=1):
    """Olive-uniformed soldier with rifle; face=1 walks right."""
    return ('<g transform="translate(%.1f %.1f) scale(%.2f %.2f)">'
            '<path d="M-3 0 L-4 -11 L4 -11 L3 0 Z" fill="#4f5a32" stroke="%s" stroke-width="1"/>'
            '<path d="M-3 0 L-5 9 M3 0 L5 9" stroke="#4f5a32" stroke-width="3" stroke-linecap="round"/>'
            '<path d="M-5 9 h3 M5 9 h-3" stroke="%s" stroke-width="2"/>'
            '<path d="M-5 -24 L-6 -11 L6 -11 L5 -24 Z" fill="#5c6a3a" stroke="%s" stroke-width="1.2"/>'
            '<circle cx="0" cy="-28" r="3.6" fill="#b07a55" stroke="%s" stroke-width="0.8"/>'
            '<path d="M-4.6 -29 Q0 -35.5 4.6 -29 Z" fill="#3d4628" stroke="%s" stroke-width="0.8"/>'
            '<path d="M-4 -20 L10 -14" stroke="%s" stroke-width="2.2"/>'
            '</g>') % (x, y, face * s, s, INK, INK, INK, INK, INK, INK)


def meza_flores_confirm(w, h):
    p = "mfc"
    defs = (_lg(p + "sky", [("0", "#9cc3d6"), ("1", "#efdcb3")])
            + _lg(p + "gnd", [("0", "#d8b37c"), ("1", "#b98c55")]))
    b = ['<rect width="325" height="132" fill="url(#%ssky)"/>' % p,
         '<path d="M0 68 L40 56 L80 63 L122 52 L170 61 L220 50 L270 59 L325 52 L325 72 L0 72 Z" fill="#a8a07a"/>',
         '<rect y="70" width="325" height="62" fill="url(#%sgnd)"/>' % p,
         '<path d="M0 104 L325 92" stroke="#e2c896" stroke-width="7" opacity="0.55"/>']
    # dust kicked up by the rotor
    for cx, cy, r in ((216, 104, 16), (244, 100, 12), (268, 106, 14), (196, 108, 8)):
        b.append('<ellipse cx="%d" cy="%d" rx="%d" ry="%.1f" fill="#ecd7ab" opacity="0.75"/>' % (cx, cy, r, r * 0.45))
    # helicopter (right)
    b.append('<g transform="translate(246 86) scale(1.3)">'
             '<path d="M-28 -4 Q-28 -18 -10 -18 L14 -18 Q22 -18 22 -8 L22 4 L-24 4 Q-28 4 -28 -4 Z" '
             'fill="#56603a" stroke="%s" stroke-width="1.4"/>'
             '<path d="M-26 -8 Q-25 -15 -14 -15 L-14 -6 Z" fill="#a9c6d4" stroke="%s" stroke-width="1"/>'
             '<rect x="-9" y="-14" width="13" height="14" fill="#2b2f22" stroke="%s" stroke-width="1"/>'
             '<path d="M22 -12 L50 -15 L50 -10 L22 -4 Z" fill="#56603a" stroke="%s" stroke-width="1.2"/>'
             '<path d="M48 -22 L52 -7" stroke="%s" stroke-width="1.4"/>'
             '<path d="M0 -18 V-23" stroke="%s" stroke-width="2"/>'
             '<path d="M-40 -24 L40 -22" stroke="%s" stroke-width="2"/>'
             '<path d="M-22 10 H18 M-16 4 V10 M12 4 V10" stroke="%s" stroke-width="1.5"/>'
             '</g>' % ((INK,) * 8))
    # Mexican flag on a pole by the airstrip
    b.append('<path d="M24 102 V54" stroke="%s" stroke-width="1.6"/>' % INK)
    b.append('<g transform="translate(25 54)"><rect width="27" height="16" fill="#fff" stroke="%s" stroke-width="0.7"/>'
             '<rect width="9" height="16" fill="#006847"/><rect x="18" width="9" height="16" fill="#ce1126"/>'
             '<circle cx="13.5" cy="8" r="2.4" fill="#8a5a2b"/>'
             '<rect width="27" height="16" fill="none" stroke="%s" stroke-width="0.7"/></g>' % (INK, INK))
    # escort: soldier, detainee, soldier walking right to the helicopter
    gy, sc = 104, 1.4
    b.append(_soldier(88, gy, sc))
    b.append(_soldier(160, gy, sc))
    b.append('<g transform="translate(124 %d) scale(%.2f)">'
             '<path d="M-3 0 L-5 9 M3 0 L5 9" stroke="#2c2c34" stroke-width="3" stroke-linecap="round"/>'
             '<path d="M-3 0 L-4 -11 L4 -11 L3 0 Z" fill="#2c2c34" stroke="%s" stroke-width="1"/>'
             '<path d="M-5 -24 L-6 -11 L6 -11 L5 -24 Z" fill="#f2efe8" stroke="%s" stroke-width="1.2"/>'
             '<circle cx="0" cy="-28" r="3.6" fill="#b07a55" stroke="%s" stroke-width="0.8"/>'
             '<path d="M-3.6 -29.5 Q0 -33.5 3.6 -29.5" fill="#2a2018"/>'
             '<path d="M-5 -21 L-8 -14" stroke="#f2efe8" stroke-width="2.6"/>'
             '<circle cx="-8" cy="-13" r="1.8" fill="none" stroke="#8a929a" stroke-width="1.2"/>'
             '<circle cx="-5.6" cy="-13" r="1.8" fill="none" stroke="#8a929a" stroke-width="1.2"/>'
             '</g>' % (gy, sc, INK, INK, INK))
    # escorts' hands on the detainee's arms
    b.append('<path d="M104 77 L115 79 M141 79 L150 77" stroke="#5c6a3a" stroke-width="2.6" stroke-linecap="round"/>')
    b.append(_label(12, 22, "ARRESTED", 16, bg="#8e1b1b"))
    return _svg(w, h, LEAD, defs, "".join(b))


# ---------------------------------------------------------- hormuz-tanker-strikes
def _tanker(x, y, s, hull="#3c4a5a"):
    """Tanker, bow right; (x, y) = deck line at stern."""
    return ('<g transform="translate(%.1f %.1f) scale(%.2f)">'
            '<path d="M0 0 L70 0 L64 10 L4 10 Z" fill="%s" stroke="%s" stroke-width="1.5"/>'
            '<path d="M2 4 H67" stroke="#a33a2a" stroke-width="2"/>'
            '<rect x="16" y="-2" width="46" height="2" fill="#7d8790" stroke="%s" stroke-width="0.6"/>'
            '<rect x="3" y="-11" width="11" height="11" fill="#ece6da" stroke="%s" stroke-width="1.3"/>'
            '<rect x="5" y="-8" width="7" height="2" fill="%s"/>'
            '<rect x="7" y="-16" width="3.5" height="5" fill="#b8862b" stroke="%s" stroke-width="0.8"/>'
            '</g>') % (x, y, s, hull, INK, INK, INK, INK, INK)


def hormuz_tanker_strikes(w, h):
    p = "hts"
    defs = (_lg(p + "sky", [("0", "#e09a72"), ("1", "#f6d6a0")])
            + _lg(p + "sea", [("0", "#4d6f86"), ("1", "#2c4659")])
            + _rg(p + "glow", [("0", "#ffcf6a", "0.9"), ("1", "#ffcf6a", "0")]))
    b = ['<rect width="191" height="66" fill="url(#%ssky)"/>' % p,
         '<rect y="24" width="191" height="42" fill="url(#%ssea)"/>' % p,
         # Iranian headland (left) and Musandam headland (right)
         '<path d="M0 0 L0 52 L14 48 L24 38 L22 30 L34 26 L40 24 L40 0 Z" fill="#7a5a4a" stroke="%s" stroke-width="1.3"/>'
         % INK,
         '<path d="M191 66 L191 0 L176 6 L170 18 L160 28 L164 40 L152 50 L158 66 Z" fill="#8b6a52" '
         'stroke="%s" stroke-width="1.3"/>' % INK]
    # struck tanker (back, right): blast and smoke
    b.append(_smoke(122, 14, [(0, 0, 6), (-7, -5, 7), (-16, -8, 7), (-26, -9, 6)], "#3a3438", 0.9))
    b.append('<circle cx="128" cy="24" r="14" fill="url(#%sglow)"/>' % p)
    b.append(_tanker(94, 30, 0.95, "#3c4a5a"))
    b.append(_star(128, 25, 7.5, 3.2, "#ffb02e"))
    # second tanker (front, left), also hit
    b.append(_smoke(64, 32, [(0, 0, 3.5), (-4, -4, 4.5)], "#3a3438", 0.85))
    b.append(_tanker(20, 42, 0.95, "#2f3c4c"))
    b.append(_star(66, 37, 5, 2.2, "#ffb02e"))
    b.append(_label(8, 15, "2 TANKERS HIT", 13, bg="#a3271d"))
    return _svg(w, h, SMALL, defs, "".join(b))


# ---------------------------------------------------------------- banda-sea-quake
def banda_sea_quake(w, h):
    p = "bsq"
    defs = _lg(p + "sea", [("0", "#a9cbd4"), ("1", "#6f9fae")])
    b = ['<rect width="191" height="66" fill="url(#%ssea)"/>' % p]
    ex, ey = 70, 38
    for i, r in enumerate((8, 15, 23, 32)):
        b.append('<circle cx="%d" cy="%d" r="%d" fill="none" stroke="#a3271d" stroke-width="%.1f" opacity="%.2f"/>'
                 % (ex, ey, r, 1.8 - i * 0.25, 0.9 - i * 0.17))
    # northern Australian coast, right edge
    b.append('<path d="M191 0 L170 0 Q162 8 166 16 L158 22 Q150 30 158 38 L154 48 Q160 58 168 66 L191 66 Z" '
             'fill="#d9c79c" stroke="%s" stroke-width="1.5"/>' % INK)
    b.append('<path d="M176 0 Q172 30 182 66" stroke="#c4ae7d" stroke-width="3" fill="none"/>')
    # seismograph trace spiking over the sea
    tr = []
    for i in range(0, 152, 2):
        d = (i - ex) / 14.0
        amp = 1.2 + 13.0 * math.exp(-d * d) + (4.0 * math.exp(-(i - ex) / 28.0) if i > ex else 0)
        y = 22 + amp * (1 if (i // 2) % 2 == 0 else -1)
        tr.append("%s%d %.1f" % ("M" if i == 0 else "L", i, y))
    b.append('<path d="%s" stroke="%s" stroke-width="1.6" fill="none" stroke-linejoin="round"/>' % (" ".join(tr), INK))
    b.append(_star(ex, ey, 6.5, 2.8))
    b.append(_label(8, 16, "M6.8", 14, bg="#a3271d"))
    return _svg(w, h, SMALL, defs, "".join(b))


ILLUS_A = {
    "gulf-finland-ship": gulf_finland_ship,
    "bahrain-sitra-fire": bahrain_sitra_fire,
    "meza-flores-confirm": meza_flores_confirm,
    "hormuz-tanker-strikes": hormuz_tanker_strikes,
    "banda-sea-quake": banda_sea_quake,
}
