# Semi Tycoon Simulator

Semiconductor-executive tycoon game. RollerCoaster Tycoon from the factory floor,
Civilization only for the rivalry.

Live: https://semitycoon.borgorg.org

| Path | What |
|---|---|
| `site/design/` | Interactive design explorer — mechanics, cycle toy, segments |
| `site/mockups/` | 13-beat gameplay storyboard, isometric UI mockups |
| `site/demo/` | **Playable prototype** — the line, defects, the world, field failures |
| `docs/DESIGN.md` | Design bible |
| `docs/UI.md` | World & interface doc (RCT layer + rivalry layer) |

## The thesis

A fab takes four years to build. A chip takes three years to design. By the time
any decision pays off, the world that justified it is gone.

## The demo's loop

Three levers — test coverage, maintenance, output rate. Defects are born from your
own choices, flow through the line, and whatever escapes test ships into the world
and lives there until it fails in the field. The log names the decision that did it.

## Deploy

Static files served by nginx (`semitycoon-web`) on `shared_network`, proxied by
Caddy in `automagica-infra`. No build step — edit and reload.
