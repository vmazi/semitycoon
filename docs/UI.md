# SEMI TYCOON SIMULATOR
### Companion doc: **The World & The Interface** (RCT-style spatial layer)
*Reads alongside DESIGN.md v0.1*

---

## 0. The Core Realisation

**A fab already *is* a theme park.**

| RollerCoaster Tycoon | Semi Tycoon |
|---|---|
| Guests | Wafer lots (FOUPs) moving through the line |
| Rides | Process tools — scanners, etchers, CMP, implant, metrology |
| Queue length | Lot queue in front of a bottleneck tool |
| Ride breakdown + mechanic walking over | Tool down + a tech walking over, $2M/hour |
| Guest thoughts ("I'm not paying that!") | Engineer thoughts ("I've flagged the overlay drift three times") |
| Ride throughput | Wafer starts per month |
| Park rating | Yield / cycle time / on-time delivery |
| Handymen, vandalism, litter | Particle counts, contamination, tool de-tune |

This mapping is almost one-to-one, which is why the genre fits. Lean into it
hard and the game reads instantly to anyone who played RCT.

### The problem this solves

DESIGN.md's whole thesis is **latency** — decisions pay off in 4 years. That's
strategically rich and *moment-to-moment inert*. RCT is the opposite: immediate,
tactile, you place a thing and guests ride it.

**The answer is two clocks in one world:**

- **Operations clock (fast, tactile, RCT-like)** — tools break, lots queue,
  particles spike, a tech is out sick, a bay is running hot. You can intervene
  *today* and see it *today*. This is the dopamine loop.
- **Strategy clock (slow, quarterly, brutal)** — fabs, nodes, tapeouts,
  sockets, geopolitics. Everything from DESIGN.md.

They're not separate screens. **The slow clock is visible as construction in
the fast world.** You watch your $12B fab go up over four years while the
market turns underneath it. A progress bar can't make you feel that. A
half-built shell with idle cranes can.

---

## 1. The Four Scales

Mouse-wheel zoom moves between them continuously — RCT's drill-down instinct,
but spanning four orders of magnitude. **Every mechanic in DESIGN.md is
assigned a home scale.** Nothing floats in an abstract menu.

```
   ╔═══════════════════════════════════════════════════════════════╗
   ║  ▲ WORLD      globe · sites · supply lines · sanctions        ║
   ║  │            → geopolitics, chokepoints, site selection      ║
   ║  │                                                            ║
   ║  │ CAMPUS     isometric site · buildings · construction       ║
   ║  │            → capacity, capex, the Latency Ledger made      ║
   ║  │              physical, people walking between buildings    ║
   ║  │                                                            ║
   ║  │ FLOOR      inside a fab · bays · tools · FOUP queues       ║
   ║  │            → yield, defect mechanisms, utilisation,        ║
   ║  │              bottlenecks, the Ripple Deck's early tells    ║
   ║  │                                                            ║
   ║  ▼ DESK       your office · documents · the Shadow Calendar   ║
   ║               → board, roadmap, forecasts, the Fog Cone       ║
   ╚═══════════════════════════════════════════════════════════════╝
```

### 1.1 WORLD

A slow, cold, political map. Not a strategy-game conquest map — closer to a
logistics board in a war room.

- **Your sites** as pins that bloom into campuses when you zoom.
- **Competitor sites** — you know roughly what they are; a teardown or an
  equipment-order-book purchase sharpens the detail.
- **Supply lines** drawn as actual threads: photoresist from one town in Japan,
  neon from one region, EUV tools from one building in the Netherlands.
  Thread thickness = dependency. Thread colour = risk.
- **Sanction shading** washes over regions as the Geopolitical Pressure track
  drifts. When a region goes red, the *threads through it visibly snap.*
- **Customer pins** with their fab-dependency. A hyperscaler goes from
  "customer" to "competitor" and its pin changes colour — a gut-punch you see
  across the map.
- Site selection for a new fab is a placement decision on this map, scored on
  talent pool / power cost / water / seismic / political risk / subsidy.

### 1.2 CAMPUS — the RCT layer proper

Isometric, buildable, walkable. This is the game's home screen.

**Placeable buildings**, each a clickable entity with its own window:

