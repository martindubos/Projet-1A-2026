import os
import datetime
import pandas as pd
from src.Model.Player import Player


class TennisWomenPlayerLoader:

    @staticmethod
    def calculer_nombre_tournois_gagnes(liste_matchs: list) -> dict:
        """
        Compte le nombre de tournois gagnés par chaque joueuse.
        Une joueuse gagne un tournoi si elle remporte la finale (round == "F").
        On utilise un ensemble (set) pour ne compter qu'une fois chaque tournoi.
        """
        tournois_gagnes_par_joueuse = {}  # { id_joueuse: set(id_tournoi) }

        for match in liste_matchs:
            if match.get("round") != "F":
                continue

            id_gagnante = match.get("winner_id")
            id_tournoi = match.get("tourney_id")

            if id_gagnante is None or id_tournoi is None:
                continue

            if id_gagnante not in tournois_gagnes_par_joueuse:
                tournois_gagnes_par_joueuse[id_gagnante] = set()

            tournois_gagnes_par_joueuse[id_gagnante].add(id_tournoi)

        # Conversion en nombre de tournois
        resultat = {}
        for id_joueuse, set_tournois in tournois_gagnes_par_joueuse.items():
            resultat[id_joueuse] = len(set_tournois)

        return resultat

    @staticmethod
    def calculer_meilleur_resultat_grand_chelem(liste_matchs: list) -> dict:
        """
        Trouve le meilleur résultat de chaque joueuse dans un Grand Chelem.
        Le tour est converti en score numérique pour comparer facilement.
        La joueuse qui remporte la finale reçoit la mention "W" (Winner).
        """
        poids_par_tour = {
            "R128": 0, "R64": 1, "R32": 2, "R16": 3,
            "QF": 4, "SF": 5, "F": 6
        }
        tour_par_poids = {poids: tour for tour, poids in poids_par_tour.items()}

        meilleur_score_par_perdante = {}
        gagnantes_finale = set()

        for match in liste_matchs:
            if match.get("tourney_level") != "G":
                continue

            tour_actuel = match.get("round")
            id_perdante = match.get("loser_id")
            id_gagnante = match.get("winner_id")

            if tour_actuel not in poids_par_tour:
                continue

            score_actuel = poids_par_tour[tour_actuel]

            if id_perdante is not None:
                if id_perdante not in meilleur_score_par_perdante:
                    meilleur_score_par_perdante[id_perdante] = score_actuel
                else:
                    if score_actuel > meilleur_score_par_perdante[id_perdante]:
                        meilleur_score_par_perdante[id_perdante] = score_actuel

            if tour_actuel == "F" and id_gagnante is not None:
                gagnantes_finale.add(id_gagnante)

        resultat = {}
        for id_joueuse, meilleur_score in meilleur_score_par_perdante.items():
            resultat[id_joueuse] = tour_par_poids[meilleur_score]

        for id_joueuse in gagnantes_finale:
            resultat[id_joueuse] = "W"

        return resultat

    @staticmethod
    def load_all_player(dossier: str) -> dict:
        """
        Charge toutes les joueuses WTA depuis les fichiers CSV du dossier donné.
        Retourne un dictionnaire { id_joueuse: Player }.
        """
        fichier_joueuses = os.path.join(dossier, "wta_players_2024.csv")
        fichier_matchs = os.path.join(dossier, "wta_matches_2024.csv")

        if not os.path.exists(fichier_joueuses) or not os.path.exists(fichier_matchs):
            return {}

        tableau_joueuses = pd.read_csv(fichier_joueuses)
        tableau_matchs = pd.read_csv(fichier_matchs)

        liste_matchs = tableau_matchs.to_dict("records")

        # Calcul des statistiques
        nb_tournois_gagnes = TennisWomenPlayerLoader.calculer_nombre_tournois_gagnes(liste_matchs)
        meilleur_gc = TennisWomenPlayerLoader.calculer_meilleur_resultat_grand_chelem(liste_matchs)

        correspondance_main = {"L": "gauche", "R": "droite", "U": "inconnue"}

        joueuses = {}

        for ligne in tableau_joueuses.to_dict("records"):
            # Date de naissance (stockée comme float ex: 19950812.0)
            date_naissance = None
            dob_brut = ligne.get("dob")
            if dob_brut is not None and not pd.isna(dob_brut):
                try:
                    date_str = str(int(dob_brut))
                    date_naissance = datetime.datetime.strptime(date_str, "%Y%m%d").date()
                except (ValueError, OverflowError):
                    date_naissance = None

            # Taille (peut être absente)
            taille_brute = ligne.get("height")
            taille = int(taille_brute) if taille_brute is not None and not pd.isna(taille_brute) else None

            id_joueuse = ligne["player_id"]

            joueuses[id_joueuse] = Player(
                id=id_joueuse,
                lastname=ligne.get("name_last", ""),
                firstname=ligne.get("name_first", ""),
                birthdate=date_naissance,
                country=ligne.get("ioc", ""),
                hand=correspondance_main.get(ligne.get("hand", "U"), "inconnue"),
                height=taille,
                gender="F"
            )

        # Ajout des statistiques calculées
        for id_joueuse, joueuse in joueuses.items():
            stats_joueuse = {}

            if id_joueuse in nb_tournois_gagnes:
                stats_joueuse["Tournois gagnes"] = nb_tournois_gagnes[id_joueuse]
            else:
                stats_joueuse["Tournois gagnes"] = 0

            if id_joueuse in meilleur_gc:
                stats_joueuse["Meilleur resultat en Grand Chelem"] = meilleur_gc[id_joueuse]
            else:
                stats_joueuse["Meilleur resultat en Grand Chelem"] = "Aucun"

            joueuse.ajouter_statistiques(2024, stats_joueuse)

        return joueuses
