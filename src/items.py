from src.utils import load_vdf, save_vdf
import os

FILENAME = "items.txt"

def process_items(config, input_dir, output_dir):
    items_cfg = config.get("items", {})
    cooldowns = items_cfg.get("AbilityCooldownOverride", {})
    disable_secretshop = set(items_cfg.get("SecretShopDisable", []))

    path_in = os.path.join(input_dir, FILENAME)
    path_out = os.path.join(output_dir, FILENAME)
    data = load_vdf(path_in)

    for item_name, item in data["DOTAAbilities"].items():
        if item_name in cooldowns:
            item["AbilityCooldown"] = str(cooldowns[item_name])
        if item_name in disable_secretshop:
            item["SecretShop"] = "0"

    save_vdf(data, path_out)
