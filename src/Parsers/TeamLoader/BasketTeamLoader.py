import os
import pandas as pd
from src.Model.Team import Team

class BasketTeamLoader():
    @staticmethod
    def load_all_team(dossier: str) -> dict:
        team_file = os.path.join(dossier, "basketball_team.csv")
        if not os.path.exists(team_file):
            return {}
            
        dataframe_equipes = pd.read_csv(team_file)
        
        res = {}
        for r in dataframe_equipes.to_dict("records"):
            team_id = r.get("id")
            res[team_id] = Team(
                id=team_id,
                nom=r.get("full_name", ""),
                nom_court=r.get("abbreviation", ""),
                pays_id="USA"
            )
            
        matches_file = os.path.join(dossier, "basketball_game.csv")
        if os.path.exists(matches_file):
            dataframe_matchs = pd.read_csv(matches_file)
            
            home_wins = dataframe_matchs[dataframe_matchs["pts_home"] > dataframe_matchs["pts_away"]]["team_id_home"].value_counts()
            away_wins = dataframe_matchs[dataframe_matchs["pts_away"] > dataframe_matchs["pts_home"]]["team_id_away"].value_counts()
            total_wins = home_wins.add(away_wins, fill_value=0)
            
            home_games = dataframe_matchs["team_id_home"].value_counts()
            away_games = dataframe_matchs["team_id_away"].value_counts()
            total_games = home_games.add(away_games, fill_value=0)

            home_pts = dataframe_matchs.groupby("team_id_home")["pts_home"].sum()
            away_pts = dataframe_matchs.groupby("team_id_away")["pts_away"].sum()
            total_pts = home_pts.add(away_pts, fill_value=0)

            home_pts_enc = dataframe_matchs.groupby("team_id_home")["pts_away"].sum()
            away_pts_enc = dataframe_matchs.groupby("team_id_away")["pts_home"].sum()
            total_pts_enc = home_pts_enc.add(away_pts_enc, fill_value=0)

            stats_df = pd.DataFrame({
                "matches_joues": total_games,
                "victoires": total_wins,
                "defaites": total_games - total_wins,
                "points_marques": total_pts,
                "points_encaisses": total_pts_enc
            }).fillna(0).astype(int)

            dict_stats = stats_df.to_dict("index")
            for team_id, st in dict_stats.items():
                if team_id in res:
                    res[team_id].ajouter_statistiques(2023, st)
                    
        return res
