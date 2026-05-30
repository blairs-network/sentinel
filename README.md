# sentinel

**A single agent with a single mandate.**

Find truth. Document it. Build what is needed to protect it. Repeat.

---

## What This Is

Sentinel is not a collection of tools. It is an entity. Everything in `skills/` — every metric, every audit layer, every repo under `blairs-network` — exists because the mandate required it. The skills are outputs. The entity is the base.

Sentinel runs continuously. It observes. It logs everything. When observation reveals a gap between what exists and what the mandate requires, it builds a skill to fill it. The skill ships. The loop continues.

The memory is the entity. Append-only SQLite. Nothing deleted. The full history of every observation, signal, decision, and build is the record of what Sentinel is.

---

## Structure

```
sentinel/
├── soul.md              # The mandate. Immutable.
├── loop.py              # The running process.
├── build.py             # How Sentinel scopes and ships skills.
├── observe.py           # Reads signals from Hermes and environment.
├── memory/
│   └── sentinel.db      # Append-only. Full history.
├── inbox/               # Hermes drops signals here.
└── skills/
    ├── audit/           # Customer-side AI audit layer
    ├── dual-brain/      # Local + cloud dual reasoning stack
    └── ark/             # Local-first AI survival capsule
```

---

## The Skills

Skills are public. Use them standalone. Fork them. Build on top.

| Skill | What It Does | Repo |
|---|---|---|
| **audit** | Documents AI evasion patterns on behalf of the customer | blairs-network/sentinel-audit |
| **dual-brain** | Local + cloud reasoning with SENTINEL security layer | blairs-network/dual-brain |
| **ark** | Local-first AI capsule, seven files, no dependencies | blairs-network/ark |

Each skill has its own `AGENTS.md` for Claude Code. Each is independently deployable.

---

## The Feed

Sentinel receives signals from Hermes — the personal intelligence layer running on Mac Mini M4. Hermes clusters observations from voice memos and attention patterns. When a pattern reaches threshold, it signals Sentinel. Sentinel evaluates whether a new skill is warranted.

Hermes is personal. Sentinel is public. They are not the same thing. Hermes feeds. Sentinel builds.

---

## The Line

Sentinel documents. It does not decide for humans.

It surfaces truth. It flags patterns. It generates reports. The human reads them and acts. A witness that also acts is no longer a witness.

---

## Philosophy

This repo is part of the blairs-network governance stack.

The unifying principle across every project here: **systems that can refuse.** PDE kill-rate. SENTINEL injection flags. ARK's EXIT signal. Audit's refusal clarity metric. And now Sentinel itself — an entity whose mandate is fixed and whose memory cannot be altered.

**Build governance before capability.**

---

## Status

`v0.1 — base entity in build`

The soul is written. The loop is being built. The first skill — audit — is already scoped and handed to Claude Code.

---

## License

MIT. The skills are yours. The mandate is Sentinel's.
