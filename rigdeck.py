"""
==========================================================================
  rigdeck.py  —  RIGDECK  ·  v3.8
==========================================================================
  Phone-screen cab panel for Euro Truck Simulator 2.

  CONTROLS page : electric windows (left + right, up/down), chassis
                  suspension raise/lower, trailer couple/release
  TACHO page    : drive time until rest, distance + ETA to delivery,
                  odometer, resettable trip meter, live speed
                  v1.1 — CONSIGNMENT card:
                    cargo carried, gross weight, pickup company + city,
                    delivery company + city, collect/loaded state
                  NEW v1.2 — DUE (deadline, game day + clock),
                    LEFT (time remaining, amber under 2 h, flags LATE),
                    INCOME (job payout, €)
                  NEW v1.4 — LIGHTS (headlights + high beam, buttons lit
                    from live telemetry so they mirror keyboard use too),
                    suspension split into FRONT / REAR raise-lower plus
                    RESET, and a new RIG page: fuel level/range/average,
                    AdBlue, air pressure, brake temp, oil, water,
                    battery, and per-component wear.
                  NEW v1.5 — TRAILER suspension raise/lower (hold pair)
                    and LIFT/DROP TRAILER AXLE (single toggle, lit from
                    telemetry: LIFTED / DOWN).
                  NEW v1.7 — ANDROID APP SUPPORT: answers discovery
                    pings on UDP 8721 so the RigDeck Android app
                    finds this PC automatically (no IP typing). If
                    Windows Firewall asks again, allow python.exe on
                    Private networks (covers UDP too).
  JOBS page     : NEW v1.8 — session log. Every job is tracked live on
                    the server: LOADED/UNLOADED now follows actual
                    trailer coupling, the consignment chip reads
                    ON ROUTE while a job is active, and each finished
                    job lands in the JOBS tab as COMPLETED or FAILED.
                    Tap a job for the full readout: distance, game time,
                    real time at the wheel, fuel used, avg consumption,
                    avg + top speed, income, EUR/km, fines picked up,
                    cargo damage, truck damage taken, early/late margin.
                    Log is per session (clears when this script exits).
  v3.8          : DIFF LOCK + AUTO TAB SWITCHING, and three real bug fixes.
                    ADDED
                      - CONTROLS: DIFF LOCK button (own plate, below
                        LIFT / DROP). Bind "." (full stop) in-game.
                      - Auto tab switching: driving shows STATUS, stopping
                        brings CONTROLS back for the handbrake, and a
                        completed delivery jumps to ACTIVE JOB so COMPLETE
                        is under your thumb. Tapping any tab yourself
                        suspends it until the next drop. Tunable via
                        AUTO_TAB_SWITCH / AUTO_TAB_MOVE_SEC /
                        AUTO_TAB_STOP_SEC.
                      - Tap-style bars (wipers, axles, susp reset, diff)
                        now depress when pressed like the square tiles
                        already did.
                    FIXED
                      - Taps could be missed by the game entirely.
                        pydirectinput.press() fires keyDown and keyUp with
                        no gap, so the key was down for well under a
                        millisecond — shorter than one frame at 60fps. A
                        real finger holds ~100ms. Taps now hold for
                        TAP_HOLD_SEC (80ms). DIFF LOCK never worked at all
                        because of this; every other tap button was
                        intermittent depending on frame timing.
                      - ACTIVE JOB always read LOADED with an owned
                        trailer. Cargo state was inferred from whether a
                        trailer was coupled, which only works for market
                        trailers (you couple up when you collect). An
                        owned trailer stays hitched, so it read LOADED
                        while running empty. Now uses real cargo data
                        (isCargoLoaded, falling back to cargo mass) and
                        shows NO TRAILER / EMPTY / LOADED.
                      - Fuel warning light flicked on and off. When the
                        consumption model briefly lost its sample window
                        (a gap in polling while the phone screen slept, a
                        ferry, a refuel) the range silently fell back to
                        the game's own estimate — a very different number
                        — then jumped back, tripping the light either way.
                        The learned burn rate is now held across short
                        dropouts and range recomputed from current fuel;
                        it only falls back to the game figure after 15
                        minutes with no model.
                      - DIFF LOCK and HAZARD lights would not stay on.
                        Both read telemetry fields (differentialLock,
                        lightsHazards) that this plugin does not report,
                        so the light was cleared on the next poll. Both
                        now use telemetry when it is available and
                        otherwise track their own state.
                      - Auto tab switching stopped for the rest of the
                        session if you changed tab once. The pause was
                        only lifted on the "pending" edge, and pending
                        only clears when the JOB COMPLETED button is
                        pressed — skip that press and the edge never
                        fired again. Delivery and collection are now
                        detected from cargo entering/leaving the trailer
                        in telemetry, so the cycle resumes every run, and
                        a bounded AUTO_TAB_HOLD_SEC backstop means a
                        pause can never last indefinitely.
                    KNOWN LIMITS
                      - Because the plugin does not report hazard or diff
                        state, quitting with either engaged shows it OFF
                        on restart; one tap resyncs. If a future plugin
                        reports those fields the buttons switch to the
                        real state automatically.
  v3.7          : WIPERS control added to the IGNITION plate as a full
                    width bar (bind V). Fuel range warning given a
                    hysteresis dead-band so it stops chattering when
                    range sits near the route distance. Tab bar given
                    bigger tap targets. Carrier name removed from the POD
                    sheet. Fixed PARK BRAKE tile being a different height
                    to its neighbours when its label wrapped.
  v3.6          : CAB AXLE lift button added above TRAILER AXLE (bind ",").
                    HAZARD button changed to a plain latch after /debug
                    confirmed this plugin never reports hazard state.
                    Self-updating exe dropped in favour of a notice plus
                    a browser link to the release, after the download and
                    file-swap proved unreliable against antivirus.
  v3.5          : Window controls moved off the numpad onto the
                    punctuation cluster ([ ] ; ') to stop them clashing
                    with ReShade and weather mods. GitHub update checking
                    added: the phone shows a passive notice, the PC window
                    shows the actionable one.
  v3.4          : HAZARD LIGHTS button added to the IGNITION plate,
                    between START and PARK BRAKE. Bind Numpad / in-game
                    to the hazard warning lights; the button latches
                    amber and mirrors the live hazard state.
  v3.3          : Fuel consumption model now records a sample once a
                    minute instead of every poll. Smoother average, same
                    live range read-out and alert on the panel.
  v3.2          : PARKING BRAKE button added to the IGNITION plate,
                    next to START. Bind Numpad + in-game to the parking
                    brake; the button latches and mirrors the live brake
                    state from telemetry.
  v3.1          : Seatbelt interlock and the pre-drive walkaround
                    checklist removed at the operator's request. The
                    PRE-DRIVE tab is gone; engine START now lives on
                    the CONTROLS page. Low-fuel and fuel-range alerts
                    are unaffected.
  v3.0          : RIGDECK — new name, mark, palette (gunmetal /
                    steel / safety orange) and type.
  v1.9          : HIDDEN IGNITION — engine start/stop lives on Numpad *
                    in-game, a key only this panel ever sends, so the
                    truck starts from the panel rather than the keyboard.
  v2.2          : TAB RESTRUCTURE + PROOF OF DELIVERY.
                    Tabs are now CONTROLS / ACTIVE JOB / STATUS / JOBS. ACTIVE JOB shows the live consignment
                    (cargo, weight, from/to, ETA, deadline, pay); STATUS
                    carries drive-time-to-rest plus all the truck vitals
                    (fuel, AdBlue, air, brakes, oil, water, battery,
                    wear). A delivered job no longer auto-files: the
                    JOB COMPLETED button on ACTIVE JOB stays red/disabled
                    until the game confirms delivery, then goes green -
                    press it to file the run into JOBS. Failed/cancelled
                    jobs still auto-file as FAILED. Each filed job opens
                    as a proof-of-delivery sheet: cargo, origin company,
                    destination, full stats, driver + warehouse
                    signatures (handwritten SVG, pulled from a pool so
                    they vary), and a free-text COMMENTS box saved per
                    job. Checklist counter bug fixed (updates on every
                    tap, counts back down on untick).

  HOW IT WORKS
    phone browser --> this script (Flask on your LAN) --> keystrokes into ETS2
    ETS2 --> RenCloud telemetry DLL (shared memory) --> this script --> phone

--------------------------------------------------------------------------
SETUP (one time)  —  unchanged from v1.0, skip if already running
--------------------------------------------------------------------------
1) Telemetry plugin
   Download the latest release (scs-telemetry.dll) from:
     https://github.com/RenCloud/scs-sdk-plugin/releases
   Put the DLL in:
     ...\\Steam\\steamapps\\common\\Euro Truck Simulator 2\\bin\\win_x64\\plugins\\
   (create the "plugins" folder if it doesn't exist)
   Launch ETS2 once and accept the "advanced SDK features" prompt.

2) Python packages (on the gaming PC):
     pip install flask truck-telemetry pydirectinput

3) ETS2 keybinds  (Options -> Keys & Buttons)  — keep NUM LOCK ON:
     Left window up ........ Numpad 7      Left window down ...... Numpad 1
     Right window up ....... Numpad 9      Right window down ..... Numpad 3
     Front susp. up ........ Numpad 8      Front susp. down ...... Numpad 2
     Rear susp. up ......... Numpad 4      Rear susp. down ....... Numpad 6
     Trailer susp. up ...... Numpad 0      Trailer susp. down .... Numpad . (Del)
     Lift/drop trailer axle  Numpad -
     Suspension reset ...... Numpad 5
     Parking brake ......... Numpad +   (bind in-game; panel-owned)
     Hazard lights ......... \\  (backslash)  (bind in-game; panel-owned)
     Cab lift axle ......... ,  (comma)      (bind in-game; panel-owned)
     Differential lock ..... .  (full stop)  (bind in-game; panel-owned)
     Attach/detach trailer . stays on default T
     Engine start/stop ..... Numpad *   AND REMOVE E from this bind —
                             the panel is now the only ignition switch.
     Light modes ........... stays on default L
     High beam ............. stays on default K
   v1.9 migration: set Engine start/stop primary to Numpad * and clear
   the old E binding. Also go to Options -> Gameplay and turn OFF
   "Automatic engine start" (otherwise pressing the throttle starts the
   engine directly).
   v1.4 migration: Numpad 8/2 previously drove front AND rear together —
   remove the rear from those two binds, then add rear on 4/6 and reset
   on 5. Lights need no binding changes at all.

--------------------------------------------------------------------------
RUN (each session)
--------------------------------------------------------------------------
   python rigdeck.py
   -> open the printed  http://<pc-ip>:8600  on your phone (same Wi-Fi).
   First run: allow Python through Windows Firewall (Private networks).
   Fullscreen on the phone:
     iPhone .. Safari -> Share -> Add to Home Screen, launch from the icon
               (opens true fullscreen, RigDeck icon, no Safari chrome).
     Android . tap the [ ] button in the panel header for fullscreen, or
               use Fully Kiosk Browser pointed at the URL for permanent
               fullscreen + keep-screen-awake. (Plain "Add to Home
               screen" opens with the address bar - Chrome only does
               proper installs over HTTPS, and the panel is LAN HTTP.)

NOTES
 * Window/suspension switches are HOLD-to-operate, like the real rockers.
 * The trailer switch needs a ~0.6 s hold so you can't knock it by accident.
 * Keystrokes go to the foreground app — the game window must be focused.
 * If ETS2 is run as administrator, run this script as administrator too.
 * Tacho times/distances mirror the in-game route advisor (game time).
 * Consignment data comes straight from the job telemetry — company and
   city names are the game's own display strings, so ProMods / RusMap /
   BXP cities all show correctly.
 * If any field shows "--", open  http://<pc-ip>:8600/debug  to see the
   raw telemetry your plugin exposes, and adjust the FIELDS map below.
==========================================================================
"""

import atexit
import base64
import json
import logging
import os
import shutil
import socket
import subprocess
import sys
import threading
import time

import urllib.error
import urllib.request

from flask import Flask, Response, jsonify, request

# ----------------------------------------------------------------------
# Version + auto-update check (notify only - never overwrites itself)
# ----------------------------------------------------------------------
APP_VERSION = "3.8"          # bump this when you cut a new release

# Auto-switch tabs based on what you're doing: leaves CONTROLS for STATUS once
# you're moving, and jumps to ACTIVE JOB when a delivery finishes (or you're
# nearly there). Set False if you'd rather the panel stay wherever you leave it.
AUTO_TAB_SWITCH = True

# How long each state has to hold before the panel acts on it.
#   MOVE: short — once you're rolling, STATUS is what you want in front of you.
#   STOP: how long stopped before CONTROLS comes back up for the handbrake.
#         At 3s this is quick, but it also means a wait at lights will flip the
#         page. Raise it (10-15) if that gets annoying on town runs.
AUTO_TAB_MOVE_SEC = 3
AUTO_TAB_STOP_SEC = 3
# Backstop only. Tapping a tab yourself pauses the auto-switching, and that
# pause normally ends at the next collection or delivery. This is just a
# ceiling so it can never stay paused indefinitely if neither happens.
AUTO_TAB_HOLD_SEC = 300

UPDATE_URL   = "https://raw.githubusercontent.com/HexLab2026/RIGDECK/main/version.json"
RELEASES_URL = "https://github.com/HexLab2026/RIGDECK/releases/latest"
UPDATE_CHECK_HOURS = 6

_update = {"latest": None, "url": RELEASES_URL, "download": None, "notes": "",
           "outdated": False, "checked": False}
_update_lock = threading.Lock()


def _ver_tuple(v):
    out = []
    for part in str(v).strip().split("."):
        try:
            out.append(int(part))
        except ValueError:
            out.append(0)
    # drop trailing zeros so 3.5, 3.5.0 and 3.50.0 all compare equal to 3.5
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return tuple(out)


def _fetch_update_once():
    """One version.json fetch. Returns True on success. Updates _update."""
    try:
        req = urllib.request.Request(UPDATE_URL, headers={"User-Agent": "RigDeck"})
        with urllib.request.urlopen(req, timeout=8) as r:
            data = json.loads(r.read().decode("utf-8"))
        latest = str(data.get("version", "")).strip()
        if latest:
            with _update_lock:
                _update["latest"]   = latest
                _update["url"]      = data.get("url", RELEASES_URL)
                _update["download"] = data.get("download")
                _update["notes"]    = data.get("notes", "")
                _update["outdated"] = _ver_tuple(latest) > _ver_tuple(APP_VERSION)
                _update["checked"]  = True
        return True
    except Exception:
        with _update_lock:
            _update["checked"] = True   # we tried; mark it so the UI can stop saying "checking"
        return False


