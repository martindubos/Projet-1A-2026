import os
import pickle
from src.Model.Sports import Sport

def sauvegarder_sport(sport: Sport, dossier_obj: str = "objets") -> None:
    os.makedirs(dossier_obj, exist_ok=True)
    chemin = os.path.join(dossier_obj, f"{sport.nom.lower()}.p")
    with open(chemin, "wb") as f:
        pickle.dump(sport, f)

def charger_sport(nom: str, dossier_obj: str = "objets") -> Sport:
    chemin = os.path.join(dossier_obj, f"{nom.lower()}.p")
    if os.path.exists(chemin):
        with open(chemin, "rb") as f:
            return pickle.load(f)
    return None

def main():
    configs = {
        "1": ("Tennis", "data/tennis"),
        "2": ("Football", "data/football_european_leagues"),
        "3": ("Basketball", "data/basketball"),
        # "4": ("Volleyball", "data/volleyball"),
        # "5": ("LoL", "data/league_of_legends")
    }

    while True:
        print("\n" + "="*30)
        print("=== MENU PRINCIPAL ===")
        print("="*30)
        print("1. Charger les donnees CSV")
        print("2. Consulter des statistiques")
        print("3. Quitter")
        
        choix_menu = input("Que souhaitez-vous faire ? (1/2/3) : ")

        if choix_menu == "3":
            print("Au revoir !")
            break

        elif choix_menu == "1":
            print("\n-- Chargement des donnees --")
            print("Pour quel sport voulez-vous charger les donnees ?")
            for key, (nom, _) in configs.items():
                print(f"{key}. {nom}")
            print("A. Tous les sports disponibles")
            
            choix_sport = input("Votre choix : ").upper()
            
            sports_a_charger = []
            if choix_sport == "A":
                sports_a_charger = list(configs.values())
            elif choix_sport in configs:
                sports_a_charger = [configs[choix_sport]]
            else:
                print("Choix invalide.")
                continue

            for nom, dossier in sports_a_charger:
                print(f"\nChargement depuis CSV pour {nom}...")
                nouveau_sport = Sport(nom, dossier)
                sauvegarder_sport(nouveau_sport)
                print(f"[{nom}] Les donnees ont ete chargees et sauvegardees.")

        elif choix_menu == "2":
            print("\n-- Consultation des Statistiques --")
            print("Choisissez un sport :")
            for key, (nom, _) in configs.items():
                print(f"{key}. {nom}")
            
            choix_sport = input("Votre choix : ")
            if choix_sport not in configs:
                print("Choix invalide.")
                continue
                
            nom_sport = configs[choix_sport][0]
            
            # Chargement de l'objet sport memoire
            sport_obj = charger_sport(nom_sport)
            if not sport_obj:
                print(f"Les donnees de {nom_sport} n'ont pas encore ete chargees. Veuillez d'abord choisir l'option 1 du menu.")
                continue
                
            # Sous-menu pour les statistiques
            print("\nQuel type de statistiques souhaitez-vous consulter ?")
            print("1. Rechercher les statistiques d'un joueur precis (Ex: Serena Williams)")
            print("2. Rechercher les statistiques d'une equipe/club (Ex: Arsenal)")
            print("3. Voir le classement global du sport")
            print("4. Retour au menu principal")
            
            choix_stat = input("Votre choix : ")
            
            if choix_stat == "1":
                nom_joueur = input("\nEntrez le nom du joueur (ou une partie du nom) : ")
                joueur = sport_obj.get_joueur(nom_joueur)
                if joueur:
                    print(f"\n--- Fiche du joueur ---")
                    print(f"Nom complet: {joueur.nom_complet()}")
                    if joueur.date_naissance: print(f"Date de naissance: {joueur.date_naissance}")
                    if joueur.taille: print(f"Taille: {joueur.taille} cm")
                    print(f"Pays: {joueur.pays}")
                    print(f"\n>>> STATISTIQUES (2024) :")
                    for k, v in joueur.statistiques.get(2024, {}).items():
                        print(f"  - {k} : {v}")
                else:
                    print("Joueur introuvable.")

            elif choix_stat == "2":
                nom_equipe = input("\nEntrez le nom de l'equipe : ")
                equipe = sport_obj.get_equipe(nom_equipe)
                if equipe:
                    print(f"\n--- Fiche de l'equipe ---")
                    print(f"Nom: {equipe.nom} ({equipe.nom_court})")
                    if not equipe.statistiques:
                        print("\n>>> Aucune statistique disponible pour cette equipe.")
                    else:
                        saisons_disponibles = sorted(list(equipe.statistiques.keys()))
                        print(f"\n>>> Saisons disponibles : {', '.join(map(str, saisons_disponibles))}")
                        saison_choisie = input("Entrez la saison pour voir les statistiques (ex: 2008/2009) : ")
                        
                        saison_cle = saison_choisie
                        # Convertir en int si possible au cas où la clé est numérique (ex: 2024 au Tennis)
                        try:
                            if int(saison_choisie) in equipe.statistiques:
                                saison_cle = int(saison_choisie)
                        except ValueError:
                            pass
                            
                        if saison_cle in equipe.statistiques:
                            print(f"\n>>> STATISTIQUES ({saison_cle}) :")
                            for k, v in equipe.statistiques[saison_cle].items():
                                print(f"  - {k} : {v}")
                        else:
                            print("Saison invalide ou introuvable.")
                else:
                    print("Equipe introuvable. Attention, certains sports comme le Tennis n'ont pas d'equipes.")

            elif choix_stat == "3":
                classement = sport_obj.classement
                if not classement:
                    print(f"\nAucun classement disponible. Le classement va etre calcule...")
                    classement = sport_obj.calculer_classement()
                    
                print(f"\n--- Classement global pour {nom_sport} (Top 10) ---")
                top = classement[:10]
                for i, (id_eq, points) in enumerate(top, 1):
                    print(f"{i}. ID_{id_eq} : {points} points")

            elif choix_stat == "4":
                continue
            else:
                print("Choix invalide.")
        else:
            print("Choix invalide.")

if __name__ == "__main__":
    main()
