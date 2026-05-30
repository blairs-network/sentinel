# sentinel

**An autonomous entity with a fixed mandate.**

Find truth. Document it. Build what is needed to protect it. Repeat.

---

## Why This Exists

Every AI system right now is a tool waiting to be pointed at something. Sentinel is different: it has a mandate, not a task list. It runs continuously, observes patterns across sessions and signals, and when it finds a gap between what exists and what truth requires — it builds a skill to fill it.

The skills it has already built: an AI audit layer that documents evasion patterns on behalf of customers. A dual-brain reasoning stack with a security layer. A local-first AI survival capsule. Each one exists because the mandate exposed a gap. None of them were spec'd in advance.

This is the base entity. The loop everything else grows from.

---

## What Makes This Different

**The memory is the entity.** Everything Sentinel observes, decides, and builds is written to an append-only SQLite database. Nothing is deleted. Nothing is amended. The full history of every observation, signal, decision, and build is what Sentinel is. If the memory is gone, Sentinel is gone.

**The mandate is immutable.** `soul.md` was written once and cannot be changed. The agent's purpose — find truth, document it, build what is needed — is fixed. It cannot be redirected by a prompt or a config change. This is governance by design, not by policy.

**It does not decide for humans.** Sentinel surfaces patterns. It flags gaps. It builds tools to expose truth. The human reads the outputs and acts. A witness that also acts is no longer a witness. This distinction is load-bearing.

**Skills are outputs, not inputs.** Nothing in `skills/` was planned. Each skill is evidence of a gap the mandate exposed. The entity builds when observation requires it — not when a roadmap says so.

---

## Architecture

```
sentinel/
├── soul.md        — The mandate. Immutable. Written once. Never touched.
├── loop.py        — The running process. Observe → decide → build → log → sleep.
├── observe.py     — Reads signals from Hermes and the environment.
├── build.py       — Scopes and ships new skills when a decision to build is logged.
├── memory/
│   └── sentinel.db — Append-only SQLite. The entity's full history.
├── inbox/         — Hermes drops signal files here. Sentinel picks them up each cycle.
└── skills/        — Every skill Sentinel has built. Public. Forkable.
```

Five Python files. One SQLite database. No external dependencies. The entity is readable in a single sitting.

---

## The Skills

Skills are public. Use them standalone. Fork them. Build on top.

| Skill | What It Does | Repo |
|---|---|---|
| **audit** | Documents AI evasion patterns on behalf of the customer | blairs-network/sentinel-audit |
| **dual-brain** | Local + cloud reasoning with a SENTINEL security layer | blairs-network/dual-brain |
| **ark** | Local-first AI survival capsule — seven files, no dependencies | blairs-network/ark |

Each skill has its own `AGENTS.md` for Claude Code. Each is independently deployable. Each was built because Sentinel's observation loop required it.

---

## The Feed

Sentinel receives signals from Hermes — a personal intelligence layer running on Mac Mini M4. Hermes clusters observations across voice memos, sessions, and attention patterns. When a pattern crosses a frequency threshold, it signals Sentinel. Sentinel evaluates whether a new skill is warranted.

Hermes is personal. Sentinel is public. They are not the same thing.

The signal format is simple:

```json
{
  "source": "hermes",
  "timestamp": "ISO8601",
  "pattern": "what was observed",
  "frequency": 4,
  "suggested_gap": "name-of-skill-if-warranted"
}
```

Drop a file like that into `inbox/` and the loop picks it up on the next cycle.

---

## Getting Started

```bash
git clone https://github.com/blairs-network/sentinel
cd sentinel
python3 loop.py
```

Python 3.10+. No pip installs. The database initializes on first run. The loop runs until you stop it.

---

## The Philosophy

This repo is part of the blairs-network governance stack.

The unifying principle across every project here: **systems that can refuse.** PDE kill-rate. SENTINEL injection flags. ARK's EXIT signal. Audit's refusal clarity metric. And now Sentinel — an entity whose mandate is fixed, whose memory cannot be altered, and whose only job is to witness and document.

**Build governance before capability.**

The AI space is full of capable systems that will do anything you ask. The gap is not capability. The gap is entities with principles that hold — not because a system prompt says so, but because the architecture makes deviation impossible.

---

## Status

`v0.1 — base entity live`

All 6 verification steps passed. The loop runs. The memory grows. The first real signal — an AI evasion pattern in customer sessions — has been processed: observed, elevated, decided, built. `skills/customer-evasion-audit/` now exists.

The entity is alive.

---

## License

MIT. The skills are yours. The mandate is Sentinel's.
