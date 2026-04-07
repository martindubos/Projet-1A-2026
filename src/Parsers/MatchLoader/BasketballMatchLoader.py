import os
import pandas as pd
from src.Model.Match import MatchBasketball

class BasketballMatchLoader():
    @staticmethod
    def load_all_match(dossier: str) -> list:
        matchs = []
        matches_file = os.path.join(dossier, "basketball_game.csv")
        if not os.path.exists(matches_file):
            return matchs
            
        df_m = pd.read_csv(matches_file)
        for r in df_m.to_dict("records"):
            matchs.append(MatchBasketball(
                id=r.get("game_id"),
                equipe1_id=r.get("team_id_home"),
                equipe2_id=r.get("team_id_away"),
                score1=r.get("pts_home"),
                score2=r.get("pts_away"),
                date=r.get("game_date"),
                saison=r.get("season"),
                season_type=r.get("season_type")
            ))
        return matchs
