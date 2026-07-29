<div align="center">

# 🛰️ RIGDECK

### Your phone becomes the cab.

**A wireless control panel and dashboard for Euro Truck Simulator 2 & American Truck Simulator.**
Windows, suspension, lights, ignition, parking brake, hazards, live fuel range, job info and
proof-of-delivery — all on your phone, over Wi-Fi, while you drive.

*Driven by precision.*

</div>

---

## What is it?

RigDeck turns any phone, tablet or second screen into a proper truck cab panel. It runs a tiny
web server on your gaming PC that reads the game's live telemetry and lets you flick switches
that fire straight into the game — so your phone acts like the dashboard controls and info
screens of a real truck.

No wires. No Bluetooth pairing. Open the RigDeck app (or any browser) on the same Wi-Fi and it
finds your PC automatically.

---

## ✨ Features

### 🎛️ CONTROLS
- **Ignition** — hidden engine start/stop. The panel is the only thing that can start the truck.
- **Lights** — headlight modes and high beam.
- **Wipers** - glows red when activated
- **Left & right windows** — hold to open, hold to close, each side independent.
- **Parking brake** — latching button that mirrors the truck's real brake state.
- **Hazard lights** — flashes red on the panel while they're active.
- **Trailer couple / release** — hold-to-arm so you can't drop a trailer by accident.
- **Trailer axle lift / drop.**
- **Air suspension** — front, rear, trailer and a level reset.

### 🚚 ACTIVE JOB
- Live route distance and ETA.
- Delivery countdown with a late warning.
- Cargo, source and destination.
- **Proof of delivery** — sign off a completed job on the phone.

### 📊 STATUS
- Fuel level and a **self-learning fuel range** — RigDeck watches your real consumption and
  works out how far you can actually go, not the game's rough guess.
- AdBlue, air pressure, brake temp, oil, water, battery.
- Component wear.

### 📋 JOBS
- A running log of every delivery with times, distance and pay.
- Add notes to any job.

### 🔔 Extras
- Low-fuel and out-of-range chimes.
- Auto-discovery — the phone finds the PC by itself.
- Works fullscreen as a phone web-app (add to home screen).
- **Auto update check** — tells you when a new version is out.

---

## 🚀 Getting started

### The easy way (Windows, pre-built app)
1. Download the latest **RigDeck.exe** from [Releases](https://github.com/HexLab2026/RIGDECK/releases/latest).
2. Run it. A small window shows a web address (like `http://192.168.1.20:8600`).
3. On your phone (same Wi-Fi), open that address in a browser — or open the RigDeck Android app,
   which finds the PC automatically.
4. Add it to your home screen for a fullscreen, app-like panel.

### Build it yourself
See [`BUILD.md`](BUILD.md) — one double-click on Windows and it compiles the exe for you.

---

## 🎮 One-time game setup

RigDeck sends its controls on **numpad and punctuation keys** so they never clash with your
normal driving keys. A few of them you bind once in-game (Options → Keys):

| Control | Bind in-game to | Why |
|---|---|---|
| Engine start/stop | **Numpad ✳** (and remove `E`) | Makes the panel the only ignition |
| Parking brake | **Numpad ➕** | Panel-owned, no keyboard clash |
| Hazard lights | **Numpad ➗** | Panel-owned |

Everything else (windows, suspension, lights, trailer) uses keys RigDeck already sends —
the panel lists them on first run. Window controls sit on the `[ ] ; '` keys specifically so
they don't fight with ReShade or weather/season mods.

You'll also need the telemetry plugin (the SCS SDK plugin) in your game's `plugins` folder —
this is what lets RigDeck read the truck's data. RigDeck tells you if it's missing.

---

## 📱 The Android app

The `android/` folder has the companion app: a fullscreen wrapper that auto-discovers your PC
so you never type an address. Build it in Android Studio, or sideload the APK from Releases.

---

## 🔄 Updates

RigDeck checks this repo on startup and every few hours. When a newer version is out:

- **On the PC** — the RigDeck window shows **UPDATE AVAILABLE** with an **Update Now** button.
  Click it and RigDeck downloads the new version, swaps itself out and restarts. Nothing happens
  until you click.
- **On the phone** — a small notice appears saying a new version is ready and to install it from
  the RigDeck window on your PC. (The phone can't update the app — RigDeck lives on the PC — so
  the notice just points you there.)

*(For maintainers: publish a release and bump `version.json` — see [`BUILD.md`](BUILD.md).)*

---

## ❓ FAQ

**Does this work on the real game / online?**
It reads telemetry and sends keypresses locally on your own PC. It's a personal convenience
panel, like using a numpad — but as with any input tool, use it within the rules of whatever
you're playing.

**Can it show the sat-nav map?**
No — the game's telemetry sends distances and times but not the map itself, so RigDeck shows
route info as numbers (ETA, distance, time to rest), not a moving map.

**My phone can't find the PC.**
Make sure both are on the same Wi-Fi, and allow RigDeck through the Windows firewall on
*private* networks when it asks. You can always type the address shown in the RigDeck window.

**Antivirus flagged the exe.**
A freshly-built PyInstaller exe with no code-signing certificate often trips a false positive.
Building it yourself from source (see BUILD.md) avoids this.

---

## 📄 Licence

Personal, non-commercial use. See [`LICENSE.txt`](LICENSE.txt).

Not affiliated with SCS Software. Euro Truck Simulator 2 and American Truck Simulator are
trademarks of their respective owners.

---

<div align="center">
<sub>RigDeck · a phone-based cab panel for people who like their trucks just so.</sub>
</div>
