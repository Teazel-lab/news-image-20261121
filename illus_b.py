"""Medium-card illustrations, part B (21 Nov 2026). ILLUS_B[id](w, h) -> inline <svg>.

Every scene is drawn on a fixed 243x80 viewBox. The bottom 16 units sit under
build.py's caption band, so key content stays above y=64. Flat editorial
vector style, light from the upper left. Standard library only, deterministic.
"""
import math

INK = "#231d17"
FONT = "Barlow Condensed"
VW, VH = 243, 80
SW = 1.5


# --- helpers --------------------------------------------------------------------
def _svg(w, h, sid, body, defs=""):
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d" '
            'preserveAspectRatio="xMidYMid slice" role="img" aria-label="%s"><defs>%s</defs>%s</svg>'
            % (round(w), round(h), VW, VH, sid, defs, body))


def _lin(i, stops, x2=0, y2=1):
    s = "".join('<stop offset="%s" stop-color="%s"/>' % (o, c) for o, c in stops)
    return '<linearGradient id="%s" x1="0" y1="0" x2="%s" y2="%s">%s</linearGradient>' % (i, x2, y2, s)


def _rect(x, y, w, h, fill, stroke=None, sw=SW, rx=0, extra=""):
    st = ' stroke="%s" stroke-width="%s" stroke-linejoin="round"' % (stroke, sw) if stroke else ""
    return '<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%s" fill="%s"%s%s/>' % (
        x, y, w, h, rx, fill, st, extra)


def _path(d, fill, stroke=None, sw=SW, extra=""):
    st = ' stroke="%s" stroke-width="%s" stroke-linejoin="round" stroke-linecap="round"' % (stroke, sw) if stroke else ""
    return '<path d="%s" fill="%s"%s%s/>' % (d, fill, st, extra)


def _circ(cx, cy, r, fill, stroke=None, sw=SW):
    st = ' stroke="%s" stroke-width="%s"' % (stroke, sw) if stroke else ""
    return '<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s"%s/>' % (cx, cy, r, fill, st)


def _line(x1, y1, x2, y2, stroke, sw=1.0, extra=""):
    return ('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%s" '
            'stroke-linecap="round"%s/>' % (x1, y1, x2, y2, stroke, sw, extra))


def _star(cx, cy, r, fill, n=5, ratio=0.42, rot=-90):
    pts = []
    for k in range(2 * n):
        rr = r if k % 2 == 0 else r * ratio
        a = math.radians(rot + k * 180.0 / n)
        pts.append("%.2f,%.2f" % (cx + rr * math.cos(a), cy + rr * math.sin(a)))
    return '<polygon points="%s" fill="%s"/>' % (" ".join(pts), fill)


def _text(x, y, s, size=13, fill="#fff", anchor="middle"):
    return ('<text x="%.1f" y="%.1f" font-family="%s" font-weight="700" font-size="%.1f" '
            'fill="%s" text-anchor="%s" letter-spacing="0.4">%s</text>' % (x, y, FONT, size, fill, anchor, s))


def _chip(x, y, label, bg=INK, fg="#fff", size=13, anchor="start"):
    """Label chip with top-left (anchor=start) / top-centre (middle) / top-right (end) at (x, y)."""
    w = len(label) * size * 0.5 + 10
    h = size + 4
    x0 = x if anchor == "start" else (x - w / 2 if anchor == "middle" else x - w)
    return (_rect(x0, y, w, h, bg, rx=2.5) +
            _text(x0 + w / 2, y + h - 4.3, label, size, fg))


def _rain(x0, x1, y0, y1, step, col="#ffffff", op=0.45):
    out = []
    k = 0
    x = x0
    while x < x1:
        yy = y0 + (k * 7) % 11
        while yy < y1:
            out.append(_line(x, yy, x - 2.2, yy + 6, col, 0.8, ' opacity="%s"' % op))
            yy += 14
        x += step
        k += 1
    return "".join(out)


