// Additions to the stretched original stand (MegaAndy "Guition 4 inch Screen Frame and Stand" v2,
// no-side-cable-hole version), stretched to fit the Raspberry Pi Touch Display 2 (7") in landscape.
// Coordinates: "use" orientation — desk at z = 0, screen at the front (-y), x = width.
include <M.scad>
part = "stand";            // "stand" (print as-is, base on the bed) | "frame" | "assembly"
$fn = 40;

// ---------- Display ----------
edge_t   = 6.45;  // official drawing: 6.45 ±0.5 at the glass edge (what the frame clamps)
cavity   = 12.0;  // original frame cavity (Guition module thickness) — do not change
glass_max = edge_t + 0.5;   // drawing tolerance ±0.5
foam_min  = 0.5;            // 2 mm foam tape on the ring, compressed to no less than 0.5 mm
spacer   = cavity - glass_max - foam_min;   // = 4.55: foam takes up 5.95-6.95 mm glass

// ---------- Pi 5 on the back wall ----------
pi_x0     = -11.2;  // Pi left edge (x); puts the Pi's USB-C right above the rear cable hole
pi_s0     = 15;     // Pi bottom edge, measured up the back wall from the floor
standoff  = 5;      // standoff height off the wall
screw_d   = 1.4;    // M2 pilot, printed undersize: drill 1/16" on site (one screw size throughout: M2 x 5 pan head)
boss_d    = 6.5;
tail      = 12;     // printable tail length

// ---------- Weight pocket (loads from inside, before the display goes on) ----------
weight  = true;
wp_w    = 96;      // pocket length — fits a 3.75" (95 mm) piece of 1" x 1/2" steel flat bar (~240 g)
wp_x    = 40;      // pocket centre x (Pi side; the speaker box sits on the floor on the other side)
wp_h    = 13.3;    // pocket height (1/2" bar = 12.7)
wb_top  = 22.4;    // box top (pocket roof + 2 mm)
wb_ft   = 10.0;    // front-top edge, clear of the display's back
wb_back = 44.6;    // box back (pocket opens here)
lean    = 0.404;   // tan(22°): front face prints face-down at a gentler angle than the original back wall

// ---------- 3" speaker (Adafruit 4 ohm 3 W: 77.8 x 77.8 x 25.5, 4 tabs 60 mm apart) ----------
spk_x  = -52.15;   // centre x (left half as you face the screen = right half seen from behind)
spk_s  = 42;       // centre, up the back wall
spk_sq = 77.8;
spk_tab = 60;      // [CHECK] tab hole pattern (assumed 60 x 60 square)
spk_pad = 3;       // pads the frame screws into; seal the gap with 3 mm foam ring
spk_seat = 1.5;    // screw head seat, measured from the inner wall face into the pad (leaves 1.5 mm under the head)
spk_screw_d = 1.4; // M2 pilot in the speaker box, drill 1/16" on site
grille_d = 66;     // grille opening over the cone

// ---------- ReSpeaker Lite v1.1 (from Seeed's STEP model) ----------
// Board 82.02 x 34.01 x 1.51. Mics (top-port), 2 buttons and an LED are on the UNDERSIDE -> underside faces the wall.
// USB-C, 3.5 mm jack and speaker JST-PH are all at one end -> that end faces the right side wall (seen from the front).
rs_x0  = -5;       // board left edge (x)
rs_s0  = 75;       // board bottom edge, up the back wall
rs_w   = 82.02; rs_h = 34.01; rs_t = 1.51;
rs_gap = 3.0;      // board off the wall (buttons stand 2.6 mm proud); mics seal to the wall with 2 mm foam
mic_x  = [5.49, 76.49];   // mic centres, from the board's left edge (71.0 mm apart)
mic_v  = 17.0;            // mic centres, from the board's bottom edge
mic_hole = 1.5;

// ---------- Vents (optional) ----------
vents = true;
vent_d = 3;        // exhaust hole diameter

