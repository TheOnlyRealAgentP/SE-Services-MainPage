"""Build the interactive service-area map (inline SVG) from Census TIGER data.

usage: python3 -I area_map.py <geo/area dir> <business.yml> <out include>
"""
import json, math, re, sys

AREA, BIZ, OUT = sys.argv[1:4]

# ---- towns served (slug order from business.yml) ----------------------------
slugs = re.findall(r"slug: (\S+)", open(BIZ).read())
names = re.findall(r"- name: (.+)", open(BIZ).read())
counties = re.findall(r"county: (.+)", open(BIZ).read())
TOWNS = list(zip(slugs, names, counties))

places = {}
for fn in ("incorporated.geojson", "cdp.geojson"):
    for f in json.load(open(f"{AREA}/{fn}"))["features"]:
        p = f["properties"]
        places[p["NAME"].rsplit(" ", 1)[0]] = (f["geometry"], float(p["INTPTLON"]), float(p["INTPTLAT"]))
HUFFMAN = (-95.0858, 30.0272)   # GNIS/GeoNames point; Huffman is not a Census place

# ---- projection ---------------------------------------------------------------
LON0, LON1, LAT0, LAT1 = -95.275, -94.825, 29.595, 30.080
COSL = math.cos(math.radians((LAT0 + LAT1) / 2))
W = 960.0
K = W / ((LON1 - LON0) * COSL)
H = (LAT1 - LAT0) * K
def P(lon, lat): return ((lon - LON0) * COSL * K, (LAT1 - lat) * K)

def rdp(pts, eps):
    if len(pts) < 3: return pts
    (ax, ay), (bx, by) = pts[0], pts[-1]
    dx, dy = bx - ax, by - ay; L = math.hypot(dx, dy)
    best, idx = -1, 0
    for i in range(1, len(pts) - 1):
        px, py = pts[i]
        d = abs(dx * (py - ay) - dy * (px - ax)) / L if L else math.hypot(px - ax, py - ay)
        if d > best: best, idx = d, i
    if best > eps:
        return rdp(pts[:idx + 1], eps)[:-1] + rdp(pts[idx:], eps)
    return [pts[0], pts[-1]]

def clip_poly(pts, xmin=-20, ymin=-20, xmax=W + 20, ymax=None):
    """Sutherland-Hodgman clip against an expanded viewBox."""
    ymax = H + 20 if ymax is None else ymax
    def clip(pts, inside, inter):
        out = []
        for i in range(len(pts)):
            cur, prev = pts[i], pts[i - 1]
            if inside(cur):
                if not inside(prev): out.append(inter(prev, cur))
                out.append(cur)
            elif inside(prev):
                out.append(inter(prev, cur))
        return out
    def ix(x):  return lambda a, b: (x, a[1] + (b[1] - a[1]) * (x - a[0]) / (b[0] - a[0]))
    def iy(y):  return lambda a, b: (a[0] + (b[0] - a[0]) * (y - a[1]) / (b[1] - a[1]), y)
    for inside, inter in ((lambda p: p[0] >= xmin, ix(xmin)), (lambda p: p[0] <= xmax, ix(xmax)),
                          (lambda p: p[1] >= ymin, iy(ymin)), (lambda p: p[1] <= ymax, iy(ymax))):
        if not pts: break
        pts = clip(pts, inside, inter)
    return pts

def fmt(pts, close=True):
    if len(pts) < 2: return ""
    s = f"M{pts[0][0]:.1f} {pts[0][1]:.1f}"
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        s += f"l{x1 - x0:.1f} {y1 - y0:.1f}"
    s = s.replace(".0 ", " ").replace(".0l", "l")
    return s + ("z" if close else "")

def rings(geom):
    if geom["type"] == "Polygon": return geom["coordinates"]
    return [r for poly in geom["coordinates"] for r in poly]

def poly_path(geom, eps=0.7, clip=True):
    out = ""
    for ring in rings(geom):
        pts = [P(*c[:2]) for c in ring]
        if clip: pts = clip_poly(pts)
        if len(pts) < 3: continue
        pts = rdp(pts, eps)
        if len(pts) >= 3: out += fmt(pts)
    return out

