import os
import datetime
import pandas as pd
from src.Model.Player import Player


class FootballPlayerLoader():
    @staticmethod
    def load_all_player(dossier: str) -> dict:
        """
        Charge tous les joueurs de football depuis le fichier CSV du dossier.

        Le fichier attendu est 'player.csv'. Chaque ligne contient :
        - player_api_id : identifiant unique du joueur
        - player_name   : nom complet du joueur (ex: "Lionel Messi")
        - birthday      : date de naissance au format 'YYYY-MM-DD'
        - height (cm)   : taille en centimètres

        Args:
            dossier (str): Chemin vers le dossier contenant player.csv.

        Returns:
            dict: Dictionnaire {player_api_id: Player}.
                  Retourne {} si le fichier est introuvable.
        """
        fichier_joueurs = os.path.join(dossier, "player.csv")
        if not os.path.exists(fichier_joueurs):
            return {}

        tableau_joueurs = pd.read_csv(fichier_joueurs)

        joueurs = {}
        for ligne in tableau_joueurs.to_dict("records"):

            # La date de naissance est au format "1987-06-24" (parfois "1987-06-24 00:00:00")
            date_naissance = None
            date_brute = ligne.get("birthday")
            if date_brute is not None and pd.notna(date_brute):
                try:
                    date_str = str(date_brute).split(" ")[0]
                    date_naissance = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
                except ValueError:
                    date_naissance = None

            # La colonne de taille s'appelle "height (cm)" dans le CSV football
            taille_brute = ligne.get("height (cm)")
            if taille_brute is not None and pd.notna(taille_brute):
                try:
                    taille = int(float(taille_brute))
                except (ValueError, TypeError):
                    taille = None
            else:
                taille = None

            id_joueur = ligne.get("player_api_id")
            joueurs[id_joueur] = Player(
                id=id_joueur,
                # Le CSV fournit un nom complet dans player_name (pas de prénom séparé)
                lastname=ligne.get("player_name", ""),
                firstname="",
                birthdate=date_naissance,
                country="",
                height=taille
            )

        return joueurs