// ---------- Geometry of the stretched stand (measured) ----------
wall_in_y0 = 76.0;  floor_top = 7.1;           // back-wall inner at floor-top level
uw = [0, -0.3407, 0.9402];                     // up the back wall
nw = [0, -0.9402, -0.3407];                    // off the back wall, into the stand
inner_x = 93.1;                                // inner side-wall half width

function wallpt(x, s, d) = [x, wall_in_y0, floor_top] + s*uw + d*nw;

module on_wall(x, s) {   // local frame: X = width, Y = up the wall, Z = out of the wall
    multmatrix([[1,0,0, x],[0,uw[1],nw[1], wall_in_y0 + s*uw[1]],[0,uw[2],nw[2], floor_top + s*uw[2]],[0,0,0,1]]) children();
}

module pi_bosses() {   // tails run up the wall (toward the apex) so they print face-down
    for (hx = [3.5, 61.5], hy = [3.5, 52.5]) {
        t = hy < 10 ? tail : max(1.5, rs_s0 - 0.5 - (pi_s0 + hy) - boss_d/2);   // top pair kept short to clear the ReSpeaker
        on_wall(pi_x0 + hx, pi_s0 + hy) difference() {
            hull() {
                translate([0,0,-1]) cylinder(d = boss_d, h = standoff + 1);
                translate([-boss_d/2, boss_d/2 + t, -1]) cube([boss_d, 0.01, 1]);
            }
            translate([0,0,-0.5]) cylinder(d = screw_d, h = standoff + 1);
        }
    }
}

// stretched insert (original rim) dimensions, original STL coords
sdx = 102.72; sdy = 33.64;
ins_ox = 43.42 + sdx/2;  ins_ix = 41.6 + sdx/2;
ins_oy0 = 18.09; ins_iy0 = 21.14; ins_oy1 = 104.93 + sdy; ins_iy1 = 103.04 + sdy;
module spacer_ring() {   // in original STL coords, moved into use coords. Chamfers keep it printable.
    zf = -5.47 - spacer;  zb = -5.17;  ch = 0.532;   // tan(28°)
    multmatrix(M_USE) difference() {
        union() {
            translate([0, 0, zf]) linear_extrude(zb - zf) difference() {
                translate([-ins_ox, ins_oy0]) offset(2) offset(-2) square([2*ins_ox, ins_oy1 - ins_oy0]);
                translate([-ins_ix, ins_iy0]) square([2*ins_ix, (ins_iy1 - 4.11) - ins_iy0]);   // bottom band thickened inward
            }
            translate([-ins_ix, 0, 0]) rotate([90, 0, 90]) linear_extrude(2*ins_ix)
                polygon([[ins_iy0 - 0.01, zf], [ins_iy0 - 0.01, zb], [ins_iy0 + (zb - zf)*ch, zb]]);
        }
        translate([-ins_ox - 2, 0, 0]) rotate([90, 0, 90]) linear_extrude(2*ins_ox + 4)
            polygon([[ins_oy1 - (-5.47 - zf)*ch, zf - 0.01], [ins_oy1 + 3, zf - 0.01], [ins_oy1 + 3, -5.47], [ins_oy1 + 0.01, -5.47]]);
    }
}

