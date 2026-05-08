"""
CHAPITRE 2.2 - ARCHITECTURE GÉNÉRALE
Affiche l'arborescence et des métriques du code.
"""

import os

ROOT    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IGNORER = {'__pycache__', '.git', '.venv', 'venv', 'objets',
           '.claude', 'figures', '.pytest_cache', 'rapport'}

def arborescence(dossier, prefixe="", max_prof=4, prof=0):
    if prof > max_prof:
        return
    try:
        entrees = sorted(os.listdir(dossier))
    except PermissionError:
        return
    entrees = [e for e in entrees if e not in IGNORER and not e.endswith('.p')]
    for i, entree in enumerate(entrees):
        est_dernier = (i == len(entrees) - 1)
        connecteur  = "└── " if est_dernier else "├── "
        chemin      = os.path.join(dossier, entree)
        if os.path.isdir(chemin):
            print(f"{prefixe}{connecteur}{entree}/")
            arborescence(chemin, prefixe + ("    " if est_dernier else "│   "), max_prof, prof+1)
        else:
            print(f"{prefixe}{connecteur}{entree}")

print("=" * 65)
print("2.2 ARCHITECTURE GÉNÉRALE")
print("=" * 65)
print(f"\n{os.path.basename(ROOT)}/")
arborescence(ROOT)

print("""
COUCHES DE L'APPLICATION :

  [__main__.py]      Interface CLI (menus, saisies, affichage)
        │
  [src/Analysis/]    Couche Analyse (recherche, statistiques avancées)
        │
  [src/Parsers/]     Couche Chargement (un loader par sport)
        │
  [src/Model/]       Couche Modèle (Player, Team, Match, Sport)
        │
  [data/]            Données brutes CSV (lecture seule)
  [objets/]          Cache pickle (données sérialisées)

FLUX DE DONNÉES :
  [CSV] → [Parser] → [Model] → [Sport] → sauvegarde pickle
                                              ↓
                                        chargement pickle
                                              ↓
                                    [__main__.py] → affichage / graphiques
""")

couches = {"Model": "src/Model", "Parsers": "src/Parsers",
           "Analysis": "src/Analysis", "Tests": "test"}
print("MÉTRIQUES DU CODE :\n")
total = 0
for couche, rel in couches.items():
    chemin = os.path.join(ROOT, rel)
    nb_f = nb_l = 0
    for dp, _, fnames in os.walk(chemin):
        for f in fnames:
            if f.endswith(".py") and f != "__init__.py":
                nb_f += 1
                with open(os.path.join(dp, f), encoding="utf-8") as fh:
                    nb_l += sum(1 for _ in fh)
    total += nb_l
    print(f"  {couche:<12} : {nb_f:>3} fichiers, {nb_l:>5} lignes")
with open(os.path.join(ROOT, "__main__.py"), encoding="utf-8") as fh:
    ml = sum(1 for _ in fh)
total += ml
print(f"  {'__main__.py':<12} :   1 fichier , {ml:>5} lignes")
print(f"  {'─'*40}")
print(f"  {'TOTAL':<12} :         {total:>5} lignes")
