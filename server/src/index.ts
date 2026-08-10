// Local stdio MCP server — Phase 1 (spec §8, §11).
// Tools: list_books, search, get_context; analyze_transcript arrives in Phase 5.
// Phase 3 swaps the transport for Streamable HTTP behind OAuth on Vercel.

import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const server = new McpServer({ name: "commonplace", version: "0.1.0" });

server.registerTool(
  "list_books",
  {
    description:
      "Full catalog for stage-1 routing. Returns routing blurbs, not full summaries. Cheap; call freely.",
    inputSchema: { domain: z.string().optional() },
  },
  async () => {
    throw new Error("not implemented — Phase 1");
  }
);

server.registerTool(
  "search",
  {
    description:
      "Vector search within selected books. Every result carries author and year — citations are not optional. Default scoped to one domain; wide mode is opt-in.",
    inputSchema: {
      query: z.string(),
      book_ids: z.array(z.string()).optional(),
      domain: z.string().optional(),
      themes: z.array(z.string()).optional(),
      mode: z.enum(["scoped", "wide"]).default("scoped"),
      limit: z.number().int().positive().default(10),
    },
  },
  async () => {
    throw new Error("not implemented — Phase 1");
  }
);

server.registerTool(
  "get_context",
  {
    description: "Neighboring chunks around a result that needs surrounding text.",
    inputSchema: {
      chunk_id: z.string(),
      window: z.number().int().positive().default(2),
    },
  },
  async () => {
    throw new Error("not implemented — Phase 1");
  }
);

const transport = new StdioServerTransport();
await server.connect(transport);
