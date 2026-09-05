# Capture log

Source of truth for loaded books is the database; this ledger adds capture
notes and pending work. Update when books load.

## Loaded (50 books, 6,169 chunks — as of 2026-09-04)

Books 32–42 (loaded 2026-08-31 overnight batch):

| # | Title | Author | Year | Domain | Chunks | Notes |
|---|-------|--------|------|--------|--------|-------|
| 32 | No Rules Rules | Hastings & Meyer | 2020 | leadership | 147 | |
| 33 | Decisive | Heath & Heath | 2013 | decision_judgment | 151 | new domain |
| 34 | The Lean Startup | Eric Ries | 2011 | entrepreneurship | 143 | new domain |
| 35 | Made to Stick | Heath & Heath | 2007 | marketing_gtm | 134 | |
| 36 | Thinking in Bets | Annie Duke | 2018 | decision_judgment | 118 | |
| 37 | The Innovator's Dilemma | Clayton Christensen | 1997 | product | 124 | new domain |
| 38 | The Ideal Team Player | Patrick Lencioni | 2016 | leadership | 80 | |
| 39 | The Hard Thing About Hard Things | Ben Horowitz | 2014 | entrepreneurship | 137 | |
| 40 | Measure What Matters | John Doerr | 2018 | leadership | 124 | |
| 41 | Deep Work | Cal Newport | 2016 | self | 111 | new domain |
| 42 | Radical Candor | Kim Scott | 2019 | leadership | 172 | 2 sessions, zero-gap seam — no splice needed |
| 43 | The Effective Executive | Peter F. Drucker | 1967 | leadership | 113 | loaded 2026-09-01 |
| 44 | Start with Why | Simon Sinek | 2009 | leadership | 131 | loaded 2026-09-03 |
| 45 | The Next Conversation | Jefferson Fisher | 2025 | leadership | 108 | loaded 2026-09-03 |
| 46 | The Anatomy of Peace | The Arbinger Institute | 2006 | leadership | 112 | loaded 2026-09-03; retired-edition, fixed via web re-sync |
| 47 | Atomic Habits | James Clear | 2018 | self | 114 | loaded 2026-09-03 |
| 48 | Zero to One | Peter Thiel & Blake Masters | 2014 | entrepreneurship | 81 | loaded 2026-09-04 |
| 49 | The Outward Mindset | The Arbinger Institute | 2016 | leadership | 72 | loaded 2026-09-04; completes Arbinger trilogy |
| 50 | Objections | Jeb Blount | 2018 | sales | 100 | loaded 2026-09-04; full re-record after Audible silent-stop |

**Leadership & Self-Deception**
recorded fully silent Sep 2→3 (retired-edition license lapsed). Bryan
removed it from his library 2026-09-04 to sort out later — PARKED, revisit
when the edition works. The Mom Test (Fitzpatrick) capturing 2026-09-04
evening → book 51.

## Previously loaded (books 1–31, as of 2026-08-31 morning)

