"""Check every VA_PHRASES entry matches a command in the VoiceAttack profile.

Usage: python scripts/check_va_phrases.py "path/to/DSP Build Hotkeys-Profile.vap"
(the generated, uncompressed .vap from the DysonSphereProgram-VoiceAttack-Profile repo)
"""
import itertools
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from layout import PAGES, VA_PHRASES  # noqa: E402


def expand(phrase):
    parts = re.split(r"(\[[^\]]*\])", phrase)
    opts = [p[1:-1].split(";") if p.startswith("[") else [p] for p in parts]
    return {" ".join("".join(c).split()).lower() for c in itertools.product(*opts)}


def main(vap):
    text = pathlib.Path(vap).read_text(encoding="utf-8")
    spoken = set()
    for cmd in re.findall(r"<CommandString>(.*?)</CommandString>", text):
        spoken |= expand(cmd)
    labels = {b[0] for _, buttons in PAGES.values() for b in buttons
              if b[0] and not any(isinstance(s, tuple) and s[0] == "page" for s in b[1])}
    bad = [f"{k}: '{v}'" for k, v in VA_PHRASES.items() if v.lower() not in spoken]
    missing = sorted(labels - VA_PHRASES.keys())
    if bad or missing:
        print("No matching VoiceAttack command:", *bad, sep="\n  ") if bad else None
        print("Buttons without a phrase:", missing) if missing else None
        sys.exit(1)
    print(f"All {len(VA_PHRASES)} phrases match a VoiceAttack command.")


if __name__ == "__main__":
    main(sys.argv[1])
