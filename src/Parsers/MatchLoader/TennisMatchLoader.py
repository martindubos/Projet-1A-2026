import os
import pandas as pd
from src.Model.Match import MatchTennis

class TennisMatchLoader():
    @staticmethod
    def load_all_match(dossier: str) -> list:
        matchs = []
        for prefix in ['wta', 'atp']:
            matches_file = os.path.join(dossier, f"{prefix}_matches_2024.csv")
            if not os.path.exists(matches_file):
                continue
                
            df_m = pd.read_csv(matches_file)
            for r in df_m.to_dict("records"):
                matchs.append(MatchTennis(
                    id=r.get("match_num"),
                    equipe1_id=r.get("winner_id"),
                    equipe2_id=r.get("loser_id"),
                    score1=1, score2=0,
                    surface=r.get("surface"),
                    round=r.get("round"),
                    tournoi=r.get("tourney_name"),
                    circuit=prefix.upper()
                ))
        return matchs
