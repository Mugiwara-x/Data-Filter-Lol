from typing import List, Dict, Any


def _compare(a: Any, op: str, b: Any) -> bool:
    if op == "==":
        return a == b
    if op == "!=":
        return a != b
    if op == "<":
        return a < b
    if op == "<=":
        return a <= b
    if op == ">":
        return a > b
    if op == ">=":
        return a >= b
    raise ValueError(op)


def filter_by_field(data: List[Dict[str, Any]], field: str, operator: str, value: Any) -> List[Dict[str, Any]]:
    result: List[Dict[str, Any]] = []
    for d in data:
        if field not in d:
            continue
        try:
            if _compare(d[field], operator, value):
                result.append(d)
        except:
            pass
    return result


def filter_by_list_length(data: List[Dict[str, Any]], field: str, operator: str, length: int) -> List[Dict[str, Any]]:
    result: List[Dict[str, Any]] = []
    for d in data:
        if isinstance(d.get(field), list):
            if _compare(len(d[field]), operator, length):
                result.append(d)
    return result


def filter_by_champion_played(data: List[Dict[str, Any]], champion_name: str) -> List[Dict[str, Any]]:
    target = champion_name.strip().lower()
    result: List[Dict[str, Any]] = []
    for d in data:
        names1 = d.get("t1_champ_names", [])
        names2 = d.get("t2_champ_names", [])
        all_names: List[str] = []
        if isinstance(names1, list):
            all_names.extend(names1)
        if isinstance(names2, list):
            all_names.extend(names2)
        if any(isinstance(n, str) and n.lower() == target for n in all_names):
            result.append(d)
    return result


def filter_by_champion_banned(data: List[Dict[str, Any]], champion_name: str) -> List[Dict[str, Any]]:
    target = champion_name.strip().lower()
    result: List[Dict[str, Any]] = []
    for d in data:
        bans1 = d.get("t1_ban_names", [])
        bans2 = d.get("t2_ban_names", [])
        all_bans: List[str] = []
        if isinstance(bans1, list):
            all_bans.extend(bans1)
        if isinstance(bans2, list):
            all_bans.extend(bans2)
        if any(isinstance(n, str) and n.lower() == target for n in all_bans):
            result.append(d)
    return result


def filter_by_tag(data: List[Dict[str, Any]], tag: str, min_count: int = 1) -> List[Dict[str, Any]]:
    target = tag.strip().lower()
    result: List[Dict[str, Any]] = []
    for d in data:
        tags1 = d.get("t1_champ_tags", [])
        tags2 = d.get("t2_champ_tags", [])
        all_tags: List[str] = []
        for team_tags in (tags1, tags2):
            if isinstance(team_tags, list):
                for champ_tags in team_tags:
                    if isinstance(champ_tags, list):
                        all_tags.extend(champ_tags)
        count = sum(1 for t in all_tags if isinstance(t, str) and t.lower() == target)
        if count >= min_count:
            result.append(d)
    return result