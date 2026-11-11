# SEMI TYCOON SIMULATOR
### Design Bible v0.1 — "You are always betting on a world that doesn't exist yet."

---

## 0. The Pitch

You are the CEO of a semiconductor company. You start in a leased corner of
somebody else's fab with four engineers and one customer. If you survive forty
years you are a geopolitical asset that three governments fight over.

The industry's defining property is **latency**. A fab takes four years to
build. A chip takes three years to design. A process node takes five years to
develop. By the time any decision you make produces a result, the world that
justified it is gone. Every other tycoon game is about *optimizing the present*.
This one is about **committing to a forecast and living with it.**

> **The one-sentence hook:** *Every lever in this game has a delay fuse on it,
> and the explosion always lands in a different market than the one you aimed at.*

---

## 1. The Three Signature Mechanics

Everything else is scaffolding around these.

### 1.1 The Latency Ledger

Every action in the game carries a visible **lead time**. You never act on
*now*. You act on a quarter 2–20 turns out.

| Lever | Lead time | Reversible? |
|---|---|---|
| Change price | 0 quarters | Yes (but the customer remembers) |
| Reallocate wafer starts | 1 quarter | Yes |
| Change test coverage | 1 quarter | Yes — consequences land in 8 |
| Hire a senior engineer | 2–4 quarters | Slowly |
| Ramp an existing design | 2 quarters | Yes |
| Tape out a new chip | 6–10 quarters | **No.** Mask set is sunk. |
| Qualify a new node | 12–20 quarters | **No.** |
| Build a fab | 14–24 quarters | **Catastrophically no.** |
| Build advanced packaging | 8–14 quarters | No |
| Change your public roadmap | 0 quarters | Costs credibility permanently |

The main screen is dominated by the **Shadow Calendar** — a horizontal strip
showing everything currently in flight and the quarter it lands. The strategic
act of the game is reading the shape of that strip against the shape of the
demand forecast and noticing they don't match.

**The trap the game is built around:** capacity decisions feel safest at the
top of the cycle, when cash is abundant and customers are begging. That
capacity arrives 18 months later, into a glut, with depreciation attached. The
game will let you do this. It will let you do it *every cycle.*

### 1.2 The Ripple Deck (consequence cards)

Every meaningful decision silently writes a face-down card into a future
quarter's event deck. This is how "past decisions ripple out" becomes a system
rather than flavor text.

```
 Q3 2031  — you cut the validation headcount 40% to make the quarter
            ↳ writes: [RIPPLE · hidden · lands Q1 2034]
 Q1 2034  — ▸ ERRATA DISCOVERED: cache coherency bug in Kestrel-3.
            Shipped into 2.1M automotive units. Field recall exposure $340M.
            Traced to: validation cuts, Q3 2031.
```

Rules that make this *fair* rather than cruel:

- **Cards are visible as shapes before they're visible as content.** The
  Shadow Calendar shows a grey marker: *"Q1 2034 — 1 unresolved consequence,
  origin: Operations, severity unknown."* You know something is coming.
- **You can spend to resolve early.** A "Technical Debt Review" action flips a
  card face-up 4 quarters ahead of time and lets you spend money/engineering
  to defuse it at 30% of the eventual cost. This is the *entire* argument for
  doing boring maintenance work, expressed as a mechanic.
- **Good decisions write cards too.** The engineer you backed in 2029 when the
  board wanted him fired invents your packaging advantage in 2036.
- **Cards compound.** Two unresolved Operations ripples landing in the same
  quarter merge into one larger event with a worse headline.

### 1.3 The Fog Cone (information as a resource)

You see demand forecasts as a **cone**, not a line. Near quarters are narrow;
far quarters are a wide fan. Your decisions must be made at the wide end.

The cone narrows when you spend on information:
- **Customer forecast sharing** — narrows the cone for *that customer*, and
  they lie slightly in a direction that benefits them (they over-forecast to
  secure allocation; the game models this and you can learn each customer's
  personal bias over years).
- **Teardowns** — buy a competitor's product, reverse-engineer it, learn their
  die size, node, and therefore their cost structure. Takes 2 quarters.
