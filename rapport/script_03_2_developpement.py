"""
CHAPITRE 3.2 - DÉVELOPPEMENT
Affiche les extraits de code importants.
"""

import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def extrait(fichier, debut, fin, titre):
    chemin = os.path.join(ROOT, fichier)
    print(f"\n── {titre} ({fichier}, l.{debut}-{fin}) ──")
    try:
        with open(chemin, encoding="utf-8") as f:
            lignes = f.readlines()
        for i, l in enumerate(lignes[debut-1:fin], debut):
            print(f"  {i:>4} │ {l}", end="")
    except Exception as e:
        print(f"  Erreur : {e}")

print("=" * 65)
print("3.2 DÉVELOPPEMENT")
print("=" * 65)

print("""
CHOIX D'ARCHITECTURE :

1. PATTERN DISPATCHER (PlayerLoader / MatchLoader / TeamLoader)
   Chaque loader a une méthode load_all_* qui délègue au loader
   spécifique selon le sport → facilite l'ajout de nouveaux sports.

2. HÉRITAGE POUR LES MATCHS
   Match est générique. Chaque sport hérite et ajoute ses attributs.
   → Traitement uniforme dans Sport.calculer_classement().

3. PERSISTANCE PAR PICKLE
   Les objets Sport sont sérialisés après chargement CSV.
   → Évite de relire les CSV à chaque lancement.

4. RECHERCHE PAR SOUS-CHAÎNE
   nom.lower() in nom_complet().lower()
   → Insensible à la casse, tolère une recherche partielle.
""")

extrait("src/Model/Sports.py", 1, 40, "Classe Sport")
extrait("src/Parsers/PlayerLoader/PlayerLoader.py", 1, 47, "Dispatcher PlayerLoader")
extrait("src/Model/Match.py", 1, 16, "Classe Match (base)")

print("""
À COMPLÉTER :
TODO: Décrire vos choix d'implémentation pour chaque partie clé.
      - Gestion des NaN dans les CSV
      - Calcul du classement
      - Génération des graphiques matplotlib
      - Gestion des homonymes
""")
