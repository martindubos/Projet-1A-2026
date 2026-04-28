import os
import pandas as pd
from src.Model.Team import Team

class FootballTeamLoader():
    @staticmethod
    def load_all_team(dossier: str) -> dict:
        team_file = os.path.join(dossier, "team.csv")
        match_file = os.path.join(dossier, "match.csv")
        if not os.path.exists(team_file):
            return {}
            
        dataframe_equipes = pd.read_csv(team_file)
        
        res = {}
        for r in dataframe_equipes.to_dict("records"):
            team_id = r.get("team_api_id")
            res[team_id] = Team(
                id=team_id,
                nom=r.get("team_long_name", ""),
                nom_court=r.get("team_short_name", "")
            )

        if os.path.exists(match_file):
            print("Calcul des statistiques des équipes de football en cours, veuillez patienter...")
            dataframe_matchs = pd.read_csv(match_file)
            
            home = dataframe_matchs[['season', 'home_team_api_id', 'home_team_goal', 'away_team_goal']].copy()
            home.columns = ['season', 'team_id', 'goals_for', 'goals_against']
            home['win'] = (home['goals_for'] > home['goals_against']).astype(int)
            home['draw'] = (home['goals_for'] == home['goals_against']).astype(int)
            home['loss'] = (home['goals_for'] < home['goals_against']).astype(int)
            home['played'] = 1

            away = dataframe_matchs[['season', 'away_team_api_id', 'away_team_goal', 'home_team_goal']].copy()
            away.columns = ['season', 'team_id', 'goals_for', 'goals_against']
            away['win'] = (away['goals_for'] > away['goals_against']).astype(int)
            away['draw'] = (away['goals_for'] == away['goals_against']).astype(int)
            away['loss'] = (away['goals_for'] < away['goals_against']).astype(int)
            away['played'] = 1

            all_matches = pd.concat([home, away])
            stats = all_matches.groupby(['season', 'team_id']).sum().reset_index()
            
            # Calcul des points et de la différence de buts pour le classement
            stats['points'] = 3 * stats['win'] + stats['draw']
            stats['goal_diff'] = stats['goals_for'] - stats['goals_against']
            
            # Classement par saison : points DESC, puis goal_diff DESC
            stats = stats.sort_values(by=['season', 'points', 'goal_diff'], ascending=[True, False, False])
            stats['rank'] = stats.groupby('season').cumcount() + 1

            for row in stats.to_dict('records'):
                t_id = row['team_id']
                if t_id in res:
                    res[t_id].ajouter_statistiques(row['season'], {
                        "Classement": int(row['rank']),
                        "Matchs joués": int(row['played']),
                        "Victoires": int(row['win']),
                        "Nuls": int(row['draw']),
                        "Défaites": int(row['loss']),
                        "Buts marqués": int(row['goals_for']),
                        "Buts encaissés": int(row['goals_against'])
                    })

        return res
