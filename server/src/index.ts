// Local stdio entrypoint — Claude Desktop on this Mac launches this.
// The remote Streamable HTTP entrypoint lives in api/mcp.ts (Vercel).

import path from "node:path";
import { fileURLToPath } from "node:url";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { config } from "dotenv";
import { buildServer } from "./tools.js";

// Repo-root .env works from both src/ (tsx) and dist/ (node)
const here = path.dirname(fileURLToPath(import.meta.url));
config({ path: path.resolve(here, "../../.env") });

const transport = new StdioServerTransport();
await buildServer().connect(transport);
console.error("commonplace MCP server ready (stdio)");
