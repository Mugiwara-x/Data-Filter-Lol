LoL Data Filter — Projet ESGI

Projet Python permettant d’explorer, filtrer et analyser un dataset de parties de League of Legends.
Le programme se lance dans un terminal et propose un menu interactif.

📁 Contenu du projet

Chargement du fichier games.csv

Enrichissement automatique avec plusieurs fichiers JSON :

Informations champions

Informations spells

Tags / rôles des champions

Tout est ensuite transformé en une liste d’objets Python exploitable.

🔎 Fonctionnalités
Filtres

Par champ numérique (gameDuration, firstDragon, etc.)

Par opérateur : ==, !=, <, <=, >, >=

Par taille de liste (t1_champ_ids, etc.)

Par champion joué

Par champion banni

Par rôle (Assassin, Tank, Mage…)

Historique des filtres

Réinitialisation des données à tout moment

Tri

Tri par n’importe quel champ numérique

Ordre ascendant ou descendant

Statistiques

Statistiques générales : min/max/moyenne

Statistiques avancées League of Legends :

Winrate global

Impact des premiers objectifs

Top champions par parties jouées

Top winrates

Statistiques d’un champion précis

Presets

Sauvegarde des filtres sous un nom personnalisé

Chargement de presets existants

Suppression de presets

Stockage dans presets/presets.json

Sauvegarde multi-formats

CSV

JSON

XML

YAML
Tous les fichiers sont enregistrés dans le dossier sauvegarde/.

▶️ Lancer le programme

Installer Python 3

Ouvrir un terminal dans le dossier du projet

Lancer :

python main.py


Le menu s’affichera automatiquement.

📦 Structure du projet
Data Filter/
│── main.py
│── data_loading.py
│── filters.py
│── sorting.py
│── stats.py
│── fields.py
│── io_formats.py
│── presets.py
│── presets/
│   └── presets.json   (créé automatiquement)
│── sauvegarde/
│   └── ...            (fichiers exportés)
│── Dataset/
    ├── games.csv
    ├── champion_info.json
    ├── champion_info_2.json
    └── summoner_spell_info.json

👥 Utilisation en groupe

Chaque membre peut cloner le projet :

git clone https://github.com/Mugiwara-x/Data-Filter-Lol


Puis exécuter :

python main.py