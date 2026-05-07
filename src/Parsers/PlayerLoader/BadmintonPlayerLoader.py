import os
import pandas as pd
from src.Model.Player import Player


class BadmintonPlayerLoader():
    @staticmethod
    def load_all_player(dossier: str) -> dict:
        """
        Charge tous les joueurs de badminton depuis le fichier CSV du dossier.

        Le fichier attendu est 'player.csv'. Chaque ligne contient :
        - name      : nom complet du joueur (utilisé comme identifiant unique)
        - country   : pays d'origine du joueur
        - continent : continent du joueur

        En badminton, le nom du joueur sert directement d'identifiant (id),
        car les matchs référencent les joueurs par leur nom.

        Args:
            dossier (str): Chemin vers le dossier contenant player.csv.

        Returns:
            dict: Dictionnaire {nom_joueur: Player}.
                  Retourne {} si le fichier est introuvable.
        """
        fichier_joueurs = os.path.join(dossier, "player.csv")
        if not os.path.exists(fichier_joueurs):
            return {}

        tableau_joueurs = pd.read_csv(fichier_joueurs)

        joueurs = {}
        for ligne in tableau_joueurs.to_dict("records"):
            nom = ligne.get("name", "")
            if not nom or (isinstance(nom, float)):
                continue

            pays = ligne.get("country", "")
            if pays is None or (isinstance(pays, float)):
                pays = ""

            # Le nom complet est stocké dans lastname, firstname laissé vide
            # pour que nom_complet() retourne le nom tel quel
            joueurs[nom] = Player(
                id=nom,
                lastname=nom,
                firstname="",
                birthdate=None,
                country=pays,
                height=None
            )

        return joueurs
