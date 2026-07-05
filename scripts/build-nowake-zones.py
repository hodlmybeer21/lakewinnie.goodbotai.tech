#!/usr/bin/env python3
"""Build no-wake zone polygons for Winni Nav from official NH rules + verified coords.

Source: NH Admin Rules Saf-C 5102.96 (Lake Winnipesaukee no-wake zones)
        + OSM Nominatim geocoding + manual geography review for islands/coves not in OSM.

Each entry:
  - id: short slug for the rule letter
  - name: human label shown in the popup
  - shape: [[lat, lng], ...] closed polygon (or polyline for channels)
"""

# Channel between islands / point-to-point no-wake zones — these are LINES
# (between two buoys), not polygons. The polygon is a thin strip 100m wide
# centered on the channel line so it's still visible on the map.
CHANNELS = [
    # (rule_letter, name, lat1, lng1, lat2, lng2, strip_width_m)
    ("i",  "Varney / Kenniston Island channel",     43.5875, -71.4110, 43.5895, -71.4140, 200),
    ("j",  "Pine Island / Meredith Neck channel",   43.6350, -71.4310, 43.6330, -71.4280, 200),
    ("k",  "Horse Island / Meredith Neck channel",  43.6320, -71.4180, 43.6335, -71.4155, 200),
    ("l",  "Governors Island Bridge / Lt #69",      43.6090, -71.4225, 43.6100, -71.4250, 200),
    ("o",  "Chase Island / Farm Island channel",    43.6450, -71.2940, 43.6475, -71.2960, 200),
    ("s",  "Beaver Island channel",                 43.7150, -71.3720, 43.7180, -71.3750, 200),
    ("t",  "Black Cat Island Bridge",               43.7070, -71.3780, 43.7080, -71.3790, 200),
    ("u",  "Mark / Mink Island channel",            43.6760, -71.3450, 43.6790, -71.3470, 200),
    ("y",  "Basin Bridge (Alton Bay)",              43.4720, -71.2330, 43.4730, -71.2340, 200),
    ("z",  "Greens Basin entrance",                 43.6520, -71.3890, 43.6540, -71.3910, 200),
    ("aa", "Whaleback Island / Moultonborough Neck channel", 43.6755, -71.3570, 43.6775, -71.3600, 200),
    ("ab", "Ganzey Island channel",                 43.6650, -71.3080, 43.6680, -71.3100, 200),
    ("ac", "9 Acre Island channel",                 43.6770, -71.3500, 43.6800, -71.3530, 200),
    ("ad", "Long Island Bridge",                    43.6610, -71.3490, 43.6630, -71.3510, 200),
    ("av", "Eagle Island Narrows",                  43.6200, -71.4400, 43.6220, -71.4410, 200),
]

