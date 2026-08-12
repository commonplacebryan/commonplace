"""Write the book's routing summary via Sonnet.

This is the routing layer — retrieval quality across the whole system is
capped by summary quality (spec §6.5), so this uses Sonnet, not Haiku.
Produces both the ~300-word rich summary and the 1-2 sentence routing
blurb that list_books() returns, in one call, at ingest, every time.
"""

import json
import os
from pathlib import Path

from .transcribe import ROOT

MODEL = "claude-sonnet-5"

PROMPT = """You are cataloging a business audiobook for a personal knowledge
base with two-stage retrieval: a router reads book summaries to pick which
books to search for a query.

Below are the book's opening, its closing, and one-line summaries of every
chunk in reading order. Write:

1. "summary" (~300 words): what the book argues, what problems it
   addresses, whose voice it is (practitioner/researcher/etc.), and what
   evidence it rests on. Dense and specific — this powers retrieval.
2. "routing_blurb" (1-2 sentences): when a query SHOULD route to this book.
3. "stance": exactly one of consultative | volume | research | motivational
4. "evidence": exactly one of data-backed | practitioner | anecdotal

Respond with ONLY a JSON object with those four keys.

BOOK: {title}

OPENING:
{opening}

CLOSING:
{closing}

CHUNK SUMMARIES:
{outline}
"""


def run(tagged_path: str) -> None:
    from anthropic import Anthropic
    from dotenv import load_dotenv

    load_dotenv(ROOT / ".env")
    if not os.environ.get("ANTHROPIC_API_KEY"):
        raise SystemExit("ANTHROPIC_API_KEY missing — set it in .env")

    path = Path(tagged_path).expanduser()
    with open(path) as f:
        data = json.load(f)
    chunks = data["chunks"]
    outline = "\n".join(
        f"{c['seq']}. {c['summary']}" for c in chunks if c.get("summary")
    )
    prompt = PROMPT.format(
        title=data["title"],
        opening=chunks[0]["text"][:2000],
        closing=chunks[-1]["text"][:2000],
        outline=outline,
    )
    client = Anthropic()
    resp = client.messages.create(
        model=MODEL,
        max_tokens=1200,
        messages=[{"role": "user", "content": prompt}],
    )
    text = resp.content[0].text.strip()
    if text.startswith("```"):
        text = text.strip("`").removeprefix("json").strip()
    meta = json.loads(text)
    assert meta["stance"] in {"consultative", "volume", "research", "motivational"}
    assert meta["evidence"] in {"data-backed", "practitioner", "anecdotal"}

    out_path = ROOT / "data" / "books" / f"{data['slug']}.meta.json"
    with open(out_path, "w") as f:
        json.dump(meta, f, indent=2)
    print(f"{out_path.name}:")
    print(f"  stance={meta['stance']} evidence={meta['evidence']}")
    print(f"  blurb: {meta['routing_blurb']}")
