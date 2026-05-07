import datetime
import os
import pickle
from src.Model.Sports import Sport

try:
    import matplotlib.pyplot as plt
except ImportError:
    plt = None

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

TENNIS_ROUND_MAP = {
    "W": "Vainqueur",
    "F": "Finaliste",
    "SF": "Demi-finaliste",
    "QF": "Quart de finaliste",
    "R16": "8ème de finale",
    "R32": "16ème de finale",
    "R64": "2ème tour",
    "R128": "1er tour",
    "Aucun": "Aucun"
}

def charger_configurations():
    config_file = "objets/config.p"
    default_config = {
        "1": ["Tennis", "Tennis", "data/tennis"],
        "2": ["Football", "Football", "data/football_european_leagues"],
        "3": ["Basketball", "Basketball", "data/basketball"],
        "4": ["Badminton", "Badminton", "data/badminton"],
        "5": ["Volleyball", "Volleyball", "data/volleyball"]
    }
    if os.path.exists(config_file):
        with open(config_file, "rb") as f:
            return pickle.load(f)
    else:
        os.makedirs(os.path.dirname(config_file), exist_ok=True)
        with open(config_file, "wb") as f:
            pickle.dump(default_config, f)
        return default_config

def sauvegarder_configurations(config):
    with open("objets/config.p", "wb") as f:
        pickle.dump(config, f)

def rechercher_et_choisir_entite(objet_sport, type_entite, prompt):
    """
    Recherche un joueur ou une equipe et permet a l'utilisateur de choisir si plusieurs resultats.
    type_entite: 'joueur' ou 'equipe'
    """
    nom_recherche = input(prompt).strip()
    if type_entite == 'joueur':
        matches = objet_sport.get_joueur_matches(nom_recherche)
    else:
        matches = objet_sport.get_equipe_matches(nom_recherche)
    
    if not matches:
        return None
    
    if len(matches) == 1:
        return matches[0]
    
    print(f"\nPlusieurs {type_entite}s correspondent a '{nom_recherche}' :")
    for i, m in enumerate(matches, 1):
        if type_entite == 'joueur':
            pays_label = CODE_TO_COUNTRY.get(m.pays, m.pays)
            print(f"{i}. {m.nom_complet()} ({pays_label})")
        else:
            print(f"{i}. {m.nom} ({m.nom_court})")
    
    choix = input(f"Choisissez le numero (ou Entree pour annuler) : ")
    if choix.isdigit() and 1 <= int(choix) <= len(matches):
        return matches[int(choix) - 1]
    return None

