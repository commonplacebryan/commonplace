"""Tag chunks against the controlled theme vocabulary via Haiku.

Classification task — Haiku is sufficient and far cheaper than Sonnet at
corpus scale (spec §6.4). Ten chunks per call, JSON array back, vocabulary
block prompt-cached since it is identical across every call. Off-list
themes are rejected, not corrected: the vocabulary is the contract.
"""

import json
import os
from pathlib import Path

from .transcribe import ROOT

MODEL = "claude-haiku-4-5-20251001"
BATCH = 10


def load_vocab() -> list[str]:
    with open(ROOT / "vocab" / "themes.json") as f:
        vocab = json.load(f)
    return sorted(
        t for k, themes in vocab.items() if not k.startswith("$") for t in themes
    )


def vocab_block() -> str:
    """Render 'theme — gloss' lines so the model tags by intended meaning,
    not by how a bare theme name happens to read (e.g. 'positioning')."""
    with open(ROOT / "vocab" / "themes.json") as f:
        vocab = json.load(f)
    glosses = vocab.get("$glosses", {})
    return "\n".join(f"{t} — {glosses[t]}" if t in glosses else t
                     for t in load_vocab())


SYSTEM = """You tag chunks of transcribed business audiobooks.

For each numbered chunk, return 1-3 themes from the ALLOWED THEMES list and
a one-line summary (max 20 words) of what the chunk actually says.

Rules:
- Themes MUST be copied exactly from the allowed list (the identifier
  before the dash). Never invent, rephrase, or pluralize a theme.
- Apply a theme only when the chunk matches its gloss (the text after
  the dash), not merely because the theme's name appears in the text.
- If no theme genuinely fits, return an empty themes list rather than
  forcing a bad match.
- Respond with ONLY a JSON array, one object per chunk, in input order:
  [{"seq": <int>, "themes": ["..."], "summary": "..."}]

ALLOWED THEMES:
"""


def tag_batch(client, vocab: set[str], batch: list[dict]) -> list[dict]:
    numbered = "\n\n".join(
        f"[chunk {c['seq']}]\n{c['text']}" for c in batch
    )
    resp = client.messages.create(
        model=MODEL,
        max_tokens=1500,
        system=[
            {
                "type": "text",
                "text": SYSTEM + vocab_block(),
                "cache_control": {"type": "ephemeral"},
            }
        ],
        messages=[{"role": "user", "content": numbered}],
    )
    text = next(b.text for b in resp.content if b.type == "text").strip()
    if text.startswith("```"):
        text = text.strip("`").removeprefix("json").strip()
    results = {r["seq"]: r for r in json.loads(text)}
    out = []
    for c in batch:
        r = results.get(c["seq"], {})
        themes = [t for t in r.get("themes", []) if t in vocab]
        rejected = [t for t in r.get("themes", []) if t not in vocab]
        if rejected:
            print(f"  seq {c['seq']}: rejected off-list themes {rejected}")
        out.append({**c, "themes": themes, "summary": r.get("summary", "")})
    return out


def run(chunks_path: str) -> None:
    from anthropic import Anthropic
    from dotenv import load_dotenv

    load_dotenv(ROOT / ".env")
    if not os.environ.get("ANTHROPIC_API_KEY"):
        raise SystemExit("ANTHROPIC_API_KEY missing — set it in .env")

    path = Path(chunks_path).expanduser()
    with open(path) as f:
        data = json.load(f)
    chunks = data["chunks"]
    client = Anthropic()
    vocab = set(load_vocab())

    tagged = []
    for i in range(0, len(chunks), BATCH):
        batch = chunks[i : i + BATCH]
        tagged.extend(tag_batch(client, vocab, batch))
        print(f"tagged {len(tagged)}/{len(chunks)}")

    out_path = path.parent / f"{data['slug']}.tagged.json"
    with open(out_path, "w") as f:
        json.dump({**data, "chunks": tagged}, f)
    themed = sum(1 for c in tagged if c["themes"])
    print(f"{out_path.name}: {themed}/{len(tagged)} chunks have themes")
