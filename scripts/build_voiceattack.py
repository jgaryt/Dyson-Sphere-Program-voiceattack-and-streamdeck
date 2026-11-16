"""Build the VoiceAttack profiles (.vap) from data/commands.toml.

Writes one profile per voice in VARIANTS. VoiceAttack imports this uncompressed XML format.
"""
import uuid
from xml.sax.saxutils import escape

import dsp

OUT_DIR = dsp.ROOT / "voiceattack" / "profiles"
PROFILE_NAME = "Dyson Sphere Program - Build Hotkeys"
# One profile per voice: (file name, TTS voice or "" for the Windows default, name suffix)
VARIANTS = [
    ("DSP Build Hotkeys-Profile.vap", "[Azure] Grant MAI-Voice-2.1-Flash (en-US)", ""),
    ("DSP Build Hotkeys-LocalVoice-Profile.vap", "", " (local voice)"),
]
MODIFIER_HOLD = 0.05    # seconds a modifier is held before and after the key/click

# Windows virtual-key codes
CODES = {str(d): 48 + d for d in range(10)}
CODES.update({chr(c): c for c in range(ord("A"), ord("Z") + 1)})
CODES.update({f"F{n}": 111 + n for n in range(1, 13)})
CODES.update({"Esc": 27, "Space": 32, "Alt": 164, "Shift": 160})   # Alt/Shift = left keys


def gid():
    return str(uuid.uuid4())


def action(kind, ordinal, duration=0, keycode=None, context=None, voice_slot=False):
    keys = f"<KeyCodes><unsignedShort>{keycode}</unsignedShort></KeyCodes>" if keycode is not None else "<KeyCodes />"
    ctx = f"<Context>{escape(context)}</Context>" if context is not None else "<Context />"
    extra = "\n          <Context2>{VOICE}</Context2>\n          <X>100</X>\n          <Y>0</Y>" if voice_slot else ""
    return f"""        <CommandAction>
          <Ordinal>{ordinal}</Ordinal>
          <Id>{gid()}</Id>
          <ActionType>{kind}</ActionType>
          <Duration>{duration}</Duration>
          <Delay>0</Delay>
          {keys}
          {ctx}{extra}
          <Disabled>false</Disabled>
        </CommandAction>
"""


def actions_for(e):
    """Speech first, so Icarus isn't delayed by the key presses, then the steps."""
    acts = [("Say", dict(context=";".join(e["reply"]), voice_slot=True))]
    for step in e["steps"]:
        if step.startswith("wait:"):
            acts.append(("Pause", dict(duration=int(step[5:]) / 1000)))
        elif "+" in step:                                   # modifier held around a key or click
            mod, target = step.split("+")
            acts.append(("KeyDown", dict(duration=0.05, keycode=CODES[mod])))
            acts.append(("Pause", dict(duration=MODIFIER_HOLD)))
            if target == "LeftClick":
                acts.append(("MouseAction", dict(context="LC")))
            else:
                acts.append(("PressKey", dict(duration=0.05, keycode=CODES[target])))
            acts.append(("Pause", dict(duration=MODIFIER_HOLD)))
            acts.append(("KeyUp", dict(duration=0.05, keycode=CODES[mod])))
        else:
            acts.append(("PressKey", dict(duration=0.05, keycode=CODES[step])))
    return "".join(action(kind, i, **kw) for i, (kind, kw) in enumerate(acts))


def command(e):
    return f"""    <Command>
      <Id>{gid()}</Id>
      <BaseId>{gid()}</BaseId>
      <CommandString>{escape(dsp.spoken_phrase(e))}</CommandString>
      <Description>{escape(e['name'] + ': ' + dsp.keys_text(e))}</Description>
      <ActionSequence>
{actions_for(e)}      </ActionSequence>
      <Async>true</Async>
      <Enabled>true</Enabled>
      <Category>Dyson Sphere Program</Category>
      <UseShortcut>false</UseShortcut>
      <UseSpokenPhrase>true</UseSpokenPhrase>
      <UseJoystick>false</UseJoystick>
      <UseMouse>false</UseMouse>
    </Command>
"""


def build(entries):
    cmds = dsp.commands(entries)
    body = "".join(command(e) for e in cmds)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for filename, voice, suffix in VARIANTS:
        xml = f"""<?xml version="1.0" encoding="utf-8"?>
<Profile xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <HasMB>false</HasMB>
  <Id>{gid()}</Id>
  <Name>{escape(PROFILE_NAME + suffix)}</Name>
  <Commands>
{body}  </Commands>
</Profile>
"""
        xml = xml.replace("<Context2>{VOICE}</Context2>", f"<Context2>{escape(voice)}</Context2>" if voice else "")
        (OUT_DIR / filename).write_text(xml, encoding="utf-8")
        print(f"wrote voiceattack/profiles/{filename} ({len(cmds)} commands)")


if __name__ == "__main__":
    build(dsp.load())
