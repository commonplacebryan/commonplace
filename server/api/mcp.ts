// Remote MCP endpoint — Streamable HTTP, stateless (one transport per
// request), bearer-token-gated. Claude reaches this from Anthropic's cloud
// as a custom connector; the token comes from the OAuth flow in api/oauth/.

import type { VercelRequest, VercelResponse } from "@vercel/node";
import { StreamableHTTPServerTransport } from "@modelcontextprotocol/sdk/server/streamableHttp.js";
import { verify } from "../src/auth.js";
import { buildServer } from "../src/tools.js";

export default async function handler(req: VercelRequest, res: VercelResponse) {
  const auth = req.headers.authorization ?? "";
  const token = auth.startsWith("Bearer ") ? auth.slice(7) : "";
  const claims = token ? verify(token) : null;
  if (!claims || claims.t !== "at") {
    res
      .status(401)
      .setHeader(
        "WWW-Authenticate",
        `Bearer resource_metadata="https://${req.headers.host}/.well-known/oauth-protected-resource"`
      )
      .json({ error: "unauthorized" });
    return;
  }

  if (req.method !== "POST") {
    // Stateless mode: no SSE stream to resume, no session to delete
    res.status(405).json({ error: "method not allowed" });
    return;
  }

  const transport = new StreamableHTTPServerTransport({
    sessionIdGenerator: undefined,
    enableJsonResponse: true,
  });
  const server = buildServer();
  await server.connect(transport);
  await transport.handleRequest(req, res, req.body);
}
