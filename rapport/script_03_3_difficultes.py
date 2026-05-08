"""
CHAPITRE 3.3 - DIFFICULTÉS RENCONTRÉES
"""

print("=" * 65)
print("3.3 DIFFICULTÉS RENCONTRÉES")
print("=" * 65)

print("""
1. GESTION DES DONNÉES MANQUANTES (NaN)
   Problème  : Les CSV contiennent de nombreuses valeurs manquantes
               (dates, tailles, résultats...).
   Solution  : Utilisation de pd.isna() et valeurs par défaut (None)
               lors de la construction des objets Player/Team/Match.

2. CHEMINS RELATIFS ET RÉPERTOIRE DE TRAVAIL
   Problème  : Selon le répertoire de lancement (IDE, terminal, cloud),
               les fichiers data/ et objets/ n'étaient pas trouvés.
   Solution  : os.chdir(os.path.dirname(os.path.abspath(__file__)))
               ajouté au début de __main__.py.

3. HÉTÉROGÉNÉITÉ DES FORMATS CSV
   Problème  : Chaque sport a un format CSV différent.
   Solution  : Un loader dédié par sport avec logique spécifique.
               La classe Sport unifie ensuite les données.

4. SÉRIALISATION PICKLE ET COMPATIBILITÉ
   Problème  : Si une classe change après création du pickle,
               le chargement échoue silencieusement.
   Solution  : Supprimer les pickles et recharger depuis les CSV.
   Piste     : Versionner les fichiers pickle.

À COMPLÉTER :
TODO: Ajouter les difficultés rencontrées par votre groupe.
      Pour chaque difficulté : problème → identification → solution → bilan.
""")
