import os
import datetime
import pandas as pd
from src.Model.Player import Player


class VolleyMenPlayerLoader():
    @staticmethod
    def load_all_player(dossier: str) -> dict:
        """
        Charge tous les joueurs masculins de volleyball depuis le fichier CSV.

        Le fichier attendu est 'volleyball_player_men.csv'. Chaque ligne contient :
        - name         : nom complet du joueur (MAJUSCULES Prénom)
        - country_code : code pays à 3 lettres (ex: 'FRA', 'USA')
        - height       : taille en centimètres
        - birth_date   : date de naissance au format 'YYYY-MM-DD'

        Le nom sert d'identifiant unique. Le genre est fixé à 'H' (homme).

        Args:
            dossier (str): Chemin vers le dossier contenant volleyball_player_men.csv.

        Returns:
            dict: Dictionnaire {nom_joueur: Player}.
                  Retourne {} si le fichier est introuvable.
        """
        fichier_joueurs = os.path.join(dossier, "volleyball_player_men.csv")
        if not os.path.exists(fichier_joueurs):
            return {}

        tableau_joueurs = pd.read_csv(fichier_joueurs)

        joueurs = {}
        for ligne in tableau_joueurs.to_dict("records"):
            nom = ligne.get("name", "")
            if not nom or (isinstance(nom, float)):
                continue

            date_naissance = None
            date_brute = ligne.get("birth_date")
            if date_brute is not None and not isinstance(date_brute, float):
                try:
                    date_naissance = datetime.datetime.strptime(
                        str(date_brute).strip(), "%Y-%m-%d"
                    ).date()
                except ValueError:
                    date_naissance = None

            taille_brute = ligne.get("height")
            if taille_brute is not None and not isinstance(taille_brute, float):
                try:
                    taille = int(taille_brute)
                except (ValueError, TypeError):
                    taille = None
            elif taille_brute is not None and pd.notna(taille_brute):
                try:
                    taille = int(taille_brute)
                except (ValueError, TypeError):
                    taille = None
            else:
                taille = None

            pays = ligne.get("country_code", "")
            if pays is None or isinstance(pays, float):
                pays = ""

            joueurs[nom] = Player(
                id=nom,
                lastname=nom,
                firstname="",
                birthdate=date_naissance,
                country=str(pays),
                height=taille,
                gender="H"
            )

        return joueurs