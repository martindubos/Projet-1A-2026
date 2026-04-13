import os
import pandas as pd
from src.Model.Match import MatchFootball

class FootballMatchLoader():
    @staticmethod
    def load_all_match(dossier: str) -> list:
        match_file = os.path.join(dossier, "match.csv")
        if not os.path.exists(match_file):
            return []
            
        dataframe_matchs = pd.read_csv(match_file)
        
        def joueurs(d, prefix):
            return [int(d[f"{prefix}{i}"])
                    for i in range(1, 12)
                    if pd.notna(d.get(f"{prefix}{i}"))]
        
        matchs = []
        for r in dataframe_matchs.to_dict("records"):
            matchs.append(MatchFootball(
                id=r.get("id"),
                equipe1_id=r.get("home_team_api_id"),
                equipe2_id=r.get("away_team_api_id"),
                score1=int(r["home_team_goal"]) if pd.notna(r.get("home_team_goal")) else 0,
                score2=int(r["away_team_goal"]) if pd.notna(r.get("away_team_goal")) else 0,
                league_id=r.get("league_id"),
                saison=r.get("season"),
                joueurs_dom=joueurs(r, "home_player_"),
                joueurs_ext=joueurs(r, "away_player_")
            ))
        return matchs
