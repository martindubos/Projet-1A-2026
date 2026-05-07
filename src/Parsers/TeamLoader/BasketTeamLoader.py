import os
import pandas as pd
from src.Model.Team import Team

class BasketTeamLoader():
    @staticmethod
    def load_all_team(dossier: str) -> dict:
        """
        Charge toutes les équipes de basketball et calcule leurs statistiques globales.

        Fichiers attendus dans le dossier :
        - 'basketball_team.csv' : colonnes id, full_name, abbreviation
        - 'basketball_game.csv' : colonnes team_id_home, team_id_away,
                                  pts_home, pts_away

        Les statistiques (matchs joués, victoires, défaites, points marqués/encaissés)
        sont calculées sur l'ensemble des matchs disponibles et stockées sous la saison 2023.

        Args:
            dossier (str): Chemin vers le dossier contenant les fichiers CSV.

        Returns:
            dict: Dictionnaire {team_id: Team} avec statistiques.
                  Retourne {} si basketball_team.csv est introuvable.
        """
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
            df = pd.read_csv(matches_file)
            saisons = df["season"].unique()
            
            for s in saisons:
                df_s = df[df["season"] == s]
                
                # Aggregation stats domicile
                home_agg = df_s.groupby("team_id_home").agg({
                    "pts_home": "sum", "pts_away": "sum",
                    "fga_home": "sum", "fgm_home": "sum", "fg3m_home": "sum",
                    "fta_home": "sum", "oreb_home": "sum", "dreb_home": "sum", "reb_home": "sum",
                    "tov_home": "sum", "ast_home": "sum", "min": "sum", "game_id": "count"
                }).rename(columns={
                    "pts_home": "pts_scored", "pts_away": "pts_allowed",
                    "fga_home": "fga", "fgm_home": "fgm", "fg3m_home": "fg3m",
                    "fta_home": "fta", "oreb_home": "oreb", "dreb_home": "dreb", "reb_home": "reb",
                    "tov_home": "tov", "ast_home": "ast", "min": "min", "game_id": "games"
                })
                
                # Aggregation stats extérieur
                away_agg = df_s.groupby("team_id_away").agg({
                    "pts_away": "sum", "pts_home": "sum",
                    "fga_away": "sum", "fgm_away": "sum", "fg3m_away": "sum",
                    "fta_away": "sum", "oreb_away": "sum", "dreb_away": "sum", "reb_away": "sum",
                    "tov_away": "sum", "ast_away": "sum", "min": "sum", "game_id": "count"
                }).rename(columns={
                    "pts_away": "pts_scored", "pts_home": "pts_allowed",
                    "fga_away": "fga", "fgm_away": "fgm", "fg3m_away": "fg3m",
                    "fta_away": "fta", "oreb_away": "oreb", "dreb_away": "dreb", "reb_away": "reb",
                    "tov_away": "tov", "ast_away": "ast", "min": "min", "game_id": "games"
                })
                
                all_stats = home_agg.add(away_agg, fill_value=0)
                
                # Victoires
                home_wins = df_s[df_s["pts_home"] > df_s["pts_away"]]["team_id_home"].value_counts()
                away_wins = df_s[df_s["pts_away"] > df_s["pts_home"]]["team_id_away"].value_counts()
                total_wins = home_wins.add(away_wins, fill_value=0)
                
                for team_id, row in all_stats.iterrows():
                    if team_id not in res: continue
                    
                    pts = row["pts_scored"]
                    pts_allow = row["pts_allowed"]
                    fga = row["fga"]; fgm = row["fgm"]; fg3m = row["fg3m"]
                    fta = row["fta"]; reb = row["reb"]; ast = row["ast"]
                    tov = row["tov"]; oreb = row["oreb"]; minutes = row["min"]
                    games = row["games"]
                    wins = total_wins.get(team_id, 0)
                    
                    # Formules
                    poss = 0.96 * (fga + tov + 0.44 * fta - oreb)
                    off_rtg = 100 * (pts / poss) if poss > 0 else 0
                    def_rtg = 100 * (pts_allow / poss) if poss > 0 else 0
                    ts_pct = pts / (2 * (fga + 0.44 * fta)) if (fga + 0.44 * fta) > 0 else 0
                    efg_pct = (fgm + 0.5 * fg3m) / fga if fga > 0 else 0
                    pace = 48 * (poss / (minutes / 5)) if minutes > 0 else 0
                    
                    res[team_id].ajouter_statistiques(s, {
                        "Matchs joues": int(games),
                        "Victoires": int(wins),
                        "Defaites": int(games - wins),
                        "Points marques": int(pts),
                        "Points encaisses": int(pts_allow),
                        "PPG": round(pts / games, 1) if games > 0 else 0,
                        "RPG": round(reb / games, 1) if games > 0 else 0,
                        "APG": round(ast / games, 1) if games > 0 else 0,
                        "TS%": round(ts_pct * 100, 1),
                        "eFG%": round(efg_pct * 100, 1),
                        "OffRtg": round(off_rtg, 1),
                        "DefRtg": round(def_rtg, 1),
                        "Net Rating": round(off_rtg - def_rtg, 1),
                        "Pace": round(pace, 1),
                        "AST/TOV": round(ast / tov, 2) if tov > 0 else ast
                    })
                    
        return res
