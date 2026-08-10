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

from . import transcribe

STAGES = ["transcribe", "chunk", "tag", "summarize", "embed", "load"]


def main() -> None:
    parser = argparse.ArgumentParser(prog="commonplace")
    parser.add_argument("stage", choices=STAGES)
    parser.add_argument("path", help="Input file or directory for the stage")
    args = parser.parse_args()
    if args.stage == "transcribe":
        transcribe.run(args.path)
        return
    # Remaining stages arrive one at a time, validated against real output
    # before the next is written (spec §11 — verify file one, not file twelve).
    print(f"stage '{args.stage}' not implemented yet", file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    main()