def line_paths(geom, eps=0.8):
    lines = geom["coordinates"] if geom["type"] == "MultiLineString" else [geom["coordinates"]]
    out = ""
    for ln in lines:
        pts = [P(*c[:2]) for c in ln]
        seg = []
        for p in pts:   # keep runs that are near the map
            if -40 <= p[0] <= W + 40 and -40 <= p[1] <= H + 40: seg.append(p)
            else:
                if len(seg) > 1: out += fmt(rdp(seg, eps), close=False)
                seg = []
        if len(seg) > 1: out += fmt(rdp(seg, eps), close=False)
    return out

# ---- layers -------------------------------------------------------------------
water = json.load(open(f"{AREA}/water.geojson"))["features"]
water_d = "".join(poly_path(f["geometry"], 0.6) for f in water)

cty = {f["properties"]["NAME"]: f["geometry"] for f in json.load(open(f"{AREA}/counties.geojson"))["features"]}
county_d = "".join(poly_path(g, 0.8) for g in cty.values())

ROUTES = {   # route label -> names in TIGER
    "I-10": {"I- 10", "East Fwy", "Baytown Tunl"},
    "BW 8": {"Beltway 8", "State Loop 8", "S Sam Houston Pkwy E", "S Sam Houston Pkwy W", "Sidney Sherman Brg"},
    "SH 225": {"State Hwy 225", "La Porte Fwy", "Pasadena Fwy"},
    "SH 146": {"State Hwy 146", "Fred Hartman Brg", "La Porte Hwy"},
    "US 90": {"US Hwy 90", "Crosby Fwy"},
    "SH 99": {"State Hwy 99", "Grand Pkwy"},
}
roads = json.load(open(f"{AREA}/primary.geojson"))["features"] + json.load(open(f"{AREA}/secondary.geojson"))["features"]
road_d = "".join(line_paths(f["geometry"]) for f in roads if f["properties"]["NAME"] not in {"Hwy 59 Hov", "I- 45-Hov"})
road_pts = {k: [] for k in ROUTES}
for f in roads:
    for k, ns in ROUTES.items():
        if f["properties"]["NAME"] in ns:
            g = f["geometry"]; ls = g["coordinates"] if g["type"] == "MultiLineString" else [g["coordinates"]]
            road_pts[k] += [P(*c[:2]) for l in ls for c in l]
# shield positions: nearest route vertex to a chosen spot
SHIELD_AT = {"I-10": (-94.915, 29.81), "BW 8": (-95.17, 29.86), "SH 225": (-95.09, 29.705),
             "SH 146": (-94.985, 29.69), "US 90": (-95.125, 29.85), "SH 99": (-94.93, 29.93)}
shields = []
for k, (lo, la) in SHIELD_AT.items():
    tx, ty = P(lo, la)
    if road_pts[k]:
        x, y = min(road_pts[k], key=lambda p: (p[0] - tx) ** 2 + (p[1] - ty) ** 2)
        if 0 < x < W and 0 < y < H: shields.append((k, x, y))

# ---- towns ---------------------------------------------------------------------
LABEL = {  # dx, dy, anchor for each town label relative to its marker
    "channelview": (-12, -14, "end"), "baytown": (12, 22, "start"), "crosby": (12, 5, "start"),
    "highlands": (12, 5, "start"), "huffman": (12, 5, "start"), "mont-belvieu": (-12, -12, "end"),
    "deer-park": (-12, 20, "end"), "la-porte": (12, 18, "start"), "pasadena": (-12, 5, "end"),
}
town_svg = []
for slug, name, county in TOWNS:
    if name in places:
        geom, lon, lat = places[name]
        shape = f'<path class="am-shape" d="{poly_path(geom, 0.6)}"/>'
    else:
        lon, lat = HUFFMAN; shape = ""
    mx, my = P(lon, lat)
    dx, dy, anc = LABEL.get(slug, (12, 5, "start"))
    office = slug == "channelview"
    marker = (f'<circle class="am-dot am-office" cx="{mx:.1f}" cy="{my:.1f}" r="11"/>'
              f'<circle class="am-dot-core" cx="{mx:.1f}" cy="{my:.1f}" r="4.5"/>') if office else \
             f'<circle class="am-dot" cx="{mx:.1f}" cy="{my:.1f}" r="7"/>'
    sub = '<tspan class="am-sub" x="{x:.1f}" dy="17">Our office</tspan>'.format(x=mx + dx) if office else ""
    label = f'<text class="am-label" x="{mx + dx:.1f}" y="{my + dy:.1f}" text-anchor="{anc}">{name}{sub}</text>'
    town_svg.append(
        f'<a class="am-town" href="{{{{ include.prefix }}}}#{slug}" data-town="{slug}" aria-label="{name}, {county}">'
        f'{shape}{marker}{label}</a>')

