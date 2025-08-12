from utils import load_vdf, save_vdf
import os

FILENAME = "items.txt"

def process_items(config, input_dir, output_dir):
    rules = config.get("items", [])

    path_in = os.path.join(input_dir, FILENAME)
    path_out = os.path.join(output_dir, FILENAME)
    data = load_vdf(path_in)

    for rule in rules:
        classes = rule.get("classes", [])
        mode = rule.get("mode", "set")  # default for items
        for cls in classes:
            item = data["DOTAAbilities"].get(cls)
            if not item:
                continue
            for key, value in rule.items():
                if key in ("classes", "mode"):
                    continue
                if mode == "mult":
                    try:
                        if key in item:
                            item[key] = str(int(float(item[key]) * float(value)))
                        else:
                            item[key] = str(value)
                    except ValueError:
                        item[key] = str(value)
                elif mode == "set":
                    item[key] = str(value)

    save_vdf(data, path_out)
