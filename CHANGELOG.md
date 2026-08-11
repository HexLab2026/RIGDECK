# Changelog

## v3.9

### Added
- **Speed unit toggle.** Tap the pill next to the live speed reading (STATUS
  page) to flip between KM/H and MPH. This is a real toggle in the sense that
  it *only* touches speed readings — the live dial, and TOP SPEED / AVG SPEED
  in job history, since those are the same kind of figure. Nothing else on the
  panel moves when you tap it.
- **Game-aware region defaults.** ETS2 and ATS share the same telemetry plugin
  and the same raw metric data — there's no separate "ATS conversion" at the
  data level, just a different sensible starting point per game. Connect to
  **ATS** and the panel shows American: miles, US gallons, MPG, 12-hour clock.
  Connect to **ETS2** and it shows European: km, litres, L/100km, 24-hour
  clock. This is locked to whichever game is actually connected — there's no
  button for it, it just follows the game, same as route distance, fuel
  level, AdBlue, average consumption and the delivery-deadline clock (DUE).
- Fuel economy conversion (L/100km ↔ MPG) uses the correct **inverse**
  relationship rather than a linear scale, since the two units measure
  opposite things — volume-per-distance vs distance-per-volume. A straight
  multiply would have quietly produced a wrong number that still looked
  plausible.

### Why speed is separate from everything else
Speed is something a driver has a personal feel for, independent of which
game or region they're actually in — a UK driver's own mph habit while
playing an American-set game is the obvious case. Distance, fuel and clock
format aren't a matter of taste the same way; they're what that game's
economy and dashboard actually run on. So the speed reading is a free toggle,
and everything else just tells the truth about the game you're connected to.

---

## v3.8

### Added
- **DIFF LOCK** control on the CONTROLS page, on its own plate below LIFT / DROP.
  Bind `.` (full stop) in-game.
- **Auto tab switching.** Driving brings up STATUS, stopping brings CONTROLS back
  so the handbrake is under your thumb, and a completed delivery jumps to ACTIVE
  JOB with COMPLETE ready. Tapping any tab yourself suspends it until the next
  drop, so it never pulls a page away while you're reading it. Tunable at the top
  of the script via `AUTO_TAB_SWITCH`, `AUTO_TAB_MOVE_SEC`, `AUTO_TAB_STOP_SEC`.
- Tap-style bar buttons (wipers, cab/trailer axle, suspension reset, diff lock)
  now visibly depress when pressed, matching the square tiles.

### Fixed
- **Taps could be missed by the game entirely.** The panel used
  `pydirectinput.press()`, which sends keyDown and keyUp back to back with no
  gap — the key was down for well under a millisecond, shorter than a single
  frame at 60fps, so the game could poll straight past it. A real keypress lasts
  around 100ms. Taps now hold for `TAP_HOLD_SEC` (80ms). DIFF LOCK never worked
  at all because of this; every other tap button was quietly intermittent
  depending on frame timing.
- **ACTIVE JOB always showed LOADED with an owned trailer.** Cargo state was
  inferred from whether a trailer was coupled. That only works for market
  trailers, where you couple up at the collection — an owned trailer stays
  hitched permanently, so it read LOADED while running empty. It now uses real
  cargo data (`isCargoLoaded`, falling back to cargo mass) and shows
  **NO TRAILER** / **EMPTY** / **LOADED**.
- **Fuel range warning light flicked on and off.** Whenever the consumption model
  briefly lost its sample window — a gap in polling while the phone screen slept,
  a ferry, a refuel — the displayed range silently fell back to the game's own
  estimate, a substantially different figure, then jumped back when the model
  recovered. If the route distance sat between the two numbers, the warning
  tripped on and off with it. The learned burn rate is now held across short
  dropouts and range recalculated from current fuel, only falling back to the
  game's figure after 15 minutes without a model.
- **DIFF LOCK and HAZARD lights wouldn't stay on.** Both read telemetry fields
  (`differentialLock`, `lightsHazards`) that this telemetry plugin doesn't
  report, so the light was cleared on the next poll. Both now use telemetry when
  it's available and otherwise track their own state.

- **Auto tab switching stopped for the rest of the session** if you changed tab
  once. The pause was only lifted on the `pending` edge, and `pending` only
  clears when the JOB COMPLETED button is pressed — skip that press and the edge
  never fired again. Delivery and collection are now detected from cargo entering
  and leaving the trailer in telemetry, so the cycle resumes on every run, and a
  and the cycle was reworked around what the truck is doing: coming to a full stop
  brings CONTROLS up immediately so the handbrake is under your thumb, pulling away
  returns to STATUS, and both are edge-triggered so shunting round a yard doesn't
  make the page chatter. Tapping a tab yourself suspends only the flip to STATUS —
  that lifts after `AUTO_TAB_RESUME_SEC` of unbroken movement if you tapped while
  driving, or when the engine is restarted if you tapped with it off (covers fuel
  stops, ferries and rest stops). A collection or delivery lifts it either way.
  All timings configurable: `AUTO_TAB_STOP_SEC`, `AUTO_TAB_MOVE_SEC`,
  `AUTO_TAB_RESUME_SEC`.

### Known limitations
- Because the plugin doesn't report hazard or diff-lock state, quitting with
  either engaged shows it OFF on restart — one tap resyncs. If a future plugin
  reports those fields, the buttons pick up the real state automatically with no
  code change.

---

## v3.7
- **WIPERS** control added as a full-width bar (bind `V`).
- Fuel range warning given a hysteresis dead-band so it stops chattering when
  remaining range sits close to the route distance.
- Tab bar given larger tap targets.
- Carrier name removed from the proof-of-delivery sheet.
- Fixed PARK BRAKE tile rendering a different height to its neighbours when its
  label wrapped to two lines.

## v3.6
- **CAB AXLE** lift button added above TRAILER AXLE (bind `,`).
- HAZARD button changed to a plain latch, after `/debug` confirmed this plugin
  never reports hazard state.
- Self-updating exe dropped in favour of an update notice plus a browser link to
  the release — the download-and-swap approach proved unreliable against
  antivirus interfering with PyInstaller's temp extraction.

## v3.5
- Window controls moved off the numpad onto the punctuation cluster
  (`[` `]` `;` `'`) to stop them clashing with ReShade and weather mods.
- GitHub update checking added: the phone shows a passive notice pointing at the
  PC, the PC window shows the actionable one.

## v3.4
- **HAZARD LIGHTS** button added to the IGNITION plate.

## v3.3
- Fuel consumption model samples once a minute instead of every poll.

## v3.2
- **PARKING BRAKE** button added to the IGNITION plate.

## v3.1
- Seatbelt interlock and pre-drive walkaround checklist removed. Engine START
  moved to the CONTROLS page.

## v3.0
- Renamed to **RIGDECK** — new mark, palette and type.
