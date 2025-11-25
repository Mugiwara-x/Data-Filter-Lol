# 📘 LoL Data Filter — Projet ESGI

Outil en Python permettant de charger, filtrer, trier et analyser un dataset de **League of Legends**.  
Le programme fonctionne entièrement en terminal, via des menus simples et clairs.

---

## 📁 Contenu du projet

Le projet charge un dataset CSV contenant des milliers de parties LoL, puis l’enrichit automatiquement grâce à trois fichiers JSON :

- `champion_info.json`  
- `champion_info_2.json`  
- `summoner_spell_info.json`  

Le programme convertit ensuite tout en objets Python exploitables pour les filtres, tris et analyses.

---

## 🔎 Fonctionnalités principales

### 🔍 **Filtres**
- Par champ numérique (`gameDuration`, `firstDragon`, etc.)
- Opérateurs : `==`, `!=`, `<`, `<=`, `>`, `>=`
- Par taille de liste (`t1_champ_ids`, `t1_bans`, etc.)
- **Par champion joué**
- **Par champion banni**
- **Par rôle (tag) : Assassin, Tank, Mage…**
- Historique des filtres
- Réinitialisation à tout moment

---

### ↕️ **Tri**
- Tri par n’importe quel champ disponible  
- Ordre croissant ou décroissant

---

### 📊 **Statistiques**
#### Statistiques générales
- Minimum / Maximum / Moyenne pour chaque champ  
- Tailles des listes  

#### Statistiques avancées LoL
- Winrate global de Team 1  
- Impact des premiers objectifs (first Dragon, first Baron, etc.)  
- Top champions par nombre de parties  
- Top champions par winrate  
- Statistiques détaillées d’un champion précis

---

### 🧩 **Presets de filtres**
Vous pouvez :
- Sauvegarder les filtres actuels sous un nom personnalisé  
- Charger un preset existant en un clic  
- Supprimer un preset  

Les presets sont enregistrés dans :

```
presets/presets.json
```

---

### 💾 **Sauvegarde multi-formats**
Export des données filtrées en :

- **CSV**
- **JSON**
- **XML**
- **YAML**

Tous les fichiers sont sauvegardés automatiquement dans :

```
sauvegarde/
```

Avec un nom basé sur les filtres actifs (ex : `champ_played_Thresh_ge_3000.yaml`).

---

## ▶️ Lancer le programme

1. Installer Python 3  
2. Ouvrir un terminal dans le dossier du projet  
3. Lancer le programme :

```bash
python main.py
```

---

## 📦 Structure du projet

```
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
│   └── presets.json     (créé automatiquement)
│── sauvegarde/
│   └── ...              (fichiers exportés)
│── Dataset/
    ├── games.csv
    ├── champion_info.json
    ├── champion_info_2.json
    └── summoner_spell_info.json
```

---

## 👥 Travail en groupe

Pour récupérer le projet :

```bash
git clone https://github.com/Mugiwara-x/Data-Filter-Lol
```

Puis :

```bash
python main.py
```

---
