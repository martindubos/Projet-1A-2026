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
    "Q-F": "Qualifications (Finale)",
    "Q-SF": "Qualifications (Demi-finale)",
    "Q-QF": "Qualifications (Quart de finale)",
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
                est_equipe = (type_sport.lower() in ["football", "basketball", "volleyball"])
                nouveau_sport = Sport(nom, dossier, sport_en_equipe=est_equipe, type_sport=type_sport)
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
            is_tennis = type_sport.lower() == "tennis"
            is_foot = type_sport.lower() == "football"
            is_basket = type_sport.lower() == "basketball"
            is_badminton = type_sport.lower() == "badminton"
            print("\nQuel type de statistiques souhaitez-vous consulter ?")
            if is_tennis:
                print(f"1. Rechercher les statistiques d'un joueur precis (Ex: {ex_joueur})")
                print("2. Historique des confrontations entre 2 joueurs")
                print("3. Retour au menu principal")
            elif is_foot:
                print(f"1. Rechercher les statistiques d'un joueur precis (Ex: {ex_joueur})")
                print(f"2. Rechercher les statistiques d'une equipe (Ex: {ex_equipe})")
                print("3. Comparer deux equipes (Face-a-Face)")
                print("4. Vue detaillee par championnat")
                print("5. Voir l'evolution d'un joueur ou d'une equipe (Graphique)")
                print("6. Retour au menu principal")
            elif is_basket:
                print(f"1. Rechercher les statistiques d'un joueur precis (Ex: {ex_joueur})")
                print(f"2. Rechercher les statistiques d'une equipe (Ex: {ex_equipe})")
                print("3. Historique de confrontations entre 2 equipes")
                print("4. Vue detaillee de la NBA")
                print("5. Retour au menu principal")
            elif is_badminton:
                print(f"1. Rechercher les statistiques d'un joueur precis (Ex: {ex_joueur})")
                print("2. Historique des confrontations entre 2 joueurs")
                print("3. Retour au menu principal")
            else:
                print(f"1. Rechercher les statistiques d'un joueur precis (Ex: {ex_joueur})")
                print(f"2. Rechercher les statistiques d'une equipe/club (Ex: {ex_equipe})")
                print("3. Comparer deux joueurs / equipes (Face-a-Face)")
                print("4. Afficher les joueurs/equipes par pays d'origine")
                print("5. Afficher l'evolution du classement (Graphique)")
                print("6. Retour au menu principal")
            
            choix_stat = input("Votre choix : ")
            
            # Ajustement des choix pour le Tennis
            # Ajustement des choix pour le Football et le Tennis
            if is_tennis or is_badminton:
                if choix_stat == "2": choix_stat = "3" # Redirige vers H2H
                elif choix_stat == "3": choix_stat = "6" # Redirige vers Retour
            
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
                        if is_foot:
                            print(f"{i}. {j.nom_complet()}")
                        else:
                            print(f"{i}. {j.nom_complet()} ({CODE_TO_COUNTRY.get(j.pays, j.pays)})")
                    
                    choix_j = input("Choisissez le numero du joueur (ou Entree pour annuler) : ")
                    if choix_j.isdigit() and 1 <= int(choix_j) <= len(matches):
                        joueur = matches[int(choix_j) - 1]
                    else:
                        print("Choix invalide ou annule.")

                if joueur:
                    print(f"\n--- Fiche du joueur ---")
                    print(f"Nom complet: {joueur.nom_complet()}")
                    if joueur.date_naissance: print(f"Date de naissance: {joueur.date_naissance.strftime('%d/%m/%Y')}")
                    if joueur.taille: print(f"Taille: {joueur.taille} cm")
                    if is_basket:
                        if hasattr(joueur, 'weight') and joueur.weight: print(f"Poids: {joueur.weight} lbs")
                        if hasattr(joueur, 'position') and joueur.position: print(f"Poste: {joueur.position}")
                    if not is_foot:
                        print(f"Pays: {CODE_TO_COUNTRY.get(joueur.pays, joueur.pays)}")

                    # --- Statistiques globales calculées depuis les matchs ---
                    est_equipe = getattr(objet_sport, 'sport_en_equipe', False) or (type_sport.lower() in ["football", "basketball", "volleyball"])
                    if est_equipe:
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
                            
                            saisons_joueur = sorted(list(set(str(m.saison) for m in matchs_joueur if m.saison)))
                            saisons_str = ", ".join(saisons_joueur)
                            
                            titre_stats = f"sur l'ensemble des saisons disponibles : {saisons_str}" if is_foot else (f"saisons disponibles : {saisons_str}" if (is_tennis or is_badminton) else "toutes saisons")
                            print(f"\n>>> STATISTIQUES GLOBALES ({titre_stats}) :")
                            print(f"  - Matchs joues     : {total_matchs}")
                            if is_foot:
                                print(f"\nButs marques par l'equipe (en sa presence) : {victoires}")
                            elif is_basket:
                                # Plus de stats moyennes pour le basket (data manquante)
                                pass
                            else:
                                taux_victoire = (victoires / total_matchs * 100)
                                print(f"  - Taux de victoire : {taux_victoire:.1f}%")

                            if is_tennis:
                                def get_val(m, attr):
                                    v = getattr(m, attr, 0)
                                    # Vérifie si c'est None ou NaN (NaN != NaN en Python)
                                    if v is None or v != v:
                                        return 0
                                    return v

                                total_aces = sum(get_val(m, 'w_ace' if m.vainqueur_id() == joueur.id else 'l_ace') for m in matchs_joueur)
                                total_df = sum(get_val(m, 'w_df' if m.vainqueur_id() == joueur.id else 'l_df') for m in matchs_joueur)
                                total_svpt = sum(get_val(m, 'w_svpt' if m.vainqueur_id() == joueur.id else 'l_svpt') for m in matchs_joueur)
                                total_1stIn = sum(get_val(m, 'w_1stIn' if m.vainqueur_id() == joueur.id else 'l_1stIn') for m in matchs_joueur)
                                total_bpSaved = sum(get_val(m, 'w_bpSaved' if m.vainqueur_id() == joueur.id else 'l_bpSaved') for m in matchs_joueur)
                                total_bpFaced = sum(get_val(m, 'w_bpFaced' if m.vainqueur_id() == joueur.id else 'l_bpFaced') for m in matchs_joueur)

                                print(f"  - Total Aces       : {int(total_aces)}")
                                print(f"  - Double Fautes    : {int(total_df)}")
                                if total_svpt > 0:
                                    print(f"  - 1er Service In   : {(total_1stIn / total_svpt * 100):.1f}%")
                                if total_bpFaced > 0:
                                    print(f"  - Balles de break sauves : {(total_bpSaved / total_bpFaced * 100):.1f}%")

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
                                    print("1. Afficher toutes les statistiques")
                                    print("2. Retour")

                                    choix_s = input("Votre choix : ").strip()
                                    if not choix_s:
                                        continue

                                    try:
                                        idx = int(choix_s)
                                        if idx == 1:
                                            print(f"\n>>> TOUTES LES STATISTIQUES ({saison_cle}) :")
                                            for k, v in stats.items():
                                                if k == "Resultats en compétitions" and isinstance(v, dict):
                                                    print(f"  - {k} :")
                                                    for t, r in v.items():
                                                        print(f"    * {t} : {TENNIS_ROUND_MAP.get(r, r)}")
                                                else:
                                                    val = TENNIS_ROUND_MAP.get(v, v) if k == "Meilleur resultat en Grand Chelem" else v
                                                    print(f"  - {k} : {val}")
                                        elif idx == 2:
                                            break
                                        else:
                                            print("Choix invalide (Veuillez choisir 1 ou 2).")
                                    except ValueError:
                                        print("Veuillez entrer un numero valide.")
                elif not matches:
                    pass # Déjà affiché plus haut

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
                            stats = equipe.statistiques[saison_cle]
                            
                            if is_foot:
                                # On identifie la ligue de l'équipe pour cette saison
                                ligue_id = None
                                for m in objet_sport.matchs:
                                    if m.saison == saison_cle and (m.equipe1_id == equipe.id or m.equipe2_id == equipe.id):
                                        ligue_id = getattr(m, 'league_id', None)
                                        break
                                
                                if ligue_id:
                                    classement = objet_sport.calculer_classement(saison_filtre=saison_cle)
                                    # Filtrer par ligue
                                    equipes_ligue = set()
                                    for m in objet_sport.matchs:
                                        if m.saison == saison_cle and getattr(m, 'league_id', None) == ligue_id:
                                            equipes_ligue.add(m.equipe1_id)
                                            equipes_ligue.add(m.equipe2_id)
                                    
                                    classement_ligue = [(id_e, pts) for id_e, pts in classement if id_e in equipes_ligue]
                                    rang = next((i + 1 for i, (id_e, _) in enumerate(classement_ligue) if id_e == equipe.id), None)
                                    if rang:
                                        print(f"  - Rang en championnat : {rang}e sur {len(classement_ligue)} equipes")
                                        pts = next((p for id_e, p in classement_ligue if id_e == equipe.id), 0)
                                        print(f"  - Points : {pts}")

                            if is_basket:
                                print(f"  - Points par match (PPG)  : {stats.get('PPG', 'N/A')}")
                                print(f"  - Rebonds par match (RPG) : {stats.get('RPG', 'N/A')}")
                                print(f"  - Passes par match (APG)  : {stats.get('APG', 'N/A')}")
                                print(f"  - True Shooting % (TS%)   : {stats.get('TS%', 'N/A')}%")
                                
                                print(f"\n>>> STATISTIQUES AVANCEES :")
                                print(f"  - Net Rating      : {stats.get('Net Rating', 'N/A')}")
                                print(f"  - OffRtg / DefRtg : {stats.get('OffRtg', 'N/A')} / {stats.get('DefRtg', 'N/A')}")
                                print(f"  - eFG%            : {stats.get('eFG%', 'N/A')}%")
                                print(f"  - Pace (Rythme)   : {stats.get('Pace', 'N/A')}")
                                print(f"  - AST/TOV         : {stats.get('AST/TOV', 'N/A')}")
                                
                                print(f"\n{'='*60}")
                                print("LEGENDE DES STATISTIQUES BASKETBALL :")
                                print("-" * 60)
                                print("PPG/RPG/APG : Moyennes de Points, Rebonds et Passes par match.")
                                print("TS%         : True Shooting % (Efficacite globale incluant les lancers francs).")
                                print("Net Rating  : Difference de points marques/encaisses sur 100 possessions.")
                                print("OffRtg      : Points marques pour 100 possessions.")
                                print("DefRtg      : Points encaisses pour 100 possessions.")
                                print("eFG%        : Efficacite au tir (ajuste la valeur des tirs a 3 points).")
                                print("Pace        : Nombre de possessions estimees par match (48 minutes).")
                                print("AST/TOV     : Ratio Passes decisives / Pertes de balle.")
                                print(f"{'='*60}")
                            else:
                                for k, v in stats.items():
                                    print(f"  - {k} : {v}")
                        else:
                            print("Saison invalide ou introuvable.")
                else:
                    print("Equipe introuvable. Attention, certains sports comme le Tennis n'ont pas d'equipes.")

            elif choix_stat == "3":
                if is_tennis or is_badminton:
                    print("\n--- Historique des confrontations entre 2 joueurs ---")
                    entite1 = rechercher_et_choisir_entite(objet_sport, 'joueur', "Nom du premier joueur : ")
                    if not entite1:
                        print("Premier joueur introuvable.")
                        continue
                    entite2 = rechercher_et_choisir_entite(objet_sport, 'joueur', "Nom du deuxieme joueur : ")
                    if not entite2:
                        print("Deuxieme joueur introuvable.")
                        continue
                    choix_type = '1'
                elif is_foot or is_basket:
                    titre = "Comparer deux equipes" if is_foot else "Historique de confrontations entre 2 equipes"
                    print(f"\n--- {titre} ---")
                    entite1 = rechercher_et_choisir_entite(objet_sport, 'equipe', "Nom de la premiere equipe : ")
                    if not entite1:
                        print("Premiere equipe introuvable.")
                        continue
                    entite2 = rechercher_et_choisir_entite(objet_sport, 'equipe', "Nom de la deuxieme equipe : ")
                    if not entite2:
                        print("Deuxieme equipe introuvable.")
                        continue
                    choix_type = '2'
                else:
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
                if is_basket:
                    saisons_disponibles = sorted(list(set(m.saison for m in objet_sport.matchs if m.saison)))
                    if not saisons_disponibles:
                        print("Aucune donnee de match disponible.")
                        continue
                    print(f"Saisons disponibles : {', '.join(saisons_disponibles)}")
                    s = input("Quelle saison ? : ").strip()
                    if s not in saisons_disponibles:
                        print("Saison invalide.")
                        continue
                    
                    print("\n--- VUE DETAILLEE NBA ---")
                    print("1. Phase Regulière")
                    print("2. Playoffs")
                    print("3. Stats globales")
                    choix_nba = input("Votre choix : ")
                    
                    if choix_nba == "1":
                        east_ids = {1610612737, 1610612738, 1610612751, 1610612766, 1610612741, 1610612739, 1610612765, 1610612754, 1610612748, 1610612749, 1610612752, 1610612753, 1610612755, 1610612761, 1610612764}
                        west_ids = {1610612743, 1610612744, 1610612745, 1610612746, 1610612747, 1610612763, 1610612750, 1610612740, 1610612760, 1610612756, 1610612757, 1610612758, 1610612759, 1610612762, 1610612742}
                        bilans = {}
                        for m in objet_sport.matchs:
                            if m.saison == s and getattr(m, 'season_type', '') == 'Regular Season':
                                for id_e in [m.equipe1_id, m.equipe2_id]:
                                    if id_e not in bilans: bilans[id_e] = [0, 0]
                                winner = m.vainqueur_id()
                                if winner:
                                    bilans[winner][0] += 1
                                    loser = m.equipe1_id if winner == m.equipe2_id else m.equipe2_id
                                    bilans[loser][1] += 1
                                    
                        def afficher_conf(nom_conf, ids):
                            print(f"\n>>> CONFERENCE {nom_conf.upper()}")
                            conf_stats = []
                            for id_e, b in bilans.items():
                                if id_e in ids:
                                    eq = objet_sport.equipes.get(id_e)
                                    wins, losses = b
                                    pct = wins / (wins + losses) if (wins + losses) > 0 else 0
                                    conf_stats.append({'nom': eq.nom if eq else f"ID {id_e}", 'w': wins, 'l': losses, 'pct': pct})
                            conf_stats.sort(key=lambda x: x['pct'], reverse=True)
                            header = f"{'Pl.':<3} | {'Equipe':<25} | {'V-D':<7} | {'%':<5}"
                            print("-" * len(header))
                            print(header); print("-" * len(header))
                            for i, st in enumerate(conf_stats, 1):
                                color = "\033[94m" if 1 <= i <= 6 else ("\033[93m" if 7 <= i <= 8 else "")
                                reset = "\033[0m" if color else ""
                                print(f"{color}{i:<3} | {st['nom']:<25} | {st['w']}-{st['l']:<5} | {st['pct']:.3f}{reset}")
                            print("-" * len(header))
                        afficher_conf("East", east_ids); afficher_conf("West", west_ids)
                        print("Legende : \033[94mPlay-off (1-6)\033[0m | \033[93mPlay-in (7-8)\033[0m")

                    elif choix_nba == "2":
                        playoff_matchs = [m for m in objet_sport.matchs if m.saison == s and getattr(m, 'season_type', '') in ['Playoffs', 'Play-In']]
                        if not playoff_matchs:
                            print("Aucun match de playoffs trouve.")
                        else:
                            east_ids = {1610612737, 1610612738, 1610612751, 1610612766, 1610612741, 1610612739, 1610612765, 1610612754, 1610612748, 1610612749, 1610612752, 1610612753, 1610612755, 1610612761, 1610612764}
                            
                            series_data = {} # (team1, team2) -> {'wins': [w1, w2], 'type': 'Playoffs'/'Play-In', 'first_date': date}
                            for m in playoff_matchs:
                                teams = tuple(sorted([m.equipe1_id, m.equipe2_id]))
                                if teams not in series_data:
                                    series_data[teams] = {'wins': [0, 0], 'type': getattr(m, 'season_type', 'Playoffs'), 'first_date': m.date}
                                winner = m.vainqueur_id()
                                if winner == teams[0]: series_data[teams]['wins'][0] += 1
                                elif winner == teams[1]: series_data[teams]['wins'][1] += 1
                            
                            # Categorization
                            rounds = {
                                "Play-In East": [], "Play-In West": [],
                                "1er Tour East": [], "1er Tour West": [],
                                "Demi-finales East": [], "Demi-finales West": [],
                                "Finales de Conference East": [], "Finales de Conference West": [],
                                "Finales NBA": []
                            }
                            
                            for (id1, id2), data in series_data.items():
                                eq1, eq2 = objet_sport.equipes.get(id1), objet_sport.equipes.get(id2)
                                n1, n2 = eq1.nom if eq1 else str(id1), eq2.nom if eq2 else str(id2)
                                w1, w2 = data['wins']
                                score_str = f"{n1} {w1}-{w2} {n2}" if w1 >= w2 else f"{n2} {w2}-{w1} {n1}"
                                
                                is_east = id1 in east_ids and id2 in east_ids
                                is_west = id1 not in east_ids and id2 not in east_ids
                                
                                if data['type'] == 'Play-In':
                                    if is_east: rounds["Play-In East"].append(score_str)
                                    else: rounds["Play-In West"].append(score_str)
                                elif not is_east and not is_west:
                                    rounds["Finales NBA"].append(score_str)
                                else:
                                    # Heuristique basée sur le nombre de victoires max pour déterminer le tour
                                    # Ou simplement le nombre de matchs joués dans la série?
                                    conf = "East" if is_east else "West"
                                    # On peut aussi regarder le nombre de séries déjà trouvées pour ce tour
                                    wins_max = max(w1, w2)
                                    if wins_max <= 1: # Play-in possiblement marqué comme Playoffs
                                        rounds[f"Play-In {conf}"].append(score_str)
                                    else:
                                        # On va trier par date pour répartir dans les tours
                                        pass
                            
                            # Approche simplifiée par date pour les tours Playoffs
                            all_series = []
                            for (id1, id2), data in series_data.items():
                                if data['type'] == 'Playoffs':
                                    all_series.append({'teams': (id1, id2), 'data': data})
                            all_series.sort(key=lambda x: x['data']['first_date'] if x['data']['first_date'] else "")
                            
                            # On répartit : les 8 premières = 1er tour, les 4 suivantes = demis, 2 = finales conf, 1 = NBA finals
                            po_series = [s for s in all_series if (s['teams'][0] in east_ids and s['teams'][1] in east_ids) or (s['teams'][0] not in east_ids and s['teams'][1] not in east_ids)]
                            finals_series = [s for s in all_series if s not in po_series]
                            
                            # Répartition par date
                            for i, s in enumerate(po_series):
                                id1, id2 = s['teams']; w1, w2 = s['data']['wins']
                                eq1, eq2 = objet_sport.equipes.get(id1), objet_sport.equipes.get(id2)
                                n1, n2 = eq1.nom if eq1 else str(id1), eq2.nom if eq2 else str(id2)
                                score_str = f"{n1} {w1}-{w2} {n2}" if w1 >= w2 else f"{n2} {w2}-{w1} {n1}"
                                conf = "East" if id1 in east_ids else "West"
                                
                                if i < 8: rounds[f"1er Tour {conf}"].append(score_str)
                                elif i < 12: rounds[f"Demi-finales {conf}"].append(score_str)
                                else: rounds[f"Finales de Conference {conf}"].append(score_str)
                            
                            for s in finals_series:
                                id1, id2 = s['teams']; w1, w2 = s['data']['wins']
                                eq1, eq2 = objet_sport.equipes.get(id1), objet_sport.equipes.get(id2)
                                n1, n2 = eq1.nom if eq1 else str(id1), eq2.nom if eq2 else str(id2)
                                score_str = f"{n1} {w1}-{w2} {n2}" if w1 >= w2 else f"{n2} {w2}-{w1} {n1}"
                                rounds["Finales NBA"].append(score_str)

                            print(f"\n>>> RÉSULTATS PLAYOFFS {s}")
                            for r_name, scores in rounds.items():
                                if scores:
                                    print(f"\n--- {r_name.upper()} ---")
                                    for sc in scores: print(f"  {sc}")

                    elif choix_nba == "3":
                        matchs_saison = [m for m in objet_sport.matchs if m.saison == s]
                        if not matchs_saison: print("Aucune donnee.")
                        else:
                            total_pts = sum(m.score1 + m.score2 for m in matchs_saison)
                            moy_ligue = total_pts / len(matchs_saison)
                            ot_matchs = len([m for m in matchs_saison if hasattr(m, 'min') and m.min > 240])
                            prolifique = max(matchs_saison, key=lambda m: m.score1 + m.score2)
                            top_score = max(max(m.score1, m.score2) for m in matchs_saison)
                            po_matchs = sorted([m for m in matchs_saison if getattr(m, 'season_type', '') == 'Playoffs'], key=lambda m: m.date if m.date else "")
                            champion = objet_sport.equipes.get(po_matchs[-1].vainqueur_id()).nom if po_matchs else "Inconnu"
                            bilans = {}
                            for m in [m for m in matchs_saison if getattr(m, 'season_type', '') == 'Regular Season']:
                                for id_e in [m.equipe1_id, m.equipe2_id]:
                                    if id_e not in bilans: bilans[id_e] = [0, 0]
                                w = m.vainqueur_id(); l = m.equipe1_id if w == m.equipe2_id else m.equipe2_id
                                if w: bilans[w][0] += 1; bilans[l][1] += 1
                            def get_nom(id_e): return objet_sport.equipes.get(id_e).nom if id_e in objet_sport.equipes else str(id_e)
                            best_bilan_id = max(bilans.items(), key=lambda x: x[1][0]/(x[1][0]+x[1][1]) if (x[1][0]+x[1][1])>0 else 0)[0]
                            worst_bilan_id = min(bilans.items(), key=lambda x: x[1][0]/(x[1][0]+x[1][1]) if (x[1][0]+x[1][1])>0 else 0)[0]
                            best_nr_team = max(objet_sport.equipes.values(), key=lambda e: e.statistiques.get(s, {}).get('Net Rating', -999))
                            best_at_team = max(objet_sport.equipes.values(), key=lambda e: e.statistiques.get(s, {}).get('AST/TOV', 0))
                            print(f"\n>>> STATS GLOBALES NBA - {s}")
                            print(f"  - Moyenne points/match : {moy_ligue:.1f}\n  - Matchs en prolongation : {ot_matchs}")
                            print(f"  - Prolifique : {prolifique.score1 + prolifique.score2} pts ({get_nom(prolifique.equipe1_id)} vs {get_nom(prolifique.equipe2_id)})")
                            print(f"  - Score max : {top_score} pts\n  - Champion : {champion}")
                            print(f"  - Meilleur bilan : {get_nom(best_bilan_id)} ({bilans[best_bilan_id][0]}-{bilans[best_bilan_id][1]})")
                            print(f"  - Pire bilan : {get_nom(worst_bilan_id)} ({bilans[worst_bilan_id][0]}-{bilans[worst_bilan_id][1]})")
                            print(f"  - Meilleur Net Rating : {best_nr_team.nom} ({best_nr_team.statistiques.get(s, {}).get('Net Rating')})")
                            print(f"  - Meilleur AST/TOV : {best_at_team.nom} ({best_at_team.statistiques.get(s, {}).get('AST/TOV')})")
                            if plt:
                                # Bar plot des 5 meilleures attaques
                                top_att = sorted(bilans.keys(), key=lambda id_e: objet_sport.equipes.get(id_e).statistiques.get(s, {}).get('PPG', 0), reverse=True)[:5]
                                noms_att = [get_nom(id_e) for id_e in top_att]
                                ppg_att = [objet_sport.equipes.get(id_e).statistiques.get(s, {}).get('PPG', 0) for id_e in top_att]
                                
                                plt.figure(figsize=(10, 6))
                                plt.bar(noms_att, ppg_att, color='orange', edgecolor='brown')
                                plt.title(f"Top 5 des meilleures attaques (Points par match) - NBA {s}")
                                plt.xlabel("Equipes")
                                plt.ylabel("Points par match (PPG)")
                                plt.ylim(min(ppg_att) - 5, max(ppg_att) + 5)
                                for i, v in enumerate(ppg_att):
                                    plt.text(i, v + 0.5, f"{v:.1f}", ha='center', fontweight='bold')
                                plt.tight_layout()
                                plt.show()
                    continue

                elif is_foot:
                    pays_input = input("\nEntrez le nom du pays ou du championnat (ex: France, England...) : ").strip()
                    
                    target_league_id = None
                    for m in objet_sport.matchs:
                        eq1 = objet_sport.equipes.get(m.equipe1_id)
                        if eq1 and hasattr(eq1, 'pays_id') and eq1.pays_id and pays_input.lower() in eq1.pays_id.lower():
                            target_league_id = getattr(m, 'league_id', None)
                            break
                    
                    if not target_league_id:
                        print(f"Aucun championnat trouve pour : {pays_input}")
                        continue
                        
                    saisons_disponibles = sorted(list(set(m.saison for m in objet_sport.matchs if m.saison and getattr(m, 'league_id', None) == target_league_id)))
                    print(f"Saisons disponibles : {', '.join(saisons_disponibles)}")
                    s = input("Quelle saison ? : ").strip()
                    
                    print(f"\n{'='*60}")
                    print(f"--- VUE DETAILLEE : {pays_input.upper()} - SAISON {s} ---")
                    print(f"{'='*60}")
                    
                    # Calcul des stats globales du championnat
                    matchs_saison = [m for m in objet_sport.matchs if m.saison == s and getattr(m, 'league_id', None) == target_league_id]
                    total_matchs_champ = len(matchs_saison)
                    total_buts_champ = sum(getattr(m, 'score1', 0) + getattr(m, 'score2', 0) for m in matchs_saison)
                    
                    if total_matchs_champ == 0:
                        print("Aucune donnee pour cette saison.")
                        continue
                        
                    moyenne_buts = total_buts_champ / total_matchs_champ
                    
                    # Recuperation des stats par equipe pour le classement
                    classement_global = objet_sport.calculer_classement(saison_filtre=s)
                    equipes_ids = set()
                    for m in matchs_saison:
                        equipes_ids.add(m.equipe1_id)
                        equipes_ids.add(m.equipe2_id)
                    
                    stats_equipes = []
                    for id_e, pts in classement_global:
                        if id_e in equipes_ids:
                            eq = objet_sport.equipes.get(id_e)
                            s_eq = eq.statistiques.get(s, {})
                            stats_equipes.append({
                                'nom': eq.nom if eq else f"Equipe {id_e}",
                                'mj': s_eq.get('Matchs joues', 0),
                                'pts': pts,
                                'buts_m': s_eq.get('Buts marques', 0),
                                'buts_e': s_eq.get('Buts encaisses', 0),
                                'diff': s_eq.get('Difference de buts', 0)
                            })
                    
                    if not stats_equipes:
                        print("Erreur lors de la recuperation des statistiques.")
                        continue
                        
                    best_attack = max(stats_equipes, key=lambda x: x['buts_m'])
                    best_defense = min(stats_equipes, key=lambda x: x['buts_e'])
                    
                    print(f"\n>>> STATISTIQUES GENERALES :")
                    print(f"  - Moyenne de buts/match : {moyenne_buts:.2f}")
                    print(f"  - Meilleure attaque     : {best_attack['nom']} ({best_attack['buts_m']} buts)")
                    print(f"  - Meilleure defense     : {best_defense['nom']} ({best_defense['buts_e']} buts encaisses)")
                    
                    print(f"\n>>> CLASSEMENT COMPLET :")
                    header = f"{'Pl.':<3} | {'Equipe':<25} | {'MJ':<2} | {'Pts':<3} | {'BP':<3} | {'BC':<3} | {'Diff':<4}"
                    print("-" * len(header))
                    print(header)
                    print("-" * len(header))
                    for i, st in enumerate(stats_equipes, 1):
                        print(f"{i:<3} | {st['nom']:<25} | {st['mj']:<2} | {st['pts']:<3} | {st['buts_m']:<3} | {st['buts_e']:<3} | {st['diff']:<+4}")
                    print("-" * len(header))
                    print("Legende : MJ = Matchs Joues | BP = Buts Pour | BC = Buts Contre | Diff = Difference de buts")
                    continue

                pays_input = input("\nEntrez le nom du pays/nationalite : ").strip()
                choix_nation = None
                
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

                if is_foot:
                    if choix_nation == "1":
                        joueurs_trouves = [j for j in objet_sport.joueurs.values() if j.pays and (pays_input.lower() in str(j.pays).lower() or pays_code.lower() in str(j.pays).lower())]
                        equipes_trouvees = []
                    else:
                        joueurs_trouves = []
                        equipes_trouvees = [e for e in objet_sport.equipes.values() if hasattr(e, 'pays_id') and e.pays_id and (pays_input.lower() in str(e.pays_id).lower() or pays_code.lower() in str(e.pays_id).lower())]
                else:
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
                if is_basket:
                    # Retour au menu principal
                    continue
                if is_foot:
                    # On demande directement l'evolution
                    pass 
                
                if not plt:
                    print("\n[Erreur] matplotlib n'est pas installe. Installez-le avec 'pip install matplotlib'.")
                    continue
                
                print("\n--- Evolution du Classement (Graphique) ---")
                if is_foot:
                    choix_type = "2"
                else:
                    choix_type = input("Voir l'evolution d'un Joueur (1) ou d'une Equipe (2) ? ").strip()
                
                if choix_type == "1":
                    entite = rechercher_et_choisir_entite(objet_sport, 'joueur', "Entrez le nom du joueur : ")
                    is_joueur = True
                elif choix_type == "2":
                    prompt_e = "Entrez le nom de l'equipe : " if not is_foot else "Entrez le nom de l'equipe pour voir son evolution : "
                    entite = rechercher_et_choisir_entite(objet_sport, 'equipe', prompt_e)
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
                    if not is_joueur and type_sport.lower() == "football":
                        ligue_de_lequipe = None
                        for m in objet_sport.matchs:
                            if str(m.saison) == str(s) and (m.equipe1_id == entite.id or m.equipe2_id == entite.id):
                                try:
                                    ligue_de_lequipe = m.league_id
                                except AttributeError:
                                    ligue_de_lequipe = None
                                    
                                if ligue_de_lequipe is not None:
                                    break
                                    
                        if ligue_de_lequipe is not None:
                            equipes_de_la_ligue = set()
                            for m in objet_sport.matchs:
                                if str(m.saison) == str(s) and getattr(m, 'league_id', None) == ligue_de_lequipe:
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
                if is_basket:
                    print("Choix invalide.")
                    continue
                pass
            else:
                print("Choix invalide.")
        else:
            print("Choix invalide.")

if __name__ == "__main__":
    main()
