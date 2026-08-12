// Local stdio MCP server — Phase 1 (spec §8, §11).
// Tools: list_books, get_book, search, get_context.
// analyze_transcript arrives in Phase 5; Phase 3 swaps this transport for
// Streamable HTTP behind OAuth on Vercel.

import path from "node:path";
import { fileURLToPath } from "node:url";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { createClient } from "@supabase/supabase-js";
import { config } from "dotenv";
import { z } from "zod";

// Repo-root .env works from both src/ (tsx) and dist/ (node)
const here = path.dirname(fileURLToPath(import.meta.url));
config({ path: path.resolve(here, "../../.env") });

const { SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY, VOYAGE_API_KEY } = process.env;
if (!SUPABASE_URL || !SUPABASE_SERVICE_ROLE_KEY || !VOYAGE_API_KEY) {
  console.error("Missing SUPABASE_URL / SUPABASE_SERVICE_ROLE_KEY / VOYAGE_API_KEY");
  process.exit(1);
}

const sb = createClient(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY);

async function embedQuery(text: string): Promise<number[]> {
  const resp = await fetch("https://api.voyageai.com/v1/embeddings", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${VOYAGE_API_KEY}`,
    },
    body: JSON.stringify({
      model: "voyage-3.5-lite",
      input: [text],
      input_type: "query",
      output_dimension: 1024,
    }),
  });
  if (!resp.ok) throw new Error(`Voyage ${resp.status}: ${await resp.text()}`);
  const data = (await resp.json()) as { data: { embedding: number[] }[] };
  return data.data[0].embedding;
}

function asText(value: unknown) {
  return { content: [{ type: "text" as const, text: JSON.stringify(value, null, 1) }] };
}

const server = new McpServer({ name: "commonplace", version: "0.2.0" });

server.registerTool(
  "list_books",
  {
    description:
      "Full catalog of the personal book corpus, for routing. Returns a short " +
      "routing_blurb per book — use it to pick which books to search, then pass " +
      "their ids to search(). Cheap; call freely.",
    inputSchema: { domain: z.string().optional() },
  },
  async ({ domain }) => {
    let q = sb
      .from("books")
      .select("id,title,author,year,domain,tier,stance,evidence,routing_blurb")
      .order("title");
    if (domain) q = q.eq("domain", domain);
    const { data, error } = await q;
    if (error) throw new Error(error.message);
    return asText(data);
  }
);

server.registerTool(
  "get_book",
  {
    description: "Full ~300-word summary and metadata for one book.",
    inputSchema: { book_id: z.string() },
  },
  async ({ book_id }) => {
    const { data, error } = await sb
      .from("books")
      .select("*")
      .eq("id", book_id)
      .single();
    if (error) throw new Error(error.message);
    return asText(data);
  }
);

server.registerTool(
  "search",
  {
    description:
      "Semantic search over book chunks. Every result carries author and year — " +
      "always cite them; the value of this corpus is knowing WHO said a thing. " +
      "When results disagree (different stance values), name the disagreement " +
      "explicitly instead of averaging it. Default is scoped (stay within one " +
      "domain when given); wide mode crosses domains and should be called out. " +
      "Prefer routing via list_books first and passing book_ids.",
    inputSchema: {
      query: z.string(),
      book_ids: z.array(z.string()).optional(),
      domain: z.string().optional(),
      themes: z.array(z.string()).optional(),
      mode: z.enum(["scoped", "wide"]).default("scoped"),
      limit: z.number().int().positive().max(25).default(8),
    },
  },
  async ({ query, book_ids, domain, themes, mode, limit }) => {
    const embedding = await embedQuery(query);
    const { data, error } = await sb.rpc("match_chunks", {
      query_embedding: embedding,
      book_ids: book_ids ?? null,
      filter_domain: mode === "wide" ? null : domain ?? null,
      filter_themes: themes ?? null,
      match_limit: limit,
    });
    if (error) throw new Error(error.message);
    return asText(data);
  }
);

server.registerTool(
  "get_context",
  {
    description:
      "Neighboring chunks around a search result, for when a passage needs " +
      "surrounding text. window is chunks on each side (default 2).",
    inputSchema: {
      chunk_id: z.string(),
      window: z.number().int().positive().max(10).default(2),
    },
  },
  async ({ chunk_id, window }) => {
    const { data: target, error: e1 } = await sb
      .from("chunks")
      .select("book_id,seq")
      .eq("id", chunk_id)
      .single();
    if (e1) throw new Error(e1.message);
    const { data, error } = await sb
      .from("chunks")
      .select("id,seq,chapter,text,summary,themes,start_ts,end_ts")
      .eq("book_id", target.book_id)
      .gte("seq", target.seq - window)
      .lte("seq", target.seq + window)
      .order("seq");
    if (error) throw new Error(error.message);
    return asText(data);
  }
);

const transport = new StdioServerTransport();
await server.connect(transport);
console.error("commonplace MCP server ready (stdio)");
