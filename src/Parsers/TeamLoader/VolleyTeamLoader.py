import os
import pandas as pd
from src.Model.Team import Team


class VolleyTeamLoader():
    @staticmethod
    def load_all_team(dossier: str) -> dict:
        """
        Charge toutes les équipes nationales de volleyball depuis les fichiers CSV.

        Le fichier 'volleyball_country.csv' fournit la liste des pays avec :
        - code         : code pays à 3 lettres (ex: 'FRA')
        - country      : nom court (ex: 'France')
        - country_long : nom complet (ex: 'France')

        Les statistiques sont calculées en parcourant les matchs (hommes + femmes) :
        - Sets gagnés / Sets perdus
        - Matchs joués / Victoires / Défaites
        Une victoire de match est accordée à l'équipe qui gagne le plus de sets (score > score adverse).

        Args:
            dossier (str): Chemin vers le dossier contenant les fichiers CSV.

        Returns:
            dict: Dictionnaire {code_pays: Team} avec statistiques par saison.
                  Retourne {} si le fichier des pays est introuvable.
        """
        fichier_pays = os.path.join(dossier, "volleyball_country.csv")
        if not os.path.exists(fichier_pays):
            return {}

        tableau_pays = pd.read_csv(fichier_pays)

        equipes = {}
        for ligne in tableau_pays.to_dict("records"):
            code = ligne.get("code", "")
            if not code or isinstance(code, float):
                continue
            nom = ligne.get("country", str(code))
            equipes[str(code)] = Team(
                id=str(code),
                nom=str(nom),
                nom_court=str(code),
                pays_id=str(code)
            )

        stats_par_saison = {}

        fichiers_a_traiter = [
            (os.path.join(dossier, "volleyball_match_men.csv"),   "country_code_1", "country_code_2"),
            (os.path.join(dossier, "volleyball_match_women.csv"), "country_1",      "country_2"),
        ]

        for fichier, col_equipe1, col_equipe2 in fichiers_a_traiter:
            if not os.path.exists(fichier):
                continue

            tableau = pd.read_csv(fichier)
            for ligne in tableau.to_dict("records"):
                id_eq1 = ligne.get(col_equipe1)
                id_eq2 = ligne.get(col_equipe2)

                if id_eq1 is None or id_eq2 is None:
                    continue
                if isinstance(id_eq1, float) or isinstance(id_eq2, float):
                    continue

                id_eq1 = str(id_eq1).strip()
                id_eq2 = str(id_eq2).strip()

                sets1 = ligne.get("set_country_1", 0) or 0
                sets2 = ligne.get("set_country_2", 0) or 0

                saison = None
                date_brute = ligne.get("date")
                if date_brute is not None and not isinstance(date_brute, float):
                    try:
                        saison = int(str(date_brute)[:4])
                    except (ValueError, IndexError):
                        saison = None

                if saison not in stats_par_saison:
                    stats_par_saison[saison] = {}

                for id_eq in [id_eq1, id_eq2]:
                    if id_eq not in stats_par_saison[saison]:
                        stats_par_saison[saison][id_eq] = {
                            "Matchs joues": 0,
                            "Victoires": 0,
                            "Defaites": 0,
                            "Sets gagnes": 0,
                            "Sets perdus": 0
                        }

                st1 = stats_par_saison[saison][id_eq1]
                st2 = stats_par_saison[saison][id_eq2]

                st1["Matchs joues"] += 1
                st2["Matchs joues"] += 1
                st1["Sets gagnes"] += int(sets1)
                st1["Sets perdus"] += int(sets2)
                st2["Sets gagnes"] += int(sets2)
                st2["Sets perdus"] += int(sets1)

                if int(sets1) > int(sets2):
                    st1["Victoires"] += 1
                    st2["Defaites"] += 1
                elif int(sets2) > int(sets1):
                    st2["Victoires"] += 1
                    st1["Defaites"] += 1

        for saison, equipes_de_la_saison in stats_par_saison.items():
            for id_eq, stats in equipes_de_la_saison.items():
                if id_eq in equipes:
                    equipes[id_eq].ajouter_statistiques(saison, stats)

        return equipes
