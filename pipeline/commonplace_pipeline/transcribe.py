"""Transcribe captured audio with mlx-whisper.

Wraps the mlx_whisper CLI rather than the library so the model runs in its
own process — a crash mid-book loses one file, not the batch. Word-level
timestamps are non-negotiable: they populate chunks.start_ts/end_ts, the
audit trail back to source audio.
"""

import json
import subprocess
import sys
from pathlib import Path

MODEL = "mlx-community/whisper-large-v3-turbo"
AUDIO_EXTS = {".mp3", ".m4a", ".wav"}
# Repo root, so output lands in the same place regardless of cwd
ROOT = Path(__file__).resolve().parents[2]


def transcribe_file(audio: Path, out_dir: Path) -> Path:
    out_path = out_dir / f"{audio.stem}.json"
    if out_path.exists():
        print(f"skip (exists): {out_path.name}")
        return out_path
    print(f"transcribing: {audio.name}")
    # Resolve from this interpreter's venv — bare name requires PATH setup
    mlx_whisper = Path(sys.executable).parent / "mlx_whisper"
    subprocess.run(
        [
            str(mlx_whisper), str(audio),
            "--model", MODEL,
            "--output-format", "json",
            "--word-timestamps", "True",
            "--language", "en",
            "--output-dir", str(out_dir),
            "--verbose", "False",
            # Prevent repetition-loop hallucinations on table-like narration:
            # never condition a segment on the previous segment's output
            "--condition-on-previous-text", "False",
        ],
        check=True,
    )
    if not out_path.exists():
        # mlx_whisper "skips" undecodable files with exit code 0; treat as failure
        raise RuntimeError(f"no output produced for {audio.name} — check audio file")
    with open(out_path) as f:
        segs = json.load(f).get("segments", [])
    mins = segs[-1]["end"] / 60 if segs else 0
    print(f"  -> {out_path.name}: {len(segs)} segments, {mins:.1f} min")
    return out_path


def run(path: str, out_dir: str | None = None) -> None:
    src = Path(path).expanduser()
    out = Path(out_dir) if out_dir else ROOT / "data" / "transcripts"
    out.mkdir(parents=True, exist_ok=True)
    files = (
        sorted(p for p in src.iterdir() if p.suffix.lower() in AUDIO_EXTS)
        if src.is_dir()
        else [src]
    )
    if not files:
        print(f"no audio files found in {src}", file=sys.stderr)
        sys.exit(1)
    for audio in files:
        transcribe_file(audio, out)