# --- 1. EU budget cut -------------------------------------------------------------
def eu_costa_budget(w, h):
    p = "eucb"
    defs = _lin(p + "bg", [(0, "#e9e2d2"), (1, "#d8cfbb")])
    b = [_rect(-5, -5, 253, 90, "url(#%sbg)" % p)]
    # EU flag
    fx, fy, fw, fh = 10, 9, 66, 44
    b.append(_rect(fx, fy, fw, fh, "#003399", INK, SW))
    cx, cy = fx + fw / 2, fy + fh / 2
    for k in range(12):
        a = math.radians(k * 30)
        b.append(_star(cx + 14.5 * math.sin(a), cy - 14.5 * math.cos(a), 3.0, "#ffcc00"))
    # flag pole shadow line
    # bar chart
    ax = 92
    b.append(_line(ax, 10, ax, 61, INK, 1.6))
    b.append(_line(ax, 61, 238, 61, INK, 1.2))
    # top bar (being cut)
    b.append(_rect(ax, 18, 88, 15, "#2f5fa8", INK, SW))
    b.append(_rect(ax, 18, 88, 4, "#5c86c8"))
    b.append(_line(181, 15, 181, 36, INK, 1.0, ' stroke-dasharray="2 1.6"'))
    # severed piece, tipping down, carries the label
    b.append('<g transform="rotate(9 188 18)">' +
             _rect(188, 18, 48, 15, "#b8322a", INK, SW) +
             _text(212, 30, "−€40BN", 13) + '</g>')
    # other bars
    b.append(_rect(ax, 38, 118, 10, "#7d9ccf", INK, 1.2))
    b.append(_rect(ax, 51, 102, 10, "#a9bede", INK, 1.2))
    # scissors pointing down through the cut
    s = ('<g transform="translate(181 17) rotate(90) scale(0.8)">' +
         _path("M0,-1.6 L25,-6.5 L25,-4 L0,2 Z", "#cfd3d8", INK, 1.1) +
         _path("M0,1.6 L25,6.5 L25,4 L0,-2 Z", "#e4e7ea", INK, 1.1) +
         _path("M0,-1 L-6,-5", "none", "#c0392b", 2.2) + _path("M0,1 L-6,5", "none", "#c0392b", 2.2) +
         '<ellipse cx="-10" cy="-7" rx="5" ry="3.6" fill="none" stroke="#c0392b" stroke-width="2.4"/>' +
         '<ellipse cx="-10" cy="7" rx="5" ry="3.6" fill="none" stroke="#c0392b" stroke-width="2.4"/>' +
         _circ(0, 0, 1.4, INK) + '</g>')
    b.append(s)
    return _svg(w, h, "eu-costa-budget", "".join(b), defs)


# --- 2. Basra power-station fire ----------------------------------------------------
def basra_hartha_fire(w, h):
    p = "bhf"
    defs = (_lin(p + "sky", [(0, "#d9a679"), (0.6, "#efc99c"), (1, "#f3dcc0")]) +
            _lin(p + "fl", [(0, "#ffe07a"), (0.5, "#f59a23"), (1, "#d9481c")]))
    b = [_rect(-5, -5, 253, 90, "url(#%ssky)" % p)]
    # black smoke drifting right
    for (x, y, r, c) in [(118, 22, 11, "#3a332e"), (132, 14, 13, "#2b2521"), (150, 9, 14, "#332c27"),
                         (170, 6, 15, "#2b2521"), (192, 5, 14, "#3d3631"), (214, 7, 12, "#4a423c"),
                         (232, 9, 10, "#5a524b"), (126, 27, 8, "#2b2521")]:
        b.append(_circ(x, y, r, c))
    # ground
    b.append(_rect(-5, 58, 253, 30, "#8c7357"))
    b.append(_rect(-5, 58, 253, 2, "#6e5a44"))
    # chimneys
    for x in (88, 104, 120):
        b.append(_path("M%d,16 L%d,16 L%d,36 L%d,36 Z" % (x - 3, x + 3, x + 4, x - 4), "#cfc6b8", INK, SW))
        b.append(_rect(x - 3.3, 19, 6.6, 3, "#c0392b"))
        b.append(_rect(x - 3.6, 26, 7.2, 3, "#c0392b"))
        b.append(_circ(x - 2, 13, 3, "#8b827a"))
    # turbine hall
    b.append(_rect(70, 34, 78, 25, "#b9b0a2", INK, SW))
    b.append(_rect(70, 34, 78, 4, "#d6cec1"))
    for i in range(6):
        b.append(_rect(75 + i * 12, 42, 7, 6, "#6b625a"))
    b.append(_rect(30, 44, 40, 15, "#a39a8c", INK, SW))  # switch house
    for i in range(3):
        b.append(_line(34 + i * 12, 47, 34 + i * 12, 56, "#6b625a", 1.6))
    # flames from roof / right end
    b.append('<g transform="translate(131 36) scale(1.35) translate(-131 -36)">')
    b.append(_path("M118,36 C116,28 122,26 121,20 C127,25 126,18 131,13 C132,22 138,22 137,16 "
                   "C144,22 146,28 144,36 Z", "url(#%sfl)" % p, "#b8401a", 1.0))
    b.append(_path("M136,48 C134,42 140,40 139,35 C145,39 147,33 150,30 C153,38 152,44 150,50 Z",
                   "url(#%sfl)" % p, "#b8401a", 1.0))
    b.append(_path("M124,36 C124,31 128,30 128,25 C131,29 134,28 134,24 C137,29 138,33 136,36 Z", "#ffe9a0"))
    b.append('</g>')
    # water jet from truck
    b.append(_path("M190,38 Q170,20 148,30", "none", "#7cc4e8", 2.2, ' opacity="0.9"'))
    # fire truck
    b.append(_rect(176, 40, 44, 15, "#c62828", INK, SW))
    b.append(_path("M220,44 L232,44 L237,50 L237,55 L220,55 Z", "#c62828", INK, SW))
    b.append(_path("M222,46 L230,46 L234,50 L222,50 Z", "#bfe1f2"))
    b.append(_rect(176, 47, 44, 2, "#f2f2f2"))
    b.append(_path("M180,39 L214,33", "none", "#e8e2d6", 2.6))
    b.append(_path("M180,39 L214,33", "none", INK, 0.6, ' stroke-dasharray="1.5 2.5"'))
    b.append(_rect(226, 41, 4, 3, "#2f7de1"))
    for x in (186, 228):
        b.append(_circ(x, 56, 4.2, INK) + _circ(x, 56, 1.6, "#9a9a9a"))
    b.append(_chip(5, 4, "HARTHA PLANT"))
    return _svg(w, h, "basra-hartha-fire", "".join(b), defs)


