"""
observe.py — Sentinel's sensory layer.

Reads from inbox/ (Hermes signals) and skills/ (current capability surface).
Returns a structured observation dict each cycle.
"""

import json
import shutil
from pathlib import Path
from datetime import datetime, timezone

INBOX = Path("inbox")
PROCESSED = Path("inbox/processed")
SKILLS = Path("skills")


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_inbox() -> list[dict]:
    """Read and process all signal files from inbox/. Move to processed/ after reading."""
    PROCESSED.mkdir(parents=True, exist_ok=True)
    signals = []

    for f in INBOX.glob("*.json"):
        try:
            data = json.loads(f.read_text())
            signals.append(data)
            dest = PROCESSED / f.name
            shutil.move(str(f), str(dest))
        except Exception as e:
            # Bad signal file — log it but don't crash
            signals.append({
                "source": "inbox_error",
                "timestamp": now(),
                "pattern": f"Unreadable signal file: {f.name}",
                "frequency": 1,
                "suggested_gap": None,
                "error": str(e)
            })

    return signals


def read_capabilities() -> list[str]:
    """Return list of skills Sentinel has already built."""
    if not SKILLS.exists():
        return []
    return [d.name for d in SKILLS.iterdir() if d.is_dir() and not d.name.startswith(".")]


def observe(cycle: int) -> dict:
    """
    Main observation function. Called once per loop cycle.
    Returns structured observation dict.
    """
    signals = read_inbox()
    capabilities = read_capabilities()

    return {
        "source": "observe",
        "cycle": cycle,
        "timestamp": now(),
        "signals": signals,
        "capabilities": capabilities,
        "signal_count": len(signals),
        "capability_count": len(capabilities)
    }
