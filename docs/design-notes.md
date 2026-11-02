# TD2 satellite stand — design notes (decisions and reasons)

So later questions don't reopen settled points. Newest at the bottom of each section.

## Base design
- **Remix, not redesign.** MegaAndy's Guition 4" frame + stand STLs were *stretched* (feature-preserving piecewise translation), not scaled, so every proven feature (snap tabs, grooves, rim, cable hole, fillets) keeps its original size. The first from-scratch attempt "lost the look".
- **Pi 5 mounted on the back wall**, not on the display: no loose parts. Pi USB-C sits right above the original rear cable hole.
- **Landscape 7" Touch Display 2**, glass 189.32 × 120.24, edge 6.45 ±0.5 (official drawing). Spacer ring 4.55 mm + 2 mm foam covers the tolerance.
- **Display cable 300 mm** (the boxed short one is for mounting the Pi on the display).

## Satellite parts
- **ReSpeaker Lite (USB, no XIAO)** on 2 M2 standoffs, mics facing the back wall through 2 pinholes with foam seals. Mounted by its own holes, not a slide-in rail (rails fought the foam).
- **Mic holes on the back wall**, not the top ridge (user's choice).
- **3" speaker in its own sealed box** (~160 cm³ net), screwed from outside the back through the wall into the box. "Simplicity and function first."
- **MUTE = flexure button** printed in the wall (with grip ridges, label under it); USR stays a poke hole.
- **Pi ports access:** plain clip-on cover on the right side; the "◀ PI PORTS" label goes on the back (the side stays clean). Fingernail notch on the cover's **underside**.
- **Wi-Fi only** (AP in the office). No Ethernet notch.

## Hardware
- **One screw for everything: M2 × 5 pan-head self-tapping (10).** The ReSpeaker's 2.16 mm holes force M2; 5 mm is the longest that won't break through the back wall behind the ReSpeaker. Speaker screws sit in Ø4.4 recesses, so 5 mm still gives 2.5 mm of thread in the box.
- **Pilot holes printed Ø1.4, drilled 1/16" on site** (playbook rule: printed holes come out small; drilling gives the same result on any printer). The screw size and drill size are engraved inside the right side wall.

## Printability (face-down stand)
- **Stand prints on its open front face**, like the original. The back wall's inside is a 54° overhang (the original's proven angle).
- **Weight: open tray on the floor, bar glued in.** A covered pocket can't print face-down (its top edge starts in mid-air). Front lip ramped at 33°.
- **Speaker grille = round holes**, not slots: the slots left long thin leaning bars ("thin fragile part" in the slicer).
- **Inside engraving on the side wall, not the back wall:** letter centres would start in mid-air on the back wall's underside.
- **Stretch artifacts fixed:** fold-over triangles on the side walls (re-triangulated), countersink skin (cones start outside the wall).
- **Slice-checked** in PrusaSlicer 2.7: no warnings, no supports. Two 0.8 mm² specks on the upper Pi standoffs' edges are accepted (trim on site if needed).

## Materials and finish
- **Stand, speaker box, cover: matte black ASA** (playbook default; better for the Pi's heat than PETG/PLA).
- **Frame: Spectrum PET-G MATT Olive Green (RAL 6003)**, the user's colour choice. ASA and PETG shrink slightly differently: the frame snap fit is on the on-site fixes list.
- **Fuzzy skin on the frame's outside band only**, painted per triangle in the 3MF (survives Bambu's geometry-only import). **0.05 mm / 0.25 mm** (playbook: 0.12 / 0.3 was too coarse and sparkly). No fuzzy skin on the stand: the back has fit-critical holes and engraving.

## Print handoff
- **Two Bambu 3MFs, one per material**: plate A black ASA (stand + box + cover), plate B olive (frame). All four parts don't fit one 256 mm plate, and plates and per-object filament don't survive a geometry-only import.
- **One plain-language note + one picture with arrows** for Jayed. The files weren't opened in Bambu Studio here (cloud workspace); the note says what the preview must show.

## Before sending
- Buy the electronics first and measure: speaker slots (60 mm square?), ReSpeaker revision and which button is MUTE, glass edge thickness.
