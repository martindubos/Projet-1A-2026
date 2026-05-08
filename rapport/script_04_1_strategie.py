"""
CHAPITRE 4.1 - STRATÉGIE DE TEST
Liste automatiquement tous les tests du projet.
"""

import os, ast

ROOT     = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEST_DIR = os.path.join(ROOT, "test")

def extraire_tests(chemin):
    tests = []
    try:
        with open(chemin, encoding="utf-8") as f:
            tree = ast.parse(f.read())
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                for item in node.body:
                    if isinstance(item, ast.FunctionDef) and item.name.startswith("test"):
                        tests.append((node.name, item.name))
            elif isinstance(node, ast.FunctionDef) and node.name.startswith("test"):
                tests.append((None, node.name))
    except Exception as e:
        tests.append((None, f"Erreur: {e}"))
    return tests

print("=" * 65)
print("4.1 STRATÉGIE DE TEST")
print("=" * 65)

print("""
APPROCHE :
  Tests unitaires (pytest/unittest) — chaque module clé est testé
  de manière isolée avec des données contrôlées.
""")

total = 0
for dp, _, fnames in os.walk(TEST_DIR):
    for f in sorted(fnames):
        if f.startswith("test_") and f.endswith(".py"):
            chemin = os.path.join(dp, f)
            tests  = extraire_tests(chemin)
            rel    = os.path.relpath(chemin, ROOT)
            print(f"  📄 {rel}  ({len(tests)} test(s))")
            for cls, meth in tests:
                print(f"       └─ {cls+'.' if cls else ''}{meth}")
            total += len(tests)

print(f"\n  Total : {total} tests\n")
print("""
À COMPLÉTER :
TODO: Décrire la stratégie de test.
      - Types de tests (unitaires, intégration)
      - Données de test utilisées
      - Couverture : pytest --cov=src test/ --cov-report=term-missing
      - Modules non couverts et pourquoi
""")
