# Two cat characters: Russian Blue (blue-grey, green eyes) and black cat (amber eyes)
BLUE = dict(fur="#7f93ab", shade="#6b7f98", ear="#e9a9b4", eye="#8fd46f", nose="#e9a9b4")
BLACK = dict(fur="#141518", shade="#2a2c31", ear="#3a3c42", eye="#ffcc1a", nose="#3a3c42")
INK = "#0b2559"

def head(c, cx, cy, r=42, look=0):
    # ears
    e = (f'<path d="M{cx-r*0.95} {cy-r*0.35} L{cx-r*0.78} {cy-r*1.35} L{cx-r*0.2} {cy-r*0.9} Z" fill="{c["fur"]}"/>'
         f'<path d="M{cx+r*0.95} {cy-r*0.35} L{cx+r*0.78} {cy-r*1.35} L{cx+r*0.2} {cy-r*0.9} Z" fill="{c["fur"]}"/>'
         f'<path d="M{cx-r*0.8} {cy-r*0.55} L{cx-r*0.72} {cy-r*1.1} L{cx-r*0.38} {cy-r*0.85} Z" fill="{c["ear"]}"/>'
         f'<path d="M{cx+r*0.8} {cy-r*0.55} L{cx+r*0.72} {cy-r*1.1} L{cx+r*0.38} {cy-r*0.85} Z" fill="{c["ear"]}"/>')
    face = f'<ellipse cx="{cx}" cy="{cy}" rx="{r*1.08}" ry="{r*0.95}" fill="{c["fur"]}"/>'
    ex, ey = r*0.42, cy - r*0.08
    eyes = ''.join(
        f'<ellipse cx="{cx+s*ex+look}" cy="{ey}" rx="{r*0.2}" ry="{r*0.24}" fill="{c["eye"]}"/>'
        f'<ellipse cx="{cx+s*ex+look}" cy="{ey}" rx="{r*0.055}" ry="{r*0.19}" fill="#0a0a0a"/>'
        f'<circle cx="{cx+s*ex+look+r*0.06}" cy="{ey-r*0.09}" r="{r*0.04}" fill="#fff"/>' for s in (-1, 1))
    ny = cy + r*0.28
    nose = f'<path d="M{cx-r*0.1} {ny} h{r*0.2} l-{r*0.1} {r*0.1} z" fill="{c["nose"]}"/>'
    mouth = (f'<path d="M{cx} {ny+r*0.1} q-{r*0.06} {r*0.14} -{r*0.16} {r*0.08} M{cx} {ny+r*0.1} q{r*0.06} {r*0.14} {r*0.16} {r*0.08}" '
             f'fill="none" stroke="{c["shade"] if c is BLUE else "#4a4c52"}" stroke-width="{r*0.045}" stroke-linecap="round"/>')
    wc = "#dfe5ee" if c is BLUE else "#5a5d64"
    wh = ''.join(f'<path d="M{cx+s*r*0.35} {ny+r*0.02+d} L{cx+s*r*1.25} {ny-r*0.06+d*2.2}" stroke="{wc}" stroke-width="{r*0.035}" stroke-linecap="round"/>' for s in (-1, 1) for d in (-r*0.05, r*0.08))
    return e + face + eyes + nose + mouth + wh

def sitting(c, cx, base, s=1.0, tail_dir=1, look=0, tilt=0, tail=True):
    r = 42*s
    body = f'<path d="M{cx-48*s} {base} C{cx-58*s} {base-60*s} {cx-40*s} {base-110*s} {cx} {base-112*s} C{cx+40*s} {base-110*s} {cx+58*s} {base-60*s} {cx+48*s} {base} Z" fill="{c["fur"]}"/>'
    chest = f'<path d="M{cx-20*s} {base} C{cx-24*s} {base-40*s} {cx-12*s} {base-70*s} {cx} {base-72*s} C{cx+12*s} {base-70*s} {cx+24*s} {base-40*s} {cx+20*s} {base} Z" fill="{c["shade"]}" opacity="0.55"/>'
    paws = ''.join(f'<ellipse cx="{cx+d*s}" cy="{base-4*s}" rx="{13*s}" ry="{8*s}" fill="{c["fur"]}"/>' for d in (-18, 18))
    t = tail_dir
    tail = f'<path d="M{cx+t*40*s} {base-8*s} C{cx+t*95*s} {base-10*s} {cx+t*100*s} {base-70*s} {cx+t*72*s} {base-92*s}" fill="none" stroke="{c["fur"]}" stroke-width="{15*s}" stroke-linecap="round"/>'
    hy = base-138*s
    hd = f'<g transform="rotate({tilt} {cx} {hy+r})">' + head(c, cx, hy, r, look) + '</g>'
    return (tail if tail_dir else '') + body + chest + paws + hd

def pair(w=440, h=300, bg=None):
    base = h - 30
    g = (sitting(BLUE, w*0.36, base, 1.0, -1, look=4) + sitting(BLACK, w*0.64, base, 1.0, 1, look=-4))
    rect = f'<rect width="{w}" height="{h}" fill="{bg}"/>' if bg else ''
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}">{rect}{g}</svg>\n'

def icon(size=512):
    s = size/512
    g = head(BLUE, 150*s, 275*s, 100*s, look=5*s) + head(BLACK, 362*s, 292*s, 100*s, look=-5*s)
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}"><rect width="{size}" height="{size}" fill="#ffdd00"/>{g}</svg>\n'

open('cats-pair.svg', 'w').write(pair())
open('icon.svg', 'w').write(icon())