// Weight: open tray on the floor, steel bar glued in. (A covered pocket can't be printed face-down:
// its front-top edge would be the lowest point of the box and start in mid-air.)
bar_l = 95.25; bar_w = 25.4; bar_h = 12.7;          // 3.75" x 1" x 1/2" steel flat bar (~240 g)
tray_h = 4; tray_t = 2; tray_c = 0.4;               // lip height, lip thickness, clearance round the bar
tray_ramp = 33;                                     // front lip ramp (deg from the floor); <= 36 prints face-down
bar_y1 = wb_back; bar_y0 = bar_y1 - bar_w;          // bar sits where the old pocket held it
module weight_box() {   // name kept for the build script
    x0 = wp_x - bar_l/2 - tray_c; x1 = wp_x + bar_l/2 + tray_c; yi = bar_y0 - tray_c; z0 = floor_top - 0.5; z1 = floor_top + tray_h;
    // front lip with printable ramp
    translate([x0 - tray_t, 0, 0]) rotate([90, 0, 90]) linear_extrude(x1 - x0 + 2*tray_t)
        polygon([[yi - tray_t - (z1 - z0)/tan(tray_ramp), z0], [yi, z0], [yi, z1], [yi - tray_t, z1]]);
    // end lips (their front ends join the front lip)
    for (xa = [x0 - tray_t, x1]) translate([xa, yi - tray_t, z0]) cube([tray_t, bar_y1 - (yi - tray_t), z1 - z0]);
}
module weight_bar() { translate([wp_x - bar_l/2, bar_y0, floor_top + 0.05]) cube([bar_l, bar_w, bar_h]); }
if (part == "bar") weight_bar();
module vent_cuts() {
    // intake: slots through the base, under the Pi side only (the speaker box covers the other side)
    for (i = [1:6]) translate([i*12 - 1.5, 48, -1]) cube([3, 18, 12]);
    // exhaust: two staggered rows of round holes high on the back wall, beside the ReSpeaker
    for (row = [0, 1]) for (k = [0:12]) {
        x = -81 + k*6.3 + row*3.15;
        if (x <= -12) on_wall(x, 93 + row*5.5) translate([0,0,-4]) cylinder(d = vent_d, h = 8, $fn = 24);
    }
}
module vent_solids() { vent_cuts(); }
module display_relief() { multmatrix(M_USE) translate([-90, 126, -5.4]) cube([180, 136.44 - 126 - 0.01, 4.6]); }
module pi_envelope() { on_wall(pi_x0, pi_s0) translate([0, 0, standoff]) cube([85, 56, 1.6 + 16]); }

