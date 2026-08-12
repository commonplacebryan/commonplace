"""Stitch per-hour transcripts into one continuous book transcript.

Hour files each start at t=0; stitching offsets every segment by the
cumulative duration of prior files so timestamps become book-global.
The per-file offset table is kept in the output so any global timestamp
can be mapped back to (source file, local time) for audio auditing.

Word-level detail is dropped here: chunk-level audit only needs segment
granularity, and it keeps the book file ~10x smaller.
"""

import json
import re
from pathlib import Path

from .transcribe import ROOT

# A chapter marker is a short segment that *starts* with a structural word.
# Whisper reliably emits these as their own segments in audiobooks.
NUMBERED_RE = re.compile(
    r"^(chapter|part)\s+(\d+|one|two|three|four|five|six|seven|eight|nine|ten|"
    r"eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|"
    r"nineteen|twenty)\b",
    re.IGNORECASE,
)
# Front/back matter words appear in ordinary prose too ("forward when
# adding..."), so they only count when they stand alone.
STANDALONE_RE = re.compile(
    r"^(introduction|foreword|forward|preface|prologue|conclusion|epilogue|"
    r"afterword|appendix)$",
    re.IGNORECASE,
)
MARKER_MAX_WORDS = 12


def is_chapter_marker(text: str) -> bool:
    t = text.strip().rstrip(".!?,;:")
    if STANDALONE_RE.match(t):
        return True
    return bool(NUMBERED_RE.match(t)) and len(t.split()) <= MARKER_MAX_WORDS


def run(transcripts_dir: str, slug: str, title: str) -> None:
    src = Path(transcripts_dir).expanduser()
    files = sorted(src.glob("*.json"))
    if not files:
        raise SystemExit(f"no transcripts in {src}")

    segments, offsets = [], []
    offset = 0.0
    for path in files:
        with open(path) as f:
            segs = json.load(f).get("segments", [])
        offsets.append({"file": path.stem, "offset": round(offset, 2)})
        for s in segs:
            text = s["text"].strip()
            if not text:
                continue
            segments.append(
                {
                    "start": round(s["start"] + offset, 2),
                    "end": round(s["end"] + offset, 2),
                    "text": text,
                    "chapter_marker": is_chapter_marker(text),
                }
            )
        if segs:
            offset += segs[-1]["end"]

    out_dir = ROOT / "data" / "books"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{slug}.json"
    with open(out_path, "w") as f:
        json.dump(
            {"slug": slug, "title": title, "files": offsets, "segments": segments},
            f,
        )

    markers = [s["text"] for s in segments if s["chapter_marker"]]
    hours = segments[-1]["end"] / 3600 if segments else 0
    print(f"{out_path.name}: {len(files)} files, {hours:.1f} h, {len(segments)} segments")
    print(f"chapter markers found ({len(markers)}):")
    for m in markers:
        print(f"  - {m}")
