import os
from src.utils import load_config
from src.process import process_file, FileType

CONFIG_PATH = "..\\config.json"
INPUT_DIR = "..\\input"
OUTPUT_DIR = "..\\output"

def main():
    config = load_config(CONFIG_PATH)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Process units
    process_file(
        config["units"],
        os.path.join(INPUT_DIR, "npc_units.txt"),
        os.path.join(OUTPUT_DIR, "npc_units.txt"),
        FileType.UNITS
    )

    # Process items
    process_file(
        config["items"],
        os.path.join(INPUT_DIR, "items.txt"),
        os.path.join(OUTPUT_DIR, "items.txt"),
        FileType.ITEMS
    )


if __name__ == "__main__":
    main()