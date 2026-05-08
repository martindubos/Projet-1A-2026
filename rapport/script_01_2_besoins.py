"""
CHAPITRE 1.2 - BESOINS FONCTIONNELS
Génère la liste des fonctionnalités depuis le code.
"""

import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

fonctionnalites = {
    "F1 - Chargement des données": {
        "description": "Charger les données CSV de chaque sport et les persister en mémoire (pickle).",
        "sports": ["Tennis (ATP + WTA)", "Football", "Basketball", "Badminton", "Volleyball"],
    },
    "F2 - Recherche de joueur": {
        "description": "Rechercher un joueur par nom (partiel) et afficher sa fiche statistique.",
        "details": ["Recherche insensible à la casse",
                    "Gestion des homonymes",
                    "Statistiques globales calculées depuis les matchs"],
        "sports": ["Tennis", "Football", "Basketball", "Badminton", "Volleyball"]
    },
    "F3 - Statistiques d'équipe": {
        "description": "Consulter les statistiques d'une équipe pour une saison donnée.",
        "details": ["Classement dans le championnat",
                    "Buts marqués / encaissés (Football)",
                    "PPG, RPG, APG, Net Rating, eFG% (Basketball)"],
        "sports": ["Football", "Basketball"]
    },
    "F4 - Confrontations directes (H2H)": {
        "description": "Afficher l'historique des confrontations entre deux joueurs ou équipes.",
        "details": ["Nombre de victoires de chaque côté", "Gestion des matchs nuls"],
        "sports": ["Tennis", "Football", "Basketball", "Badminton"]
    },
    "F5 - Vue détaillée par compétition": {
        "description": "Afficher le classement complet d'un championnat pour une saison.",
        "details": ["Classement Football avec points, buts, différence",
                    "Conférences Est/Ouest, Play-In, Playoffs NBA"],
        "sports": ["Football", "Basketball"]
    },
    "F6 - Évolution graphique": {
        "description": "Tracer l'évolution du classement ou des points saison par saison.",
        "details": ["Graphique matplotlib interactif",
                    "Inversion de l'axe Y pour le classement"],
        "sports": ["Football", "Tennis"]
    },
    "F7 - Statistiques Volleyball JO 2024": {
        "description": "Module dédié aux JO de Paris 2024.",
        "details": ["Résultats par phase", "Ratio de sets",
                    "Profils athlètes", "Encadrement technique"],
        "sports": ["Volleyball"]
    },
    "F8 - Ajout de jeux de données": {
        "description": "Ajouter un nouveau jeu de données CSV sans modifier le code.",
        "sports": ["Tous"]
    },
}

print("=" * 60)
print("1.2 BESOINS FONCTIONNELS")
print("=" * 60)
print(f"\nL'application comprend {len(fonctionnalites)} grandes fonctionnalités :\n")

for code, details in fonctionnalites.items():
    print(f"\n{'─'*50}")
    print(f"  {code}")
    print(f"{'─'*50}")
    print(f"  Description : {details['description']}")
    if "sports" in details:
        print(f"  Sports       : {', '.join(details['sports'])}")
    if "details" in details:
        print("  Détails      :")
        for d in details["details"]:
            print(f"    • {d}")

print("\n" + "=" * 60)
print("CONTRAINTES TECHNIQUES")
print("=" * 60)
for c in ["Python 3", "POO", "Git / GitHub", "Tests unitaires (pytest)",
          "Données CSV uniquement", "Interface CLI"]:
    print(f"  • {c}")
