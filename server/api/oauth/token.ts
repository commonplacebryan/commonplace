// Token endpoint: authorization_code (with PKCE verification) and
// refresh_token grants. Access tokens last 30 days, refresh tokens 180.

import type { VercelRequest, VercelResponse } from "@vercel/node";
import { s256, sign, verify } from "../../src/auth.js";

const AT_TTL = 30 * 24 * 3600;
const RT_TTL = 180 * 24 * 3600;

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
  const body = (req.body ?? {}) as Record<string, string>;

  if (body.grant_type === "authorization_code") {
    const claims = verify(body.code ?? "");
    if (!claims || claims.t !== "code") {
      res.status(400).json({ error: "invalid_grant" });
      return;
    }
    if (!body.code_verifier || s256(body.code_verifier) !== claims.ch) {
      res.status(400).json({ error: "invalid_grant", error_description: "PKCE failed" });
      return;
    }
    if (body.redirect_uri && body.redirect_uri !== claims.ru) {
      res.status(400).json({ error: "invalid_grant", error_description: "redirect_uri mismatch" });
      return;
    }
    res.json({
      access_token: sign({ t: "at" }, AT_TTL),
      token_type: "Bearer",
      expires_in: AT_TTL,
      refresh_token: sign({ t: "rt" }, RT_TTL),
    });
    return;
  }

  if (body.grant_type === "refresh_token") {
    const claims = verify(body.refresh_token ?? "");
    if (!claims || claims.t !== "rt") {
      res.status(400).json({ error: "invalid_grant" });
      return;
    }
    res.json({
      access_token: sign({ t: "at" }, AT_TTL),
      token_type: "Bearer",
      expires_in: AT_TTL,
      refresh_token: sign({ t: "rt" }, RT_TTL),
    });
    return;
  }

  res.status(400).json({ error: "unsupported_grant_type" });
}
