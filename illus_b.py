"""Small-card illustrations, part B (21 Nov 2026). ILLUS_B[id](w, h) -> inline <svg>.

Every scene is drawn on a fixed 191x66 viewBox (v2 small cards). The bottom 15
units sit under build.py's caption band, so key content stays above y=51.
One big subject per card, at most one label (Barlow Condensed 700, >= 13 units).
Flat editorial vector style, light from the upper left. Standard library only,
deterministic.
"""
import math

INK = "#231d17"
FONT = "Barlow Condensed"
VW, VH = 191, 66
SW = 1.5
BAND = 51  # top of the caption band


# --- helpers --------------------------------------------------------------------
def _svg(w, h, sid, body, defs=""):
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d" '
            'preserveAspectRatio="xMidYMid slice" role="img" aria-label="%s"><defs>%s</defs>%s</svg>'
            % (round(w), round(h), VW, VH, sid, defs, body))


def _lin(i, stops, x2=0, y2=1):
    s = "".join('<stop offset="%s" stop-color="%s"/>' % (o, c) for o, c in stops)
    return '<linearGradient id="%s" x1="0" y1="0" x2="%s" y2="%s">%s</linearGradient>' % (i, x2, y2, s)


def _rad(i, stops, cx=0.35, cy=0.3, r=0.75):
    s = "".join('<stop offset="%s" stop-color="%s"/>' % (o, c) for o, c in stops)
    return '<radialGradient id="%s" cx="%s" cy="%s" r="%s">%s</radialGradient>' % (i, cx, cy, r, s)


def _rect(x, y, w, h, fill, stroke=None, sw=SW, rx=0, extra=""):
    st = ' stroke="%s" stroke-width="%s" stroke-linejoin="round"' % (stroke, sw) if stroke else ""
    return '<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%s" fill="%s"%s%s/>' % (
        x, y, w, h, rx, fill, st, extra)


def _path(d, fill, stroke=None, sw=SW, extra=""):
    st = ' stroke="%s" stroke-width="%s" stroke-linejoin="round" stroke-linecap="round"' % (stroke, sw) if stroke else ""
    return '<path d="%s" fill="%s"%s%s/>' % (d, fill, st, extra)


def _circ(cx, cy, r, fill, stroke=None, sw=SW, extra=""):
    st = ' stroke="%s" stroke-width="%s"' % (stroke, sw) if stroke else ""
    return '<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s"%s%s/>' % (cx, cy, r, fill, st, extra)


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


def _text(x, y, s, size=14, fill="#fff", anchor="middle"):
    return ('<text x="%.1f" y="%.1f" font-family="%s" font-weight="700" font-size="%.1f" '
            'fill="%s" text-anchor="%s" letter-spacing="0.4">%s</text>' % (x, y, FONT, size, fill, anchor, s))


def _chip(x, y, label, bg=INK, fg="#fff", size=14, anchor="start"):
    """Label chip; (x, y) is its top-left / top-centre / top-right corner per anchor."""
    w = len(label) * size * 0.5 + 10
    h = size + 4
    x0 = x if anchor == "start" else (x - w / 2 if anchor == "middle" else x - w)
    return (_rect(x0, y, w, h, bg, INK, 1.0, rx=2.5) +
            _text(x0 + w / 2, y + h - 4.6, label, size, fg))


