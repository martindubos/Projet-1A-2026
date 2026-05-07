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
                # La date du tournoi est au format YYYYMMDD (ex: 20240101)
                # On extrait les 4 premiers caractères pour obtenir l'année
                date_tournoi = ligne.get("tourney_date")
                if date_tournoi is not None and pd.notna(date_tournoi):
                    annee = int(str(date_tournoi)[:4])
                else:
                    annee = 2024

                matchs.append(MatchTennis(
                    id=ligne.get("match_num"),
                    # En tennis, chaque joueur est directement l'entité (pas une équipe)
                    equipe1_id=ligne.get("winner_id"),
                    equipe2_id=ligne.get("loser_id"),
                    # score1=1 car le gagnant a forcément gagné le match
                    score1=1,
                    score2=0,
                    surface=ligne.get("surface"),
                    round=ligne.get("round"),
                    tournoi=ligne.get("tourney_name"),
                    circuit=circuit.upper(),
                    saison=annee
                ))

        return matchs