// ---- speaker: 4 screw pads (printable tails toward the apex) + grille
module spk_pads() {   // pads the speaker frame sits on (screws come in from the back face)
    for (i = [-1, 1], j = [-1, 1])
        on_wall(spk_x + i*spk_tab/2, spk_s + j*spk_tab/2) hull() {
            translate([0,0,-1]) cylinder(d = 7, h = spk_pad + 1);
            translate([-3.5, 3.5 + 8, -1]) cube([7, 0.01, 1]);
        }
}
module spk_screw_holes()   {   // M2 x 5 pan head from outside: counterbore to a seat 1.5 mm into the pad, clearance through the rest
    for (i = [-1, 1], j = [-1, 1])
        on_wall(spk_x + i*spk_tab/2, spk_s + j*spk_tab/2) {
            translate([0,0,-2.4]) cylinder(d = 4.4, h = 2.4 + spk_seat, $fn = 40);      // head recess (M2 pan head is ~3.8 mm)
            translate([0,0,-1]) cylinder(d = 2.4, h = spk_pad + 2, $fn = 24);           // clearance
        }
}
module spk_grille() {   // round holes (hex grid) over the cone: same look as the exhaust vents; slots made long thin bars that print poorly face-down
    p = 4.2; d = 3.0;    // pitch, hole size: about 46 % open
    on_wall(spk_x, spk_s) for (j = [-9:9], i = [-9:9]) let(x = (i + (j % 2 == 0 ? 0 : 0.5))*p, y = j*p*0.866)
        if (sqrt(x*x + y*y) <= grille_d/2 - d/2) translate([x, y, -3]) cylinder(d = d, h = 8, $fn = 20);
}
module spk_envelope() { // frame + magnet, for clearance checks
    on_wall(spk_x, spk_s) union() {
        // from Adafruit's 3" speaker CAD: 77.8 sq flange 1 mm, front gasket ring Ø74 x 0.5, basket, Ø32 magnet, 25.8 deep
        translate([-spk_sq/2, -spk_sq/2, spk_pad]) cube([spk_sq, spk_sq, 1]);
        translate([0,0,spk_pad - 0.5]) cylinder(d = 74, h = 0.5);
        translate([0,0,spk_pad + 1]) cylinder(d1 = 76, d2 = 52, h = 8);
        translate([0,0,spk_pad + 9]) cylinder(d1 = 52, d2 = 34, h = 5);
        translate([0,0,spk_pad]) cylinder(d = 32.5, h = 25.5);
    }
}
// ---- ReSpeaker: card-guide rails at the board ends, run up to the apex so they print face-down
// Board's two M2 mounting holes (Seeed STEP): straight push-on mount, foam gaskets compress evenly
rs_holes = [[2.46, 31.56], [60.16, 2.66]];   // from the board's left / bottom edges
module rs_rails() {   // (name kept for the build script) -> two standoffs with printable tails toward the apex
    for (h = rs_holes) on_wall(rs_x0 + h[0], rs_s0 + h[1]) difference() {
        hull() {
            translate([0,0,-1]) cylinder(d = 5, h = rs_gap + 1, $fn = 32);
            translate([-2.5, 2.5 + 6, -1]) cube([5, 0.01, 1]);
        }
        translate([0,0,-0.5]) cylinder(d = screw_d, h = rs_gap + 1, $fn = 16);   // M2 pilot, drill 1/16" on site
    }
}
module rs_envelope() { // board + top-side parts (4 mm general, JST-PH 6.8 mm) + right-angle USB-C plug, for clearance checks
    on_wall(rs_x0, rs_s0) translate([0, 0, rs_gap]) {
        cube([rs_w, rs_h, rs_t + 2.6]);
        translate([73.9, 12.8, 0]) cube([7.1, 8.1, 8.35]);            // speaker JST-PH (vertical) + plug
        translate([82.9, 21, -0.5]) cube([12, 13, 8]);                // right-angle USB-C plug body
    }
}
module mic_holes() {
    for (mx = mic_x) on_wall(rs_x0 + mx, rs_s0 + mic_v) {
        translate([0,0,-4]) cylinder(d = mic_hole, h = 8);
        translate([0,0,-2.3]) cylinder(d1 = 3.2, d2 = mic_hole, h = 0.9);
    }
}

// ---- button poke holes + engraved labels (back face, read from behind)
btn_x = [3.53, 11.22];  btn_v = 5.74;              // K1, K2 centres on the board (Seeed STEP)
btn_label = ["MUTE", "USR"];
mt_w = 9; mt_free = 4.5; mt_hinge = 6; mt_slot = 1.0;   // MUTE tab: width, length below / above the button, slot width                         // [CHECK] swap if the silkscreen says otherwise
module poke_holes() {
    for (i = [1]) on_wall(rs_x0 + btn_x[i], rs_s0 + btn_v) {          // USR: poke hole
        translate([0,0,-4]) cylinder(d = 2.6, h = 8, $fn = 24);
        translate([0,0,-2.4]) cylinder(d1 = 4.4, d2 = 2.6, h = 0.9, $fn = 24);
    }
    // MUTE: flexure button — U-slot through the wall leaves a tab hinged along its top edge
    on_wall(rs_x0 + btn_x[0], rs_s0 + btn_v) translate([0, 0, -4]) difference() {
        translate([-mt_w/2 - mt_slot, -mt_free - mt_slot, 0]) cube([mt_w + 2*mt_slot, mt_free + mt_hinge + mt_slot, 8]);
        translate([-mt_w/2, -mt_free, -1]) cube([mt_w, mt_free + mt_hinge + mt_slot + 1, 10]);
    }
}
module labels() {   // 0.6 mm deep engraving on the outer face; mirrored so it reads from behind
    // MUTE: centred under its tab
    on_wall(rs_x0 + btn_x[0], rs_s0 + btn_v - mt_free - mt_slot - 3.0) translate([0, 0, -1.82 - 0.01]) mirror([1, 0, 0])
        linear_extrude(0.61) text("MUTE", size = 3.2, font = "DejaVu Sans:style=Bold", halign = "center", valign = "center");
    // USR: beside its poke hole
    on_wall(rs_x0 + btn_x[1] + 4.2, rs_s0 + btn_v) translate([0, 0, -1.82 - 0.01]) mirror([1, 0, 0])
        linear_extrude(0.61) text("USR", size = 3.2, font = "DejaVu Sans:style=Bold", halign = "right", valign = "center");
}
module mute_grip() {  // three low ridges on the outside of the MUTE tab
    for (k = [-1, 0, 1]) on_wall(rs_x0 + btn_x[0], rs_s0 + btn_v + 0.75 + k*2.6)
        translate([-(mt_w - 2.4)/2, -0.45, -1.82 - 0.4]) hull() {
            translate([0, 0, 0.4]) cube([mt_w - 2.4, 0.9, 0.35]);
            translate([0, 0.2, 0]) cube([mt_w - 2.4, 0.5, 0.01]);
        }
}

