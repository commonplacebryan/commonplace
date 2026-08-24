// Dynamic client registration (RFC 7591), single-user edition: every
// registrant gets the same public client id. Authorization still requires
// the owner's passphrase, so open registration grants nothing by itself.

import type { VercelRequest, VercelResponse } from "@vercel/node";

export default function handler(req: VercelRequest, res: VercelResponse) {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Headers", "content-type");
  if (req.method === "OPTIONS") {
    res.status(204).end();
    return;
  }
  if (req.method !== "POST") {
    res.status(405).json({ error: "method not allowed" });
    return;
  }
  const body = (req.body ?? {}) as Record<string, unknown>;
  res.status(201).json({
    client_id: "commonplace-client",
    token_endpoint_auth_method: "none",
    redirect_uris: body.redirect_uris ?? [],
    client_name: body.client_name ?? "client",
  });
}
