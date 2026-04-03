import os
import datetime
import pandas as pd
from src.Model.Player import Player

class FootballPlayerLoader():
    @staticmethod
    def load_all_player(dossier: str) -> dict:
        player_file = os.path.join(dossier, "player.csv")
        if not os.path.exists(player_file):
            return {}
            
        df_p = pd.read_csv(player_file)
        
        res = {}
        for r in df_p.to_dict("records"):
            # Date de naissance format ex: 1992-02-28 00:00:00
            birthdate = None
            if pd.notna(r.get("birthday")):
                try:
                    d_str = str(r["birthday"]).split(" ")[0]
                    d = datetime.datetime.strptime(d_str, "%Y-%m-%d")
                    birthdate = d.date()
                except ValueError:
                    pass
                    
            player_id = r.get("player_api_id")
            res[player_id] = Player(
                id=player_id,
                lastname=r.get("player_name", ""),
                firstname="", # Le CSV fournit souvent un seul nom complet sous player_name
                birthdate=birthdate,
                country="", # Le JSON/CSV ne contient pas tjs le pays directement
                height=int(r["height"]) if pd.notna(r.get("height")) else None
            )
        return res