def _check_for_update():
    """Background loop: check now, then every few hours."""
    while True:
        _fetch_update_once()
        time.sleep(max(1, UPDATE_CHECK_HOURS) * 3600)


threading.Thread(target=_check_for_update, daemon=True).start()

# ----------------------------------------------------------------------
# Keyboard output (pydirectinput uses DirectInput scan codes -> works in ETS2)
# ----------------------------------------------------------------------
INPUT_OK = False
try:
    import pydirectinput

    pydirectinput.PAUSE = 0.0
    try:
        pydirectinput.FAILSAFE = False
    except Exception:
        pass
    # pydirectinput 1.0.x ships with the numpad block commented out —
    # re-register the standard DIK scan codes so numpad keys work.
    pydirectinput.KEYBOARD_MAPPING.update({
        "num0": 0x52, "num1": 0x4F, "num2": 0x50, "num3": 0x51,
        "num4": 0x4B, "num5": 0x4C, "num6": 0x4D, "num7": 0x47,
        "num8": 0x48, "num9": 0x49,
        "numdot": 0x53, "numminus": 0x4A, "numstar": 0x37, "numplus": 0x4E,
        "comma": 0x33,   # cab/tractor lift axle
        "period": 0x34,  # differential lock
        "numslash": 0xB5,
        # window keys: off the numpad to avoid ReShade (Home) / SnowyMoon clashes
        "lbracket": 0x1A, "rbracket": 0x1B, "semicolon": 0x27, "quote": 0x28,
        "backslash": 0x2B,
    })
    INPUT_OK = True
except Exception as e:  # pragma: no cover
    print("[!] pydirectinput unavailable:", e)

# ----------------------------------------------------------------------
# Telemetry input (RenCloud scs-sdk-plugin shared memory)
# ----------------------------------------------------------------------
TELE_LIB = False
try:
    import truck_telemetry

    TELE_LIB = True
except Exception as e:  # pragma: no cover
    print("[!] truck-telemetry unavailable:", e)

_tele_ready = False


def read_telemetry():
    """Return the raw telemetry dict, or None if the game isn't up yet."""
    global _tele_ready
    if not TELE_LIB:
        return None
    try:
        if not _tele_ready:
            truck_telemetry.init()          # attaches to Local\SCSTelemetry
            _tele_ready = True
        return truck_telemetry.get_data()
    except Exception:
        _tele_ready = False
        return None


# Exact field names verified against truck-telemetry 0.0.3 / RenCloud SDK.
# Fallback aliases included in case a future plugin version renames them.
FIELDS = {
    # tacho
    "speed":        ["speed"],                                  # m/s
    "odometer":     ["truckOdometer", "odometer"],              # km
    "rest_min":     ["restStop", "nextRestStop"],               # game min
    "route_m":      ["routeDistance", "navigationDistance"],    # metres
    "route_s":      ["routeTime", "navigationTime"],            # seconds
    "paused":       ["paused", "gamePaused"],
    # consignment (NEW v1.1)
    "on_job":       ["onJob", "jobIncome" ],                    # bool-ish
    "cargo":        ["cargo", "cargoName"],                     # display str
    "cargo_kg":     ["cargoMass", "cargoWeight"],               # kg
    "src_city":     ["citySrc", "sourceCity"],
    "src_comp":     ["compSrc", "sourceCompany"],
    "dst_city":     ["cityDst", "destinationCity"],
    "dst_comp":     ["compDst", "destinationCompany"],
    "loaded":       ["isCargoLoaded", "cargoLoaded"],           # bool (newer SDK)
    "game_min":     ["time_abs", "timeAbs", "gameTime"],        # game clock, abs min
    "due_min":      ["time_abs_delivery", "deliveryTime",
                     "jobDeliveryTime"],                        # deadline, abs min
    "income":       ["income", "jobIncome"],                    # payout, € internal
    # engine state
    "engine":       ["engineEnabled", "engineOn"],              # bool
    "park_brake":   ["parkingBrake", "parkBrake", "parkBrakeOn"],  # bool
    "diff_lock":    ["differentialLock"],                       # bool
    "hazards":      ["lightsHazards", "hazardWarning"],            # bool
    "wipers":       ["wipers", "wipersOn"],                        # bool
    "blink_l_act":  ["blinkerLeftActive"],    "blink_l_on":  ["blinkerLeftOn"],
    "blink_r_act":  ["blinkerRightActive"],   "blink_r_on":  ["blinkerRightOn"],
    # lights (NEW v1.4)
    "light_low":    ["lightsBeamLow", "beamLow"],
    "light_high":   ["lightsBeamHigh", "beamHigh"],
    "light_park":   ["lightsParking", "parkingLights"],
    # rig page (NEW v1.4)
    "fuel":         ["fuel"],                                   # litres
    "fuel_cap":     ["fuelCapacity"],
    "fuel_range":   ["fuelRange"],                              # km
    "fuel_avg":     ["fuelAvgConsumption",
                     "fuelAverageConsumption"],                 # l/km
    "fuel_warn":    ["fuelWarning", "fuelWarningOn"],
    "adblue":       ["adblue", "adBlue"],                       # litres
    "adblue_cap":   ["adblueCapacity", "adBlueCapacity"],
    "air":          ["airPressure", "brakeAirPressure"],        # psi
    "air_warn":     ["airPressureWarning", "airPressureWarningOn"],
    "brake_temp":   ["brakeTemperature"],                       # °C
    "oil_temp":     ["oilTemperature"],                         # °C
    "oil_press":    ["oilPressure"],                            # psi
    "oil_warn":     ["oilPressureWarning", "oilPressureWarningOn"],
    "water_temp":   ["waterTemperature"],                       # °C
    "water_warn":   ["waterTemperatureWarning", "waterTemperatureWarningOn"],
    "battery":      ["batteryVoltage"],                         # V
    "batt_warn":    ["batteryVoltageWarning", "batteryVoltageWarningOn"],
    "wear_engine":  ["wearEngine"],                             # 0..1
    "wear_trans":   ["wearTransmission", "wearTransmision"],
    "wear_cabin":   ["wearCabin"],
    "wear_chassis": ["wearChassis"],
    "wear_wheels":  ["wearWheels"],
    # trailer axle (NEW v1.5)
    "cabaxle_ind":  ["liftAxleIndicator"],
    "axle_ind":     ["trailerLiftAxleIndicator", "liftAxleIndicatorTrailer"],
    "axle_raw":     ["trailerLiftAxle", "liftAxleTrailer"],
    # job tracking (NEW v1.8)
    "trailer_att":  ["trailerAttached", "isTrailerAttached", "trailerAttach"],
    "cargo_dmg":    ["cargoDamage"],
    "ev_delivered": ["jobDelivered", "jobFinished", "specialJobDelivered"],
    "ev_cancelled": ["jobCancelled", "specialJobCancelled"],
    "ev_fined":     ["fined"],
    "fine_amount":  ["fineAmount", "fineAmout"],
}


def getf(data, key, default=None):
    for name in FIELDS.get(key, []):
        if data and name in data:
            return data[name]
    return default


def clean_str(v):
    if isinstance(v, bytes):
        v = v.decode("utf-8", "ignore")
    if isinstance(v, str):
        v = v.strip().strip("\x00")
        return v or None
    return None


def cargo_loaded(data):
    """Is there actually cargo aboard?

    This is deliberately NOT the same as 'is a trailer coupled'. With a market /
    quick-job trailer you only couple up once you collect, so coupling happens to
    coincide with being loaded. An OWNED trailer stays hitched permanently, so
    coupling tells you nothing — it would read 'loaded' even when running empty.

    Prefer the SDK's explicit cargo flag; fall back to cargo mass for older
    plugin builds that don't report it. Returns True/False, or None if the
    telemetry gives us nothing to go on.
    """
    v = getf(data, "loaded")
    if v is not None:
        return bool(v)
    kg = getf(data, "cargo_kg")
    if isinstance(kg, (int, float)):
        return kg > 1.0        # any real cargo mass means something's aboard
    return None


def trailer_attached(data):
    """Coupling state; handles both flat and nested trailer layouts."""
    v = getf(data, "trailer_att")
    if v is not None:
        return bool(v)
    tr = data.get("trailer") if isinstance(data, dict) else None
    if tr is None and isinstance(data, dict):
        tr = data.get("trailers")
    if isinstance(tr, (list, tuple)) and tr and isinstance(tr[0], dict):
        if "attached" in tr[0]:
            return bool(tr[0]["attached"])
    return None


# ----------------------------------------------------------------------
# App icon (RigDeck mark, embedded PNG for the manifest / home screen)
# ----------------------------------------------------------------------
ICON_PNG = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAgAAAAIACAIAAAB7GkOtAAAINUlEQVR42u3dvY3CQBCA0eHkAghABOSWHLgQkIiokw\
gJCnFgyS2QUMJFF/s4ONif90rw7syHnbBYbbYBQH2+PAIAAQBAAAAQAAAEAAABAEAAABAAAAQAAAEAQAAAEAAABAAA\
AQBAAAAQAAAEAAABAEAAABAAAAQAAAEAQAAAEAAAAQBAAAAQAAAEAAABAEAAABAAAAQAAAEAQAAAEAAABAAAAQBAAA\
AQAAAEAAABAEAAABAAAAQAAAEAQAAAEAAAAQBAAAAQAAAEAAABAEAAABAAAAQAAAEAQAAAEAAABAAAAQBAAAAQAAAE\
AAABAEAAABAAAAQAAAEAQAAAEAAABABAAAAQAAAEAAABAEAAABAAAAQAAAEAQAAAEAAABAAAAQBAAAAQAAAEAAABAE\
AAABAAAAQAAAEAQAAAEAAABABAAAAQAAAEAAABAEAAABAAAAQAAAEAQAAAEAAABACANDQeQUbOl6uHQPoO+52HkIXF\
arP1FKx+kIEK+QRk+4N76w0AIwReBbwBYPuDmywAmBlwnwUA0wJutQBgTsDdFgBMCLjhAoDZAPdcADAV4LYLAOYB3H\
kBwCSAmy8AmAFw/wXA7QdTgAC492AWEAA3HkwEAuCug7lAANxyMB0IgPsNZgQBcLPBpCAA7jSYF37HX0Jmf5v93x7u\
Nt4ATAi827/eQO8BAmD72/5oAAJg+9v+aAACYPt7wmgAAmD7gwYgALY/aAACYPuDBiAAtj9oAAJg+4MGIAC2P2iAAG\
D7gwYIADXND7jDAkCiP0NMDhrgJUAAzAy4zwhAHT//TQsa4CVAAMwJuNsIgAkBNxwBSMTL3z3NBhqQwiQKAH4Zgdsu\
AJgHcOcFAJMAbr4AYAbA/RcA3H4wBQIAgAAAIAAACAAAAgCAAAAgAAAIAAACAIAAACAAAAgAAAIAgAAAIAAACAAAAg\
AgAAAIAAACAIAAACAAAAgAAAIAgAAAIAAACAAAAgCAAAAgAAAIAAACAIAAACAAADyp8Qh4SNv1HkLKpnHwEBAA7P2q\
T0oJmOUTELa/U8MbAFgiJR6fVwG8AWD7O0cQAGwNpwkCACAA4AejM0UAsClwsggAAAIAgABQLl8JnC8CAIAAACAAAA\
gAAAIAgAAAIAAACAAAAgCAAAAgAAAIAAACAIAAACAAAAgAAAIAgAAAIAAACAAAAgCAAAAIAERExDQOHoLzRQAAEAAA\
BIDi+UrgZBEAbAqcKQIAgADgByNOEwHA1sA5krHGI2B2d7Rd71FY/XgDwB7BqeENgCq3ibcBex8BwH4B8uYTEIAAAF\
ATn4B4zO249BBStj7dPQQEAHu/6pNSAmb5BITt79TwBgCWSInH51UAbwDY/s4RBABbw2mCAAAIAPjB6EwRAGwKnCwC\
AIAAACAAlMtXAueLAAAgAAAIAAACAIAAACAAAAgAAAIAgAAAIAAACAAAAgCAAAAgAAAIAAACAIAAACAAAAgAAAIAgA\
AAIAAAAgAREbE+3T0E54sAACAAAAgAxfOVwMkiANgUOFMEAAABwA9GnCYCgK2BcyRjjUfA7O64HZcehdWPNwDsEZwa\
3gCocpt4G7D3EQDsFyBvPgEBCAAANfEJiMe0Xe8hpGwaBw8BAcDer/qklIBZPgFh+zs1vAGAJVLi8XkVwBsAtr9zBA\
HA1nCaIAAAAgB+MDpTBACbAieLAAAgAAAIAOXylcD5IgAACAAAAgCAAAAgAAAIAAACAIAAACAAAAgAAAIAgAAAIAAA\
CAAAAgCAAAAgAAAIAAACAIAAACAAAAgAgABARERM4+AhOF8EAAABAEAAKJ6vBE4WAcCmwJkiAAAIAH4w4jQRAGwNnC\
MZazwCZndH2/UehdWPNwDsEZwa3gCocpt4G7D3EQDsFyBvPgEBCAAAAgCAAAAgAAAIAAACAIAAACAAAAgAAAIAgAAA\
IAAACAAAAgCAAAAgAAAIAAACAIAAACAAAAgAAAIAgAAACAAAAgCAAAAgAAAIAAACAIAAACAAAAgAAAIAgADw43y5eg\
iYAg9BANx+cP8RADMAbj4CYBLAnUcAzAO47QhAGg77namAj9/zl0+iAOCXEbjhAoAJAXdbAHjPu6c5wfb/7AwKAH4r\
gfssAHziB4iZwfb3818ATA64wwhAZS8B5gfb389/AdAAsP1tfwHQALD9EQANANsfAdAAsP0RAA0A2x8B0ACw/READQ\
DbHwHQALD9EQANANtfANAAsP3rslhttp5C7nMCfjnhDcBtBvOCALjTYFIQADcbzAgC4H6D6UAA3HIwFwKAuw4mQgBw\
48EsCADuPZgCAcDtB/dfADAD4OYLACYB3HkBwDyA2y4AmApwzwUAswFuuABgQsDdFgDMCW41AoBpwX1GADAzuMm8mb\
+EzIC/k8TqxxuAKQL3Fm8AXgXA6kcAAPgDn4AABAAAAQBAAAAQAAAEAAABAEAAABAAAAQAAAEAQAAAEAAABAAAAQBA\
AAAQAAAEAAABAEAAABAAAAQAAAEAQAAABAAAAQBAAAAQAAAEAAABAEAAABAAAAQAAAEAQAAAEAAABAAAAQBAAAAQAA\
AEAAABAEAAABAAAAQAAAEAQAAABMAjABAAAAQAAAEAQAAAEAAABAAAAQBAAAAQAAAEAAABAEAAABAAAAQAAAEAQAAA\
EAAABAAAAQBAAAAQAAAEAAABABAAAAQAAAEAQAAAEAAABAAAAQBAAAAQAAAEAAABAEAAABAAAAQAAAEAQAAAEAAABA\
AAAQBAAAAQAAAEAAABABAAAAQAAAEAQAAAEAAABAAAAQBAAAAQAAAEAID0fAMMniAnKssydwAAAABJRU5ErkJggg=="
)

