#!/usr/bin/env python3
"""Pull NH GRANIT Lake Winnipesaukee shoreline and simplify for client."""
import json

with open('/tmp/winni-lake-outline.json') as f:
    pts = json.load(f)

print(f"Original: {len(pts)} points")

# Douglas-Peucker simplification
def perp_dist(p, a, b):
    if a == b:
        dx, dy = p[0]-a[0], p[1]-a[1]
        return (dx*dx + dy*dy) ** 0.5
    n = abs((b[0]-a[0])*(a[1]-p[1]) - (a[0]-p[0])*(b[1]-a[1]))
    d = ((b[0]-a[0])**2 + (b[1]-a[1])**2) ** 0.5
    return n / d

def simplify(points, eps):
    if len(points) < 3: return points
    dmax, idx = 0, 0
    for i in range(1, len(points)-1):
        d = perp_dist(points[i], points[0], points[-1])
        if d > dmax: dmax, idx = d, i
    if dmax > eps:
        left = simplify(points[:idx+1], eps)
        right = simplify(points[idx:], eps)
        return left[:-1] + right
    return [points[0], points[-1]]

# Eps ~ 0.0005 deg ≈ 55m at this latitude
simp = simplify(pts, 0.0005)
print(f"Simplified: {len(simp)} points (target ~250)")

out = {
    "comment": "Lake Winnipesaukee shoreline from NH GRANIT NHD Waterbody (objectid 24453). Douglas-Peucker simplified to ~250 points.",
    "outline": simp,
    "bbox": {"minLat": 43.4707, "maxLat": 43.7360, "minLng": -71.4992, "maxLng": -71.1827},
}

open('/tmp/winni-outline.json', 'w').write(json.dumps(out))
print("Saved /tmp/winni-outline.json")
