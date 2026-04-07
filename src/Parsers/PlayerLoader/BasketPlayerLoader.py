import os
import datetime
import pandas as pd
from src.Model.Player import Player

class BasketPlayerLoader():
    @staticmethod
    def load_all_player(dossier: str) -> dict:
        player_file = os.path.join(dossier, "basketball_player.csv")
        if not os.path.exists(player_file):
            return {}
            
        df_p = pd.read_csv(player_file)
        
        res = {}
        for r in df_p.to_dict("records"):
            birthdate = None
            if pd.notna(r.get("birthdate")):
                try:
                    d_str = str(r["birthdate"]).split(" ")[0]
                    d = datetime.datetime.strptime(d_str, "%Y-%m-%d")
                    birthdate = d.date()
                except ValueError:
                    pass
                    
            height_cm = None
            h_str = str(r.get("height"))
            if "-" in h_str:
                parts = h_str.split("-")
                if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
                    height_cm = int(round(int(parts[0]) * 30.48 + int(parts[1]) * 2.54))

            player_id = r.get("person_id")
            res[player_id] = Player(
                id=player_id,
                lastname=r.get("last_name", "") if pd.notna(r.get("last_name")) else "",
                firstname=r.get("first_name", "") if pd.notna(r.get("first_name")) else "",
                birthdate=birthdate,
                country="",
                height=height_cm
            )
        return res