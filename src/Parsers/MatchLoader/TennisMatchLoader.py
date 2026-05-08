import os
import pandas as pd
from src.Model.Match import MatchTennis


class TennisMatchLoader():
    @staticmethod
    def load_all_match(dossier: str) -> list:
        """
        Charge tous les matchs de tennis depuis les fichiers CSV du dossier.

        Les fichiers sont cherchés pour les deux circuits :
        - ATP (hommes) : 'atp_matches_2024.csv'
        - WTA (femmes) : 'wta_matches_2024.csv'

        Colonnes utilisées : winner_id, loser_id, tourney_date (YYYYMMDD),
        surface, round, tourney_name.
        En tennis, chaque joueur est l'entité directe (pas d'équipe).
        Le score encode toujours 1/0 (victoire/défaite car il n'y a pas de match nul).
        La saison est l'année extraite de tourney_date.

        Args:
            dossier (str): Chemin vers le dossier contenant les fichiers CSV.

        Returns:
            list: Liste d'objets MatchTennis (ATP + WTA combinés).
        """
        matchs = []

        for circuit in ['wta', 'atp']:
            fichier_matchs = os.path.join(dossier, f"{circuit}_matches_2024.csv")
            if not os.path.exists(fichier_matchs):
                continue

            tableau_matchs = pd.read_csv(fichier_matchs)

            for ligne in tableau_matchs.to_dict("records"):
                date_tournoi = ligne.get("tourney_date")
                if date_tournoi is not None and pd.notna(date_tournoi):
                    annee = int(str(date_tournoi)[:4])
                else:
                    annee = 2024

                matchs.append(MatchTennis(
                    id=ligne.get("match_num"),
                    equipe1_id=ligne.get("winner_id"),
                    equipe2_id=ligne.get("loser_id"),
                    score1=1,
                    score2=0,
                    surface=ligne.get("surface"),
                    round=ligne.get("round"),
                    tournoi=ligne.get("tourney_name"),
                    circuit=circuit.upper(),
                    saison=annee,
                    w_ace=ligne.get("w_ace"),
                    w_df=ligne.get("w_df"),
                    w_svpt=ligne.get("w_svpt"),
                    w_1stIn=ligne.get("w_1stIn"),
                    w_1stWon=ligne.get("w_1stWon"),
                    w_2ndWon=ligne.get("w_2ndWon"),
                    w_SvGms=ligne.get("w_SvGms"),
                    w_bpSaved=ligne.get("w_bpSaved"),
                    w_bpFaced=ligne.get("w_bpFaced"),
                    l_ace=ligne.get("l_ace"),
                    l_df=ligne.get("l_df"),
                    l_svpt=ligne.get("l_svpt"),
                    l_1stIn=ligne.get("l_1stIn"),
                    l_1stWon=ligne.get("l_1stWon"),
                    l_2ndWon=ligne.get("l_2ndWon"),
                    l_SvGms=ligne.get("l_SvGms"),
                    l_bpSaved=ligne.get("l_bpSaved"),
                    l_bpFaced=ligne.get("l_bpFaced")
                ))

        return matchs
