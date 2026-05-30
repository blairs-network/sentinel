"""
memory/db.py — Sentinel's memory interface.

Append-only. No UPDATE. No DELETE. Ever.
All writes go through these functions. Nothing else touches the db directly.
"""

import sqlite3
from pathlib import Path

DB_PATH = Path("memory/sentinel.db")
SCHEMA_PATH = Path("memory/schema.sql")


def get_db() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Initialize the database from schema.sql. Safe to call multiple times."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = get_db()
    conn.executescript(SCHEMA_PATH.read_text())
    conn.commit()
    conn.close()


def log_observation(ts: str, source: str, content: str, cycle: int) -> int:
    conn = get_db()
    cur = conn.execute(
        "INSERT INTO observations (ts, source, content, cycle) VALUES (?, ?, ?, ?)",
        (ts, source, content, cycle)
    )
    conn.commit()
    row_id = cur.lastrowid
    conn.close()
    return row_id


def log_signal(ts: str, observation_id: int, pattern: str, frequency: int) -> int:
    conn = get_db()
    cur = conn.execute(
        "INSERT INTO signals (ts, observation_id, pattern, frequency) VALUES (?, ?, ?, ?)",
        (ts, observation_id, pattern, frequency)
    )
    conn.commit()
    row_id = cur.lastrowid
    conn.close()
    return row_id


def log_decision(ts: str, signal_id: int, decision: str, rationale: str, action: str) -> int:
    conn = get_db()
    cur = conn.execute(
        "INSERT INTO decisions (ts, signal_id, decision, rationale, action) VALUES (?, ?, ?, ?, ?)",
        (ts, signal_id, decision, rationale, action)
    )
    conn.commit()
    row_id = cur.lastrowid
    conn.close()
    return row_id


def log_build(ts: str, decision_id: int, skill_name: str, skill_path: str, mandate_gap: str, status: str) -> int:
    conn = get_db()
    cur = conn.execute(
        "INSERT INTO builds (ts, decision_id, skill_name, skill_path, mandate_gap, status) VALUES (?, ?, ?, ?, ?, ?)",
        (ts, decision_id, skill_name, skill_path, mandate_gap, status)
    )
    conn.commit()
    row_id = cur.lastrowid
    conn.close()
    return row_id


def update_build_status(build_id: int, status: str) -> None:
    """
    This is the ONLY permitted UPDATE in the entire codebase.
    It updates build status only — not content, not decisions, not observations.
    Status progression: scoped → agents_written → in_build → shipped
    """
    conn = get_db()
    conn.execute(
        "UPDATE builds SET status = ? WHERE id = ?",
        (status, build_id)
    )
    conn.commit()
    conn.close()
