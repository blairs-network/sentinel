"""
loop.py — Sentinel's core running process.

Observe → Evaluate → Decide → (Build) → Log → Sleep. Repeat.

This process does not stop. Every cycle is logged. Every exception is caught and logged.
The loop is the entity being alive.
"""

import time
import json
import traceback
from datetime import datetime, timezone
from pathlib import Path

from observe import observe
from build import scope_build
from memory.db import init_db, log_observation, log_signal, log_decision, get_db

CYCLE_SECONDS_IDLE = 900       # 15 minutes when nothing is happening
CYCLE_SECONDS_ACTIVE = 60      # 1 minute when signals are present
SIGNAL_FREQUENCY_THRESHOLD = 3 # How many times a pattern must appear before action


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def evaluate(observation: dict, cycle: int) -> list[dict]:
    """
    Given an observation, return a list of signals that warrant attention.
    A signal is elevated when a pattern has appeared frequently enough.
    """
    signals = []
    for raw_signal in observation.get("signals", []):
        if raw_signal.get("frequency", 1) >= SIGNAL_FREQUENCY_THRESHOLD:
            signals.append(raw_signal)
    return signals


def decide(signal: dict) -> dict:
    """
    Given a signal, decide what to do.
    Returns a decision dict with keys: decision, rationale, action.

    Current decision tree is simple. It grows as Sentinel grows.
    """
    gap = signal.get("suggested_gap")

    if gap:
        return {
            "decision": "build",
            "rationale": f"Pattern '{signal['pattern']}' appeared {signal['frequency']} times. Gap identified: {gap}",
            "action": gap
        }
    else:
        return {
            "decision": "watch",
            "rationale": f"Pattern '{signal['pattern']}' is elevated but gap not yet clear. Continue observing.",
            "action": None
        }


def run():
    init_db()
    cycle = 0
    print(f"[{now()}] Sentinel is running. Mandate: find truth, document it, build what is needed.")

    while True:
        cycle += 1
        print(f"[{now()}] Cycle {cycle} — observing.")

        try:
            # 1. Observe
            observation = observe(cycle)
            obs_id = log_observation(
                ts=now(),
                source=observation.get("source", "loop"),
                content=json.dumps(observation),
                cycle=cycle
            )

            # 2. Evaluate
            signals = evaluate(observation, cycle)

            if not signals:
                print(f"[{now()}] Cycle {cycle} — nothing elevated. Sleeping {CYCLE_SECONDS_IDLE}s.")
                time.sleep(CYCLE_SECONDS_IDLE)
                continue

            # 3. For each signal: decide and act
            for signal in signals:
                sig_id = log_signal(
                    ts=now(),
                    observation_id=obs_id,
                    pattern=signal["pattern"],
                    frequency=signal["frequency"]
                )

                decision = decide(signal)

                dec_id = log_decision(
                    ts=now(),
                    signal_id=sig_id,
                    decision=decision["decision"],
                    rationale=decision["rationale"],
                    action=decision.get("action")
                )

                print(f"[{now()}] Decision: {decision['decision']} — {decision['rationale']}")

                # 4. Build if warranted
                if decision["decision"] == "build" and decision["action"]:
                    scope_build(
                        decision_id=dec_id,
                        skill_name=decision["action"].lower().replace(" ", "-"),
                        mandate_gap=decision["action"]
                    )

            print(f"[{now()}] Cycle {cycle} — complete. Sleeping {CYCLE_SECONDS_ACTIVE}s.")
            time.sleep(CYCLE_SECONDS_ACTIVE)

        except Exception:
            error = traceback.format_exc()
            print(f"[{now()}] Cycle {cycle} — exception caught. Logging. Continuing.\n{error}")
            try:
                log_observation(
                    ts=now(),
                    source="loop_error",
                    content=error,
                    cycle=cycle
                )
            except Exception:
                pass  # If we can't log, we still continue.
            time.sleep(CYCLE_SECONDS_IDLE)


if __name__ == "__main__":
    run()