# --- 3. COP31 overtime ------------------------------------------------------------
def cop31_overtime(w, h):
    p = "cop"
    defs = (_lin(p + "wall", [(0, "#2b5f6e"), (1, "#3f7b86")]) +
            _lin(p + "win", [(0, "#101a33"), (1, "#283a63")]))
    b = [_rect(-5, -5, 253, 90, "url(#%swall)" % p)]
    # night window with moon
    b.append(_rect(152, 6, 24, 28, "url(#%swin)" % p, INK, SW))
    b.append(_circ(161, 15, 5, "#f3e7b3") + _circ(163.5, 13.5, 4.3, "#16213f"))
    b.append(_star(170, 26, 1.4, "#f3e7b3") + _star(157, 29, 1.0, "#f3e7b3"))
    b.append(_line(164, 6, 164, 34, INK, 1.0))
    # big globe emblem on backdrop
    gx, gy, gr = 128, 13, 10
    b.append(_circ(gx, gy, gr, "#5aa7c9", INK, SW))
    b.append(_path("M%f,%f c4,-3 9,-2 10,2 c-3,4 -7,3 -8,8 c-3,-2 -4,-6 -2,-10 Z" % (gx - 9, gy - 5), "#6cae5a"))
    b.append(_path("M%f,%f c3,-1 6,2 5,6 c-1,3 -4,4 -6,2 Z" % (gx + 3, gy - 2), "#6cae5a"))
    b.append('<ellipse cx="%d" cy="%d" rx="5.5" ry="%d" fill="none" stroke="%s" stroke-width="0.8"/>' % (gx, gy, gr, INK))
    b.append(_line(gx - gr, gy, gx + gr, gy, INK, 0.8))
    # stage
    b.append(_rect(-5, 40, 253, 9, "#c49a5b", INK, SW))
    b.append(_rect(-5, 40, 253, 2.5, "#dcb879"))
    # podium
    b.append(_path("M118,42 L138,42 L135,27 L121,27 Z", "#e9e1d0", INK, SW))
    b.append(_rect(119, 25, 18, 3, "#cfc4ae", INK, 1.2))
    b.append(_circ(128, 35, 3.5, "#5aa7c9", INK, 0.8))
    b.append(_line(125, 25, 122, 21, INK, 1.0) + _circ(122, 20.5, 1.2, INK))
    # wall clock: ten past twelve
    cx, cy, r = 205, 24, 18
    b.append(_circ(cx + 1.5, cy + 1.5, r, "#1d3d46"))
    b.append(_circ(cx, cy, r, "#f8f4ea", INK, 2.0))
    for k in range(12):
        a = math.radians(k * 30)
        r0 = r - (4 if k % 3 == 0 else 2.5)
        b.append(_line(cx + r0 * math.sin(a), cy - r0 * math.cos(a), cx + (r - 1.5) * math.sin(a),
                       cy - (r - 1.5) * math.cos(a), INK, 1.5 if k % 3 == 0 else 0.8))
    ha, ma = math.radians(5), math.radians(60)
    b.append(_line(cx, cy, cx + 9 * math.sin(ha), cy - 9 * math.cos(ha), INK, 2.4))
    b.append(_line(cx, cy, cx + 14 * math.sin(ma), cy - 14 * math.cos(ma), INK, 1.6))
    b.append(_path("M%f,%f A15,15 0 0 1 %f,%f" % (cx, cy - 15, cx + 15 * math.sin(ma), cy - 15 * math.cos(ma)),
                   "none", "#c0392b", 2.2, ' opacity="0.85"'))
    b.append(_circ(cx, cy, 1.6, "#c0392b"))
    # delegate chairs (rows, many empty)
    b.append(_rect(-5, 49, 253, 40, "#24434b"))
    for row, (y, s, col) in enumerate([(50, 1.0, "#4d6f78"), (56, 1.15, "#3a5a63")]):
        x = 4 + row * 6
        while x < 243:
            b.append(_rect(x, y, 11 * s, 8 * s, col, INK, 0.9, rx=2.5))
            x += 15 * s
    b.append(_chip(5, 4, "COP31 OVERTIME"))
    return _svg(w, h, "cop31-overtime", "".join(b), defs)


