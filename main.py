import re
import os
import json
import math

# === Constants ===
CONFIG_FILE = "config.json"
DEFAULT_DIR = "default"
MODIFIED_DIR = "modified"
FILENAME = "npc_units.txt"

XP_PATTERN = re.compile(r'("BountyXP"\s*")(\d+)(")')
GOLD_PATTERN = re.compile(r'("BountyGold(?:Min|Max)"\s*")(\d+)(")')
HP_PATTERN = re.compile(r'("StatusHealth"\s*")(\d+)(")')
ARMOR_PATTERN = re.compile(r'("ArmorPhysical"\s*")(\d+(?:\.\d+)?)(")')
MAGIC_RESIST_PATTERN = re.compile(r'("MagicalResistance"\s*")(\d+(?:\.\d+)?)(")')
MOVESPEED_PATTERN = re.compile(r'("MovementSpeed"\s*")(\d+)(")')
REGEN_PATTERN = re.compile(r'("StatusHealthRegen"\s*")(\d+(?:\.\d+)?)(")')


def load_config(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_file_lines(path: str) -> list:
    with open(path, "r", encoding="utf-8") as f:
        return f.readlines()


def save_file_lines(path: str, lines: list):
    with open(path, "w", encoding="utf-8") as f:
        f.writelines(lines)


def modify_line(line: str,
                unit_name: str,
                gold_xp_targets: set,
                stats_targets: set,
                xp_mult: float,
                gold_mult: float,
                hp_mult: float,
                armor_mult: float,
                courier_name: str,
                courier_settings: dict) -> str:

    if unit_name in gold_xp_targets:
        line = XP_PATTERN.sub(lambda m: f'{m.group(1)}{int(int(m.group(2)) * xp_mult)}{m.group(3)}', line)
        line = GOLD_PATTERN.sub(lambda m: f'{m.group(1)}{int(int(m.group(2)) * gold_mult)}{m.group(3)}', line)

    if unit_name in stats_targets:
        line = HP_PATTERN.sub(lambda m: f'{m.group(1)}{int(round(int(m.group(2)) * hp_mult))}{m.group(3)}', line)
        line = ARMOR_PATTERN.sub(lambda m: f'{m.group(1)}{int(round(float(m.group(2)) * armor_mult))}{m.group(3)}', line)

    if unit_name == courier_name:
        line = MOVESPEED_PATTERN.sub(lambda m: f'{m.group(1)}{courier_settings["MovementSpeed"]}{m.group(3)}', line)
        line = HP_PATTERN.sub(lambda m: f'{m.group(1)}{courier_settings["StatusHealth"]}{m.group(3)}', line)
        line = REGEN_PATTERN.sub(lambda m: f'{m.group(1)}{courier_settings["StatusHealthRegen"]}{m.group(3)}', line)
        line = ARMOR_PATTERN.sub(lambda m: f'{m.group(1)}{courier_settings["ArmorPhysical"]}{m.group(3)}', line)
        line = MAGIC_RESIST_PATTERN.sub(lambda m: f'{m.group(1)}{courier_settings["MagicalResistance"]}{m.group(3)}', line)

    return line


def insert_armor_block(lines: list, unit_index: int, courier_settings: dict) -> list:
    insert_lines = [
        '\t\t// Armor\n',
        '\t\t//----------------------------------------------------------------\n',
        f'\t\t"ArmorPhysical"\t\t\t\t"{courier_settings["ArmorPhysical"]}"\t\t// Physical protection.\n',
        f'\t\t"MagicalResistance"\t\t\t\t"{courier_settings["MagicalResistance"]}"\t\t\t// Magical protection.\n'
    ]

    for i in range(unit_index, len(lines)):
        if "}" in lines[i]:
            for j, insert_line in enumerate(insert_lines):
                lines.insert(i + j, insert_line)
            break
    return lines


def process_units(lines: list,
                  gold_xp_targets: set,
                  stats_targets: set,
                  xp_mult: float,
                  gold_mult: float,
                  hp_mult: float,
                  armor_mult: float,
                  courier_settings: dict) -> list:

    output_lines = []
    current_unit = None
    inside_block = False
    i = 0

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if stripped.startswith('"') and not stripped.endswith('{') and not inside_block:
            match = re.match(r'"([^"]+)"', stripped)
            if match:
                current_unit = match.group(1)

        if "{" in line:
            inside_block = True
            if current_unit == "npc_dota_courier":
                block_start = i

        if "}" in line:
            if current_unit == "npc_dota_courier":
                block_text = ''.join(lines[block_start:i + 1])
                if "ArmorPhysical" not in block_text and "MagicalResistance" not in block_text:
                    output_lines.append('\t\t// Armor\n')
                    output_lines.append(f'\t\t"ArmorPhysical"\t\t\t\t"{courier_settings["ArmorPhysical"]}"\t\t// Physical protection.\n')
                    output_lines.append(f'\t\t"MagicalResistance"\t\t\t"{courier_settings["MagicalResistance"]}"\t\t// Magical protection.\n')

            inside_block = False
            current_unit = None

        if inside_block and current_unit:
            line = modify_line(line,
                               current_unit,
                               gold_xp_targets,
                               stats_targets,
                               xp_mult,
                               gold_mult,
                               hp_mult,
                               armor_mult,
                               "npc_dota_courier",
                               courier_settings)
            line = modify_line(line,
                               current_unit,
                               gold_xp_targets,
                               stats_targets,
                               xp_mult,
                               gold_mult,
                               hp_mult,
                               armor_mult,
                               "npc_dota_flying_courier",
                               courier_settings)

        output_lines.append(line)
        i += 1

    return output_lines


def main():
    config = load_config(CONFIG_FILE)

    xp_multiplier = config.get("XPModifier", 1)
    gold_multiplier = config.get("GoldModifier", 1)
    hp_multiplier = config.get("HPModifier", 1.0)
    armor_multiplier = config.get("ArmorModifier", 1.0)
    courier_settings = config.get("CourierOverride", {})

    gold_xp_units = set(config.get("UnitsAffectedByGoldXPModifiers", []))
    stats_units = set(config.get("UnitsAffectedByStatsModifiers", []))

    input_path = os.path.join(DEFAULT_DIR, FILENAME)
    output_path = os.path.join(MODIFIED_DIR, FILENAME)
    os.makedirs(MODIFIED_DIR, exist_ok=True)

    input_lines = load_file_lines(input_path)
    modified_lines = process_units(input_lines,
                                   gold_xp_units,
                                   stats_units,
                                   xp_multiplier,
                                   gold_multiplier,
                                   hp_multiplier,
                                   armor_multiplier,
                                   courier_settings)
    save_file_lines(output_path, modified_lines)


if __name__ == "__main__":
    main()