def main():
    configurations = charger_configurations()

    while True:
        print("\n" + "="*30)
        print("=== MENU PRINCIPAL ===")
        print("="*30)
        print("1. Charger les donnees CSV")
        print("2. Consulter des statistiques")
        print("3. Ajouter un nouveau jeu de donnees")
        print("4. Quitter")
        
        choix_menu = input("Que souhaitez-vous faire ? (1/2/3/4) : ")

        if choix_menu == "4":
            print("Au revoir !")
            break
            
        elif choix_menu == "3":
            print("\n-- Ajouter un nouveau jeu de donnees --")
            nom_affichage = input("Nom a afficher dans le menu (ex: Mes Matchs Foot) : ").strip()
            type_sport = input("Type de sport (Tennis, Football, Basketball) : ").strip()
            dossier = input("Chemin vers le dossier contenant les fichiers CSV (ex: data/mon_foot) : ").strip()
            
            if not os.path.exists(dossier):
                print(f"Attention: Le dossier '{dossier}' n'existe pas encore. Vous pourrez y placer vos CSV plus tard.")
                
            nouvel_index = str(len(configurations) + 1)
            configurations[nouvel_index] = [nom_affichage, type_sport, dossier]
            sauvegarder_configurations(configurations)
            print(f"Le jeu de donnees '{nom_affichage}' a ete ajoute avec succes !")
            continue

        elif choix_menu == "1":
            print("\n-- Chargement des donnees --")
            print("Pour quel sport voulez-vous charger les donnees ?")
            for key, val in configurations.items():
                print(f"{key}. {val[0]}")
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

            for config_val in sports_a_charger:
                nom = config_val[0]
                type_sport = config_val[1]
                dossier = config_val[2]
                
                print(f"\nChargement depuis CSV pour {nom}...")
                nouveau_sport = Sport(nom, dossier, type_sport=type_sport)
                sauvegarder_sport(nouveau_sport)
                print(f"[{nom}] Les donnees ont ete chargees et sauvegardees.")

        elif choix_menu == "2":
            print("\n-- Consultation des Statistiques --")
            print("Choisissez un sport :")
            for key, val in configurations.items():
                print(f"{key}. {val[0]}")
            
            choix_sport = input("Votre choix : ")
            if choix_sport not in configurations:
                print("Choix invalide.")
                continue
                
            nom_sport = configurations[choix_sport][0]
            type_sport = configurations[choix_sport][1]
            
            # Chargement de l'objet sport memoire
            objet_sport = charger_sport(nom_sport)
            if not objet_sport:
                print(f"Les donnees de {nom_sport} n'ont pas encore ete chargees. Veuillez d'abord choisir l'option 1 du menu.")
                continue
                
            ex_joueur = (
                "Novak Djokovic" if type_sport.lower() == "tennis"
                else "Lionel Messi" if type_sport.lower() == "football"
                else "Stephen Curry" if type_sport.lower() == "basketball"
                else "Akane Yamaguchi" if type_sport.lower() == "badminton"
                else "EGONU Paola Ogechi" if type_sport.lower() == "volleyball"
                else "Joueur Exemple"
            )
            ex_equipe = (
                "France" if type_sport.lower() == "tennis"
                else "Real Madrid" if type_sport.lower() == "football"
                else "Golden State Warriors" if type_sport.lower() == "basketball"
                else "FRA" if type_sport.lower() == "volleyball"
                else "Equipe Exemple"
            )

            # Sous-menu pour les statistiques
            print("\nQuel type de statistiques souhaitez-vous consulter ?")
            print(f"1. Rechercher les statistiques d'un joueur precis (Ex: {ex_joueur})")
            print(f"2. Rechercher les statistiques d'une equipe/club (Ex: {ex_equipe})")
            print("3. Comparer deux joueurs / equipes (Face-a-Face)")
            print("4. Afficher les joueurs/equipes par pays d'origine")
            print("5. Afficher l'evolution du classement (Graphique)")
            print("6. Retour au menu principal")
            
            choix_stat = input("Votre choix : ")
            
            if choix_stat == "1":
                nom_joueur = input("\nEntrez le nom du joueur (ou une partie du nom) : ").strip()
                matches = objet_sport.get_joueur_matches(nom_joueur)
                
                joueur = None
                if not matches:
                    print("Joueur introuvable.")
                elif len(matches) == 1:
                    joueur = matches[0]
                else:
                    print(f"\nPlusieurs joueurs correspondent a '{nom_joueur}' :")
                    for i, j in enumerate(matches, 1):
                        print(f"{i}. {j.nom_complet()} ({CODE_TO_COUNTRY.get(j.pays, j.pays)})")
                    
                    choix_j = input("Choisissez le numero du joueur (ou Entree pour annuler) : ")
                    if choix_j.isdigit() and 1 <= int(choix_j) <= len(matches):
                        joueur = matches[int(choix_j) - 1]

                if joueur:
                    print(f"\n--- Fiche du joueur ---")
                    print(f"Nom complet: {joueur.nom_complet()}")
                    if joueur.date_naissance: print(f"Date de naissance: {joueur.date_naissance.strftime('%d/%m/%Y')}")
                    if joueur.taille: print(f"Taille: {joueur.taille} cm")
                    print(f"Pays: {CODE_TO_COUNTRY.get(joueur.pays, joueur.pays)}")

                    # --- Statistiques globales calculées depuis les matchs ---
                    if objet_sport.sport_en_equipe:
                        # Sport d'equipe (Foot, Basket) : recherche dans les compositions
                        matchs_joueur = [
                            m for m in objet_sport.matchs
                            if (hasattr(m, 'joueurs_dom') and joueur.id in m.joueurs_dom) or 
                               (hasattr(m, 'joueurs_ext') and joueur.id in m.joueurs_ext)
                        ]
                    else:
                        # Sport individuel (Tennis) : recherche directe par ID d'entite
                        matchs_joueur = [
                            m for m in objet_sport.matchs
                            if m.equipe1_id == joueur.id or m.equipe2_id == joueur.id
                        ]
                    
                    total_matchs = len(matchs_joueur)
                    
                    if not joueur.statistiques and total_matchs == 0:
                        print("\n>>> Aucune statistique disponible pour ce joueur.")
                    else:
                        if total_matchs > 0:
                            # Calcul des victoires
                            victoires = 0
                            for m in matchs_joueur:
                                v_id = m.vainqueur_id()
                                if v_id is not None:
                                    # Pour le tennis, v_id == joueur.id
                                    # Pour le foot/basket, v_id est l'ID de l'equipe gagnante. 
                                    # On doit verifier si le joueur etait dans l'equipe gagnante.
                                    if objet_sport.sport_en_equipe:
                                        role = "dom" if joueur.id in getattr(m, 'joueurs_dom', []) else "ext"
                                        equipe_joueur_id = m.equipe1_id if role == "dom" else m.equipe2_id
                                        if v_id == equipe_joueur_id:
                                            victoires += 1
                                    else:
                                        if v_id == joueur.id:
                                            victoires += 1
                            
                            taux_victoire = (victoires / total_matchs * 100)
                            print(f"\n>>> STATISTIQUES GLOBALES (toutes saisons) :")
                            print(f"  - Matchs joues     : {total_matchs}")
                            print(f"  - Taux de victoire : {taux_victoire:.1f}%")

                        if joueur.statistiques:
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
                                        val = TENNIS_ROUND_MAP.get(v, v) if k == "Meilleur resultat en Grand Chelem" else v
                                        print(f"  - {k} : {val}")
                                elif choix_stat_joueur.isdigit() and 1 <= int(choix_stat_joueur) <= len(keys):
                                    k = keys[int(choix_stat_joueur) - 1]
                                    val = TENNIS_ROUND_MAP.get(stats[k], stats[k]) if k == "Meilleur resultat en Grand Chelem" else stats[k]
                                    print(f"\n  - {k} : {val}")
                                elif choix_stat_joueur == str(len(keys) + 1):
                                    break
                                else:
                                    print("Choix invalide.")
                else:
                    print("Joueur introuvable.")

            elif choix_stat == "2":
                nom_equipe = input("\nEntrez le nom de l'equipe (ou une partie du nom) : ").strip()
                matches = objet_sport.get_equipe_matches(nom_equipe)
                
                equipe = None
                if not matches:
                    print("Equipe introuvable. Attention, certains sports comme le Tennis n'ont pas d'equipes.")
                elif len(matches) == 1:
                    equipe = matches[0]
                else:
                    print(f"\nPlusieurs equipes correspondent a '{nom_equipe}' :")
                    for i, e in enumerate(matches, 1):
                        print(f"{i}. {e.nom} ({e.nom_court})")
                    
                    choix_e = input("Choisissez le numero de l'equipe (ou Entree pour annuler) : ")
                    if choix_e.isdigit() and 1 <= int(choix_e) <= len(matches):
                        equipe = matches[int(choix_e) - 1]

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
                print("\n--- Face-a-Face (Head-to-Head) ---")
                choix_type = input("Voulez-vous comparer des Joueurs (1) ou des Equipes (2) ? ").upper()
                if choix_type == '1':
                    entite1 = rechercher_et_choisir_entite(objet_sport, 'joueur', "Nom du premier joueur : ")
                    if not entite1:
                        print("Premier joueur introuvable.")
                        continue
                    entite2 = rechercher_et_choisir_entite(objet_sport, 'joueur', "Nom du deuxieme joueur : ")
                    if not entite2:
                        print("Deuxieme joueur introuvable.")
                        continue
                elif choix_type == '2':
                    entite1 = rechercher_et_choisir_entite(objet_sport, 'equipe', "Nom de la premiere equipe : ")
                    if not entite1:
                        print("Premiere equipe introuvable. Attention, certains sports comme le Tennis n'ont pas d'equipes.")
                        continue
                    entite2 = rechercher_et_choisir_entite(objet_sport, 'equipe', "Nom de la deuxieme equipe : ")
                    if not entite2:
                        print("Deuxieme equipe introuvable. Attention, certains sports comme le Tennis n'ont pas d'equipes.")
                        continue
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

            elif choix_stat == "4":
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

            elif choix_stat == "5":
                if not plt:
                    print("\n[Erreur] matplotlib n'est pas installe. Installez-le avec 'pip install matplotlib'.")
                    continue
                
                print("\n--- Evolution du Classement (Graphique) ---")
                choix_type = input("Voir l'evolution d'un Joueur (1) ou d'une Equipe (2) ? ").strip()
                if choix_type == "1":
                    nom = input("Entrez le nom du joueur : ").strip()
                    entite = objet_sport.get_joueur(nom)
                    is_joueur = True
                elif choix_type == "2":
                    nom = input("Entrez le nom de l'equipe : ").strip()
                    entite = objet_sport.get_equipe(nom)
                    is_joueur = False
                else:
                    print("Choix invalide.")
                    continue
                    
                if not entite:
                    print("Entite introuvable.")
                    continue
                
                # On collecte toutes les saisons disponibles dans les matchs
                saisons_disponibles = set()
                for m in objet_sport.matchs:
                    if m.saison is not None:
                        saisons_disponibles.add(m.saison)
                saisons_disponibles = sorted(list(saisons_disponibles))
                
                if not saisons_disponibles:
                    print("Aucune donnee de saison disponible pour generer le graphique.")
                    continue
                
                nom_affiche = entite.nom_complet() if is_joueur else entite.nom
                
                choix_metrique = input("Voulez-vous afficher l'evolution des Points (1) ou du Classement (2) ? ").strip()
                afficher_classement = (choix_metrique == "2")
                
                print(f"Calcul des donnees par saison pour {nom_affiche}...")
                
                valeurs_par_saison = []
                saisons_plot = []
                
                for s in saisons_disponibles:
                    classement_saison = objet_sport.calculer_classement(saison_filtre=s)
                    
                    # Pour le football, les matchs ont un attribut league_id
                    # On identifie la ligue de l'équipe pour ne comparer que dans son championnat
                    if not is_joueur:
                        ligue_de_lequipe = None
                        for m in objet_sport.matchs:
                            if str(m.saison) == str(s) and (m.equipe1_id == entite.id or m.equipe2_id == entite.id):
                                ligue_de_lequipe = m.league_id
                                if ligue_de_lequipe is not None:
                                    break
                                    
                        if ligue_de_lequipe is not None:
                            equipes_de_la_ligue = set()
                            for m in objet_sport.matchs:
                                if str(m.saison) == str(s) and m.league_id == ligue_de_lequipe:
                                    equipes_de_la_ligue.add(m.equipe1_id)
                                    equipes_de_la_ligue.add(m.equipe2_id)
                            classement_saison = [(id_ent, pts) for id_ent, pts in classement_saison if id_ent in equipes_de_la_ligue]
                    
                    
                    if afficher_classement:
                        # Trouver le rang
                        rang = next((i + 1 for i, (id_ent, _) in enumerate(classement_saison) if id_ent == entite.id), None)
                        if rang is not None:
                            saisons_plot.append(str(s))
                            valeurs_par_saison.append(rang)
                    else:
                        # Trouver les points
                        pts = next((points for id_ent, points in classement_saison if id_ent == entite.id), 0)
                        if pts > 0:
                            saisons_plot.append(str(s))
                            valeurs_par_saison.append(pts)
                            
                if not valeurs_par_saison:
                    print("Aucune donnee trouvee pour cette entite sur les saisons disponibles.")
                    continue
                    
                plt.figure(figsize=(10, 6))
                plt.plot(saisons_plot, valeurs_par_saison, marker='o', linestyle='-', color='b', linewidth=2)
                
                if afficher_classement:
                    plt.title(f"Evolution du classement - {nom_affiche}", fontsize=14)
                    plt.ylabel("Position au classement", fontsize=12)
                    plt.gca().invert_yaxis()  # La 1ere place en haut !
                    from matplotlib.ticker import MaxNLocator
                    plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
                else:
                    plt.title(f"Evolution des points - {nom_affiche}", fontsize=14)
                    plt.ylabel("Points", fontsize=12)
                    
                plt.xlabel("Saison", fontsize=12)
                plt.grid(True, linestyle='--', alpha=0.7)
                plt.xticks(rotation=45)
                plt.tight_layout()
                print(">>> Affichage du graphique dans une nouvelle fenetre. Fermez-la pour continuer.")
                plt.show()

            elif choix_stat == "6":
                pass
            else:
                print("Choix invalide.")
        else:
            print("Choix invalide.")

if __name__ == "__main__":
    main()