- **Analyst / channel checks** — cheap, noisy, systematically lagging.
- **Your own sales force** — the best signal, but it's biased by comp structure.
  If you pay on bookings, your forecast is optimistic. If you pay on margin,
  your reps don't tell you about volume opportunities. *This is a setting you
  choose and it permanently colors your information.*
- **Equipment order book** — watching litho tool lead times tells you what
  *everyone else* is building. The single best leading indicator in the game,
  and it is public. Most players never look at it.

---

## 2. Core Loop

```
   ┌─────────────────────────────────────────────────────────────┐
   │  QUARTER TURN                                               │
   │                                                             │
   │  1. BRIEF      Market moves, competitor news, world events  │
   │  2. RIPPLE     Face-down cards from past quarters flip      │
   │  3. ALLOCATE   Wafers, engineers, capex, cash               │
   │  4. COMMIT     Start things that land 2–20 quarters out     │
   │  5. NEGOTIATE  Customers, suppliers, governments, the board │
   │  6. RESOLVE    Yield, revenue, cash, morale, reputation     │
   │                                                             │
   │  ── every 4 quarters ──▸ BOARD MEETING (the real boss)      │
   │  ── every ~12–20 q  ──▸ CYCLE TURN (boom ⇄ bust)           │
   │  ── every ~8–12 q   ──▸ NODE TRANSITION DECISION            │
   └─────────────────────────────────────────────────────────────┘
```

**The four resources you're actually juggling** (money is the least interesting):

1. **Cash** — obvious, but in this industry it's really *cash minus the capex
   you already committed to.*
2. **Engineering-quarters** — your scarcest resource. Splittable across design,
   process, packaging, validation, failure analysis, and customer support.
   Every one you spend on a customer's problem is one you didn't spend on the
   node.
3. **Credibility** — with customers, with the Street, with governments. Spent
   when you miss a roadmap. Earned when you deliver early or eat a cost that
   was technically the customer's fault.
4. **Slack** — organizational margin. Invisible gauge. High slack absorbs
   shocks; zero slack means every surprise becomes a crisis and your best
   people quit. Running at zero slack is the most profitable way to play for
   eight quarters and the fastest way to lose the game by quarter twenty.

---

## 3. The Company Model

### 3.1 The Identity Trilemma

Your business model is a live choice you can switch between (expensively):

| Model | You own | Strength | Fatal flaw |
|---|---|---|---|
| **Fabless** | Design + IP | Capital-light, pivot fast | You are a *guest* in someone's fab. In a crunch you are allocated last. |
| **IDM** | Design + Fab | Margin, control, secrecy | Fab fill risk. Your fab is sized for a product forecast that will be wrong. |
| **Foundry** | Fab + process | Scale, customer diversity | You must never compete with your customers, which caps your ambition forever. |
| **Fab-lite** | Design + trailing fab | Hedged | Good at nothing; a real mid-game trap. |

Switching is a multi-year project with its own ripple cards. A fabless company
that builds its first fab discovers it has no manufacturing culture — a hidden
"Operations Maturity" stat that starts near zero and only climbs with
experience. Your first fab will have terrible yield and the game will not
warn you.

### 3.2 The Yield Model (why this is fun and not a slider)

Yield is **not a number you buy.** It's a curve you climb, and it's gated by
hidden **defect mechanisms**.

```
  Node: 7nm "Vireo"        Maturity: 31%        Yield: 44%
  ┌──────────────────────────────────────────────────────┐
  │  KNOWN DEFECT MECHANISMS                             │
  │   ▸ Overlay error, M2–M3         -11% yield   [FA 2q]│
  │   ▸ Particle, chamber 4          -6%  yield   [fix 1q]│
  │   ▸ ████████████ (unidentified)  -?            [FA 3q]│
  │   ▸ ████████████ (unidentified)  -?            [FA 4q]│
  │  Baseline random defect D₀ ........ -14%             │
  └──────────────────────────────────────────────────────┘
```

- You assign **failure-analysis engineer-quarters** to reveal a hidden
  mechanism. Then you assign more to fix it.
