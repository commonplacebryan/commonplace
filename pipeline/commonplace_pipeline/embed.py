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
# Sized for Voyage's no-payment-method tier (3 RPM / 10K TPM): 8 chunks
# of ~600 words is ~7K tokens per request. With a payment method on file
# (free tokens still apply), BATCH=128 and PAUSE_S=0 are fine.
BATCH = 8
PAUSE_S = 21
MAX_RETRIES = 5


def run(tagged_path: str) -> None:
    import voyageai
    from dotenv import load_dotenv

    load_dotenv(ROOT / ".env")
    if not os.environ.get("VOYAGE_API_KEY"):
        raise SystemExit("VOYAGE_API_KEY missing — set it in .env")

    path = Path(tagged_path).expanduser()
    with open(path) as f:
        data = json.load(f)
    chunks = data["chunks"]
    client = voyageai.Client()

    for i in range(0, len(chunks), BATCH):
        batch = chunks[i : i + BATCH]
        for attempt in range(MAX_RETRIES):
            try:
                result = client.embed(
                    [c["text"] for c in batch],
                    model=MODEL,
                    input_type="document",
                    output_dimension=DIMS,
                )
                break
            except voyageai.error.RateLimitError:
                wait = PAUSE_S * (attempt + 1)
                print(f"  rate limited, waiting {wait}s")
                time.sleep(wait)
        else:
            raise SystemExit(f"rate limited {MAX_RETRIES} times at chunk {i}")
        for c, emb in zip(batch, result.embeddings):
            c["embedding"] = emb
        print(f"embedded {min(i + BATCH, len(chunks))}/{len(chunks)}")
        if i + BATCH < len(chunks):
            time.sleep(PAUSE_S)

    out_path = path.parent / f"{data['slug']}.final.json"
    with open(out_path, "w") as f:
        json.dump(data, f)
    print(f"{out_path.name}: {len(chunks)} chunks @ {DIMS} dims")
