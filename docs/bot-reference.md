# MiniAurasVoicePackChinese - bot reference

Version 1.0.0. Interface version 120100. No saved variables, no options UI,
no slash commands.

## What it does

Adds three Mandarin voices, **Amy**, **Anna Su**, and **Jason Chen**, to the
voice pack dropdown in MiniAuras' Alerts settings. They speak the Chinese
spell names for the same announcements the shipped English voices cover:
important cooldowns, defensive cooldowns, and enemy debuffs.

These three shipped inside MiniAuras itself until they moved out. The
audio is identical; only where it lives has changed, so that players on other
clients stop downloading about 6 MB they can never hear.

The addon is audio plus one registration call. It draws nothing, stores
nothing, and does not change how or when MiniAuras announces.

## How it works

- Ships one OGG per announced spell name under `Sounds\Amy\`,
  `Sounds\Anna Su\`, and `Sounds\Jason Chen\`, using the same file names as
  MiniAuras' own packs.
- Hands all three folders to MiniAuras through
  `MiniAurasApi.v1:RegisterVoicePack`, tagged for the `zhCN` and `zhTW`
  client locales.
- MiniAuras is an optional dependency, so it normally loads first. If it has
  not, the addon waits on ADDON_LOADED and registers as soon as the API
  appears.

## Settings

None of its own. The voice is picked in MiniAuras under **Alerts > Voice
pack**, and the choice is saved by MiniAuras.

## Troubleshooting

**"My voice reset to an English one after updating MiniAuras."** MiniAuras
stopped shipping these three voices, and a saved voice it cannot find falls
back to the first one it can. Installing this addon brings the name back and
the setting starts working again, because MiniAuras saves the voice by name.

**"The voices are not in the dropdown."** They are offered on Chinese
clients only. On any other client the dropdown shows MiniAuras' English
voices instead. The names stay reserved everywhere, so a saved setting still
means this pack when the player switches back to a Chinese client.

**"I have both this and a MiniAuras that still ships them."** That MiniAuras
ships the same three names itself, and a name is reserved by whoever ships
it, so registration is refused and the built-in copies are used. Nothing
breaks, and nothing is duplicated in the dropdown.

**"The dropdown is empty of Mandarin voices but the addon is enabled."**
Check MiniAuras itself is installed and enabled, and is recent enough to
have the voice pack API with locale support (5.2.0 and later).

**"A spell announces in English."** That name had no entry in
`scripts/SpellNamesZhCN.json` when the clips were rendered. Since 1.0.0 the
generator stops rather than shipping that, so it can only affect clips
rendered before then.
