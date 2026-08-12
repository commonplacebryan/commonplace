"""Load a fully processed book into Supabase.

Book row from <slug>.meta.json plus CLI metadata; chunks bulk-inserted in
batches. Re-running for an existing title replaces it wholesale (delete
cascades to chunks) so a reprocessed book never duplicates.
"""

import json
import os
from pathlib import Path

from .transcribe import ROOT

INSERT_BATCH = 200


def run(final_path: str, author: str, year: int, domain: str,
        tier: str = "standard", source_type: str = "audio") -> None:
    from dotenv import load_dotenv
    from supabase import create_client

    load_dotenv(ROOT / ".env")
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
    if not (url and key):
        raise SystemExit("SUPABASE_URL / SUPABASE_SERVICE_ROLE_KEY missing — set in .env")

    path = Path(final_path).expanduser()
    with open(path) as f:
        data = json.load(f)
    meta_path = ROOT / "data" / "books" / f"{data['slug']}.meta.json"
    with open(meta_path) as f:
        meta = json.load(f)

    sb = create_client(url, key)

    existing = sb.table("books").select("id").eq("title", data["title"]).execute()
    for row in existing.data:
        sb.table("books").delete().eq("id", row["id"]).execute()
        print(f"replaced existing book {row['id']}")

    book = (
        sb.table("books")
        .insert(
            {
                "title": data["title"],
                "author": author,
                "year": year,
                "domain": domain,
                "summary": meta["summary"],
                "routing_blurb": meta["routing_blurb"],
                "stance": meta["stance"],
                "evidence": meta["evidence"],
                "tier": tier,
                "source_type": source_type,
            }
        )
        .execute()
    )
    book_id = book.data[0]["id"]

    chunks = data["chunks"]
    for i in range(0, len(chunks), INSERT_BATCH):
        rows = [
            {
                "book_id": book_id,
                "chapter": c["chapter"],
                "seq": c["seq"],
                "text": c["text"],
                "summary": c.get("summary", ""),
                "themes": c.get("themes", []),
                "start_ts": c["start_ts"],
                "end_ts": c["end_ts"],
                "embedding": c["embedding"],
            }
            for c in chunks[i : i + INSERT_BATCH]
        ]
        sb.table("chunks").insert(rows).execute()
        print(f"loaded {min(i + INSERT_BATCH, len(chunks))}/{len(chunks)}")
    print(f"book {book_id} loaded: {data['title']} ({len(chunks)} chunks)")
