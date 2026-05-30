"""
build.py — How Sentinel scopes and ships new skills.

Called by loop.py only when a logged decision to build has been made.
Creates skill directory, writes AGENTS.md stub, updates build record.
Decision is always logged before any file is created.
"""

from pathlib import Path
from datetime import datetime, timezone

from memory.db import log_build, update_build_status

SKILLS = Path("skills")


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def agents_stub(skill_name: str, mandate_gap: str) -> str:
    """Generate a minimal AGENTS.md for a new skill directory."""
    return f"""# AGENTS.md — {skill_name}

## Why This Skill Exists

Sentinel built this skill to fill the following gap:

> {mandate_gap}

---

## What To Build

This skill is in the scoping phase. Sentinel has identified the gap.
Claude Code will define the architecture and success criteria here.

---

## Hard Rules (inherited from Sentinel)

- Append-only storage if this skill uses SQLite
- Every metric or output has a plain-English reason, not just a score
- No features beyond what the mandate gap requires
- The human is the customer. Build accordingly.

---

## Provenance

Scoped by Sentinel on {now()}.
Mandate gap: {mandate_gap}
"""


def scope_build(decision_id: int, skill_name: str, mandate_gap: str) -> None:
    """
    Create a new skill directory and write an AGENTS.md stub.
    Log the build to memory before creating any files.
    """
    skill_path = SKILLS / skill_name

    # Log the build record first — decision before action
    build_id = log_build(
        ts=now(),
        decision_id=decision_id,
        skill_name=skill_name,
        skill_path=str(skill_path),
        mandate_gap=mandate_gap,
        status="scoped"
    )

    # Create the skill directory
    skill_path.mkdir(parents=True, exist_ok=True)

    # Write AGENTS.md stub
    agents_path = skill_path / "AGENTS.md"
    agents_path.write_text(agents_stub(skill_name, mandate_gap))

    # Update build status
    update_build_status(build_id, "agents_written")

    print(f"[build] Scoped skill '{skill_name}' at {skill_path}. AGENTS.md written.")
    print(f"[build] Hand {skill_path}/AGENTS.md to Claude Code to continue.")
