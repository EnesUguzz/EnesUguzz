import sys
from collections import deque
from PIL import Image, ImageOps, ImageEnhance, ImageFilter
src, W, H = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
INV = len(sys.argv) > 4 and sys.argv[4] == 'invert'
rgb = Image.open(src).convert("RGB")
w, h = rgb.size
rgb = rgb.crop((int(w*0.10), 0, int(w*0.90), h))
small = rgb.resize((W, H), Image.LANCZOS)
g = ImageOps.autocontrast(small.convert("L"), cutoff=1)
g = ImageEnhance.Contrast(g).enhance(1.25)
P = small.load(); G = g.load()
bgc = P[0, 0]
def near(c): return sum(abs(a-b) for a, b in zip(c, bgc)) < 34
bg = [[False]*W for _ in range(H)]
q = deque([(x, 0) for x in range(W)] + [(0, y) for y in range(H)] + [(W-1, y) for y in range(H)])
while q:
    x, y = q.popleft()
    if not (0 <= x < W and 0 <= y < H) or bg[y][x] or not near(P[x, y]): continue
    bg[y][x] = True
    q.extend([(x+1, y), (x-1, y), (x, y+1), (x, y-1)])
ramp = ".:-=+*#%@"
out = []
for y in range(H):
    r = ""
    for x in range(W):
        if bg[y][x]: r += " "; continue
        v = G[x, y] / 255
        if INV: v = 1 - v
        r += ramp[min(len(ramp)-1, int(v * len(ramp)))]
    out.append(r.rstrip())
print("\n".join(out))