| Building | What it does | Clicking it gives you |
|---|---|---|
| **Fab shell** | Capacity | Utilisation, yield, depreciation clock, the P&L that won't stop |
| **Design centre** | Chips | Layout tables, tapeout countdowns, the project board |
| **Validation lab** | Not shipping bugs | Coverage %, the testbench queue, *the ripple card you're writing right now* |
| **Packaging & test** | Advanced packaging, chiplets | Bonders, test handlers, the late-game frontier |
| **Failure analysis** | Yield learning | SEM images of actual defects, the mechanism board |
| **Bring-up lab** | First silicon | Where a new chip either boots or doesn't, on camera |
| **Admin tower** | You | The DESK scale lives at the top floor |
| **Loading dock** | The outside world | Mask sets, tool deliveries, customer cars, government cars |
| **Training centre** | Talent pipeline | The thing you cut first and regret for a decade |

**Construction is the Latency Ledger, physically.** A fab goes:

```
  site clearing → pit → foundation → steel → shell → cleanroom buildout
  → utilities → tool move-in → qualification → first production
  ╰─────────────────────── 14–24 quarters ──────────────────────────╯
```

Each stage looks different on screen. You can stand in the campus view in the
middle of a crash and *see* your half-finished $12B shell with the cranes
stopped. Cancelling mid-build leaves a scar on your campus for the rest of the
run — a permanent monument to a forecast you believed. (Yes, it should be
re-startable later, at a penalty. Yes, the Founder board member should mention
it every single board meeting.)

**People walk the campus.** Engineers, techs, visitors. This isn't decoration —
see §3.

### 1.3 FLOOR — inside the fab

Cut away the roof. Cleanroom bays, tool rows, overhead FOUP transport, bunny
suits colour-coded by function (litho = blue, etch = green, metrology = white,
maintenance = amber).

- **Lots queue in front of tools.** A bottleneck is *visible as a pile-up*,
  exactly like a coaster queue. You don't need a report to know your implanter
  is the constraint; you can see the line.
- **Tools are clickable entities** with RCT-style tabbed windows (§2).
- **Don't simulate 1,200 tools.** Simulate 40–80 clickable instances grouped
  into module types. Dense enough to feel real, sparse enough to click.
- **Placement matters** — a genuine spatial puzzle, not decoration:
  - Litho scanners need vibration isolation. Put one near the loading dock and
    overlay error rises. *That becomes a hidden defect mechanism you'll spend
    three quarters of failure analysis to find.*
  - Ultrapure water and gas lines have to reach; long runs cost and leak.
  - Bay reconfiguration to add a tool disrupts production for a quarter.
  - Cleanroom class is per-bay. A dirtier bay is cheaper and shows up in D₀.
- **Yield is spatial.** The yield heatmap overlay shows which *bay* is killing
  you, not just which number. Defect mechanisms have addresses.

### 1.4 DESK — the office

Zoom all the way in to your own office and the game becomes diegetic documents,
exactly as DESIGN.md §13 wants:

- The **Shadow Calendar** is a literal Gantt chart on the wall, with magnets.
- The **roadmap** is a whiteboard — and the public version is a framed printout
  of what you promised at analyst day, hanging next to it. The gap between the
  two boards is the game's central anxiety, rendered as wall decor.
- The **Fog Cone** is a printed forecast with error bars, re-issued quarterly,
  and old copies stack up so you can see how wrong you were.
- The **news ticker** is a screen in the corner.
- Board meetings happen one floor up and you walk there.

---

## 2. Clicking Things — the window system

Straight RCT: **non-modal, draggable, multiple-open, tabbed.** You should be
able to have a tool window, an engineer window, and a customer window open at
once and compare them. No full-screen modal menus, ever.

```
 ┌─ SCANNER 04 · Litho Bay 2 ──────────────────── [_][□][✕] ┐
 │ ⚙ │ 📈 │ 🔧 │ ⚠ │ 👷                                      │
 ├──────────────────────────────────────────────────────────┤
 │                                                          │
 │   [ live iso view of the tool, lots queued, tech idle ]  │
 │                                                          │
 │  Status ....... RUNNING          Uptime 91.2%            │
 │  Utilisation .. 97%  ◀ bottleneck                        │
 │  Queue ........ 14 lots (3.1 days)                       │
 │  Contributes .. Overlay M2–M3 defect mechanism  −11% Y   │
 │  Last PM ...... 41 days ago  (interval: 30)  ⚠           │
 │                                                          │
 │  [Assign tech] [Schedule PM] [Failure analysis] [Idle]   │
 └──────────────────────────────────────────────────────────┘
```