# --- 4. Vietnam land law ----------------------------------------------------------
def vietnam_land_law(w, h):
    p = "vnl"
    defs = (_lin(p + "sky", [(0, "#cfe3e6"), (1, "#eaf0dc")]) +
            _lin(p + "hall", [(0, "#8a2a24"), (1, "#6b1f1b")]))
    b = [_rect(-5, -5, 253, 90, "url(#%ssky)" % p)]
    # assembly chamber panel (left)
    b.append(_rect(-5, -5, 122, 90, "url(#%shall)" % p))
    # vote board
    b.append(_rect(8, 5, 96, 36, "#1c2430", INK, SW))
    b.append(_text(56, 20, "466 YES", 14, "#7ee08a"))
    b.append(_rect(14, 26, 84, 9, "#3a4350"))
    b.append(_rect(14, 26, 77, 9, "#2fa84f"))
    b.append(_rect(91, 26, 4, 9, "#d24a3a"))
    b.append(_rect(14, 26, 77, 2.5, "#5fd07a"))
    # raised hands of deputies
    for i in range(8):
        x = 10 + i * 13
        y = 52 + (i % 2) * 3
        b.append(_path("M%f,%f l0,-9 l3.6,0 l0,9 Z" % (x + 1.4, y - 3), "#e6b98c", INK, 0.8))
        b.append(_rect(x + 0.6, y - 16, 5.2, 7, "#f0c79a", INK, 0.8, rx=2))
        b.append(_circ(x + 3, y + 3, 4.2, "#2b211b"))
        b.append(_rect(x - 2, y + 6, 10, 12, "#3b4a6b", rx=2.5))
    # flag on pole
    b.append(_line(112, 6, 112, 62, "#5b4c3c", 1.4))
    b.append(_rect(113, 6, 21, 14, "#da251d", INK, 1.0))
    b.append(_star(123.5, 13.2, 4.8, "#ffff00", ratio=0.38))
    # rice field plots in perspective
    b.append(_path("M120,34 L248,30 L248,85 L120,85 Z", "#9cc35a"))
    rows = [(34, "#a9cf63"), (40, "#86b44a"), (47, "#9cc35a"), (55, "#7aa843")]
    for y, c in rows:
        b.append(_path("M120,%d L248,%d L248,%d L120,%d Z" % (y, y - 3, y + 4, y + 7), c))
        b.append(_line(120, y, 248, y - 3, "#6a8d3a", 0.8))
    for x in (150, 182, 214):
        b.append(_line(x, 34, x - 8, 80, "#6a8d3a", 0.8))
    b.append(_path("M120,40 L248,36 L248,39 L120,44 Z", "#bfdde6", extra=' opacity="0.6"'))
    # survey stakes with string line
    stakes = [(140, 50), (172, 44), (204, 39), (232, 35)]
    b.append(_path("M" + " L".join("%d,%d" % (x, y - 10) for x, y in stakes), "none", "#c0392b", 0.9))
    for x, y in stakes:
        b.append(_path("M%f,%f L%f,%f L%f,%f L%f,%f Z" % (x - 1.6, y - 13, x + 1.6, y - 13, x + 1.2, y, x - 1.2, y),
                       "#d8b47a", INK, 0.9))
        b.append(_rect(x - 1.6, y - 13, 3.2, 3.5, "#d9482b"))
    b.append(_path("M120,34 L248,30", "none", "#6a8d3a", 1.0))
    return _svg(w, h, "vietnam-land-law", "".join(b), defs)


