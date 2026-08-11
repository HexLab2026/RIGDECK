<div align="center">

# 🛰️ RIGDECK

### Your phone becomes the cab.

**A wireless control panel and dashboard for Euro Truck Simulator 2 & American Truck Simulator.**
Windows, suspension, lights, ignition, parking brake, hazards, wipers, diff lock, live fuel
range, job info and proof-of-delivery — all on your phone, over Wi-Fi, while you drive. The
panel even switches itself between pages depending on what you're doing.

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
- **Hazard lights** — latches on/off, flashes red round the edge while active.
- **Parking brake.**
- **Wipers.**
- **Lights** — headlight modes and high beam, each showing live on/off state.
- **Left & right windows** — hold to open, hold to close, independent per side.
- **Trailer couple / release** — hold for 0.6s to arm, so you can't drop a trailer by accident.
- **Cab & trailer lift axles.**
- **Differential lock.**
- **Air suspension** — front, rear, trailer, plus a level reset.

A couple of these (hazards, diff lock) read their state from the game when your telemetry
plugin reports it, and fall back to the button remembering its own state when it doesn't —
either way the light matches what you last told it to do.

### 🔄 The panel switches itself
RigDeck watches what the truck is doing and moves to the page you actually need, without you
reaching for it:

- **Come to a full stop** → jumps straight to **CONTROLS**, so the handbrake is right there.
- **Pull away** → after a couple of seconds of moving, back to **STATUS** for the drive.
- **Delivery completes** → straight to **ACTIVE JOB**, with the COMPLETE button ready.

Tap any tab yourself and the panel leaves you exactly where you put it — it won't fight you
mid-read. That pause lifts on its own once you're genuinely back on the road: after a few
seconds of continuous driving, or the moment you restart the engine if you'd parked up with it
off (covers fuel stops, ferries, rest breaks). A collection or delivery clears it either way, so
the cycle is always ready to go again next run.

Not for you? It's a single flag near the top of the script (`AUTO_TAB_SWITCH = True`) — flip it
off and the panel stays wherever you leave it, like it used to.

### 🚚 ACTIVE JOB
- Live route distance and ETA.
- Cargo status at a glance — **NO TRAILER**, **EMPTY**, or **LOADED**, worked out from the
  truck's actual cargo data rather than just whether a trailer's hitched (an owned trailer
  stays hitched permanently, so that alone can't tell you if it's running empty).
- **Proof of delivery** once a job's done — driver and warehouse signatures, sign off on the
  phone.

### 📊 STATUS
- Time to your next rest stop, route distance, odometer, resettable trip meter.
- **Self-learned fuel range.** RigDeck watches your actual burn rate over the last ~40km and
  works out how far you can really go — not the game's rough built-in guess. A small **•**
  next to the range figure means that learned number is live.
- A **fuel warning light** that goes red when your range won't cover the remaining route, amber
  when it's tight, green when you're fine — with enough hysteresis built in that it holds
  steady instead of flickering when your range sits right on the edge.
- AdBlue, air pressure, brake temperature, oil, water, battery.
- Wear on every major component — engine, transmission, cabin, chassis, wheels.

### 📋 JOBS
- A running log of every delivery — distance, time, pay.
- Notes on any job.

