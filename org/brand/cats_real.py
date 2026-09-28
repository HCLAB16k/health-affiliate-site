import os
HERE = os.path.dirname(os.path.abspath(__file__))
# Semi-realistic sitting cats (original drawing). Base cat: head right, tail to the left.
def cat(fur, line, inner, iris, nose, whisker, look=3):
    body = ('<path d="M163 92 C163 70 167 48 170 30 C180 42 188 54 196 62 Q212 57 228 62 '
            'C236 50 244 38 252 26 C259 46 263 74 257 94 C258 114 248 131 233 141 '
            'C245 172 251 228 247 282 C246 293 236 297 226 293 L208 293 '
            'C172 296 142 294 130 274 C118 246 126 196 153 164 C164 150 165 124 163 92 Z" fill="%s"/>' % fur)
    tail = ('<path d="M150 292 C96 296 54 288 32 254 C24 240 32 231 41 238 '
            'C58 264 96 276 140 276 Z" fill="%s"/>' % fur)
    ears = ('<path d="M174 44 C181 54 187 60 193 65 L178 76 Z" fill="%s"/>'
            '<path d="M248 40 C246 52 243 62 238 68 L227 64 Z" fill="%s"/>' % (inner, inner))
    contours = ('<g fill="none" stroke="%s" stroke-width="1.6" stroke-linecap="round" opacity="0.9">'
                '<path d="M222 196 C226 236 227 266 224 292"/>'
                '<path d="M235 204 C238 240 238 268 236 292"/>'
                '<path d="M158 228 C177 248 183 270 179 292"/>'
                '<path d="M224 292 c-2 -5 -8 -5 -10 0 M238 293 c-2 -5 -8 -5 -10 0"/>'
                '</g>' % line)
    eyes = ''
    for ex, d in ((193, -1), (234, 1)):
        # sharp almond, outer corner raised
        o, i = ex + d*15, ex - d*13
        eyes += ('<path d="M%d 93 Q%d 82 %d 100 Q%d 107 %d 93 Z" fill="%s" stroke="#050505" stroke-width="1.5" stroke-linejoin="miter"/>' % (o, ex + d*2, i, ex + d*2, o, iris))
        eyes += '<ellipse cx="%d" cy="96" rx="2" ry="8.5" fill="#050505"/>' % (ex+look)
        eyes += '<circle cx="%d" cy="92" r="1.6" fill="#fff"/>' % (ex+look+3)
    face = ('<path d="M208 114 h12 l-6 7 z" fill="%s"/>'
            '<path d="M214 121 v4 M214 125 q-5 5 -10 2 M214 125 q5 5 10 2" fill="none" stroke="%s" stroke-width="1.4" stroke-linecap="round"/>' % (nose, line))
    wh = '<g stroke="%s" stroke-width="1" stroke-linecap="round" fill="none" opacity="0.85">' % whisker
    for dy, ang in ((0, -6), (5, 0), (10, 6)):
        wh += '<path d="M200 %d Q176 %d 150 %d"/>' % (118+dy, 116+dy+ang/2, 114+dy+ang)
        wh += '<path d="M228 %d Q252 %d 280 %d"/>' % (118+dy, 116+dy+ang/2, 114+dy+ang)
    wh += '</g>'
    return tail + body + ears + contours + eyes + face + wh

BLACK = dict(fur="#101114", line="#3a3d44", inner="#5e5358", iris="#f2c21b", nose="#3b3438", whisker="#c9cbd0")
BLUE  = dict(fur="#7b8ba2", line="#a6b4c7", inner="#b89aa3", iris="#86c86a", nose="#8e7d86", whisker="#eef1f5")

def pair(bg="#ebebec"):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 540 320">'
            + (f'<rect width="540" height="320" fill="{bg}"/>' if bg else '')
            + '<g>' + cat(**BLUE, look=3) + '</g>'
            + '<g transform="translate(540 0) scale(-1 1)">' + cat(**BLACK, look=3) + '</g>'
            + '</svg>\n')

def single(c, bg="#ebebec"):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 320"><rect width="300" height="320" fill="{bg}"/>' + cat(**c, look=0) + '</svg>\n'

if __name__ == '__main__':
    open(os.path.join(HERE,'real-pair.svg'),'w').write(pair())

    def icon():
        p = pair(bg=None)
        inner = p[p.index('>')+1:p.rindex('</svg>')]
        return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="135 -2 270 270">'
                '<rect x="135" y="-2" width="270" height="270" fill="#ffdd00"/>' + inner + '</svg>\n')

    open(os.path.join(HERE,'icon-real.svg'),'w').write(icon())
    open(os.path.join(HERE,'real-black.svg'),'w').write(single(BLACK, '#ffffff'))