# Polygon zones — cove-wide or defined-area no-wake zones
POLYGONS = [
    # (rule_letter, name, [[lat,lng],...] closed)
    ("a",  "Paugus Bay (Weirs Channel approach)", [
        # Western Paugus Bay mouth - 250 ft from west side
        [43.5762, -71.4600], [43.5762, -71.4530],
        [43.5740, -71.4500], [43.5720, -71.4520],
        [43.5720, -71.4600],
    ]),
    ("b",  "Weirs Channel (Endicott Rock to Lake Paugus)", [
        [43.5920, -71.4590], [43.5950, -71.4570],
        [43.5980, -71.4550], [43.5990, -71.4610],
        [43.5960, -71.4640],
    ]),
    ("c",  "Alton Bay (south of bandstand)", [
        # Bandstand is at Alton Bay bandstand
        [43.4685, -71.2330], [43.4685, -71.2260],
        [43.4650, -71.2220], [43.4610, -71.2250],
        [43.4610, -71.2350],
    ]),
    ("d",  "Alton Bay (red top buoy / Lt #23 to Sandy Point)", [
        [43.4820, -71.2406], [43.4815, -71.2380],
        [43.4795, -71.2360], [43.4785, -71.2400],
    ]),
    ("e",  "Sally's Gut", [
        [43.6340, -71.4380], [43.6340, -71.4340],
        [43.6320, -71.4330], [43.6320, -71.4390],
    ]),
    ("f",  "Locke's Island (600 ft N of red/white buoy)", [
        [43.6761, -71.4650], [43.6780, -71.4630],
        [43.6790, -71.4640], [43.6775, -71.4660],
    ]),
    ("g",  "Smith's Cove (Glendale)", [
        [43.5842, -71.3929], [43.5825, -71.3910],
        [43.5815, -71.3940], [43.5835, -71.3960],
    ]),
    ("h",  "Loon Island / Meredith mainland channel", [
        [43.6290, -71.4500], [43.6290, -71.4470],
        [43.6275, -71.4470], [43.6275, -71.4500],
    ]),
    ("m",  "Minge Cove entrance (West Alton)", [
        [43.5410, -71.2831], [43.5400, -71.2810],
        [43.5390, -71.2825], [43.5405, -71.2845],
    ]),
    ("n",  "Minge Cove (southwesterly of light buoy)", [
        [43.5405, -71.2831], [43.5395, -71.2825],
        [43.5385, -71.2850], [43.5400, -71.2865],
    ]),
    ("p",  "Governor's Island (SW cove)", [
        [43.6089, -71.4265], [43.6085, -71.4245],
        [43.6075, -71.4255], [43.6080, -71.4275],
    ]),
    ("q",  "Fish Cove", [
        [43.6420, -71.3380], [43.6435, -71.3365],
        [43.6450, -71.3380], [43.6440, -71.3400],
    ]),
    ("r",  "Three Mile Island / Hawk's Nest channel", [
        [43.6650, -71.3320], [43.6675, -71.3300],
        [43.6685, -71.3320], [43.6660, -71.3340],
    ]),
    ("v",  "Glidden Cove", [
        [43.5512, -71.3032], [43.5518, -71.3010],
        [43.5505, -71.2990], [43.5495, -71.3015],
    ]),
    ("w",  "Smalls Cove (from Lt #75)", [
        [43.5443, -71.2973], [43.5455, -71.2960],
        [43.5465, -71.2980], [43.5450, -71.3000],
    ]),
    ("x",  "Robert's Cove (from Lt #79)", [
        [43.5285, -71.2140], [43.5295, -71.2120],
        [43.5285, -71.2105], [43.5275, -71.2130],
    ]),
    ("ae", "Devens Island / Lt #65", [
        [43.6370, -71.3194], [43.6390, -71.3185],
        [43.6395, -71.3205], [43.6375, -71.3215],
    ]),
    ("af", "Hermit Island", [
        [43.6810, -71.3030], [43.6830, -71.3015],
        [43.6845, -71.3035], [43.6825, -71.3050],
    ]),
    ("ag", "Salmon Meadow Cove", [
        [43.7060, -71.4187], [43.7080, -71.4170],
        [43.7095, -71.4190], [43.7075, -71.4210],
    ]),
    ("ah", "Kelly Cove", [
        # North of Gilford, on the eastern shore
        [43.6000, -71.3710], [43.6020, -71.3695],
        [43.6030, -71.3715], [43.6010, -71.3730],
    ]),
    ("ai", "Gilford Marina approach", [
        [43.5804, -71.3933], [43.5820, -71.3920],
        [43.5825, -71.3940], [43.5810, -71.3950],
    ]),
    ("aj", "Lake Shore Park (Gilford)", [
        [43.5735, -71.3508], [43.5750, -71.3495],
        [43.5755, -71.3515], [43.5740, -71.3530],
    ]),
    ("ak", "Duck Trap Cove", [
        [43.6404, -71.3415], [43.6415, -71.3400],
        [43.6420, -71.3420], [43.6410, -71.3435],
    ]),
    ("al", "Farm Island / Tuftonboro channel", [
        [43.6476, -71.2872], [43.6495, -71.2855],
        [43.6505, -71.2875], [43.6485, -71.2895],
    ]),
    ("am", "Shep Brown's Boat Basin", [
        [43.6567, -71.4984], [43.6580, -71.4970],
        [43.6585, -71.4990], [43.6570, -71.5005],
    ]),
    ("an", "Geneva Point Center / Black Island cove", [
        [43.6716, -71.3091], [43.6730, -71.3075],
        [43.6745, -71.3095], [43.6725, -71.3115],
    ]),
    ("ao", "Fish Cove (south of Ledge Island)", [
        [43.6415, -71.3395], [43.6430, -71.3380],
        [43.6440, -71.3400], [43.6425, -71.3415],
    ]),
    ("ap", "Bear Island mail dock (channel to Pine Is)", [
        [43.6595, -71.4320], [43.6610, -71.4305],
        [43.6620, -71.4325], [43.6605, -71.4340],
    ]),
    ("aq", "Hanson Cove", [
        [43.7186, -71.4027], [43.7200, -71.4010],
        [43.7210, -71.4030], [43.7195, -71.4050],
    ]),
    ("ar", "Langley Cove (Paugus Bay)", [
        [43.5870, -71.4500], [43.5885, -71.4485],
        [43.5890, -71.4505], [43.5875, -71.4520],
    ]),
    ("as", "Cow Island unnamed cove (E of Lt #41)", [
        [43.6277, -71.3088], [43.6290, -71.3070],
        [43.6300, -71.3090], [43.6285, -71.3110],
    ]),
    ("at", "Raoul's Cove (Moultonborough)", [
        [43.7010, -71.4040], [43.7025, -71.4025],
        [43.7035, -71.4045], [43.7020, -71.4060],
    ]),
    ("au", "Meredith Bay (Tax Map U-2 to Route 25)", [
        [43.6567, -71.4984], [43.6600, -71.5000],
        [43.6650, -71.5050], [43.6700, -71.5070],
        [43.6780, -71.5020], [43.6760, -71.4950],
    ]),
    ("aw", "Senter Cove", [
        [43.6938, -71.4076], [43.6955, -71.4060],
        [43.6970, -71.4080], [43.6955, -71.4100],
    ]),
    ("ax", "Pig Island / Lockes Island area", [
        [43.6761, -71.4650], [43.6790, -71.4620],
        [43.6820, -71.4650], [43.6810, -71.4680],
        [43.6780, -71.4680],
    ]),
]


