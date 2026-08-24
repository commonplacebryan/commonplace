// Minimal stateless token machinery for the single-user OAuth server.
// Tokens are HMAC-SHA256-signed JSON payloads: base64url(payload).base64url(sig).
// No storage: possession of a validly signed, unexpired token IS the state.

import { createHmac, timingSafeEqual, createHash } from "node:crypto";
import { requireEnv } from "./tools.js";

function b64url(buf: Buffer): string {
  return buf.toString("base64url");
}

export function sign(payload: Record<string, unknown>, ttlSeconds: number): string {
  const body = { ...payload, exp: Math.floor(Date.now() / 1000) + ttlSeconds };
  const data = b64url(Buffer.from(JSON.stringify(body)));
  const sig = b64url(
    createHmac("sha256", requireEnv("TOKEN_SECRET")).update(data).digest()
  );
  return `${data}.${sig}`;
}

export function verify(token: string): Record<string, unknown> | null {
  const parts = token.split(".");
  if (parts.length !== 2) return null;
  const [data, sig] = parts;
  const expected = createHmac("sha256", requireEnv("TOKEN_SECRET"))
    .update(data)
    .digest();
  const given = Buffer.from(sig, "base64url");
  if (given.length !== expected.length || !timingSafeEqual(given, expected)) {
    return null;
  }
  try {
    const body = JSON.parse(Buffer.from(data, "base64url").toString());
    if (typeof body.exp !== "number" || body.exp < Date.now() / 1000) return null;
    return body;
  } catch {
    return null;
  }
}

export function checkPassphrase(given: string): boolean {
  const expected = Buffer.from(requireEnv("AUTH_PASSPHRASE"));
  const g = Buffer.from(given);
  // Length-equalized constant-time comparison
  const a = createHash("sha256").update(expected).digest();
  const b = createHash("sha256").update(g).digest();
  return timingSafeEqual(a, b);
}

export function s256(verifier: string): string {
  return b64url(createHash("sha256").update(verifier).digest());
}

// Only Claude's own OAuth callbacks may receive authorization codes.
const REDIRECT_ALLOWLIST = [
  "https://claude.ai/",
  "https://claude.com/",
  "https://www.claude.ai/",
  "https://www.claude.com/",
];

export function redirectAllowed(uri: string): boolean {
  return REDIRECT_ALLOWLIST.some((p) => uri.startsWith(p));
}