| # | Title | Author | Year | Domain | Chunks | Notes |
|---|-------|--------|------|--------|--------|-------|
| 1 | Freemium | Dave Boyce | 2024 | marketing_gtm | 151 | first book; proved the loop |
| 2 | The Sales Acceleration Formula | Mark Roberge | 2015 | sales_management | 90 | |
| 3 | The Qualified Sales Leader | John McMahon | 2021 | sales_management | 138 | |
| 4 | Cracking the Sales Management Code | Jordan & Vazzana | 2012 | sales_management | 113 | |
| 5 | The Challenger Sale | Dixon & Adamson | 2011 | sales | 105 | |
| 6 | Gap Selling | Keenan | 2018 | sales | 117 | |
| 7 | Who: The A Method for Hiring | Smart & Street | 2008 | leadership | 76 | |
| 8 | Fanatical Prospecting | Jeb Blount | 2015 | sales | 148 | |
| 9 | Never Split the Difference | Chris Voss | 2016 | sales | 141 | |
| 10 | Crucial Conversations (3rd ed) | Grenny et al. | 2021 | leadership | 134 | |
| 11 | High Output Management | Andy Grove | 1983 | leadership | 125 | |
| 12 | Exactly What to Say | Phil M. Jones | 2017 | sales | 23 | shortest book |
| 13 | Sales EQ | Jeb Blount | 2017 | sales | 235 | spliced from 2 captures (Audible position bug) |
| 14 | Good to Great | Jim Collins | 2001 | leadership | 153 | |
| 15 | The Sales Development Playbook | Trish Bertuzzi | 2016 | sales_management | 115 | |
| 16 | Obviously Awesome | April Dunford | 2019 | marketing_gtm | 55 | |
| 17 | Cold Calling Sucks | Farrokh & Cegelski | 2024 | sales | 81 | |
| 18 | Multipliers | Liz Wiseman | 2010 | leadership | 172 | |
| 19 | Pitch Anything | Oren Klaff | 2011 | sales | 115 | |
| 20 | The First 90 Days | Michael D. Watkins | 2003 | leadership | 108 | |
| 21 | Coaching Salespeople into Sales Champions | Keith Rosen | 2008 | sales_management | 187 | |
| 22 | SPIN Selling | Neil Rackham | 1988 | sales | 111 | |
| 23 | Amp It Up | Frank Slootman | 2022 | sales_management | 87 | missing first ~seconds (late session start); optional patch |
| 24 | The Challenger Customer | Adamson, Dixon, et al. | 2015 | sales | 123 | |
| 25 | Crossing the Chasm | Geoffrey A. Moore | 1991 | marketing_gtm | 135 | |
| 26 | Extreme Ownership | Willink & Babin | 2015 | leadership | 126 | |
| 27 | The JOLT Effect | Dixon & McKenna | 2022 | sales | 104 | missing first seconds (dual-narrator front matter) |
| 28 | Influence (New & Expanded) | Robert B. Cialdini | 2021 | sales | 249 | author-read, ~21h, largest book |
| 29 | $100M Leads | Alex Hormozi | 2023 | sales | 136 | |
| 30 | Supercommunicators | Charles Duhigg | 2024 | leadership | 124 | |
| 31 | Turn the Ship Around! | L. David Marquet | 2012 | leadership | 120 | |

## Other pending

- Radical Candor loaded (book 42) — obsolete partial can now be deleted:
  `data/transcripts/radical-candor-partial` + mp3s `20260814 2153/2253/2353`.
- **Queue**: next ~21 books listed in chat 2026-08-25 (Objections, Ideal
  Team Player, Anatomy of Peace, Made to Stick, $100M Offers, Lean Startup,
  Zero to One, Mom Test, Hard Thing, Measure What Matters, Innovator's
  Dilemma, Competing Against Luck, Thinking in Bets, Decisive, Start with
  Why, No Rules Rules, Leadership & Self-Deception, Next Conversation,
  Atomic Habits, Deep Work, Outward Mindset) — see also
  `docs/library-triage.md` for the full 250-book plan.
- **`~/Music/Audio Hijack/autoplay-overflow/`**: quarantined files from the
  first night's autoplay accident — contains a partial Four Steps to the
  Epiphany (owned; potentially usable someday) — plus an Audible Original.
- Canon-tier promotions not yet made (⭐ candidates in library-triage.md).
- Phase 5 (`analyze_transcript` call analysis) not started.

## Vocabulary history

- v1 (39 themes) shipped with book 1.
- v2 (2026-08-21, 45 themes): retired `sales_process` (had become a 25%
  catch-all across 9/10 books) → `sales_methodology` / `funnel_design` /
  `process_management`; split `onboarding` → `rep_onboarding` +
  `customer_onboarding`; added `marketing_gtm` block; dropped unused
  `discounting`. All books re-tagged; embeddings preserved.
- Glosses added 2026-08-21 after `positioning` over-applied (417 chunks
  corpus-wide → 9 on the first glossed book). Books 1–19 were tagged
  pre-gloss; re-tag only if positioning noise shows up in real queries.
