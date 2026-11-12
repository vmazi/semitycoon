# Kill Your Own Semiconductor Company Simulator

You run a chip company for forty years. Most people kill it.

RollerCoaster Tycoon from the factory floor, Civilization only for the rivalry.
Vanilla JS and a 2D canvas, no build step.

**Play: https://semitycoon.borgorg.org**

| Path | What |
|---|---|
| `site/demo/` | **The game** — served at the site root |
| `site/design/` | Interactive design explorer — mechanics, cycle toy, segments |
| `site/mockups/` | 13-beat gameplay storyboard, isometric UI mockups |
| `site/about/` | Landing page |
| `docs/DESIGN.md` | Design bible |
| `docs/UI.md` | World & interface doc (RCT layer + rivalry layer) |

## The thesis

A fab takes four years to build. A chip takes three years to design. By the time
any decision pays off, the world that justified it is gone.

## The loop

Five eras — mainframe, PC, networking, mobile, cloud. Each goes to whoever holds the
most of that era's market by value when it ends; most points after five eras wins.
Sometimes the right move is to concede an era to be built for the next one.

You never set the plant by hand. **Quarterly scenarios** force a choice four times an
era, **ad-hoc actions** spend capital for an immediate effect, and **generational
planning** between eras spends a limited pick budget on what you will be good at
later. Capital gates the ad-hoc layer, placement feeds the pick budget, and some
scenarios hand you budget now for a backlash that lands two or three quarters out.

Underneath, defects are born from those choices, flow through the line, and whatever
escapes test ships into the world and lives there until it fails in the field. The
log names the decision that did it.

## Deploy

Static files served by nginx (`semitycoon-web`) on `shared_network`, proxied by
Caddy in `automagica-infra`. No build step — edit and reload.
