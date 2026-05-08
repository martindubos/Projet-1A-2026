import os
import pandas as pd
from src.Model.Match import Match


class BadmintonMatchLoader():
    @staticmethod
    def load_all_match(dossier: str) -> list:
        """
        Charge tous les matchs de badminton depuis le fichier CSV du dossier.

        Le fichier attendu est 'match.csv'. Chaque ligne contient :
        - player_1     : nom du premier joueur
        - player_2     : nom du deuxième joueur
        - winner       : nom du vainqueur (égal à player_1 ou player_2)
        - date         : date du match au format 'YYYY-MM-DD'
        - tournament   : nom du tournoi
        - round        : tour du tournoi (ex: 'Final', 'Semi-final')

        En badminton (sport individuel), equipe1_id et equipe2_id sont les noms
        des joueurs. score1=1/score2=0 encode le résultat (pas de score numérique).
        La saison est l'année extraite de la date.

        Args:
            dossier (str): Chemin vers le dossier contenant match.csv.

        Returns:
            list: Liste d'objets Match.
                  Retourne [] si le fichier est introuvable.
        """
        fichier_matchs = os.path.join(dossier, "match.csv")
        if not os.path.exists(fichier_matchs):
            return []

        tableau_matchs = pd.read_csv(fichier_matchs)

        matchs = []
        for ligne in tableau_matchs.to_dict("records"):
            joueur1 = ligne.get("player_1")
            joueur2 = ligne.get("player_2")
            vainqueur = ligne.get("winner")

            if joueur1 is None or joueur2 is None or vainqueur is None:
                continue
            if isinstance(joueur1, float) or isinstance(joueur2, float):
                continue

            if str(vainqueur).strip() == str(joueur1).strip():
                score1, score2 = 1, 0
            else:
                score1, score2 = 0, 1
            saison = None
            date_brute = ligne.get("date")
            if date_brute is not None and not isinstance(date_brute, float):
                try:
                    saison = int(str(date_brute)[:4])
                except (ValueError, IndexError):
                    saison = None

            matchs.append(Match(
                id=None,
                equipe1_id=str(joueur1).strip(),
                equipe2_id=str(joueur2).strip(),
                score1=score1,
                score2=score2,
                date=date_brute,
                saison=saison
            ))

        return matchs
