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
        tournois_gagnes_par_joueur = {}  # { id_joueur: set(id_tournoi) }

        for match in liste_matchs:
            # On ne s'intéresse qu'aux finales
            if match.get("round") != "F":
                continue

            id_gagnant = match.get("winner_id")
            id_tournoi = match.get("tourney_id")

            if id_gagnant is None or id_tournoi is None:
                continue

            # On crée la liste du joueur s'il n'existe pas encore
            if id_gagnant not in tournois_gagnes_par_joueur:
                tournois_gagnes_par_joueur[id_gagnant] = set()

            tournois_gagnes_par_joueur[id_gagnant].add(id_tournoi)

        # On convertit les ensembles en nombre
        resultat = {}
        for id_joueur, set_tournois in tournois_gagnes_par_joueur.items():
            resultat[id_joueur] = len(set_tournois)

        return resultat

    @staticmethod
    def calculer_meilleur_resultat_grand_chelem(liste_matchs: list) -> dict:
        """
        Trouve le meilleur résultat de chaque joueur dans un Grand Chelem.
        On attribue un score numérique à chaque tour pour pouvoir comparer.
        Le joueur qui gagne la finale reçoit la mention "W" (Winner).
        """
        # Plus le score est élevé, plus le tour est avancé
        poids_par_tour = {
            "R128": 0, "R64": 1, "R32": 2, "R16": 3,
            "QF": 4, "SF": 5, "F": 6
        }
        # Pour retrouver le nom du tour à partir de son score
        tour_par_poids = {poids: tour for tour, poids in poids_par_tour.items()}

        # Meilleur score atteint avant de perdre, pour chaque joueur
        meilleur_score_par_perdant = {}  # { id_joueur: score_max }
        gagnants_finale = set()

        for match in liste_matchs:
            # On ignore les matchs qui ne sont pas des Grand Chelems
            if match.get("tourney_level") != "G":
                continue

            tour_actuel = match.get("round")
            id_perdant = match.get("loser_id")
            id_gagnant = match.get("winner_id")

            if tour_actuel not in poids_par_tour:
                continue

            score_actuel = poids_par_tour[tour_actuel]

            # Mise à jour du meilleur résultat du perdant
            if id_perdant is not None:
                if id_perdant not in meilleur_score_par_perdant:
                    meilleur_score_par_perdant[id_perdant] = score_actuel
                else:
                    if score_actuel > meilleur_score_par_perdant[id_perdant]:
                        meilleur_score_par_perdant[id_perdant] = score_actuel

            # Si c'est une finale, le gagnant a gagné le tournoi
            if tour_actuel == "F" and id_gagnant is not None:
                gagnants_finale.add(id_gagnant)

        # Construction du dictionnaire final
        resultat = {}
        for id_joueur, meilleur_score in meilleur_score_par_perdant.items():
            resultat[id_joueur] = tour_par_poids[meilleur_score]

        # Les vainqueurs de finale écrasent le résultat précédent avec "W"
        for id_joueur in gagnants_finale:
            resultat[id_joueur] = "W"

        return resultat

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

        # Lecture des fichiers CSV avec pandas
        tableau_joueurs = pd.read_csv(fichier_joueurs)
        tableau_matchs = pd.read_csv(fichier_matchs)

        # Conversion du tableau de matchs en liste de dictionnaires pour les boucles
        liste_matchs = tableau_matchs.to_dict("records")

        # Calcul des statistiques pour chaque joueur
        nb_tournois_gagnes = TennisMenPlayerLoader.calculer_nombre_tournois_gagnes(liste_matchs)
        meilleur_gc = TennisMenPlayerLoader.calculer_meilleur_resultat_grand_chelem(liste_matchs)

        # Correspondance entre le code CSV et un texte lisible
        correspondance_main = {"L": "gauche", "R": "droite", "U": "inconnue"}

        joueurs = {}

        for ligne in tableau_joueurs.to_dict("records"):
            # Gestion de la date de naissance (stockée comme float ex: 19860603.0)
            date_naissance = None
            dob_brut = ligne.get("dob")
            if dob_brut is not None and not pd.isna(dob_brut):
                try:
                    # On convertit d'abord en entier pour supprimer le ".0"
                    date_str = str(int(dob_brut))
                    date_naissance = datetime.datetime.strptime(date_str, "%Y%m%d").date()
                except (ValueError, OverflowError):
                    date_naissance = None

            # Gestion de la taille (peut être vide dans le CSV)
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

        # Ajout des statistiques calculées à chaque joueur
        for id_joueur, joueur in joueurs.items():
            stats_joueur = {}

            if id_joueur in nb_tournois_gagnes:
                stats_joueur["Tournois gagnes"] = nb_tournois_gagnes[id_joueur]
            else:
                stats_joueur["Tournois gagnes"] = 0

            if id_joueur in meilleur_gc:
                stats_joueur["Meilleur resultat en Grand Chelem"] = meilleur_gc[id_joueur]
            else:
                stats_joueur["Meilleur resultat en Grand Chelem"] = "Aucun"

            joueur.ajouter_statistiques(2024, stats_joueur)

        return joueurs
