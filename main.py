import json
import os
import vdf

CONFIG_FILE = "config.json"
INPUT_DIR = "input"
OUTPUT_DIR = "output"
FILENAME = "npc_units.txt"


def load_config():
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def load_units(path):
    with open(path, "r", encoding="utf-8") as f:
        return vdf.load(f)


def save_units(units, path):
    with open(path, "w", encoding="utf-8") as f:
        vdf.dump(units, f, pretty=True)


def apply_modifiers(units, config):
    xp_mult = config["XPModifier"]
    gold_mult = config["GoldModifier"]
    hp_mult = config["HPModifier"]
    armor_mult = config["ArmorModifier"]

    gold_xp_units = set(config["UnitsAffectedByGoldXPModifiers"])
    stats_units = set(config["UnitsAffectedByStatsModifiers"])

    for unit_name, unit_data in units["DOTAUnits"].items():
        if unit_name in gold_xp_units:
            if "BountyXP" in unit_data:
                unit_data["BountyXP"] = str(int(int(unit_data["BountyXP"]) * xp_mult))
            if "BountyGoldMin" in unit_data:
                unit_data["BountyGoldMin"] = str(int(int(unit_data["BountyGoldMin"]) * gold_mult))
            if "BountyGoldMax" in unit_data:
                unit_data["BountyGoldMax"] = str(int(int(unit_data["BountyGoldMax"]) * gold_mult))

        if unit_name in stats_units:
            if "StatusHealth" in unit_data:
                unit_data["StatusHealth"] = str(int(int(unit_data["StatusHealth"]) * hp_mult))
            if "ArmorPhysical" in unit_data:
                unit_data["ArmorPhysical"] = str(int(float(unit_data["ArmorPhysical"]) * armor_mult))

    return units


def override_couriers(units, config):
    override = config["CourierOverride"]
    target_units = ["npc_dota_courier", "npc_dota_flying_courier"]

    for name in target_units:
        unit = units["DOTAUnits"].get(name)
        if not unit:
            continue

        unit["MovementSpeed"] = str(override["MovementSpeed"])
        unit["StatusHealth"] = str(override["StatusHealth"])
        unit["StatusHealthRegen"] = str(override["StatusHealthRegen"])
        unit["ArmorPhysical"] = str(override["ArmorPhysical"])
        unit["MagicalResistance"] = str(override["MagicalResistance"])

    return units


def main():
    config = load_config()
    input_path = os.path.join(INPUT_DIR, FILENAME)
    output_path = os.path.join(OUTPUT_DIR, FILENAME)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    units = load_units(input_path)
    units = apply_modifiers(units, config)
    units = override_couriers(units, config)
    save_units(units, output_path)


if __name__ == "__main__":
    main()
