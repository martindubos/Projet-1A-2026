import os
import pandas as pd
from src.Model.Match import Match, MatchVolley


class VolleyMatchLoader():
    @staticmethod
    def load_all_match(dossier: str) -> list:
        """
        Charge tous les matchs de volleyball (hommes et femmes) depuis les fichiers CSV.

        Fichiers attendus dans le dossier :
        - 'volleyball_match_men.csv'   : colonnes date, stage, country_code_1,
                                         country_code_2, set_country_1, set_country_2
        - 'volleyball_match_women.csv' : colonnes date, stage, country_1,
                                         country_2, set_country_1, set_country_2

        L'identifiant de chaque équipe est son code pays (ex: 'FRA', 'USA').
        Le score encode le nombre de sets gagnés par chaque équipe.
        La saison est l'année extraite de la date.

        Args:
            dossier (str): Chemin vers le dossier contenant les fichiers CSV.

        Returns:
            list: Liste d'objets Match combinant les matchs masculins et féminins.
        """
        matchs = []

        fichier_hommes = os.path.join(dossier, "volleyball_match_men.csv")
        if os.path.exists(fichier_hommes):
            tableau = pd.read_csv(fichier_hommes)
            for ligne in tableau.to_dict("records"):
                pays1 = ligne.get("country_code_1")
                pays2 = ligne.get("country_code_2")

                if pays1 is None or pays2 is None:
                    continue
                if isinstance(pays1, float) or isinstance(pays2, float):
                    continue

                sets1 = ligne.get("set_country_1", 0) or 0
                sets2 = ligne.get("set_country_2", 0) or 0

                saison = None
                date_brute = ligne.get("date")
                if date_brute is not None and not isinstance(date_brute, float):
                    try:
                        saison = int(str(date_brute)[:4])
                    except (ValueError, IndexError):
                        saison = None

                matchs.append(MatchVolley(
                    id=None,
                    equipe1_id=str(pays1).strip(),
                    equipe2_id=str(pays2).strip(),
                    score1=int(sets1),
                    score2=int(sets2),
                    date=date_brute,
                    saison=saison,
                    gender='H',
                    stage=ligne.get('stage')
                ))

        fichier_femmes = os.path.join(dossier, "volleyball_match_women.csv")
        if os.path.exists(fichier_femmes):
            tableau = pd.read_csv(fichier_femmes)
            for ligne in tableau.to_dict("records"):
                pays1 = ligne.get("country_1")
                pays2 = ligne.get("country_2")

                if pays1 is None or pays2 is None:
                    continue
                if isinstance(pays1, float) or isinstance(pays2, float):
                    continue

                sets1 = ligne.get("set_country_1", 0) or 0
                sets2 = ligne.get("set_country_2", 0) or 0

                saison = None
                date_brute = ligne.get("date")
                if date_brute is not None and not isinstance(date_brute, float):
                    try:
                        saison = int(str(date_brute)[:4])
                    except (ValueError, IndexError):
                        saison = None

                matchs.append(MatchVolley(
                    id=None,
                    equipe1_id=str(pays1).strip(),
                    equipe2_id=str(pays2).strip(),
                    score1=int(sets1),
                    score2=int(sets2),
                    date=date_brute,
                    saison=saison,
                    gender='F',
                    stage=ligne.get('stage')
                ))

        return matchs
