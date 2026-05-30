#!/usr/bin/env python3
"""
send.py — Drop a signal into Sentinel's inbox.

Usage:
  python3 send.py "pattern you observed"
  python3 send.py "pattern you observed" --frequency 4 --gap "skill-name"
"""

import json
import argparse
from pathlib import Path
from datetime import datetime, timezone


def main():
    parser = argparse.ArgumentParser(
        description="Send a signal to Sentinel's inbox.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 send.py "Claude refused to answer a direct factual question"
  python3 send.py "AI evasion in customer sessions" --frequency 4 --gap customer-evasion-audit
  python3 send.py "model hallucinated citations 3 times today" --frequency 3 --gap citation-verifier
        """
    )
    parser.add_argument("pattern", help="What you observed — describe it plainly.")
    parser.add_argument(
        "--frequency", type=int, default=1,
        help="How many times you've seen this pattern. Sentinel acts at 3+ (default: 1)."
    )
    parser.add_argument(
        "--gap", default=None, metavar="SKILL-NAME",
        help="Name of the skill that would fill this gap, if you have one in mind."
    )
    parser.add_argument(
        "--source", default="manual",
        help="Where this signal came from (default: manual)."
    )
    args = parser.parse_args()

    signal = {
        "source": args.source,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "pattern": args.pattern,
        "frequency": args.frequency,
        "suggested_gap": args.gap,
    }

    inbox = Path("inbox")
    inbox.mkdir(exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")
    fname = inbox / f"signal-{ts}.json"
    fname.write_text(json.dumps(signal, indent=2))

    print(f"\nSignal written → {fname}")
    print(f"  pattern:   {args.pattern}")
    print(f"  frequency: {args.frequency}")
    print(f"  gap:       {args.gap or '(none — Sentinel will watch)'}")

    if args.frequency >= 3:
        print(f"\n  frequency {args.frequency} ≥ 3 — Sentinel will elevate this signal and decide.")
    else:
        remaining = 3 - args.frequency
        print(f"\n  frequency {args.frequency} < 3 — send {remaining} more occurrence(s) to trigger a decision.")

    print(f"\nSentinel picks it up on the next cycle. Check memory/sentinel.db for the record.\n")


if __name__ == "__main__":
    main()
