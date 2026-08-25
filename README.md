# MiniAurasVoicePackChinese

Mandarin voice packs for [MiniAuras](https://www.curseforge.com/wow/addons/miniauras).

MiniAuras can call out important and defensive cooldowns as they land. This addon adds three
Mandarin voices to that list, speaking the Chinese spell names rather than the English ones.
They shipped inside MiniAuras itself until they moved out here, so that players who do not need
them stop downloading them.

- **Amy** - female, bright and casual.
- **Anna Su** - female, friendly and even.
- **Jason Chen** - male, steady.

[Discord](https://discord.gg/UruPTPHHxK)

## Install

Install MiniAuras first, then this. The voices appear in **MiniAuras > Alerts > Voice pack**
on a Chinese client; they are hidden on other clients, so pick one from the addon's own list
of English voices there instead.

Your saved voice carries across the move. The name is what MiniAuras stores, so a player who
had Amy selected gets Amy back as soon as this addon is installed.

## Download

Available on [CurseForge](https://www.curseforge.com/wow/addons/miniauras-chinese-voice-pack).

## Regenerating the clips

The clips are baked audio, one file per announced spell name, rendered with ElevenLabs. The
script expects a MiniAuras checkout beside this one, because the spell lists and the clip file
names belong to it.

```
python scripts/GenerateVoicePack.py            # renders whatever is missing
python scripts/GenerateVoicePack.py --force    # re-renders everything
```

It needs `ELEVENLABS_API_KEY` and ffmpeg on the path, and refuses to run if its clip names have
drifted from the packs MiniAuras ships, since a mismatched name is a clip that silently never
plays.

`scripts/SpellNamesZhCN.json` is written by hand. Do not rebuild it by asking the client for the
name of each spell id: six of the announced ids are the aura rather than the cast, and the aura
carries another ability's name, so Guardian of the Forgotten Queen would come back as Divine
Shield. Add new spells to the file by hand, and the generator stops rather than quietly
announcing one in English.
