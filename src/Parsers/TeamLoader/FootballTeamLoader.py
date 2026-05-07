import os
import pandas as pd
from src.Model.Team import Team


class FootballTeamLoader():
    @staticmethod
    def load_all_team(dossier: str) -> dict:
        """
        Charge toutes les équipes de football et calcule leurs statistiques par saison.

        Fichiers attendus dans le dossier :
        - 'team.csv'  : colonnes team_api_id, team_long_name, team_short_name
        - 'match.csv' : colonnes season, home_team_api_id, away_team_api_id,
                        home_team_goal, away_team_goal

        Les statistiques sont calculées en parcourant les matchs avec des boucles simples
        (sans opérations vectorielles Pandas complexes) pour plus de lisibilité.
        Pour chaque saison, on calcule par équipe : matchs joués, victoires, nuls,
        défaites, buts marqués, buts encaissés, points (V*3 + N), différence de buts.

        Args:
            dossier (str): Chemin vers le dossier contenant team.csv et match.csv.

        Returns:
            dict: Dictionnaire {team_api_id: Team} avec statistiques par saison.
                  Retourne {} si team.csv est introuvable.
        """
        fichier_equipes = os.path.join(dossier, "team.csv")
        fichier_matchs = os.path.join(dossier, "match.csv")

        if not os.path.exists(fichier_equipes):
            return {}

        tableau_equipes = pd.read_csv(fichier_equipes)

        # Construction du dictionnaire des équipes
        equipes = {}
        for ligne in tableau_equipes.to_dict("records"):
            id_equipe = ligne.get("team_api_id")
            equipes[id_equipe] = Team(
                id=id_equipe,
                nom=ligne.get("team_long_name", ""),
                nom_court=ligne.get("team_short_name", "")
            )

        # Mapping des noms de pays
        fichier_pays = os.path.join(dossier, "country.csv")
        noms_pays = {}
        if os.path.exists(fichier_pays):
            df_pays = pd.read_csv(fichier_pays)
            for _, r in df_pays.iterrows():
                noms_pays[r['id']] = r['name']

        # Attribution du pays aux équipes via match.csv
        if os.path.exists(fichier_matchs):
            df_matchs = pd.read_csv(fichier_matchs, usecols=['home_team_api_id', 'country_id'])
            mapping_team_country = df_matchs.drop_duplicates('home_team_api_id').set_index('home_team_api_id')['country_id'].to_dict()
            for id_e, eq in equipes.items():
                c_id = mapping_team_country.get(id_e)
                if c_id in noms_pays:
                    eq.pays_id = noms_pays[c_id]

        # Calcul des statistiques à partir des matchs
        if not os.path.exists(fichier_matchs):
            return equipes

        print("Calcul des statistiques des équipes de football en cours, veuillez patienter...")
        tableau_matchs = pd.read_csv(fichier_matchs)
        liste_matchs = tableau_matchs.to_dict("records")

        # On construit un dictionnaire :
        # stats_par_equipe = { saison: { id_equipe: { "victoires": ..., ...} } }
        stats_par_equipe = {}

        for match in liste_matchs:
            saison = match.get("season")
            id_domicile = match.get("home_team_api_id")
            id_exterieur = match.get("away_team_api_id")

            # On ignore les matchs avec des données manquantes
            if saison is None or id_domicile is None or id_exterieur is None:
                continue

            buts_domicile = match.get("home_team_goal", 0) or 0
            buts_exterieur = match.get("away_team_goal", 0) or 0

            # Initialisation des statistiques pour la saison si besoin
            if saison not in stats_par_equipe:
                stats_par_equipe[saison] = {}

            for id_equipe in [id_domicile, id_exterieur]:
                if id_equipe not in stats_par_equipe[saison]:
                    stats_par_equipe[saison][id_equipe] = {
                        "matchs_joues": 0,
                        "victoires": 0,
                        "nuls": 0,
                        "defaites": 0,
                        "buts_marques": 0,
                        "buts_encaisses": 0
                    }

            stats_dom = stats_par_equipe[saison][id_domicile]
            stats_ext = stats_par_equipe[saison][id_exterieur]

            stats_dom["matchs_joues"] += 1
            stats_ext["matchs_joues"] += 1
            stats_dom["buts_marques"] += buts_domicile
            stats_dom["buts_encaisses"] += buts_exterieur
            stats_ext["buts_marques"] += buts_exterieur
            stats_ext["buts_encaisses"] += buts_domicile

            if buts_domicile > buts_exterieur:
                stats_dom["victoires"] += 1
                stats_ext["defaites"] += 1
            elif buts_exterieur > buts_domicile:
                stats_ext["victoires"] += 1
                stats_dom["defaites"] += 1
            else:
                stats_dom["nuls"] += 1
                stats_ext["nuls"] += 1

        # Calcul des points et injection dans les objets Team
        for saison, equipes_de_la_saison in stats_par_equipe.items():
            for id_equipe, stats in equipes_de_la_saison.items():
                if id_equipe in equipes:
                    points = stats["victoires"] * 3 + stats["nuls"]
                    difference_buts = stats["buts_marques"] - stats["buts_encaisses"]

                    equipes[id_equipe].ajouter_statistiques(saison, {
                        "Matchs joues": stats["matchs_joues"],
                        "Victoires": stats["victoires"],
                        "Nuls": stats["nuls"],
                        "Defaites": stats["defaites"],
                        "Buts marques": stats["buts_marques"],
                        "Buts encaisses": stats["buts_encaisses"],
                        "Points": points,
                        "Difference de buts": difference_buts
                    })

        return equipes
