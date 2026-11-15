# Changing Icarus's voice

Every command starts with a VoiceAttack **Say Something with Text-To-Speech** action. The repo
builds two profiles that differ only in which voice those actions use:

| Profile | Voice |
|---|---|
| `DSP Build Hotkeys-Profile.vap` | An Azure voice, currently `[Azure] Blue (en-US)` |
| `DSP Build Hotkeys-LocalVoice-Profile.vap` | No voice set, so it uses the Windows default voice |

## Changing the Azure voice (recommended way)

Change the voice in the generator. Voice changes made inside VoiceAttack are saved with the
profile, but they're replaced the next time you import a newly generated profile.

1. **Find the exact voice name VoiceAttack uses.**
   1. In VoiceAttack, edit any command and double-click its **Say** action. You can also add a
      temporary one under **Other → Sounds → Say Something with Text-To-Speech**.
   2. Open the **Voice** dropdown. Azure voices are listed with an `[Azure]` prefix, for example
      `[Azure] Blue (en-US)`.
   3. Note the name exactly as shown, including the brackets, spaces and the region in parentheses.
      Then cancel without saving.

   Azure voices only show up once Azure text-to-speech is set up in VoiceAttack. If the dropdown
   has no `[Azure]` entries, see [One-time Azure setup](#one-time-azure-setup) below.

2. **Edit the generator.** In `scripts/build_profile.py`, find the `VARIANTS` list near the bottom:

   ```python
   VARIANTS = [
       ("profiles/DSP Build Hotkeys-Profile.vap", "[Azure] Blue (en-US)", ""),
       ("profiles/DSP Build Hotkeys-LocalVoice-Profile.vap", "", " (local voice)"),
   ]
   ```

   Replace `[Azure] Blue (en-US)` with the new name from step 1.

3. **Regenerate the profiles.** Run `python scripts/build_profile.py`.

4. **Re-import.** In VoiceAttack, delete the old **Dyson Sphere Program - Build Hotkeys** profile,
   then import `profiles/DSP Build Hotkeys-Profile.vap`.

5. **Commit** the changed script and profiles.

### If the name doesn't match

If the name in the generator doesn't exactly match a voice VoiceAttack knows, the replies may play
in the default voice or not at all. Check for typos and the `[Azure]` prefix.

To be sure of the exact format, set the voice on one Say action by hand, export the profile, and
compare it with the generated file.

## The Text-to-Speech options tab

Most voice settings live in VoiceAttack's **Options** (the wrench icon), on the **Text-to-Speech**
tab. Screens below are from VoiceAttack v2.2.0.3.

| Setting | What it does |
|---|---|
| **Override Default Text-to-Speech Device** | Send Icarus to a specific output, e.g. your headset. The default is the Windows playback device. |
| **TTS Volume Offset** | Volume for all speech. |
| **Single TTS Instance** | Only one reply plays at a time. Useful if replies pile up when you give commands quickly. |
| **Click here for the TTS Sound Effects Manager** | Add effects to the voice, such as pitch shift or reverb/delay, for a more robotic Icarus. |
| **Click here for Azure TTS Settings** | Azure key, region and the Enable Azure TTS switch (see below). |

Sending Icarus to a headset also stops the microphone from hearing him. Together with the
generator's reply check, that's a second guard against feedback loops.

## One-time Azure setup

Azure voices need an Azure Speech key in VoiceAttack. Based on the VoiceAttack forum post
"Setting up Azure Services": https://forum.voiceattack.com/smf/index.php?topic=5207.0

1. In the Azure portal, create a Speech resource. Open its **Keys and endpoint** page and copy a
   **key** and the **region**.
2. In VoiceAttack, open **Options** (wrench icon) → **Text-to-Speech** tab, then click
   **Click here for Azure TTS Settings**.
3. Click **Click here to open Azure speech key settings**, enter the Speech Key and Region, and
   click OK.
4. Back on the Azure TTS Settings screen, tick **Enable Azure TTS**, set any other options, and
   click OK.
5. Azure voices now appear in the Voice dropdown of the **Say Something with Text-To-Speech**
   action.

Azure text-to-speech is a paid service with a free monthly allowance. Short replies use very
little of it. Keep the key private, and don't commit it to this repo.

## Changing the voice inside VoiceAttack

This works for Azure and Windows voices alike:

1. With the profile loaded, click the **edit** (pencil) icon next to the profile name.
2. Select a command and click **Edit** (top right of the Edit a Profile screen).
3. In the action list, highlight the line that begins with **Say**.
4. Click **Edit**.
5. In **Say Something with Text-To-Speech**:
   - **Voice** chooses the voice, e.g. `[Azure] Grant MAI-Voice-2.1-Flash (en-US)`.
   - **Effect Set** applies a sound effect set (pitch, reverb/delay and so on). The **…** button
     next to it edits effect sets and creates new ones.
   - **Preview** plays it.
6. Click OK on each screen.

On its own this changes one command. To change **every** command at once, use **Mass update**:

1. Do steps 1–5 on any one command, choosing the new voice and effect set.
2. Tick **Mass update** (bottom left of the Say dialog) and click OK.
3. VoiceAttack shows a **Mass Update Selected** warning listing what will change across the whole
   profile. Every Say action using the old voice gets the new voice. Any that have no effect set
   get the new effect set, and a blank locale becomes `Default`. Click **Yes**.
4. Click OK on the command screen and on the profile screen to save. Clicking **Cancel** on the
   command screen undoes the mass update.

Mass update matches on the **old voice**. Replies that use a different voice are left alone.

Changes made here are saved with the profile in VoiceAttack and stay put. They are only replaced
when you delete the profile and import a newly generated one, which happens whenever commands are
added or changed in this repo. To keep a voice choice across those updates, also set it in the
generator (above).

## Changing the local (Windows) voice

The local-voice profile uses whatever Windows' default text-to-speech voice is, so no repo change
is needed:

1. Press **Win + R** and run `C:\Windows\SysWOW64\Speech\SpeechUX\sapi.cpl`. Use the 32-bit panel,
   because that's the one VoiceAttack reads.
2. On the **Text to Speech** tab, pick a voice, such as **Microsoft David**.
3. Restart VoiceAttack.

### More local voices: Microsoft Speech Platform 11

VoiceAttack can also use voices from Microsoft Speech Platform 11, which are free and local. See
https://voiceattack.com/alternate.aspx.

1. Install the Microsoft Speech Platform runtime, from Microsoft or VoiceAttack.com.
2. Install the TTS voices you want from the same place. You only need the voices for text-to-speech,
   not a speech recognition engine.
3. Start VoiceAttack. It finds them automatically.
4. Set one as the Windows default voice (see above) for the local-voice profile to pick it up.
   No repo change is needed.

They play instantly but sound older and more robotic than Azure voices, which can suit Icarus.

**Leave speech recognition on Windows.** The same page offers Speech Platform recognition engines,
but those don't learn your voice, need a confidence setting above 75, and don't log unrecognized
commands. Recognition is set under **Options → System/Advanced** and affects every profile,
including Elite Dangerous.

## Things to keep in mind

- **Azure is cloud-based.** Each reply needs a quick trip to Azure, so expect a small delay. If it
  matters, use the local-voice profile.
- **Replies must never match a command.** VoiceAttack can hear Icarus through the speakers, and a
  reply that matches a command will set it off again in a loop. Changing the voice doesn't affect
  this. The generator refuses to build a profile if any reply matches a command.
