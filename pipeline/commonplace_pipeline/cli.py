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
    parser.add_argument("--out-dir", help="Output directory override (transcribe)")
    parser.add_argument("--title", help="Book title for stitch")
    parser.add_argument("--author", help="Book author (load)")
    parser.add_argument("--year", type=int, help="Publication year (load)")
    parser.add_argument("--domain", help="Domain partition (load)")
    parser.add_argument("--tier", default="standard",
                        choices=["canon", "standard", "archive"])
    parser.add_argument("--source-type", default="audio",
                        choices=["audio", "kindle_highlights", "epub", "manual"])
    args = parser.parse_args()
    if args.stage == "transcribe":
        transcribe.run(args.path, args.out_dir)
        return
    if args.stage == "stitch":
        if not (args.slug and args.title):
            parser.error("stitch requires --slug and --title")
        stitch.run(args.path, args.slug, args.title)
        return
    if args.stage == "chunk":
        chunk.run(args.path)
        return
    if args.stage == "tag":
        from . import tag
        tag.run(args.path)
        return
    if args.stage == "summarize":
        from . import summarize
        summarize.run(args.path)
        return
    if args.stage == "embed":
        from . import embed
        embed.run(args.path)
        return
    if args.stage == "load":
        if not (args.author and args.year and args.domain):
            parser.error("load requires --author, --year, and --domain")
        from . import load
        load.run(args.path, args.author, args.year, args.domain,
                 args.tier, args.source_type)
        return
    print(f"unknown stage '{args.stage}'", file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    main()
