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

STAGES = ["transcribe", "chunk", "tag", "summarize", "embed", "load"]


def main() -> None:
    parser = argparse.ArgumentParser(prog="commonplace")
    parser.add_argument("stage", choices=STAGES)
    parser.add_argument("path", help="Input file or directory for the stage")
    args = parser.parse_args()
    # Phase 1: implement stages one at a time, validating output at each step
    # before writing the next (spec §11 — verify file one, not file twelve).
    print(f"stage '{args.stage}' not implemented yet", file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    main()