# --- 1. Peru, Junin M6.7 earthquake --------------------------------------------------
def peru_junin_m67(w, h):
    p = "perujunin"
    defs = _lin(p + "sky", [(0, "#9cc3d8"), (1, "#efe2c8")])
    b = [_rect(-5, -5, VW + 10, VH + 10, "url(#%ssky)" % p)]
    # Andes
    b.append(_path("M-5,40 L22,12 L38,26 L58,4 L84,30 L102,14 L128,36 L-5,40 Z", "#7d7187", INK, 1.0))
    b.append(_path("M22,12 L28,19 L24,18 L19,21 Z M58,4 L66,13 L60,12 L56,15 L51,12 Z M102,14 L109,21 L104,20 L98,19 Z",
                   "#f7f4ee"))
    b.append(_path("M60,40 L120,8 L150,30 L170,16 L196,34 L196,40 Z", "#968aa0", INK, 1.0))
    b.append(_path("M120,8 L128,14 L123,14 L119,17 L114,12 Z M170,16 L177,22 L172,21 L167,20 Z", "#f7f4ee"))
    # ground
    b.append(_rect(-5, 38, VW + 10, 40, "#b9925f"))
    b.append(_rect(-5, 38, VW + 10, 2, "#9c7748"))
    # adobe house: left part standing, right wall collapsed
    b.append(_path("M18,50 L18,26 L66,22 L70,50 Z", "#d4a36a", INK, SW))
    b.append(_path("M14,27 L44,14 L74,22 L72,25 L44,18 L16,30 Z", "#a8452e", INK, SW))  # tilted tile roof
    b.append(_rect(28, 34, 10, 16, "#5b3a22", INK, 1.2))  # door
    b.append(_rect(48, 30, 9, 8, "#3d2a1b", INK, 1.2))  # window
    # crack
    b.append(_path("M62,23 L58,30 L63,34 L57,41 L61,46 L58,50", "none", INK, 1.6))
    # fallen wall rubble
    for (x, y, rw, rh, rot) in [(70, 44, 10, 6, 18), (80, 46, 11, 5, -12), (74, 39, 9, 5, 34),
                                (90, 45, 8, 5, 8), (84, 41, 7, 4, -25), (97, 47, 7, 4, 15)]:
        b.append('<g transform="rotate(%d %f %f)">%s</g>' % (rot, x + rw / 2, y + rh / 2,
                                                             _rect(x, y, rw, rh, "#c8955c", INK, 1.0)))
    # dust puffs
    for (x, y, r) in [(86, 36, 5), (95, 38, 4), (78, 34, 3.5)]:
        b.append(_circ(x, y, r, "#e9dcc4", extra=' opacity="0.8"'))
    # seismograph strip with a spike
    sx, sy, sw_, sh = 112, 24, 74, 26
    b.append(_rect(sx, sy, sw_, sh, "#fbf8f0", INK, SW, rx=2))
    for k in range(1, 4):
        b.append(_line(sx + 2, sy + k * sh / 4, sx + sw_ - 2, sy + k * sh / 4, "#e7b9a8", 0.5))
    mid = sy + sh / 2
    pts = [(sx + 3, mid), (sx + 20, mid), (sx + 24, mid - 2), (sx + 27, mid + 2), (sx + 31, mid - 11),
           (sx + 35, mid + 11), (sx + 39, mid - 8), (sx + 43, mid + 6), (sx + 47, mid - 3), (sx + 51, mid + 2),
           (sx + 55, mid), (sx + sw_ - 3, mid)]
    b.append(_path("M" + " L".join("%.1f,%.1f" % q for q in pts), "none", "#b8322a", 1.6))
    b.append(_chip(VW - 4, 3, "M6.7", bg="#b8322a", anchor="end"))
    return _svg(w, h, "peru-junin-m67", "".join(b), defs)


