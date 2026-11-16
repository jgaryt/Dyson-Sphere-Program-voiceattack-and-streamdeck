"""Build the Stream Deck XL profiles (.streamDeckProfile) from data/commands.toml.

Two profiles from the same layout:
  keys - Stream Deck sends the keys itself (no VoiceAttack needed)
  va   - each button runs a VoiceAttack command through the HCS Stream Deck Connector
         plugin (shown in Stream Deck as "VA Streamdeck")

Format matched to profiles exported by Stream Deck 7.6.1 for a Stream Deck XL.
"""
import json
import zipfile

import dsp
from icons import ICON_DIR, filename as icon_file

OUT_DIR = dsp.ROOT / "streamdeck" / "profiles"
VARIANTS = {
    "keys": ("DSP Stream Deck XL.streamDeckProfile", "Dyson Sphere Program"),
    "va": ("DSP Stream Deck XL (VoiceAttack).streamDeckProfile", "Dyson Sphere Program (VoiceAttack)"),
}
DEVICE_MODEL = "20GAT9901"  # Stream Deck XL
DEVICE_UUID = "3886e867-0ea5-45cc-99be-48c57f7d6c07"  # from a sample export; Stream Deck reassigns on import
PREV_COL, NEXT_COL = 7, 8   # bottom-row columns for page switching

# Key name -> (QTKeyCode, Windows VKeyCode)
KEYS = {str(d): (48 + d, 48 + d) for d in range(10)}
KEYS.update({chr(c): (c, c) for c in range(ord("A"), ord("Z") + 1)})
KEYS.update({f"F{n}": (16777263 + n, 111 + n) for n in range(1, 13)})
KEYS.update({"Esc": (16777216, 27), "Space": (32, 32)})
# KeyModifiers bits (from exports). A modifier on its own = modifier with no key.
MODIFIERS = {"Shift": 1, "Alt": 4}
NO_KEY = (33554431, -1)
EMPTY_HOTKEY = {"KeyModifiers": 0, "QTKeyCode": 33554431, "VKeyCode": -1}
# Built-in Stream Deck actions can't click the mouse; these buttons are left out of the keys version.
UNSUPPORTED = {"Shift+LeftClick"}

PLUGINS = {
    "hotkey": {"Name": "Activate a Key Command", "UUID": "com.elgato.streamdeck.system.hotkey", "Version": "1.0"},
    "multi": {"Name": "Multi Action", "UUID": "com.elgato.streamdeck.multiactions", "Version": "1.0"},
    "page": {"Name": "Pages", "UUID": "com.elgato.streamdeck.page", "Version": "1.0"},
    "va": {"Name": "VA Streamdeck", "UUID": "com.finethinking.vastreamdeck", "Version": "1.0.8"},
}
VA_CONTEXT = "5e96c48814cd150165d6072828e0901e"     # copied from a working export
VA_ICON = "actions/CustomAction/HCSAction.jpg"


# IDs are derived from what they belong to, so the same data builds identical profiles.
_seed, _count = "", 0


def seed_ids(*parts):
    global _seed, _count
    _seed, _count = "|".join(str(p) for p in parts), 0


def gid():
    global _count
    _count += 1
    return dsp.stable_id("sd", _seed, _count)


ZIP_TIME = (2024, 1, 1, 0, 0, 0)   # fixed timestamp inside the zip, for repeatable builds


def zwrite(z, name, data=b""):
    info = zipfile.ZipInfo(name, date_time=ZIP_TIME)
    info.compress_type = zipfile.ZIP_DEFLATED
    z.writestr(info, data)


