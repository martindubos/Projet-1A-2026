import os
import pandas as pd
from src.Model.Match import MatchTennis


class TennisMatchLoader():
    @staticmethod
    def load_all_match(dossier: str) -> list:
        """
        Charge tous les matchs de tennis depuis les fichiers CSV du dossier.
        Les fichiers sont cherchés pour les deux circuits : ATP (hommes) et WTA (femmes).
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