# ----------------------------------------------------------------------
# Trip meter persistence
# ----------------------------------------------------------------------
TRIP_FILE = "rigdeck_trip.json"


def load_trip_base():
    try:
        with open(TRIP_FILE) as f:
            return float(json.load(f).get("base", 0.0))
    except Exception:
        return 0.0


def save_trip_base(v):
    try:
        with open(TRIP_FILE, "w") as f:
            json.dump({"base": v}, f)
    except Exception:
        pass


_trip_base = load_trip_base()

# ----------------------------------------------------------------------
# Self-computed fuel range (smoother than the plugin's twitchy fuelRange).
# We watch litres burned per km over a sliding distance window and derive
# range = fuel_now / (litres per km). Refuels and idle are handled so the
# estimate doesn't jump around.
# ----------------------------------------------------------------------
_fuel_lock = threading.Lock()
_fuel_hist = []                 # list of (odo_km, fuel_l, t) samples, recent last
_FUEL_WINDOW_KM = 40.0          # average consumption over the last ~40 km
_FUEL_MIN_KM = 2.0              # need at least this much distance to estimate
_FUEL_SAMPLE_SEC = 60.0         # only record a new sample once a minute
_fuel_last_t = 0.0              # timestamp of the last recorded sample
# Last good reading from OUR model, kept so a brief dropout (a gap in polling
# while the phone screen is off, a ferry, a refuel) doesn't make the range jump
# to the game's built-in estimate — which is a very different number and makes
# the fuel-range warning light flick on and off.
_fuel_last_good = {"l100": None, "range": None, "t": 0.0}
_FUEL_HOLD_SEC = 900.0          # keep showing our last figure for up to 15 min


def _estimate(hist, fuel_l):
    """Derive (l/100km, range_km) from the current sample window."""
    if len(hist) < 2:
        return None, None
    dist = hist[-1][0] - hist[0][0]
    used = hist[0][1] - hist[-1][1]
    if dist < _FUEL_MIN_KM or used <= 0:
        return None, None
    l_per_km = used / dist
    range_km = fuel_l / l_per_km if l_per_km > 0 else None
    return l_per_km * 100.0, range_km


def update_fuel_model(odo_km, fuel_l):
    """Record a sample at most once a minute; always return the live estimate.

    The panel polls every ~0.7s, but the consumption average only needs a
    fresh data point once a minute — sampling faster just adds noise. Between
    samples we still return the estimate from the existing window, so the
    RIG page and range alert stay responsive."""
    global _fuel_last_t
    if not isinstance(odo_km, (int, float)) or not isinstance(fuel_l, (int, float)):
        return None, None
    now = time.time()
    with _fuel_lock:
        hist = _fuel_hist
        # sudden refuel or teleport/reset — clear and restart cleanly, and take
        # this sample immediately rather than waiting out the minute.
        if hist:
            d_km = odo_km - hist[-1][0]
            d_fuel = hist[-1][1] - fuel_l
            if d_fuel < -0.5 or d_km < 0 or d_km > 5:
                hist.clear()
                _fuel_last_t = 0.0
        # Record a sample once a minute in normal running. BUT while the model
        # hasn't got a usable estimate yet (fewer than 2 points, or not enough
        # distance covered), sample on every call so it warms up quickly instead
        # of sitting blank for the first minute. Also require a little movement
        # between minute-samples so a parked truck doesn't fill the window with
        # identical points.
        warming = len(hist) < 2 or (hist[-1][0] - hist[0][0]) < _FUEL_MIN_KM
        moved = (not hist) or (odo_km - hist[-1][0]) >= 0.05   # ~50 m
        due = (now - _fuel_last_t) >= _FUEL_SAMPLE_SEC
        if not hist or warming or (due and moved):
            hist.append((odo_km, fuel_l))
            _fuel_last_t = now
            while len(hist) > 2 and (hist[-1][0] - hist[0][0]) > _FUEL_WINDOW_KM:
                hist.pop(0)
        return _estimate(hist, fuel_l)

# ----------------------------------------------------------------------
# Held-key registry + safety watchdog (auto-release stale holds)
# ----------------------------------------------------------------------
ENGINE_KEY = "numstar"    # hidden ignition: bound in-game, never on the keyboard
HOLD_KEYS = {"num8", "num2", "num4", "num6", "num0", "numdot",
             "lbracket", "rbracket", "semicolon", "quote"}   # windows on punctuation cluster
PARK_KEY = "numplus"      # parking brake: bind in-game to Numpad +, panel-owned
HAZ_KEY  = "backslash"    # hazard lights: bind in-game to \\ , panel-owned (numpad-/ was unreliable)
CABAXLE_KEY = "comma"    # tractor/cab lift axle: bind in-game to , (comma)
DIFF_KEY    = "period"   # differential lock: bind in-game to . (full stop)
TAP_KEYS = {"t", ENGINE_KEY, "num5", "l", "k", "v", "numminus", PARK_KEY, HAZ_KEY,
            CABAXLE_KEY, DIFF_KEY}

_held = {}                     # key -> last refresh time
_held_lock = threading.Lock()
WATCHDOG_STALE = 3.0           # seconds without refresh -> force release
# How long a "tap" holds the key down. pydirectinput's press() sends keyDown and
# keyUp back to back, which can be over in well under a millisecond — short
# enough that a game polling input once per frame (~16ms) never sees it. A real
# finger holds a key for ~100ms. This gives taps a few frames of contact so they
# register reliably.
TAP_HOLD_SEC = 0.08


def _key_down(key):
    if INPUT_OK:
        try:
            pydirectinput.keyDown(key)
        except Exception:
            pass


def _key_up(key):
    if INPUT_OK:
        try:
            pydirectinput.keyUp(key)
        except Exception:
            pass


def _watchdog():
    while True:
        time.sleep(0.5)
        now = time.time()
        with _held_lock:
            for k, ts in list(_held.items()):
                if now - ts > WATCHDOG_STALE:
                    _key_up(k)
                    _held.pop(k, None)


threading.Thread(target=_watchdog, daemon=True).start()

# ----------------------------------------------------------------------
# Session job tracker (feeds the JOBS page)
# ----------------------------------------------------------------------
import hashlib
import random

# Name pools for proof-of-delivery signatures. Large enough that repeats
# are rare across a session's worth of jobs.
# Warehouse signatory pool for proof-of-delivery. Large enough that
_WAREHOUSE = [
    "J. Pemberton", "S. Duchamp", "M. Andersson", "R. Kovač", "T. Bianchi",
    "L. Świątek", "D. García", "A. Müller", "C. O'Riordan", "K. Voss",
    "P. Larsen", "N. Radić", "G. Fournier", "H. Weber", "B. Jankowski",
    "E. Virtanen", "F. Romano", "W. Haugen", "V. Sokolov", "O. Berg",
]
_ROLES = [
    "Warehouse Supervisor", "Goods-In Clerk", "Loading Bay Manager",
    "Dispatch Coordinator", "Shift Supervisor", "Depot Manager",
]


def _sig_svg(name, seed):
    """Deterministic handwritten-style signature path for a name+seed."""
    rnd = random.Random(seed)
    w, h = 240, 70
    baseline = 46
    x = 12.0
    # first-initial flourish
    parts = []
    n_strokes = len(name.replace(" ", "").replace(".", "")) + 3
    y = baseline
    parts.append(f"M {x:.1f} {y:.1f}")
    # opening capital loop
    cap_h = rnd.uniform(20, 30)
    parts.append(
        f"c {rnd.uniform(2,5):.1f} -{cap_h:.1f} {rnd.uniform(10,16):.1f} -{cap_h:.1f} "
        f"{rnd.uniform(12,18):.1f} -{rnd.uniform(2,8):.1f}")
    x += rnd.uniform(14, 20)
    # cursive body: alternating up/down bezier humps
    for i in range(n_strokes):
        dx = rnd.uniform(9, 17)
        up = rnd.uniform(8, 22) * (1 if i % 2 else -1)
        mid = rnd.uniform(-6, 6)
        parts.append(
            f"q {dx/2:.1f} {up:.1f} {dx:.1f} {mid:.1f}")
        x += dx
        if x > w - 40:
            break
    # trailing dash + optional dot
    parts.append(f"m {rnd.uniform(3,7):.1f} {rnd.uniform(-4,4):.1f} "
                 f"l {rnd.uniform(14,26):.1f} {rnd.uniform(-2,3):.1f}")
    d = " ".join(parts)
    rot = rnd.uniform(-3, 3)
    return (
        f'<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" class="sigsvg">'
        f'<g transform="rotate({rot:.1f} {w/2:.0f} {h/2:.0f})">'
        f'<path d="{d}" fill="none" stroke="#262B33" stroke-width="2.1" '
        f'stroke-linecap="round" stroke-linejoin="round"/></g></svg>')


# Your driver — signs every POD. Set this to your driver's name;
# the signature scrawl is generated once and stays identical all session,
# the way a real driver's signature would.
DRIVER_NAME = "A. Driver"

_DRIVER_SIG = None   # built lazily so DRIVER_NAME edits are picked up


def make_signoff(job_id):
    """Fixed driver (you) + a varied warehouse signatory per job."""
    global _DRIVER_SIG
    if _DRIVER_SIG is None:
        # stable seed from the name only — same scrawl every job
        dseed = int(hashlib.md5(DRIVER_NAME.encode()).hexdigest(), 16)
        _DRIVER_SIG = _sig_svg(DRIVER_NAME, dseed)
    seed = int(hashlib.md5(f"rigdeck{job_id}".encode()).hexdigest(), 16)
    rnd = random.Random(seed)
    whs = rnd.choice(_WAREHOUSE)
    role = rnd.choice(_ROLES)
    return {
        "driver_name": DRIVER_NAME,
        "driver_sig": _DRIVER_SIG,
        "wh_name": whs,
        "wh_role": role,
        "wh_sig": _sig_svg(whs, seed ^ 0x5),
    }


JOBS = []            # finished jobs, newest first (this session only)
_job_lock = threading.Lock()
_job_seq = 0
PENDING = {"job": None}   # delivered-but-not-yet-confirmed job awaiting the button


def _job_tracker():
    global _job_seq
    cur = None
    prev_fuel = None
    prev_fined = False
    ev_del = 0.0
    ev_can = 0.0

    def _wear_avg(d):
        vals = [getf(d, k) for k in ("wear_engine", "wear_trans",
                                     "wear_cabin", "wear_chassis", "wear_wheels")]
        vals = [float(v) for v in vals if isinstance(v, (int, float))]
        return sum(vals) / len(vals) if vals else None

    while True:
        time.sleep(1.0)
        data = read_telemetry()
        if not data:
            continue
        now = time.time()
        if getf(data, "ev_delivered"):
            ev_del = now
        if getf(data, "ev_cancelled"):
            ev_can = now
        fined_now = bool(getf(data, "ev_fined"))
        fined_edge = fined_now and not prev_fined
        prev_fined = fined_now

        cargo = clean_str(getf(data, "cargo"))
        on = bool(getf(data, "on_job")) or bool(cargo)
        fuel = getf(data, "fuel")
        odo = getf(data, "odometer")
        gmin = getf(data, "game_min")
        spd = abs(float(getf(data, "speed") or 0.0)) * 3.6
        dmg = getf(data, "cargo_dmg")

        with _job_lock:
            if cur is None:
                if on:
                    kg = getf(data, "cargo_kg") or 0.0
                    inc = getf(data, "income")
                    cur = {
                        "cargo": cargo,
                        "mass_t": round(float(kg) / 1000.0, 1) if kg else None,
                        "src_comp": clean_str(getf(data, "src_comp")),
                        "src_city": clean_str(getf(data, "src_city")),
                        "dst_comp": clean_str(getf(data, "dst_comp")),
                        "dst_city": clean_str(getf(data, "dst_city")),
                        "income": int(inc) if isinstance(inc, (int, float)) and inc > 0 else None,
                        "due": getf(data, "due_min"),
                        "g0": gmin, "odo0": odo,
                        "t0": now, "fines": 0, "wear0": _wear_avg(data),
                        "fuel_used": 0.0, "vmax": 0.0, "dmg": None,
                    }
                    prev_fuel = fuel
                continue

            # --- active job: accumulate ---
            if isinstance(fuel, (int, float)) and isinstance(prev_fuel, (int, float)):
                d = prev_fuel - fuel
                if 0 < d < 5:          # burn only; ignores refuels/teleports
                    cur["fuel_used"] += d
            prev_fuel = fuel
            if spd > cur["vmax"]:
                cur["vmax"] = spd
            if fined_edge:
                amt = getf(data, "fine_amount")
                cur["fines"] += int(amt) if isinstance(amt, (int, float)) and amt > 0 else 0
            if isinstance(dmg, (int, float)):
                cur["dmg"] = float(dmg)
            # some fields populate late (e.g. after coupling on some markets)
            if cargo:
                cur["cargo"] = cargo
            for k, key in (("src_comp", "src_comp"), ("src_city", "src_city"),
                           ("dst_comp", "dst_comp"), ("dst_city", "dst_city")):
                if not cur[k]:
                    cur[k] = clean_str(getf(data, key))
            if cur["mass_t"] is None:
                kg = getf(data, "cargo_kg") or 0.0
                if kg:
                    cur["mass_t"] = round(float(kg) / 1000.0, 1)
            if cur["due"] is None:
                cur["due"] = getf(data, "due_min")

            if on:
                continue

            # --- job ended: close it out ---
            failed = (now - ev_can) < 12 and not ((now - ev_del) < 12)
            dist = None
            if isinstance(odo, (int, float)) and isinstance(cur["odo0"], (int, float)):
                dist = max(0.0, float(odo) - float(cur["odo0"]))
            tmin = None
            if isinstance(gmin, (int, float)) and isinstance(cur["g0"], (int, float)):
                tmin = max(0, int(gmin) - int(cur["g0"]))
            late = None
            due = cur["due"]
            if (isinstance(due, (int, float)) and 0 < due < 0xFFFFFFFF
                    and isinstance(gmin, (int, float))):
                late = int(gmin) - int(due)   # +ve = late
            _job_seq += 1
            w1 = _wear_avg(data)
            tdmg = None
            if isinstance(cur.get("wear0"), float) and isinstance(w1, float):
                tdmg = max(0.0, w1 - cur["wear0"])
            record = {
                "id": _job_seq,
                "status": "FAILED" if failed else "COMPLETED",
                "cargo": cur["cargo"], "mass_t": cur["mass_t"],
                "src_comp": cur["src_comp"], "src_city": cur["src_city"],
                "dst_comp": cur["dst_comp"], "dst_city": cur["dst_city"],
                "income": cur["income"],
                "dist_km": round(dist, 1) if dist is not None else None,
                "time_min": tmin,
                "real_s": int(now - cur["t0"]),
                "fuel_l": round(cur["fuel_used"], 1),
                "vmax": round(cur["vmax"]),
                "cargo_dmg": cur["dmg"],
                "truck_dmg": tdmg,
                "fines": cur["fines"],
                "late_min": late,
                "comment": "",
            }
            if failed:
                record["signoff"] = None
                JOBS.insert(0, record)          # failures file straight away
            else:
                record["signoff"] = make_signoff(_job_seq)
                PENDING["job"] = record          # await the JOB COMPLETED button
            cur = None


