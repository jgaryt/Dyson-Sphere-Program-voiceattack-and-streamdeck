"""Shared helpers: load data/commands.toml and check it.

Every other script imports this. Nothing here writes files.
"""
import itertools
import pathlib
import re
import tomllib

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "commands.toml"

COLS, ROWS = 8, 4           # Stream Deck XL
BOTTOM = ROWS               # row 4 is the shared bottom row
BAR_WAIT_MS = 100           # pause between bar keys in build commands
BUILD_PREFIX = "[build;place;] "
KINDS = ("building", "action", "panel", "slot")


def load():
    """Return every entry as a dict with `kind` added and `steps` filled in for buildings."""
    with open(DATA, "rb") as f:
        raw = tomllib.load(f)
    unknown = set(raw) - set(KINDS)
    if unknown:
        raise SystemExit(f"commands.toml: unknown section(s) {sorted(unknown)}")
    entries = []
    for kind in KINDS:
        for e in raw.get(kind, []):
            e = dict(e, kind=kind)
            if kind == "building":
                e["steps"] = build_steps(e["bar"], e["key"])
            entries.append(e)
    return entries


def commands(entries):
    """Entries that become voice commands (have a phrase)."""
    return [e for e in entries if e.get("phrase")]


def build_steps(bar, key):
    """DSP's bar keys toggle, so press a *different* bar first, then the wanted bar, then the F-key."""
    first = 8 if bar == 9 else 9
    return [str(first), f"wait:{BAR_WAIT_MS}", str(bar), f"wait:{BAR_WAIT_MS}", key]


def spoken_phrase(e):
    """Full VoiceAttack phrase. Buildings also accept 'build'/'place' in front."""
    return (BUILD_PREFIX if e["kind"] == "building" else "") + e["phrase"]


def expand(phrase):
    """Every sentence a VoiceAttack phrase accepts: '[a;b] c' -> {'a c', 'b c'}."""
    parts = re.split(r"(\[[^\]]*\])", phrase)
    opts = [p[1:-1].split(";") if p.startswith("[") else [p] for p in parts]
    return {" ".join("".join(c).split()).lower() for c in itertools.product(*opts)}


def keys_text(e):
    """Human-readable keys, e.g. '1 → F4' or 'Shift + F11'."""
    if e["kind"] in ("building", "slot"):
        return f"{e['bar']} → {e['key']}"
    out = []
    for s in e["steps"]:
        if s.startswith("wait:"):
            continue
        out.append(s.replace("+", " + ").replace("LeftClick", "Left Click"))
    return ", ".join(out)


def check(entries):
    """Fail loudly on anything that would break a profile. Returns a list of problems."""
    problems = []
    cmds = commands(entries)
    spoken = {}
    for e in cmds:
        for s in expand(spoken_phrase(e)):
            if s in spoken and spoken[s] != e["name"]:
                problems.append(f"'{s}' is a phrase for both {spoken[s]} and {e['name']}")
            spoken[s] = e["name"]
    for e in cmds:
        for line in e.get("reply", []):
            if line.strip().lower() in spoken:
                problems.append(f"{e['name']}: reply '{line}' matches a voice command (feedback loop)")
        deck = e.get("deck")
        if deck and deck.get("say", "").lower() not in spoken:
            problems.append(f"{e['name']}: deck say '{deck.get('say')}' matches no voice command")
    seen = {}
    for e in entries:
        d = e.get("deck")
        if not d:
            continue
        if d.get("row") == "bottom":
            spots = [(p, BOTTOM, d["col"]) for p in pages(entries)]
        else:
            if not (1 <= d["row"] < BOTTOM and 1 <= d["col"] <= COLS):
                problems.append(f"{e['name']}: deck position row {d['row']} col {d['col']} is off the grid")
            spots = [(d["page"], d["row"], d["col"])]
        for spot in spots:
            if spot in seen:
                problems.append(f"{e['name']} and {seen[spot]} share deck page {spot[0]} row {spot[1]} col {spot[2]}")
            seen[spot] = e["name"]
        if d.get("row") == "bottom" and d["col"] >= COLS - 1:
            problems.append(f"{e['name']}: bottom-row columns 7-8 are reserved for Prev/Next")
    return problems


def pages(entries):
    return sorted({e["deck"]["page"] for e in entries if e.get("deck") and "page" in e["deck"]})