# --- 2. COP31 runs into overtime ------------------------------------------------------
def cop31_overtime(w, h):
    p = "cop31ot"
    defs = (_lin(p + "wall", [(0, "#2b5f6e"), (1, "#41808a")]) +
            _rad(p + "glb", [(0, "#8fd0ea"), (1, "#3f8fb4")]))
    b = [_rect(-5, -5, VW + 10, VH + 10, "url(#%swall)" % p)]
    # big wall clock, ten past twelve (deadline passed)
    cx, cy, r = 38, 24, 19
    b.append(_circ(cx + 1.8, cy + 1.8, r, "#1d3d46"))
    b.append(_circ(cx, cy, r, "#f8f4ea", INK, 2.0))
    for k in range(12):
        a = math.radians(k * 30)
        r0 = r - (4.5 if k % 3 == 0 else 2.6)
        b.append(_line(cx + r0 * math.sin(a), cy - r0 * math.cos(a), cx + (r - 1.6) * math.sin(a),
                       cy - (r - 1.6) * math.cos(a), INK, 1.6 if k % 3 == 0 else 0.8))
    ma = math.radians(60)
    b.append(_path("M%f,%f L%f,%f A15,15 0 0 1 %f,%f Z" % (cx, cy, cx, cy - 15, cx + 15 * math.sin(ma),
                                                       cy - 15 * math.cos(ma)), "#e07a5f", extra=' opacity="0.55"'))
    b.append(_line(cx, cy, cx + 9 * math.sin(math.radians(5)), cy - 9 * math.cos(math.radians(5)), INK, 2.6))
    b.append(_line(cx, cy, cx + 15 * math.sin(ma), cy - 15 * math.cos(ma), INK, 1.8))
    b.append(_circ(cx, cy, 1.8, "#c0392b"))
    # globe emblem on backdrop
    gx, gy, gr = 118, 18, 12
    b.append(_circ(gx, gy, gr, "url(#%sglb)" % p, INK, SW))
    b.append(_path("M%f,%f c4,-3 9,-2 10,2 c-3,4 -7,3 -8,8 c-3,-2 -4,-6 -2,-10 Z" % (gx - 10, gy - 5), "#6cae5a"))
    b.append(_path("M%f,%f c3,-1 7,2 6,7 c-1,3 -5,4 -7,2 Z" % (gx + 3, gy - 3), "#6cae5a"))
    b.append('<ellipse cx="%d" cy="%d" rx="6" ry="%d" fill="none" stroke="%s" stroke-width="0.8"/>' % (gx, gy, gr, INK))
    b.append(_line(gx - gr, gy, gx + gr, gy, INK, 0.8))
    # negotiating table across the front
    b.append(_rect(-5, 40, VW + 10, 30, "#24434b"))
    b.append(_path("M66,44 L186,44 L182,51 L70,51 Z", "#c49a5b", INK, SW))
    b.append(_rect(66, 42, 120, 3, "#dcb879", INK, 1.0))
    # papers + microphones on table
    for x in (80, 112, 144, 170):
        b.append(_rect(x, 39.5, 9, 3, "#fbf8f0", INK, 0.7))
        b.append(_line(x + 12, 42, x + 14, 35, INK, 1.0) + _circ(x + 14, 34.5, 1.3, INK))
    # lectern centre
    b.append(_path("M108,44 L128,44 L125,30 L111,30 Z", "#e9e1d0", INK, SW))
    b.append(_rect(109, 28, 18, 3, "#cfc4ae", INK, 1.1))
    b.append(_chip(VW - 4, 3, "OVERTIME", bg="#c0392b", anchor="end"))
    return _svg(w, h, "cop31-overtime", "".join(b), defs)


