"""
CHAPITRE 4.2 - RÉSULTATS DES TESTS
Lance pytest et génère une figure.
"""

import os, sys, subprocess
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT        = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIGURES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures")
os.makedirs(FIGURES_DIR, exist_ok=True)

print("=" * 65)
print("4.2 RÉSULTATS DES TESTS")
print("=" * 65)

result = subprocess.run(
    [sys.executable, "-m", "pytest", "test/", "-v", "--tb=short"],
    capture_output=True, text=True, cwd=ROOT
)
print(result.stdout)

lignes = result.stdout.split('\n')
passed = sum(1 for l in lignes if " PASSED" in l)
failed = sum(1 for l in lignes if " FAILED" in l)
error  = sum(1 for l in lignes if " ERROR"  in l)
total  = passed + failed + error

print(f"Réussis : {passed}/{total} | Échoués : {failed} | Erreurs : {error}")
if total > 0:
    print(f"Taux de succès : {passed/total*100:.1f}%")

if total > 0:
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(['Réussis', 'Échoués', 'Erreurs'], [passed, failed, error],
           color=['#4CAF50', '#F44336', '#FF9800'])
    ax.set_title(f"Résultats des tests ({total} tests)", fontweight='bold')
    ax.set_ylabel("Nombre de tests")
    plt.tight_layout()
    path = os.path.join(FIGURES_DIR, "fig_04_2_tests.png")
    plt.savefig(path, dpi=150, bbox_inches='tight')
    print(f"\n✅ Figure : {path}")

print("\nQUALITÉ DU CODE (flake8) :")
flake = subprocess.run(
    [sys.executable, "-m", "flake8", "src/", "--max-line-length=100", "--count", "--statistics"],
    capture_output=True, text=True, cwd=ROOT
)
print(flake.stdout[:1000] if flake.stdout.strip() else "  Aucune erreur ✅")