def hotkey(spec, title):
    parts = spec.split("+")
    if parts[-1] in MODIFIERS:
        mod_names, (qt, vk) = parts, NO_KEY
    else:
        mod_names, (qt, vk) = parts[:-1], KEYS[parts[-1]]
    mods = 0
    for m in mod_names:
        mods |= MODIFIERS[m]
    return {
        "ActionID": gid(), "LinkedTitle": True, "Name": "Hotkey", "Plugin": PLUGINS["hotkey"],
        "Resources": None,
        "Settings": {"Coalesce": True, "Hotkeys": [{"KeyModifiers": mods, "QTKeyCode": qt, "VKeyCode": vk}]
                     + [dict(EMPTY_HOTKEY) for _ in range(3)]},
        "State": 0, "States": [{"Title": title}], "UUID": "com.elgato.streamdeck.system.hotkey",
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


def va_command(label, phrase):
    return {
        "ActionID": gid(), "LinkedTitle": True, "Name": "Custom Command", "Plugin": PLUGINS["va"],
        "Resources": None,
        "Settings": {"context": VA_CONTEXT, "event": "setSettings",
                     "payload": {"command": phrase, "iconPath": VA_ICON, "title": label}},
        "State": 0, "States": [{"Title": label}], "UUID": "com.finethinking.vastreamdeck.customaction",
    }


def key_button(label, steps):
    steps = [s for s in steps if s not in UNSUPPORTED]
    if not steps:
        return None
    if len(steps) == 1:
        return hotkey(steps[0], label)
    inner = [delay(int(s[5:])) if s.startswith("wait:") else hotkey(s, s) for s in steps]
    return {
        "ActionID": gid(), "Actions": [{"Actions": inner}, {"Actions": []}], "LinkedTitle": True,
        "Name": "Multi Action", "Plugin": PLUGINS["multi"], "Resources": None, "Settings": {},
        "State": 0, "States": [{"Title": label}], "UUID": "com.elgato.streamdeck.multiactions.routine",
    }


def layout(entries):
    """{page: {(col, row): (label, entry or None)}} with the shared bottom row and page buttons."""
    page_nums = dsp.pages(entries)
    grid = {p: {} for p in page_nums}
    for e in entries:
        d = e.get("deck")
        if not d:
            continue
        if d["row"] == "bottom":
            for p in page_nums:
                grid[p][(d["col"], dsp.BOTTOM)] = (d["label"], e)
        else:
            grid[d["page"]][(d["col"], d["row"])] = (d["label"], e)
    for i, p in enumerate(page_nums):
        if i > 0:
            grid[p][(PREV_COL, dsp.BOTTOM)] = ("Prev", None)
        if i < len(page_nums) - 1:
            grid[p][(NEXT_COL, dsp.BOTTOM)] = ("Next", None)
    return grid


def build_variant(entries, variant):
    filename, profile_name = VARIANTS[variant]
    page_ids, files, images, skipped = [], {}, {}, set()
    for page, cells in layout(entries).items():
        actions, pid = {}, dsp.stable_id("sd-page", variant, page)
        for (col, row), (label, e) in sorted(cells.items()):
            seed_ids(variant, page, col, row, label)
            if e is None:
                action = page_action("previous" if label == "Prev" else "next", label)
            elif variant == "va":
                action = va_command(label, e["deck"]["say"])
            else:
                action = key_button(label, e["steps"])
                if action is None:
                    skipped.add(label)
                    continue
            icon = ICON_DIR / icon_file(label)
            if icon.exists():
                # The icon already shows the label, so hide Stream Deck's own title text.
                action["States"][0].update({"Image": f"Images/{icon.name}", "ShowTitle": False})
                images.setdefault(pid, []).append(icon)
            actions[f"{col - 1},{row - 1}"] = action
        page_ids.append(pid)
        files[pid] = {"Controllers": [{"Actions": actions or None, "Type": "Keypad"}], "Icon": "", "Name": ""}
    default_page = dsp.stable_id("sd-default-page", variant)
    files[default_page] = {"Controllers": [{"Actions": None, "Type": "Keypad"}], "Icon": "", "Name": ""}

    base = f"Profiles/{dsp.stable_id('sd-profile', variant).upper()}.sdProfile"
    package = {
        "AppVersion": "7.6.1.23033", "DeviceModel": DEVICE_MODEL, "DeviceSettings": None,
        "FormatVersion": 1, "OSType": "Windows", "OSVersion": "10.0.22631",
        "RequiredPlugins": (["com.finethinking.vastreamdeck", "com.elgato.streamdeck.page"] if variant == "va"
                            else ["com.elgato.streamdeck.system.hotkey", "com.elgato.streamdeck.multiactions",
                                  "com.elgato.streamdeck.page"]),
    }
    root = {
        "Device": {"Model": DEVICE_MODEL, "UUID": DEVICE_UUID}, "Name": profile_name,
        "Pages": {"Current": "00000000-0000-0000-0000-000000000000", "Default": default_page, "Pages": page_ids},
        "Version": "3.0",
    }
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(OUT_DIR / filename, "w", zipfile.ZIP_DEFLATED) as z:
        # Same entries as Stream Deck's own export, including the empty folder entries.
        zwrite(z, "package.json", json.dumps(package, indent=1))
        for folder in ("Profiles/", f"{base}/"):
            zwrite(z, folder)
        zwrite(z, f"{base}/manifest.json", json.dumps(root, indent=1))
        zwrite(z, f"{base}/Profiles/")
        for pid, man in files.items():
            page = f"{base}/Profiles/{pid.upper()}"
            zwrite(z, f"{page}/")
            zwrite(z, f"{page}/Images/")
            for icon in images.get(pid, []):
                zwrite(z, f"{page}/Images/{icon.name}", icon.read_bytes())
            zwrite(z, f"{page}/manifest.json", json.dumps(man, indent=1))
    note = f", left out (needs a mouse plugin): {', '.join(sorted(skipped))}" if skipped else ""
    print(f"wrote streamdeck/profiles/{filename}{note}")


def build(entries):
    for variant in VARIANTS:
        build_variant(entries, variant)


if __name__ == "__main__":
    build(dsp.load())