- **Some fixes trade off against each other.** Tightening the etch to kill the
  via problem raises line-edge roughness. The game shows you this only after
  you've done it once — you build an institutional knowledge base across
  playthroughs *within a campaign*, as a tech tree of "things our company
  learned the hard way."
- **Die size interacts brutally.** Yield falls superlinearly with area, so the
  big fat AI accelerator your sales team wants is the one your yield can't
  support. The counter-play — **chiplets** — is a real mid/late-game unlock
  that trades yield for packaging complexity and a whole new failure domain.
- **Yield learning is a company asset, not a node asset.** Ship a node for
  three years and you'll run the next one better. Skip a node and you lose the
  learning. *This is the real reason "just sit out one generation" is a trap.*

### 3.3 Capacity & The Depreciation Guillotine

A fab's cost isn't the capex — it's the **depreciation that keeps hitting your
P&L every quarter whether the fab runs or not.** This is the mechanic that
makes downturns terrifying.

```
  FAB 2 · Dresden · 300mm · 28nm      Utilization: 41%
  Capacity 42k wspm · Running 17k wspm
  Quarterly depreciation ............ $310M   (unavoidable)
  Quarterly fixed opex .............. $180M   (idling saves only 30%)
  Gross margin at 41% util .......... −12%
  ▸ Breakeven utilization: 68%
```

Options under a glut, each a different flavor of pain:
- **Dump product at cost** to fill the fab (destroys ASPs industry-wide, and
  the competitor you hurt remembers for a decade)
- **Take foundry work** from anyone, including a competitor (fills the fab,
  teaches them your cost structure)
- **Idle the fab** (saves little; demoralizes; the tools de-tune and yield
  regresses when you restart — a nasty, real detail)
