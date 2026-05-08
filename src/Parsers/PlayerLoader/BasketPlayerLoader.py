import os
import datetime
import pandas as pd
from src.Model.Player import Player


class BasketPlayerLoader():
    @staticmethod
    def load_all_player(dossier: str) -> dict:
        """
        Charge tous les joueurs de basketball depuis le fichier CSV du dossier.
        La taille est convertie du format américain pieds-pouces (ex: "6-5") en centimètres.
        """
        fichier_joueurs = os.path.join(dossier, "basketball_player.csv")
        if not os.path.exists(fichier_joueurs):
            return {}

        tableau_joueurs = pd.read_csv(fichier_joueurs)

        joueurs = {}
        for ligne in tableau_joueurs.to_dict("records"):

            date_naissance = None
            date_brute = ligne.get("birthdate")
            if date_brute is not None and pd.notna(date_brute):
                try:
                    date_str = str(date_brute).split(" ")[0]
                    date_naissance = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
                except ValueError:
                    date_naissance = None

            taille_cm = None
            taille_brute = str(ligne.get("height", ""))
            if "-" in taille_brute:
                parties = taille_brute.split("-")
                if len(parties) == 2 and parties[0].isdigit() and parties[1].isdigit():
                    pieds = int(parties[0])
                    pouces = int(parties[1])
                    taille_cm = int(round(pieds * 30.48 + pouces * 2.54))

            id_joueur = ligne.get("person_id")
            joueurs[id_joueur] = Player(
                id=id_joueur,
                lastname=ligne.get("last_name", "") if pd.notna(ligne.get("last_name")) else "",
                firstname=ligne.get("first_name", "") if pd.notna(ligne.get("first_name")) else "",
                birthdate=date_naissance,
                country="USA",
                height=taille_cm,
                weight=ligne.get("weight"),
                position=ligne.get("position")
            )

        return joueurs