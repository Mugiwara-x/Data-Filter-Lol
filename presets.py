import json
from pathlib import Path
from typing import List, Dict, Any

from filters import (
    filter_by_field,
    filter_by_list_length,
    filter_by_champion_played,
    filter_by_champion_banned,
    filter_by_tag,
)

BASE_DIR = Path(__file__).parent
PRESETS_DIR = BASE_DIR / "presets"
PRESETS_DIR.mkdir(exist_ok=True)
PRESETS_PATH = PRESETS_DIR / "presets.json"

LABEL_TO_OP = {
    "eq": "==",
    "ne": "!=",
    "lt": "<",
    "le": "<=",
    "gt": ">",
    "ge": ">=",
}

def _parse_value(raw: str) -> Any:
    s = raw.strip()
    lower = s.lower()
    if lower in ("true", "vrai", "yes", "oui"):
        return True
    if lower in ("false", "faux", "no", "non"):
        return False
    if s.isdigit() or (s.startswith("-") and s[1:].isdigit()):
        return int(s)
    return s

def load_presets() -> Dict[str, List[str]]:
    if not PRESETS_PATH.exists():
        return {}
    try:
        with open(PRESETS_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        return {}
    if not isinstance(data, dict):
        return {}
    cleaned: Dict[str, List[str]] = {}
    for name, lst in data.items():
        if isinstance(name, str) and isinstance(lst, list):
            cleaned[name] = [str(x) for x in lst]
    return cleaned

def save_presets(presets: Dict[str, List[str]]) -> None:
    with open(PRESETS_PATH, "w", encoding="utf-8") as f:
        json.dump(presets, f, ensure_ascii=False, indent=4)
    print(f"Presets sauvegardés dans {PRESETS_PATH}")

def apply_filter_descriptor(data: List[Dict[str, Any]], desc: str) -> List[Dict[str, Any]]:
    parts = desc.split("_")
    if not parts:
        return data

    if parts[0] == "champ" and len(parts) >= 3:
        if parts[1] == "played":
            name = "_".join(parts[2:])
            return filter_by_champion_played(data, name)
        if parts[1] == "banned":
            name = "_".join(parts[2:])
            return filter_by_champion_banned(data, name)
        return data

    if parts[0] == "tag" and len(parts) >= 4:
        tag = parts[1]
        try:
            min_count = int(parts[-1])
        except ValueError:
            min_count = 1
        return filter_by_tag(data, tag, min_count)

    if "len" in parts:
        try:
            len_index = parts.index("len")
        except ValueError:
            return data
        field = "_".join(parts[:len_index])
        if len_index + 2 >= len(parts):
            return data
        label = parts[len_index + 1]
        op = LABEL_TO_OP.get(label)
        if op is None:
            return data
        value_str = "_".join(parts[len_index + 2:])
        try:
            length = int(value_str)
        except ValueError:
            return data
        return filter_by_list_length(data, field, op, length)

    label_index = -1
    label_found = None
    for i, p in enumerate(parts):
        if p in LABEL_TO_OP:
            label_index = i
            label_found = p
            break
    if label_index == -1 or label_found is None:
        return data

    field = "_".join(parts[:label_index])
    op = LABEL_TO_OP[label_found]
    if label_index + 1 >= len(parts):
        return data
    value_str = "_".join(parts[label_index + 1:])
    value = _parse_value(value_str)

    return filter_by_field(data, field, op, value)

def apply_preset(
    all_games: List[Dict[str, Any]],
    descriptors: List[str]
) -> tuple[List[Dict[str, Any]], List[str]]:
    current = list(all_games)
    history: List[str] = []
    for desc in descriptors:
        current = apply_filter_descriptor(current, desc)
        history.append(desc)
    return current, history