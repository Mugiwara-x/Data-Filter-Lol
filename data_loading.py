import csv
import json
from pathlib import Path
from typing import List, Dict, Any

BASE_DIR = Path(__file__).parent
DATASET_DIR = BASE_DIR / "dataset"


def _to_int(row: Dict[str, str], key: str, default: int = 0) -> int:
    val = row.get(key, "")
    if val is None or val == "":
        return default
    try:
        return int(val)
    except ValueError:
        return default


def load_champion_name_mapping() -> Dict[int, str]:
    mapping: Dict[int, str] = {}

    path1 = DATASET_DIR / "champion_info.json"
    try:
        with open(path1, encoding="utf-8") as f:
            data = json.load(f)
        for _, info in data["data"].items():
            champ_id = int(info["id"])
            name = info["name"]
            mapping[champ_id] = name
    except FileNotFoundError:
        pass

    path2 = DATASET_DIR / "champion_info_2.json"
    try:
        with open(path2, encoding="utf-8") as f:
            data = json.load(f)
        for _, info in data["data"].items():
            champ_id = int(info["id"])
            name = info["name"]
            mapping[champ_id] = name
    except FileNotFoundError:
        pass

    return mapping


def load_champion_tags_mapping() -> Dict[int, List[str]]:
    tags_by_id: Dict[int, List[str]] = {}
    path = DATASET_DIR / "champion_info_2.json"
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        for _, info in data["data"].items():
            champ_id = int(info["id"])
            tags = info.get("tags", [])
            tags_by_id[champ_id] = tags
    except FileNotFoundError:
        pass
    return tags_by_id


def load_summoner_spell_mapping() -> Dict[int, str]:
    mapping: Dict[int, str] = {}
    path = DATASET_DIR / "summoner_spell_info.json"
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        for _, info in data["data"].items():
            spell_id = int(info["id"])
            name = info["name"]
            mapping[spell_id] = name
    except FileNotFoundError:
        pass
    return mapping


