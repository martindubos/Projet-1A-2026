import os
import datetime
import pandas as pd
from src.Model.Player import Player


class TennisMenPlayerLoader:

    @staticmethod
    def calculer_nombre_tournois_gagnes(liste_matchs: list) -> dict:
        """
        Compte le nombre de tournois gagnés par chaque joueur.
        Un tournoi est gagné si le joueur a remporté la finale (round == "F").
        On utilise un ensemble (set) pour ne pas compter deux fois le même tournoi.
        """
        tournois_gagnes_par_joueur = {}  

        for match in liste_matchs:
            if match.get("round") != "F":
                continue

            id_gagnant = match.get("winner_id")
            id_tournoi = match.get("tourney_id")

            if id_gagnant is None or id_tournoi is None:
                continue

            if id_gagnant not in tournois_gagnes_par_joueur:
                tournois_gagnes_par_joueur[id_gagnant] = set()

            tournois_gagnes_par_joueur[id_gagnant].add(id_tournoi)
        resultat = {}
        for id_joueur, set_tournois in tournois_gagnes_par_joueur.items():
            resultat[id_joueur] = len(set_tournois)

        return resultat

    @staticmethod
    def calculer_resultats_competitions(liste_matchs: list) -> dict:
        """
        Trouve le meilleur résultat de chaque joueur pour CHAQUE tournoi.
        On attribue un score numérique à chaque tour pour pouvoir comparer.
        """
        poids_par_tour = {
            "R128": 1, "R64": 2, "R32": 3, "R16": 4,
            "QF": 5, "SF": 6, "F": 7
        }
        tour_par_poids = {poids: tour for tour, poids in poids_par_tour.items()}

        resultats_par_joueur = {}

        for match in liste_matchs:
            tournoi = match.get("tourney_name")
            tour_actuel = match.get("round")
            id_perdant = match.get("loser_id")
            id_gagnant = match.get("winner_id")

            if tour_actuel not in poids_par_tour or not tournoi:
                continue

            score_actuel = poids_par_tour[tour_actuel]

            if id_perdant is not None:
                if id_perdant not in resultats_par_joueur:
                    resultats_par_joueur[id_perdant] = {}
                if tournoi not in resultats_par_joueur[id_perdant] or score_actuel > resultats_par_joueur[id_perdant][tournoi]:
                    resultats_par_joueur[id_perdant][tournoi] = score_actuel

            if tour_actuel == "F" and id_gagnant is not None:
                if id_gagnant not in resultats_par_joueur:
                    resultats_par_joueur[id_gagnant] = {}
                resultats_par_joueur[id_gagnant][tournoi] = 8
                
        tour_par_poids[8] = "W"
        final_result = {}
        for id_joueur, stats_tournois in resultats_par_joueur.items():
            final_result[id_joueur] = {t: tour_par_poids[s] for t, s in stats_tournois.items()}

        return final_result

    @staticmethod
    def load_all_player(dossier: str) -> dict:
        """
        Charge tous les joueurs ATP depuis les fichiers CSV du dossier donné.
        Retourne un dictionnaire { id_joueur: Player }.
        """
        fichier_joueurs = os.path.join(dossier, "atp_players_2024.csv")
        fichier_matchs = os.path.join(dossier, "atp_matches_2024.csv")

        if not os.path.exists(fichier_joueurs) or not os.path.exists(fichier_matchs):
            return {}

        tableau_joueurs = pd.read_csv(fichier_joueurs)
        tableau_matchs = pd.read_csv(fichier_matchs)

        liste_matchs = tableau_matchs.to_dict("records")
        nb_tournois_gagnes = TennisMenPlayerLoader.calculer_nombre_tournois_gagnes(liste_matchs)
        resultats_competitions = TennisMenPlayerLoader.calculer_resultats_competitions(liste_matchs)

        correspondance_main = {"L": "gauche", "R": "droite", "U": "inconnue"}

        joueurs = {}

        for ligne in tableau_joueurs.to_dict("records"):
            date_naissance = None
            dob_brut = ligne.get("dob")
            if dob_brut is not None and not pd.isna(dob_brut):
                try:
                    date_str = str(int(dob_brut))
                    date_naissance = datetime.datetime.strptime(date_str, "%Y%m%d").date()
                except (ValueError, OverflowError):
                    date_naissance = None

            taille_brute = ligne.get("height")
            taille = int(taille_brute) if taille_brute is not None and not pd.isna(taille_brute) else None

            id_joueur = ligne["player_id"]

            joueurs[id_joueur] = Player(
                id=id_joueur,
                lastname=ligne.get("name_last", ""),
                firstname=ligne.get("name_first", ""),
                birthdate=date_naissance,
                country=ligne.get("ioc", ""),
                hand=correspondance_main.get(ligne.get("hand", "U"), "inconnue"),
                height=taille,
                gender="H"
            )

        for id_joueur, joueur in joueurs.items():
            stats_joueur = {}

            if id_joueur in nb_tournois_gagnes:
                stats_joueur["Tournois gagnes"] = nb_tournois_gagnes[id_joueur]
            else:
                stats_joueur["Tournois gagnes"] = 0

            if id_joueur in resultats_competitions:
                stats_joueur["Resultats en compétitions"] = resultats_competitions[id_joueur]
            else:
                stats_joueur["Resultats en compétitions"] = {}

            joueur.ajouter_statistiques(2024, stats_joueur)

        return joueurs
