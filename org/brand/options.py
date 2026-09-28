from gen import BLUE, BLACK, head, sitting

def sleepy_head(c, cx, cy, r):
    # head with closed eyes (arcs)
    h = head(c, cx, cy, r)
    # cover open eyes with fur ellipses then draw arcs
    ex, ey = r*0.42, cy - r*0.08
    lc = "#2c3a4d" if c is BLUE else "#6a6d74"
    for s in (-1, 1):
        h += f'<ellipse cx="{cx+s*ex}" cy="{ey}" rx="{r*0.24}" ry="{r*0.27}" fill="{c["fur"]}"/>'
        h += f'<path d="M{cx+s*ex-r*0.17} {ey} q{r*0.17} {r*0.16} {r*0.34} 0" fill="none" stroke="{lc}" stroke-width="{r*0.07}" stroke-linecap="round"/>'
    return h

def loaf(c, cx, base, s=1.0, sleepy=False):
    body = f'<rect x="{cx-70*s}" y="{base-78*s}" width="{140*s}" height="{78*s}" rx="{38*s}" fill="{c["fur"]}"/>'
    hd = (sleepy_head if sleepy else head)(c, cx, base-88*s, 40*s)
    return body + hd

def svg(inner, w=440, h=300, bg="#ebebec"):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}"><rect width="{w}" height="{h}" fill="{bg}"/>{inner}</svg>\n'

opts = {}
# A: sitting side by side (current)
opts['A-sitting'] = svg(sitting(BLUE, 158, 270, 1.0, -1, 4) + sitting(BLACK, 282, 270, 1.0, 1, -4))
# B: sitting, looking at each other, tails crossed between them
opts['B-looking'] = svg(sitting(BLUE, 160, 270, 1.0, -1, 12, tilt=12) + sitting(BLACK, 280, 270, 1.0, 1, -12, tilt=-12))
heart = (f'<path d="M176 264 Q205 262 220 246 C176 212 178 158 220 186" fill="none" stroke="{BLUE["fur"]}" stroke-width="13" stroke-linecap="round" stroke-linejoin="round"/>'
         f'<path d="M264 264 Q235 262 220 246 C264 212 262 158 220 186" fill="none" stroke="{BLACK["fur"]}" stroke-width="13" stroke-linecap="round" stroke-linejoin="round"/>')
opts['F-tail-heart'] = svg(heart + sitting(BLUE, 130, 270, 1.0, 0, 4) + sitting(BLACK, 310, 270, 1.0, 0, -4))
# C: two loaves (cat loaf) side by side, one sleepy
opts['C-loaf'] = svg(loaf(BLUE, 140, 262, 1.0) + loaf(BLACK, 300, 262, 1.0, sleepy=True))
# D: black cat loaf in front, Russian Blue peeking from behind
peek = head(BLUE, 262, 150, 44, look=-6) + f'<ellipse cx="262" cy="196" rx="52" ry="30" fill="{BLUE["fur"]}"/>'
opts['D-peek'] = svg(peek + loaf(BLACK, 200, 272, 1.15))
# E: curled up asleep together (two round bodies, heads tucked)
def curl(c, cx, cy, r, flip=1):
    body = f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{c["fur"]}"/>'
    tail = f'<path d="M{cx-flip*r*0.9} {cy+r*0.45} C{cx-flip*r*0.2} {cy+r*1.15} {cx+flip*r*0.7} {cy+r*0.9} {cx+flip*r*0.95} {cy+r*0.35}" fill="none" stroke="{c["shade"]}" stroke-width="{r*0.2}" stroke-linecap="round"/>'
    return body + tail + sleepy_head(c, cx+flip*r*0.35, cy-r*0.25, r*0.55)
opts['E-sleeping'] = svg(curl(BLUE, 160, 190, 78, 1) + curl(BLACK, 285, 200, 78, -1))
for k, v in opts.items():
    open(f'opt-{k}.svg', 'w').write(v)
print(list(opts))
