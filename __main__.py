import datetime
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

CODE_TO_COUNTRY = {
    "FRA": "France", "ESP": "Espagne", "ITA": "Italie", "SUI": "Suisse",
    "GER": "Allemagne", "ENG": "Angleterre", "USA": "États-Unis", "BEL": "Belgique",
    "ARG": "Argentine", "BRA": "Brésil", "POR": "Portugal", "SRB": "Serbie",
    "CRO": "Croatie", "NED": "Pays-Bas", "RUS": "Russie", "CAN": "Canada",
    "AUS": "Australie", "GRE": "Grèce", "JPN": "Japon", "CHN": "Chine",
    "FR": "France", "ES": "Espagne", "IT": "Italie", "CH": "Suisse",
    "DE": "Allemagne", "UK": "Royaume-Uni", "PT": "Portugal", "NL": "Pays-Bas",
    "BE": "Belgique", "AR": "Argentine", "BR": "Brésil"
}

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
                    if joueur.date_naissance: print(f"Date de naissance: {joueur.date_naissance.strftime('%d/%m/%Y')}")
                    if joueur.taille: print(f"Taille: {joueur.taille} cm")
                    print(f"Pays: {CODE_TO_COUNTRY.get(joueur.pays, joueur.pays)}")

                    if not joueur.statistiques:
                        print("\n>>> Aucune statistique disponible pour ce joueur.")
                    else:
                        saisons_disponibles = sorted(joueur.statistiques.keys())
                        print(f"\n>>> Saisons disponibles : {', '.join(map(str, saisons_disponibles))}")
                        saison_saisie = input("Entrez la saison pour voir les statistiques (ex: 2024) : ").strip()
                        try:
                            saison_cle = int(saison_saisie)
                        except ValueError:
                            saison_cle = saison_saisie

                        if saison_cle not in joueur.statistiques:
                            print("Saison invalide ou introuvable.")
                        else:
                            # --- Statistiques globales calculées depuis les matchs ---
                            matchs_joueur = [
                                m for m in objet_sport.matchs
                                if m.equipe1_id == joueur.id or m.equipe2_id == joueur.id
                            ]
                            total_matchs = len(matchs_joueur)
                            victoires = sum(1 for m in matchs_joueur if m.vainqueur_id() == joueur.id)
                            taux_victoire = (victoires / total_matchs * 100) if total_matchs > 0 else 0.0

                            print(f"\n>>> STATISTIQUES GLOBALES (toutes saisons) :")
                            print(f"  - Matchs joues     : {total_matchs}")
                            print(f"  - Taux de victoire : {taux_victoire:.1f}%")

                            stats = joueur.statistiques[saison_cle]
                            keys = list(stats.keys())

                            # Sous-menu des statistiques
                            while True:
                                print(f"\n=== MENU DES STATISTIQUES ({joueur.nom_complet()} - {saison_cle}) ===")
                                print("0. Afficher toutes les statistiques")
                                for i, k in enumerate(keys, 1):
                                    print(f"{i}. {k}")
                                print(f"{len(keys)+1}. Retour")

                                choix_stat_joueur = input("Votre choix : ").strip()

                                if choix_stat_joueur == "0":
                                    print(f"\n>>> TOUTES LES STATISTIQUES ({saison_cle}) :")
                                    for k, v in stats.items():
                                        print(f"  - {k} : {v}")
                                elif choix_stat_joueur.isdigit() and 1 <= int(choix_stat_joueur) <= len(keys):
                                    k = keys[int(choix_stat_joueur) - 1]
                                    print(f"\n  - {k} : {stats[k]}")
                                elif choix_stat_joueur == str(len(keys) + 1):
                                    break
                                else:
                                    print("Choix invalide.")
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
                    
                # Distinction par sexe si disponible
                sexe_disponibles = set(j.sexe for j in objet_sport.joueurs.values() if j.sexe)
                filtre_sexe = None
                if len(sexe_disponibles) > 1:
                    print("\nVoulez-vous filtrer par sexe ?")
                    print("1. Hommes uniquement")
                    print("2. Femmes uniquement")
                    print("3. Classement global (tout sexe confondu)")
                    choix_filtre = input("Votre choix : ")
                    if choix_filtre == "1": filtre_sexe = "H"
                    elif choix_filtre == "2": filtre_sexe = "F"

                if filtre_sexe:
                    classement_a_afficher = [
                        (id_ent, pts) for id_ent, pts in classement 
                        if id_ent in objet_sport.joueurs and objet_sport.joueurs[id_ent].sexe == filtre_sexe
                    ]
                    titre_classement = f"Classement {'Masculin' if filtre_sexe == 'H' else 'Feminin'}"
                else:
                    classement_a_afficher = classement
                    titre_classement = "Classement global"

                print(f"\n--- {titre_classement} pour {nom_sport} (Top 10) ---")
                top = classement_a_afficher[:10]
                for i, (id_eq, points) in enumerate(top, 1):
                    nom_affiche = f"ID_{id_eq}"
                    if id_eq in objet_sport.joueurs:
                        nom_affiche = objet_sport.joueurs[id_eq].nom_complet()
                    elif id_eq in objet_sport.equipes:
                        nom_affiche = objet_sport.equipes[id_eq].nom
                    print(f"{i}. {nom_affiche} : {points} points")

            elif choix_stat == "4":
                print("\n--- Face-a-Face (Head-to-Head) ---")
                choix_type = input("Voulez-vous comparer des Joueurs (1) ou des Equipes (2) ? ").upper()
                if choix_type == '1':
                    nom1 = input("Nom du premier joueur : ")
                    nom2 = input("Nom du deuxieme joueur : ")
                    entite1 = objet_sport.get_joueur(nom1)
                    entite2 = objet_sport.get_joueur(nom2)
                elif choix_type == '2':
                    nom1 = input("Nom de la premiere equipe : ")
                    nom2 = input("Nom de la deuxieme equipe : ")
                    entite1 = objet_sport.get_equipe(nom1)
                    entite2 = objet_sport.get_equipe(nom2)
                else:
                    print("Choix invalide.")
                    continue
                
                if not entite1 or not entite2:
                    print("Une ou les deux entités n'ont pas été trouvées.")
                    continue
                
                id1, id2 = entite1.id, entite2.id
                nom_entite1 = entite1.nom_complet() if choix_type == '1' else entite1.nom
                nom_entite2 = entite2.nom_complet() if choix_type == '1' else entite2.nom
                
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
                    print("Aucune confrontation.")

            elif choix_stat == "5":
                pays_input = input("\nEntrez le nom du pays/nationalite : ").strip()
                
                # Distinction par sexe si disponible
                sexe_disponibles = set(j.sexe for j in objet_sport.joueurs.values() if j.sexe)
                filtre_sexe = None
                if len(sexe_disponibles) > 1:
                    print("\nVoulez-vous filtrer par sexe ?")
                    print("1. Hommes")
                    print("2. Femmes")
                    print("3. Tous")
                    choix_filtre = input("Votre choix : ")
                    if choix_filtre == "1": filtre_sexe = "H"
                    elif choix_filtre == "2": filtre_sexe = "F"

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

                joueurs_trouves = [
                    j for j in objet_sport.joueurs.values() 
                    if j.pays and (pays_input.lower() in str(j.pays).lower() or pays_code.lower() in str(j.pays).lower())
                    and (not filtre_sexe or j.sexe == filtre_sexe)
                ]
                equipes_trouvees = [e for e in objet_sport.equipes.values() if hasattr(e, 'pays_id') and e.pays_id and (pays_input.lower() in str(e.pays_id).lower() or pays_code.lower() in str(e.pays_id).lower())]
                
                complement_titre = f" ({'Hommes' if filtre_sexe == 'H' else 'Femmes'})" if filtre_sexe else ""
                
                if joueurs_trouves:
                    print(f"\n--- Joueurs {complement_titre} ({pays_input.capitalize()} / {pays_code.upper()}) ---")
                    for j in joueurs_trouves:
                        print(f"- {j.nom_complet()}")
                if equipes_trouvees:
                    print(f"\n--- Equipes ({pays_input.capitalize()} / {pays_code.upper()}) ---")
                    for e in equipes_trouvees:
                        print(f"- {e.nom}")
                if not joueurs_trouves and not equipes_trouvees:
                    print(f"Aucun resultat trouve pour le pays : {pays_input}")

            elif choix_stat == "6":
                pass
            else:
                print("Choix invalide.")
        else:
            print("Choix invalide.")

if __name__ == "__main__":
    main()
