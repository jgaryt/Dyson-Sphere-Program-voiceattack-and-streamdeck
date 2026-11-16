"""Check data/commands.toml, then build everything from it.

    python scripts/build_all.py           check + build
    python scripts/build_all.py --check   check only

Builds: Stream Deck icons, VoiceAttack profiles, Stream Deck profiles, docs/command-map.csv,
docs/layout.md and docs/icons-preview.png. Needs Python 3.11+ and Pillow.
"""
import sys

import dsp


def main():
    entries = dsp.load()
    problems = dsp.check(entries)
    if problems:
        print("commands.toml has problems:")
        print("\n".join(f"  - {p}" for p in problems))
        sys.exit(1)
    n = len(dsp.commands(entries))
    print(f"ok: {n} commands, no reply matches a command, every deck phrase matches a command")
    if "--check" in sys.argv:
        return
    import build_docs, build_streamdeck, build_voiceattack, icons
    icons.build(entries)           # icons first: the Stream Deck profiles embed them
    build_voiceattack.build(entries)
    build_streamdeck.build(entries)
    build_docs.build(entries)


if __name__ == "__main__":
    main()
