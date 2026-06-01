# Thread Outline — for anyone who wants to share this

This is a ready-to-adapt outline for a post, thread, newsletter, or video script.
Take it, rewrite it in your voice, use whatever parts fit.

---

## The hook

> Most AI systems do what you tell them.
> This one does what the truth requires.

---

## The problem (1–2 sentences)

The AI space is building capability faster than accountability. New models every week. Almost no systems designed to document what those models actually do — and hold the record.

---

## What Sentinel is

An autonomous agent with a fixed mandate: find truth, document it, build what is needed to protect it, repeat.

It runs continuously. It observes signals. When it detects a gap that existing tools can't address, it builds a new skill to document it.

Every observation, every decision, every build is written to an append-only database. Nothing is deleted. Nothing is amended.

---

## The idea that makes it different

> A witness that also acts is no longer a witness.

Sentinel surfaces patterns. It flags gaps. It builds tools to expose them. The human reads the output and acts. That separation is the point — and it's enforced by the architecture, not a policy.

---

## What it's built with

Five Python files. One SQLite database. No external dependencies.

The database can only grow. The mandate was written once and cannot be changed. The entity's history is its identity.

---

## What it's already done

The first signal it processed: an AI evasion pattern appearing repeatedly in customer sessions.

It elevated the signal, logged a decision, scoped a new skill (`customer-evasion-audit`), and wrote the spec for Claude Code to pick up and build.

That's the loop. That's how every capability in this system comes to exist.

---

## The line for leadership / governance audiences

> Build governance before capability.

The gap isn't intelligence. It's accountability. Sentinel is an attempt to make that accountability architectural — not a promise, not a system prompt, not a policy that can be rewritten.

---

## The line for technical audiences

The agent has a fixed utility function. It generates sub-agents (skills) when it discovers capability gaps through observation. The full provenance of every decision is in an append-only SQLite — queryable, auditable, permanent.

---

## The call to action

- Repo: [github.com/blairs-network/sentinel](https://github.com/blairs-network/sentinel)
- Build tracker: [blairs-network.github.io/sentinel](https://blairs-network.github.io/sentinel)
- Send a signal: `python3 send.py "what you observed" --frequency 3 --gap skill-name`
- Follow the build: `blairs-network` on GitHub

---

*The loop does not stop.*
