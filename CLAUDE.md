# Commonplace — working context

Queryable personal knowledge base over Bryan's owned audiobook library.
Spec: `~/Downloads/commonplace-spec.pdf` (V3). Target: 250+ books. Purpose is
retention, not substitution — a recall layer over real reading/listening.

## Non-negotiable constraints

- **No DRM circumvention, ever.** Audio comes from Audio Hijack capturing
  legitimate Audible playback. Never suggest or use DRM-removal tools.
- **Personal use, single user.** No sharing access, no charging, corpus serves
  only Bryan. (His passphrase gates the remote server; it is not shared.)
- **Never commit:** `.env`, audio, `data/` (transcripts/chunks). Only
  `.env.example` is tracked. Audit confirmed clean 2026-08-31.
- Dedicated accounts, all under the commonplace Google identity: GitHub
  `commonplacebryan` (SSH alias `github-commonplace`), Supabase, Vercel
  (team `commonplace4`), Anthropic Console, Voyage. Git identity is repo-local.

## Architecture

Two-stage retrieval: route via short `routing_blurb`s (`list_books`), then
vector-search within chosen books (`match_chunks` RPC, HNSW, 1024-dim
voyage-3.5-lite). Domains hard-partition books; ~45 glossed themes
(vocab v2) cut across them. `books.summary` (~300w) is separate from
`routing_blurb` (1–2 sentences) — the blurb is what routing reads.

- `pipeline/` Python 3.12, venv at `pipeline/.venv`. Stages:
  `transcribe → stitch → chunk → tag → summarize → embed → load`
- `server/` TypeScript MCP server. `src/tools.ts` is shared by the local
  stdio entrypoint (`src/index.ts`, wired into Claude Desktop) and the
  remote Vercel endpoint (`api/mcp.ts` + OAuth in `api/oauth/`).
- Remote MCP (live): `https://commonplace-commonplace4.vercel.app/api/mcp`,
  single-user OAuth (passphrase = `AUTH_PASSPHRASE` in `.env`).
  Deploy: `cd server && vercel deploy --prod --token $VERCEL_TOKEN`.
- DB: Supabase `cxmtxsolltackzlhengp`, migrations in `supabase/migrations/`
  (`supabase db push` with env from `.env`).

## Processing a captured book (the runbook)

```sh
V=./pipeline/.venv/bin/commonplace
$V transcribe "<mp3>" --out-dir data/transcripts/<slug>   # one call per hour-file
$V stitch data/transcripts/<slug> --slug <slug> --title "<Title>"
$V chunk data/books/<slug>.json
$V tag data/chunks/<slug>.json
$V summarize data/chunks/<slug>.tagged.json
$V embed data/chunks/<slug>.tagged.json
$V load data/chunks/<slug>.final.json --author "<A>" --year <Y> --domain <d>
```

Domains in use: `sales`, `sales_management`, `leadership`, `marketing_gtm`.
Planned: `entrepreneurship`, `product`, `self`, `decision_judgment`, `faith`
(faith is confirmed in-scope, hard-partitioned). Tier: all `standard` so far;
`canon` gets a small ranking boost — promotion is a future curation pass.
Re-load of an existing title replaces it wholesale (safe to re-run).

## Capture operations (hard-won knowledge)

- Audio Hijack session: source = Audible app, MP3 128kbps mono VBR, 60-min
  file splits, output `~/Music/Audio Hijack`. 1x speed always.
- **Stop-before-play** when switching books, else the new book's opening
  lands in the old book's final file (fixable by ffmpeg trim, but avoid).
- Sessions never auto-stop; the recorder just goes silent at book end.
  Run `caffeinate -dims -t <secs>` detached (nohup) during captures.
- **The Audible app (post-Aug-2026 update) lies.** It loses playback
  positions, shows wrong remaining time, and silently stops playback.
  Never trust its display or session timers — verify by sampling the
  capture tail with mlx_whisper: a finished book ends with outro credits
  ("Audible hopes you have enjoyed this program").
- Retired-edition titles that won't play in the Mac app: open the library
  on audible.com in a browser; that re-syncs licenses and fixes the app.
- Runtime estimates from memory have been wrong repeatedly (Sales EQ ~14h
  not 9h; Influence expanded ~21h not 16h). The tape is the only truth.
- Interrupted/replayed captures are repairable at transcript level:
  transcribe both sets, find the cut sentence via normalized 12-word match
  (fall back to fuzzy), trim overlap segments, stitch merged dir. Detect
  suspected internal replays with an 8-word shingle scan before assuming
  duplication — author-read books legitimately repeat phrases.
- Sweep discipline: list the ENTIRE capture folder when looking for
  unprocessed sessions (a head-limited listing once hid a week of books).
  Group files by their minute signature (sessions roll files hourly).

## Vocabulary rules

`vocab/themes.json` v2: 45 themes with `$glosses` (the tag prompt shows
"name — gloss"; tagging rejects off-list themes). Additions are schema
changes — batch them, don't drift. Re-tag procedure preserving embeddings:
re-run `tag`, merge new themes/summaries into `<slug>.final.json` by seq,
re-run `load` (embeddings ride along; nothing re-embeds).

## Costs / limits

- Voyage has no payment method: embed uses token-aware batches ≤5.5K est.
  tokens, 45s pacing, resume-from-checkpoint. Adding a card lifts limits
  at no cost (200M free tokens still apply).
- Supabase free tier (500MB) is fine to ~100+ books; switch `embedding` to
  `halfvec(1024)` if storage pinches at scale.
- Ingestion ~$0.50–1/book (Haiku tags + one Sonnet summary).

## State ledger

`docs/capture-log.md` = what's loaded and what's pending (keep it updated
when books load). `docs/library-triage.md` = the 250-book plan and tags.
The database itself is the source of truth for loaded books.
