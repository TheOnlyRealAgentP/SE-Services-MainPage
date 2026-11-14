"""Build a Harris County contour-map SVG from terrarium elevation tiles + Census boundary."""
import json, math, sys, glob, os
import numpy as np
from PIL import Image
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.path import Path

GEO, OUT = sys.argv[1], sys.argv[2]   # GEO: folder with harris.geojson and tiles/
Z = 11
files = sorted(glob.glob(f"{GEO}/tiles/{Z}-*.png"))
xs = sorted({int(os.path.basename(f).split("-")[1]) for f in files})
ys = sorted({int(os.path.basename(f).split("-")[2].split(".")[0]) for f in files})
H = np.zeros((len(ys) * 256, len(xs) * 256), dtype=np.float64)
for f in files:
    _, x, y = os.path.basename(f)[:-4].split("-"); x, y = int(x), int(y)
    a = np.asarray(Image.open(f).convert("RGB"), dtype=np.float64)
    elev_m = a[..., 0] * 256 + a[..., 1] + a[..., 2] / 256 - 32768
    r, c = (y - ys[0]) * 256, (x - xs[0]) * 256
    H[r:r + 256, c:c + 256] = elev_m * 3.28084        # feet
X0, Y0 = xs[0] * 256, ys[0] * 256                       # global mercator pixel origin

def gauss(a, sigma):
    r = int(3 * sigma); k = np.exp(-np.arange(-r, r + 1) ** 2 / (2 * sigma ** 2)); k /= k.sum()
    a = np.apply_along_axis(lambda v: np.convolve(np.pad(v, r, mode="edge"), k, "valid"), 1, a)
    return np.apply_along_axis(lambda v: np.convolve(np.pad(v, r, mode="edge"), k, "valid"), 0, a)
H = gauss(H, 2.2)

def merc(lon, lat):
    n = 2 ** Z * 256
    return (lon + 180) / 360 * n - X0, (1 - math.asinh(math.tan(math.radians(lat))) / math.pi) / 2 * n - Y0

g = json.load(open(f"{GEO}/harris.geojson"))["features"][0]["geometry"]
ring = np.array([merc(lo, la) for lo, la in g["coordinates"][0]])

def rdp(pts, eps):
    if len(pts) < 3: return pts
    a, b = pts[0], pts[-1]; ab = b - a; L = np.hypot(*ab)
    d = np.abs(ab[0] * (pts[:, 1] - a[1]) - ab[1] * (pts[:, 0] - a[0])) / L if L else np.hypot(*(pts - a).T)
    i = int(np.argmax(d))
    if d[i] > eps:
        return np.vstack([rdp(pts[:i + 1], eps)[:-1], rdp(pts[i:], eps)])
    return np.array([a, b])

ring_s = rdp(ring, 0.6)
# mask outside the county
yy, xx = np.mgrid[0:H.shape[0], 0:H.shape[1]]
inside = Path(ring_s).contains_points(np.c_[xx.ravel() + .5, yy.ravel() + .5]).reshape(H.shape)
Hm = np.ma.array(H, mask=~inside)
print("elevation ft inside county: min %.0f max %.0f" % (Hm.min(), Hm.max()))

levels = np.arange(10, Hm.max() + 10, 10)
cs = plt.contour(np.arange(H.shape[1]), np.arange(H.shape[0]), Hm, levels=levels)
minx, miny = ring_s[:, 0].min() - 8, ring_s[:, 1].min() - 8
W, Hh = ring_s[:, 0].max() + 8 - minx, ring_s[:, 1].max() + 8 - miny

def d_attr(pts):
    pts = pts - [minx, miny]
    out = "M" + " ".join(f"{p[0]:.1f} {p[1]:.1f}" for p in pts[:1])
    prev = pts[0]
    for p in pts[1:]:
        dx, dy = p - prev
        out += f"l{dx:.1f} {dy:.1f}"; prev = p
    return out.replace(".0 ", " ").replace(".0l", "l")

minor, major = [], []
for lev, segs in zip(cs.levels, cs.allsegs):
    for seg in segs:
        if len(seg) < 4: continue
        length = np.sum(np.hypot(*np.diff(seg, axis=0).T))
        closed = np.hypot(*(seg[0] - seg[-1])) < 1.5
        if length < 25 or (closed and length < 80): continue
        s = rdp(np.asarray(seg), 0.9)
        (major if int(round(lev)) % 50 == 0 else minor).append(d_attr(s))
outline = d_attr(ring_s) + "z"

svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.0f} {Hh:.0f}" width="{W:.0f}" height="{Hh:.0f}">'
       f'<!-- Harris County, TX: 10 ft elevation contours (index every 50 ft). Terrain: AWS Terrain Tiles (USGS NED / SRTM); boundary: U.S. Census TIGER. -->'
       f'<g fill="none" stroke-linejoin="round" stroke-linecap="round">'
       f'<path stroke="#8CCBF2" stroke-opacity=".26" stroke-width="1.1" d="{"".join(minor)}"/>'
       f'<path stroke="#B9DEF7" stroke-opacity=".5" stroke-width="1.8" d="{"".join(major)}"/>'
       f'<path stroke="#F0B7BB" stroke-opacity=".75" stroke-width="2.6" stroke-dasharray="10 6" d="{outline}"/>'
       f'</g></svg>\n')
open(OUT, "w").write(svg)
print(f"levels {len(levels)} minor {len(minor)} major {len(major)} size {len(svg)} bytes viewBox {W:.0f}x{Hh:.0f}")
