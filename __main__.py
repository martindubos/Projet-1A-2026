import os
import pickle
from src.Model.Sports import Sport

def sauvegarder_sport(sport: Sport, dossier_objets: str = "objets") -> None:
    os.makedirs(dossier_objets, exist_ok=True)
    chemin = os.path.join(dossier_objets, f"{sport.nom.lower()}.p")
    with open(chemin, "wb") as f:
        pickle.dump(sport, f)

def charger_sport(nom: str, dossier_objets: str = "objets") -> Sport:
    chemin = os.path.join(dossier_objets, f"{nom.lower()}.p")
    if os.path.exists(chemin):
        with open(chemin, "rb") as f:
            return pickle.load(f)
    return None

def main():
    configurations = {
        "1": ("Tennis", "data/tennis"),
        "2": ("Football", "data/football_european_leagues"),
        "3": ("Basketball", "data/basketball"),
        # "4": ("Volleyball", "data/volleyball"),
        # "5": ("LoL", "data/league_of_legends")
    }

    while True:
        print("\n" + "="*30)
        print("=== MENU PRINCIPAL ===")
        print("="*30)
        print("1. Charger les donnees CSV")
        print("2. Consulter des statistiques")
        print("3. Quitter")
        
        choix_menu = input("Que souhaitez-vous faire ? (1/2/3) : ")

        if choix_menu == "3":
            print("Au revoir !")
            break

        elif choix_menu == "1":
            print("\n-- Chargement des donnees --")
            print("Pour quel sport voulez-vous charger les donnees ?")
            for key, (nom, _) in configurations.items():
                print(f"{key}. {nom}")
            print("A. Tous les sports disponibles")
            
            choix_sport = input("Votre choix : ").upper()
            
            sports_a_charger = []
            if choix_sport == "A":
                sports_a_charger = list(configurations.values())
            elif choix_sport in configurations:
                sports_a_charger = [configurations[choix_sport]]
            else:
                print("Choix invalide.")
                continue

            for nom, dossier in sports_a_charger:
                print(f"\nChargement depuis CSV pour {nom}...")
                nouveau_sport = Sport(nom, dossier)
                sauvegarder_sport(nouveau_sport)
                print(f"[{nom}] Les donnees ont ete chargees et sauvegardees.")

        elif choix_menu == "2":
            print("\n-- Consultation des Statistiques --")
            print("Choisissez un sport :")
            for key, (nom, _) in configurations.items():
                print(f"{key}. {nom}")
            
            choix_sport = input("Votre choix : ")
            if choix_sport not in configurations:
                print("Choix invalide.")
                continue
                
            nom_sport = configurations[choix_sport][0]
            
            # Chargement de l'objet sport memoire
            objet_sport = charger_sport(nom_sport)
            if not objet_sport:
                print(f"Les donnees de {nom_sport} n'ont pas encore ete chargees. Veuillez d'abord choisir l'option 1 du menu.")
                continue
                
            ex_joueur = "Novak Djokovic" if nom_sport.lower() == "tennis" else "Lionel Messi" if nom_sport.lower() == "football" else "Joueur Exemple"
            ex_equipe = "France" if nom_sport.lower() == "tennis" else "Real Madrid" if nom_sport.lower() == "football" else "Equipe Exemple"

            # Sous-menu pour les statistiques
            print("\nQuel type de statistiques souhaitez-vous consulter ?")
            print(f"1. Rechercher les statistiques d'un joueur precis (Ex: {ex_joueur})")
            print(f"2. Rechercher les statistiques d'une equipe/club (Ex: {ex_equipe})")
            print("3. Voir le classement global du sport")
            print("4. Comparer deux joueurs / equipes (Face-a-Face)")
            print("5. Afficher les joueurs/equipes par pays d'origine")
            print("6. Retour au menu principal")
            
            choix_stat = input("Votre choix : ")
            
            if choix_stat == "1":
                nom_joueur = input("\nEntrez le nom du joueur (ou une partie du nom) : ")
                joueur = objet_sport.get_joueur(nom_joueur)
                if joueur:
                    print(f"\n--- Fiche du joueur ---")
                    print(f"Nom complet: {joueur.nom_complet()}")
                    if joueur.date_naissance: print(f"Date de naissance: {joueur.date_naissance}")
                    if joueur.taille: print(f"Taille: {joueur.taille} cm")
                    print(f"Pays: {joueur.pays}")
                    print(f"\n>>> STATISTIQUES (2024) :")
                    for k, v in joueur.statistiques.get(2024, {}).items():
                        print(f"  - {k} : {v}")
                else:
                    print("Joueur introuvable.")

            elif choix_stat == "2":
                nom_equipe = input("\nEntrez le nom de l'equipe : ")
                equipe = objet_sport.get_equipe(nom_equipe)
                if equipe:
                    print(f"\n--- Fiche de l'equipe ---")
                    print(f"Nom: {equipe.nom} ({equipe.nom_court})")
                    if not equipe.statistiques:
                        print("\n>>> Aucune statistique disponible pour cette equipe.")
                    else:
                        saisons_disponibles = sorted(list(equipe.statistiques.keys()))
                        print(f"\n>>> Saisons disponibles : {', '.join(map(str, saisons_disponibles))}")
                        saison_choisie = input("Entrez la saison pour voir les statistiques (ex: 2008/2009) : ")
                        
                        saison_cle = saison_choisie
                        # Convertir en int si possible au cas où la clé est numérique (ex: 2024 au Tennis)
                        try:
                            if int(saison_choisie) in equipe.statistiques:
                                saison_cle = int(saison_choisie)
                        except ValueError:
                            pass
                            
                        if saison_cle in equipe.statistiques:
                            print(f"\n>>> STATISTIQUES ({saison_cle}) :")
                            for k, v in equipe.statistiques[saison_cle].items():
                                print(f"  - {k} : {v}")
                        else:
                            print("Saison invalide ou introuvable.")
                else:
                    print("Equipe introuvable. Attention, certains sports comme le Tennis n'ont pas d'equipes.")

            elif choix_stat == "3":
                classement = objet_sport.classement
                if not classement:
                    print(f"\nAucun classement disponible. Le classement va etre calcule...")
                    classement = objet_sport.calculer_classement()
                    
                print(f"\n--- Classement global pour {nom_sport} (Top 10) ---")
                top = classement[:10]
                for i, (id_eq, points) in enumerate(top, 1):
                    print(f"{i}. ID_{id_eq} : {points} points")

            elif choix_stat == "4":
                print("\n--- Face-a-Face (Head-to-Head) ---")
                choix_type = input("Voulez-vous comparer des Joueurs (J) ou des Equipes (E) ? ").upper()
                if choix_type == 'J':
                    nom1 = input("Nom du premier joueur : ")
                    nom2 = input("Nom du deuxieme joueur : ")
                    entite1 = objet_sport.get_joueur(nom1)
                    entite2 = objet_sport.get_joueur(nom2)
                elif choix_type == 'E':
                    nom1 = input("Nom de la premiere equipe : ")
                    nom2 = input("Nom de la deuxieme equipe : ")
                    entite1 = objet_sport.get_equipe(nom1)
                    entite2 = objet_sport.get_equipe(nom2)
                else:
                    print("Choix invalide.")
                    continue
                
                if not entite1 or not entite2:
                    print("Une ou les deux entites n'ont pas ete trouvees.")
                    continue
                
                id1, id2 = entite1.id, entite2.id
                nom_entite1 = entite1.nom_complet() if choix_type == 'J' else entite1.nom
                nom_entite2 = entite2.nom_complet() if choix_type == 'J' else entite2.nom
                
                victoires_1, victoires_2, nuls = 0, 0, 0
                for m in objet_sport.matchs:
                    if (m.equipe1_id == id1 and m.equipe2_id == id2) or (m.equipe1_id == id2 and m.equipe2_id == id1):
                        vainqueur = m.vainqueur_id()
                        if vainqueur == id1:
                            victoires_1 += 1
                        elif vainqueur == id2:
                            victoires_2 += 1
                        else:
                            nuls += 1
                
                print(f"\n>>> Historique des confrontations :")
                print(f"{nom_entite1} - {victoires_1} victoire(s)")
                print(f"{nom_entite2} - {victoires_2} victoire(s)")
                if nuls > 0:
                    print(f"Matchs nuls - {nuls}")
                if (victoires_1 + victoires_2 + nuls) == 0:
                    print("Aucun match trouve entre ces deux opposants.")

            elif choix_stat == "5":
                pays_input = input("\nEntrez le nom du pays/nationalite : ").strip()
                
                mapping_pays = {
                    "france": "FRA", "espagne": "ESP", "italie": "ITA", 
                    "suisse": "SUI", "allemagne": "GER", "angleterre": "ENG", 
                    "etats-unis": "USA", "usa": "USA", "belgique": "BEL", 
                    "argentine": "ARG", "bresil": "BRA", "portugal": "POR",
                    "serbie": "SRB", "croatie": "CRO", "pays-bas": "NED",
                    "russie": "RUS", "canada": "CAN", "australie": "AUS",
                    "grece": "GRE", "japon": "JPN", "chine": "CHN"
                }
                
                pays_code = mapping_pays.get(pays_input.lower(), pays_input)

                joueurs_trouves = [j for j in objet_sport.joueurs.values() if j.pays and (pays_input.lower() in str(j.pays).lower() or pays_code.lower() in str(j.pays).lower())]
                equipes_trouvees = [e for e in objet_sport.equipes.values() if hasattr(e, 'pays_id') and e.pays_id and (pays_input.lower() in str(e.pays_id).lower() or pays_code.lower() in str(e.pays_id).lower())]
                
                if joueurs_trouves:
                    print(f"\n--- Joueurs ({pays_input.capitalize()} / {pays_code.upper()}) ---")
                    for j in joueurs_trouves:
                        print(f"- {j.nom_complet()}")
                if equipes_trouvees:
                    print(f"\n--- Equipes ({pays_input.capitalize()} / {pays_code.upper()}) ---")
                    for e in equipes_trouvees:
                        print(f"- {e.nom}")
                if not joueurs_trouves and not equipes_trouvees:
                    print(f"Aucun resultat trouve pour le pays : {pays_input}")

            elif choix_stat == "6":
                continue
            else:
                print("Choix invalide.")
        else:
            print("Choix invalide.")

if __name__ == "__main__":
    main()
