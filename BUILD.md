# Building RigDeck

## The panel (Windows exe)

1. Install **Python 3** from python.org — tick **"Add python.exe to PATH"** on the first screen.
2. Double-click **`BUILD_EXE.bat`**.
3. When it says DONE, your app is at **`dist\RigDeck.exe`**.

That's it. The batch file installs everything it needs and builds a single self-contained exe.

### Running from source instead
```
pip install flask truck-telemetry pydirectinput
python rigdeck.py
```

## Cutting a release (for the maintainer)

RigDeck's auto-update check reads **`version.json`** from the repo's `main` branch. To publish
an update:

1. Bump `APP_VERSION` near the top of `rigdeck.py`.
2. Build the new `RigDeck.exe`.
3. Create a GitHub **Release** and attach the exe.
4. Edit **`version.json`** so `version` matches, and update the notes:
   ```json
   {
     "version": "3.6",
     "url": "https://github.com/HexLab2026/RIGDECK/releases/latest",
     "download": "https://github.com/HexLab2026/RIGDECK/releases/latest/download/RigDeck.exe",
     "notes": "What changed in this build"
   }
   ```
5. Commit `version.json` to `main`.

**Important:** the `download` field must point straight at the `RigDeck.exe` asset on your
release. The `/latest/download/RigDeck.exe` form always resolves to the newest release, so you
usually don't need to change it — just attach the exe to each release with that exact filename.

Every running copy of RigDeck notices within a few hours (or on next launch). On the PC it offers
a one-click **Update Now** that downloads and swaps the exe; on phones it shows a notice pointing
to the PC. If you ever omit the `download` field, RigDeck falls back to just showing the notice
with a link to the releases page (no auto-swap).

### How the self-update works (so you can trust it)
When you click Update Now, RigDeck downloads the new exe to a temp file, checks it's a real
non-empty Windows executable, backs up the current exe, then launches a tiny helper that waits
for RigDeck to close, swaps the files and relaunches. If the download fails or looks wrong, it
cancels and leaves your working copy untouched.

## The Android app
Open the `android/` project in Android Studio and Build → Generate Signed APK, or attach the
APK to the same GitHub release.
