"""Renders the Mandarin voice packs into src/Sounds/<pack>/.

The spell lists, the file naming and the rendering pipeline all belong to MiniAuras, so this
imports its generator from the sibling checkout rather than restating any of it. What lives here
is the Mandarin side: which voices, what they say, and the check that the clip names still match
the packs MiniAuras ships.

Run from the repo root with the ELEVENLABS_API_KEY environment variable set:
    python scripts/GenerateVoicePack.py [--force] [--allow-english]

Existing clips are skipped unless --force is given. A spell with no Mandarin name stops the run,
because a pack that announces one spell in English is worse than one that was never built;
--allow-english renders it in English anyway.

SpellNamesZhCN.json is written by hand, not fetched. Asking the client for the name of each id
would get six of them wrong, because those ids are the aura rather than the cast and the aura
carries another ability's name.
"""

import json
import os
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
# MiniAuras is expected beside this repo. Nothing is copied out of it: the spell lists and the
# clip names have one owner, and a stale duplicate here would ship a pack that plays nothing.
MINIAURAS = REPO.parent / "MiniAuras"

if not MINIAURAS.is_dir():
    sys.exit(f"MiniAuras checkout not found at {MINIAURAS}")

sys.path.insert(0, str(MINIAURAS / "scripts"))

import GenerateTtsAudio as base  # noqa: E402

VOICES = {
    "Amy": "bhJUNIXWQQ94l8eI2VUf",
    "Anna Su": "9lHjugDhwqoxA5MhX0az",
    "Jason Chen": "DowyQ68vDpgFYdWVGjc3",
}
# Multilingual v2's tone accuracy is not good enough for Mandarin.
MODEL_ID = "eleven_v3"

NAMES = pathlib.Path(__file__).resolve().parent / "SpellNamesZhCN.json"
OUT_DIR = REPO / "src" / "Sounds"
# The pack every generated clip name is checked against.
REFERENCE_PACK = MINIAURAS / "src" / "Sounds" / "TTS" / "David"

PREVIEWS = {
    "PreviewImportant": "重要",
    "PreviewDefensive": "防御",
    "PreviewEnemyDebuff": "敌方减益",
}
# Spoken when the pack is picked in the dropdown. The longest name, as a sample of the
# announcements themselves.
PREVIEW_VOICE_TEXT = "化身：乌索克的守护者"

# English spell name -> what the Mandarin voices say instead of the translated name. Empty
# because the Mandarin names are already short enough to call out.
SHORT_NAMES = {}


def build_texts(categories, names):
    """File stem -> the Mandarin text that stem's clip speaks, and the names with no Mandarin."""
    texts = {}
    untranslated = []

    for ids in categories.values():
        for name in ids.values():
            text = base.spoken_text(name)
            spoken = SHORT_NAMES.get(text) or names.get(text)

            if not spoken:
                untranslated.append(text)

            texts[base.slug(text)] = spoken or text

    texts.update(PREVIEWS)
    texts["PreviewVoice"] = PREVIEW_VOICE_TEXT

    return texts, sorted(set(untranslated))


def check_against_shipped(stems):
    """A pack whose file names drift from MiniAuras' own plays nothing for the clips that
    differ, and says so nowhere, so the mismatch is caught here instead."""
    if not REFERENCE_PACK.is_dir():
        sys.exit(f"reference pack not found at {REFERENCE_PACK}")

    shipped = {path.stem for path in REFERENCE_PACK.glob("*.ogg")}
    missing = sorted(shipped - stems)
    extra = sorted(stems - shipped)

    if missing or extra:
        sys.exit(f"clip names do not match {REFERENCE_PACK.name}: missing {missing}, extra {extra}")


def main():
    api_key = os.environ.get("ELEVENLABS_API_KEY")

    if not api_key:
        sys.exit("set ELEVENLABS_API_KEY")

    force = "--force" in sys.argv

    names = json.loads(NAMES.read_text(encoding="utf-8"))
    texts, untranslated = build_texts(base.parse_categories(), names)

    if untranslated and "--allow-english" not in sys.argv:
        listed = "\n  ".join(untranslated)
        sys.exit(
            f"no Mandarin name for:\n  {listed}\n"
            "add them to scripts/SpellNamesZhCN.json, or pass --allow-english to speak them in English"
        )

    for name in untranslated:
        print(f"WARNING: no Mandarin name for '{name}', speaking English")

    check_against_shipped(set(texts))

    rendered, reused = 0, 0

    for pack, voice_id in VOICES.items():
        pack_dir = OUT_DIR / pack
        pack_dir.mkdir(parents=True, exist_ok=True)

        for file_stem in sorted(texts):
            path = pack_dir / f"{file_stem}.ogg"

            if path.exists() and not force:
                reused += 1
                continue

            base.render(api_key, voice_id, texts[file_stem], path, 0.0, MODEL_ID)
            rendered += 1
            print(f"rendered {pack}/{path.name}")

    print(f"{rendered} clip(s) rendered, {reused} reused")


if __name__ == "__main__":
    main()
