# Winni Nav

A lightweight, no-backend web app for navigating Lake Winnipesaukee from your phone's GPS — like a Garmin HUD, but in Chrome.

## What it does

- **Live GPS dot** for your boat (phone GPS, ~3 m accuracy)
- **Speed** in knots + **heading** in degrees + **compass rose**
- **Public boat launches** — all 18+ NH launches with fees, parking notes, and restrictions
- **No-wake zones** — translucent overlays for Meredith Bay, Weirs Beach, Alton Bay, Wolfeboro Bay
- **Named hazards** — The Broads, Rocky Shoal, Five-Finger Point (informational only)
- **Crowdsourced buoys** — tap a button, tap the map, log any buoy you see while boating. Saves to your phone's localStorage. Export as JSON anytime.

## What it does NOT do (yet)

- **No official buoy data.** USCG ATON dataset is coastal-only — inland lake buoys on Winnipesaukee are maintained by NH Marine Patrol (~600 of them) and not published in machine-readable form. The printed **Bizer chart** sold at marinas is the authoritative source. Buoy layer is user-contributed; populate it by boating and tapping.
- **Not a navigation system.** Recreation aid. Always defer to official charts and visual markers.

## Files

```
winni-map/
├── index.html        ← The whole app (HTML + CSS + JS, single file)
├── README.md         ← This file
└── data/             ← Empty. Reserved for future tile caches or exports.
```

## How to use it

### Option 1: Open on your phone (no hosting needed)
1. Install **a-Shell** or **iSH** on iOS, or use any file manager on Android
2. Copy `index.html` to your phone
3. Open it in Chrome / Safari

Works, but **HTTPS is required for `navigator.geolocation`** in most browsers. So Option 2 is recommended.

### Option 2: GitHub Pages (free, recommended)
1. Create a GitHub repo, push `index.html`
2. Settings → Pages → Deploy from branch `main` → `/ (root)`
3. Visit `https://yourusername.github.io/repo-name/`
4. On your phone, open that URL in Chrome, tap **Start GPS**, grant location permission

The phone GPS will start updating your position on the map.

### Option 3: Any static host
Netlify, Vercel, Cloudflare Pages, S3 — all work. Just upload `index.html`.

### Option 4: Local server (testing)
```bash
cd winni-map
python3 -m http.server 8765
# open http://localhost:8765 in Chrome
```

## Crowdsourcing the buoys

Since official buoy data isn't freely available, the buoy layer is built by **you and your crew** while boating:

1. Open the app, tap **📍** (bottom-right) to enter buoy-add mode
2. Tap anywhere on the map where you see a buoy
3. Pick its color/type (red nun, green can, white/spar, yellow hazard)
4. Add an optional note (e.g. "marks submerged rock, white stripe")
5. Tap **Save**

Buoys are stored in your phone's `localStorage`. They persist across sessions on the same device/browser.

**Export** — tap 💾 to download your buoys as a JSON file. Share it with friends. I can merge multiple JSON files into a community dataset if this gets traction.

## How it works (technical)

- **Leaflet 1.9.4** for the map (CDN)
- **OpenStreetMap** tiles (free, no API key)
- **`navigator.geolocation.watchPosition`** with `enableHighAccuracy: true` for GPS
- **`DeviceOrientationEvent`** for compass heading on iOS (`webkitCompassHeading`) and Android (`alpha`)
- **`localStorage`** for buoy persistence
- **Single 32 KB HTML file** — no build step, no dependencies to install

## Data sources

- **Public launches:** [Roche Realty Lake Winnipesaukee launch list](https://rocherealty.com/boat-launches/), cross-checked with [lakewinnipesaukee.net](http://lakewinnipesaukee.net/boating/boat-launches-lakes-region-nh/)
- **No-wake zones:** Approximated from NH Marine Patrol descriptions. **Not authoritative** — verify on the Bizer chart.
- **Lake outline:** Hand-traced approximation. The actual shoreline is much more detailed. Acceptable as a background; not for navigation.
- **Buoys:** Community-contributed. Authoritative source: Bizer chart (paper) + NH Marine Patrol buoys on the water.

## Roadmap

- [ ] **v1.1** — Trip logging (record GPS trail, distance, max speed, downloadable GPX)
- [ ] **v1.2** — Bridge clearance markers (low-clearance bridges on Winni: Center Harbor, Egg Harbor)
- [ ] **v1.3** — Marina / restaurant / sand bar markers (POI layer)
- [ ] **v1.4** — Weather overlay (NOAA station at Wolfeboro)
- [ ] **v2.0** — Multi-user live tracking (backend, friends can see each other)

## License

MIT — do whatever you want with it. Credit appreciated but not required.

## Author

Built 2026-07-05 by GoodBot for Tyler.