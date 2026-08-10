-- Commonplace initial schema (spec §5, with review amendments:
-- HNSW instead of ivfflat, routing_blurb split from summary, asin column)

create extension if not exists vector;

create table books (
  id            uuid primary key default gen_random_uuid(),
  title         text not null,
  author        text not null,
  year          int,
  domain        text not null,        -- hard partition; see spec §4
  asin          text unique,          -- Audible/Amazon id; seeds from library export
  summary       text,                 -- ~300 words; ingest-time, full detail
  routing_blurb text,                 -- 1-2 sentences; what list_books() returns
  stance        text check (stance in ('consultative','volume','research','motivational')),
  evidence      text check (evidence in ('data-backed','practitioner','anecdotal')),
  tier          text not null default 'standard'
                     check (tier in ('canon','standard','archive')),
  source_type   text check (source_type in ('audio','kindle_highlights','epub','manual')),
  created_at    timestamptz not null default now()
);

create table chunks (
  id         uuid primary key default gen_random_uuid(),
  book_id    uuid not null references books(id) on delete cascade,
  chapter    text,
  seq        int not null,
  text       text not null,
  summary    text,                    -- one line, generated at ingest
  themes     text[] not null default '{}',  -- controlled vocabulary only
  start_ts   int,                     -- seconds; audio sources only
  end_ts     int,
  embedding  vector(1024),            -- voyage-3.5-lite @ 1024 dims
  created_at timestamptz not null default now(),
  unique (book_id, seq)
);

-- HNSW: builds incrementally as books are added, unlike ivfflat which
-- degrades unless retrained after the corpus grows
create index chunks_embedding_idx on chunks using hnsw (embedding vector_cosine_ops);
create index chunks_themes_idx    on chunks using gin (themes);
create index chunks_book_id_idx   on chunks (book_id);
create index books_domain_idx     on books (domain);

-- Single-tenant today, but cheap now and painful to retrofit (spec §10).
-- No policies defined: the MCP server connects with the service-role key.
alter table books  enable row level security;
alter table chunks enable row level security;
