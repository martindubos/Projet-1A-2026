"""
CHAPITRE 3.1 - ORGANISATION DU TRAVAIL
Analyse le dépôt Git.
"""

import os, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def git(cmd):
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=ROOT)
        return r.stdout.strip()
    except Exception as e:
        return f"Erreur : {e}"

print("=" * 65)
print("3.1 ORGANISATION DU TRAVAIL")
print("=" * 65)

print(f"\nNombre de commits    : {git('git rev-list --count HEAD')}")
print(f"Premier commit       : {git('git log --reverse --format=%ad --date=short | head -1')}")
print(f"Dernier commit       : {git('git log -1 --format=%ad --date=short')}")

print("\nCONTRIBUTIONS PAR AUTEUR :")
for ligne in git("git shortlog -sn --no-merges HEAD").split('\n'):
    if ligne.strip():
        parts = ligne.strip().split('\t', 1)
        if len(parts) == 2:
            print(f"  {parts[1]:<30} : {parts[0].strip():>4} commits")

print("\nHISTORIQUE (20 derniers commits) :")
for ligne in git("git log --oneline --no-merges -20").split('\n'):
    print(f"  {ligne}")

print("\nFICHIERS LES PLUS MODIFIÉS :")
f = git("git log --no-merges --name-only --pretty=format: | sort | uniq -c | sort -rn | head -10")
for ligne in f.split('\n'):
    if ligne.strip():
        print(f"  {ligne.strip()}")

print("""
À COMPLÉTER :

[RÉPARTITION DES TÂCHES]
TODO:
      - Étudiant A : ...
      - Étudiant B : ...
      - Étudiant C : ...

[WORKFLOW GIT]
TODO: Branches utilisées, fréquence des commits, PR, revues de code.

[COMMUNICATION]
TODO: Discord, réunions, outils utilisés.
""")