# --- 3. BepiColombo enters orbit around Mercury ---------------------------------------
def bepicolombo_mercury(w, h):
    p = "bepimerc"
    defs = (_rad(p + "pl", [(0, "#c9c4bc"), (0.7, "#8d8780"), (1, "#5d5852")], 0.3, 0.3, 0.8) +
            _lin(p + "plume", [(0, "#ffffff"), (0.4, "#9fd8ff"), (1, "#3b7fd0")], 1, 0) +
            '<clipPath id="%sclip"><circle cx="34" cy="44" r="40"/></clipPath>' % p)
    b = [_rect(-5, -5, VW + 10, VH + 10, "#0b0d16")]
    for k in range(34):
        x = (k * 53 + 11) % 191
        y = (k * 29 + 7) % 50
        r = 0.5 + (k % 3) * 0.3
        b.append(_circ(x, y, r, "#f4efe4", extra=' opacity="%.2f"' % (0.45 + (k % 4) * 0.13)))
    # Mercury, big, lower left
    b.append(_circ(34, 44, 40, "url(#%spl)" % p, INK, SW))
    cr = ['<g clip-path="url(#%sclip)">' % p]
    for (x, y, r) in [(20, 22, 6), (44, 14, 4), (52, 34, 7), (22, 44, 5), (62, 18, 3), (8, 34, 3.5), (40, 30, 2.5)]:
        cr.append(_circ(x, y, r, "#7a756e", "#5a554f", 0.8))
        cr.append(_path("M%f,%f a%f,%f 0 0 1 %f,%f" % (x - r * 0.8, y + r * 0.4, r, r, r * 1.6, 0), "none",
                        "#d4cfc7", 0.8))
    cr.append('</g>')
    b.append("".join(cr))
    # night-side shade
    b.append(_path("M74,44 A40,40 0 0 1 34,84 A46,46 0 0 0 74,44 Z", "#000", extra=' opacity="0.25"'))
    # orbit arc
    b.append('<ellipse cx="40" cy="40" rx="92" ry="22" fill="none" stroke="#f2c14e" stroke-width="1.4" '
             'stroke-dasharray="4 3" transform="rotate(-14 40 40)"/>')
    # spacecraft on the arc, upper right
    sx, sy = 126, 26
    g = ['<g transform="translate(%f %f) rotate(-14)">' % (sx, sy)]
    # thruster plume, trailing behind (to the right)
    g.append(_path("M7,-1.5 L30,-5 L33,0 L30,5 L7,1.5 Z", "url(#%splume)" % p, extra=' opacity="0.9"'))
    # solar wings (long)
    for side in (-1, 1):
        y0 = -4 if side < 0 else 4
        g.append(_line(0, 0, 0, side * 5, "#c8c8c8", 1.2))
        ww = 44
        g.append(_rect(-ww / 2 - 0, side * 5 + (0 if side > 0 else -7), ww, 7, "#2b4f9a", "#d9d9d9", 0.9))
        for k in range(1, 6):
            xx = -ww / 2 + k * ww / 6
            g.append(_line(xx, side * 5 + (0 if side > 0 else -7), xx, side * 5 + (7 if side > 0 else 0),
                           "#7fa2e0", 0.5))
    # box body with gold foil
    g.append(_rect(-7, -5, 14, 10, "#d9a63a", INK, 1.4, rx=1))
    g.append(_rect(-7, -5, 14, 3, "#f0cf72"))
    g.append(_rect(-7, -5, 14, 10, "none", INK, 1.4, rx=1))
    g.append(_circ(-10, 0, 3.2, "#e8e8e8", INK, 1.0))  # dish
    g.append('</g>')
    b.append("".join(g))
    b.append(_chip(VW - 4, 3, "IN ORBIT", bg="#f2c14e", fg=INK, anchor="end"))
    return _svg(w, h, "bepicolombo-mercury", "".join(b), defs)


# --- 4. Bitcoin at a two-year low, then bounces --------------------------------------
def bitcoin_two_year_low(w, h):
    p = "btclow"
    defs = (_lin(p + "bg", [(0, "#f6efe0"), (1, "#e8dcc4")]) +
            _rad(p + "coin", [(0, "#ffc35a"), (1, "#e2850f")], 0.35, 0.3, 0.8))
    b = [_rect(-5, -5, VW + 10, VH + 10, "url(#%sbg)" % p)]
    # chart grid
    for y in (12, 24, 36, 48):
        b.append(_line(62, y, 188, y, "#d3c6ad", 0.6))
    # price line
    pts = [(62, 8), (72, 12), (80, 10), (90, 18), (98, 16), (108, 26), (116, 24), (124, 34), (132, 32),
           (140, 44), (147, 37), (154, 40), (162, 30), (170, 33), (178, 26), (188, 22)]
    d = "M" + " L".join("%.1f,%.1f" % q for q in pts)
    b.append(_path(d + " L188,%d L62,%d Z" % (BAND + 4, BAND + 4), "#c0392b", extra=' opacity="0.13"'))
    b.append(_path(d, "none", "#b8322a", 2.2))
    b.append(_path("M147,37 L154,40 L162,30 L170,33 L178,26 L188,22", "none", "#2e8b57", 2.2))
    # low marker
    b.append(_circ(140, 44, 2.8, "#fff", INK, 1.4))
    # Bitcoin coin
    cx, cy, r = 30, 26, 21
    b.append(_circ(cx + 2, cy + 2, r, "#9c5a10", extra=' opacity="0.4"'))
    b.append(_circ(cx, cy, r, "url(#%scoin)" % p, INK, 2.0))
    b.append(_circ(cx, cy, r - 4, "none", "#b5650a", 1.2))
    b.append(_text(cx + 0.5, cy + 9.5, "&#8383;", 28, "#fff8e8"))
    b.append(_chip(VW - 4, 2, "$55,830 LOW", bg=INK, anchor="end"))
    return _svg(w, h, "bitcoin-two-year-low", "".join(b), defs)


