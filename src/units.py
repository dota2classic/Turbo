from utils import load_vdf, save_vdf
import os

FILENAME = "npc_units.txt"

def process_units(config, input_dir, output_dir):
    cfg = config.get("units", {})
    xp_mult = cfg.get("XPModifier", 1)
    gold_mult = cfg.get("GoldModifier", 1)
    hp_mult = cfg.get("HPModifier", 1.0)
    armor_mult = cfg.get("ArmorModifier", 1.0)
    gold_xp_units = set(cfg.get("UnitsAffectedByGoldXPModifiers", []))
    stats_units = set(cfg.get("UnitsAffectedByStatsModifiers", []))
    courier_override = cfg.get("CourierOverride", {})

    path_in = os.path.join(input_dir, FILENAME)
    path_out = os.path.join(output_dir, FILENAME)
    data = load_vdf(path_in)

    for name, unit in data["DOTAUnits"].items():
        if name in gold_xp_units:
            unit["BountyXP"] = str(int(int(unit.get("BountyXP", "0")) * xp_mult))
            unit["BountyGoldMin"] = str(int(int(unit.get("BountyGoldMin", "0")) * gold_mult))
            unit["BountyGoldMax"] = str(int(int(unit.get("BountyGoldMax", "0")) * gold_mult))

        if name in stats_units:
            unit["StatusHealth"] = str(int(int(unit.get("StatusHealth", "0")) * hp_mult))
            unit["ArmorPhysical"] = str(int(float(unit.get("ArmorPhysical", "0")) * armor_mult))

        if name in ["npc_dota_courier", "npc_dota_flying_courier"]:
            for key, value in courier_override.items():
                unit[key] = str(value)

    save_vdf(data, path_out)
