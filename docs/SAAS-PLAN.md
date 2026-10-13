# The SaaS: from chronology research to finished films

*Working draft, 13 October 2026. Working name: **Rogue Chronicon** (placeholder until you pick one).*

## In one sentence

A subscription workspace where a researcher puts dates into the Chronicon's clocks and cycles, runs them through the
Ophis projection engine, and turns what they find into a captioned, voiced short film, all in one place.

## What already exists

Most of the product is built. It sits in eight repos that don't talk to each other yet.

| Piece | Repo | State | License today |
|---|---|---|---|
| **Chronicon Desk**: 30 live clocks, a 7-lane timeline, the 138 wheel, 105 events, 43 witnesses, Nemesis X / Nibiru | `chronicon-desk` (new, local only) | Built; portable `.exe` 0.1.0 | none yet |
| **Ophis rebuild**: date-projection engine, bit-exact against v12 | `natori-on-psyfr` | Built, tested, live on Pages | CC BY-NC-SA 4.0 |
| **Natorion Cipher**: Ophis joined to the Chronicon clocks, plus a Studio that writes a documentary production package from the numbers | `NatorionCipherPredictiveEngine/natorion` | Built, live on Pages | CC BY-NC-SA 4.0 |
| **Rogue Walker Studio**: Claude skills that turn clips into finished films (walker reels, captioner, ArtCraft → FilmCraft director) | `rogue-walker-studio` | v1.4.0 released | source-available, no resale |
| **Phoenix Chronicles**: station sheets, transcripts, film generators (Remotion, audio) | `phoenix-chronicles-tools` | Production archive | MIT |
| **Chronotecture atlas**: 119 plates + interactive redesigns | `Chronotecture-Charts` | **Private on purpose** (scans of Breshears' charts) | not yours to publish |
| Finished films: *The Deposition*, *The Engineered Sky*, Ere-We-Were stations, shorts | Desktop / Higgsfield | Proof of output | — |

The gap is not features. It's **one account, one data model, and payment**.

## Decision #1, before anything is sold: rights

The Chronicon, its dates and cycles, the Ophis method and the Chronotecture charts are **Jason M. Breshears' work**.
Your repos say the Ophis teardown was done with the owner's permission for a portfolio write-up. That permission does
not cover selling access. Your own rebuilds are licensed CC BY-NC-SA, which is non-commercial.

Selling this needs **written permission from Breshears for commercial use**. Three ways to structure that:

1. **Licensed partner.** A revenue share or flat fee for the method and the data. Cleanest; probably the best product.
2. **Official tool.** Build it for him or with him, under his brand. You get paid for the build and maintenance.
3. **Method-free.** Sell only what is yours: the film pipeline, the clocks engine as generic calendar math, and
   user-entered timelines. Strip the Chronicon dataset and the Ophis operations. Weaker, but needs no one's permission.

Nothing below should launch before this is settled. Free, non-commercial sharing can continue as it does now.

## Who pays

| Who | What they want | What they'd pay for |
|---|---|---|
| **Chronicon / Archaix readers** (the existing audience for the books and channel) | The clocks, the cycles and projections on their own dates | Saved timelines, projections, alerts on cycle days |
| **Alt-history and mystery creators** (YouTube, TikTok) | Turn a date chain into a video fast | The research → script → film pipeline |
| **AI-film creators** with piles of clips | Finished, captioned, voiced films | The walker / director pipeline, done-for-you reels |

## The product

Four modules sharing one account and one data model: **dates, events, cycles, projects**.

1. **Desk.** The Chronicon Desk views (clocks, timeline, wheel, events, witnesses, bodies). Users add their own
   events and witnesses beside the reference set, so every entry carries the same `source` field the data has now.
2. **Engine.** Ophis projections from any selection of events on the timeline. Results drop back onto the timeline
   as a lane.
3. **Studio.** Natorion's production-package writer, fed from a selection: beats, script, shot sheet, captions, look.
   Exports a `cutsheet.json` in the rogue-ai format.
4. **Cut.** The rogue-ai / walker-reel pipeline turns the cutsheet and the user's clips into a finished film. Rendering
   runs on the user's machine (FilmCraft headless) or as a paid render job.

**Trust rule, kept from the desktop app:** source conflicts are shown, not smoothed over (the Source Notes tab).
Projections are sold as a **research and storytelling tool, not as predictions**. Wording in the app, pricing page
and ads must not promise that events will happen. This is both honest and a consumer-protection requirement.

## Plans (proposed; prices echo your 19/138 house style)

| Plan | Price | Includes |
|---|---|---|
| **Free** | $0 | Desktop `.exe` and web Desk, read-only reference set, live clocks |
| **Researcher** | $13.80 / mo | Own events and witnesses, saved timelines, Ophis projections, cycle-day alerts, CSV/PDF export |
| **Creator** | $27.60 / mo | Researcher + Studio packages + cutsheet export + local Cut pipeline + 2 render jobs/mo |
| **Services** | from `SALES.md` | $138 setup · $276 custom look · from $190 per done-for-you reel · $69/mo support |

**Paid AI generation (ArtCraft, Higgsfield, ElevenLabs) stays on the user's own account (bring your own key).** The
service never holds credits or resells generation. That keeps costs predictable and avoids reselling someone else's
API, and it follows the rule the kit already has: stop before every paid generate.

## Architecture

The desktop app was built so the same code serves the web.

```text
React app (chronicon-desk/src) ──┬── Electron shell → portable .exe   (offline, Free tier)
                                 └── Web (Vite build on static hosting)
                                        │
                     Supabase: Auth · Postgres (users' events, timelines, projects) · Storage (cutsheets)
                                        │
                     Stripe: Checkout + customer portal → plan flag on the Supabase user
                                        │
                     Render jobs (Creator): queue → a worker running filmcraft-cli headless → signed download
```

- **Reference data** (`clocks.json`, `phoenix.json`) ships with the app and is versioned in git. User data never
  mixes into it; it lives in Postgres with row-level security per user.
- **Engine** stays client-side (the Ophis rebuild has no dependencies and runs in the browser). Cheap to host, and
  a user's dates never leave their device unless they save them.
- **Render worker** is the only server-side compute. Start with one Windows box running FilmCraft. The rogue-ai skill
  already builds a cut headless in about 2.5 minutes for 138 s of film.

## Roadmap

| Phase | Ships | Done when |
|---|---|---|
| **0 · Rights** | Written agreement with Breshears, or the method-free decision | Signed, or scope cut |
| **1 · Desk on the web** | Chronicon Desk at a URL; Free tier; same build as the `.exe` | Loads in a browser, no login |
| **2 · Accounts** | Supabase auth, own events and witnesses, saved timelines | A user's own event appears on the timeline after reload |
| **3 · Engine** | Ophis projections from a timeline selection, as a lane | Parity test against v12 still passes inside the app |
| **4 · Billing** | Stripe checkout, Researcher plan | A test-mode purchase unlocks Researcher |
| **5 · Studio + Cut** | Package writer → cutsheet → local cut; Creator plan | A cutsheet from the app renders with `rogue_cut.py` |
| **6 · Render jobs** | Hosted FilmCraft worker | A Creator job returns a film without the user installing anything |

## Open decisions for you

1. **Rights path:** licensed partner, official tool, or method-free.
2. **Name:** "Rogue Chronicon" is a placeholder.
3. **Where Chronicon Desk lives:** new public repo, private repo, or folded into `NatorionCipherPredictiveEngine`.
4. **Source conflicts:** 32 are listed in the app's Source Notes tab (Phoenix numbering, AM 0 vs AM 1, 15/16/17 May
   2040, off-by-one BC years). Ruling on them makes the reference set authoritative.
5. **Code signing:** the `.exe` is unsigned. A certificate (about $200–400/yr) removes the SmartScreen warning before
   paying customers see it.
