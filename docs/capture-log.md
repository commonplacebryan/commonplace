# Capture log

Source of truth for loaded books is the database; this ledger adds capture
notes and pending work. Update when books load.

## Loaded (60 books, 7,647 chunks — as of 2026-09-14)

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
| 51 | The Mom Test | Rob Fitzpatrick | 2013 | entrepreneurship | 81 | loaded 2026-09-14 |
| 52 | $100M Offers | Alex Hormozi | 2021 | marketing_gtm | 82 | |
| 53 | The Founder's Dilemmas | Noam Wasserman | 2012 | entrepreneurship | 218 | |
| 54 | Empowered | Marty Cagan & Chris Jones | 2020 | product | 205 | |
| 55 | Think Again | Adam Grant | 2021 | decision_judgment | 126 | |
| 56 | Transformed | Marty Cagan | 2024 | product | 172 | |
| 57 | Blitzscaling | Reid Hoffman & Chris Yeh | 2018 | entrepreneurship | 146 | |
| 58 | Build | Tony Fadell | 2022 | product | 188 | |
| 59 | Competing Against Luck | Clayton M. Christensen | 2016 | product | 128 | |
| 60 | Predictably Irrational | Dan Ariely | 2008 | decision_judgment | 132 | |

Outstanding recommendations still un-captured (as of 2026-09-14):
**Inspired** (Cagan — the foundational product book; Bryan has Empowered
+ Transformed but not this), **The Psychology of Money** (Housel), and
**Leadership & Self-Deception** (PARKED — retired-edition Audible issue,
Bryan removed it from his library to sort out later). Empowered (54) and
Transformed (56) were bonus captures, not on the rec list.
Full owned library now at docs/owned-library.csv (809 titles).

SPEED AUDIT (2026-09-15): checked recorded-duration vs real Audible runtime
across the corpus. Only **Supercommunicators** (book 30) was recorded at
1.5x — needs re-capture at 1x + reload. **Psychology of Money** also caught
at 1.5x before loading (Bryan re-recording). All other loaded books
confirmed 1x. Detection: wpm screen (flag >185/min) then runtime cross-check
(1.5x capture = 2/3 real runtime); wpm alone false-positives on fast
narrators (Hormozi, Mom Test all verified 1x).

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
| 30 | Supercommunicators | Charles Duhigg | 2024 | leadership | 124 | ⚠️ RECORDED AT 1.5x (5.0h vs 7h28m real) — degraded transcription; RE-CAPTURE at 1x and reload |
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
