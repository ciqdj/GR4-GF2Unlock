<p align="center">
  <img src="assets/icon-256.png" width="112" height="112" alt="GR4-GF2Unlock icon: a GF-2 flash whose beam falls off in six one-stop bands">
</p>

<h1 align="center">GR4-GF2Unlock</h1>

<p align="center">
  <strong>The GR III's GF-2 Flash Mode, on your RICOH GR IV.<br>Focus on your subject; the camera sets the flash exposure.</strong>
</p>

<p align="center">
  <strong>English</strong> |
  <a href="README.ja.md">日本語</a> |
  <a href="README.zh-CN.md">简体中文</a> |
  <a href="README.zh-TW.md">繁體中文</a> |
  <a href="README.ko.md">한국어</a> |
  <a href="README.de.md">Deutsch</a> |
  <a href="README.fr.md">Français</a> |
  <a href="README.es.md">Español</a>
</p>

In firmware 2.10, RICOH gave the GR III **GF-2 Flash Mode**: with the small RICOH
GF-2 flash attached, the camera fires the flash at a fixed power and works out
aperture, ISO and shutter speed from the **focus distance**. The GR IV never got
this mode.

GR4-GF2Unlock adds it to the GR IV as a **fifth Flash Mode option**, next to
Flash On, Flash On+Red-eye, Slow-speed Sync and Slow Sync+Red-eye. Everything
else on your camera stays exactly as it was, and you can go back to the official
firmware at any time.

This repository contains no RICOH firmware. You download the official firmware
from RICOH yourself, and the included tool turns it into the GF-2 Flash Mode
version, on your own computer.