if (part == "poke")   poke_holes();
if (part == "labels") labels();
if (part == "grip")   mute_grip();
// ---- raised pad under the ReSpeaker: thin foam tape (with holes at the mics) seals mic to pinhole
foam_t = 1.0;                                // foam tape thickness
mic_face = rs_gap - 1.28;                    // mic underside, off the wall (mics stand 1.28 proud of the PCB)
pad_h = mic_face - foam_t + 0.2;             // 0.2 mm compression
// underside parts that need relief in the pad (board coords: x0, y0, x1, y1), from the STEP model
rs_relief = [[0.7, 3.6, 6.3, 7.9],    // K1 button
             [8.4, 3.6, 14.0, 7.9],   // K2 button
             [39.3, 13.6, 42.4, 18.5]]; // LED D1 + neighbour
module rs_pad() {   // small raised squares at the two mics (stick a foam square on each, pierce at the pinhole)
    for (mx = mic_x) on_wall(rs_x0 + mx, rs_s0 + mic_v) hull() {
        translate([-4, -4, -1]) cube([8, 8, pad_h + 1]);
        translate([-5, -5, -1]) cube([10, 10, 1]);
    }
    // nub on the inside of the MUTE tab, just above the switch plunger (plunger is 0.41 mm off the wall)
    on_wall(rs_x0 + btn_x[0], rs_s0 + btn_v) translate([0,0,-1]) cylinder(d = 2.4, h = 1 + 0.1, $fn = 32);   // 0.31 mm gap to the plunger: tolerant of print error, no pre-press
}

if (part == "spkpads")  spk_pads();
if (part == "rspad")    rs_pad();
if (part == "spkholes") spk_screw_holes();
if (part == "grille")   spk_grille();
if (part == "spkenv")   spk_envelope();
if (part == "rails")    rs_rails();
if (part == "rsenv")    rs_envelope();
if (part == "mics")     mic_holes();
if (part == "ring")      spacer_ring();
if (part == "bosses")    pi_bosses();
if (part == "wbox")      weight_box();
if (part == "vents")     vent_solids();
if (part == "relief")    display_relief();
if (part == "pi")        pi_envelope();

// ---- engraved hardware note on the inside of the right side wall, above the cover opening (read from the open front).
// On the side wall it prints vertically; on the back wall the letter counters would start in mid-air.
module screw_note() {
    multmatrix([[0,0,-1, 93.1],[-1,0,0, 33],[0,1,0, 84],[0,0,0,1]]) translate([0, 0, -0.5]) linear_extrude(1.5) {
        translate([0,  2.3]) text("M2x5 SCREWS", size = 2.4, font = "DejaVu Sans:style=Bold", halign = "center", valign = "center");
        translate([0, -2.3]) text("DRILL 1/16\"", size = 2.4, font = "DejaVu Sans:style=Bold", halign = "center", valign = "center");
    }
}
if (part == "screwnote") screw_note();