### 🔔 Extras
- Low-fuel and out-of-range chimes.
- Auto-discovery — the phone finds the PC by itself.
- Works fullscreen as a phone web-app (add to home screen).
- **Update notifications** — see [Updates](#-updates) below.

---

## 🚀 Getting started

### The easy way (Windows, pre-built app)
1. Download the latest **RigDeck.exe** from [Releases](https://github.com/HexLab2026/RIGDECK/releases/latest).
2. Run it. A small window shows a web address (like `http://192.168.1.20:8600`).
3. On your phone (same Wi-Fi), open that address in a browser — **Android** users can instead
   open the RigDeck app, which finds the PC automatically without typing the address.
   **iPhone/iPad** don't need an app at all: RigDeck is a normal web page, so Safari works
   exactly the same as the Android app does, just typing the address once instead of
   auto-discovering it.
4. Add it to your home screen for a fullscreen, app-like panel — this works in Safari on iOS
   too, not just Android.

**If it won't start** with a "Failed to load Python DLL" error, that's antivirus — see the
troubleshooting note in [`BUILD.md`](BUILD.md).

### Build it yourself
See [`BUILD.md`](BUILD.md) — one double-click on Windows and it compiles the exe for you.

---

### The telemetry plugin (required — RigDeck can't read the truck without this)

RigDeck doesn't talk to the game directly. It reads data written by a separate plugin —
[**RenCloud/scs-sdk-plugin**](https://github.com/RenCloud/scs-sdk-plugin) — that SCS Software's
own SDK uses to share live telemetry over shared memory. This is a one-time, unrelated install,
and it's just one file:

1. Download the latest build from the
   [**Releases page**](https://github.com/RenCloud/scs-sdk-plugin/releases/latest) (grab the
   `.zip` — the exact filename changes with each version, the Releases link above always points
   at whichever is current).
2. Unzip it. Inside you'll see a `Demo` folder, a `Win32` folder and a `Win64` folder — **you
   only want one file**: `Win64\scs-telemetry.dll`. Ignore everything else in the zip; the
   `Demo` folder is developer sample code, not something you install, and `Win32` is the old
   32-bit build almost nobody needs.
3. Copy that one file, `scs-telemetry.dll`, into **`bin/win_x64/plugins/`** inside your ETS2 or
   ATS install folder. That `plugins` folder usually doesn't exist yet on a fresh install — just
   create it, then drop the DLL straight in.
4. Do the same in your ATS install folder too if you play both — each game needs its own copy.
5. Launch the game. You'll get a one-off popup saying the SDK plugin has been activated — click
   OK. It only asks once per session.

If RigDeck's STATUS page just shows `--` everywhere, this is almost always why — check
`http://<pc-ip>:8600/debug` to see whether telemetry is actually connected.

---

## 🎮 One-time game setup

RigDeck sends its controls on keys chosen so they never clash with your normal driving keys or
common mods (ReShade, weather/season mods). A handful you bind once in-game
(Options → Key/Button Assignments):

| Control | Bind in-game to | Why |
|---|---|---|
| Engine start/stop | **Numpad ✳** (and remove `E`) | Makes the panel the only ignition |
| Parking brake | **Numpad ➕** | Panel-owned, no keyboard clash |
| Hazard lights | **\\** (backslash) | Panel-owned |
| Cab lift axle | **,** (comma) | Panel-owned |
| Differential lock | **.** (full stop) | Panel-owned |

Everything else already uses keys RigDeck registers for itself — windows on `[` `]` `;` `'`,
suspension and trailer axle on the numpad, wipers/lights/couple-release on their normal
defaults (`V` / `L` `K` / `T`). The panel lists the full set on startup if you ever need to
check.

---

## 📱 Android app, or just use the browser

The pre-built Android app is **Android only** — it's a thin wrapper that auto-discovers your PC
so you never have to type an address. The `android/` folder has the project; build it in Android
Studio, or sideload the APK from Releases.

**There's no iOS app, and you don't need one.** RigDeck is just a web page — open the address
shown in the RigDeck window (`http://<pc-ip>:8600`) in Safari on an iPhone or iPad and you get
the exact same panel, same controls, same live updates. The only thing the Android app adds on
top is auto-discovery so you don't have to type that address in; on iOS you type it once, add
the page to your home screen (Share → Add to Home Screen), and it behaves like an app from then
on — fullscreen, its own icon, no browser chrome.

Either way, it's a thin shell over the same server: the actual panel lives on the PC and is
served fresh each time, so you only need to rebuild the Android app if you're changing the
wrapper itself (icon, fullscreen behaviour, discovery). Ordinary panel updates just need the PC
exe rebuilt; reload the page on the phone (or fully close and reopen it) to pick them up — true
whether you're on the Android app or Safari.

---

## 🔄 Updates

RigDeck checks this repo on startup and every few hours. It never downloads or replaces
anything on its own — self-updating exes turned out to be unreliable against antivirus, so this
is deliberately hands-off:

- **On the PC** — the RigDeck window shows **UPDATE AVAILABLE — vX** with an **Open Download
  Page** button. Click it, download the new `RigDeck.exe` from the release, and replace the old
  one yourself.
- **On the phone** — a small notice tells you a new version's ready and to grab it from the
  RigDeck window on your PC. It's informational only; the phone can't install anything, since
  RigDeck itself lives on the PC.

*(For maintainers: publish a release and bump `version.json` — see [`BUILD.md`](BUILD.md).)*

Full version history: [`CHANGELOG.md`](CHANGELOG.md)

---

## ❓ FAQ

**Does this work on the real game / online?**
It reads telemetry and sends keypresses locally on your own PC. It's a personal convenience
panel, like using a numpad — but as with any input tool, use it within the rules of whatever
you're playing.

**Can it show the sat-nav map?**
No — the game's telemetry sends distances and times but not the map itself, so RigDeck shows
route info as numbers (ETA, distance, time to rest), not a moving map or turn-by-turn.

**My phone can't find the PC.**
Make sure both are on the same Wi-Fi, and allow RigDeck through the Windows firewall on
*private* networks when it asks. You can always type the address shown in the RigDeck window.

**Antivirus flagged the exe, or it won't start.**
A freshly-built PyInstaller exe with no code-signing certificate often trips a false positive,
and Defender can interfere with it unpacking at launch. Add a Defender exclusion for the folder
you keep RigDeck in (and your Temp folder) — see [`BUILD.md`](BUILD.md).

**Hazards / diff lock don't stay lit after I quit and restart.**
Some telemetry plugin builds don't report those two fields, so the button can't know what the
truck was doing before RigDeck connected — it starts back at OFF and one tap resyncs it. If your
plugin does report them, this doesn't apply; the light just follows the truck.

---

## 📄 Licence

Personal, non-commercial use. See [`LICENSE.txt`](LICENSE.txt).

Not affiliated with SCS Software. Euro Truck Simulator 2 and American Truck Simulator are
trademarks of their respective owners.

---

<div align="center">
<sub>RigDeck · a phone-based cab panel for people who like their trucks just so.</sub>
</div>
