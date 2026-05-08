"""
CHAPITRE 4.3 - LIMITES DE L'APPLICATION
"""

print("=" * 65)
print("4.3 LIMITES DE L'APPLICATION")
print("=" * 65)

print("""
1. INTERFACE CLI UNIQUEMENT
   Pas d'interface graphique. Une GUI web (Streamlit) rendrait
   l'application plus accessible.

2. DONNÉES FIGÉES (2024 / JO 2024)
   Les loaders sont codés en dur pour des fichiers précis.
   → Amélioration : détection automatique ou API temps réel.

3. SÉRIALISATION PICKLE FRAGILE
   Modification d'une classe = pickle incompatible.
   → Amélioration : SQLite ou JSON avec versionnage.

4. PlayerSearch VIDE
   src/Analysis/PlayerSearch.py ne contient qu'une classe vide.
   La logique de recherche est dans __main__.py.

5. __main__.py TROP LONG (1200+ lignes)
   → Amélioration : découper en modules View / Controller.

6. GESTION D'ERREURS SILENCIEUSE
   Les erreurs de chargement sont catchées sans alerter clairement.
   → Amélioration : logging, messages d'erreur explicites.

7. COUVERTURE DE TESTS PARTIELLE
   __main__.py non testé (interactions stdin difficiles à mocker).

À COMPLÉTER :
TODO: Ajouter d'autres limites identifiées par votre groupe.
""")
