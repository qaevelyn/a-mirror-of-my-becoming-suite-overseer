#!/usr/bin/env python3
"""mirror_failsafe.py — fleet-wide resilience module
Owner design rulings, Oct 11 2026: checkpoint worker pairs (radio-in, one at a time),
backup overseer semantics, adaptive armor (threat levels), state-file resume.
Doctrine: the machine fails definitely; the architecture assumes it."""
import os, json, time, socket, urllib.request

OLLS = [11434, 11435]  # primary, backup server
STATE = os.path.expanduser("~/.overseer_state.json")
TZ = time.strftime("%Z")

def now(): return {"z": time.strftime("%H%M") + "Z", "local": time.strftime("%H:%M:%S ") + TZ}

def http_alive(url, timeout=3):
    try:
        urllib.request.urlopen(url, timeout=timeout); return True
    except Exception: return False

def probe_servers():
    """GREEN/ELEVATED/RED from observed reality."""
    alive = [p for p in OLLS if http_alive(f"http://localhost:{p}/api/tags")]
    if len(alive) == 2: return "GREEN", alive
    if len(alive) == 1: return "ELEVATED", alive
    return "RED", alive

def preflight(needs=("~/Mirror-Food/vector-store",)):
    level, servers = probe_servers()
    problems = []
    if not servers: problems.append("no model server on 11434/11435")
    for n in needs:
        if not os.path.exists(os.path.expanduser(n)): problems.append(f"missing {n}")
    try:
        with open(STATE, "a"): pass
    except Exception as e: problems.append(f"state file unwritable: {e}")
    print(f"[PREFLIGHT {now()['z']}] level={level} servers={servers} problems={problems or 'none'}")
    return level, servers, problems

class Checkpoint:
    """Radio-in worker pair: one on duty, silence = replacement steps in."""
    def __init__(self, name): self.name, self.duty_log = name, []
    def radio(self, where, what): self.duty_log.append({**now(), "where": where, "what": what})

def heartbeat(name, stage, note=""):
    """Advancing heartbeat: alive AND progressing. Watchdogs read stage, not just mtime."""
    hb = os.path.expanduser("~/.mirror_heartbeat.jsonl")
    with open(hb, "a") as f:
        f.write(json.dumps({**now(), "who": name, "stage": stage, "note": note}) + "\n")

def save_state(stage, payload):
    tmp = STATE + ".tmp"
    json.dump({"saved": now(), "stage": stage, "payload": payload}, open(tmp, "w"))
    os.replace(tmp, STATE)  # atomic — never a half-written state file

def load_state():
    try: return json.load(open(STATE))
    except Exception: return None

if __name__ == "__main__":
    preflight()
