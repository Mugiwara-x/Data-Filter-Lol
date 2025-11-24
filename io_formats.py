import csv
import json
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import List, Dict, Any

BASE_DIR = Path(__file__).parent
SAVE_DIR = BASE_DIR / "sauvegarde"
SAVE_DIR.mkdir(exist_ok=True)


def save_csv(data: List[Dict[str, Any]], filename: str) -> None:
    if not data:
        print("Aucune donnée à sauvegarder.")
        return
    path = SAVE_DIR / filename
    fieldnames = list(data[0].keys())
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    print(f"CSV sauvegardé dans {path}")


def save_json(data: List[Dict[str, Any]], filename: str) -> None:
    path = SAVE_DIR / filename
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"JSON sauvegardé dans {path}")


def load_json(filename: str) -> List[Dict[str, Any]]:
    path = BASE_DIR / filename
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save_xml(data: List[Dict[str, Any]], filename: str) -> None:
    if not data:
        print("Aucune donnée à sauvegarder.")
        return

    root = ET.Element("games")
    for game in data:
        game_el = ET.SubElement(root, "game")
        for key, value in game.items():
            child = ET.SubElement(game_el, key)
            if isinstance(value, list):
                for item in value:
                    item_el = ET.SubElement(child, "item")
                    item_el.text = str(item)
            else:
                child.text = str(value)

    tree = ET.ElementTree(root)
    path = SAVE_DIR / filename
    tree.write(path, encoding="utf-8", xml_declaration=True)
    print(f"XML sauvegardé dans {path}")


def _format_yaml_scalar(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if value is None:
        return "null"
    if isinstance(value, (int, float)):
        return str(value)
    s = str(value)
    if (
        any(c in s for c in [":", "-", "{", "}", "[", "]", "#", ","])
        or s.strip() != s
        or " " in s
    ):
        s = '"' + s.replace('"', '\\"') + '"'
    return s


def _write_yaml_field(f, key: str, value: Any, indent: int) -> None:
    indent_str = " " * indent
    if isinstance(value, list):
        if not value:
            f.write(f"{indent_str}{key}: []\n")
        else:
            f.write(f"{indent_str}{key}:\n")
            for item in value:
                if isinstance(item, list):
                    f.write(f"{indent_str}  -\n")
                    for sub in item:
                        f.write(f"{indent_str}    - {_format_yaml_scalar(sub)}\n")
                else:
                    f.write(f"{indent_str}  - {_format_yaml_scalar(item)}\n")
    else:
        f.write(f"{indent_str}{key}: {_format_yaml_scalar(value)}\n")


def save_yaml(data: List[Dict[str, Any]], filename: str) -> None:
    if not data:
        print("Aucune donnée à sauvegarder.")
        return

    path = SAVE_DIR / filename
    with open(path, "w", encoding="utf-8") as f:
        f.write("games:\n")
        for game in data:
            f.write("  -\n")
            for key, value in game.items():
                _write_yaml_field(f, key, value, indent=4)

    print(f"YAML sauvegardé dans {path}")