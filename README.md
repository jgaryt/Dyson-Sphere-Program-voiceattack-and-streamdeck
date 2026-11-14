# DysonSphereProgram-VoiceAttack-Profile
A Voice Attack 2 Profile for Dyson Sphere Program

## Layout

| Path | What it is |
|---|---|
| `profiles/DSP Build Hotkeys-Profile.vap` | Importable VoiceAttack profile (generated, do not hand-edit) |
| `scripts/build_profile.py` | Generator for the profile: commands, keys, replies, voice |
| `docs/hotkey-map.csv` | Full build-bar map: keys, spoken commands, replies, status |

## How commands work

DSP's number keys **toggle** a build bar, so pressing `1` when Power is already open closes it.
Each build command presses a *different* bar first, then the target bar, then the F-key:

```
say reply → 9 → (0.1 s) → 1 → (0.1 s) → F4      # "wind turbine"
```

Bar 9 items use `8` as the switch key instead. Single-key actions (Upgrade `U`, Dismantle `X`,
Cancel `Esc`, Land `Left Alt`) and Fly (`Space` twice) don't need this.

Replies use VoiceAttack text-to-speech with the `[Azure] Blue (en-US)` voice. Each reply lists
2–3 phrases separated by `;`; VoiceAttack picks one at random. The speech action runs first so
the reply isn't delayed by the key presses.

## Making changes

1. Edit the `rows` list (commands and keys) or the `REPLY` dict (replies) in `scripts/build_profile.py`.
2. Run `python scripts/build_profile.py` to regenerate the profile.
3. In VoiceAttack, delete the old profile, then import the new `.vap`.
4. Update `docs/hotkey-map.csv` to match.

## Open items

- Identify the Guess slots (see `docs/hotkey-map.csv`) and add them as commands.
- Add commands as locked slots unlock.

## License

GPL-3.0, see `LICENSE`.