# --- 5. Bayelsa boat rescue ---------------------------------------------------------
def _mangrove(x, y, s, flip=False):
    tr = "translate(%f %f) scale(%f %f)" % (x, y, -s if flip else s, s)
    g = ['<g transform="%s">' % tr]
    for dx in (-8, -3, 3, 8):
        g.append(_path("M0,-6 Q%f,-2 %f,8" % (dx * 0.6, dx), "none", "#4a3a26", 1.4))
    g.append(_line(0, -18, 0, -4, "#4a3a26", 2.2))
    for (cx, cy, r, c) in [(-8, -22, 9, "#2f6a35"), (6, -26, 11, "#3b7d3f"), (-2, -32, 9, "#4c9150"),
                           (12, -18, 7, "#2f6a35")]:
        g.append(_circ(cx, cy, r, c))
    g.append('</g>')
    return "".join(g)


def tinubu_bayelsa_rescue(w, h):
    p = "tbr"
    defs = (_lin(p + "sky", [(0, "#cfdfe0"), (1, "#eae7d6")]) +
            _lin(p + "w", [(0, "#6f8f78"), (1, "#3f5f55")]))
    b = [_rect(-5, -5, 253, 90, "url(#%ssky)" % p)]
    b.append(_path("M-5,30 Q60,24 120,29 T248,27 L248,36 L-5,36 Z", "#4f7d4a"))  # far bank
    b.append(_rect(-5, 33, 253, 60, "url(#%sw)" % p))
    for i in range(7):
        b.append(_line(30 + i * 30, 52 + (i % 3) * 3, 42 + i * 30, 52 + (i % 3) * 3, "#a9c2b4", 0.9, ' opacity="0.7"'))
    b.append(_mangrove(14, 44, 1.15))
    b.append(_mangrove(232, 44, 1.15, flip=True))
    # capsized wooden boat (keel up)
    b.append(_path("M54,44 Q85,26 120,42 Z", "#8a5a33", INK, SW))
    for k in range(1, 3):
        b.append(_path("M%f,%f Q86,%f %f,%f" % (54 + k * 4, 44 - k * 1.2, 26 + k * 5.5, 120 - k * 4, 42 - k * 1.2),
                       "none", "#5e3c22", 0.8))
    b.append(_path("M50,45 Q86,41 124,43", "none", "#d8e6dc", 1.4))
    # survivors clinging / life ring
    b.append(_circ(60, 46, 2.8, "#3a2a20") + _path("M57,49 q3,-2 6,0", "none", "#f07f1a", 2.0))
    b.append('<circle cx="132" cy="47" r="4.5" fill="none" stroke="#f07f1a" stroke-width="2.6"/>')
    b.append('<circle cx="132" cy="47" r="4.5" fill="none" stroke="#fff" stroke-width="2.6" stroke-dasharray="2 5"/>')
    # rescue boat
    b.append(_path("M150,46 L206,46 L200,56 L156,56 Z", "#f4f1ea", INK, SW))
    b.append(_rect(152, 49, 52, 2, "#1f5fa8"))
    b.append(_path("M170,46 L170,38 L186,38 L190,46 Z", "#e3ddd0", INK, 1.1))
    b.append(_rect(173, 40, 10, 4, "#9cc8de"))
    for x in (160, 196):
        b.append(_circ(x, 37, 3, "#3a2a20"))
        b.append(_rect(x - 3.5, 40, 7, 7, "#f07f1a", INK, 0.9, rx=1.5))
    b.append(_path("M160,42 L145,46", "none", "#3a2a20", 1.6))  # reaching out
    # Nigeria flag on mast
    b.append(_line(188, 38, 188, 18, "#5b4c3c", 1.2))
    b.append(_rect(189, 18, 6, 12, "#008751"))
    b.append(_rect(195, 18, 6, 12, "#ffffff"))
    b.append(_rect(201, 18, 6, 12, "#008751"))
    b.append(_rect(189, 18, 18, 12, "none", INK, 0.8))
    b.append(_path("M150,53 Q140,56 128,54", "none", "#d8e6dc", 1.0))
    b.append(_chip(118, 4, "RESCUE", bg="#c0392b", anchor="middle"))
    return _svg(w, h, "tinubu-bayelsa-rescue", "".join(b), defs)


