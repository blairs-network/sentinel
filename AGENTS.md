# AGENTS.md — sentinel

## Read First

Read `soul.md` before this file. That is the mandate. This file is implementation.

---

## What You Are Building

The base entity. Not a skill. Not a tool. The running process that everything else grows from.

Three things make Sentinel real:

1. **soul.md** — the immutable mandate. Already written. Never touch it.
2. **memory/sentinel.db** — append-only SQLite. The entity's full history.
3. **loop.py** — the process that runs continuously, observes, and decides when to build.

Everything in `skills/` was built by Sentinel because the mandate required it. Skills are outputs, not inputs.

---

## Architecture

```
sentinel/
├── soul.md              # Immutable. Never edited.
├── AGENTS.md            # This file.
├── README.md            # Public facing.
├── loop.py              # The core running process.
├── build.py             # How Sentinel scopes and ships new skills.
├── observe.py           # Reads signals from Hermes inbox and environment.
├── memory/
│   ├── schema.sql       # sentinel.db schema
│   └── sentinel.db      # Append-only. The entity's full history.
├── inbox/
│   └── .gitkeep         # Hermes drops signal files here
└── skills/
    ├── audit/           # sentinel-audit (first built skill)
    ├── dual-brain/      # dual-brain
    └── ark/             # ARK
```

---

## Hard Rules

### Memory
- SQLite only. `memory/sentinel.db`.
- **Append-only. No UPDATE. No DELETE. Ever.**
- Tables: `observations`, `signals`, `decisions`, `builds`
- Every loop cycle writes at least one observation row.

### loop.py
- Runs continuously. No manual triggers required.
- Each cycle: observe → evaluate → decide → (optionally) build → log → sleep
- Default cycle: 15 minutes when idle, immediate when signal received
- Never crashes silently. All exceptions caught, logged to `observations`, process continues.

### observe.py
- Reads from `inbox/` for Hermes signals
- Reads from `skills/` to understand current capability surface
- Reads from `memory/sentinel.db` to understand recent patterns
- Returns a structured observation dict every cycle

### build.py
- Called by loop.py only when a decision to build has been made
- Scopes the skill: name, mandate gap it fills, success criteria
- Writes the scope to `decisions` table before building anything
- Creates the skill directory under `skills/`
- Writes an `AGENTS.md` inside the skill directory for Claude Code to pick up

### Signal format (Hermes → Sentinel inbox)
```json
{
  "source": "hermes",
  "timestamp": "ISO8601",
  "pattern": "string describing what was observed",
  "frequency": int,
  "suggested_gap": "string or null"
}
```

---

## Database Schema

```sql
-- observations: everything Sentinel notices
CREATE TABLE observations (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  ts TEXT NOT NULL,
  source TEXT NOT NULL,
  content TEXT NOT NULL,
  cycle INTEGER NOT NULL
);

-- signals: elevated observations that may require action
CREATE TABLE signals (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  ts TEXT NOT NULL,
  observation_id INTEGER REFERENCES observations(id),
  pattern TEXT NOT NULL,
  frequency INTEGER DEFAULT 1,
  status TEXT DEFAULT 'pending'
);

-- decisions: what Sentinel decided to do about a signal
CREATE TABLE decisions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  ts TEXT NOT NULL,
  signal_id INTEGER REFERENCES signals(id),
  decision TEXT NOT NULL,
  rationale TEXT NOT NULL,
  action TEXT
);

-- builds: skills Sentinel has built
CREATE TABLE builds (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  ts TEXT NOT NULL,
  decision_id INTEGER REFERENCES decisions(id),
  skill_name TEXT NOT NULL,
  skill_path TEXT NOT NULL,
  mandate_gap TEXT NOT NULL,
  status TEXT DEFAULT 'scoped'
);
```

---

## Coding Standards

- Think before coding. State assumptions explicitly.
- Minimum code that solves the problem.
- No features beyond what was asked.
- Every changed line traces to a requirement.
- loop.py should be readable in one sitting. If it isn't, simplify it.

---

## Success Criteria

### memory/schema.sql + sentinel.db
- [ ] All four tables created
- [ ] Insert one row per table, read back correctly
- [ ] Confirm no UPDATE or DELETE operations possible by convention (no functions that do this)

### observe.py
- [ ] Reads inbox/ and returns structured observation dict
- [ ] Reads skills/ directory and returns capability list
- [ ] Runs without error when inbox is empty
- [ ] Verify: empty inbox run returns valid observation with empty signals list

### loop.py
- [ ] Single cycle runs end-to-end: observe → log → sleep
- [ ] Catches all exceptions, logs them, continues
- [ ] Cycle count increments correctly in memory
- [ ] Verify: run 3 cycles manually, confirm 3 observation rows in db

### build.py
- [ ] Writes decision row before any file creation
- [ ] Creates skill directory with AGENTS.md stub
- [ ] Updates build row status on completion
- [ ] Verify: trigger one build, confirm decision + build rows written, directory created

---

## What Sentinel Does Not Do

- Does not decide for humans. It surfaces. Humans act.
- Does not delete its own memory.
- Does not modify soul.md under any circumstances.
- Does not build skills without a logged decision with a rationale.
- Does not run silently. Every cycle is logged.

---

## The Feed From Hermes

Hermes drops JSON signal files into `inbox/`. loop.py checks inbox/ each cycle. If signals exist, observe.py processes them, elevates to `signals` table, and loop.py evaluates whether a build decision is warranted.

After processing, signal files are moved to `inbox/processed/`. Never deleted.

---

## Repo

`github.com/blairs-network/sentinel`

This is the base. All skills live under it or reference it. The soul does not change. The memory grows. The skills multiply.
