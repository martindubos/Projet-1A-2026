import os
import pandas as pd
from src.Model.Player import Player


class BadmintonPlayerLoader():
    @staticmethod
    def load_all_player(dossier: str) -> dict:
        """
        Charge tous les joueurs de badminton depuis le fichier CSV du dossier.

        Le fichier attendu est 'player.csv'. Chaque ligne contient :
        - name      : nom complet du joueur (utilisé comme identifiant unique)
        - country   : pays d'origine du joueur
        - continent : continent du joueur

        En badminton, le nom du joueur sert directement d'identifiant (id),
        car les matchs référencent les joueurs par leur nom.

        Args:
            dossier (str): Chemin vers le dossier contenant player.csv.

        Returns:
            dict: Dictionnaire {nom_joueur: Player}.
                  Retourne {} si le fichier est introuvable.
        """
        fichier_joueurs = os.path.join(dossier, "player.csv")
        if not os.path.exists(fichier_joueurs):
            return {}

        tableau_joueurs = pd.read_csv(fichier_joueurs)

        joueurs = {}
        for ligne in tableau_joueurs.to_dict("records"):
            nom = ligne.get("name", "")
            if not nom or (isinstance(nom, float)):
                continue

            pays = ligne.get("country", "")
            if pays is None or (isinstance(pays, float)):
                pays = ""

            joueurs[nom] = Player(
                id=nom,
                lastname=nom,
                firstname="",
                birthdate=None,
                country=pays,
                height=None
            )

        fichier_matchs = os.path.join(dossier, "match.csv")
        if os.path.exists(fichier_matchs):
            print("Calcul des statistiques des joueurs de badminton...")
            df_matchs = pd.read_csv(fichier_matchs)
            
            stats_par_joueur = {}
            
            round_priority = {
                "Final": 7, "Semi final": 6, "Quarter final": 5,
                "Round of 16": 4, "Round of 32": 3,
                "Qualification final": 2, "Qualification semi final": 1, "Qualification quarter final": 0
            }
            round_to_code = {
                "Final": "F", "Semi final": "SF", "Quarter final": "QF",
                "Round of 16": "R16", "Round of 32": "R32",
                "Qualification final": "Q-F", "Qualification semi final": "Q-SF", "Qualification quarter final": "Q-QF"
            }

            for _, row in df_matchs.iterrows():
                p1, p2, winner = row['player_1'], row['player_2'], row['winner']
                tournament = row['tournament']
                round_name = row['round']
                date_val = str(row['date'])
                try:
                    saison = int(date_val[:4])
                except Exception:
                    saison = "Inconnue"
                
                if saison not in stats_par_joueur:
                    stats_par_joueur[saison] = {}
                
                for p in [p1, p2]:
                    if p not in stats_par_joueur[saison]:
                        stats_par_joueur[saison][p] = {
                            "Matchs joues": 0, "Victoires": 0, "Defaites": 0,
                            "Sets gagnes": 0, "Sets perdus": 0,
                            "Points marques": 0, "Points encaisses": 0,
                            "Tournois": {}, 
                        }
                    st = stats_par_joueur[saison][p]
                    st["Matchs joues"] += 1
                    
                    curr_prio = round_priority.get(round_name, -1)
                    if tournament not in st["Tournois"]:
                        st["Tournois"][tournament] = (round_name, p == winner)
                    else:
                        prev_round, _ = st["Tournois"][tournament]
                        prev_prio = round_priority.get(prev_round, -1)
                        if curr_prio >= prev_prio:
                            st["Tournois"][tournament] = (round_name, p == winner)

                    if p == winner:
                        st["Victoires"] += 1
                    else:
                        st["Defaites"] += 1
                        
                    for g in ['game_1_score', 'game_2_score', 'game_3_score']:
                        score_raw = row.get(g)
                        if pd.isna(score_raw) or score_raw == "":
                            continue
                        try:
                            s1, s2 = map(int, str(score_raw).split('-'))
                            my_score = s1 if p == p1 else s2
                            opp_score = s2 if p == p1 else s1
                            st["Points marques"] += my_score
                            st["Points encaisses"] += opp_score
                            if my_score > opp_score:
                                st["Sets gagnes"] += 1
                            elif my_score < opp_score:
                                st["Sets perdus"] += 1
                        except Exception:
                            pass

            for saison, players in stats_par_joueur.items():
                for p_name, st in players.items():
                    if p_name in joueurs:
                        win_rate = (st["Victoires"] / st["Matchs joues"] * 100) if st["Matchs joues"] > 0 else 0
                        
                        resultats_compet = {}
                        for t, (r_name, won) in st["Tournois"].items():
                            if r_name == "Final" and won:
                                code = "W"
                            else:
                                code = round_to_code.get(r_name, r_name)
                            resultats_compet[t] = code

                        final_stats = {
                            "Matchs joues": st["Matchs joues"],
                            "Victoires": st["Victoires"],
                            "Defaites": st["Defaites"],
                            "Taux de victoire": f"{win_rate:.1f}%",
                            "Sets gagnes": st["Sets gagnes"],
                            "Sets perdus": st["Sets perdus"],
                            "Points marques": st["Points marques"],
                            "Points encaisses": st["Points encaisses"],
                            "Nombre de tournois": len(st["Tournois"]),
                            "Resultats en compétitions": resultats_compet
                        }
                        
                        joueurs[p_name].ajouter_statistiques(saison, final_stats)

        return joueurs
