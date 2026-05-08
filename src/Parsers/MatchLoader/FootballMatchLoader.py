import os
import pandas as pd
from src.Model.Match import MatchFootball


class FootballMatchLoader():
    @staticmethod
    def load_all_match(dossier: str) -> list:
        """
        Charge tous les matchs de football depuis le fichier CSV du dossier.

        Le fichier attendu est 'match.csv'. Pour chaque match, on récupère :
        - les IDs des équipes domicile/extérieur
        - les buts de chaque équipe
        - la saison (ex: '2015/2016')
        - la ligue (league_id)
        - les compositions : joueurs home_player_1 à home_player_11
          et away_player_1 à away_player_11

        Args:
            dossier (str): Chemin vers le dossier contenant match.csv.

        Returns:
            list: Liste d'objets MatchFootball.
                  Retourne [] si le fichier est introuvable.
        """
        fichier_matchs = os.path.join(dossier, "match.csv")
        if not os.path.exists(fichier_matchs):
            return []

        tableau_matchs = pd.read_csv(fichier_matchs)

        matchs = []
        for ligne in tableau_matchs.to_dict("records"):

            joueurs_domicile = []
            for numero in range(1, 12):
                id_joueur = ligne.get(f"home_player_{numero}")
                if id_joueur is not None and pd.notna(id_joueur):
                    joueurs_domicile.append(int(id_joueur))

            joueurs_exterieur = []
            for numero in range(1, 12):
                id_joueur = ligne.get(f"away_player_{numero}")
                if id_joueur is not None and pd.notna(id_joueur):
                    joueurs_exterieur.append(int(id_joueur))

            buts_domicile = ligne.get("home_team_goal")
            buts_exterieur = ligne.get("away_team_goal")
            buts_domicile = int(buts_domicile) if buts_domicile is not None and pd.notna(buts_domicile) else 0
            buts_exterieur = int(buts_exterieur) if buts_exterieur is not None and pd.notna(buts_exterieur) else 0

            matchs.append(MatchFootball(
                id=ligne.get("id"),
                equipe1_id=ligne.get("home_team_api_id"),
                equipe2_id=ligne.get("away_team_api_id"),
                score1=buts_domicile,
                score2=buts_exterieur,
                league_id=ligne.get("league_id"),
                saison=ligne.get("season"),
                joueurs_dom=joueurs_domicile,
                joueurs_ext=joueurs_exterieur
            ))

        return matchs