# --- 5. England beat New Zealand 37-12 ------------------------------------------------
def england_nz_rugby(w, h):
    p = "engnz"
    defs = (_lin(p + "sky", [(0, "#a7c9de"), (1, "#dfe9e4")]) +
            _lin(p + "pitch", [(0, "#5f9e48"), (1, "#3f7d33")]) +
            _rad(p + "ball", [(0, "#ffffff"), (1, "#d8d2c6")], 0.35, 0.3, 0.8))
    b = [_rect(-5, -5, VW + 10, VH + 10, "url(#%ssky)" % p)]
    # stands
    b.append(_rect(-5, 22, VW + 10, 12, "#6d6a75"))
    for k in range(48):
        b.append(_circ(2 + k * 4, 25 + (k % 3) * 3, 1.3, ["#e8e2d4", "#c0392b", "#2b2b2b"][k % 3],
                       extra=' opacity="0.7"'))
    b.append(_rect(-5, 33, VW + 10, 40, "url(#%spitch)" % p))
    for x in range(-5, VW + 10, 24):
        b.append(_rect(x, 33, 12, 40, "#ffffff", extra=' opacity="0.06"'))
    # H posts on the left
    for (x1, y1, x2, y2) in [(12, 3, 12, 48), (42, 3, 42, 48), (12, 30, 42, 30)]:
        b.append(_line(x1, y1, x2, y2, INK, 4.4))
    for (x1, y1, x2, y2) in [(12, 3, 12, 48), (42, 3, 42, 48), (12, 30, 42, 30)]:
        b.append(_line(x1, y1, x2, y2, "#fbf8f0", 2.6))
    # rugby ball sailing between the posts
    b.append('<g transform="rotate(-30 30 15)">' +
             '<ellipse cx="30" cy="15" rx="9" ry="5.5" fill="url(#%sball)" stroke="%s" stroke-width="1.4"/>' % (p, INK) +
             _line(25, 15, 35, 15, "#c0392b", 1.1) +
             ''.join(_line(x, 13.5, x, 16.5, "#c0392b", 0.8) for x in (27.5, 30, 32.5)) + '</g>')
    b.append(_path("M44,22 q4,2 8,6", "none", "#fff", 1.0, ' opacity="0.8"'))
    # scoreboard: one label, two kit-coloured cells
    x0, y0, cw, ch = 58, 6, 62, 26
    b.append(_rect(x0 - 3, y0 - 3, 2 * cw + 6, ch + 6, "#2a2a2a", INK, SW, rx=3))
    b.append(_rect(x0, y0, cw, ch, "#fbf8f0", INK, 1.0))
    b.append(_rect(x0 + cw, y0, cw, ch, "#111111", INK, 1.0))
    b.append(_rect(x0, y0 + ch - 3, cw, 3, "#c8102e"))
    b.append(_line(x0 + 2 * cw - 30, y0 + ch + 3, x0 + 2 * cw - 30, BAND, "#4a4a4a", 2.0))
    b.append(_line(x0 + 30, y0 + ch + 3, x0 + 30, BAND, "#4a4a4a", 2.0))
    b.append('<text y="%.1f" font-family="%s" font-weight="700" font-size="18" letter-spacing="0.6">'
             '<tspan x="%.1f" text-anchor="middle" fill="%s">ENG 37</tspan>'
             '<tspan x="%.1f" text-anchor="middle" fill="#ffffff">NZ 12</tspan></text>'
             % (y0 + 19, FONT, x0 + cw / 2, INK, x0 + cw * 1.5))
    return _svg(w, h, "england-nz-rugby", "".join(b), defs)


