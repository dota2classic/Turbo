from utils import load_vdf, save_vdf
import os

FILENAME = "items.txt"

def process_items(config, input_dir, output_dir):
    overrides = config.get("items", {}).get("AbilityCooldownOverride", {})

    path_in = os.path.join(input_dir, FILENAME)
    path_out = os.path.join(output_dir, FILENAME)
    data = load_vdf(path_in)

    for item_name, cooldown in overrides.items():
        item = data["DOTAAbilities"].get(item_name)
        if item:
            item["AbilityCooldown"] = str(cooldown)

    save_vdf(data, path_out)
