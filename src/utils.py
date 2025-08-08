import json
import vdf

def load_config(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def load_vdf(path):
    with open(path, "r", encoding="utf-8") as f:
        return vdf.load(f)

def save_vdf(data, path):
    with open(path, "w", encoding="utf-8") as f:
        vdf.dump(data, f, pretty=True, escaped=True)
