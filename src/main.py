from utils import load_config
from units import process_units
from items import process_items
import os

CONFIG_FILE = "..\\config.json"
INPUT_DIR = "..\\input"
OUTPUT_DIR = "..\\output"

def main():
    config = load_config(CONFIG_FILE)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    process_units(config, INPUT_DIR, OUTPUT_DIR)
    process_items(config, INPUT_DIR, OUTPUT_DIR)

if __name__ == "__main__":
    main()