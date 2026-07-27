[README.md](https://github.com/user-attachments/files/30397647/README.md)
# RigDeck

**A phone cab panel for Euro Truck Simulator 2.**

RigDeck turns your phone into a second control screen for ETS2. A small
script runs on your gaming PC and your phone connects to it over your home
Wi-Fi — either through any web browser, or through a dedicated Android app that
finds the PC on the network automatically (no typing IP addresses).

Everything is driven off the game's own telemetry, so every readout is **live
and real** — speed, fuel, drive time, your current job, the lot. The control
switches send real key presses into the game, so they work exactly like using
the keyboard or wheel, just from your phone.

---

## What it does

### Controls — tap and hold switches on the phone
- **Electric windows** — left and right, up/down
- **Suspension** — front, rear, and trailer, raise/lower, plus a level reset
- **Lights** — headlights and high beam, with indicators that glow when they're
  actually on (they mirror the truck's real state, so they light up even if you
  use the keyboard or wheel)
- **Trailer** — couple/release (guarded with a hold-to-arm so you can't knock it
  by accident) and lift/drop trailer axle
- **Engine start** — but only once your seatbelt is on (see below)

### Seatbelt interlock
Tap the belt icon before the truck will start. The ignition is moved to a hidden
key that only the panel ever sends, so the engine **physically cannot start**
until you've buckled up — you can't fake it from the keyboard. The belt resets
at the start of every session, so it stays a proper pre-drive ritual. If the
engine ever starts unbuckled (a wheel button, auto-start), the panel shuts it
back off and plays a warning chime.

### Pre-drive walkaround — DVSA-style inspection
Use the in-game freecam to "walk" around your rig and tick off a real inspection
checklist on the phone. Items start **red** and turn **green** as you check them:

- **Unit (cab):** lights & indicators, mirrors & glass, wipers & washers, horn,
  tyres & wheel nuts, oil & coolant, air build-up & leaks, fifth wheel &
  mounting
- **Trailer:** kingpin locked (tug test), air lines & susies, trailer lights,
  trailer tyres, load security/doors, landing legs stowed, number plate &
  markers, brake check

The unit list holds for the whole session. The **trailer list wipes itself
every time you couple a new trailer**, so every load gets a fresh walkaround.

### Active job screen
A live consignment card showing:
- Cargo and gross weight
- Pickup and delivery (company + city)
- ETA and route distance
- Deadline and a countdown of time remaining (turns amber when you're short)
- The payout for the job
- A **LOADED / UNLOADED** tag that follows your actual trailer coupling — not
  the game's instant "loaded" flag

### Status screen
Drive time and full truck vitals in one place:
- Live speed, and **drive time until your mandatory rest**
- Route distance, odometer, and a resettable trip meter
- **Fuel** — level, range, and average consumption
- **AdBlue** level
- **Air pressure** and **brake temperature**
- **Engine** — oil temp and pressure, water temp, battery voltage
- **Wear** — engine, transmission, cabin, chassis, wheels

Anything running low or on a warning flips amber so you spot it at a glance.

### Job log with proof-of-delivery sheets
When you deliver a load, you press **JOB COMPLETED** — a button that only
becomes active once the game confirms the drop — and the run is filed into a
session job log. Failed or cancelled jobs file themselves automatically.

Tap any job to open a full **proof-of-delivery sheet**:
- Cargo, origin company, and destination
- Distance driven, game time, and **real time** at the wheel
- Fuel used and average consumption
- Average and top speed
- Income and revenue per km
- Fines picked up, cargo damage, and truck damage taken over the job
- Whether you delivered early or late
- **Driver and warehouse signatures** (handwritten style) and a free-text
  **comments box** you can fill in and save per job

### The Android app
- **Fullscreen** — no browser bars, just the panel
- **Keeps the screen awake** for the whole drive
- **Finds the PC automatically** on your network — no IP typing
- **Auto-reconnects** if the PC or script restarts
- Manual IP entry as a fallback, and a retry button if a scan comes up empty

---

## Setup

You need two things: the **script running on the PC**, and the **panel open on
your phone** (browser or app).

### 1. Telemetry plugin (one time)
The script reads live data from the game through a free telemetry plugin.

1. Download the latest `scs-telemetry.dll` from the SCS SDK plugin releases
   (RenCloud's `scs-sdk-plugin` on GitHub).
2. Put the DLL in your ETS2 install under:
   `...\Euro Truck Simulator 2\bin\win_x64\plugins\`
   (create the `plugins` folder if it isn't there).
3. Launch ETS2 once and accept the "advanced SDK features" prompt.

### 2. Python packages (one time)
On the gaming PC, with Python installed:

```
pip install flask truck-telemetry pydirectinput
```

### 3. Key bindings in ETS2
In **Options → Keys & Buttons**, with **Num Lock ON**, set:

| Function | Key |
|---|---|
| Left window up / down | Numpad 7 / Numpad 1 |
| Right window up / down | Numpad 9 / Numpad 3 |
| Front suspension up / down | Numpad 8 / Numpad 2 |
| Rear suspension up / down | Numpad 4 / Numpad 6 |
| Trailer suspension up / down | Numpad 0 / Numpad . |
| Suspension reset | Numpad 5 |
| Lift/drop trailer axle | Numpad − |
| Trailer attach/detach | T (default) |
| Light modes | L (default) |
| High beam | K (default) |
| **Engine start/stop** | **Numpad ∗** — and **remove E** from this bind |

Also in **Options → Gameplay**, turn **off "Automatic engine start"** — otherwise
pressing the throttle starts the engine and bypasses the seatbelt interlock.

### 4. Run it
On the PC:

```
python rigdeck.py
```

It prints a web address like `http://192.168.1.80:8600`.

- **Browser:** open that address on your phone (same Wi-Fi).
- **App:** just open the RigDeck app — it finds the PC by itself.

The first time, allow Python through **Windows Firewall for Private networks**
when prompted (this covers both the panel and the app's auto-discovery).

---

## Notes & tips

- The **game window must be focused** for the control switches to work — key
  presses go to whatever window is in front.
- Window and suspension switches are **hold-to-operate**, like real dashboard
  rockers.
- On Android, "Add to Home Screen" from a browser still shows the address bar
  (browsers only do full installs over HTTPS). The **app** is the way to get
  true fullscreen and keep-screen-awake.
- The job log and walkaround checks are **per session** — they clear when you
  stop the script.
- If a value ever shows "--" on your setup, the plugin may name that field
  differently in your version; the script has a `/debug` page that shows the raw
  telemetry so the field can be matched up.

---

## Requirements at a glance

- Euro Truck Simulator 2 on PC (Windows)
- The free SCS SDK telemetry plugin
- Python 3 with `flask`, `truck-telemetry`, `pydirectinput`
- A phone on the same Wi-Fi (Android for the app; any phone for the browser)
