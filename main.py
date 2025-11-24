from typing import List, Dict, Any
import sys

from data_loading import load_games_csv
from stats import (
    compute_stats,
    print_stats,
    compute_lol_stats,
    print_lol_stats,
    print_champion_winrate,
    print_objectives_stats,
)
from filters import (
    filter_by_field,
    filter_by_list_length,
    filter_by_champion_played,
    filter_by_champion_banned,
    filter_by_tag,
)
from sorting import sort_by_field
from io_formats import save_csv, save_json, save_xml, save_yaml
from fields import FILTERABLE_FIELDS, LIST_FIELDS, SORTABLE_FIELDS
from presets import load_presets, save_presets, apply_preset

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


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


def print_main_menu() -> None:
    print("\n=== MENU PRINCIPAL ===")
    print("1. Résumé")
    print("2. Statistiques")
    print("3. Statistiques avancées")
    print("4. Filtrer")
    print("5. Trier")
    print("6. Presets de filtres")
    print("7. Sauvegarder")
    print("8. Réinitialiser les données")
    print("0. Quitter")


def print_filter_menu() -> None:
    print("\n--- MENU FILTRAGE ---")
    print("1. Filtrer par champ")
    print("2. Filtrer par taille de liste")
    print("3. Filtrer par champion joué")
    print("4. Filtrer par champion banni")
    print("5. Filtrer par tag (rôle)")
    print("0. Retour")


def print_sort_menu() -> None:
    print("\n--- MENU TRI ---")
    print("1. Trier par champ")
    print("0. Retour")


def print_save_menu() -> None:
    print("\n--- MENU SAUVEGARDE ---")
    print("1. Sauvegarder en CSV")
    print("2. Sauvegarder en JSON")
    print("3. Sauvegarder en XML")
    print("4. Sauvegarder en YAML")
    print("0. Retour")


def print_presets_menu() -> None:
    print("\n--- PRESETS DE FILTRES ---")
    print("1. Sauvegarder les filtres actuels comme preset")
    print("2. Charger un preset")
    print("3. Supprimer un preset")
    print("0. Retour")


def choose_field_from_list(fields: List[str]) -> str | None:
    print("\nChamps disponibles :")
    for i, f in enumerate(fields, 1):
        print(f"{i}. {f}")
    index = input("Numéro du champ : ").strip()
    if not index.isdigit():
        print("Choix invalide.")
        return None
    i = int(index)
    if not (1 <= i <= len(fields)):
        print("Choix invalide.")
        return None
    return fields[i - 1]


OP_LABELS = {
    "==": "eq",
    "!=": "ne",
    "<": "lt",
    "<=": "le",
    ">": "gt",
    ">=": "ge",
}


