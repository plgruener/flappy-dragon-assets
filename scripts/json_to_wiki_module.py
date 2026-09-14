import os
import sys
import json
import re
from slpp import slpp

CONTROLS = {
    "Tap": "[[:Category:Tap Dragons|Tap]]",
    "RTap": "[[:Category:Tap (Inverse) Dragons|Tap (Inverse)]]",
    "Hold": "[[:Category:Hold & Release Dragons|Hold & Release]]",
    "RHold": "[[:Category:Hold & Release (Inverse) Dragons|Hold & Release (Inverse)]]",
    "Follow": "[[:Category:Follow Finger Dragons|Follow Finger]]",
}

SEASON_EGGS = {
    "Pyrotechnic": "[[:Category:New Year Dragons|New Year]]",
    "Love": "[[:Category:Valentine Dragons|Valentine]]",
    "Floral": "[[:Category:Floral Bloom Dragons|Floral Bloom]]",
    "Royal": "[[:Category:Royal Ascension Dragons|Royal Ascension]]",
    "Retro": "[[:Category:Neon Nostalgia Dragons|Neon Nostalgia]]",
    "Beach": "[[:Category:Wet Sun Dragons|Wet Sun]]",
    "Scorched": "[[:Category:Dry Sun Dragons|Dry Sun]]",
    "Meteoric": "[[:Category:Starfall Dragons|Starfall]]",
    "Harvest": "[[:Category:Harvest Festival Dragons|Harvest Festival]]",
    "Tetric": "[[:Category:Halloween Dragons|Halloween]]",
    "Anniversary": "[[:Category:Anniversary Dragons|Anniversary]]",
    "Boreal": "[[:Category:Christmas Dragons|Christmas]]",
}

POWERUP_EGGS = {
    "Heart": "[[:Category:Dragon Heart Dragons|Dragon Heart]]",
    "Suspicious": "[[:Category:Suspicious Mushroom Dragons|Suspicious Mushroom]]",
    "Glitter": "[[:Category:Fairy Dust Dragons|Fairy Dust]]",
    "Optical": "[[:Category:Dragon Eye Dragons|Dragon Eye]]",
    "Spicy": "[[:Category:Dragon Chilli Dragons|Dragon Chilli]]",
    "Stormy": "[[:Category:Thundercloud Dragons|Thundercloud]]",
    "Time": "[[:Category:Sands of Time Dragons|Sands of Time]]",
    "Stellar": "[[:Category:Cosmic Stars Dragons|Cosmic Stars]]",
    "Rainbow": "[[:Category:Lucky Charm Dragons|Lucky Charm]]",
    "Psychic": "[[:Category:Curved Spoon Dragons|Curved Spoon]]",
    "Frost": "[[:Category:Magic Snowflake Dragons|Magic Snowflake]]",
    "Spectral": "[[:Category:Spooky Ghost Dragons|Spooky Ghost]]",
}

SUBTYPE_EGG_EXCEPTIONS = {
    "Synth": "Synthwave",
    "Chrysalis": "Insect",
    "Mirage": "Djinn",
}


def titlecase(s):
    exceptions = ["a", "an", "of", "the", "is", "or", "and", "from", "FD3000"]
    word_list = re.split(" ", s)
    final = [word_list[0].capitalize()]
    for word in word_list[1:]:
        final.append(word if word in exceptions else word.capitalize())
    return " ".join(final)


def generate_lua(json_data):
    out_data = {}
    for dragon in json_data:
        name = dragon["name"]
        for key in ("speed", "force", "weight"):
            dragon[key] = f"{dragon[key]:.2f}"
        dragon["control"] = CONTROLS[dragon["control"]]
        dragon["skill"] = titlecase(dragon["skill"]["name"]["en"])
        dragon["type"] = f"[[:Category:{dragon['type']} Dragons|{dragon['type']}]]"
        dragon["rarity"] = f"[[:Category:{dragon['rarity']} Dragons|{dragon['rarity']}]]"
        dragon["season"] = ", ".join([SEASON_EGGS[egg] for egg in dragon["breeding_eggs"] if egg in SEASON_EGGS]) or ""
        dragon["skilltypes"] = (
            ", ".join([POWERUP_EGGS[egg] for egg in dragon["breeding_eggs"] if egg in POWERUP_EGGS]) or ""
        )
        dragon["subtypes"] = []
        for egg in dragon["breeding_eggs"]:
            if egg not in {**SEASON_EGGS, **POWERUP_EGGS}:
                subtype = SUBTYPE_EGG_EXCEPTIONS.get(egg, egg)
                dragon["subtypes"].append(f"[[:Category:{subtype} Dragons|{subtype}]]")
        dragon["subtypes"] = ", ".join(dragon["subtypes"]) or ""

        out_data[name] = {}
        for key in (
            "name",
            "type",
            "subtypes",
            "rarity",
            "control",
            "skill",
            "skilltypes",
            "season",
            "speed",
            "force",
            "weight",
        ):
            out_data[name][key] = dragon[key]

    lua = f"return {slpp.encode(out_data)}\n"
    lua = lua.replace("\t{", "{")
    lua = lua.replace("\t{", "{")
    lua = lua.replace("\t", "    ")
    return lua


if __name__ == "__main__":
    OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")
    INPUT_DIR = OUTPUT_DIR if len(sys.argv) < 2 else sys.argv[1]
    with open(os.path.join(INPUT_DIR, "dragons.json"), encoding="utf-8", newline="\n") as f:
        json_data = json.load(f)
    with open(os.path.join(OUTPUT_DIR, "wiki_module.lua"), "w", encoding="utf-8", newline="\n") as out_file:
        out_file.write(generate_lua(json_data))