threading.Thread(target=_job_tracker, daemon=True).start()

# 

@atexit.register
def _release_all():
    with _held_lock:
        for k in list(_held):
            _key_up(k)
        _held.clear()


# ----------------------------------------------------------------------
# Discovery responder (lets the Android app find this PC automatically)
# ----------------------------------------------------------------------
DISCOVERY_PORT = 8721
DISCOVERY_MAGIC = b"RIGDECK_DISCOVER"


def _discovery_responder():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(("0.0.0.0", DISCOVERY_PORT))
    except Exception as e:
        print("[!] discovery responder unavailable:", e)
        return
    while True:
        try:
            data, addr = s.recvfrom(64)
            if data.strip() == DISCOVERY_MAGIC:
                s.sendto(b"RIGDECK 8600", addr)
        except Exception:
            pass


threading.Thread(target=_discovery_responder, daemon=True).start()

# ----------------------------------------------------------------------
# Flask app
# ----------------------------------------------------------------------
app = Flask(__name__)
logging.getLogger("werkzeug").setLevel(logging.WARNING)


@app.route("/press", methods=["POST"])
def press():
    key = (request.json or {}).get("key")
    if key not in HOLD_KEYS:
        return jsonify(ok=False), 400
    with _held_lock:
        fresh = key not in _held
        _held[key] = time.time()
    if fresh:
        _key_down(key)
    return jsonify(ok=True)


@app.route("/release", methods=["POST"])
def release():
    key = (request.json or {}).get("key")
    if key not in HOLD_KEYS:
        return jsonify(ok=False), 400
    with _held_lock:
        was = _held.pop(key, None)
    if was is not None:
        _key_up(key)
    return jsonify(ok=True)


@app.route("/tap", methods=["POST"])
def tap():
    key = (request.json or {}).get("key")
    if key == "engine":
        key = ENGINE_KEY
    elif key == "park":
        key = PARK_KEY
    elif key == "haz":
        key = HAZ_KEY
    elif key == "cabaxle":
        key = CABAXLE_KEY
    elif key == "diff":
        key = DIFF_KEY
    if key not in TAP_KEYS:
        return jsonify(ok=False), 400
    if INPUT_OK:
        # hold briefly rather than pydirectinput.press(), which can be too fast
        # for the game to notice — see TAP_HOLD_SEC above
        _key_down(key)
        time.sleep(TAP_HOLD_SEC)
        _key_up(key)
    return jsonify(ok=True)


@app.route("/trip/reset", methods=["POST"])
def trip_reset():
    global _trip_base
    data = read_telemetry()
    odo = getf(data, "odometer")
    if isinstance(odo, (int, float)):
        _trip_base = float(odo)
        save_trip_base(_trip_base)
        return jsonify(ok=True)
    return jsonify(ok=False)


@app.route("/jobs")
def jobs():
    with _job_lock:
        return jsonify(list(JOBS))


@app.route("/job/pending")
def job_pending():
    with _job_lock:
        return jsonify(job=PENDING["job"])


@app.route("/job/complete", methods=["POST"])
def job_complete():
    """File the delivered-but-unconfirmed job into the log (the button)."""
    note = (request.json or {}).get("comment", "")
    with _job_lock:
        rec = PENDING["job"]
        if rec is None:
            return jsonify(ok=False, reason="no_pending"), 409
        if isinstance(note, str):
            rec["comment"] = note[:500]
        JOBS.insert(0, rec)
        PENDING["job"] = None
        return jsonify(ok=True, id=rec["id"])


@app.route("/job/comment", methods=["POST"])
def job_comment():
    """Update the comment on an already-filed job."""
    b = request.json or {}
    jid, note = b.get("id"), b.get("comment", "")
    with _job_lock:
        for rec in JOBS:
            if rec["id"] == jid:
                rec["comment"] = note[:500] if isinstance(note, str) else ""
                return jsonify(ok=True)
    return jsonify(ok=False), 404


@app.route("/telemetry")
def telemetry():
    data = read_telemetry()
    if not data:
        return jsonify(ok=False, game=False)

    speed = getf(data, "speed") or 0.0
    odo = getf(data, "odometer")
    rest = getf(data, "rest_min")
    route_m = getf(data, "route_m")
    route_s = getf(data, "route_s")

    trip = None
    if isinstance(odo, (int, float)):
        trip = max(0.0, float(odo) - _trip_base)

    # ---- consignment ----
    cargo = clean_str(getf(data, "cargo"))
    kg = getf(data, "cargo_kg") or 0.0
    on_job = bool(getf(data, "on_job")) or bool(cargo)

    def _valid_min(v):
        # 0 and 0xFFFFFFFF are the "no deadline" sentinels
        return isinstance(v, (int, float)) and 0 < v < 0xFFFFFFFF

    now_min = getf(data, "game_min")
    due_min = getf(data, "due_min")
    income = getf(data, "income")
    remain = None
    if _valid_min(due_min) and _valid_min(now_min):
        remain = int(due_min) - int(now_min)

    def num(k):
        v = getf(data, k)
        return float(v) if isinstance(v, (int, float)) else None

    lights = {
        "low": bool(getf(data, "light_low")),
        "park": bool(getf(data, "light_park")),
        "high": bool(getf(data, "light_high")),
    }
    avg = num("fuel_avg")
    # our own smoothed model from actual burn over distance
    _our_l100, _our_range = update_fuel_model(getf(data, "odometer"), num("fuel"))

    # Keep our learned burn rate across brief dropouts. The model resets its
    # window on a polling gap / ferry / refuel, and without this the displayed
    # range would jump to the game's built-in estimate (a very different figure)
    # and then jump back — which shows up as the fuel warning light flicking on
    # and off. We cache the consumption rate, not the range, so the held value
    # still tracks the fuel actually left in the tank.
    _fuel_now = num("fuel")
    _now = time.time()
    if _our_l100 is not None and _our_l100 > 0:
        _fuel_last_good["l100"] = _our_l100
        _fuel_last_good["t"] = _now
    elif (_fuel_last_good["l100"] and
          (_now - _fuel_last_good["t"]) <= _FUEL_HOLD_SEC and
          isinstance(_fuel_now, (int, float))):
        _our_l100 = _fuel_last_good["l100"]
        _our_range = _fuel_now / (_our_l100 / 100.0)

    avg100 = _our_l100 if _our_l100 is not None else ((avg * 100.0) if avg else None)
    frange = _our_range if _our_range is not None else num("fuel_range")
    rig = {
        "fuel": num("fuel"), "fuel_cap": num("fuel_cap"),
        "range": frange,
        "avg100": avg100,
        "range_est": _our_range is not None,   # True once our model is live
        "fuel_warn": bool(getf(data, "fuel_warn")),
        "adb": num("adblue"), "adb_cap": num("adblue_cap"),
        "air": num("air"), "air_warn": bool(getf(data, "air_warn")),
        "brake_c": num("brake_temp"),
        "oil_c": num("oil_temp"), "oil_p": num("oil_press"),
        "oil_warn": bool(getf(data, "oil_warn")),
        "water_c": num("water_temp"), "water_warn": bool(getf(data, "water_warn")),
        "batt": num("battery"), "batt_warn": bool(getf(data, "batt_warn")),
        "wear": {
            "eng": num("wear_engine"), "tra": num("wear_trans"),
            "cab": num("wear_cabin"), "cha": num("wear_chassis"),
            "whe": num("wear_wheels"),
        },
    }

    job = {
        "on": on_job,
        "cargo": cargo,
        "mass_t": round(float(kg) / 1000.0, 1) if kg else None,
        "src_comp": clean_str(getf(data, "src_comp")),
        "src_city": clean_str(getf(data, "src_city")),
        "dst_comp": clean_str(getf(data, "dst_comp")),
        "dst_city": clean_str(getf(data, "dst_city")),
        "coupled": trailer_attached(data),
        "loaded": cargo_loaded(data),
        "due_min": int(due_min) if _valid_min(due_min) else None,
        "remain_min": remain,
        "income": int(income) if isinstance(income, (int, float)) and income > 0 else None,
    }

    ax = getf(data, "axle_ind")
    if ax is None:
        ax = getf(data, "axle_raw")

    with _job_lock:
        pending = PENDING["job"] is not None

    return jsonify(
        ok=True,
        game=True,
        paused=bool(getf(data, "paused")),
        engine=bool(getf(data, "engine")),
        park=bool(getf(data, "park_brake")),
        diff=getf(data, "diff_lock"),
        wipers=bool(getf(data, "wipers")),
        haz=bool(getf(data, "hazards"))
            or (
                (bool(getf(data, "blink_l_act")) or bool(getf(data, "blink_l_on")))
                and
                (bool(getf(data, "blink_r_act")) or bool(getf(data, "blink_r_on")))
            ),
        speed_kmh=abs(float(speed)) * 3.6,
        odo_km=float(odo) if isinstance(odo, (int, float)) else None,
        trip_km=trip,
        rest_min=int(rest) if isinstance(rest, (int, float)) else None,
        route_km=(float(route_m) / 1000.0) if isinstance(route_m, (int, float)) else None,
        route_min=(float(route_s) / 60.0) if isinstance(route_s, (int, float)) else None,
        lights=lights,
        rig=rig,
        axle=(bool(ax) if ax is not None else None),
        job=job,
        pending=pending,
    )


@app.route("/update")
def update():
    with _update_lock:
        u = dict(_update)
    u["current"] = APP_VERSION
    return jsonify(u)


@app.route("/debug")
def debug():
    data = read_telemetry()
    if not data:
        return Response("telemetry not connected", mimetype="text/plain")
    # surface every hazard/blinker-related field so we can see what's actually set
    watch = ["lightsHazards", "hazardWarning",
             "blinkerLeftActive", "blinkerRightActive",
             "blinkerLeftOn", "blinkerRightOn"]
    head = ["=== HAZARD FIELDS (what the panel reads) ==="]
    for k in watch:
        head.append(f"  {k:22} = {data.get(k, '<<NOT IN TELEMETRY>>')}")
    head.append(f"  derived haz (what button syncs) = "
                f"{bool(getf(data,'hazards')) or (bool(getf(data,'blink_l')) and bool(getf(data,'blink_r')))}")
    head.append("")
    head.append("=== FULL TELEMETRY ===")
    txt = "\n".join(head) + "\n" + json.dumps(data, indent=2, default=str)
    return Response(txt, mimetype="text/plain")


@app.route("/manifest.json")
def manifest():
    return jsonify(
        name="RigDeck", short_name="RIGDECK", start_url="/",
        display="fullscreen", background_color="#14171B",
        theme_color="#14171B", orientation="portrait",
        icons=[{"src": "/icon-512.png", "sizes": "512x512",
                "type": "image/png", "purpose": "any maskable"}],
    )


@app.route("/icon-512.png")
def icon():
    return Response(ICON_PNG, mimetype="image/png")


# ----------------------------------------------------------------------
# The phone panel (single page, RigDeck identity)
# ----------------------------------------------------------------------
PAGE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
<meta name="theme-color" content="#14171B">
<link rel="manifest" href="/manifest.json">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<link rel="apple-touch-icon" href="/icon-512.png">
<title>RIGDECK</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Chakra+Petch:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
:root{
  --ink:#14171B; --acc:#FF6A2B; --steel:#1B2026; --well:#111418;
  --line:#2A3038; --lab:#7A838C; --val:#E8ECEF; --amber:#FFD23F;
  --red:#FF5340;
}
*{box-sizing:border-box;-webkit-tap-highlight-color:transparent;user-select:none;-webkit-user-select:none;-webkit-touch-callout:none}
html,body{margin:0;height:100%;background:var(--ink);color:var(--val);
  font-family:'Chakra Petch',sans-serif;overflow-x:hidden}
body::after{content:"";position:fixed;inset:0;pointer-events:none;z-index:9;
  background:repeating-linear-gradient(0deg,rgba(255,255,255,.028) 0 1px,transparent 1px 3px)}
.wrap{max-width:560px;margin:0 auto;padding:10px 12px 26px}

/* header */
header{display:flex;align-items:center;gap:10px;padding:6px 2px 10px;
  border-bottom:1px solid var(--line)}
