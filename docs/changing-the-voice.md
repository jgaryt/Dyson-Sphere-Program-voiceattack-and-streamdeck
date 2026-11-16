# Changing Icarus's voice

Every command starts with a **Say Something with Text-To-Speech** action, the reply Icarus
speaks. This guide covers changing the voice and its sound effects, setting up Azure voices, and
the related VoiceAttack settings. Written against VoiceAttack v2.2.0.3.

**Which section do I need?**

- *I want a different voice or effect, now:* [Change it in VoiceAttack](#change-it-in-voiceattack)
- *I want new profile versions to use that voice too:* [Make it the default](#make-it-the-default-for-new-versions)
- *There are no `[Azure]` voices in the list:* [One-time Azure setup](#one-time-azure-setup)
- *I'm using the local-voice profile:* [Windows voices](#windows-voices-local-voice-profile)

## Change it in VoiceAttack

This works for Azure and Windows voices alike.

**One command:**

1. With the profile loaded, click the **edit** (pencil) icon next to the profile name.
2. Select a command and click **Edit** (top right).
3. Highlight the action line that begins with **Say** and click **Edit**.
4. Choose a **Voice**, and an **Effect Set** if you want one, e.g. pitch shift or reverb. The
   **…** button next to Effect Set edits effect sets or creates new ones. Click **Preview** to
   hear it.
5. Click **OK** on each screen to save.

**Every command at once (Mass update):**

1. Do steps 1–4 on any one command.
2. Before clicking OK in the Say dialog, tick **Mass update** (bottom left).
3. A **Mass Update Selected** warning lists the changes. Every reply using the *old* voice gets
   the new voice, and those with no effect set get the new one. Click **Yes**.
4. Click **OK** on the command screen and the profile screen to save. Clicking **Cancel** on the
   command screen undoes it.

Your changes are saved with the profile. Importing a new version of the profile replaces them,
so redo the Mass update after each import. That takes about a minute.

## Make it the default for new versions

To make new profile versions start with your voice, set it in the build script. **The effect set
can't be set this way yet.** Re-apply it with Mass update after importing.

1. **Get the exact voice name.** In any Say action, open the **Voice** dropdown and copy the name
   exactly, including brackets, spaces and the region, e.g.
   `[Azure] Grant MAI-Voice-2.1-Flash (en-US)`. Then cancel.
2. **Edit `scripts/build_voiceattack.py`.** Near the top, put the name in the `VARIANTS` list:

   ```python
   VARIANTS = [
       ("DSP Build Hotkeys-Profile.vap", "[Azure] Grant MAI-Voice-2.1-Flash (en-US)", ""),
       ("DSP Build Hotkeys-LocalVoice-Profile.vap", "", " (local voice)"),
   ]
   ```

   The first line is the Azure profile. The local-voice profile is left blank on purpose, so it
   uses the Windows default voice.
3. **Rebuild:** run `python scripts/build_all.py`.
4. **Re-import:** delete the old profile in VoiceAttack, then import the new `.vap` from
   `voiceattack/profiles`.
5. **Commit** the changes to the repo.

If replies come out in the wrong voice or stay silent, the name probably doesn't exactly match.
Check spelling and the `[Azure]` prefix.

## One-time Azure setup

Azure voices only appear in the Voice dropdown once VoiceAttack has an Azure Speech key. Steps
from the VoiceAttack forum post "Setting up Azure Services":
https://forum.voiceattack.com/smf/index.php?topic=5207.0

1. In the Azure portal, create a **Speech** resource. On its **Keys and endpoint** page, copy a
   **key** and the **region**.
2. In VoiceAttack, open **Options** (wrench icon) → **Text-to-Speech** tab, then click
   **Click here for Azure TTS Settings**.
3. Click **Click here to open Azure speech key settings**, enter the key and region, and click OK.
4. Tick **Enable Azure TTS** and click OK.

Things to know about Azure:
- **It costs money past a free monthly allowance.** Icarus's short replies use very little.
- **Keep the key private.** Never commit it to this repo.
- **Each reply makes a quick trip to the internet,** so expect a small delay. The local-voice
  profile has none.

## Text-to-Speech settings

**Options** (wrench icon) → **Text-to-Speech** tab:

| Setting | What it does |
|---|---|
| **Override Default Text-to-Speech Device** | Plays Icarus on a chosen output, e.g. your headset. |
| **TTS Volume Offset** | Volume of all speech. |
| **Single TTS Instance** | Plays one reply at a time. Recommended. |
| **Click here for the TTS Sound Effects Manager** | Create and edit effect sets (pitch shift, reverb/delay and so on). |
| **Click here for Azure TTS Settings** | Azure key, region and on/off switch (see above). |

Playing Icarus through a headset also stops the microphone from hearing him.

## Windows voices (local-voice profile)

The local-voice profile uses the Windows default text-to-speech voice. To change it:

1. Press **Win + R** and run `C:\Windows\SysWOW64\Speech\SpeechUX\sapi.cpl`. Use this 32-bit
   panel, because it's the one VoiceAttack reads.
2. On the **Text to Speech** tab, pick a voice, e.g. **Microsoft David**.
3. Restart VoiceAttack.

You can also use Mass update to pick a voice and effect set instead (see above).

**Want more Windows voices?** Microsoft Speech Platform 11 adds free voices that play instantly
and sound older and more robotic, which can suit Icarus. See https://voiceattack.com/alternate.aspx.

1. Install the Speech Platform runtime and the voices you want.
2. Restart VoiceAttack.

You don't need its speech recognition engines. Leave recognition on Windows (**Options →
System/Advanced**), since that setting affects every profile, including Elite Dangerous.

## Whatever voice you choose

Icarus's replies must never match a voice command, or VoiceAttack hears him and repeats the
command in a loop. Changing the voice doesn't affect this. If you edit replies in the build
script, it checks for you.
