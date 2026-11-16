"""Check that the committed profiles and docs are up to date with data/commands.toml.

Rebuilds everything in place, then compares against the last commit (HEAD):
  - VoiceAttack profiles and the text docs must match byte for byte.
  - Stream Deck profiles must have the same buttons (positions, titles, keys, phrases, icon
    names). Icon image bytes are not compared: they can differ slightly between computers.
  - The set of icon files must match.

Exit code 1 means: run `python scripts/build_all.py` and commit the result.
Used by .github/workflows/verify.yml; you can also run it locally.
"""
import json
import subprocess
import sys
import zipfile
from io import BytesIO

import dsp

EXACT = ["voiceattack/profiles", "docs/command-map.csv", "docs/layout.md"]
DECKS = "streamdeck/profiles"


def git(*args, binary=False):
    out = subprocess.run(["git", *args], cwd=dsp.ROOT, capture_output=True, check=True).stdout
    return out if binary else out.decode()


def deck_summary(data):
    """Buttons per page, ignoring IDs and image bytes."""
    z = zipfile.ZipFile(BytesIO(data))
    names = z.namelist()
    root_name = next(n for n in names if n.count("/") == 2 and n.endswith("manifest.json"))
    root = json.loads(z.read(root_name))
    pages = []
    for pid in root["Pages"]["Pages"]:
        man = next(n for n in names if pid.upper() in n and n.endswith("manifest.json"))
        actions = json.loads(z.read(man))["Controllers"][0]["Actions"] or {}
        page = {}
        for pos, a in sorted(actions.items()):
            s = a.get("Settings", {})
            inner = [(i["UUID"], i["Settings"]) for i in a["Actions"][0]["Actions"]] if a.get("Actions") else None
            page[pos] = (a["UUID"], a["States"][0].get("Title"), a["States"][0].get("Image"),
                         s.get("Hotkeys"), s.get("payload", {}).get("command"), inner)
        pages.append(page)
    return root["Name"], pages


def main():
    import build_all
    sys.argv = [sys.argv[0]]
    build_all.main()
    problems = []

    changed = git("diff", "--name-only", "--", *EXACT).split()
    problems += [f"{f} is out of date" for f in changed]

    for f in sorted((dsp.ROOT / DECKS).glob("*.streamDeckProfile")):
        rel = f.relative_to(dsp.ROOT).as_posix()
        try:
            committed = git("show", f"HEAD:{rel}", binary=True)
        except subprocess.CalledProcessError:
            problems.append(f"{rel} is new and not committed")
            continue
        if deck_summary(committed) != deck_summary(f.read_bytes()):
            problems.append(f"{rel} has different buttons than the data says")

    committed_icons = set(git("ls-tree", "--name-only", "HEAD", "streamdeck/icons/").split())
    built_icons = {p.relative_to(dsp.ROOT).as_posix() for p in (dsp.ROOT / "streamdeck/icons").glob("*.png")}
    problems += [f"icon missing from commit: {p}" for p in sorted(built_icons - committed_icons)]
    problems += [f"icon no longer used: {p}" for p in sorted(committed_icons - built_icons)]

    if problems:
        print("\nGenerated files don't match data/commands.toml:")
        print("\n".join(f"  - {p}" for p in problems))
        print("\nFix: run `python scripts/build_all.py` and commit the result.")
        sys.exit(1)
    print("\nverified: committed profiles, icons and docs match data/commands.toml")


if __name__ == "__main__":
    main()
