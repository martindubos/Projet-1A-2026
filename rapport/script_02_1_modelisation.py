"""
CHAPITRE 2.1 - MODÉLISATION
Décrit les classes du projet.
"""

import os, sys, inspect
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.Model.Player import Player
from src.Model.Match  import Match, MatchTennis, MatchFootball, MatchBasketball, MatchVolley
from src.Model.Team   import Team
from src.Model.Sports import Sport

print("=" * 65)
print("2.1 MODÉLISATION — CLASSES")
print("=" * 65)

classes = [
    ("Player",          Player,          "Représente un joueur (toutes disciplines)"),
    ("Team",            Team,            "Représente une équipe ou un pays"),
    ("Match",           Match,           "Match générique (classe de base)"),
    ("MatchTennis",     MatchTennis,     "Match ATP/WTA (+ surface, round, stats service)"),
    ("MatchFootball",   MatchFootball,   "Match de football (+ league_id, compositions)"),
    ("MatchBasketball", MatchBasketball, "Match NBA (+ season_type)"),
    ("MatchVolley",     MatchVolley,     "Match volleyball (+ gender, stage)"),
    ("Sport",           Sport,           "Agrégateur : joueurs + équipes + matchs"),
]

for nom, cls, desc in classes:
    print(f"\n┌─ {nom}")
    print(f"│  {desc}")
    try:
        sig    = inspect.signature(cls.__init__)
        params = [p for p in sig.parameters if p != 'self']
        if params:
            print(f"│  Attributs : {', '.join(params)}")
    except Exception:
        pass
    methodes = [m for m in dir(cls) if not m.startswith('_') and callable(getattr(cls, m))]
    if methodes:
        print(f"│  Méthodes  : {', '.join(methodes)}")
    print("└" + "─" * 40)

print("""
HIÉRARCHIE D'HÉRITAGE :
  Match
  ├── MatchTennis
  ├── MatchFootball
  ├── MatchBasketball
  └── MatchVolley

CAS D'UTILISATION :
  UC1 - Charger des données CSV
  UC2 - Rechercher un joueur
  UC3 - Consulter stats joueur / saison
  UC4 - Rechercher une équipe
  UC5 - Consulter stats équipe / saison
  UC6 - Comparer deux entités (H2H)
  UC7 - Classement d'un championnat
  UC8 - Évolution graphique
  UC9 - Ajouter un jeu de données

TODO: Insérer le diagramme UML (image) dans le rapport.
""")
