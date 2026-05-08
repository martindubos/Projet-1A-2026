"""
CHAPITRE 2.3 - CHOIX TECHNOLOGIQUES
Détecte les bibliothèques utilisées dans le projet.
"""

import os, sys, ast

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def extraire_imports(chemin):
    imports = set()
    try:
        with open(chemin, encoding="utf-8") as f:
            tree = ast.parse(f.read())
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for a in node.names:
                    imports.add(a.name.split('.')[0])
            elif isinstance(node, ast.ImportFrom):
                if node.module and not node.module.startswith('src'):
                    imports.add(node.module.split('.')[0])
    except Exception:
        pass
    return imports

tous_imports = set()
for dp, dns, fnames in os.walk(ROOT):
    dns[:] = [d for d in dns if d not in
              {'__pycache__', '.git', '.venv', 'venv', '.claude', 'rapport'}]
    for f in fnames:
        if f.endswith(".py"):
            tous_imports |= extraire_imports(os.path.join(dp, f))

stdlib = {'os', 'sys', 'datetime', 'pickle', 'ast', 'json', 'csv', 'math',
          'random', 'time', 'collections', 'itertools', 'functools', 'typing',
          'abc', 're', 'pathlib', 'io', 'copy', 'warnings', 'inspect',
          'unittest', 'subprocess'}
libs = sorted(tous_imports - stdlib - {'src', '__future__', ''})

descriptions = {
    "pandas":     "Lecture CSV, filtres, agrégations",
    "matplotlib": "Graphiques : barres, courbes, camemberts, histogrammes",
    "pickle":     "Sérialisation des objets (cache données)",
    "pytest":     "Framework de tests unitaires",
}

print("=" * 65)
print("2.3 CHOIX TECHNOLOGIQUES")
print("=" * 65)
print("\nLANGAGE : Python 3.10+ | Paradigme : POO\n")
print("BIBLIOTHÈQUES DÉTECTÉES :")
for lib in libs:
    print(f"  • {lib:<15} — {descriptions.get(lib, 'TODO: décrire')}")

print("\nOUTILS DE DÉVELOPPEMENT :")
for o, d in [("Git / GitHub",       "Gestion de versions et collaboration"),
             ("VS Code",            "IDE principal"),
             ("Onyxia / SSP Cloud", "Environnement d'exécution cloud ENSAI"),
             ("pytest",             "Tests automatisés")]:
    print(f"  • {o:<22} — {d}")

print("""
JUSTIFICATIONS :
  pandas    : Standard pour la manipulation de CSV en Python.
  matplotlib: Bibliothèque de visualisation la plus répandue,
              permet graphiques interactifs et export PNG.
  pickle    : Cache les objets chargés → évite de relire les CSV
              à chaque lancement (gain de temps significatif).
  Git       : Imposé par le cahier des charges.

TODO: Compléter avec vos propres justifications.
""")
