#!/usr/bin/env -S uv run --script

import xml.etree.ElementTree as ET
import pathlib
import os


def find_and_set(config, key_name, default_val):
    val = os.getenv(key_name.upper(), default_val)
    elem = config.find(key_name)

    if elem is None:
        print(f"Added {key_name} to the config")
        elem = ET.SubElement(config, key_name)


    if elem.text is None or elem.text != val:
        print(f"Set {key_name} in config!")
        elem.text = val
    else:
        print(f"{key_name} is already set to the expected value.")

def main():
    config_path = pathlib.Path("config.xml")

    if not config_path.exists():
        with config_path.open("w") as f:
            # pretty hacky but eh
            f.write("<Config></Config>")

    config_root = ET.parse(config_path)
    config = config_root.getroot()

    postgres_values = [
        ("PostgresUser", ""),
        ("PostgresPassword", ""),
        ("PostgresHost", ""),
        ("PostgresPort", "5432"),
    ]

    for postgres_key, default_value in postgres_values:
        find_and_set(config, postgres_key, default_value)

    config_root.write(config_path)

main()