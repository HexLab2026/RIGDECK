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
     "url": "https://github.com/HexLab2026/RIGDECK",
     "download": "https://raw.githubusercontent.com/HexLab2026/RIGDECK/main/RigDeck.exe",
     "notes": "What changed in this build"
   }
   ```
5. Commit **both** the new `RigDeck.exe` AND `version.json` to `main`.

**How this works:** the exe lives in the repo alongside version.json, served over the same raw
URL. When you commit a newer exe and bump `version.json`, every running copy sees the new number
and can download the new exe from that raw path. Keep the filename exactly `RigDeck.exe`.

*(Alternative: if you'd rather not keep the exe in git, use GitHub Releases instead and set
`download` to `https://github.com/HexLab2026/RIGDECK/releases/latest/download/RigDeck.exe` — but
then you must publish a Release with the exe attached each version, or that URL 404s.)*

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


## Testing the updater before you rely on it

With `APP_VERSION` in the script and `version` in `version.json` both the same, RigDeck correctly
shows "up to date" — so you won't see the update UI. To prove the mechanism works, force a
mismatch once:

**Quickest test (no rebuild):**
1. Publish `version.json` to your repo's `main` with a *higher* number than your running build,
   e.g. set `"version": "3.6"` while your exe is still 3.5.
2. Start RigDeck. Within a few seconds the PC window shows **UPDATE AVAILABLE — v3.6** and the
   phone shows its notice.
3. That confirms the check + both banners work. (Update Now will then try to download whatever
   `download` points at — so only click it once you've actually attached a real newer exe.)
4. Set `version.json` back to match once you're done.

**Full test:** cut a real v3.6 release with a rebuilt exe attached, leave your local exe at 3.5,
and click Update Now — it should download, swap and relaunch as 3.6.

## Publishing a release (step by step)

The in-app update button opens your **Releases page**, so there must be a published
release with `RigDeck.exe` attached — otherwise the page looks empty.

1. **Build:** run `BUILD_EXE.bat`. You get a single file: `dist\RigDeck.exe`.
2. On GitHub: your repo -> **Releases** -> **Draft a new release**.
3. **Tag:** type `v3.5`, click "Create new tag: v3.5 on publish".
4. **Title:** `RigDeck v3.5`.
5. **Attach:** drag `RigDeck.exe` into the "Attach binaries" box; wait for the upload.
6. Click **Publish release**.

Now `https://github.com/HexLab2026/RIGDECK/releases/latest` shows the release with
`RigDeck.exe` attached, and the in-app button lands people there.

**Next version:** bump `APP_VERSION` in `rigdeck.py`, rebuild, publish a new release
(tag `v3.6`, attach the new exe), then bump `version` in `version.json` and commit it to
`main` so running copies show the update notice.

## If RigDeck won't start: "Failed to load Python DLL"

This is **antivirus**, not a bug. Windows Defender blocks the exe's bundled Python as it
unpacks. Fix it once:

- Windows Security -> Virus & threat protection -> Manage settings -> **Exclusions**
- Add **Folder**: the folder you keep `RigDeck.exe` in
- Add **Folder**: `C:\Users\<you>\AppData\Local\Temp`

Then run RigDeck again. (This is why the exe may also get flagged when you download it in a
browser - same false positive. Building it yourself and excluding the folder avoids it.)
