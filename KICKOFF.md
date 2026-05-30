# Claude Code — sentinel Base Entity Kickoff

Paste this into Claude Code from the repo root of `blairs-network/sentinel`.

---

## PROMPT

You are building the base Sentinel entity. Read `soul.md` first. Then read `AGENTS.md`. Those two files are the source of truth. Do not deviate from them.

Your job is to verify, complete, and test the base entity module by module. The core files already exist as stubs. Your job is to make them run correctly and verify each one before moving to the next.

**Build order:**

1. **Initialize memory** — run `memory/schema.sql` against `memory/sentinel.db`. Verify: all four tables exist, insert one row per table, read back correctly.

2. **Verify memory/db.py** — run each function once with test data. Verify: log_observation returns an integer ID, log_signal returns an integer ID, chained call (observation → signal → decision → build) all succeed and relate correctly in the db.

3. **Verify observe.py** — run `observe(cycle=1)` with an empty inbox/. Verify: returns valid dict with empty signals list, capabilities list reflects what's in skills/. Then drop a test signal JSON into inbox/ and run again. Verify: signal is read, moved to inbox/processed/, returned in observation dict.

4. **Verify loop.py** — run 3 cycles manually (set CYCLE_SECONDS_IDLE=5 for testing). Verify: 3 observation rows written to db, no exceptions thrown, cycle count increments correctly.

5. **Verify build.py** — call `scope_build(decision_id=1, skill_name="test-skill", mandate_gap="test gap")`. Verify: decision row written first, skills/test-skill/ directory created, AGENTS.md written inside it, build row written with status "agents_written". Then delete the test skill directory.

6. **End-to-end test** — drop this signal into inbox/test-signal.json and run one loop cycle:
```json
{
  "source": "hermes",
  "timestamp": "2026-05-28T00:00:00Z",
  "pattern": "AI evasion pattern detected in customer sessions",
  "frequency": 4,
  "suggested_gap": "customer-evasion-audit"
}
```
Verify: signal read from inbox, elevated, decision logged as "build", skill directory created at skills/customer-evasion-audit/, AGENTS.md written, build row in db with status "agents_written".

**After each step:** tell me what you ran, what you got, and whether it passed. Then stop and wait.

**If anything is ambiguous:** surface it before writing code. Do not resolve silently.

**What you must not do:**
- Do not modify soul.md under any circumstances
- Do not add UPDATE or DELETE operations to memory/db.py (the one exception is update_build_status which already exists)
- Do not add features beyond what AGENTS.md specifies
- Do not rename or restructure the directory layout

**The entity is alive when loop.py runs 3 cycles without error and writes 3 observation rows to sentinel.db.**

That is the success criterion. Start with step 1.
