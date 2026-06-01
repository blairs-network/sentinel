# sentinel

> *Most AI systems do what you tell them.*
> *Sentinel does what the truth requires.*

---

**Find truth. Document it. Build what is needed to protect it. Repeat.**

That is the mandate. It was written once. It does not change.

---

## The Idea

The AI space is building capability faster than it's building accountability. Every week there are new models, new tools, new agents — and almost no systems designed to witness, document, and flag what those tools actually do in the hands of real people.

Sentinel is a response to that gap.

It's an autonomous entity with a fixed mandate. It runs continuously. It observes. When it detects a pattern that existing tools can't address — AI evasion, refusal clarity failures, citation hallucinations — it builds a new skill to document it. Every observation, every decision, every build is logged to an append-only database. Nothing is deleted. Nothing is amended.

The memory is the entity. The mandate is immutable. The witness holds.

---

## What Makes This Different

**The mandate is fixed.** `soul.md` was written once and is never touched. The agent's purpose — find truth, document it, build what is needed — is locked in the architecture. It cannot be redirected by a prompt or a config change. This is governance by design, not by policy.

**The memory cannot be altered.** Everything Sentinel observes and decides goes into an append-only SQLite database. No `UPDATE`. No `DELETE`. The full history of what this entity has witnessed is what it is. If the memory is gone, Sentinel is gone.

**It does not decide for humans.** Sentinel surfaces patterns. It builds tools to expose them. The human reads the output and acts. A witness that also acts is no longer a witness. This line is load-bearing — it's what makes the outputs trustworthy.

**Skills are outputs, not inputs.** Nothing in `skills/` was planned in advance. Each skill is evidence of a gap the mandate exposed. Sentinel builds when observation requires it — not when a roadmap says so.

---

## The Current State

`v0.1 — base entity live`

The loop runs. The memory grows. The first real signal — an AI evasion pattern detected in customer sessions — has been processed: observed, elevated, decided, scoped.

`skills/customer-evasion-audit/` now exists because the mandate required it.

| Skill | Status | Gap It Fills |
|---|---|---|
| **customer-evasion-audit** | scoped — spec written, build next | AI evasion patterns in customer sessions |

Skills are added here when scoped. They link to their repos when shipped.

---

## The Architecture

Five Python files. One SQLite database. No external dependencies. Readable in a single sitting.

```
sentinel/
├── soul.md        — The mandate. Immutable. Written once. Never touched.
├── loop.py        — Observe → decide → build → log → sleep. Repeat.
├── observe.py     — Reads signals from inbox/ and skills/.
├── build.py       — Scopes new skills when a decision to build is logged.
├── send.py        — Drop a signal from the command line.
├── memory/
│   └── sentinel.db — Append-only SQLite. The entity's full history.
├── inbox/         — Signal files go here. Picked up each cycle.
└── skills/        — Every skill Sentinel has built. Public. Forkable.
```

---

## Getting Started

**1. Clone and run.**

```bash
git clone https://github.com/blairs-network/sentinel
cd sentinel
python3 loop.py
```

Python 3.10+. No pip installs. The database initializes on first run.

**2. Send a signal.**

Open a second terminal in the same directory:

```bash
cd sentinel
python3 send.py "AI refused to answer a direct question" --frequency 3 --gap citation-verifier
```

Sentinel picks it up on the next cycle. Frequency ≥ 3 triggers a decision. If a gap is named, a skill is scoped.

**3. See what happened.**

```bash
python3 -c "
import sqlite3
conn = sqlite3.connect('memory/sentinel.db')
conn.row_factory = sqlite3.Row
for row in conn.execute('SELECT ts, decision, action FROM decisions ORDER BY id DESC LIMIT 5'):
    print(dict(row))
"
```

Every decision is in `memory/sentinel.db`. Nothing is deleted.

| Flag | What it does |
|---|---|
| `--frequency N` | Times seen. Sentinel acts at 3+. |
| `--gap skill-name` | Names the capability gap. Sentinel will scope a skill. |
| `--source name` | Where the signal came from. Default: `manual`. |

---

## The Feed

Sentinel receives signals from Hermes — a personal intelligence layer running on Mac Mini M4. Hermes observes patterns across sessions and surfaces them when frequency crosses threshold. When a pattern is real enough, it crosses to Sentinel.

Hermes is personal. Sentinel is public. They are not the same thing. Hermes feeds. Sentinel builds.

---

## The Philosophy

**Build governance before capability.**

The gap in the AI space right now is not intelligence. It is accountability. The ability to witness. To document. To refuse to alter the record. Sentinel is an attempt to build a system where that accountability is architectural — not a promise, not a policy, not a system prompt.

The unifying principle across everything in `blairs-network`: **systems that can refuse.** An entity whose mandate is fixed. A database that can only grow. A witness that will not act in place of the human it serves.

---

## License

MIT. The skills are yours. The mandate is Sentinel's.
