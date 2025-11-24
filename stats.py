from typing import List, Dict, Any


def compute_stats(data: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    stats: Dict[str, Dict[str, Any]] = {}
    if not data:
        return stats

    keys = set()
    for d in data:
        keys.update(d.keys())

    for key in keys:
        values = [d[key] for d in data if key in d and d[key] is not None]
        if not values:
            continue

        first = values[0]

        if isinstance(first, (int, float, bool)):
            numeric_vals = []
            for v in values:
                if isinstance(v, bool):
                    numeric_vals.append(1 if v else 0)
                elif isinstance(v, (int, float)):
                    numeric_vals.append(v)
            if not numeric_vals:
                continue
            s = sum(numeric_vals)
            mn = min(numeric_vals)
            mx = max(numeric_vals)
            avg = s / len(numeric_vals)
            stats[key] = {
                "type": "number",
                "min": mn,
                "max": mx,
                "avg": avg,
            }

        elif isinstance(first, list):
            lengths = [len(v) for v in values if isinstance(v, list)]
            if not lengths:
                continue
            mn = min(lengths)
            mx = max(lengths)
            avg = sum(lengths) / len(lengths)
            stats[key] = {
                "type": "list",
                "min_len": mn,
                "max_len": mx,
                "avg_len": avg,
            }

        else:
            stats[key] = {
                "type": "other",
                "example": first,
            }

    return stats


def print_stats(stats: Dict[str, Dict[str, Any]]) -> None:
    if not stats:
        print("Aucune donnée pour les statistiques.")
        return

    for field, info in stats.items():
        t = info.get("type")
        if t == "number":
            print(f"\n{field} (number)")
            print(f"min = {info['min']}")
            print(f"max = {info['max']}")
            print(f"avg = {info['avg']:.2f}")
        elif t == "list":
            print(f"\n{field} (list)")
            print(f"min length = {info['min_len']}")
            print(f"max length = {info['max_len']}")
            print(f"avg length = {info['avg_len']:.2f}")
        else:
            print(f"\n{field} ({t})")
            print(f"example = {info.get('example')}")


def compute_lol_stats(data: List[Dict[str, Any]]) -> Dict[str, Any]:
    stats: Dict[str, Any] = {}
    n = len(data)
    stats["total_games"] = n
    if n == 0:
        return stats

    team1_wins = sum(1 for g in data if g.get("team1Wins") is True)
    stats["team1_winrate"] = team1_wins / n

    objectives = ["firstTower", "firstDragon", "firstBaron", "firstInhibitor", "firstRiftHerald"]
    obj_stats: Dict[str, Dict[str, Any]] = {}

    for obj in objectives:
        t1_games = t1_wins = 0
        t2_games = t2_wins = 0
        for g in data:
            v = g.get(obj)
            if v == 1:
                t1_games += 1
                if g.get("team1Wins"):
                    t1_wins += 1
            elif v == 2:
                t2_games += 1
                if not g.get("team1Wins"):
                    t2_wins += 1
        obj_stats[obj] = {
            "t1_games": t1_games,
            "t1_wins": t1_wins,
            "t1_winrate": (t1_wins / t1_games) if t1_games > 0 else None,
            "t2_games": t2_games,
            "t2_wins": t2_wins,
            "t2_winrate": (t2_wins / t2_games) if t2_games > 0 else None,
        }

    stats["objectives"] = obj_stats

    champ_stats: Dict[str, Dict[str, Any]] = {}
    for g in data:
        t1_names = g.get("t1_champ_names", [])
        t2_names = g.get("t2_champ_names", [])
        t1_set = {name for name in t1_names if isinstance(name, str)}
        t2_set = {name for name in t2_names if isinstance(name, str)}
        t1_win = bool(g.get("team1Wins"))

        for name in t1_set:
            if name not in champ_stats:
                champ_stats[name] = {"games": 0, "wins": 0}
            champ_stats[name]["games"] += 1
            if t1_win:
                champ_stats[name]["wins"] += 1

        for name in t2_set:
            if name not in champ_stats:
                champ_stats[name] = {"games": 0, "wins": 0}
            champ_stats[name]["games"] += 1
            if not t1_win:
                champ_stats[name]["wins"] += 1

    for name, cs in champ_stats.items():
        gms = cs["games"]
        cs["winrate"] = cs["wins"] / gms if gms > 0 else None

    stats["champions"] = champ_stats
    return stats


def print_lol_stats(stats: Dict[str, Any], min_games_for_champion: int = 50) -> None:
    total = stats.get("total_games", 0)
    print("\n======== STATISTIQUES LOL AVANCÉES ========")

    print(f"\n📊 Nombre total de parties analysées : {total}")

    winrate_t1 = stats.get("team1_winrate")
    if winrate_t1 is not None:
        print(f"\n🏆 Winrate global (Team 1) : {winrate_t1 * 100:.2f}%")

    obj_stats = stats.get("objectives", {})
    if obj_stats:
        print("\n-------------------------------------------")
        print("🔥 IMPACT DES PREMIERS OBJECTIFS")
        print("-------------------------------------------")

        for obj, info in obj_stats.items():
            print(f"\n➡ {obj} :")

            t1_games = info["t1_games"]
            t2_games = info["t2_games"]
            t1_wr = info["t1_winrate"]
            t2_wr = info["t2_winrate"]

            if t1_games > 0 and t1_wr is not None:
                print(
                    f"  - Team 1 prend le {obj} en premier : "
                    f"{t1_games} parties, {t1_wr * 100:.2f}% de victoires"
                )

            if t2_games > 0 and t2_wr is not None:
                print(
                    f"  - Team 2 prend le {obj} en premier : "
                    f"{t2_games} parties, {t2_wr * 100:.2f}% de victoires"
                )

    champ_stats = stats.get("champions", {})
    if not champ_stats:
        print("\nAucune statistique de champions disponible.")
        print("\n===========================================\n")
        return

    print("\n-------------------------------------------")
    print(f"👑 TOP CHAMPIONS PAR NOMBRE DE PARTIES (min {min_games_for_champion})")
    print("-------------------------------------------")

    champs_sorted = sorted(
        champ_stats.items(),
        key=lambda item: item[1]["games"],
        reverse=True,
    )

    count = 0
    for name, cs in champs_sorted:
        games = cs["games"]
        if games < min_games_for_champion:
            continue
        wins = cs["wins"]
        wr = cs.get("winrate")
        if wr is None:
            continue
        print(f"- {name:<12} | {games:4d} games | {wins:4d} wins | {wr * 100:5.2f}%")
        count += 1
        if count >= 10:
            break

    print("\n-------------------------------------------")
    print(f"💎 TOP WINRATES (min {min_games_for_champion} games)")
    print("-------------------------------------------")

    champs_sorted_wr = sorted(
        (item for item in champ_stats.items() if item[1]["games"] >= min_games_for_champion),
        key=lambda item: item[1]["winrate"],
        reverse=True,
    )

    count = 0
    for name, cs in champs_sorted_wr:
        games = cs["games"]
        wins = cs["wins"]
        wr = cs.get("winrate")
        if wr is None:
            continue
        print(f"- {name:<12} | {games:4d} games | {wins:4d} wins | {wr * 100:5.2f}%")
        count += 1
        if count >= 10:
            break

    print("\n===========================================\n")


def print_champion_winrate(stats: Dict[str, Any], name: str) -> None:
    champs = stats.get("champions", {})
    name = name.strip()

    if name not in champs:
        print(f"\n⚠️ Le champion '{name}' n'apparaît pas dans les données.")
        return

    data = champs[name]
    games = data["games"]
    wins = data["wins"]
    wr = data["winrate"] * 100 if data["winrate"] is not None else None

    print("\n===== STATISTIQUES DU CHAMPION =====")
    print(f"Champion : {name}")
    print(f"Parties totales : {games}")
    print(f"Victoires : {wins}")
    if wr is not None:
        print(f"Winrate : {wr:.2f}%")
    else:
        print("Winrate : N/A")
    print("====================================\n")


def print_objectives_stats(stats: Dict[str, Any]) -> None:
    total = stats.get("total_games", 0)
    print("\n====== STATISTIQUES SUR LES OBJECTIFS ======")
    print(f"\nNombre total de parties analysées : {total}")

    winrate_t1 = stats.get("team1_winrate")
    if winrate_t1 is not None:
        print(f"Winrate global (Team 1) : {winrate_t1 * 100:.2f}%")

    obj_stats = stats.get("objectives", {})
    if not obj_stats:
        print("\nAucune statistique d'objectifs disponible.")
        print("\n===========================================\n")
        return

    print("\nImpact des premiers objectifs :")
    for obj, info in obj_stats.items():
        print(f"\n- {obj} :")
        t1_games = info["t1_games"]
        t2_games = info["t2_games"]
        t1_wr = info["t1_winrate"]
        t2_wr = info["t2_winrate"]

        if t1_games > 0 and t1_wr is not None:
            print(
                f"  Team 1 prend le {obj} en premier : "
                f"{t1_games} parties, {t1_wr * 100:.2f}% de victoires"
            )

        if t2_games > 0 and t2_wr is not None:
            print(
                f"  Team 2 prend le {obj} en premier : "
                f"{t2_games} parties, {t2_wr * 100:.2f}% de victoires"
            )

    print("\n===========================================\n")