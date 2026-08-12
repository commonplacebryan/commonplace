-- Stage-2 retrieval: cosine similarity over chunks, optionally scoped to
-- selected books / domain / themes (spec §4, §8). Canon tier gets a small
-- ranking boost. The MCP server calls this via RPC.

create or replace function match_chunks(
  query_embedding vector(1024),
  book_ids uuid[] default null,
  filter_domain text default null,
  filter_themes text[] default null,
  match_limit int default 10
)
returns table (
  chunk_id uuid,
  book_title text,
  author text,
  year int,
  chapter text,
  themes text[],
  start_ts int,
  stance text,
  tier text,
  chunk_text text,
  chunk_summary text,
  score float
)
language sql stable as $$
  select c.id, b.title, b.author, b.year, c.chapter, c.themes, c.start_ts,
         b.stance, b.tier, c.text, c.summary,
         1 - (c.embedding <=> query_embedding) as score
  from chunks c
  join books b on b.id = c.book_id
  where (book_ids is null or c.book_id = any(book_ids))
    and (filter_domain is null or b.domain = filter_domain)
    and (filter_themes is null or c.themes && filter_themes)
  order by (c.embedding <=> query_embedding)
           - (case when b.tier = 'canon' then 0.03 else 0 end)
  limit match_limit;
$$;