- **Mothball permanently** (one-time writedown, board revolt, but it's over)
- **Sell it** to the one buyer who exists, at the worst possible moment

---

## 4. The Market Map

Segments appear, grow, mature, and die over the campaign. Each is a different
*shape* of business, not just a different margin number.

| Segment | Volume | Margin | Node | Qual burden | Personality |
|---|---|---|---|---|---|
| **Consumer / toys** | High | Awful | Trailing | None | Pays late, churns instantly |
| **PC / client** | High | Thin | Leading-1 | Medium | Brutally cyclical, one OEM is 30% of it |
| **Mobile AP** | Huge | Thin | Bleeding | High | Annual design-win cliff; lose it and you lose *everything* for a year |
| **Automotive MCU** | Medium | Good | Trailing | **Extreme** (AEC-Q100, 15yr supply) | Never leaves — unless you fail them once |
| **Industrial** | Low | Great | Trailing | High | Thousands of tiny loyal customers; recession-resistant |
| **Datacenter CPU** | Medium | Excellent | Bleeding | Medium | 4 customers on Earth, all of them want to build it themselves |
| **AI accelerator** | ??? | ??? | Bleeding + packaging | Low | Appears mid-game, 10x's, then either becomes infrastructure or craters |
| **RF / connectivity** | High | Medium | Specialty | High | Standards-cycle locked; miss the standard, miss the decade |
| **Power (SiC/GaN)** | Growing | Good | Specialty | Extreme | Entirely different fab. A real "second company" decision. |
| **Memory** | Enormous | −40% to +60% | Own thing | Low | A commodity casino. Optional late-game mode for lunatics. |
| **Optical / co-packaged** | Small→? | ? | Packaging-led | Extreme | Late-game frontier |

**Design wins, not sales.** You don't sell chips, you win sockets. A design win
is a 2-year sales cycle that produces 5–8 years of revenue. This means:
- Your revenue today is the product of decisions from 2019.
- Losing a socket doesn't hurt today — it hollows out 2031.
- **The Socket Board** is a key screen: every socket you hold, its ramp curve,
  its end-of-life date, and whether it's being re-competed. A board full of
  sockets all expiring in the same 18 months is a death sentence you can see
  coming for three years and still fail to prevent.

---

## 5. People

Engineers are **named individuals with a bus factor**, not a headcount slider.

```
  ┌───────────────────────────────────────────────────────┐
  │  Dr. Wen Li        Lithography / Overlay      ★★★★★    │
  │  11 years · Morale 3/10 · Vesting cliff Q4 2031       │
  │  ▸ Sole owner of: 7nm overlay recipe, EUV pellicle qual│
  │  ▸ Flight risk: HIGH (competitor opened a site 9mi away)│
  │  ▸ Last promoted: never                                │
  └───────────────────────────────────────────────────────┘
```

- **Specialists own knowledge.** If Wen Li leaves, the 7nm overlay fix you were
  three quarters from completing resets to zero *and* a competitor's node
  schedule improves. The game shows you her "sole owner of" list — the
  mitigation is deliberate knowledge-spreading, which costs engineer-quarters
  and produces nothing visible. Classic.
- **Morale is driven by what you actually did**, not a budget slider: did you
  ship their project or cancel it? did you blame engineering publicly for the
  errata? did you backfill after layoffs or pile the work on survivors?
- **Culture drift.** Repeatedly prioritizing schedule over quality shifts a
  hidden org stat. Eventually your engineers *stop raising problems* — the
  game simply gives you fewer warnings. Your information quality degrades and
  you won't be told why. (Reveal on post-mortem screen.)
- **The hiring raid.** You can open a design center 9 miles from a competitor
  and poach. They can do it to you. Retaliation spirals are a real dynamic:
  salaries in a region inflate permanently once started.
- **Succession.** Your own key lieutenants age out. The VP of Operations who
  carried you through two downturns retires in 2034 and you'd better have
  someone ready.

---

## 6. Geopolitics — The Pressure System

A background **Geopolitical Pressure** track drifts over the campaign, with
visible leading indicators (trade rhetoric, election cycles, a border incident
on the news ticker). It manifests through four instruments:

**1. Entity lists / export controls.** A customer, a country, or a *performance
threshold* gets restricted. The threshold mechanic is the most fun:

> *New rule: devices exceeding 4,800 TOPS/mm² may not be exported to Region B.*
>
> Your Hawk-5 is at 5,200. Options:
> - **De-content it.** Spend 3 quarters making a deliberately worse chip to
>   stay under the line. Costs engineering, saves 31% of revenue.
> - **Ship as-is, lose the region.** Clean, honest, expensive.
> - **Route it through a distributor in Region C.** +Revenue now.
>   [RIPPLE · hidden · lands 6–14 quarters] ← this card is an investigation.
> - **Lobby.** Costs cash and credibility, 40% chance of a 2-quarter delay.
>
> *Eighteen months later the threshold moves to 3,200 and your de-contented
> part is illegal too.* The game does this on purpose.

**2. Subsidies with strings.** A government offers $4B toward a fab — in the
wrong place, with hiring quotas, a profit-sharing clawback, and a condition
that you don't expand in Region B for ten years. Accepting is usually correct
and always costs you optionality later.

**3. Chokepoints.** EUV tools, photoresist, neon, rare-earth targets, substrate
materials, and a single Japanese company that makes one chemical. Your supply
chain is a visible graph with risk weightings. Second-sourcing costs money and
qualification time and the board will ask why you're spending it. Then one
node fails and everyone who second-sourced looks like a genius.

**4. National champion status.** Late game, you can become strategically
important enough that a government will not let you fail — which also means
they will not let you be sold, will not let you build where you want, and
will expect you to answer the phone.

---

## 7. Espionage & Counterintelligence

A hidden-information minigame that runs the whole campaign, played with
**tells, not certainties.**

Signals you might notice (all deniable):
- A competitor announces a part with suspiciously convergent specs 5 months
  after your internal spec freeze.
- Your bid for a socket loses by 2%, three times in a row.
- A supplier mentions your unannounced wafer-start ramp, casually.
- An engineer's badge-in pattern changes.

Responses, all costly:
- **Compartmentalize** — slows your own engineering (people can't see the
  whole design), permanently, ~8% velocity.
- **Counterintelligence investment** — surfaces more tells, including **false
  positives.** Acting on a false positive and firing a loyal 12-year engineer
  is devastating to morale and the game will absolutely let you do it.
- **Feed disinformation** — plant a fake roadmap. If it works, your competitor
  commits $2B to a node nobody needs. If it's discovered, your credibility with
  customers (who also saw the fake roadmap) collapses.
- **Do nothing.** Often correct. The paranoid player loses to the calm one.

You can also *be* the aggressor. Hiring a competitor's engineer and asking the
wrong question produces a trade-secrets lawsuit that lands 3 years later and
takes 11% of your market cap. The game is not moralistic about this; it's
actuarial.

---

## 8. The Industry Cycle

A hidden cycle phase, inferable from public indicators:

```
   ◂── ACCUMULATION ── EUPHORIA ── DENIAL ── CAPITULATION ── ◂
        lead times↑    lead times↑↑  inventory↑   util↓↓
        util↑          everyone      cancellations  writedowns
        prices stable  announces     begin          M&A window
                       capex
```

**Visible indicators** (all public, all lagging differently):
`book-to-bill` · `channel inventory weeks` · `litho tool lead time` ·
`competitor capex announcements` · `spot wafer price` · `your own customers'
forecast revisions`

The cycle is the game's metronome. It rewards contrarians and punishes
consensus, which is correct and also very hard to actually do when your board
is screaming at you during EUPHORIA that you're ceding share.

**The Capitulation M&A window** is the game's great opportunity: at the bottom,
good assets are cheap and nobody has cash. Having cash at the bottom is the
whole game, and it requires you to have been unpopular at the top.

---

## 9. Screens (storyboard)

### 9.1 The Bridge — main quarterly view

```
╔══════════════════════════════════════════════════════════════════════════╗
║ KESTREL MICROSYSTEMS          Q2 2031        Cash $1.84B   ▲ Cycle: DENIAL║
╠══════════════════════════════════════════════════════════════════════════╣
║ SHADOW CALENDAR                                                          ║
║  '31 ▏'32 ▏'33 ▏'34 ▏'35 ▏'36                                           ║
║  ──●──────────────────────────────  Hawk-5 tapeout       lands Q4'32     ║
║  ────────●──────────────────────── 5nm qual              lands Q1'33 ⚠   ║
║  ──────────────●────────────────── Fab 3 Dresden         lands Q3'34     ║
║  ──────▒──────────────▒─────────── 2 unresolved ripples  [REVIEW]        ║
║  ░░░░░░░░▒▒▒▒▒▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ demand fog cone                       ║
╠══════════════════════════════════════════════════════════════════════════╣
║ ENG-QUARTERS  840 available                                              ║
║   Design ████████████░░ 420   Process ██████░░ 210   Validation ██ 60 ⚠  ║
║   Failure analysis ███ 90     Customer support ██ 60                     ║
╠══════════════════════════════════════════════════════════════════════════╣
║ ▸ NorthStar revised Q4 forecast DOWN 22%. Third cut this year.           ║
║ ▸ ASML lead times extended to 26 months. Someone is ordering heavily.    ║
║ ▸ Dr. Wen Li declined the retention package.                             ║
║ ▸ Board meeting in 2 quarters. Roadmap commitment due.                   ║
╚══════════════════════════════════════════════════════════════════════════╝
            [ FAB ]  [ ROADMAP ]  [ MARKET ]  [ PEOPLE ]  [ WORLD ]
```

### 9.2 The Boardroom (annual)

Three factions with different win conditions, and you can't satisfy all three:

- **The Activist** — wants buybacks, margin, headcount discipline. Ally during
  a downturn, poison during a buildout.
- **The Strategic** (your government / a sovereign fund) — wants fabs onshore,
  supply security, employment. Patient capital with a political price.
- **The Founder/Technologist** — wants the roadmap, hates de-contenting,
  resigns loudly if you become a trailing-edge milk machine.

Board confidence is a real gauge. At zero you're replaced and the run ends —
but the *epilogue* shows you what your successor did with your decisions, which
is the best possible way to deliver the "ripple" theme as a game-over screen.

### 9.3 The Post-Mortem (end of run)

Not a score screen. A **causal trace**: the game picks your 6 most consequential
decisions and draws the line from each to the outcome, including the ones that
went right. Shows the ripple cards you never saw. Shows the counterfactual the
simulation was tracking the whole time.

---

## 10. Scenario Cards (the writing room)

Each is a decision with no clean answer, a lead time, and a ripple.

**▸ THE WHALE.** NorthStar is 44% of revenue. They demand a 20% price cut and
"second source qualification" — meaning they're teaching your competitor to
build your part. Options: eat it · refuse and lose them over 6 quarters ·
offer a cut contingent on volume commitment (they'll break it) · deliberately
start courting their competitor *now*, which they will find out about.

**▸ THE FIRE.** A chemical supplier's plant burns down. 40% of world photoresist
supply, 4 quarters to restore. You have 11 weeks of inventory. So does a
competitor who serves a customer you've wanted for a decade. Do you sell them
resist at cost to make a friend, hoard, or sell at 6x to a desperate market and
become the industry's villain for fifteen years?

**▸ THE ERRATA.** Field failures in an automotive part. 2.1M units. The bug is
in a block you licensed from a third party. You can: full recall ($340M,
honest, your automotive reputation survives) · silent firmware mitigation
(works 94% of the time, and the 6% is a lawsuit) · blame the IP vendor
(true, and nobody cares, and now no IP vendor trusts you).

**▸ THE NODE CLIFF.** 3nm costs $6B to develop, 4x the mask cost, and only
three customers on Earth can afford parts built on it. Follow, or stop here
and become a very profitable trailing-edge specialist forever? *The game must
make "stop" a legitimately winning strategy* — otherwise it's a treadmill, not
a choice. Trailing-edge is where the margin actually is; the cost is that you
will never matter again, and the Founder board member will say so out loud.

**▸ THE ALLOCATION.** Capacity crunch. You have 60% of the wafers your customers
want. Rank them. The automotive OEM will sue and never return. The hyperscaler
will build in-house if starved. The three-person startup you cut to zero is
building the AI accelerator that defines 2035. *You are not told which one that
is.* (Faint tell: their order grew 300% QoQ off a tiny base, which is also what
every doomed startup looks like.)

**▸ THE SANCTION.** Overnight, 31% of revenue is illegal. See §6.

**▸ THE RAID.** A competitor opens a design center across the street and takes
nine of your people in a quarter. Match salaries (permanent regional inflation,
and your *loyal* people now feel underpaid) · sue over non-competes (2 years,
unenforceable in this jurisdiction, poisons recruiting) · raid them back ·
accept it and fix why people left.

**▸ THE SUBSIDY.** $4B for a fab in a region with no talent pipeline, a hiring
quota, and a 10-year non-expansion clause elsewhere. The money is real. The
constraint kills your 2040.

**▸ THE SANDBAG.** Analyst day. You believe 5nm slips 2 quarters. Announce the
slip (stock −18%, customers start hedging, but you have room) or commit to the
original date (stock holds, and now you *must* ship, which means cutting
validation — hello, THE ERRATA, three years early).

**▸ THE GHOST ORDER.** A customer's orders double. Is it real demand, or are
they double-ordering across suppliers because lead times scared them? Build for
it and you're the one holding inventory when it evaporates. The tell exists in
the data if you bought the right information three quarters ago.

**▸ THE ACQUISITION.** At the bottom of the cycle, a rival with great IP and no
cash is for sale at 0.3x of its peak. You can afford it only if you were
disciplined during EUPHORIA. Integration takes 12 quarters, their culture hates
yours, and their best people vest out in 8.

---

## 11. Era Timeline (campaign)

Playable as **historical campaign** (real-ish eras, fictional companies) or
**open sandbox** (procedural cycles and segments).

| Era | Years | Your scale | Defining pressure |
|---|---|---|---|
| **I · Garage** | 1985–1994 | 4 people, borrowed fab time | One customer is everything; the memory price war wipes out your peers |
| **II · Scale** | 1995–2004 | First fab, 200mm | PC boom → dot-com bust. Your first depreciation guillotine. |
| **III · The Great Split** | 2005–2014 | Fabless/IDM/foundry decision becomes irreversible | Mobile explodes; node costs begin culling the industry |
| **IV · Chokepoint** | 2015–2024 | National relevance | EUV, geopolitics arrives, the auto shortage, packaging becomes king |
| **V · Open horizon** | 2025–→ | Whatever you built | Procedural: AI demand shock, chiplet standards, new materials, and a cycle that doesn't care |

Each era has a **cull event** — a bust that kills a fixed fraction of AI
competitors. Surviving a cull with cash is how you jump tiers.

---

## 12. Numbers Model (first-pass sim spec)

Enough to prototype in a spreadsheet before any art exists.

```
good_die_per_wafer = die_per_wafer × Y
Y                  = exp(−D₀ × A) × Π(1 − m_i)      # m_i = active defect mechanisms
D₀                 = D₀_base × (1 − maturity)^1.6
maturity           += f(eng_quarters_FA, wafer_volume_run, company_yield_learning)

revenue            = Σ_sockets ( units × ASP )
ASP                = ASP₀ × (1 − erosion)^quarters_since_launch × crunch_multiplier
units              = min( demand, allocated_capacity × good_die_per_wafer )

gross_margin       = revenue − (wafer_cost + test_cost + package_cost)
operating_income   = gross_margin − opex − R&D − depreciation
   # depreciation is the term that does not move when revenue halves

cycle_phase        = f(industry_capacity, industry_demand, inventory_weeks)
   # industry capacity includes AI competitors' decisions from 14 quarters ago
```

**Tuning targets:** gross margin 35–60% in good times, −10% in a trough.
Breakeven utilization ~65–70%. Node cost roughly 1.9x per generation. A design
win is 5–8 years of revenue with a 2-year sales cycle. Keep the model honest
enough that a player who learns the game learns something true about the
industry.

---

## 13. Tone & Presentation

- **Diegetic UI.** Everything is an internal document: a board deck, an eng
  status report, a supply-chain risk memo, an export-control counsel email.
  No floating health bars.
- **The news ticker is the ambient narrative.** Competitors act visibly.
  Governments posture. A fire happens in Taiwan. The ticker is how the world
  feels alive without cutscenes.
- **No villain.** Nobody in this industry is evil; everyone is responding to
  a 4-year lead time with 6-month information.
- **Readable art, not photoreal.** Think *Papers, Please* meets a Bloomberg
  terminal meets a Factorio production graph. Dense, legible, monospace-adjacent.
- **Sound:** fab hum, HVAC, a very quiet room where very expensive decisions
  get made.

---

## 14. Build Order (prototype path)

1. **Spreadsheet sim** — cycle + capacity + depreciation + yield curve only.
   Play it in a terminal. If the *capacity-timing trap* is already painful and
   fun here, the game works. If not, nothing else saves it.
2. **Latency Ledger UI** — the Shadow Calendar. The single screen that sells it.
3. **Ripple Deck** — 20 hand-authored consequence cards. Validate that delayed
   consequences feel *earned* and not random.
4. **Socket Board + design wins** — turns revenue into a 5-year-lagged object.
5. **People** — 12 named engineers with ownership graphs.
6. **Geopolitics layer** — the threshold mechanic first, it's the most novel.
7. **Espionage** — last; it's the most elaborate and the least load-bearing.

---

## 15. Open Questions

- Is the quarter the right turn length, or should early eras run on years and
  late eras on quarters?
- Should AI competitors be full simulations (slow, emergent, fair) or scripted
  archetypes (fast, legible, gameable)? **Lean:** 3 full sims + 8 statistical.
- How much real-world history before it becomes a licensing problem? **Lean:**
  fictional companies, real physics, real-shaped events.
- Multiplayer: is there a 4-player version where the capacity glut is *caused
  by the other players*? (This is probably a great game and a different game.)

---

*Working title alternatives: **Fab** · **Tapeout** · **Yield** ·
**Node** · **Wafer Thin** · **The Long Lead** · **Silicon Cycle***