def load_games_csv(filename: str = "games.csv") -> List[Dict[str, Any]]:
    path = DATASET_DIR / filename

    champion_by_id = load_champion_name_mapping()
    champ_tags_by_id = load_champion_tags_mapping()
    spell_by_id = load_summoner_spell_mapping()

    games: List[Dict[str, Any]] = []

    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            game: Dict[str, Any] = {}

            game["gameId"] = _to_int(row, "gameId")
            game["creationTime"] = _to_int(row, "creationTime")
            game["gameDuration"] = _to_int(row, "gameDuration")
            game["seasonId"] = _to_int(row, "seasonId")

            winner = _to_int(row, "winner")
            game["winner"] = winner
            game["team1Wins"] = (winner == 1)

            game["firstBlood"] = _to_int(row, "firstBlood")
            game["firstTower"] = _to_int(row, "firstTower")
            game["firstInhibitor"] = _to_int(row, "firstInhibitor")
            game["firstBaron"] = _to_int(row, "firstBaron")
            game["firstDragon"] = _to_int(row, "firstDragon")
            game["firstRiftHerald"] = _to_int(row, "firstRiftHerald")

            t1_champs = [
                _to_int(row, "t1_champ1id"),
                _to_int(row, "t1_champ2id"),
                _to_int(row, "t1_champ3id"),
                _to_int(row, "t1_champ4id"),
                _to_int(row, "t1_champ5id"),
            ]
            t2_champs = [
                _to_int(row, "t2_champ1id"),
                _to_int(row, "t2_champ2id"),
                _to_int(row, "t2_champ3id"),
                _to_int(row, "t2_champ4id"),
                _to_int(row, "t2_champ5id"),
            ]

            game["t1_champ_ids"] = t1_champs
            game["t2_champ_ids"] = t2_champs

            game["t1_champ_names"] = [
                champion_by_id.get(cid, f"Unknown_{cid}") for cid in t1_champs
            ]
            game["t2_champ_names"] = [
                champion_by_id.get(cid, f"Unknown_{cid}") for cid in t2_champs
            ]

            game["t1_champ_tags"] = [
                champ_tags_by_id.get(cid, []) for cid in t1_champs
            ]
            game["t2_champ_tags"] = [
                champ_tags_by_id.get(cid, []) for cid in t2_champs
            ]

            t1_spells_ids = [
                [
                    _to_int(row, "t1_champ1_sum1"),
                    _to_int(row, "t1_champ1_sum2"),
                ],
                [
                    _to_int(row, "t1_champ2_sum1"),
                    _to_int(row, "t1_champ2_sum2"),
                ],
                [
                    _to_int(row, "t1_champ3_sum1"),
                    _to_int(row, "t1_champ3_sum2"),
                ],
                [
                    _to_int(row, "t1_champ4_sum1"),
                    _to_int(row, "t1_champ4_sum2"),
                ],
                [
                    _to_int(row, "t1_champ5_sum1"),
                    _to_int(row, "t1_champ5_sum2"),
                ],
            ]
            t2_spells_ids = [
                [
                    _to_int(row, "t2_champ1_sum1"),
                    _to_int(row, "t2_champ1_sum2"),
                ],
                [
                    _to_int(row, "t2_champ2_sum1"),
                    _to_int(row, "t2_champ2_sum2"),
                ],
                [
                    _to_int(row, "t2_champ3_sum1"),
                    _to_int(row, "t2_champ3_sum2"),
                ],
                [
                    _to_int(row, "t2_champ4_sum1"),
                    _to_int(row, "t2_champ4_sum2"),
                ],
                [
                    _to_int(row, "t2_champ5_sum1"),
                    _to_int(row, "t2_champ5_sum2"),
                ],
            ]

            game["t1_summoner_spells_ids"] = t1_spells_ids
            game["t2_summoner_spells_ids"] = t2_spells_ids

            game["t1_summoner_spells_names"] = [
                [spell_by_id.get(sid, f"Unknown_{sid}") for sid in pair]
                for pair in t1_spells_ids
            ]
            game["t2_summoner_spells_names"] = [
                [spell_by_id.get(sid, f"Unknown_{sid}") for sid in pair]
                for pair in t2_spells_ids
            ]

            game["t1_towerKills"] = _to_int(row, "t1_towerKills")
            game["t1_inhibitorKills"] = _to_int(row, "t1_inhibitorKills")
            game["t1_baronKills"] = _to_int(row, "t1_baronKills")
            game["t1_dragonKills"] = _to_int(row, "t1_dragonKills")
            game["t1_riftHeraldKills"] = _to_int(row, "t1_riftHeraldKills")

            game["t2_towerKills"] = _to_int(row, "t2_towerKills")
            game["t2_inhibitorKills"] = _to_int(row, "t2_inhibitorKills")
            game["t2_baronKills"] = _to_int(row, "t2_baronKills")
            game["t2_dragonKills"] = _to_int(row, "t2_dragonKills")
            game["t2_riftHeraldKills"] = _to_int(row, "t2_riftHeraldKills")

            t1_bans = [
                _to_int(row, "t1_ban1"),
                _to_int(row, "t1_ban2"),
                _to_int(row, "t1_ban3"),
                _to_int(row, "t1_ban4"),
                _to_int(row, "t1_ban5"),
            ]
            t2_bans = [
                _to_int(row, "t2_ban1"),
                _to_int(row, "t2_ban2"),
                _to_int(row, "t2_ban3"),
                _to_int(row, "t2_ban4"),
                _to_int(row, "t2_ban5"),
            ]

            game["t1_bans"] = t1_bans
            game["t2_bans"] = t2_bans

            game["t1_ban_names"] = [
                champion_by_id.get(bid, f"Unknown_{bid}") for bid in t1_bans
            ]
            game["t2_ban_names"] = [
                champion_by_id.get(bid, f"Unknown_{bid}") for bid in t2_bans
            ]

            game["t1_objectives"] = [
                game["t1_towerKills"],
                game["t1_inhibitorKills"],
                game["t1_baronKills"],
                game["t1_dragonKills"],
                game["t1_riftHeraldKills"],
            ]
            game["t2_objectives"] = [
                game["t2_towerKills"],
                game["t2_inhibitorKills"],
                game["t2_baronKills"],
                game["t2_dragonKills"],
                game["t2_riftHeraldKills"],
            ]

            games.append(game)

    return games