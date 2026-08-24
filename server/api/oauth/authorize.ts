// Authorization endpoint. GET renders a passphrase form (the owner is the
// only user); POST verifies the passphrase and redirects back to Claude
// with a short-lived signed code carrying the PKCE challenge.

import type { VercelRequest, VercelResponse } from "@vercel/node";
import { checkPassphrase, redirectAllowed, sign } from "../../src/auth.js";

function esc(s: string): string {
  return s.replace(/[&<>"']/g, (c) =>
    ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]!)
  );
}

export default function handler(req: VercelRequest, res: VercelResponse) {
  const q = (req.method === "POST" ? req.body : req.query) as Record<string, string>;
  const { redirect_uri, state, code_challenge, code_challenge_method } = q;

  if (!redirect_uri || !redirectAllowed(redirect_uri)) {
    res.status(400).send("invalid redirect_uri");
    return;
  }
  if (code_challenge_method !== "S256" || !code_challenge) {
    res.status(400).send("PKCE S256 required");
    return;
  }

  if (req.method === "POST") {
    if (!checkPassphrase(q.passphrase ?? "")) {
      res.status(200).send(page(q, "Wrong passphrase — try again."));
      return;
    }
    const code = sign({ t: "code", ch: code_challenge, ru: redirect_uri }, 300);
    const target = new URL(redirect_uri);
    target.searchParams.set("code", code);
    if (state) target.searchParams.set("state", state);
    res.status(302).setHeader("Location", target.toString()).end();
    return;
  }
  res.status(200).setHeader("Content-Type", "text/html").send(page(q, ""));
}

function page(q: Record<string, string>, notice: string): string {
  const hidden = ["redirect_uri", "state", "code_challenge", "code_challenge_method"]
    .filter((k) => q[k])
    .map((k) => `<input type="hidden" name="${k}" value="${esc(q[k])}">`)
    .join("\n");
  return `<!doctype html>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Commonplace</title>
<body style="font-family: system-ui; max-width: 22rem; margin: 15vh auto; padding: 0 1rem; color: #1F2823;">
  <h1 style="font-size: 1.3rem;">Commonplace</h1>
  <p>Claude is requesting access to your book corpus. Enter your passphrase to allow it.</p>
  ${notice ? `<p style="color: #8C3226;">${esc(notice)}</p>` : ""}
  <form method="POST">
    ${hidden}
    <input type="password" name="passphrase" autofocus
           style="width: 100%; padding: .6rem; font-size: 1rem; box-sizing: border-box;">
    <button type="submit"
            style="margin-top: .75rem; width: 100%; padding: .6rem; font-size: 1rem;
                   background: #1F5C45; color: white; border: 0; border-radius: 4px;">
      Allow access
    </button>
  </form>
</body>`;
}
