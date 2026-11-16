"""Shared helpers: load data/commands.toml and check it.

Every other script imports this. Nothing here writes files.
"""
import itertools
import pathlib
import re
import tomllib
import uuid

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "commands.toml"
KEYBINDS = ROOT / "data" / "keybinds.toml"

COLS, ROWS = 8, 4           # Stream Deck XL
BOTTOM = ROWS               # row 4 is the shared bottom row
BAR_WAIT_MS = 100           # pause between bar keys in build commands
BUILD_PREFIX = "[build;place;] "
KINDS = ("building", "action", "panel", "slot")


# DSP's default key for each control. commands.toml is written with these keys;
# data/keybinds.toml can override any of them.
DEFAULT_KEYS = {
    **{f"bar{n}": str(n) for n in range(1, 10)},
    **{f"slot{n}": f"F{n}" for n in range(1, 11)},
    "cancel": "Esc", "upgrade": "U", "dismantle": "X", "copy": "Shift+LeftClick",
    "fly": "Space", "land": "Alt", "face_north": "N", "screenshot": "Shift+F11",
    "mecha": "C", "statistics": "P", "inventory": "E", "replicator": "F", "details": "H",
    "tech_tree": "T", "logistics": "I", "starmap": "V", "planet": "M",
}
SINGLE_KEYS = ({str(d) for d in range(10)} | {chr(c) for c in range(ord("A"), ord("Z") + 1)}
               | {f"F{n}" for n in range(1, 13)} | {"Esc", "Space", "Alt"})
MODIFIER_KEYS = {"Shift", "Alt"}


def key_supported(k):
    """Keys both VoiceAttack and Stream Deck profiles can send: single keys, or Shift/Alt + key/click."""
    if k in SINGLE_KEYS:
        return True
    mod, _, target = k.partition("+")
    return mod in MODIFIER_KEYS and (target in SINGLE_KEYS - {"Alt"} or target == "LeftClick")


def keybinds():
    """{control: key} after applying data/keybinds.toml overrides."""
    bound = dict(DEFAULT_KEYS)
    if KEYBINDS.exists():
        with open(KEYBINDS, "rb") as f:
            custom = tomllib.load(f).get("keys", {})
        unknown = set(custom) - set(DEFAULT_KEYS)
        if unknown:
            raise SystemExit(f"keybinds.toml: unknown control(s) {sorted(unknown)}; "
                             f"valid: {', '.join(DEFAULT_KEYS)}")
        bound.update(custom)
    return bound


def remap_table():
    """{default key: your key} for every control you've rebound."""
    return {DEFAULT_KEYS[c]: k for c, k in keybinds().items() if k != DEFAULT_KEYS[c]}


# Generated IDs are derived from content, so the same data always builds byte-identical profiles.
_ID_NAMESPACE = uuid.UUID("6f1c2a52-4d0e-4b8e-9a51-0d5b2e7c3f10")


def stable_id(*parts):
    return str(uuid.uuid5(_ID_NAMESPACE, "|".join(str(p) for p in parts)))


def load():
    """Return every entry as a dict with `kind` added and `steps` filled in for buildings."""
    with open(DATA, "rb") as f:
        raw = tomllib.load(f)
    unknown = set(raw) - set(KINDS)
    if unknown:
        raise SystemExit(f"commands.toml: unknown section(s) {sorted(unknown)}")
    remap = remap_table()
    entries = []
    for kind in KINDS:
        for e in raw.get(kind, []):
            e = dict(e, kind=kind)
            if kind == "building":
                e["steps"] = build_steps(e["bar"], e["key"])
            if "steps" in e:
                e["steps"] = [remap.get(s, s) for s in e["steps"]]
            if kind in ("building", "slot"):
                e["keys_shown"] = f"{remap.get(str(e['bar']), str(e['bar']))} → {remap.get(e['key'], e['key'])}"
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
        return e["keys_shown"]
    out = []
    for s in e["steps"]:
        if s.startswith("wait:"):
            continue
        out.append(s.replace("+", " + ").replace("LeftClick", "Left Click"))
    return ", ".join(out)


def check(entries):
    """Fail loudly on anything that would break a profile. Returns a list of problems."""
    problems = []
    bound = keybinds()
    used = {}
    for control, key in bound.items():
        if not key_supported(key):
            problems.append(f"keybinds: {control} = '{key}' isn't a key the profiles can send")
        if key in used:
            problems.append(f"keybinds: {control} and {used[key]} are both on '{key}'")
        used[key] = control
    for e in entries:
        for step in e.get("steps", []):
            if not step.startswith("wait:") and not key_supported(step):
                problems.append(f"{e['name']}: step '{step}' isn't a supported key")
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
