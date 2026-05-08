import os
import datetime
import pandas as pd
from src.Model.Player import Player


class FootballPlayerLoader():
    @staticmethod
    def load_all_player(dossier: str) -> dict:
        fichier_joueurs = os.path.join(dossier, "player.csv")
        if not os.path.exists(fichier_joueurs):
            return {}

        tableau_joueurs = pd.read_csv(fichier_joueurs)

        joueurs = {}
        for ligne in tableau_joueurs.to_dict("records"):

            date_naissance = None
            date_brute = ligne.get("birthday")
            if date_brute is not None and pd.notna(date_brute):
                try:
                    date_str = str(date_brute).split(" ")[0]
                    date_naissance = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
                except ValueError:
                    date_naissance = None

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
                lastname=ligne.get("player_name", ""),
                firstname="",
                birthdate=date_naissance,
                country="",
                height=taille
            )

        return joueurs