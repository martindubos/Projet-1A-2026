import csv


import numpy as np
import pandas as pd

class TennisWomenPlayerLoader():
    def creer_objets_joueuses() -> dict[int, Player]:
        path = os.path.join("data","tennis")
        df_player = pd.read_csv(os.path.join(path, "wta_players_2024.csv"))
        df_match = pd.read_csv(os.path.join(path, "wta_matches_2024.csv"))
        
        df_statistics = pd.concat([
            calculer_nombre_tournois_gagnes(),
            calculer_taux_victoires(),
            calculer_meilleur_resultat_grand_chelem(),
        ], axis=1)
        
        mapping_hand = {"L": "gauche", "R": "droite", "U": "inconnue"}
        
        res = {}
        for record in df_player.to_dict("records"):
            
            # Date de naissance
            if not np.isnan(record["dob"]):
                birthdate = datetime.datetime.strptime(f"{record["dob"]:.0f}", "%Y%m%d")
                birthdate = datetime.date(birthdate.year, birthdate.month, birthdate.day)
            else:
                birthdate = None
            
            # Taille
            height = int(record["height"]) if not np.isnan(record["height"]) else None

            res[record["player_id"]] = Player(
                lastname=record["name_first"],
                firstname=record["name_last"],
                birthdate=birthdate,
                country=record["ioc"],
                hand=mapping_hand[record["hand"]],
                height=height,
            )
            
            res[record["player_id"]]

        dict_statistics = df_statistics.to_dict("index")
        for key, value in dict_statistics.items():
            res[key].ajouter_statistiques(2024, value)

        return res
