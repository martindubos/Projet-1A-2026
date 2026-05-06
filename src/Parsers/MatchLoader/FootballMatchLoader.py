import os
import pandas as pd
from src.Model.Match import MatchFootball


class FootballMatchLoader():
    @staticmethod
    def load_all_match(dossier: str) -> list:
        """
        Charge tous les matchs de football depuis le fichier CSV du dossier.
        Pour chaque match, on récupère aussi la liste des joueurs qui ont joué
        dans chaque équipe (colonnes home_player_1 à home_player_11).
        """
        fichier_matchs = os.path.join(dossier, "match.csv")
        if not os.path.exists(fichier_matchs):
            return []

        tableau_matchs = pd.read_csv(fichier_matchs)

        matchs = []
        for ligne in tableau_matchs.to_dict("records"):

            # Récupération des IDs des joueurs à domicile (home_player_1 à home_player_11)
            joueurs_domicile = []
            for numero in range(1, 12):
                id_joueur = ligne.get(f"home_player_{numero}")
                if id_joueur is not None and pd.notna(id_joueur):
                    joueurs_domicile.append(int(id_joueur))

            # Récupération des IDs des joueurs à l'extérieur (away_player_1 à away_player_11)
            joueurs_exterieur = []
            for numero in range(1, 12):
                id_joueur = ligne.get(f"away_player_{numero}")
                if id_joueur is not None and pd.notna(id_joueur):
                    joueurs_exterieur.append(int(id_joueur))

            # Récupération des buts (on met 0 si la valeur est absente)
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
