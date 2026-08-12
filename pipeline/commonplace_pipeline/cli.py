"""Pipeline entry point.

Stages run independently so a failed stage reruns without repeating earlier
work. Intermediate outputs land in data/ (gitignored).

    commonplace transcribe data/audio/<book>/   -> data/transcripts/<book>.json
    commonplace chunk      data/transcripts/<book>.json
    commonplace tag        data/chunks/<book>.json
    commonplace summarize  data/chunks/<book>.tagged.json
    commonplace embed      data/chunks/<book>.tagged.json
    commonplace load       data/chunks/<book>.final.json
"""

import argparse
import sys

from . import chunk, stitch, transcribe

STAGES = ["transcribe", "stitch", "chunk", "tag", "summarize", "embed", "load"]


def main() -> None:
    parser = argparse.ArgumentParser(prog="commonplace")
    parser.add_argument("stage", choices=STAGES)
    parser.add_argument("path", help="Input file or directory for the stage")
    parser.add_argument("--slug", help="Book slug, e.g. 'freemium' (stitch/chunk)")
    parser.add_argument("--title", help="Book title for stitch")
    args = parser.parse_args()
    if args.stage == "transcribe":
        transcribe.run(args.path)
        return
    if args.stage == "stitch":
        if not (args.slug and args.title):
            parser.error("stitch requires --slug and --title")
        stitch.run(args.path, args.slug, args.title)
        return
    if args.stage == "chunk":
        chunk.run(args.path)
        return
    # Remaining stages arrive one at a time, validated against real output
    # before the next is written (spec §11 — verify file one, not file twelve).
    print(f"stage '{args.stage}' not implemented yet", file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    main()