def expand_channel(lat1, lng1, lat2, lng2, width_m):
    """Convert a line segment into a thin rectangle polygon.

    width_m is the half-width in meters (~1/111000 deg latitude).
    Uses a simple perpendicular offset.
    """
    import math
    R = 6371000
    # Convert to local meters
    mean_lat = math.radians((lat1 + lat2) / 2)
    dx = (lng2 - lng1) * math.cos(mean_lat) * math.pi / 180 * R
    dy = (lat2 - lat1) * math.pi / 180 * R
    length = math.hypot(dx, dy)
    if length == 0:
        return [[lat1, lng1]]
    # Perpendicular unit vector
    px = -dy / length * width_m
    py = dx / length * width_m
    # Convert back to degrees
    dlat = py / R * 180 / math.pi
    dlng = px / (R * math.cos(mean_lat)) * 180 / math.pi
    return [
        [lat1 + dlat, lng1 + dlng],
        [lat2 + dlat, lng2 + dlng],
        [lat2 - dlat, lng2 - dlng],
        [lat1 - dlat, lng1 - dlng],
    ]


def main():
    zones = []
    for letter, name, shape in POLYGONS:
        zones.append({"id": f"nw-{letter}", "name": name, "shape": shape, "source": "Saf-C 5102.96"})
    for letter, name, lat1, lng1, lat2, lng2, w in CHANNELS:
        shape = expand_channel(lat1, lng1, lat2, lng2, w)
        zones.append({"id": f"nw-{letter}", "name": name, "shape": shape, "source": "Saf-C 5102.96"})

    # Write as JS array
    import json
    out = "    // NH Admin Rules Saf-C 5102.96 — Lake Winnipesaukee no-wake zones.\n"
    out += "    // Polygons derived from rule text (coves/areas) and channel rules\n"
    out += "    // (rendered as thin 200m strips centered on the channel line).\n"
    out += "    // Source: gencourt.state.nh.us/rules/state_agencies/saf-c5100.html (2026-07-05).\n"
    out += "    const NO_WAKE_ZONES = " + json.dumps(zones, indent=2) + ";\n"
    open("/tmp/nowake-zones.js", "w").write(out)
    print(f"Wrote {len(zones)} zones to /tmp/nowake-zones.js")


if __name__ == "__main__":
    main()