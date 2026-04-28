import os
import datetime
import numpy as np
import pandas as pd
from src.Model.Player import Player

class TennisWomenPlayerLoader:

    @staticmethod
    def calculer_nombre_tournois_gagnes(dataframe_matchsatch: pd.DataFrame) -> pd.Series:
        # On récupère tous les ID uniques possibles (gagnantes et perdantes)
        players = pd.concat([dataframe_matchsatch["winner_id"], dataframe_matchsatch["loser_id"]]).unique()
        
        # On crée une Series remplie de 0 pour tout le monde
        res = pd.Series(data=0, index=players, name="n_tournaments_won")
        
        # On filtre les matchs qui sont des finales (round == "F")
        # On compte ensuite le nombre de tournois distincts ("tourney_id") gagnés par chaque gagnante
        winners = (
            dataframe_matchsatch.loc[dataframe_matchsatch["round"] == "F", ["winner_id", "tourney_id"]]
            .groupby("winner_id")["tourney_id"]
            .nunique()
        )
        
        # On met à jour la Series avec le vrai compte
        res.loc[winners.index] = winners
        return res

    @staticmethod
    def calculer_taux_victoires(dataframe_matchsatch: pd.DataFrame) -> pd.Series:
        players = pd.concat([dataframe_matchsatch["winner_id"], dataframe_matchsatch["loser_id"]]).unique()
        
        wins = pd.Series(data=0, index=players)
        losses = pd.Series(data=0, index=players)
        
        # count() automatique sur les apparitions dans la colonne winner_id et loser_id
        wins_actual = dataframe_matchsatch["winner_id"].value_counts()
        losses_actual = dataframe_matchsatch["loser_id"].value_counts()
        
        # Mise à jour
        wins.loc[wins_actual.index] = wins_actual
        losses.loc[losses_actual.index] = losses_actual
        
        # Calcul du ratio
        res = wins / (wins + losses)
        res.name = "winning_ratio"
        return res

    @staticmethod
    def calculer_meilleur_resultat_grand_chelem(dataframe_matchsatch: pd.DataFrame) -> pd.Series:
        players = pd.concat([dataframe_matchsatch["winner_id"], dataframe_matchsatch["loser_id"]]).unique()
        res = pd.Series(data=None, index=players, dtype=str, name="best_grand_chelem_result")
        
        # On filtre les Grand Chelems (tourney_level == "G")
        dataframe_matchsatch_g = dataframe_matchsatch[dataframe_matchsatch["tourney_level"] == "G"].copy()
        
        # Mapping pour donner un poids numérique à chaque tour
        mapping_round_int = {
            "R128": 0, "R64": 1, "R32": 2, "R16": 3,
            "QF": 4, "SF": 5, "F": 6
        }
        mapping_int_round = {v: k for k, v in mapping_round_int.items()}
        
        # On applique le mapping
        dataframe_matchsatch_g["round_int"] = dataframe_matchsatch_g["round"].map(mapping_round_int)
        
        # On cherche l'étape maximale atteinte avant de perdre
        best_results = (
            dataframe_matchsatch_g.groupby("loser_id")["round_int"].max()
            .map(mapping_int_round)
        )
        
        # Les joueuses qui ont gagné une finale ("W")
        winners = dataframe_matchsatch_g.loc[dataframe_matchsatch_g["round"] == "F", "winner_id"].to_numpy()
        
        res.loc[best_results.index] = best_results
        res.loc[winners] = "W"
        return res

    @staticmethod
    def load_all_player(dossier: str) -> dict:
        players_file = os.path.join(dossier, "wta_players_2024.csv")
        matches_file = os.path.join(dossier, "wta_matches_2024.csv")
        
        if not os.path.exists(players_file) or not os.path.exists(matches_file):
            return {}
            
        dataframe_joueurslayer = pd.read_csv(players_file)
        dataframe_matchsatch = pd.read_csv(matches_file)
        
        # 1. Calcul des statistiques en Pandas
        df_statistics = pd.concat([
            TennisWomenPlayerLoader.calculer_nombre_tournois_gagnes(dataframe_matchsatch),
            TennisWomenPlayerLoader.calculer_taux_victoires(dataframe_matchsatch),
            TennisWomenPlayerLoader.calculer_meilleur_resultat_grand_chelem(dataframe_matchsatch),
        ], axis=1)
        
        mapping_hand = {"L": "gauche", "R": "droite", "U": "inconnue"}
        res = {}
        
        # 2. Création itérative des objets
        for record in dataframe_joueurslayer.to_dict("records"):
            # Gestion de la date de naissance (float dans le CSV original, géré avec np.isnan)
            if not np.isnan(record["dob"]):
                # .0f pour retirer le .0 décimal
                birthdate = datetime.datetime.strptime(f"{record['dob']:.0f}", "%Y%m%d")
                birthdate = datetime.date(birthdate.year, birthdate.month, birthdate.day)
            else:
                birthdate = None

            # Gestion de la taille
            height = int(record["height"]) if not np.isnan(record["height"]) else None

            res[record["player_id"]] = Player(
                id=record["player_id"],
                lastname=record["name_last"],
                firstname=record["name_first"],
                birthdate=birthdate,
                country=record["ioc"],
                hand=mapping_hand.get(record.get("hand", "U"), "inconnue"),
                height=height,
            )
            
        # 3. Injection des statistiques
        dict_statistics = df_statistics.to_dict("index")
        for key, value in dict_statistics.items():
            if key in res:
                res[key].ajouter_statistiques(2024, value)

        return res