# --- 6. Savar garment factories shut ---------------------------------------------------
def _worker(x, y, shirt, skin="#8a5a3b", s=1.0):
    return ('<g transform="translate(%f %f) scale(%f)">' % (x, y, s) +
            _rect(-3.2, -11, 6.4, 11, shirt, INK, 0.9, rx=2.5) +
            _rect(-2.6, -1, 2.2, 6, "#3b3b4a") + _rect(0.4, -1, 2.2, 6, "#3b3b4a") +
            _circ(0, -14, 3, skin, INK, 0.9) + '</g>')


def savar_closures(w, h):
    p = "savarsh"
    defs = (_lin(p + "sky", [(0, "#d5cfc0"), (1, "#efe7d6")]) +
            _lin(p + "sh", [(0, "#a3a8ad"), (1, "#7c8288")]))
    b = [_rect(-5, -5, VW + 10, VH + 10, "url(#%ssky)" % p)]
    b.append(_rect(-5, 46, VW + 10, 30, "#8e8676"))
    # three factory blocks with sawtooth roofs
    for i, (x, wd, col) in enumerate([(4, 58, "#c9b48f"), (66, 60, "#bfa27a"), (130, 58, "#c9b48f")]):
        top = 14 + (i % 2) * 2
        b.append(_rect(x, top, wd, 46 - top, col, INK, SW))
        # sawtooth roof
        n = 3
        tw = wd / n
        d = "M%f,%f" % (x, top)
        for k in range(n):
            d += " L%f,%f L%f,%f" % (x + k * tw, top - 7, x + (k + 1) * tw, top)
        b.append(_path(d + " Z", "#8c7a63", INK, 1.2))
        # window band
        for k in range(4):
            b.append(_rect(x + 4 + k * (wd - 8) / 4, top + 3, (wd - 8) / 4 - 3, 5, "#5d5446", INK, 0.6))
        # rolled-down shutter
        sx, sy, sw_, sh = x + 8, top + 12, wd - 16, 46 - top - 12
        b.append(_rect(sx, sy, sw_, sh, "url(#%ssh)" % p, INK, SW))
        yy = sy + 2.5
        while yy < sy + sh - 1:
            b.append(_line(sx + 1, yy, sx + sw_ - 1, yy, "#5f656b", 0.7))
            yy += 3
        # padlock at the bottom centre
        lx, ly = sx + sw_ / 2, sy + sh - 6
        b.append(_path("M%f,%f v-3 a3,3 0 0 1 6,0 v3" % (lx - 3, ly), "none", INK, 1.6))
        b.append(_rect(lx - 4.5, ly - 0.5, 9, 7, "#e0a43a", INK, 1.2, rx=1))
        b.append(_circ(lx, ly + 2.8, 1.0, INK))
    # a few workers waiting outside
    for (x, c) in [(62, "#c0392b"), (127, "#2f7d6e"), (133, "#e0a43a"), (186, "#3b5998")]:
        b.append(_worker(x, 47, c))
    b.append(_chip(VW / 2, 0, "SHUT", bg="#b8322a", anchor="middle"))
    return _svg(w, h, "savar-closures", "".join(b), defs)