.hex{width:26px;height:26px;flex:0 0 26px}
h1{font-family:'Chakra Petch';font-weight:700;font-size:18px;letter-spacing:1px;margin:0;color:#C7CDD2}
h1 span{color:var(--acc)}
h1 small{color:var(--lab);font-size:10px;letter-spacing:3px;display:block;font-family:'Chakra Petch';font-weight:600}
.link{margin-left:auto;display:flex;align-items:center;gap:6px;font-weight:600;
  font-size:11px;letter-spacing:2px;color:var(--lab)}
.dot{width:9px;height:9px;border-radius:50%;background:#444;box-shadow:0 0 6px #000}
.dot.ok{background:var(--acc);box-shadow:0 0 8px var(--acc)}
.dot.wait{background:var(--amber);box-shadow:0 0 8px var(--amber)}

/* tabs */
.tabs{display:flex;gap:8px;margin:12px 0}
.tab{flex:1;text-align:center;padding:13px 0;font-weight:700;letter-spacing:1px;font-size:12.5px;
  color:var(--lab);background:var(--steel);border:1px solid var(--line);
  clip-path:polygon(10px 0,100% 0,100% calc(100% - 10px),calc(100% - 10px) 100%,0 100%,0 10px)}
.tab.on{color:var(--ink);background:var(--acc);border-color:var(--acc)}

/* plates */
.plate{position:relative;background:var(--steel);border:1px solid var(--line);
  padding:12px;margin-bottom:12px;
  clip-path:polygon(12px 0,100% 0,100% calc(100% - 12px),calc(100% - 12px) 100%,0 100%,0 12px)}
.plate .pt{font-size:11px;font-weight:700;letter-spacing:3px;color:var(--lab);margin:0 0 10px}
.tick{position:absolute;width:10px;height:10px;border-color:var(--acc);border-style:solid;opacity:.55}
.tick.tl{top:3px;left:3px;border-width:1px 0 0 1px}
.tick.br{bottom:3px;right:3px;border-width:0 1px 1px 0}

/* switch rows */
.row2{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.row1{display:grid;grid-template-columns:1fr;gap:10px}
.row3{display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px}
.sw{position:relative}
.well{background:var(--well);border:1px solid var(--line);padding:6px;
  box-shadow:inset 0 3px 8px rgba(0,0,0,.7)}
.cap{background:linear-gradient(180deg,#232830,#161A20);border:1px solid #39414C;
  padding:16px 4px;text-align:center;font-weight:700;letter-spacing:2px;font-size:14px;
  color:var(--val);transition:transform .05s, box-shadow .05s, border-color .05s}
.sw.held .cap{transform:translateY(2px);border-color:var(--acc);color:var(--acc);
  box-shadow:0 0 14px rgba(255,106,43,.45), inset 0 0 8px rgba(255,106,43,.15)}
.cap small{display:block;font-size:9px;letter-spacing:2px;color:var(--lab);margin-top:3px}

/* engine start button */
.pd .well{height:100%;box-sizing:border-box}
.pd .cap{padding:12px 4px;cursor:pointer;height:100%;box-sizing:border-box;
  display:flex;flex-direction:column;align-items:center;justify-content:center}
.pd .cap:active{transform:translateY(2px)}
/* tap-style bars (wipers, axles, reset) get the same physical press as the
   tiles above — .sw.held covers hold-buttons, this covers a plain tap. */
.sw .cap:active{transform:translateY(2px);border-color:var(--acc);color:var(--acc)}
.bicon{width:36px;height:36px;display:block;margin:0 auto 4px;color:var(--lab)}
.pd.on .bicon,.pd.run .bicon{color:var(--acc);filter:drop-shadow(0 0 8px rgba(255,106,43,.55))}
.pd.on .cap,.pd.run .cap{border-color:var(--acc);color:var(--acc)}
.pd.park .bicon{color:var(--acc);opacity:.45}
.pd#haz.on .bicon{color:#ff4d4d;opacity:1}
@keyframes hazflash{
  0%,100%{border-color:#ff4d4d;box-shadow:0 0 16px rgba(255,60,60,.65)}
  50%{border-color:rgba(255,77,77,.25);box-shadow:0 0 4px rgba(255,60,60,.15)}}
.pd#haz.on{animation:hazflash .55s infinite}
.pd.locked .cap{opacity:.45}
.fired .cap{border-color:var(--acc)!important;color:var(--acc);
  box-shadow:0 0 14px rgba(255,106,43,.5)}
.sw.lit .cap{border-color:var(--acc);color:var(--acc);
  box-shadow:0 0 12px rgba(255,106,43,.4)}
.sub{font-size:9px;font-weight:700;letter-spacing:2px;color:var(--lab);margin:10px 0 6px}
.sub:first-of-type{margin-top:0}
@keyframes pdflash{0%,100%{border-color:var(--line);box-shadow:none}
  50%{border-color:var(--amber);box-shadow:0 0 16px rgba(255,210,63,.35)}}
.plate.alert{animation:pdflash 1.1s infinite}
.updbar[hidden]{display:none}
.updbar{display:flex;align-items:center;gap:10px;margin:0 0 12px;padding:9px 12px;
  border:1px solid rgba(199,205,210,.22);border-left:3px solid var(--amber);
  border-radius:10px;background:rgba(199,205,210,.05);cursor:default;user-select:none}
.updbar .ub-l{font:800 10px/1 "Chakra Petch",sans-serif;letter-spacing:1.5px;
  color:#0b0d10;background:var(--amber);padding:3px 6px;border-radius:4px;flex:0 0 auto}
.updbar .ub-t{color:#c7cdd2;font-weight:600;font-size:12.5px;flex:1 1 auto}
.updbar .ub-pc{color:#8A917A;font-weight:700;font-size:10px;letter-spacing:1px;
  border:1px solid rgba(138,145,122,.4);border-radius:5px;padding:3px 6px;flex:0 0 auto}

/* rig page */
.bar2{height:10px;background:var(--well);border:1px solid var(--line);
  margin-bottom:10px;overflow:hidden}
.fill2{height:100%;width:0%;background:var(--acc);
  box-shadow:0 0 8px rgba(255,106,43,.5);transition:width .4s}
.fill2.low{background:var(--amber);box-shadow:0 0 8px rgba(255,210,63,.5)}
.cell .v.low{color:var(--amber);text-shadow:0 0 10px rgba(255,210,63,.3)}
.fuelchk{display:flex;align-items:center;gap:10px;margin-top:10px;
  background:var(--well);border:1px solid var(--line);
  border-left:3px solid var(--acc);padding:9px 12px}
.fuelchk .fclamp{width:10px;height:10px;border-radius:50%;flex:0 0 10px;
  background:var(--acc);box-shadow:0 0 8px rgba(255,106,43,.5)}
.fuelchk .fctxt{font-weight:700;letter-spacing:1px;font-size:12px;color:var(--lab)}
.fuelchk.ok{border-left-color:#59B06B}
.fuelchk.ok .fclamp{background:#59B06B;box-shadow:0 0 8px rgba(89,176,107,.5)}
.fuelchk.ok .fctxt{color:#9AA3AC}
.fuelchk.warn{border-left-color:var(--amber)}
.fuelchk.warn .fclamp{background:var(--amber);box-shadow:0 0 8px rgba(255,210,63,.6)}
.fuelchk.warn .fctxt{color:var(--amber)}
.fuelchk.crit{border-left-color:var(--red)}
.fuelchk.crit .fclamp{background:var(--red);box-shadow:0 0 10px rgba(255,83,64,.7)}
.fuelchk.crit .fctxt{color:var(--red)}

/* trailer guard */
.guard{position:relative}
.guard .ring{position:absolute;inset:0;pointer-events:none;opacity:0}
.guard.arming .ring{opacity:1}
.guard .cap{padding:20px 4px}
.guard .bar{height:3px;background:#20241a;margin-top:8px;overflow:hidden}
.guard .fill{height:100%;width:0%;background:var(--amber)}
.guard.fired .cap{border-color:var(--acc);color:var(--acc);
  box-shadow:0 0 16px rgba(255,106,43,.6)}

/* tacho readouts */
.speed{font-size:64px;font-weight:700;line-height:1;text-align:center;color:var(--acc);
  text-shadow:0 0 18px rgba(255,106,43,.35)}
.speed small{font-size:14px;color:var(--lab);letter-spacing:3px;display:block;font-weight:600}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:12px}
.cell{background:var(--well);border:1px solid var(--line);padding:8px 10px}
.cell .l{font-size:10px;font-weight:700;letter-spacing:2px;color:var(--lab)}
.cell .v{font-size:22px;font-weight:700;color:var(--val)}
.cell .v em{font-style:normal;font-size:12px;color:var(--lab)}
.tripbtn{margin-top:6px;width:100%;background:none;border:1px solid var(--line);
  color:var(--lab);font-family:inherit;font-weight:700;letter-spacing:2px;font-size:10px;padding:5px}
.tripbtn:active{color:var(--acc);border-color:var(--acc)}

/* consignment */
.con .hd{display:flex;align-items:center;justify-content:space-between;margin-bottom:10px}
.chip{font-size:10px;font-weight:700;letter-spacing:2px;padding:3px 9px;border:1px solid var(--line);color:var(--lab)}
.chip.collect{color:var(--ink);background:var(--amber);border-color:var(--amber)}
.chip.loaded{color:var(--ink);background:var(--acc);border-color:var(--acc)}
.con .crow{display:grid;grid-template-columns:64px 1fr;gap:8px;align-items:baseline;
  padding:7px 0;border-top:1px dashed var(--line)}
.con .crow:first-of-type{border-top:0}
.con .cl{font-size:10px;font-weight:700;letter-spacing:2px;color:var(--lab)}
.con .cv{font-size:19px;font-weight:700;color:var(--val);text-transform:uppercase}
.con .cv span{color:var(--lab);font-size:13px;font-weight:600;text-transform:none}
.con .cv.acid{color:var(--acc)}
.jstrip{display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;margin-top:10px}
.jcell{background:var(--well);border:1px solid var(--line);padding:6px 4px;text-align:center}
.jcell .l{font-size:9px;font-weight:700;letter-spacing:2px;color:var(--lab)}
.jcell .v{font-size:16px;font-weight:700;color:var(--val);white-space:nowrap}
.jcell .v.low{color:var(--amber);text-shadow:0 0 10px rgba(255,210,63,.35)}
.chips{display:flex;gap:6px}
.chip.failed{color:var(--ink);background:var(--amber);border-color:var(--amber)}
.chip.fail{color:#fff;background:var(--red);border-color:var(--red)}

/* big action button (JOB COMPLETED) */
.bigbtn{width:100%;padding:16px;font-family:inherit;font-weight:700;
  letter-spacing:2px;font-size:15px;border:1px solid var(--acc);
  background:var(--acc);color:var(--ink);cursor:pointer}
.bigbtn:active{transform:translateY(1px)}
.bigbtn.locked{background:transparent;border-color:var(--red);
  color:var(--red);opacity:.7;cursor:not-allowed}
.bigbtn.armed{box-shadow:0 0 16px rgba(255,106,43,.5)}

/* proof-of-delivery sheet (inside a job row) */
.pod{border-top:1px dashed var(--line);margin-top:10px;padding-top:12px}
.pod .podh{font-size:10px;font-weight:700;letter-spacing:3px;color:var(--lab);margin-bottom:8px}
.sigwrap{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:6px}
.sigbox{background:#fbfbf7;border:1px solid var(--line);padding:6px 8px 4px;position:relative}
.sigsvg{width:100%;height:44px;display:block}
.sigcap{font-size:9px;font-weight:700;letter-spacing:1px;color:#3a3f30;
  border-top:1px solid #cfd2c4;padding-top:3px;margin-top:2px}
.sigcap span{display:block;color:#6f745f;font-weight:600;letter-spacing:0}
.cmt{width:100%;box-sizing:border-box;margin-top:10px;background:var(--well);
  border:1px solid var(--line);color:var(--val);font-family:inherit;
  font-size:13px;padding:8px;resize:vertical;min-height:52px;letter-spacing:.5px}
.cmt:focus{outline:none;border-color:var(--acc)}
.cmtsave{margin-top:6px;background:none;border:1px solid var(--line);color:var(--lab);
  font-family:inherit;font-weight:700;letter-spacing:2px;font-size:10px;padding:6px 12px}
.cmtsave:active{color:var(--acc);border-color:var(--acc)}
.podlogo{display:inline-flex;align-items:center;gap:7px;margin-bottom:8px}
.podlogo .lm{width:20px;height:20px;flex:0 0 20px}
.podlogo .lt{font-family:'Chakra Petch';font-size:13px;color:var(--acc);letter-spacing:1px}
.empty{color:var(--lab);font-size:12px;letter-spacing:2px;text-align:center;
  padding:18px 0;font-weight:600}
.jrow{border:1px solid var(--line);background:var(--well);margin-bottom:10px}
.jrow .jh{display:flex;align-items:center;gap:8px;padding:10px 10px 8px;flex-wrap:wrap}
.jrow .jc{font-weight:700;font-size:16px;text-transform:uppercase;color:var(--val)}
.jrow .jr{font-size:11px;color:var(--lab);font-weight:600;width:100%;
  letter-spacing:1px;text-transform:uppercase}
.jdet{display:none;border-top:1px dashed var(--line);padding:10px}
.jrow.open .jdet{display:block}
.jgrid{display:grid;grid-template-columns:1fr 1fr;gap:8px}
.wm{position:fixed;bottom:8px;left:0;right:0;text-align:center;font-size:9px;
  letter-spacing:4px;color:#2e332255;pointer-events:none;font-weight:700}
.page{display:none}.page.on{display:block}
</style>
</head>
<body>
<div class="wrap">
  <header>
    <svg class="hex" viewBox="0 0 120 120"><polygon points="18,6 102,6 114,18 114,102 102,114 18,114 6,102 6,18"
      fill="none" stroke="#C7CDD2" stroke-width="8"/>
      <rect x="30" y="53" width="60" height="14" rx="4" fill="#FF6A2B"/></svg>
    <h1>RIG<span>DECK</span><small>CAB PANEL · V""" + APP_VERSION + """</small></h1>
    <div class="link"><span id="lt">LINK</span><span class="dot" id="dot"></span></div>
  </header>

  <div id="updbar" class="updbar" hidden>
    <span class="ub-l">UPDATE</span>
    <span class="ub-t" id="updtxt">A new version is available</span>
    <span class="ub-pc">INSTALL ON PC</span>
  </div>

  <div class="tabs">
    <div class="tab on" data-p="controls">CONTROLS</div>
    <div class="tab" data-p="job">ACTIVE JOB</div>
    <div class="tab" data-p="status">STATUS</div>
    <div class="tab" data-p="jobs">JOBS</div>
  </div>

  <!-- ============ CONTROLS ============ -->
  <div class="page on" id="p-controls">
    <div class="plate" id="predrive"><span class="tick tl"></span><span class="tick br"></span>
      <p class="pt">IGNITION</p>
      <div class="row3">
        <div class="pd" id="engstart">
          <div class="well"><div class="cap">
            <svg class="bicon" viewBox="0 0 48 48">
              <circle cx="24" cy="27" r="13" fill="none" stroke="currentColor" stroke-width="6"/>
              <path d="M24 7 V21" stroke="currentColor" stroke-width="6" stroke-linecap="round"/>
            </svg>
            <small id="startlbl">START</small>
          </div></div>
        </div>
        <div class="pd" id="haz">
          <div class="well"><div class="cap">
            <svg class="bicon" viewBox="0 0 48 48">
              <path d="M24 8 L41 38 H7 Z" fill="none" stroke="currentColor"
                stroke-width="3.5" stroke-linejoin="round"/>
              <line x1="24" y1="19" x2="24" y2="29" stroke="currentColor"
                stroke-width="3.5" stroke-linecap="round"/>
              <circle cx="24" cy="33.5" r="1.9" fill="currentColor"/>
            </svg>
            <small id="hazlbl">HAZARDS</small>
          </div></div>
        </div>
        <div class="pd" id="park">
          <div class="well"><div class="cap">
            <svg class="bicon" viewBox="0 0 48 48">
              <circle cx="24" cy="24" r="18" fill="none" stroke="currentColor" stroke-width="4"/>
              <path d="M20 15 h6 a4.5 4.5 0 0 1 0 9 h-6 z M20 15 v18" fill="none"
                stroke="currentColor" stroke-width="4" stroke-linejoin="round"/>
            </svg>
            <small id="parklbl">PARK BRAKE</small>
          </div></div>
        </div>
      </div>
      <div class="row1" style="margin-top:10px">
        <div class="sw" id="wipers"><div class="well"><div class="cap">WIPERS<small id="wiperlbl">TAP</small></div></div></div>
      </div>
    </div>
    <div class="plate"><span class="tick tl"></span><span class="tick br"></span>
      <p class="pt">LIGHTS</p>
      <div class="row2">
        <div class="pd" id="headl">
          <div class="well"><div class="cap">
            <svg class="bicon" viewBox="0 0 48 48">
              <path d="M20 10 C10 14 10 34 20 38 L26 38 L26 10 Z"
                fill="none" stroke="currentColor" stroke-width="5"/>
              <path d="M31 13 L42 17 M31 22 L42 26 M31 31 L42 35"
                stroke="currentColor" stroke-width="4" stroke-linecap="round"/>
            </svg>
            <small id="headlbl">OFF</small>
          </div></div>
        </div>
        <div class="pd" id="highb">
          <div class="well"><div class="cap">
            <svg class="bicon" viewBox="0 0 48 48">
              <path d="M20 10 C10 14 10 34 20 38 L26 38 L26 10 Z"
                fill="none" stroke="currentColor" stroke-width="5"/>
              <path d="M31 14 L43 14 M31 24 L43 24 M31 34 L43 34"
                stroke="currentColor" stroke-width="4" stroke-linecap="round"/>
            </svg>
            <small id="highlbl">OFF</small>
          </div></div>
        </div>
      </div>
    </div>
    <div class="plate"><span class="tick tl"></span><span class="tick br"></span>
      <p class="pt">LEFT WINDOW</p>
      <div class="row2">
        <div class="sw" data-key="lbracket"><div class="well"><div class="cap">OPEN<small>HOLD</small></div></div></div>
        <div class="sw" data-key="rbracket"><div class="well"><div class="cap">CLOSE<small>HOLD</small></div></div></div>
      </div>
    </div>
    <div class="plate"><span class="tick tl"></span><span class="tick br"></span>
      <p class="pt">RIGHT WINDOW</p>
      <div class="row2">
        <div class="sw" data-key="semicolon"><div class="well"><div class="cap">OPEN<small>HOLD</small></div></div></div>
        <div class="sw" data-key="quote"><div class="well"><div class="cap">CLOSE<small>HOLD</small></div></div></div>
      </div>
    </div>
    <div class="plate"><span class="tick tl"></span><span class="tick br"></span>
      <p class="pt">COUPLE / RELEASE</p>
      <div class="sw guard" id="trailer">
        <div class="well"><div class="cap">COUPLE / RELEASE<small>HOLD 0.6 S TO ARM</small>
          <div class="bar"><div class="fill" id="tfill"></div></div>
        </div></div>
      </div>
    </div>
    <div class="plate"><span class="tick tl"></span><span class="tick br"></span>
      <p class="pt">LIFT / DROP</p>
      <div class="sw" id="cabaxle"><div class="well"><div class="cap">CAB AXLE<small id="cabaxlelbl">TAP</small></div></div></div>
      <div class="sw" id="axlelift"><div class="well"><div class="cap">TRAILER AXLE<small id="axlelbl">TAP</small></div></div></div>
    </div>
    <div class="plate"><span class="tick tl"></span><span class="tick br"></span>
      <p class="pt">DIFF LOCK</p>
      <div class="sw" id="difflock"><div class="well"><div class="cap">DIFF LOCK<small id="difflbl">TAP</small></div></div></div>
    </div>
    <div class="plate"><span class="tick tl"></span><span class="tick br"></span>
      <p class="pt">SUSPENSION</p>
      <p class="sub">FRONT</p>
      <div class="row2">
        <div class="sw" data-key="num8"><div class="well"><div class="cap">RAISE<small>HOLD</small></div></div></div>
        <div class="sw" data-key="num2"><div class="well"><div class="cap">LOWER<small>HOLD</small></div></div></div>
      </div>
      <p class="sub">REAR</p>
      <div class="row2">
        <div class="sw" data-key="num4"><div class="well"><div class="cap">RAISE<small>HOLD</small></div></div></div>
        <div class="sw" data-key="num6"><div class="well"><div class="cap">LOWER<small>HOLD</small></div></div></div>
      </div>
      <p class="sub">TRAILER</p>
      <div class="row2">
        <div class="sw" data-key="num0"><div class="well"><div class="cap">RAISE<small>HOLD</small></div></div></div>
        <div class="sw" data-key="numdot"><div class="well"><div class="cap">LOWER<small>HOLD</small></div></div></div>
      </div>
      <p class="sub">LEVEL</p>
      <div class="sw" id="suspreset"><div class="well"><div class="cap">RESET<small>TAP</small></div></div></div>
    </div>
  </div>

  <!-- ============ ACTIVE JOB ============ -->
  <div class="page" id="p-job">
    <div class="plate con"><span class="tick tl"></span><span class="tick br"></span>
      <div class="hd"><p class="pt" style="margin:0">CONSIGNMENT</p>
        <span class="chips"><span class="chip" id="jchip2" style="display:none">--</span><span class="chip" id="jchip">NO JOB</span></span></div>
      <div class="crow"><div class="cl">CARGO</div><div class="cv acid" id="jcargo">--</div></div>
      <div class="crow"><div class="cl">GROSS</div><div class="cv" id="jmass">--</div></div>
      <div class="crow"><div class="cl">FROM</div><div class="cv" id="jfrom">--</div></div>
      <div class="crow"><div class="cl">TO</div><div class="cv" id="jto">--</div></div>
      <div class="jstrip">
        <div class="jcell"><div class="l">DUE</div><div class="v" id="jdue">--</div></div>
        <div class="jcell"><div class="l">LEFT</div><div class="v" id="jleft">--</div></div>
        <div class="jcell"><div class="l">INCOME</div><div class="v" id="jpay">--</div></div>
      </div>
    </div>

    <div class="plate"><span class="tick tl"></span><span class="tick br"></span>
      <p class="pt">ROUTE</p>
      <div class="grid" style="margin-top:0">
        <div class="cell"><div class="l">ETA</div><div class="v" id="jeta">--</div></div>
        <div class="cell"><div class="l">DISTANCE</div><div class="v" id="jroute">--</div></div>
      </div>
      <div class="fuelchk" id="fuelchk">
        <span class="fclamp" id="fclamp"></span>
        <span class="fctxt" id="fctxt">FUEL RANGE OK</span>
      </div>
    </div>

    <div class="plate"><span class="tick tl"></span><span class="tick br"></span>
      <p class="pt">PROOF OF DELIVERY</p>
      <p class="sub" style="margin-top:0" id="podhint">DELIVER THE LOAD TO ENABLE</p>
      <button class="bigbtn locked" id="completebtn" disabled>JOB COMPLETED</button>
    </div>
  </div>

  <!-- ============ STATUS ============ -->
  <div class="page" id="p-status">
    <div class="plate"><span class="tick tl"></span><span class="tick br"></span>
      <div class="speed"><span id="spd">--</span><small>KM/H</small></div>
      <div class="grid">
        <div class="cell"><div class="l">REST IN</div><div class="v" id="rest">--</div></div>
        <div class="cell"><div class="l">ETA</div><div class="v" id="eta">--</div></div>
        <div class="cell"><div class="l">ROUTE</div><div class="v" id="route">--</div></div>
        <div class="cell"><div class="l">ODOMETER</div><div class="v" id="odo">--</div></div>
        <div class="cell" style="grid-column:1/3"><div class="l">TRIP</div>
          <div class="v" id="trip">--</div>
          <button class="tripbtn" id="tripreset">RESET TRIP</button></div>
      </div>
    </div>
    <div class="plate"><span class="tick tl"></span><span class="tick br"></span>
      <p class="pt">FUEL</p>
      <div class="bar2"><div class="fill2" id="fbar"></div></div>
      <div class="grid">
        <div class="cell"><div class="l">LEVEL</div><div class="v" id="rfuel">--</div></div>
        <div class="cell"><div class="l">RANGE</div><div class="v" id="rrange">--</div></div>
        <div class="cell" style="grid-column:1/3"><div class="l">AVERAGE</div><div class="v" id="ravg">--</div></div>
      </div>
    </div>
    <div class="plate"><span class="tick tl"></span><span class="tick br"></span>
      <p class="pt">ADBLUE</p>
      <div class="bar2"><div class="fill2" id="abar"></div></div>
      <div class="grid">
        <div class="cell" style="grid-column:1/3"><div class="l">LEVEL</div><div class="v" id="radb">--</div></div>
      </div>
    </div>
    <div class="plate"><span class="tick tl"></span><span class="tick br"></span>
      <p class="pt">AIR &amp; BRAKES</p>
      <div class="grid" style="margin-top:0">
        <div class="cell"><div class="l">AIR PRESSURE</div><div class="v" id="rair">--</div></div>
        <div class="cell"><div class="l">BRAKE TEMP</div><div class="v" id="rbrk">--</div></div>

      </div>
    </div>
    <div class="plate"><span class="tick tl"></span><span class="tick br"></span>
      <p class="pt">ENGINE</p>
      <div class="grid" style="margin-top:0">
        <div class="cell"><div class="l">OIL TEMP</div><div class="v" id="roilt">--</div></div>
        <div class="cell"><div class="l">OIL PRESSURE</div><div class="v" id="roilp">--</div></div>
        <div class="cell"><div class="l">WATER</div><div class="v" id="rwat">--</div></div>
        <div class="cell"><div class="l">BATTERY</div><div class="v" id="rbat">--</div></div>
      </div>
    </div>
    <div class="plate"><span class="tick tl"></span><span class="tick br"></span>
      <p class="pt">WEAR</p>
      <div class="grid" style="margin-top:0">
        <div class="cell"><div class="l">ENGINE</div><div class="v" id="weng">--</div></div>
        <div class="cell"><div class="l">TRANSMISSION</div><div class="v" id="wtra">--</div></div>
        <div class="cell"><div class="l">CABIN</div><div class="v" id="wcab">--</div></div>
        <div class="cell"><div class="l">CHASSIS</div><div class="v" id="wcha">--</div></div>
        <div class="cell" style="grid-column:1/3"><div class="l">WHEELS</div><div class="v" id="wwhe">--</div></div>
      </div>
    </div>
  </div>

  <!-- ============ JOBS ============ -->
  <div class="page" id="p-jobs">
    <div class="plate con"><span class="tick tl"></span><span class="tick br"></span>
      <div class="hd"><p class="pt" style="margin:0">SESSION LOG</p>
        <span class="chip" id="jobcount">0 JOBS</span></div>
      <div id="joblist"><p class="empty">NO JOBS LOGGED THIS SESSION</p></div>
    </div>
  </div>
</div>
<div class="wm">RIGDECK</div>

<script>
const $=id=>document.getElementById(id);
const post=(u,b)=>fetch(u,{method:"POST",headers:{"Content-Type":"application/json"},
  body:JSON.stringify(b||{})}).catch(()=>{});

/* tabs */
document.querySelectorAll(".tab").forEach(t=>t.addEventListener("click",()=>{
  document.querySelectorAll(".tab").forEach(x=>x.classList.remove("on"));
  document.querySelectorAll(".page").forEach(x=>x.classList.remove("on"));
  t.classList.add("on");$("p-"+t.dataset.p).classList.add("on");
  if(t.dataset.p==="jobs")loadJobs();
  if(!_autoNav){ _autoOnStatus=false; _holdUntil=performance.now()+AUTO_HOLD_MS; }
}));

/* hold switches */
document.querySelectorAll(".sw[data-key]").forEach(sw=>{
  const key=sw.dataset.key;let iv=null;
  const down=e=>{e.preventDefault();sw.classList.add("held");
    post("/press",{key});iv=setInterval(()=>post("/press",{key}),1200);};
  const up=()=>{if(!iv&&!sw.classList.contains("held"))return;
    sw.classList.remove("held");clearInterval(iv);iv=null;post("/release",{key});};
  sw.addEventListener("pointerdown",down);
  ["pointerup","pointercancel","pointerleave"].forEach(ev=>sw.addEventListener(ev,up));
});

/* trailer guard: hold 600 ms then fire a single T tap */
(()=>{
  const g=$("trailer"),fill=$("tfill");let t0=0,raf=null,armed=false;
  const step=()=>{const p=Math.min(1,(performance.now()-t0)/600);
    fill.style.width=(p*100)+"%";
    if(p>=1&&!armed){armed=true;post("/tap",{key:"t"});
      g.classList.add("fired");navigator.vibrate&&navigator.vibrate(40);
      setTimeout(()=>g.classList.remove("fired"),450);}
    if(p<1)raf=requestAnimationFrame(step);};
  const down=e=>{e.preventDefault();armed=false;t0=performance.now();
    g.classList.add("arming");raf=requestAnimationFrame(step);};
  const up=()=>{g.classList.remove("arming");cancelAnimationFrame(raf);
    fill.style.width="0%";};
  g.addEventListener("pointerdown",down);
  ["pointerup","pointercancel","pointerleave"].forEach(ev=>g.addEventListener(ev,up));
})();

/* engine start */
let _fcState=null;   // fuel-reachability hysteresis state: null|"ok"|"warn"|"crit"
let _moveSince=null, _stopSince=null, _autoOnStatus=false;
let _holdUntil=0, _wasPending=false, _wasLoaded=false;
let engineOn=false;
const startEl=$("engstart");
function drawPD(){
  startEl.classList.toggle("run",engineOn);
  $("startlbl").textContent=engineOn?"RUNNING":"START";
}
startEl.addEventListener("click",()=>{post("/tap",{key:"engine"});});
let parkOn=false;
const parkEl=$("park");
function drawPark(){parkEl.classList.toggle("on",parkOn);
  $("parklbl").textContent=parkOn?"BRAKE SET":"PARK BRAKE";}
parkEl.addEventListener("click",()=>{parkOn=!parkOn;post("/tap",{key:"park"});
  navigator.vibrate&&navigator.vibrate(25);drawPark();});
let diffOn=false;
const dflEl=$("difflock");
function drawDiff(){dflEl.classList.toggle("lit",diffOn);
  $("difflbl").textContent=diffOn?"ENGAGED":"OFF";}
dflEl.addEventListener("click",()=>{
  diffOn=!diffOn;post("/tap",{key:"diff"});
  dflEl.classList.add("fired");setTimeout(()=>dflEl.classList.remove("fired"),300);
  navigator.vibrate&&navigator.vibrate(25);drawDiff();});

let hazOn=false;
const hazEl=$("haz");
function drawHaz(){hazEl.classList.toggle("on",hazOn);
  $("hazlbl").textContent=hazOn?"HAZARDS ON":"HAZARDS";}
hazEl.addEventListener("click",()=>{hazOn=!hazOn;post("/tap",{key:"haz"});
  navigator.vibrate&&navigator.vibrate(25);drawHaz();});
/* tap buttons: lights, high beam, suspension reset */
const tapBtn=(id,key)=>{const el=$(id);el.addEventListener("click",()=>{
  post("/tap",{key});el.classList.add("fired");
  navigator.vibrate&&navigator.vibrate(25);
  setTimeout(()=>el.classList.remove("fired"),300);});};
tapBtn("headl","l");tapBtn("highb","k");tapBtn("suspreset","num5");tapBtn("wipers","v");
tapBtn("axlelift","numminus");tapBtn("cabaxle","cabaxle");

let ac=null;
function tone(f1,f2,dur){try{ac=ac||new (window.AudioContext||window.webkitAudioContext)();
  const o=ac.createOscillator(),g=ac.createGain();o.connect(g);g.connect(ac.destination);
  o.type="sine";o.frequency.setValueAtTime(f1,ac.currentTime);
  o.frequency.setValueAtTime(f2,ac.currentTime+dur*0.45);
  g.gain.setValueAtTime(.10,ac.currentTime);
  g.gain.exponentialRampToValueAtTime(.001,ac.currentTime+dur);
  o.start();o.stop(ac.currentTime+dur+.02);}catch(e){}}
/* fuel: slow low double-beep (440->330). */
const _iv={};
function alarm(name,on,fn,gap){
  if(on&&!_iv[name]){fn();_iv[name]=setInterval(fn,gap);}
  if(!on&&_iv[name]){clearInterval(_iv[name]);_iv[name]=null;}}
const dingFuel=()=>{tone(440,330,.22);setTimeout(()=>tone(440,330,.22),300);};
function fuelChime(on){alarm("fuel",on,dingFuel,4000);}
/* range alert: three descending notes, played ONCE on the warning's rising edge */
function dingRange(){tone(660,660,.16);setTimeout(()=>tone(550,550,.16),200);
  setTimeout(()=>tone(440,440,.26),400);}
let _rangeArmed=false;
function rangeAlert(bad){
  if(bad&&!_rangeArmed){_rangeArmed=true;dingRange();
    navigator.vibrate&&navigator.vibrate([80,50,80]);}
  if(!bad)_rangeArmed=false;   // re-arm once you're OK again (refuelled / re-routed)
}

/* formatting */
const hm=m=>{if(m==null||isNaN(m))return"--";m=Math.max(0,Math.round(m));
  return Math.floor(m/60)+"h "+String(m%60).padStart(2,"0")+"m";};
const km=v=>v==null?"--":(v>=100?Math.round(v):v.toFixed(1));
/* game clock: minutes since a Monday-origin epoch, matches route advisor */
const DAYS=["MON","TUE","WED","THU","FRI","SAT","SUN"];
const due=m=>{if(m==null)return"--";
  const d=DAYS[Math.floor(m/1440)%7];
  const h=String(Math.floor((m%1440)/60)).padStart(2,"0");
  const mm=String(Math.floor(m%60)).padStart(2,"0");
  return d+" "+h+":"+mm;};
const left=m=>{if(m==null)return"--";const late=m<0;m=Math.abs(m);
  const dd=Math.floor(m/1440),h=Math.floor((m%1440)/60),mm=Math.floor(m%60);
  const s=(dd?dd+"d ":"")+h+"h "+String(mm).padStart(2,"0")+"m";
  return late?"LATE "+s:s;};

/* telemetry poll */
let _updChecked=false;
const AUTO_TAB = __AUTOTAB__;
const AUTO_MOVE_MS = __AUTOMOVEMS__, AUTO_STOP_MS = __AUTOSTOPMS__;
const AUTO_HOLD_MS = __AUTOHOLDMS__;
let _autoNav=false;
function goTab(p){
  const t=document.querySelector('.tab[data-p="'+p+'"]');
  if(t && !t.classList.contains("on")){ _autoNav=true; t.click(); _autoNav=false; }
}
async function checkUpdate(){
  try{
    const r=await fetch("/update");const u=await r.json();
    if(u&&u.outdated&&u.latest){
      $("updtxt").textContent="Version "+u.latest+" ready \u2014 update from the RigDeck window on your PC";
      $("updbar").hidden=false;
    }
  }catch(e){}
}
async function poll(){
  if(!_updChecked){_updChecked=true;checkUpdate();}
  try{
    const r=await fetch("/telemetry");const d=await r.json();
    const dot=$("dot");
    if(!d.game){dot.className="dot wait";$("lt").textContent="GAME";
      engineOn=false;parkOn=false;drawPark();hazOn=false;drawHaz();$("wipers").classList.remove("lit");$("wiperlbl").textContent="TAP";diffOn=false;drawDiff();fuelChime(false);rangeAlert(false);drawPD();
      _moveSince=null;_stopSince=null;_autoOnStatus=false;_holdUntil=0;_wasPending=false;_wasLoaded=false;
      return;}
    dot.className="dot ok";$("lt").textContent="LINK";
    engineOn=!!d.engine;
    parkOn=!!d.park;drawPark();
    /* wipers */
    const wp=$("wipers");
    if(!("wipers" in d)){wp.classList.remove("lit");$("wiperlbl").textContent="TAP";}
    else{wp.classList.toggle("lit",!!d.wipers);
      $("wiperlbl").textContent=d.wipers?"ON":"OFF";}
    // hazards: this telemetry plugin does not report hazard state (no
    // lightsHazards field, blinker flags stay false), so the button simply
    // tracks its own on/off state. It starts OFF on each connect; if hazards
    // happen to be physically on, one tap syncs them. The button latches its
    // don't report. It stays lit + flashing until you press it again.
    drawPD();

    /* lights: mirror actual truck state (works for keyboard use too) */
    const L=d.lights||{};
    const he=$("headl");
    he.classList.toggle("on",!!L.low);
    he.classList.toggle("park",!L.low&&!!L.park);
    $("headlbl").textContent=L.low?"ON":(L.park?"PARK":"OFF");
    const hb=$("highb");
    hb.classList.toggle("on",!!L.high);
    $("highlbl").textContent=L.high?"ON":"OFF";

    /* If the plugin reports differentialLock, that's authoritative — the light
       then follows the truck even if you toggle it from the keyboard. If it
       doesn't report it (some builds don't, same as hazards), fall back to the
       button remembering its own state so it still stays lit while engaged. */
    if(d.diff!=null) diffOn=!!d.diff;
    drawDiff();

    /* trailer lift axle */
    const axl=$("axlelift");
    if(d.axle==null){axl.classList.remove("lit");$("axlelbl").textContent="TAP";}
    else{axl.classList.toggle("lit",d.axle);
      $("axlelbl").textContent=d.axle?"LIFTED":"DOWN";}

    /* auto tab switching. The cycle:
         drop the load  -> ACTIVE JOB (so COMPLETE is right there)
         drive away     -> STATUS after a few seconds of sustained movement
         stop           -> back to CONTROLS
       Tapping a tab yourself pauses all of it so the panel never yanks a page
       away while you're reading. That pause ends at the next collection or
       delivery, so the cycle restarts every run.

       Delivery is detected from cargo LEAVING the trailer, not from the
       COMPLETE button: pending only clears when that button is pressed, so
       relying on it meant one skipped press left auto-switching paused for the
       rest of the session. Cargo state comes straight from telemetry, so it
       follows what the truck is actually doing. */
    if(AUTO_TAB){
      const now=performance.now(), speed=d.speed_kmh||0, cur=document.querySelector(".tab.on").dataset.p;
      const loaded = !!(d.job && d.job.loaded===true);

      const delivered = (d.pending && !_wasPending) || (_wasLoaded && !loaded);
      const collected = (!_wasLoaded && loaded);
      if(delivered || collected){ _holdUntil=0; _autoOnStatus=false; }   // resume the cycle
      if(delivered) goTab("job");
      _wasPending=!!d.pending; _wasLoaded=loaded;

      if(now >= _holdUntil){
        if(speed>5){ if(_moveSince==null)_moveSince=now; }else{ _moveSince=null; }
        if(speed<2){ if(_stopSince==null)_stopSince=now; }else{ _stopSince=null; }
        if(_moveSince!=null && now-_moveSince>AUTO_MOVE_MS && cur!=="status"){ goTab("status"); _autoOnStatus=true; }
        if(_stopSince!=null && now-_stopSince>AUTO_STOP_MS && cur==="status" && _autoOnStatus){ goTab("controls"); _autoOnStatus=false; }
      }
    }

    /* rig page */
    const g=d.rig||{};
    const wv=(id,txt,warn)=>{const el=$(id);el.innerHTML=txt;
      el.classList.toggle("low",!!warn);};
    const fpct=(g.fuel!=null&&g.fuel_cap)?g.fuel/g.fuel_cap*100:0;
    const flow=g.fuel_warn||fpct<15;
    fuelChime(flow&&engineOn&&!d.paused);
    const fb=$("fbar");fb.style.width=fpct+"%";fb.classList.toggle("low",flow);
    wv("rfuel",g.fuel==null?"--":Math.round(g.fuel)+" <em>/ "+Math.round(g.fuel_cap||0)+" L</em>",flow);
    wv("rrange",g.range==null?"--":Math.round(g.range).toLocaleString("en-GB")+" <em>KM</em>"+(g.range_est?" <em style='color:var(--acc)'>&bull;</em>":""),false);
    wv("ravg",g.avg100==null?"--":g.avg100.toFixed(1)+" <em>L/100KM</em>",false);
    const apct=(g.adb!=null&&g.adb_cap)?g.adb/g.adb_cap*100:0;
    const alow=g.adb_cap?apct<15:false;
    const ab=$("abar");ab.style.width=apct+"%";ab.classList.toggle("low",alow);
    wv("radb",!g.adb_cap?"--":Math.round(g.adb)+" <em>/ "+Math.round(g.adb_cap)+" L</em>",alow);
    wv("rair",g.air==null?"--":Math.round(g.air)+" <em>PSI</em>",g.air_warn||(g.air!=null&&g.air<65));
    wv("rbrk",g.brake_c==null?"--":Math.round(g.brake_c)+"<em>°C</em>",false);
    wv("roilt",g.oil_c==null?"--":Math.round(g.oil_c)+"<em>°C</em>",false);
    wv("roilp",g.oil_p==null?"--":Math.round(g.oil_p)+" <em>PSI</em>",g.oil_warn);
    wv("rwat",g.water_c==null?"--":Math.round(g.water_c)+"<em>°C</em>",g.water_warn);
    wv("rbat",g.batt==null?"--":g.batt.toFixed(1)+" <em>V</em>",g.batt_warn);
    const W=g.wear||{};
    const wpc=(id,v)=>wv(id,v==null?"--":Math.round(v*100)+"<em>%</em>",v!=null&&v>0.15);
    wpc("weng",W.eng);wpc("wtra",W.tra);wpc("wcab",W.cab);
    wpc("wcha",W.cha);wpc("wwhe",W.whe);
    $("spd").textContent=Math.round(d.speed_kmh);
    $("rest").textContent=hm(d.rest_min);
    $("eta").textContent=hm(d.route_min);
    $("route").innerHTML=d.route_km==null?"--":km(d.route_km)+" <em>KM</em>";
    $("odo").innerHTML=d.odo_km==null?"--":Math.round(d.odo_km).toLocaleString()+" <em>KM</em>";
    $("trip").innerHTML=d.trip_km==null?"--":d.trip_km.toFixed(1)+" <em>KM</em>";

    /* consignment */
    const j=d.job||{};const chip=$("jchip"),chip2=$("jchip2");
    if(!j.on){chip.textContent="NO JOB";chip.className="chip";chip2.style.display="none";
      ["jcargo","jmass","jfrom","jto","jdue","jleft","jpay"].forEach(i=>$(i).textContent="--");
      $("jleft").classList.remove("low");}
    else{
      chip.textContent="ON ROUTE";chip.className="chip loaded";
      /* Cargo state. Must come from real cargo data, not from whether a
         trailer is hitched: an owned trailer is always hitched, so coupling
         would wrongly read as LOADED while running empty. */
      if(j.coupled===false){chip2.style.display="";chip2.textContent="NO TRAILER";chip2.className="chip collect";}
      else if(j.loaded===true){chip2.style.display="";chip2.textContent="LOADED";chip2.className="chip loaded";}
      else if(j.loaded===false){chip2.style.display="";chip2.textContent="EMPTY";chip2.className="chip collect";}
      else{chip2.style.display="none";}
      $("jcargo").textContent=j.cargo||"--";
      $("jmass").innerHTML=j.mass_t==null?"--":j.mass_t.toFixed(1)+" <span>t</span>";
      $("jfrom").innerHTML=(j.src_comp||"--")+(j.src_city?" <span>· "+j.src_city+"</span>":"");
      $("jto").innerHTML=(j.dst_comp||"--")+(j.dst_city?" <span>· "+j.dst_city+"</span>":"");
      $("jdue").textContent=due(j.due_min);
      const lf=$("jleft");lf.textContent=left(j.remain_min);
      lf.classList.toggle("low",j.remain_min!=null&&(j.remain_min<120));
      $("jpay").textContent=j.income==null?"--":"\u20AC"+j.income.toLocaleString("en-GB");
    }
    $("jeta").textContent=hm(d.route_min);
    $("jroute").innerHTML=d.route_km==null?"--":km(d.route_km)+" <em>KM</em>";

    /* fuel reachability: can this tank reach the drop? (15% safety margin) */
    const fc=$("fuelchk"),ft=$("fctxt");
    const rng=(d.rig||{}).range, dist=d.route_km;
    const active=(d.job&&d.job.on);
    if(!active||rng==null||dist==null||dist<1){
      fc.className="fuelchk";ft.textContent="FUEL RANGE \u2014";
      rangeAlert(false);_fcState=null;
    }else{
      // hysteresis: once in a worse state, need a bit more margin to climb
      // back out, so small range-estimate wobble near a boundary doesn't
      // flicker the light on and off every poll.
      const over=rng-dist;
      const relax=dist*0.04;                   // ~4% of route as a dead-band
      const margin=dist*1.15;                  // want 15% headroom over the route
      let next=_fcState;
      if(_fcState==="crit"){
        next = (rng < dist+relax) ? "crit" : (rng<margin ? "warn":"ok");
      }else if(_fcState==="warn"){
        next = (rng < dist) ? "crit" : (rng < margin+relax ? "warn":"ok");
      }else{ // ok or null: normal thresholds
        next = (rng<dist)?"crit":(rng<margin?"warn":"ok");
      }
      _fcState=next;
      if(next==="crit"){
        fc.className="fuelchk crit";
        ft.textContent="WON'T REACH \u2014 SHORT BY "+Math.round(Math.max(0,dist-rng))+" KM";
        rangeAlert(true);
      }else if(next==="warn"){
        fc.className="fuelchk warn";
        ft.textContent="TIGHT \u2014 "+Math.round(over)+" KM SPARE, FUEL SOON";
        rangeAlert(true);
      }else{
        fc.className="fuelchk ok";
        ft.textContent="RANGE OK \u2014 "+Math.round(over)+" KM SPARE";
        rangeAlert(false);
      }
    }

    /* proof-of-delivery button arms only once the game confirms delivery */
    const cb=$("completebtn");
    if(d.pending){cb.disabled=false;cb.className="bigbtn armed";
      $("podhint").textContent="DELIVERED — FILE THE RUN";}
    else{cb.disabled=true;cb.className="bigbtn locked";
      $("podhint").textContent="DELIVER THE LOAD TO ENABLE";}
  }catch(e){$("dot").className="dot";$("lt").textContent="OFF";}
}
setInterval(poll,700);poll();

$("tripreset").addEventListener("click",()=>post("/trip/reset"));

/* JOB COMPLETED button files the pending run into the log */
$("completebtn").addEventListener("click",()=>{
  const cb=$("completebtn");if(cb.disabled)return;
  cb.disabled=true;cb.className="bigbtn locked";
  $("podhint").textContent="FILED — SEE JOBS TAB";
  navigator.vibrate&&navigator.vibrate(40);
  post("/job/complete",{comment:""}).then(()=>{jobsCache="";loadJobs();});
});

/* session job log */
let jobsCache="";
async function loadJobs(){
  try{
    const r=await fetch("/jobs");const txt=await r.text();
    if(txt===jobsCache)return;
    jobsCache=txt;renderJobs(JSON.parse(txt));
  }catch(e){}
}
const DECKMARK='<svg class="lm" viewBox="0 0 120 120"><polygon points="18,6 102,6 114,18 114,102 102,114 18,114 6,102 6,18" fill="none" stroke="#C7CDD2" stroke-width="8"/><rect x="30" y="53" width="60" height="14" rx="4" fill="#FF6A2B"/></svg>';
function esc(s){return (s||"").replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));}
function renderJobs(arr){
  $("jobcount").textContent=arr.length+" JOB"+(arr.length===1?"":"S");
  const el=$("joblist");
  if(!arr.length){el.innerHTML='<p class="empty">NO JOBS LOGGED THIS SESSION</p>';return;}
  const cell=(l,v)=>'<div class="cell"><div class="l">'+l+'</div><div class="v">'+(v==null?"--":v)+'</div></div>';
  el.innerHTML=arr.map(J=>{
    const cls=J.status==="FAILED"?"failed":"loaded";
    const route=((J.src_city||"?")+" \u2192 "+(J.dst_city||"?"));
    const avg=(J.dist_km&&J.time_min)?Math.round(J.dist_km/(J.time_min/60))+" KM/H":null;
    const l100=(J.dist_km&&J.fuel_l)?(J.fuel_l/J.dist_km*100).toFixed(1)+" L/100":null;
    const perkm=(J.dist_km&&J.income)?"\u20AC"+Math.round(J.income/J.dist_km):null;
    let del=null;
    if(J.late_min!=null){del=J.late_min>0?hm(J.late_min)+" LATE":hm(-J.late_min)+" EARLY";}
    let pod="";
    if(J.status!=="FAILED"&&J.signoff){const s=J.signoff;
      pod='<div class="pod">'
        +'<div class="podlogo">'+DECKMARK+'</div>'
        +'<div class="podh">PROOF OF DELIVERY</div>'
        +'<div class="sigwrap">'
        +'<div class="sigbox">'+s.driver_sig
          +'<div class="sigcap">DRIVER<span>'+esc(s.driver_name)+'</span></div></div>'
        +'<div class="sigbox">'+s.wh_sig
          +'<div class="sigcap">RECEIVED<span>'+esc(s.wh_name)+' \u00b7 '+esc(s.wh_role)+'</span></div></div>'
        +'</div>'
        +'<textarea class="cmt" data-id="'+J.id+'" placeholder="Additional comments...">'+esc(J.comment)+'</textarea>'
        +'<button class="cmtsave" data-id="'+J.id+'">SAVE COMMENT</button>'
        +'</div>';
    }
    return '<div class="jrow"><div class="jh">'
      +'<span class="chip '+cls+'">'+J.status+'</span>'
      +'<span class="jc">'+esc(J.cargo||"UNKNOWN CARGO")+'</span>'
      +'<span class="jr">'+esc(route)+'</span></div>'
      +'<div class="jdet">'
      +'<div class="crow"><div class="cl">FROM</div><div class="cv">'+esc(J.src_comp||"--")
        +(J.src_city?' <span>\u00b7 '+esc(J.src_city)+'</span>':'')+'</div></div>'
      +'<div class="crow"><div class="cl">TO</div><div class="cv">'+esc(J.dst_comp||"--")
        +(J.dst_city?' <span>\u00b7 '+esc(J.dst_city)+'</span>':'')+'</div></div>'
      +'<div class="jgrid" style="margin-top:8px">'
      +cell("DISTANCE",J.dist_km==null?null:J.dist_km.toFixed(1)+" KM")
      +cell("TIME",J.time_min==null?null:hm(J.time_min))
      +cell("REAL TIME",J.real_s==null?null:(J.real_s<3600?Math.round(J.real_s/60)+"m":Math.floor(J.real_s/3600)+"h "+String(Math.round(J.real_s%3600/60)).padStart(2,"0")+"m"))
      +cell("FUEL USED",J.fuel_l==null?null:J.fuel_l.toFixed(1)+" L")
      +cell("AVG BURN",l100)
      +cell("AVG SPEED",avg)
      +cell("TOP SPEED",J.vmax==null?null:J.vmax+" KM/H")
      +cell("INCOME",J.income==null?null:"\u20AC"+J.income.toLocaleString("en-GB"))
      +cell("PER KM",perkm)
      +cell("CARGO DMG",J.cargo_dmg==null?null:(J.cargo_dmg*100).toFixed(1)+"%")
      +cell("TRUCK DMG",J.truck_dmg==null?null:"+"+(J.truck_dmg*100).toFixed(1)+"%")
      +cell("FINES",!J.fines?null:"\u20AC"+J.fines.toLocaleString("en-GB"))
      +cell("GROSS",J.mass_t==null?null:J.mass_t.toFixed(1)+" t")
      +cell("DELIVERY",del)
      +'</div>'+pod+'</div></div>';
  }).join("");
  el.querySelectorAll(".jrow").forEach(r=>r.addEventListener("click",e=>{
    if(e.target.closest(".cmt")||e.target.closest(".cmtsave"))return;  // don't collapse while editing
    r.classList.toggle("open");}));
  el.querySelectorAll(".cmtsave").forEach(b=>b.addEventListener("click",e=>{
    e.stopPropagation();const id=+b.dataset.id;
    const ta=el.querySelector('.cmt[data-id="'+id+'"]');
    b.textContent="SAVED";jobsCache="";
    post("/job/comment",{id:id,comment:ta.value}).then(()=>setTimeout(()=>b.textContent="SAVE COMMENT",1200));
  }));
}
setInterval(loadJobs,8000);loadJobs();

</script>
</body>
</html>"""


@app.route("/")
def index():
    out = (PAGE.replace("__AUTOTAB__", "true" if AUTO_TAB_SWITCH else "false")
               .replace("__AUTOMOVEMS__", str(int(AUTO_TAB_MOVE_SEC * 1000)))
               .replace("__AUTOSTOPMS__", str(int(AUTO_TAB_STOP_SEC * 1000)))
               .replace("__AUTOHOLDMS__", str(int(AUTO_TAB_HOLD_SEC * 1000))))
    return Response(out, mimetype="text/html")


# ----------------------------------------------------------------------
def lan_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


def _print_banner():
    """Print startup info. Safe even when there's no console (windowed exe)."""
    lines = [
        "=" * 58,
        "  RIGDECK  ·  CAB PANEL  v3.0",
        "=" * 58,
        f"  Phone URL :  http://{lan_ip()}:8600",
        f"  Debug     :  http://{lan_ip()}:8600/debug",
        "  Input     : " + ("OK" if INPUT_OK else "UNAVAILABLE"),
        "  Telemetry : " + ("lib loaded" if TELE_LIB else "UNAVAILABLE"),
        "  Discovery :  UDP 8721 (Android app auto-find)",
        f"  Start key :  {ENGINE_KEY.upper()}",
        f"  Park brake:  {PARK_KEY.upper()}",
        f"  Hazards   :  {HAZ_KEY.upper()}",
        "  Game must be focused for switches.",
        "=" * 58,
    ]
    try:
        for ln in lines:
            print(ln)
    except Exception:
        pass  # no console attached (built with --noconsole); ignore


def _status_window():
    """
    When built as a windowed exe there's no console, so show a tiny always-on
    status window with the phone URL and a Stop button. Uses tkinter (bundled
    with Python). If tkinter isn't available, the server still runs headless.
    """
    try:
        import tkinter as tk
    except Exception:
        return False

    url = f"http://{lan_ip()}:8600"
    root = tk.Tk()
    root.title("RigDeck")
    root.configure(bg="#14171B")
    root.geometry("360x200")
    root.resizable(False, False)
    try:
        root.attributes("-topmost", True)
    except Exception:
        pass

    def lbl(text, fg, size, weight="normal", pady=(0, 0)):
        w = tk.Label(root, text=text, bg="#14171B", fg=fg,
                     font=("Consolas", size, weight))
        w.pack(pady=pady)
        return w

    lbl("RIGDECK", "#FF6A2B", 15, "bold", (16, 0))
    lbl("CAB PANEL RUNNING", "#8A917A", 9, "normal", (0, 10))
    lbl("On your phone (same Wi-Fi), open:", "#8A917A", 9, "normal", (0, 2))
    lbl(url, "#e9edde", 13, "bold", (0, 2))
    lbl("or just open the RigDeck app", "#8A917A", 8, "normal", (0, 12))

    tk.Button(root, text="STOP BRIDGE", command=lambda: os._exit(0),
              bg="#2a2e21", fg="#FF5340", relief="flat",
              font=("Consolas", 10, "bold"), padx=12, pady=4).pack()

    # --- update row: always present, contents swap as state changes ---
    tk.Frame(root, bg="#2a2e21", height=1).pack(fill="x", padx=24, pady=(14, 0))
    upd_frame = tk.Frame(root, bg="#14171B")
    upd_frame.pack(pady=(10, 0), fill="x")
    upd_lbl = tk.Label(upd_frame, text="Checking for updates\u2026",
                       bg="#14171B", fg="#8A917A", font=("Consolas", 9))
    upd_lbl.pack(pady=(0, 4))
    upd_status = tk.Label(upd_frame, text="", bg="#14171B", fg="#8A917A",
                          font=("Consolas", 8))

    def do_update():
        # Open the download page in the browser. Manual replace is far more
        # reliable than an in-place exe swap (PyInstaller + antivirus make
        # self-replacing exes flaky on Windows).
        import webbrowser
        with _update_lock:
            page = _update.get("url") or RELEASES_URL
        try:
            webbrowser.open(page)
            upd_status.config(
                text="Opened the download page in your browser.\n"
                     "Download the new RigDeck, then close this and run it.",
                fg="#8A917A", justify="center")
        except Exception:
            upd_status.config(text=f"Download it here:\n{page}",
                              fg="#8A917A", justify="center")
        upd_status.pack(pady=(4, 0))

    upd_btn = tk.Button(upd_frame, text="OPEN DOWNLOAD PAGE", command=do_update,
                        bg="#FFB03F", fg="#0b0d10", relief="flat",
                        font=("Consolas", 10, "bold"), padx=14, pady=4)

    _shown = {"up": False, "grown": False}

    def render_update():
        with _update_lock:
            checked  = _update.get("checked")
            outdated = _update.get("outdated")
            latest   = _update.get("latest")
            has_dl   = bool(_update.get("download"))
        if outdated and latest:
            upd_lbl.config(text=f"UPDATE AVAILABLE  \u2014  v{latest}", fg="#FFB03F")
            if has_dl:
                if not _shown["up"]:
                    upd_btn.pack(); _shown["up"] = True
            else:
                upd_status.config(text="Open the releases page to download.", fg="#8A917A")
                upd_status.pack(pady=(4, 0))
            if not _shown["grown"]:
                root.geometry("360x300"); _shown["grown"] = True
        elif checked:
            upd_lbl.config(text="RigDeck is up to date.", fg="#8A917A")
        # else: still "Checking for updates…"
        root.after(3000, render_update)

    # kick an immediate check so we don't wait on the background loop, then render
    threading.Thread(target=_fetch_update_once, daemon=True).start()
    root.after(800, render_update)
    root.protocol("WM_DELETE_WINDOW", lambda: os._exit(0))
    root.mainloop()
    return True


if __name__ == "__main__":
    import os
    _print_banner()
    # Run Flask in a background thread so the status window (if any) owns the
    # main thread. Headless console users see the banner and Ctrl+C as before.
    server = threading.Thread(
        target=lambda: app.run(host="0.0.0.0", port=8600, threaded=True),
        daemon=True)
    server.start()
    # Try to show the GUI status window; if there's no display/tkinter,
    # fall back to just keeping the process alive.
    if not _status_window():
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            pass
