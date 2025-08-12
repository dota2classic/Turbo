from utils import load_vdf, save_vdf
import os

FILENAME = "npc_units.txt"

def process_units(config, input_dir, output_dir):
    rules = config.get("units", [])

    path_in = os.path.join(input_dir, FILENAME)
    path_out = os.path.join(output_dir, FILENAME)
    data = load_vdf(path_in)

    for rule in rules:
        classes = rule.get("classes", [])
        mode = rule.get("mode", "mult")  # default for units
        for cls in classes:
            unit = data["DOTAUnits"].get(cls)
            if not unit:
                continue
            for key, value in rule.items():
                if key in ("classes", "mode"):
                    continue
                if mode == "mult":
                    try:
                        if key in unit:
                            unit[key] = str(int(float(unit[key]) * float(value)))
                        else:
                            unit[key] = str(value)
                    except ValueError:
                        unit[key] = str(value)
                elif mode == "set":
                    unit[key] = str(value)

    save_vdf(data, path_out)