# ---- static labels ---------------------------------------------------------------
def tlabel(cls, lon, lat, text, anchor="middle", rot=0):
    x, y = P(lon, lat)
    t = f' transform="rotate({rot} {x:.1f} {y:.1f})"' if rot else ""
    return f'<text class="{cls}" x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}"{t}>{text}</text>'
static = [
    tlabel("am-water-label", -95.115, 30.045, "Lake Houston"),
    tlabel("am-water-label", -94.93, 29.625, "Galveston Bay"),
    tlabel("am-water-label", -94.855, 29.69, "Trinity Bay", rot=-60),
    tlabel("am-water-label am-small", -95.045, 29.875, "San Jacinto River", rot=-75),
    tlabel("am-county", -95.235, 30.055, "HARRIS COUNTY", "start"),
    tlabel("am-county", -94.84, 29.95, "CHAMBERS CO.", "end"),
]
hx, hy = P(-95.275, 29.778)
static.append(f'<text class="am-city" x="{hx + 8:.1f}" y="{hy - 10:.1f}">&#8592; Downtown Houston</text>')
shield_svg = "".join(
    f'<g class="am-shield" transform="translate({x:.1f} {y:.1f})"><rect x="-{len(k) * 4.4 + 7:.1f}" y="-11" width="{len(k) * 8.8 + 14:.1f}" height="22" rx="5"/><text y="5" text-anchor="middle">{k}</text></g>'
    for k, x, y in shields)

# scale bar (5 miles) and north arrow
mi5 = 5 * 1.609344 / (111.32 * COSL) * COSL * K   # km -> deg lon -> px
sx, sy = 24, H - 28
scale = (f'<g class="am-scale" transform="translate({sx} {sy})"><rect width="{mi5:.1f}" height="6" rx="1"/>'
         f'<rect width="{mi5 / 2:.1f}" height="6" class="am-scale-alt"/><text x="0" y="-8">0</text>'
         f'<text x="{mi5:.1f}" y="-8" text-anchor="middle">5 mi</text></g>')
north = (f'<g class="am-north" transform="translate({W - 34:.0f} 40)"><path d="M0 -22 L9 8 L0 2 L-9 8 Z"/>'
         f'<text y="26" text-anchor="middle">N</text></g>')

svg = f'''<svg class="area-map" viewBox="0 0 {W:.0f} {H:.0f}" width="{W:.0f}" height="{H:.0f}" role="group" aria-labelledby="am-title-{{{{ include.id | default: 'a' }}}}">
<title id="am-title-{{{{ include.id | default: 'a' }}}}">Map of the communities we serve in East Harris County and Chambers County</title>
<rect class="am-land" width="{W:.0f}" height="{H:.0f}"/>
<path class="am-water" d="{water_d}"/>
<path class="am-county-line" d="{county_d}"/>
<path class="am-road" d="{road_d}"/>
{"".join(static)}
{shield_svg}
{"".join(town_svg)}
{scale}{north}
</svg>'''

header = ("{%- comment -%}\n  Service-area map, generated from U.S. Census TIGER data (town and county\n"
          "  boundaries, water, highways). Each town links to its section on\n"
          "  /service-area. Usage: {% include area-map.html prefix=\"/service-area\" id=\"home\" %}\n"
          "  (leave prefix empty on the service-area page itself). Do not edit by hand.\n{%- endcomment -%}\n")
open(OUT, "w").write(header + svg + "\n")
print(f"viewBox {W:.0f}x{H:.0f}, {len(svg)} bytes, shields: {[s[0] for s in shields]}")
