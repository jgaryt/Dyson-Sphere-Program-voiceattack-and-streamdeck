"""Generate docs/command-map.csv and docs/layout.md from data/commands.toml."""
import csv

import dsp
from build_streamdeck import layout

BAR_NAMES = {1: "Power", 2: "Collecting", 3: "Logistics", 4: "Storage", 5: "Production",
             6: "Transportation", 7: "Defence", 8: "COSMO", 9: "Foundation"}


def fkey_num(k):
    return int(k[1:])


def command_map(entries):
    bars = sorted((e for e in entries if e["kind"] in ("building", "slot")),
                  key=lambda e: (e["bar"], fkey_num(e["key"])))
    others = [e for e in entries if e["kind"] in ("action", "panel")]
    path = dsp.ROOT / "docs" / "command-map.csv"
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["Name", "Keys", "Group", "Voice command", "Icarus reply", "Deck label",
                    "Deck position", "Status", "Notes"])
        for e in bars + others:
            d = e.get("deck") or {}
            if not d:
                pos = ""
            elif d["row"] == "bottom":
                pos = f"bottom row, col {d['col']} (every page)"
            else:
                pos = f"page {d['page']}, row {d['row']}, col {d['col']}"
            group = f"{e['bar']} {BAR_NAMES[e['bar']]}" if "bar" in e else e["kind"].title()
            w.writerow([e["name"], dsp.keys_text(e), group,
                        dsp.spoken_phrase(e) if e.get("phrase") else "",
                        " / ".join(e.get("reply", [])), d.get("label", ""), pos,
                        e["status"].title(), e.get("note", "")])
    print("wrote docs/command-map.csv")


def layout_doc(entries):
    lines = ["# Stream Deck XL layout", "",
             "Generated from `data/commands.toml` by `scripts/build_docs.py`, so don't edit by hand.",
             "", "The bottom row is the same on every page. Prev and Next switch pages.", ""]
    for page, cells in layout(entries).items():
        lines += [f"## Page {page}", "",
                  "| " + " | ".join(f"Col {c}" for c in range(1, dsp.COLS + 1)) + " |",
                  "|" + "---|" * dsp.COLS]
        for row in range(1, dsp.ROWS + 1):
            lines.append("| " + " | ".join(
                f"**{cells[(c, row)][0]}**" if (c, row) in cells else "" for c in range(1, dsp.COLS + 1)) + " |")
        lines.append("")
    (dsp.ROOT / "docs" / "layout.md").write_text("\n".join(lines), encoding="utf-8")
    print("wrote docs/layout.md")


def build(entries):
    command_map(entries)
    layout_doc(entries)


if __name__ == "__main__":
    build(dsp.load())