**Tabs per entity type:**

- **Tool** — Status · Utilisation graph · Maintenance log · Defect contribution · Staff
- **Building/Fab** — Overview · P&L (with the depreciation line glowing) · Utilisation history · Tool list · Construction
- **Engineer** — Profile · Skills · Morale & history · **Sole owner of** · Thoughts · Career/vesting
- **Design project** — Spec · Schedule (with tapeout fuse) · Die size & yield projection · Team · IP dependencies
- **Customer** — Sockets held · Forecast history *vs actual* (their personal bias, learned over years) · Relationship · Contract terms
- **Socket** — Ramp curve · Revenue to date · End-of-life date · Re-compete status
- **Supplier** — Dependency · Second-source status · Lead time trend
- **Node/process** — Maturity · Yield curve · Defect mechanism board · Cost per wafer

Double-click any entity to **follow** it with the camera. Follow a lot through
the line, follow an engineer around the campus, follow a mask set from the dock
to the litho bay. RCT's "pick up a guest and watch them" feature, and it's how
players will learn the fab.

---

## 3. Peeps: engineers with thoughts

**The single most important translation from RCT.** Guest thoughts were how RCT
told you the truth about your park without a spreadsheet. Here they're your
early-warning system *and* the thing your management style can destroy.

Hover an engineer, or open the **Thoughts** panel (RCT's guest-thoughts list):

```
 ▸ "Scanner 04 overlay is drifting. I've flagged it three times."
 ▸ "We're shipping Kestrel-3 with 61% coverage. I signed the waiver."
 ▸ "Second interview at the place across the street went well."
 ▸ "Nobody has touched the FA backlog since the layoffs."
 ▸ "This is the best silicon I've worked on."
```

The mechanics that hang off this:

- **Ripple cards announce themselves as thoughts first.** Before a consequence
  card flips, the world leaks tells: a thought repeated four quarters running,
  a maintenance log slipping, lots dwelling a little long in one bay. **The
  player who walks their fab catches ripples early. The player who only reads
  the dashboard gets ambushed.** This is the best thing in either document —
  it converts an abstract delayed-consequence system into *observable reality*,
  and makes "management by walking around" a literal, rewarded mechanic.
- **Culture drift is visible as absence.** DESIGN.md §5: if you repeatedly
  punish bad news, engineers stop raising problems. On screen, **the thought
  bubbles simply thin out.** The fab goes quiet. New players will think things
  are going well. That silence is the scariest thing in the game and it costs
  nothing to implement.
- **Flight risk is visible as behaviour** — an engineer taking calls outside,
  a badge-in at an odd hour, a desk getting tidier.
- **Morale overlay** = RCT's guest-happiness overlay, straight across.

**Attention as a resource.** You're a CEO; you can't be everywhere. You get a
small number of **attention tokens** per quarter. A floor walk, a skip-level
1:1, a customer visit, a deep-dive on a defect — each costs one. Walking the
floor surfaces information that exists in no report. This makes the RCT-ish
pottering *strategically correct* rather than a distraction from the "real"
game, which is the trap a spatial layer usually falls into.

---

## 4. Overlays (the toolbar that does the heavy lifting)

RCT's overlay buttons, repurposed. Each is one click and re-skins the world:

| Overlay | Shows | Scale |
|---|---|---|
| **Yield heatmap** | Which bay is killing you | Floor |
| **Particles / contamination** | Cleanliness by bay | Floor |
| **Utilisation** | Bottlenecks in red, idle capacity in blue | Floor/Campus |
| **Cycle time** | Where lots dwell | Floor |
| **Cost per wafer pass** | Where money burns | Floor |
| **Morale** | Guest-happiness, basically | Campus |
| **Clearance / security** | Who can walk where — see §5 | Campus/Floor |
| **Construction** | What's being built and when it lands | Campus |
| **Age / depreciation** | Which assets are still bleeding you | Campus |
| **Supply risk** | Thread thickness and single points of failure | World |
| **Political risk** | Sanction exposure by region | World |

---

## 5. Spatialising the weirder mechanics

The test of this interface is whether the *abstract* systems from DESIGN.md get
better when made physical. They do:

**Espionage → doors.** Compartmentalisation (DESIGN.md §7, "−8% engineering
velocity") becomes **placing badge-reader doors on your campus.** You draw the
boundaries. Engineers now walk further and collaborate less — the velocity hit
is emergent from pathing, not a modifier. And a mole's badge-in pattern is
visible on the clearance overlay *if you look*. False positives stay possible,
because a weird badge pattern is also what a new parent on a shifted schedule
looks like.

**Export-control thresholds → the loading dock.** When a sanction lands, trucks
physically stop leaving for that region. Finished goods pile up at the dock.
The de-contenting decision (ship a deliberately worse chip to stay legal) is a
project on a layout table in the design centre, and you can watch a team of
your best engineers spend nine months making your product worse.

**The Allocation crisis → a queue at the dock.** When you're capacity-short,
customer reps literally show up. Cars arrive. The automotive OEM's logistics
manager stands in your lobby. You drag wafer-start allocations between them in
a physical board. Starving the three-person startup is a thing you *do with
your hand* rather than a number you type.

**Design wins → the socket wall.** A physical board in the design centre, one
card per socket, with its ramp curve and its end-of-life date. A wall where
everything expires in the same 18 months is a visual gut-punch you can see
three years out — and still fail to prevent.

**First silicon → the bring-up lab.** Tapeout sends a truck to the mask shop.
Ten weeks later masks come back in cases. Then there's a night in the bring-up
lab where the part either posts or it doesn't, with your team standing around
an oscilloscope. If it doesn't: a respin, two quarters, and a mask-set bill.
This should be the most tense 30 seconds in the game and it's free drama — it's
just a room you zoom into.

**The Fire / supply shock → the thread snaps.** You see it on the world map
before you get the email.

---

## 6. Time controls

Paradox-style, RCT-flavoured:

- **Pause / 1× / 2× / 4×.** The world freezes mid-stride on pause; you can still
  click, inspect, and issue orders. Inspection is always free.
- Operations tick continuously (days). Quarters close with a small ceremony —
  the numbers land, the board gets a report, ripple cards flip.
- **Auto-pause on events**, fully configurable (tool down >4h, engineer
  resignation, sanction, forecast revision >15%, construction milestone). This
  is how you stop a spatial game from being a vigilance tax.
- **Speed through the boring quarters** — and the game will let you speed right
  past the four tells it gave you. That's the deal.

---

## 7. Art direction

- **Isometric, clean, legible.** Not photoreal, not cartoon — somewhere near
  *Project Highrise* / *Two Point* precision with a colder palette.
- **A fab is already gorgeous**: white and beige surfaces, amber FOUP status
  lights, overhead transport gliding, bunny suits as colour-coded blobs. Lean
  into it. The cleanroom should look *calm and expensive*, which makes the
  P&L underneath it funnier.
- **Mood by scale** is the whole emotional design:
  - **Floor** — warm, humming, busy, competent. HVAC roar. Things working.
  - **Campus** — weather, seasons, construction, cars arriving. Time passing.
  - **Desk** — quiet, paper, a ticking clock.
  - **World** — cold, political, slow. No people.
- **Sound:** HVAC hum, FOUP transport whir, a tool alarm that you will learn to
  dread, and total silence in the boardroom.
- **Seasons and years visibly pass on the campus.** Trees you planted in 1998
  are large in 2031. Nothing sells a 40-year campaign like that.

---

## 8. What this changes about the build order

DESIGN.md §14 said "spreadsheet sim first." That's still right — but the
prototype order now forks:

1. **Spreadsheet sim** (unchanged) — cycle + capacity + depreciation + yield.
   Prove the capacity-timing trap is painful before any pixels.
2. **The FLOOR toy** — one fab, 20 tools, lots flowing, queues forming, tools
   breaking, one clickable tool window. No strategy layer at all. Prove that
   *watching a fab run is fun on its own*. If it isn't, the spatial layer is
   decoration and we should know that in week three.
3. **Engineer thoughts** — 30 authored thought lines, flight risk, morale. Prove
   the "walk the floor and catch the problem early" loop.
4. **Join the clocks** — put the spreadsheet sim's quarterly layer under the
   floor toy. Campus scale with visible construction.
5. Then the rest of DESIGN.md in its stated order (sockets → people graph →
   geopolitics → espionage).

**The kill-switch question for step 2:** can a player, with no tutorial, look
at the fab floor for 60 seconds and correctly identify the bottleneck? If yes,
the whole interface works. If no, reduce the tool count until they can.

---

## 9. Open questions this raises

- **Do you build the fab interior, or does it auto-plan?** Full tool-by-tool
  placement is a great puzzle and a terrible onboarding. **Lean:** auto-plan a
  valid layout, let the player *re-arrange* for optimisation. Opt-in depth.
- **How many campuses before it's unmanageable?** Late-game you'll have 5–8
  sites. **Lean:** only your "home" campus is fully walkable; satellites get a
  simplified floor view and a site manager you hire, whose competence is itself
  a hiring decision.
- **Does the operations clock become busywork by hour 20?** **Lean:** yes,
  unless you can delegate. Hiring a strong VP of Operations should let you
  automate PM scheduling, tech assignment, and lot dispatch — turning the
  early-game micro into a late-game *trust* decision. Delegation is a feature,
  not a convenience.
- Is the office/DESK scale one zoom too many, or is it the best part?

---
---

# PART II — The Civilization Layer

*Added after vmaz: "or a bit like Civilization."*

## 10. They don't compete — they stack

The two references land on **different scales**, and the weakest-specified part
of Part I was the WORLD scale. Civ fills exactly that hole.

```
   WORLD    ◂── CIVILIZATION ──▸   tiles, strategic resources, rivals,
                                   tech tree, diplomacy, eras, "Firsts"
   CAMPUS   ◂── RCT ───────────▸   buildings, construction, people
   FLOOR    ◂── RCT ───────────▸   tools, queues, bottlenecks, yield
   DESK     ◂── diegetic docs ─▸   board, roadmap, forecasts
```

**The pitch becomes:** *Civilization from the boardroom, RollerCoaster Tycoon
from the factory floor.* Zoom out and you're playing a 40-year game of
technological geopolitics against three rivals. Zoom in and you're figuring out
why Bay 2 is dirty. Same world, same clock, same decisions — just different
altitudes. That's a real game, and I don't think it exists.

---

## 11. Strategic resources — Civ's best mechanic, and it's *literally true here*

Civ: *you cannot build Legions without Iron.* The semiconductor industry works
exactly this way, which is almost unfair as a design gift.

The world map has **nodes of material and capability** sitting in specific
territories, and you cannot build certain things without securing access:

| Resource | Gates | Where it is |
|---|---|---|
| **EUV scanners** | Everything below 7nm | One building, one country |
| **High-purity quartz** | Crucibles → all silicon | Two deposits on Earth |
| **Advanced photoresist** | Leading-edge litho | A handful of Japanese chemical towns |
| **Neon / rare gases** | Excimer lasers | Concentrated, and in a war zone a worrying amount of the time |
| **Substrates (ABF)** | Advanced packaging | A chronic, boring, fatal shortage |
| **Rare-earth targets** | Deposition | One country's export policy |
| **Talent clusters** | Everything | Tiles, not minerals — and they take 20 years to grow |
| **Grid power + water** | Fab siting | Why fabs go where they go |

**How you secure access** (none of it is conquest):
- long-term offtake contracts
- equity stakes in the supplier
- co-funding their capacity expansion (expensive, years early, invisible on
  your P&L until the year it saves you)
- being politically welcome in that territory
- second-sourcing — costs money and qualification time and your board will ask
  why, right up until the quarter it makes you look like a prophet

**Rivals can lock resources up.** Pre-buying three years of a supplier's
output is a legitimate, visible, infuriating move — and it's exactly what
really happens. You can see it coming on the supply-thread overlay if you're
watching.

**Resources can be severed.** A region turns red, a thread snaps, and the fab
you spent four years building cannot start wafers. This is where Part I's
"threads snap on the world map" and DESIGN.md's geopolitics track converge.

---

## 12. The Tech Tree

Civ's clearest contribution. The semiconductor tech tree is genuinely
beautiful, branching, and full of real trade-offs — and unlike Civ, **you will
never light up more than ~40% of it in a run.** Node cost scales ~1.9× per
generation, so the tree is a *choice* structure, not a completion checklist.
That's a straight improvement on the genre's usual tech tree.

```
LITHOGRAPHY     i-line ─ DUV ─ immersion DUV ─ EUV ─ High-NA EUV
                                  ╰─ multi-patterning (cheap, slow, ugly)
TRANSISTOR      planar ─ strained Si ─ FinFET ─ GAA/nanosheet ─ CFET
MATERIALS       Si ─ SOI ─ SiGe ─┬─ SiC ──┐
                                 ╰─ GaN ──┴─ power segment unlock
                                 ╰─ 2D materials (late, speculative)
PACKAGING       wirebond ─ flip-chip ─ 2.5D interposer ─ hybrid bonding
                                    ╰─ chiplets ─ co-packaged optics
DESIGN / EDA    schematic ─ synthesis ─ P&R ─ DFM ─ ML-assisted closure
METROLOGY       optical ─ e-beam ─ in-line ─ computational
                 ↳ gates how fast you can *learn* every other branch
MEMORY          DRAM ─ stacked ─ HBM ─ in-memory compute
```

Rules that keep it from being a Civ clone:

- **Branches gate each other diagonally.** GAA without advanced metrology = you
  get the transistor and your yield is garbage for six quarters, because you
  cannot *see* your defects. Metrology is the unglamorous branch that secretly
  accelerates everything, and most players will underinvest in it. Correctly.
- **No tech is free to hold.** Leading-edge capability has an ongoing R&D cost.
  Stop paying and it rots — your 3nm team disperses.
- **Techs unlock *products*, not units.** A tech plus a segment plus a socket
  win plus capacity equals revenue. Four gates, each with its own lead time.
- **Some branches are exits, not upgrades.** SiC/GaN power isn't "ahead of"
  logic — it's a different company. Taking that branch is a strategic fork, and
  the game should treat it as a legitimate way to win.

---

## 13. "Firsts" — Civ Wonders, and they're a race

World Wonders translate perfectly, because semiconductor firsts are genuinely
winner-take-most and genuinely wasteful to lose.

> **FIRST PRODUCTION EUV FAB** — 16 quarters, $11.4B
> *Rumour (confidence: medium): Hoshino Semiconductor is ~70% complete.*
> [Continue] [Accelerate: +$2.1B, −3 quarters] [Abandon: recover 20%]

- **Win it:** an 18-month monopoly window at monopoly pricing, a permanent
  prestige modifier that pulls talent and design wins for a decade, and
  first-mover yield learning your rivals can't buy.
- **Lose it:** you get the learning (real, and it compounds) but none of the
  prize, and a $9B hole. The *decision to keep going at 70% when you hear the
  rumour* is one of the best decision points in the design — and the rumour's
  confidence level is itself something you paid for three quarters ago.

Candidate Firsts: 300mm conversion · first production EUV · first GAA in volume
· first HBM stack · first commercial chiplet standard · first co-packaged
optical interconnect · first 2nm-class node · first fully-automated fab.

---

## 14. Rivals as Civ leaders

Three **fully-simulated** rivals with visible doctrines (plus ~8 statistical
background competitors, per DESIGN.md §15). Each is a coherent, legible
personality — Civ's leaders, but as industrial strategies you can learn to
predict and bait:

| Rival | Doctrine | How to beat them | How they beat you |
|---|---|---|---|
| **The Scale Monopolist** | Builds capacity recklessly, crashes ASPs, survives on balance sheet | Don't fight on price; own a segment they can't serve | Out-waits you in a glut |
| **The Node Purist** | Always bleeding-edge, chronically cash-poor | Buy them at the bottom | Takes every premium socket for a decade |
| **The Trailing-Edge Milker** | Never advances, prints money, buys your cast-off fabs | Ignore them — they're not your problem | They're *never* your problem, and they outlive you |
| **The National Champion** | Subsidised, cannot fail, irrational pricing | You can't. You route around them. | Distorts every market they enter |

They act *visibly*: capex announcements, hiring raids, tool orders you can see
in the equipment order book, Firsts progress rumours, poaching your people.
The news ticker is the diplomacy screen for most of the game.

**Diplomacy, industry-flavoured** — not war and peace, but:
cross-licensing · patent litigation · second-source agreements · joint process
development consortia (IMEC-style: share cost, share learning, share it with
your rival) · capacity swaps in a crunch · and embargoes, which are Civ's
embargo mechanic with the serial numbers filed off.

A **joint development agreement** with the Node Purist is Civ's alliance: you
split a $6B node cost, you both get it, and you've permanently armed someone
who will use it against you in 2038. Classic.

---

## 15. Civics → Corporate Doctrine

Civ's government/policy cards become your **operating doctrine** — a small set
of slotted choices you can swap at a real cost and a cooldown:

- **Sales comp:** bookings (optimistic forecasts, volume, margin erosion) vs
  margin (honest forecasts, missed volume opportunities). *Already load-bearing
  in DESIGN.md §1.3 — it permanently colours your information quality.*
- **Capital discipline:** build-ahead · build-to-order · build-only-with-prepay
- **Secrecy posture:** open/collaborative (faster, leakier) vs compartmentalised
  (slower, safer — and in Part I this is literally doors on your campus)
- **R&D intensity:** a % that the Activist board member attacks every meeting
- **Talent strategy:** grow-your-own (slow, loyal, 20-year payoff) vs
  acquire-and-raid (fast, mercenary, inflates your whole region's salaries)

Doctrine swaps cost morale and take quarters to take effect. The Latency Ledger
applies to culture too.

---

## 16. Site selection = city placement

Part I §1.1 had site selection as a scored decision. Civ sharpens it into the
real thing: **good sites are finite and contested, and your rival can take one
first.**

Tiles carry yields — talent pool, grid power, water, political stability,
logistics, seismic risk, subsidy on offer — and **adjacency matters**: a design
centre next to a university tile compounds over twenty years; a fab next to
your own existing fab shares utilities, talent, and institutional knowledge
(this is why real fab clusters exist, and the game should reward it).

Some tiles are **generational**: a cluster that takes two decades to mature.
Planting a design centre in 1996 next to a good university and watching it
become your crown jewel in 2024 is the Civ feeling, exactly, and it's
historically true.

---

## 17. Advisors

Civ's advisors, but **each one is systematically wrong in a learnable
direction** — and discovering their biases over a 40-year campaign is part of
the play:

- **CFO** — always wants less capex. Right in 3 of 4 cycle phases. Catastrophic
  in the fourth.
- **CTO** — always wants the next node. Will not acknowledge that trailing edge
  is where the margin is.
- **COO** — always wants more slack and more PM. Boring, unglamorous, and the
  reason you survive.
- **Head of Sales** — forecast is a function of their comp plan, which *you set*.
- **General Counsel** — the only one who ever mentions export controls, and
  only the quarter before it's too late.

Their advice goes in the quarterly brief. Players who learn to apply a standing
correction to each advisor are playing the game correctly.

---

## 18. What stays RCT, what becomes Civ

| System | Home | Why |
|---|---|---|
| Tech tree, Firsts, resources, rivals, diplomacy, doctrine, site placement | **Civ** | Strategic, turn-based, global, 40-year arc |
| Tools, queues, bottlenecks, yield, defect mechanisms, construction, engineer thoughts, floor walks, overlays, attention tokens | **RCT** | Tactile, immediate, spatial, learnable by looking |
| Shadow Calendar, Fog Cone, board, roadmap | **Diegetic docs** | They're documents in real life too |

**Turn structure resolves cleanly:** the quarter is the Civ turn. Within a
quarter, operations run on the fast clock (pausable, speed-uppable) — so the
RCT layer is what you *do* while the Civ turn is resolving, rather than a
separate mode. End-of-quarter is Civ's "next turn" button, with the board
report, the ripple flips, and the rivals' moves landing at once.

## 19. Revised prototype order

Part I's build order holds, with Civ bolted on at the right moment:

1. Spreadsheet sim — cycle, capacity, depreciation, yield *(unchanged)*
2. **The FLOOR toy** — 20 tools, queues, one clickable window. *Can a new
   player spot the bottleneck in 60 seconds with no tutorial?*
3. Engineer thoughts + the floor-walk loop
4. Join the clocks: quarterly layer under the floor toy, campus construction
5. **The Civ layer**: tech tree + one rival + strategic resources. Test
   specifically whether zooming between altitudes feels like one game or two.
   *This is the project's biggest risk and should be tested early-ish, not last.*
6. Firsts, diplomacy, doctrine, site contest
7. Sockets → people graph → geopolitics → espionage *(per DESIGN.md §14)*

**The risk to name out loud:** two beloved references can produce a game that
does neither well. The mitigation is that they're assigned to *different
altitudes of the same world* rather than interleaved — and step 5 is the
honest test of whether that's true.
