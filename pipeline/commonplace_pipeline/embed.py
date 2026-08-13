"""Embed tagged chunks with Voyage voyage-3.5-lite at 1024 dims.

Dimension choice is locked to the vector(1024) column — changing it later
means re-embedding the corpus (spec §3). input_type='document' here;
the MCP server must use input_type='query' at query time.
"""

import json
import os
import time
from pathlib import Path

from .transcribe import ROOT

MODEL = "voyage-3.5-lite"
DIMS = 1024
# Sized for Voyage's no-payment-method tier (3 RPM / 10K TPM). Batches are
# built by estimated token count, not chunk count — a fixed-count batch of
# long chunks can exceed 10K tokens and then no amount of waiting helps.
# With a payment method on file (free tokens still apply), raise
# TOKEN_BUDGET and drop PAUSE_S.
TOKEN_BUDGET = 5500
TOKENS_PER_WORD = 1.5  # conservative estimate
PAUSE_S = 45
MAX_RETRIES = 6


def token_batches(chunks: list[dict]) -> list[list[dict]]:
    batches: list[list[dict]] = []
    cur: list[dict] = []
    cur_tokens = 0.0
    for c in chunks:
        est = len(c["text"].split()) * TOKENS_PER_WORD
        if cur and cur_tokens + est > TOKEN_BUDGET:
            batches.append(cur)
            cur, cur_tokens = [], 0.0
        cur.append(c)
        cur_tokens += est
    if cur:
        batches.append(cur)
    return batches


def run(tagged_path: str) -> None:
    import voyageai
    from dotenv import load_dotenv

    load_dotenv(ROOT / ".env")
    if not os.environ.get("VOYAGE_API_KEY"):
        raise SystemExit("VOYAGE_API_KEY missing — set it in .env")

    path = Path(tagged_path).expanduser()
    with open(path) as f:
        data = json.load(f)
    out_path = path.parent / f"{data['slug']}.final.json"
    if out_path.exists():
        # Resume: keep embeddings already written by an interrupted run
        with open(out_path) as f:
            data = json.load(f)
        done = sum(1 for c in data["chunks"] if c.get("embedding"))
        print(f"resuming — {done} chunks already embedded")
    chunks = data["chunks"]
    client = voyageai.Client()

    todo = [c for c in chunks if not c.get("embedding")]
    for batch in token_batches(todo):
        for attempt in range(MAX_RETRIES):
            try:
                result = client.embed(
                    [c["text"] for c in batch],
                    model=MODEL,
                    input_type="document",
                    output_dimension=DIMS,
                )
                break
            except (
                voyageai.error.RateLimitError,
                voyageai.error.APIConnectionError,
                voyageai.error.ServiceUnavailableError,
            ) as e:
                wait = PAUSE_S * (attempt + 1)
                print(f"  {type(e).__name__}, waiting {wait}s")
                time.sleep(wait)
        else:
            raise SystemExit(f"rate limited {MAX_RETRIES} times at chunk {i}")
        for c, emb in zip(batch, result.embeddings):
            c["embedding"] = emb
        with open(out_path, "w") as f:
            json.dump(data, f)
        done = sum(1 for c in chunks if c.get("embedding"))
        print(f"embedded {done}/{len(chunks)}")
        if done < len(chunks):
            time.sleep(PAUSE_S)

    print(f"{out_path.name}: {len(chunks)} chunks @ {DIMS} dims")
