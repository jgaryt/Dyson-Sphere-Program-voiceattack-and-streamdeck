"""Build the Stream Deck profile (.streamDeckProfile) from scripts/layout.py.

Format taken from a profile exported by Stream Deck 7.6.1 for a Stream Deck XL.
Run: python scripts/build_profile.py
"""
import json
import pathlib
import sys
import uuid
import zipfile

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from layout import COLS, PAGES, ROWS  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "profiles" / "DSP Stream Deck XL.streamDeckProfile"
PROFILE_NAME = "Dyson Sphere Program"
DEVICE_MODEL = "20GAT9901"  # Stream Deck XL
DEVICE_UUID = "3886e867-0ea5-45cc-99be-48c57f7d6c07"  # from the sample export; Stream Deck reassigns on import

# Key name -> (QTKeyCode, Windows VKeyCode)
KEYS = {str(d): (48 + d, 48 + d) for d in range(10)}
KEYS.update({chr(c): (c, c) for c in range(ord("A"), ord("Z") + 1)})
KEYS.update({f"F{n}": (16777263 + n, 111 + n) for n in range(1, 13)})
KEYS.update({"Esc": (16777216, 27), "Space": (32, 32)})
# KeyModifiers bits. Shift and Alt confirmed from exports; Alt on its own = modifier with no key.
MODIFIERS = {"Shift": 1, "Alt": 4}
NO_KEY = (33554431, -1)
EMPTY_HOTKEY = {"KeyModifiers": 0, "QTKeyCode": 33554431, "VKeyCode": -1}
# Built-in Stream Deck actions can't click the mouse, so these steps are skipped (see README).
UNSUPPORTED = {"Shift+LeftClick"}

PLUGINS = {
    "hotkey": {"Name": "Activate a Key Command", "UUID": "com.elgato.streamdeck.system.hotkey", "Version": "1.0"},
    "multi": {"Name": "Multi Action", "UUID": "com.elgato.streamdeck.multiactions", "Version": "1.0"},
    "page": {"Name": "Pages", "UUID": "com.elgato.streamdeck.page", "Version": "1.0"},
}


def gid():
    return str(uuid.uuid4())


def hotkey(spec, title=None):
    mods = 0
    parts = spec.split("+")
    if parts[-1] in MODIFIERS:          # a modifier pressed on its own, e.g. "Alt"
        mod_names, (qt, vk) = parts, NO_KEY
    else:
        mod_names, (qt, vk) = parts[:-1], KEYS[parts[-1]]
    for m in mod_names:
        mods |= MODIFIERS[m]
    return {
        "ActionID": gid(), "LinkedTitle": True, "Name": "Hotkey", "Plugin": PLUGINS["hotkey"],
        "Resources": None,
        "Settings": {"Coalesce": True, "Hotkeys": [{"KeyModifiers": mods, "QTKeyCode": qt, "VKeyCode": vk}]
                     + [dict(EMPTY_HOTKEY) for _ in range(3)]},
        "State": 0, "States": [{"Title": title if title is not None else spec}],
        "UUID": "com.elgato.streamdeck.system.hotkey",
    }


def delay(ms):
    return {
        "ActionID": gid(), "LinkedTitle": True, "Name": "Delay", "Plugin": PLUGINS["multi"],
        "Resources": None, "Settings": {"delay": ms}, "State": 0,
        "States": [{"Title": f"{ms}ms"}], "UUID": "com.elgato.streamdeck.multiactions.delay",
    }


def page_action(direction, title):
    return {
        "ActionID": gid(), "LinkedTitle": True,
        "Name": "Next Page" if direction == "next" else "Previous Page",
        "Plugin": PLUGINS["page"], "Resources": None, "Settings": {}, "State": 0,
        "States": [{"Title": title}], "UUID": f"com.elgato.streamdeck.page.{direction}",
    }


def button(label, steps, page_num):
    steps = [s for s in steps if s not in UNSUPPORTED]
    if not steps:
        return None
    if len(steps) == 1 and isinstance(steps[0], tuple) and steps[0][0] == "page":
        return page_action("next" if steps[0][1] > page_num else "previous", label)
    if len(steps) == 1:
        return hotkey(steps[0], label)
    inner = [delay(s[1]) if isinstance(s, tuple) else hotkey(s) for s in steps]
    return {
        "ActionID": gid(), "Actions": [{"Actions": inner}, {"Actions": []}], "LinkedTitle": True,
        "Name": "Multi Action", "Plugin": PLUGINS["multi"], "Resources": None, "Settings": {},
        "State": 0, "States": [{"Title": label}], "UUID": "com.elgato.streamdeck.multiactions.routine",
    }


def page_manifest(actions):
    return {"Controllers": [{"Actions": actions or None, "Type": "Keypad"}], "Icon": "", "Name": ""}


def main():
    profile_id = gid().upper()
    default_page = gid()
    page_ids, files, skipped = [], {}, []
    for num, (_name, buttons) in PAGES.items():
        assert len(buttons) == COLS * ROWS
        actions = {}
        for i, (label, steps) in enumerate(buttons):
            if not label:
                continue
            action = button(label, steps, num)
            if action is None:
                skipped.append(label)
                continue
            actions[f"{i % COLS},{i // COLS}"] = action
        pid = gid()
        page_ids.append(pid)
        files[pid] = page_manifest(actions)
    files[default_page] = page_manifest({})

    base = f"Profiles/{profile_id}.sdProfile"
    package = {
        "AppVersion": "7.6.1.23033", "DeviceModel": DEVICE_MODEL, "DeviceSettings": None,
        "FormatVersion": 1, "OSType": "Windows", "OSVersion": "10.0.22631",
        "RequiredPlugins": ["com.elgato.streamdeck.system.hotkey", "com.elgato.streamdeck.multiactions",
                            "com.elgato.streamdeck.page"],
    }
    root = {
        "Device": {"Model": DEVICE_MODEL, "UUID": DEVICE_UUID}, "Name": PROFILE_NAME,
        "Pages": {"Current": "00000000-0000-0000-0000-000000000000", "Default": default_page,
                  "Pages": page_ids},
        "Version": "3.0",
    }
    OUT.parent.mkdir(exist_ok=True)
    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
        # Same entries as Stream Deck's own export, including the empty folder entries.
        z.writestr("package.json", json.dumps(package, indent=1))
        for folder in ("Profiles/", f"{base}/"):
            z.writestr(folder, "")
        z.writestr(f"{base}/manifest.json", json.dumps(root, indent=1))
        z.writestr(f"{base}/Profiles/", "")
        for pid, man in files.items():
            page = f"{base}/Profiles/{pid.upper()}"
            z.writestr(f"{page}/", "")
            z.writestr(f"{page}/Images/", "")
            z.writestr(f"{page}/manifest.json", json.dumps(man, indent=1))
    print("wrote", OUT)
    if skipped:
        print("skipped (needs a plugin):", ", ".join(skipped))


if __name__ == "__main__":
    main()
