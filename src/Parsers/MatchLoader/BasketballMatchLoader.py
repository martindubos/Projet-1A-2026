import os
import pandas as pd
from src.Model.Match import MatchBasketball


class BasketballMatchLoader():
    @staticmethod
    def load_all_match(dossier: str) -> list:
        """
        Charge tous les matchs de basketball depuis le fichier CSV du dossier.

        Le fichier attendu est 'basketball_game.csv'. Chaque ligne contient :
        - game_id       : identifiant unique du match
        - team_id_home  : ID de l'équipe domicile
        - team_id_away  : ID de l'équipe extérieure
        - pts_home      : points de l'équipe domicile
        - pts_away      : points de l'équipe extérieure
        - game_date     : date du match
        - season        : saison (ex: 2022)
        - season_type   : type de saison ('Regular Season', 'Playoffs')

        Args:
            dossier (str): Chemin vers le dossier contenant basketball_game.csv.

        Returns:
            list: Liste d'objets MatchBasketball.
                  Retourne [] si le fichier est introuvable.
        """
        fichier_matchs = os.path.join(dossier, "basketball_game.csv")
        if not os.path.exists(fichier_matchs):
            return []

        tableau_matchs = pd.read_csv(fichier_matchs)

        matchs = []
        for ligne in tableau_matchs.to_dict("records"):
            matchs.append(MatchBasketball(
                id=ligne.get("game_id"),
                equipe1_id=ligne.get("team_id_home"),
                equipe2_id=ligne.get("team_id_away"),
                score1=ligne.get("pts_home"),
                score2=ligne.get("pts_away"),
                date=ligne.get("game_date"),
                saison=ligne.get("season"),
                season_type=ligne.get("season_type")
            ))

        return matchs