# --- 6. CAF backs Infantino; grants triple ----------------------------------------------
def caf_infantino_grants(w, h):
    p = "cafg"
    defs = (_lin(p + "bg", [(0, "#e3ecd9"), (1, "#c9d9b6")]) +
            _lin(p + "gold", [(0, "#f2cf63"), (1, "#c89a2c")]))
    b = [_rect(-5, -5, 253, 90, "url(#%sbg)" % p)]
    for i in range(0, 260, 30):
        b.append(_rect(i - 5, 48, 15, 40, "#b9cfa0"))
    b.append(_rect(-5, 48, 253, 1.2, "#f4efe4", extra=' opacity="0.7"'))
    # plinth with football
    b.append(_rect(26, 44, 60, 17, "#e8e1d1", INK, SW))
    b.append(_rect(32, 36, 48, 9, "#f4efe4", INK, SW))
    b.append(_rect(32, 39, 48, 2.5, "url(#%sgold)" % p))
    bx, by, br = 56, 22, 13
    b.append('<ellipse cx="56" cy="36" rx="11" ry="1.8" fill="#000" opacity="0.18"/>')
    b.append(_circ(bx, by, br, "#ffffff", INK, SW))
    b.append('<clipPath id="%sball"><circle cx="%d" cy="%d" r="%d"/></clipPath>' % (p, bx, by, br))
    b.append(_star(bx, by, 4.4, INK, n=5, ratio=0.81))
    b.append('<g clip-path="url(#%sball)">' % p)
    for k in range(5):
        a = math.radians(-90 + 36 + k * 72)
        b.append(_line(bx + 3.6 * math.cos(a), by + 3.6 * math.sin(a), bx + 9 * math.cos(a), by + 9 * math.sin(a), INK, 0.9))
        b.append(_star(bx + 12.5 * math.cos(a), by + 12.5 * math.sin(a), 4.2, INK, n=5, ratio=0.81, rot=-90 + 36 + k * 72 + 36))
    b.append('</g>')
    b.append(_circ(bx, by, br, "none", INK, SW))
    b.append(_path("M47,15 Q51,11 56,11", "none", "#ffffff", 1.4))
    # bar chart: $8M -> $25M
    base = 61
    b.append(_line(118, base, 236, base, INK, 1.4))
    small_h = 14.0
    tall_h = small_h * 25 / 8  # ~43.8
    b.append(_rect(130, base - small_h, 28, small_h, "#7d9a68", INK, SW))
    b.append(_rect(190, base - tall_h, 30, tall_h, "url(#%sgold)" % p, INK, SW))
    b.append(_rect(190, base - tall_h, 6, tall_h, "#f7dd8a", extra=' opacity="0.6"'))
    b.append(_text(144, base - small_h - 4, "$8M", 13, INK))
    b.append(_text(205, base - tall_h - 3.5, "$25M", 13, INK))
    # rising arrow
    b.append(_path("M163,40 Q172,28 182,22", "none", "#b8322a", 2.2))
    b.append(_path("M184,21 L177,19.5 L180.5,26 Z", "#b8322a"))
    return _svg(w, h, "caf-infantino-grants", "".join(b), defs)


# --- 7. Florida record flood ------------------------------------------------------
def _palm(x, y, s):
    g = ['<g transform="translate(%f %f) scale(%f)">' % (x, y, s)]
    g.append(_path("M0,0 Q2,-14 -1,-30", "none", "#6b5235", 2.4))
    for (dx, dy) in [(-13, -24), (-11, -34), (0, -38), (11, -35), (14, -26)]:
        g.append(_path("M-1,-30 Q%f,%f %f,%f" % (dx * 0.5, -36, dx, dy), "none", "#3f6e3c", 2.8))
    g.append('</g>')
    return "".join(g)


