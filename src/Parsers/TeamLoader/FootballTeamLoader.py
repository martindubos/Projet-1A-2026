import os
import pandas as pd
from src.Model.Team import Team

class FootballTeamLoader():
    @staticmethod
    def load_all_team(dossier: str) -> dict:
        team_file = os.path.join(dossier, "team.csv")
        if not os.path.exists(team_file):
            return {}
            
        df_t = pd.read_csv(team_file)
        
        res = {}
        for r in df_t.to_dict("records"):
            team_id = r.get("team_api_id")
            res[team_id] = Team(
                id=team_id,
                nom=r.get("team_long_name", ""),
                nom_court=r.get("team_short_name", "")
            )
        return res