# --- 7. Bayelsa boat capsize rescue ----------------------------------------------------
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
    p = "tinububy"
    defs = (_lin(p + "sky", [(0, "#cfdfe0"), (1, "#eae7d6")]) +
            _lin(p + "w", [(0, "#6f8f78"), (1, "#3f5f55")]))
    b = [_rect(-5, -5, VW + 10, VH + 10, "url(#%ssky)" % p)]
    b.append(_path("M-5,24 Q50,19 100,23 T196,21 L196,30 L-5,30 Z", "#4f7d4a"))  # far bank
    b.append(_rect(-5, 28, VW + 10, 50, "url(#%sw)" % p))
    for i in range(6):
        b.append(_line(24 + i * 28, 46 + (i % 3) * 2, 34 + i * 28, 46 + (i % 3) * 2, "#a9c2b4", 0.9,
                       ' opacity="0.7"'))
    b.append(_mangrove(8, 38, 1.0))
    b.append(_mangrove(185, 38, 1.0, flip=True))
    # capsized wooden boat, keel up, big
    b.append(_path("M18,40 Q50,14 88,38 Z", "#8a5a33", INK, 1.8))
    for k in range(1, 3):
        b.append(_path("M%f,%f Q51,%f %f,%f" % (18 + k * 5, 40 - k * 1.5, 14 + k * 6.5, 88 - k * 5, 38 - k * 1.5),
                       "none", "#5e3c22", 0.9))
    b.append(_path("M14,41 Q52,37 92,39", "none", "#d8e6dc", 1.6))
    # survivors in the water
    b.append(_circ(26, 42.5, 3, "#3a2a20", INK, 0.6) + _path("M22.5,45 q3.5,-2 7,0", "none", "#f07f1a", 2.2))
    b.append('<circle cx="98" cy="42" r="4.6" fill="none" stroke="#f07f1a" stroke-width="2.8"/>')
    b.append('<circle cx="98" cy="42" r="4.6" fill="none" stroke="#fff" stroke-width="2.8" stroke-dasharray="2 5"/>')
    b.append(_circ(98, 42, 2.6, "#3a2a20"))
    # rescue boat
    b.append(_path("M110,39 L172,39 L165,49 L117,49 Z", "#f4f1ea", INK, SW))
    b.append(_rect(113, 42, 56, 2.2, "#1f5fa8"))
    b.append(_path("M134,39 L134,30 L152,30 L157,39 Z", "#e3ddd0", INK, 1.1))
    b.append(_rect(137, 32, 11, 4.5, "#9cc8de", INK, 0.6))
    for x in (121, 164):
        b.append(_circ(x, 30, 3, "#3a2a20"))
        b.append(_rect(x - 3.5, 33, 7, 7, "#f07f1a", INK, 0.9, rx=1.5))
    b.append(_path("M120,35 L103,40", "none", "#3a2a20", 1.8))  # reaching to survivor
    b.append(_path("M110,46 Q100,49 90,47", "none", "#d8e6dc", 1.0))
    # Nigeria flag on mast
    b.append(_line(152, 30, 152, 8, "#5b4c3c", 1.3))
    b.append(_rect(153, 8, 7, 13, "#008751"))
    b.append(_rect(160, 8, 7, 13, "#ffffff"))
    b.append(_rect(167, 8, 7, 13, "#008751"))
    b.append(_rect(153, 8, 21, 13, "none", INK, 0.9))
    b.append(_chip(56, 0, "RESCUE", bg="#c0392b", anchor="middle"))
    return _svg(w, h, "tinubu-bayelsa-rescue", "".join(b), defs)