> [!WARNING]
> **Unofficial, at your own risk.** Not made or endorsed by RICOH IMAGING.
> Installing modified firmware may void your warranty. Please read
> [Before you start](#before-you-start) and [Risks](#risks) first.

| You want to | Go to |
| --- | --- |
| See what the camera sets at each distance | [What to expect](#what-to-expect) |
| Make the firmware (macOS, Windows, Linux) | [Make the firmware](#make-the-firmware) |
| Use a flash other than the GF-2 | [Your own flash](#your-own-flash) |
| Install it | [Put it on the camera](#put-it-on-the-camera) |
| Find out what a firmware file contains | [Check a firmware file](#check-a-firmware-file) |
| Go back to RICOH's firmware | [Going back to the official firmware](#going-back-to-the-official-firmware) |

**Contents:**
[How it works](#how-it-works) |
[What you get](#what-you-get) |
[Before you start](#before-you-start) |
[Make the firmware](#make-the-firmware) |
[Put it on the camera](#put-it-on-the-camera) |
[Good to know](#good-to-know) |
[Risks](#risks) |
[Testing status](#testing-status) |
[For developers](#for-developers)

## How it works

With GF-2 Flash Mode selected, the camera fires the flash like Flash On, but at
a **fixed power**. It then plans the exposure the way the GR III's GF-2 Flash
Mode does: from the flash's **guide number** and the **focus distance**
(autofocus or manual focus), within the GR IV's own aperture, ISO and
flash-sync limits. The guide number is the GF-2's, 3, unless you give your own
flash's when you make the firmware (see [Your own flash](#your-own-flash)).

- **The power:** the camera sets the GF-2 with **Flash Output**: **Auto or
  1/1** is full power, **1/4** is quarter power. Another flash fires at the
  power set on the flash itself (see [Your own flash](#your-own-flash)).
- **With ISO Auto,** the camera opens the aperture and raises the ISO as the
  subject gets farther away. Close up, it stays at the lowest ISO and closes
  the aperture as far as the distance needs, down to f/16.
- **With a fixed ISO,** the camera picks the aperture that suits the distance.
- **The shutter speed** follows the light around the subject. It stays within
  flash sync, so the flash is always in the picture. The slowest is 1/32 s, or
  up to 32 s with slow sync in a dark place.
- **In Tv, Av and M,** the values you dial in are overridden, as on the GR III.

The exposure maths is RICOH's own, carried over from the GR III's firmware 2.10.
Everything else is the official GR IV firmware, unchanged.

### What to expect

Typical values in a dim room, Flash Output Auto or 1/1, ND filter off (EXIF may
round them slightly):

| Distance | ISO Auto | Fixed ISO 400 |
| ---: | --- | --- |
| 0.5 m | f/5.9, ISO 100 | f/11.8 |
| 1 m | f/3.0, ISO 100 | f/5.9 |
| 2 m | f/2.8, ISO 367 | f/3.0 |
| 3 m | f/2.8, ISO 800 | f/2.8 |
| 5 m | f/2.8, ISO 2263 | f/2.8 (subject darker: out of flash range) |

With Flash Output **1/4**, the ISO is about two stops higher, or the aperture
about two stops wider. With another guide number, the aperture scales with it:
f-number = guide number × √(ISO / 100) ÷ distance, within f/2.8–f/16.

> [!TIP]
> **Check that the mode is active.** Select GF-2 Flash Mode, set mode **M**,
> **ISO 400** and a shutter speed of 1/2000 s or slower. Take a picture of
> something about 1 m away, then of something about 3 m away. The aperture
> changes by itself, to about f/5.9 and f/2.8, whatever you dialled in.

## What you get

After installing, **Flash Mode** (in the menu, on the ADJ lever and on the Fn
button) offers:

| Shown as | What the flash does |
| --- | --- |
| Flash On | fires every shot, as before |
| Flash On+Red-eye | as before |
| Slow-speed Sync | as before |
| Slow Sync+Red-eye | as before |
| **GF-2 Flash Mode** | **fixed power; aperture, ISO and shutter speed from the focus distance** |

- The new entry has its own name in every menu language, such as "GF-2 Flash
  Mode" in English. When slow sync is not available, the choices are Flash On,
  Flash On+Red-eye and GF-2 Flash Mode.
- It works in **P, Tv, Av or M** with the GF-2 and with **any flash that does
  not communicate with the camera**, such as a manual flash, as on the GR III.
  The exposure is worked out for the guide number in the firmware: the GF-2's,
  or your own flash's (see [Your own flash](#your-own-flash)).
- With a **P-TTL flash** that communicates with the camera, such as a RICOH or
  PENTAX flash, GF-2 Flash Mode works as Flash On, also as on the GR III.
- The setting is kept when the camera is off, like any Flash Mode setting.
- The shooting screen shows the **Flash On** icon, and pictures record the flash
  as fired, like Flash On.
- **Every other Flash Mode works exactly as before**, including Flash Output
  Auto, 1/1 and 1/4.

### Better than the original on the GR III

Around RICOH's exposure maths, the GR IV version uses hardware the GR III does
not have, and fixes a few weak spots:

| | GR III 2.10 | GR4-GF2Unlock |
| --- | --- | --- |
| Flash power | Full power only: the GR III cannot control the GF-2 | With the GF-2, full or quarter power (Flash Output 1/1 or 1/4), with the exposure worked out for each |
| Guide number | Always 3, the GF-2's | 3, or your own flash's (1 to 90) |
| Close subjects with ISO Auto | Up to about 1 EV too bright closer than 0.7 m | The aperture the distance needs, down to f/16 |
| ISO Auto with the ND filter on | The background comes out two stops too dark | The shutter speed allows for the ND filter, so the background is exposed correctly |
| Very close subjects in bright light | Can ask for f/19, beyond the lens's f/16 | Stays within f/2.8–f/16 |
| Flash sync | Can ask for a shutter speed faster than flash sync | Always within flash sync, which on the GR IV depends on the aperture |
| Everything else | Turning the mode on replaces the normal flash behaviour | One Flash Mode choice among five: switch back to Flash On and the GR IV's automatic flash output whenever you like |

More than 250,000 combinations of distance, ISO, ND filter, flash mode, light,
flash type and guide number (1 to 90) have been checked. None calls for an aperture
outside f/2.8–f/16, an ISO outside your limits, or a shutter speed the flash
cannot sync with.

## Before you start

- **Camera:** RICOH GR IV (the standard colour model). Other models are not
  supported.
- **Flash:** RICOH GF-2, or a manual flash whose guide number you know (see
  [Your own flash](#your-own-flash)). The other Flash Modes work with every
  flash as before.
- **Your camera must already be on firmware 1.11.** Check the version in the
  camera's setup menu.
  - Older version: first update to 1.11 the normal way, with RICOH's official file.
  - Newer version: **do not use this tool.** It only supports 1.11.
- **The official firmware file.** From RICOH IMAGING's official GR IV support
  page, download **firmware version 1.11**. Unpack it if needed until you have
  the file **`fwdc248b.bin`**.
- **A fully charged battery.** A firmware update must never lose power.
- **An SD card** you can format.
- **A computer with Python 3.8 or newer.** macOS and most Linux systems already
  have it; on Windows, install it from python.org. Nothing else is needed.
- Note down any custom settings (C1, C2, …) you would not want to set up again.

## Make the firmware

Open a terminal in this folder and run (use the path where you saved the
official file):

```sh
python3 gr4_gf2unlock.py patch ~/Downloads/fwdc248b.bin
```

On Windows:

```bat
py gr4_gf2unlock.py patch C:\Users\you\Downloads\fwdc248b.bin
```

The tool first makes sure you gave it the genuine official 1.11 file. It then
creates the GF-2 Flash Mode firmware and checks it. This takes about a minute.
When everything is right, it ends with:

```
wrote output/fwdc248b.bin  (SHA-256 86abac009d3664ede49ef912073d00b8fb15ac7e9867265aecda581c932db41a)
```

If something is wrong, it prints `refused: …` and writes **nothing**: for
example, a different firmware version, an already modified file, or a damaged
download.

### Your own flash

GF-2 Flash Mode plans the exposure for the GF-2's guide number, 3. To use
another flash, add its guide number with `--gn`:

```sh
python3 gr4_gf2unlock.py patch ~/Downloads/fwdc248b.bin --gn 12
```

- **Which flashes:** any flash that does not communicate with the camera and
  fires from the centre contact of the hot shoe: manual flashes, and most
  flashes made for other camera brands. A P-TTL flash, or a compatible flash in
  P-TTL mode, communicates with the camera; GF-2 Flash Mode then works as
  Flash On, as on the GR III.
- Give the guide number **at ISO 100, in metres**, at full power, from the
  flash's manual. A guide number in feet: divide it by 3.3. A zoom flash: use
  the guide number for the zoom setting you shoot at.
- Allowed: **1 to 90**. The camera works in 1/16-stop steps, and the tool shows
  the value it uses, for example `guide number: 11.81` for 12.
- **The camera cannot set the power of such a flash.** Set the flash to **full
  manual power** and Flash Output to **Auto** or **1/1**. If you set the flash
  to 1/4 power instead, set Flash Output to **1/4** too: the camera then plans
  for two stops less.
- The tool first makes the standard firmware and checks it as above, then
  changes only the guide number. The SHA-256 is then different from the one
  above; `check` shows the guide number of a file.
- To change the guide number, make the firmware again and install it.

## Put it on the camera

### 1. Copy it to the SD card

1. **Format the SD card in the camera.**
2. Copy **`output/fwdc248b.bin`** to the **top level** of the card: not into a
   folder, and keep the name exactly `fwdc248b.bin`.

### 2. Update the camera

1. Insert the fully charged battery and the SD card.
2. Start the firmware update from the camera's setup menu, as described in
   RICOH's official GR IV firmware update instructions.
3. **The camera shows an update from version 1.11 to version 1.11.** This is
   expected: the GF-2 Flash Mode firmware keeps the version number. Confirm the
   update.

> [!CAUTION]
> **Do not turn the camera off, open the battery or card door, or remove the
> card** until the update has finished and the camera has restarted.

### 3. Shoot

1. With the camera and the GF-2 both **off**, slide the GF-2 fully into the hot
   shoe, then switch both on.
2. Shooting menu → **Flash Mode** → **GF-2 Flash Mode**.
3. Set **Flash Output** to **Auto** or **1/1** for full power, or **1/4**.
4. Focus on your subject and shoot.

- The firmware version still shows **1.11**. That is normal.
- Delete `fwdc248b.bin` from the card (or format the card) so the update is not
  started again by accident.

### Going back to the official firmware

> [!IMPORTANT]
> **First set Flash Mode to anything other than GF-2 Flash Mode**, for example
> Flash On. Do the same in every custom mode (C1, C2, …) that uses it. The
> official firmware has no GF-2 Flash Mode setting.

Then repeat steps 1–2 with the **official** `fwdc248b.bin` from RICOH instead.
The camera again shows **1.11 → 1.11**; confirm it, and your camera is back to
stock.

## Good to know

- **Turn the camera and the GF-2 off before attaching or removing the flash**,
  and push the GF-2 fully into the hot shoe.
- **The camera cannot tell whether the flash will fire.** With GF-2 Flash Mode
  selected, it sets the exposure for a flash picture even when the flash is
  off, not attached or still charging. That picture will be too dark. The same
  is true on the GR III.
- **A powerful flash close up:** when the subject is so close that even f/16
  at the lowest ISO lets in too much flash, the picture comes out brighter than
  planned. With ISO Auto and the ND filter set to Auto, the camera adds the ND
  filter once it is about one stop too bright. Otherwise use Flash Output 1/4,
  or step back.
- **Fixed ISO and distant subjects:** once the aperture is fully open (f/2.8),
  a subject farther away gets darker. Raise the ISO, or use ISO Auto.
- **Bright daylight:** the shutter speed cannot go faster than flash sync
  (1/2500 s at f/2.8–f/4). With the ND filter set to Auto, the camera uses the
  ND filter when the light is much brighter than that. The flash then acts as a
  fill light.
- **Continuous shooting:** there is no automatic wait for the flash to recharge,
  unlike the GR III. Leave about two seconds between flash pictures.
- **Snap Distance Priority, B and T, and movies** work as before. GF-2 Flash Mode
  does not apply there.
- **Not combinable with GR4-MonoUnlock or GR4-XPanUnlock.** Each tool starts
  from the official firmware, and this tool refuses their files.
- **Updating from an earlier GR4-GF2Unlock:** install the new file the same way.
  There is no need to go back to the official firmware first. Versions 1.1.0
  and 1.2.0 applied GF-2 Flash Mode only to flashes the camera detects, so it
  had no effect with a manual flash; 1.3.0 fixes this.
- **An official RICOH update removes GF-2 Flash Mode.** It replaces the whole
  firmware. Set another Flash Mode first (see
  [Going back](#going-back-to-the-official-firmware)).
- **Only for the standard GR IV.** Never install the file on another model.
- **Before sending the camera for service,** go back to the official firmware.

### Check a firmware file

Before copying any firmware file to a card:

```sh
python3 gr4_gf2unlock.py check path/to/fwdc248b.bin
```

It tells you whether the file is the official 1.11, the GF-2 Flash Mode version
made by this tool (with its guide number), or something else (it also
recognises GR4-GF2Unlock 1.0.0, 1.1.0 and 1.2.0, GR4-MonoUnlock and
GR4-XPanUnlock files).

## Risks

- Your camera cannot tell a good firmware file from a damaged one. Only copy a
  file the tool has written (or confirmed with `check`) to your card.
- If an update is interrupted, or a firmware file cannot start, the camera may
  not reach the update function again, and it would then need RICOH service.
  This did not happen in testing, but it cannot be ruled out.
- Going back to the official firmware while GF-2 Flash Mode is still selected
  has not been tested. Set another Flash Mode first.
- Your camera's own calibration data is not touched.

## Testing status

| What | Status |
| --- | --- |
| Update accepted, camera starts | tested on a GR IV 1.11 |
| GF-2 Flash Mode in the Flash Mode menu | tested on a GR IV 1.11 |
| Exposure from the focus distance with the GF-2 | tested on a GR IV 1.11 |
| GF-2 Flash Mode with a manual flash (1.3.0) | checked offline; please report your results |
| P-TTL flashes work as Flash On (1.3.0) | checked offline; please report your results |
| Your own guide number (`--gn`) | checked offline; please report your results |
| Close subjects with ISO Auto (exact aperture) | checked offline; please report your results |
| ADJ lever and Fn button cycles | checked offline; please report your results |
| Flash Output 1/4, fixed ISO, ND filter, slow sync | checked offline; please report your results |
| Other Flash Modes unchanged | checked offline; please report your results |
| Going back to the official 1.11 restores the camera completely | tested with earlier modified firmware on a GR IV 1.11; not yet with this version |
| The tool reproduces the reference firmware exactly | tested |

The camera tests were done with version 1.0.0. Since then, the guide number
can be set and close subjects with ISO Auto get the exact aperture (1.2.0), and
GF-2 Flash Mode applies to flashes the camera does not detect, as on the GR III
(1.3.0).

## For developers

```
GR4-GF2Unlock/
├── README.md           this guide
├── README.*.md         this guide in Japanese, Chinese, Korean, German, French and Spanish
├── gr4_gf2unlock.py    the tool (Python 3.8+, no extra packages)
└── assets/             the icon, and the script that draws it (render_icon.py)
```

| File | SHA-256 |
| --- | --- |
| official RICOH GR IV 1.11 `fwdc248b.bin` | `a2f664dfca034059eb0fd6e18ab08684c326b4a034d85c164dad7e1ec9b5655f` |
| GF-2 Flash Mode `fwdc248b.bin` made by this tool (1.3.0, guide number 3) | `86abac009d3664ede49ef912073d00b8fb15ac7e9867265aecda581c932db41a` |
| GF-2 Flash Mode `fwdc248b.bin`, version 1.2.0 | `225258d201217bac3416de79de94aea4d05c6aab74d4f026c30280ac8a624c22` |
| GF-2 Flash Mode `fwdc248b.bin`, version 1.1.0 | `660df9de1e611325fc41df2e42499028c7296c037201b7fd7be828b813ec1c75` |
| GF-2 Flash Mode `fwdc248b.bin`, version 1.0.0 (GF-2 only) | `45a2edd33a0e0783458b1052ad8b67514f48b45a5db7b47013543eb46d247f0c` |