def florida_flood_shift(w, h):
    p = "flf"
    defs = (_lin(p + "sky", [(0, "#7d8794"), (1, "#b9bdc0")]) +
            _lin(p + "w", [(0, "#7d7a62"), (1, "#5a5944")]))
    b = [_rect(-5, -5, 253, 90, "url(#%ssky)" % p)]
    # houses partly submerged
    for (x, wd, ht, c) in [(40, 30, 16, "#d9c9a8"), (120, 34, 18, "#c9b896"), (164, 26, 14, "#ddd0b4")]:
        b.append(_rect(x, 42 - ht, wd, ht + 4, c, INK, 1.1))
        b.append(_path("M%f,%f L%f,%f L%f,%f Z" % (x - 2, 42 - ht, x + wd / 2, 42 - ht - 8, x + wd + 2, 42 - ht),
                       "#8a5a3c", INK, 1.1))
        b.append(_rect(x + 5, 42 - ht + 4, 6, 5, "#6f7c86"))
    b.append(_palm(18, 44, 1.0))
    b.append(_palm(200, 44, 0.9))
    # floodwater
    b.append(_rect(-5, 40, 253, 50, "url(#%sw)" % p))
    b.append(_rect(-5, 40, 253, 1.6, "#a7a58b"))
    # car half under water
    b.append(_path("M76,40 L80,31 Q82,29 86,29 L106,29 Q110,29 112,32 L117,40 Z", "#c0392b", INK, SW))
    b.append(_path("M83,38 L86,32 L95,32 L95,38 Z M98,32 L106,32 L110,38 L98,38 Z", "#bcd3e0"))
    for i in range(3):
        b.append(_line(72 + i * 4, 43 + i * 2, 120 - i * 4, 43 + i * 2, "#a7a58b", 0.8, ' opacity="0.8"'))
    # small boat with person
    b.append(_path("M136,44 L170,44 L165,50 L140,50 Z", "#e9e1cf", INK, SW))
    b.append(_circ(152, 37, 2.8, "#2b211b"))
    b.append(_rect(149, 40, 6, 5, "#f07f1a", rx=1.2))
    b.append(_line(156, 41, 168, 52, "#6b5235", 1.3))
    # river gauge post with record line
    gx = 224
    b.append(_rect(gx - 4, 6, 9, 58, "#f4efe4", INK, SW))
    for k in range(11):
        y = 9 + k * 5
        b.append(_line(gx - 4, y, gx + (2 if k % 2 else 0), y, INK, 0.9))
    b.append(_rect(gx - 8, 27, 17, 3, "#d0281c", INK, 0.8))
    b.append(_rect(gx - 4, 40, 9, 24, "#5a5944", extra=' opacity="0.65"'))
    b.append(_rain(6, 243, -4, 40, 9))
    b.append(_chip(5, 4, "RECORD FLOOD", bg="#1f4e79"))
    return _svg(w, h, "florida-flood-shift", "".join(b), defs)


# --- 8. Home-birth rallies, Australia ----------------------------------------------
def _au_flag(x, y, fw):
    fh = fw / 2
    cw, chh = fw / 2, fh / 2
    cid = "hbrcanton"
    g = ['<clipPath id="%s"><rect x="%f" y="%f" width="%f" height="%f"/></clipPath>' % (cid, x, y, cw, chh)]
    g.append(_rect(x, y, fw, fh, "#012169"))
    g.append('<g clip-path="url(#%s)">' % cid)
    g.append(_line(x, y, x + cw, y + chh, "#fff", 2.6) + _line(x + cw, y, x, y + chh, "#fff", 2.6))
    g.append(_line(x, y, x + cw, y + chh, "#c8102e", 0.9) + _line(x + cw, y, x, y + chh, "#c8102e", 0.9))
    g.append(_rect(x + cw / 2 - 2, y, 4, chh, "#fff") + _rect(x, y + chh / 2 - 2, cw, 4, "#fff"))
    g.append(_rect(x + cw / 2 - 1.1, y, 2.2, chh, "#c8102e") + _rect(x, y + chh / 2 - 1.1, cw, 2.2, "#c8102e"))
    g.append('</g>')
    g.append(_star(x + cw / 2, y + fh * 0.75, fw * 0.075, "#fff", n=7, ratio=0.45))
    for (fx, fy, r, n) in [(0.75, 0.83, 0.036, 7), (0.625, 0.47, 0.036, 7), (0.75, 0.17, 0.036, 7),
                           (0.87, 0.40, 0.036, 7), (0.80, 0.58, 0.022, 5)]:
        g.append(_star(x + fw * fx, y + fh * fy, fw * r, "#fff", n=n, ratio=0.45))
    g.append(_rect(x, y, fw, fh, "none", INK, 0.8))
    return "".join(g)