# --- 8. Australia home-birth rallies ---------------------------------------------------
def _au_flag(x, y, fw, cid):
    fh = fw / 2
    cw, chh = fw / 2, fh / 2
    g = ['<clipPath id="%s"><rect x="%f" y="%f" width="%f" height="%f"/></clipPath>' % (cid, x, y, cw, chh)]
    g.append(_rect(x, y, fw, fh, "#012169"))
    g.append('<g clip-path="url(#%s)">' % cid)
    g.append(_line(x, y, x + cw, y + chh, "#fff", 2.4) + _line(x + cw, y, x, y + chh, "#fff", 2.4))
    g.append(_line(x, y, x + cw, y + chh, "#c8102e", 0.8) + _line(x + cw, y, x, y + chh, "#c8102e", 0.8))
    g.append(_rect(x + cw / 2 - 1.8, y, 3.6, chh, "#fff") + _rect(x, y + chh / 2 - 1.8, cw, 3.6, "#fff"))
    g.append(_rect(x + cw / 2 - 1, y, 2, chh, "#c8102e") + _rect(x, y + chh / 2 - 1, cw, 2, "#c8102e"))
    g.append('</g>')
    g.append(_star(x + cw / 2, y + fh * 0.75, fw * 0.075, "#fff", n=7, ratio=0.45))
    for (fx, fy, r, n) in [(0.75, 0.83, 0.036, 7), (0.625, 0.47, 0.036, 7), (0.75, 0.17, 0.036, 7),
                           (0.87, 0.40, 0.036, 7), (0.80, 0.58, 0.022, 5)]:
        g.append(_star(x + fw * fx, y + fh * fy, fw * r, "#fff", n=n, ratio=0.45))
    g.append(_rect(x, y, fw, fh, "none", INK, 0.8))
    return "".join(g)


def homebirth_rallies(w, h):
    p = "homebirth"
    defs = _lin(p + "sky", [(0, "#a9d2ea"), (1, "#e9f1ee")])
    b = [_rect(-5, -5, VW + 10, VH + 10, "url(#%ssky)" % p)]
    b.append(_rect(-5, 44, VW + 10, 30, "#c9bfae"))
    # Australian flag on a pole, left
    b.append(_line(6, 3, 6, 50, "#6b5235", 1.8))
    b.append(_au_flag(7, 4, 44, p + "canton"))
    # placards (behind heads): hearts and houses
    for i, x in enumerate([70, 98, 126, 154, 180]):
        sx = x + (i % 2) * 2
        top = 18 + (i % 2) * 3
        b.append(_line(sx, top + 12, sx, 40, "#6b5235", 1.4))
        b.append(_rect(sx - 11, top, 22, 15, "#fbf8f0", INK, 1.3, rx=1))
        cy = top + 12
        if i % 2 == 0:
            b.append(_path("M%f,%f c-5.5,-3 -6.5,-8.5 -2.7,-9.5 c1.6,-0.4 2.7,0.6 2.7,1.7 c0,-1.1 1.1,-2.1 2.7,-1.7 "
                           "c3.8,1 2.8,6.5 -2.7,9.5 Z" % (sx, cy), "#d0281c"))
        else:
            b.append(_path("M%f,%f l7.5,-6.5 l7.5,6.5 l-2,0 l0,5.5 l-11,0 l0,-5.5 Z" % (sx - 7.5, cy - 3.5),
                           "#2f7d6e"))
            b.append(_rect(sx - 1.4, cy - 2, 2.8, 4, "#fbf8f0"))
    # crowd: two rows
    skins = ["#e6b98c", "#b07a52", "#d9a06e", "#7a4e31", "#f0c79a"]
    shirts = ["#2f7d6e", "#c0392b", "#e0a43a", "#3b5998", "#8e5aa8", "#4f8a3c"]
    for row, (y0, sp, off) in enumerate([(30, 11, 58), (36, 13, 54)]):
        x = off
        k = row * 2
        while x < VW + 6:
            b.append(_rect(x - 5, y0 + 6, 10, 18, shirts[k % len(shirts)], INK, 0.8, rx=4))
            b.append(_circ(x, y0 + 2, 4, skins[k % len(skins)], INK, 0.8))
            x += sp
            k += 1
    b.append(_chip(4, 31, "RALLIES", bg="#178a8a"))
    return _svg(w, h, "homebirth-rallies", "".join(b), defs)


ILLUS_B = {
    "peru-junin-m67": peru_junin_m67,
    "cop31-overtime": cop31_overtime,
    "bepicolombo-mercury": bepicolombo_mercury,
    "bitcoin-two-year-low": bitcoin_two_year_low,
    "england-nz-rugby": england_nz_rugby,
    "savar-closures": savar_closures,
    "tinubu-bayelsa-rescue": tinubu_bayelsa_rescue,
    "homebirth-rallies": homebirth_rallies,
}
