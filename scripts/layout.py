"""Stream Deck XL (8 x 4) layout for Dyson Sphere Program.

Each button is (label, steps). Steps run in order:
  "9"            press and release a key
  "Shift+F11"    press a key while holding a modifier
  ("wait", 100)  pause in milliseconds
  ("page", 2)    switch to another page of this profile

Build buttons use the same trick as the VoiceAttack profile: DSP's bar keys toggle,
so press a *different* bar first, then the wanted bar, then the F-key.

Run `python scripts/layout.py` to regenerate docs/layout.md.
"""

COLS, ROWS = 8, 4
WAIT = ("wait", 100)


def build(bar, fkey):
    """Steps that select a building on build bar `bar` (1-9) at F-key `fkey`."""
    first = "8" if bar == 9 else "9"
    return [first, WAIT, str(bar), WAIT, fkey]


def key(*steps):
    return list(steps)


PAGES = {
    1: ("Build", [
        # Row 1: power and collecting
        ("Tesla", build(1, "F1")), ("Wireless", build(1, "F2")), ("Wind", build(1, "F4")),
        ("Thermal", build(1, "F5")), ("Solar", build(1, "F6")), ("Geo", build(1, "F7")),
        ("Miner", build(2, "F1")), ("Pump", build(2, "F3")),
        # Row 2: oil and logistics
        ("Oil", build(2, "F4")), ("Belt 1", build(3, "F1")), ("Belt 2", build(3, "F2")),
        ("Belt 3", build(3, "F3")), ("Sort 1", build(3, "F4")), ("Sort 2", build(3, "F5")),
        ("Sort 3", build(3, "F6")), ("Split", build(3, "F8")),
        # Row 3: logistics, storage, production
        ("Monitor", build(3, "F9")), ("Spray", build(3, "F10")), ("Depot 1", build(4, "F1")),
        ("Depot 2", build(4, "F2")), ("Tank", build(4, "F3")), ("Smelter", build(5, "F1")),
        ("Asm 1", build(5, "F3")), ("Asm 2", build(5, "F4")),
        # Row 4: production, research, foundation, defence, page switch
        ("Refinery", build(5, "F6")), ("Chem", build(5, "F7")), ("Lab", build(8, "F1")),
        ("Found", build(9, "F1")), ("Gauss", build(7, "F1")), ("Missile", build(7, "F2")),
        ("Implosion", build(7, "F3")), ("Actions >", key(("page", 2))),
    ]),
    2: ("Actions", [
        # Row 1: modes and movement
        ("Cancel", key("Esc")), ("Upgrade", key("U")), ("Dismantle", key("X")),
        ("Copy", key("Shift+LeftClick")), ("Fly", key("Space", WAIT, "Space")),
        ("Land", key("Alt")), ("North", key("N")), ("Screenshot", key("Shift+F11")),
        # Row 2: panels
        ("Mecha", key("C")), ("Stats", key("P")), ("Inventory", key("E")),
        ("Replicator", key("F")), ("Details", key("H")), ("Tech", key("T")),
        ("Logistics", key("I")), ("Starmap", key("V")),
        # Row 3: views and remaining defence
        ("Planet", key("M")), ("Jammer", build(7, "F8")), ("Signal", build(7, "F9")),
        ("Substation", build(1, "F3")), ("Fusion", build(1, "F8")), ("Accum", build(1, "F9")),
        (None, []), (None, []),
        # Row 4: page switch
        ("< Build", key(("page", 1))), ("Distrib", build(6, "F1")), ("Piler", build(6, "F2")),
        ("PLS", build(6, "F3")), ("ILS", build(6, "F4")), ("Ejector", build(8, "F2")),
        ("Receiver", build(8, "F3")), (None, []),
    ]),
}


# VoiceAttack phrase for each button, used by the VoiceAttack version of the profile.
# Each must match a command in the VoiceAttack profile (see scripts/check_va_phrases.py).
# Page-switch buttons stay native Stream Deck actions.
VA_PHRASES = {
    "Tesla": "tesla tower", "Wireless": "wireless tower", "Wind": "wind turbine",
    "Thermal": "thermal plant", "Solar": "solar panel", "Geo": "geothermal",
    "Miner": "miner", "Pump": "water pump", "Oil": "oil extractor",
    "Belt 1": "belt one", "Belt 2": "belt two", "Belt 3": "belt three",
    "Sort 1": "sorter one", "Sort 2": "sorter two", "Sort 3": "sorter three",
    "Split": "splitter", "Monitor": "traffic monitor", "Spray": "spray coater",
    "Depot 1": "depot one", "Depot 2": "depot two", "Tank": "storage tank",
    "Smelter": "smelter", "Asm 1": "assembler one", "Asm 2": "assembler two",
    "Refinery": "refinery", "Chem": "chemical plant", "Lab": "matrix lab",
    "Found": "foundation", "Gauss": "gauss turret", "Missile": "missile turret",
    "Implosion": "implosion cannon", "Jammer": "jammer tower", "Signal": "signal tower",
    "Cancel": "cancel", "Upgrade": "upgrade", "Dismantle": "dismantle", "Copy": "copy",
    "Fly": "fly", "Land": "land", "North": "face north", "Screenshot": "screenshot",
    "Mecha": "mecha", "Stats": "statistics", "Inventory": "inventory",
    "Replicator": "replicator", "Details": "details display", "Tech": "tech tree",
    "Logistics": "logistics", "Starmap": "starmap", "Planet": "planet",
    "Substation": "substation", "Fusion": "fusion plant", "Accum": "accumulator",
    "Distrib": "distributor", "Piler": "piler", "PLS": "planetary station",
    "ILS": "interstellar station", "Ejector": "rail ejector", "Receiver": "ray receiver",
}


def describe(steps):
    out = []
    for s in steps:
        if isinstance(s, tuple):
            out.append(f"wait {s[1]} ms" if s[0] == "wait" else f"go to page {s[1]}")
        else:
            out.append(s)
    return " → ".join(out)


def markdown():
    lines = ["# Stream Deck XL layout", "",
             "Generated by `scripts/layout.py`, so don't edit this file by hand.", ""]
    for num, (name, buttons) in PAGES.items():
        assert len(buttons) == COLS * ROWS, f"page {num} has {len(buttons)} buttons"
        lines += [f"## Page {num}: {name}", "",
                  "| " + " | ".join(f"Col {c + 1}" for c in range(COLS)) + " |",
                  "|" + "---|" * COLS]
        for r in range(ROWS):
            row = buttons[r * COLS:(r + 1) * COLS]
            lines.append("| " + " | ".join(f"**{b[0]}**" if b[0] else "" for b in row) + " |")
        lines += ["", "| Button | Steps |", "|---|---|"]
        lines += [f"| {b[0]} | {describe(b[1])} |" for b in buttons if b[0]]
        lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    import pathlib
    path = pathlib.Path(__file__).resolve().parent.parent / "docs" / "layout.md"
    path.parent.mkdir(exist_ok=True)
    path.write_text(markdown(), encoding="utf-8")
    print("wrote", path)
