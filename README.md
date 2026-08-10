# Commonplace

A private, queryable knowledge base built from owned audiobooks and ebooks —
named after the historical commonplace book. Audio from legitimate playback is
transcribed locally, chunked on semantic boundaries, tagged against a
controlled theme vocabulary, embedded, and stored in Postgres. An MCP server
exposes the corpus to Claude for coaching questions, cited retrieval, and
sales-call analysis.

Spec: `commonplace-spec.pdf` (V3). Purpose is **retention, not substitution** —
a recall layer on top of real reading.

## Constraints (non-negotiable)

- **No DRM circumvention.** Audio comes from normal playback capture only.
- **Personal use only.** Transcripts and chunks never leave private infrastructure.
- **Owned material only.**
- Raw audio and transcripts are never committed to this repo (see `.gitignore`).

## Architecture

Two-stage retrieval: a query first routes to 6–10 relevant books via short
routing blurbs (`list_books()`), then vector search runs only within the
selected books. Domains partition books hard; themes cut across them at the
chunk level.

```
pipeline/   Python — transcribe (mlx-whisper), chunk, tag (Haiku),
            summarize (Sonnet), embed (Voyage), load
server/     TypeScript MCP server — local stdio first, Vercel later
supabase/   Database migrations (Postgres + pgvector)
vocab/      Controlled theme vocabulary (shared by tagging and call analysis)
```

## Build phases

1. **Prove the loop** — one book end to end, queried through a local MCP server
2. **Schema and vocabulary** — lock decisions against four real books
3. **Remote MCP** — Vercel + OAuth, added as a Claude custom connector
4. **Domains and routing at scale**
5. **Call transcript analysis** — `analyze_transcript()`

## Setup

```sh
# Pipeline (Python 3.11+, Apple Silicon for mlx-whisper)
cd pipeline && python3 -m venv .venv && .venv/bin/pip install -e .

# Server (Node 20+)
cd server && npm install

# Environment
cp .env.example .env   # then fill in keys
```

## Accounts

Everything runs under dedicated project accounts (GitHub `commonplacebryan`,
plus separate Supabase, Vercel, Anthropic Console, and Voyage accounts) —
never personal ones. Querying runs on the Claude subscription; ingestion runs
on the Anthropic API; embeddings on Voyage.
