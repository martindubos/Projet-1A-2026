import os
import datetime
import numpy as np
import pandas as pd
from src.Model.Player import Player

class TennisMenPlayerLoader:

    @staticmethod
    def calculer_nombre_tournois_gagnes(dataframe_matchsatch: pd.DataFrame) -> pd.Series:
        # ETAPE 1 : On recupere la liste de tous les joueurs uniques
        players = pd.concat([dataframe_matchsatch["winner_id"], dataframe_matchsatch["loser_id"]]).unique()
        res = pd.Series(data=0, index=players, name="n_tournaments_won")
        
        # ETAPE 2 : On filtre les matchs pour ne garder que les Finales (round == "F")
        finales = dataframe_matchsatch[dataframe_matchsatch["round"] == "F"]
        
        # ETAPE 3 : On regroupe par vainqueur (groupby) et on compte le nombre de tournois uniques (nunique)
        winners = finales.groupby("winner_id")["tourney_id"].nunique()
        
        # ETAPE 4 : On met a jour notre serie de resultats
        res.loc[winners.index] = winners
        return res

    @staticmethod
    def calculer_taux_victoires(dataframe_matchsatch: pd.DataFrame) -> pd.Series:
        players = pd.concat([dataframe_matchsatch["winner_id"], dataframe_matchsatch["loser_id"]]).unique()
        wins = pd.Series(data=0, index=players)
        losses = pd.Series(data=0, index=players)
        
        wins_actual = dataframe_matchsatch["winner_id"].value_counts()
        losses_actual = dataframe_matchsatch["loser_id"].value_counts()
        
        wins.loc[wins_actual.index] = wins_actual
        losses.loc[losses_actual.index] = losses_actual
        
        res = wins / (wins + losses)
        res.name = "winning_ratio"
        return res

    @staticmethod
    def calculer_meilleur_resultat_grand_chelem(dataframe_matchsatch: pd.DataFrame) -> pd.Series:
        players = pd.concat([dataframe_matchsatch["winner_id"], dataframe_matchsatch["loser_id"]]).unique()
        res = pd.Series(data=None, index=players, dtype=str, name="best_grand_chelem_result")
        
        dataframe_matchsatch_g = dataframe_matchsatch[dataframe_matchsatch["tourney_level"] == "G"].copy()
        
        mapping_round_int = {
            "R128": 0, "R64": 1, "R32": 2, "R16": 3,
            "QF": 4, "SF": 5, "F": 6
        }
        mapping_int_round = {v: k for k, v in mapping_round_int.items()}
        
        dataframe_matchsatch_g["round_int"] = dataframe_matchsatch_g["round"].map(mapping_round_int)
        
        best_results = (
            dataframe_matchsatch_g.groupby("loser_id")["round_int"].max()
            .map(mapping_int_round)
        )
        
        winners = dataframe_matchsatch_g.loc[dataframe_matchsatch_g["round"] == "F", "winner_id"].to_numpy()
        
        res.loc[best_results.index] = best_results
        res.loc[winners] = "W"
        return res

    @staticmethod
    def load_all_player(dossier: str) -> dict:
        players_file = os.path.join(dossier, "atp_players_2024.csv")
        matches_file = os.path.join(dossier, "atp_matches_2024.csv")
        
        if not os.path.exists(players_file) or not os.path.exists(matches_file):
            return {}
            
        dataframe_joueurslayer = pd.read_csv(players_file)
        dataframe_matchsatch = pd.read_csv(matches_file)
        
        df_statistics = pd.concat([
            TennisMenPlayerLoader.calculer_nombre_tournois_gagnes(dataframe_matchsatch).rename("nombre de tournois gagnés"),
        ], axis=1)
        
        mapping_hand = {"L": "gauche", "R": "droite", "U": "inconnue"}
        res = {}
        
        for record in dataframe_joueurslayer.to_dict("records"):
            if not np.isnan(record["dob"]):
                birthdate = datetime.datetime.strptime(f"{record['dob']:.0f}", "%Y%m%d")
                birthdate = datetime.date(birthdate.year, birthdate.month, birthdate.day)
            else:
                birthdate = None

            height = int(record["height"]) if not np.isnan(record["height"]) else None

            res[record["player_id"]] = Player(
                id=record["player_id"],
                lastname=record["name_last"],
                firstname=record["name_first"],
                birthdate=birthdate,
                country=record["ioc"],
                hand=mapping_hand.get(record.get("hand", "U"), "inconnue"),
                height=height,
                gender="H"
            )
            
        dict_statistics = df_statistics.to_dict("index")
        for key, value in dict_statistics.items():
            if key in res:
                res[key].ajouter_statistiques(2024, value)

        return res