def main() -> None:
    all_games = load_games_csv("games.csv")
    current_data: List[Dict[str, Any]] = list(all_games)
    filters_history: List[str] = []

    print(f"{len(all_games)} parties chargées.")

    while True:
        print_main_menu()
        choice = input("Choix : ").strip()

        if choice == "0":
            print("Au revoir.")
            break

        elif choice == "1":
            print(f"\nRésumé : {len(current_data)} parties dans les données courantes.")
            if filters_history:
                print("Filtres actifs :", ", ".join(filters_history))
            else:
                print("Aucun filtre actif.")
            if current_data:
                from pprint import pprint
                print("Exemple de partie :")
                pprint(current_data[0])

        elif choice == "2":
            stats = compute_stats(current_data)
            print_stats(stats)

        elif choice == "3":
            lol_stats = compute_lol_stats(current_data)

            print("\n--- STATISTIQUES AVANCÉES ---")
            print("1. Vue d'ensemble")
            print("2. Champion précis")
            print("3. Objectifs (premiers drakes, barons, tours, etc.)")
            print("0. Retour")

            sub = input("Choix : ").strip()

            if sub == "1":
                print_lol_stats(lol_stats)

            elif sub == "2":
                name = input("Nom du champion : ").strip()
                if name:
                    print_champion_winrate(lol_stats, name)
                else:
                    print("Nom vide, retour au menu.")

            elif sub == "3":
                print_objectives_stats(lol_stats)

            elif sub == "0":
                pass
            else:
                print("Choix invalide.")

        elif choice == "4":
            while True:
                print_filter_menu()
                sub = input("Choix (filtrer) : ").strip()

                if sub == "0":
                    break

                elif sub == "1":
                    field = choose_field_from_list(FILTERABLE_FIELDS)
                    if field is None:
                        continue
                    op = input("Opérateur (==, !=, <, <=, >, >=) : ").strip()
                    val = _parse_value(input("Valeur : "))
                    current_data = filter_by_field(current_data, field, op, val)
                    label = OP_LABELS.get(op, op)
                    filters_history.append(f"{field}_{label}_{val}")
                    print(len(current_data), "résultats après filtrage.")

                elif sub == "2":
                    field = choose_field_from_list(LIST_FIELDS)
                    if field is None:
                        continue
                    op = input("Opérateur (==, !=, <, <=, >, >=) : ").strip()
                    raw_len = input("Longueur (entier) : ").strip()
                    try:
                        length = int(raw_len)
                    except ValueError:
                        print("Longueur invalide.")
                        continue
                    current_data = filter_by_list_length(current_data, field, op, length)
                    label = OP_LABELS.get(op, op)
                    filters_history.append(f"{field}_len_{label}_{length}")
                    print(len(current_data), "résultats après filtrage.")

                elif sub == "3":
                    name = input("Nom du champion : ").strip()
                    if not name:
                        print("Nom vide.")
                        continue
                    current_data = filter_by_champion_played(current_data, name)
                    filters_history.append(f"champ_played_{name}")
                    print(len(current_data), "résultats après filtrage.")

                elif sub == "4":
                    name = input("Nom du champion banni : ").strip()
                    if not name:
                        print("Nom vide.")
                        continue
                    current_data = filter_by_champion_banned(current_data, name)
                    filters_history.append(f"champ_banned_{name}")
                    print(len(current_data), "résultats après filtrage.")

                elif sub == "5":
                    tag = input("Tag / rôle (ex: Assassin) : ").strip()
                    if not tag:
                        print("Tag vide.")
                        continue
                    raw_min = input("Nombre min de champions avec ce tag : ").strip()
                    try:
                        min_count = int(raw_min) if raw_min else 1
                    except ValueError:
                        min_count = 1
                    current_data = filter_by_tag(current_data, tag, min_count)
                    filters_history.append(f"tag_{tag}_ge_{min_count}")
                    print(len(current_data), "résultats après filtrage.")

                else:
                    print("Choix invalide (filtrer).")

        elif choice == "5":
            while True:
                print_sort_menu()
                sub = input("Choix (tri) : ").strip()

                if sub == "0":
                    break

                elif sub == "1":
                    field = choose_field_from_list(SORTABLE_FIELDS)
                    if field is None:
                        continue
                    order = input("Ordre (asc/desc) : ").strip().lower()
                    reverse = (order == "desc")
                    current_data = sort_by_field(current_data, field, reverse)
                    print("Tri effectué.")

                else:
                    print("Choix invalide (tri).")

        elif choice == "6":
            while True:
                print_presets_menu()
                sub = input("Choix (presets) : ").strip()

                if sub == "0":
                    break

                elif sub == "1":
                    if not filters_history:
                        print("Aucun filtre actif à sauvegarder.")
                        continue
                    name = input("Nom du preset : ").strip()
                    if not name:
                        print("Nom vide, preset non sauvegardé.")
                        continue
                    presets = load_presets()
                    presets[name] = list(filters_history)
                    save_presets(presets)
                    print(f"Preset '{name}' sauvegardé.")

                elif sub == "2":
                    presets = load_presets()
                    if not presets:
                        print("Aucun preset disponible.")
                        continue
                    names = list(presets.keys())
                    print("\nPresets disponibles :")
                    for i, n in enumerate(names, 1):
                        descs = presets[n]
                        print(f"{i}. {n} ({len(descs)} filtres)")
                    idx = input("Numéro du preset : ").strip()
                    if not idx.isdigit():
                        print("Choix invalide.")
                        continue
                    i = int(idx)
                    if not (1 <= i <= len(names)):
                        print("Choix invalide.")
                        continue
                    selected_name = names[i - 1]
                    descriptors = presets[selected_name]
                    current_data, filters_history = apply_preset(all_games, descriptors)
                    print(f"Preset '{selected_name}' appliqué.")
                    print(len(current_data), "résultats après application du preset.")

                elif sub == "3":
                    presets = load_presets()
                    if not presets:
                        print("Aucun preset à supprimer.")
                        continue
                    names = list(presets.keys())
                    print("\nPresets disponibles :")
                    for i, n in enumerate(names, 1):
                        print(f"{i}. {n}")
                    idx = input("Numéro du preset à supprimer : ").strip()
                    if not idx.isdigit():
                        print("Choix invalide.")
                        continue
                    i = int(idx)
                    if not (1 <= i <= len(names)):
                        print("Choix invalide.")
                        continue
                    to_delete = names[i - 1]
                    del presets[to_delete]
                    save_presets(presets)
                    print(f"Preset '{to_delete}' supprimé.")

                else:
                    print("Choix invalide (presets).")

        elif choice == "7":
            while True:
                print_save_menu()
                sub = input("Choix (sauvegarde) : ").strip()

                if sub == "0":
                    break

                else:
                    base_name = "_".join(filters_history) if filters_history else "all_data"

                    if sub == "1":
                        filename = base_name + ".csv"
                        save_csv(current_data, filename)

                    elif sub == "2":
                        filename = base_name + ".json"
                        save_json(current_data, filename)

                    elif sub == "3":
                        filename = base_name + ".xml"
                        save_xml(current_data, filename)

                    elif sub == "4":
                        filename = base_name + ".yaml"
                        save_yaml(current_data, filename)

                    else:
                        print("Choix invalide (sauvegarde).")

        elif choice == "8":
            current_data = list(all_games)
            filters_history = []
            print("Données réinitialisées.")

        else:
            print("Choix invalide.")


if __name__ == "__main__":
    main()