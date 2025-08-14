import os
from enum import Enum
from src.utils import load_vdf, save_vdf


class FileType(Enum):
    UNITS = "DOTAUnits"
    ITEMS = "DOTAAbilities"


def process_file(config_rules, path_in, path_out, file_type: FileType):
    data = load_vdf(path_in)
    root_key = file_type.value  # "DOTAUnits" or "DOTAAbilities"

    for rule in config_rules:
        mode = rule.get("mode", "mult")  # default mode
        classes = rule.get("classes", [])

        for cls in classes:
            obj = data[root_key].get(cls)
            if not obj:
                continue

            for key, value in rule.items():
                if key in ("classes", "mode"):
                    continue

                if mode == "mult":
                    try:
                        if key in obj:
                            obj[key] = str(int(float(obj[key]) * float(value)))
                        else:
                            obj[key] = str(value)
                    except ValueError:
                        obj[key] = str(value)
                elif mode == "set":
                    obj[key] = str(value)
    # Hardcode midas values
    if file_type == FileType.ITEMS:
        midas = data[root_key]["item_hand_of_midas"]
        #xp_block = midas["AbilitySpecial"]["02"]
        #xp_block["xp_multiplier"] = str(float(xp_block["xp_multiplier"]) * 2)
        gold_block = midas["AbilitySpecial"]["03"]
        gold_block["bonus_gold"] = str(float(gold_block["bonus_gold"]) * 2)

    save_vdf(data, path_out)
