"""Chunk a stitched book transcript on structural boundaries.

Chapter markers from stitch are boundary hints; markers within 60s of the
previous one are collapsed (table-of-contents read-throughs produce runs of
false markers at the start of audiobooks). Within a chapter, chunks flush
at sentence-ending segments once they reach the target size, with one
sentence of overlap carried forward. Book title and chapter are prepended
to the chunk text itself — it measurably improves retrieval (spec §6.3).

Phase 2 adds Claude-refined topic-shift boundaries; the structural pass
exists so retrieval quality can be evaluated end-to-end on book one first.
"""

import json
import re
from pathlib import Path

from .transcribe import ROOT

TARGET_WORDS = 550
MAX_WORDS = 750
MARKER_MERGE_S = 60

SENT_END = re.compile(r"[.!?][\"')\]]?$")


def last_sentence(text: str) -> str:
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return parts[-1] if parts else ""


def run(book_path: str) -> None:
    with open(Path(book_path).expanduser()) as f:
        book = json.load(f)
    title, slug = book["title"], book["slug"]

    chunks = []
    chapter = "Front Matter"
    last_marker_t = -1e9
    cur: list[dict] = []
    cur_words = 0
    carry = ""

    def flush() -> None:
        nonlocal cur, cur_words, carry
        if not cur:
            return
        body = " ".join(s["text"] for s in cur)
        text = f"{title} — {chapter}\n\n"
        if carry:
            text += carry + " "
        text += body
        chunks.append(
            {
                "seq": len(chunks),
                "chapter": chapter,
                "text": text,
                "start_ts": int(cur[0]["start"]),
                "end_ts": int(cur[-1]["end"]),
                "words": cur_words,
            }
        )
        carry = last_sentence(body)
        cur, cur_words = [], 0

    for seg in book["segments"]:
        if seg["chapter_marker"]:
            if seg["start"] - last_marker_t > MARKER_MERGE_S:
                flush()
                carry = ""  # no overlap across chapter boundaries
                chapter = seg["text"].strip().rstrip(".,;:")
            else:
                # marker run (TOC read-through): extend the same boundary,
                # keeping the latest label
                chapter = seg["text"].strip().rstrip(".,;:")
            last_marker_t = seg["start"]
            continue
        cur.append(seg)
        cur_words += len(seg["text"].split())
        if cur_words >= MAX_WORDS or (
            cur_words >= TARGET_WORDS and SENT_END.search(seg["text"])
        ):
            flush()
    flush()

    out_dir = ROOT / "data" / "chunks"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{slug}.json"
    with open(out_path, "w") as f:
        json.dump({"slug": slug, "title": title, "chunks": chunks}, f)

    sizes = sorted(c["words"] for c in chunks)
    n = len(sizes)
    print(f"{out_path.name}: {n} chunks across {len({c['chapter'] for c in chunks})} chapters")
    print(f"words/chunk — min {sizes[0]}, median {sizes[n // 2]}, max {sizes[-1]}")
    small = sum(1 for s in sizes if s < 200)
    print(f"chunks under 200 words: {small} (chapter tails)")