def _pram(x, y, c):
    return ('<g transform="translate(%f %f) scale(1.35) translate(%f %f)">' % (x, y, -x, -y) +_path("M%f,%f a9,7 0 0 0 18,0 Z" % (x, y), c, INK, 1.1) +
            _path("M%f,%f a9,9 0 0 1 9,-9 l0,9 Z" % (x, y), "#5b4c6b", INK, 1.1) +
            _path("M%f,%f l5,-6" % (x + 18, y), "none", INK, 1.2) +
            _circ(x + 4, y + 9, 2.4, INK) + _circ(x + 14, y + 9, 2.4, INK) + '</g>')


def homebirth_rallies(w, h):
    p = "hbr"
    defs = _lin(p + "sky", [(0, "#a9d2ea"), (1, "#e9f1ee")])
    b = [_rect(-5, -5, 253, 90, "url(#%ssky)" % p)]
    b.append(_rect(-5, 52, 253, 40, "#c9bfae"))
    # flag on pole
    b.append(_line(10, 4, 10, 62, "#6b5235", 1.6))
    b.append(_au_flag(11, 5, 50))
    # crowd: back row then front row
    skins = ["#e6b98c", "#b07a52", "#d9a06e", "#7a4e31", "#f0c79a"]
    shirts = ["#2f7d6e", "#c0392b", "#e0a43a", "#3b5998", "#8e5aa8", "#4f8a3c"]
    icons = ["heart", "house", "heart", "house", "heart", "house"]
    # placards (behind heads)
    for i, x in enumerate([100, 132, 164, 196, 228]):
        sx = x + (i % 2) * 3
        b.append(_line(sx, 22, sx, 44, "#6b5235", 1.3))
        b.append(_rect(sx - 11, 10, 22, 15, "#fbf8f0", INK, 1.2, rx=1))
        if icons[i] == "heart":
            b.append(_path("M%f,%f c-5,-3 -6,-8 -2.5,-9 c1.5,-0.4 2.5,0.6 2.5,1.6 c0,-1 1,-2 2.5,-1.6 c3.5,1 2.5,6 -2.5,9 Z"
                           % (sx, 22), "#d0281c"))
        else:
            b.append(_path("M%f,%f l7,-6 l7,6 l-2,0 l0,5 l-10,0 l0,-5 Z" % (sx - 7, 19), "#2f7d6e"))
            b.append(_rect(sx - 1.3, 20.5, 2.6, 3.5, "#fbf8f0"))
    for row, (y0, sp, off) in enumerate([(36, 13, 92), (42, 15, 86)]):
        x = off
        k = row
        while x < 240:
            b.append(_rect(x - 5, y0 + 6, 10, 18, shirts[k % len(shirts)], INK, 0.8, rx=4))
            b.append(_circ(x, y0 + 2, 4, skins[k % len(skins)], INK, 0.8))
            x += sp
            k += 1
    # prams in front
    b.append(_pram(104, 50, "#e07a8f"))
    b.append(_pram(178, 50, "#7fb4d6"))
    b.append(_chip(4, 36, "HOME BIRTH", bg="#178a8a"))
    return _svg(w, h, "homebirth-rallies", "".join(b), defs)


ILLUS_B = {
    "eu-costa-budget": eu_costa_budget,
    "basra-hartha-fire": basra_hartha_fire,
    "cop31-overtime": cop31_overtime,
    "vietnam-land-law": vietnam_land_law,
    "tinubu-bayelsa-rescue": tinubu_bayelsa_rescue,
    "caf-infantino-grants": caf_infantino_grants,
    "florida-flood-shift": florida_flood_shift,
    "homebirth-rallies": homebirth_rallies,
}
