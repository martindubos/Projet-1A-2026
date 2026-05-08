from src.Parsers.PlayerLoader.PlayerLoader import PlayerLoader
from src.Parsers.MatchLoader.MatchLoader import MatchLoader
from src.Parsers.TeamLoader.TeamLoader import TeamLoader

class Sport:
    def __init__(self, nom: str, dossier: str = None, sport_en_equipe: bool = False, type_sport: str = None):
        self.nom = nom
        self.type_sport = type_sport if type_sport else nom
        self.dossier = dossier
        self.sport_en_equipe = sport_en_equipe
        self.equipes = {}
        self.joueurs = {}
        self.matchs = []
        self.classement = []
        
        if self.dossier:
            self.charger_donnees()

    def charger_donnees(self) -> None:
        print(f"Chargement des Donnees pour le sport: {self.nom}")
        
        try:
            self.joueurs = PlayerLoader.load_all_player(self.type_sport, self.dossier)
        except Exception as e:
            print(f"[{self.nom}] Erreur chargement joueurs: {e}")
            
        try:
            self.equipes = TeamLoader.load_all_team(self.type_sport, self.dossier)
        except Exception as e:
            print(f"[{self.nom}] Erreur chargement equipes: {e}")
            
        try:
            self.matchs = MatchLoader.load_all_match(self.type_sport, self.dossier)
        except Exception as e:
            print(f"[{self.nom}] Erreur chargement matchs: {e}")
            
        self.calculer_classement()

    def calculer_classement(self, saison_filtre=None) -> list:
        """
        Calcule le classement : 3 points pour une victoire, 1 point par équipe pour un nul.
        Si saison_filtre est fourni, on ne prend en compte que les matchs de cette saison.
        """
        points_par_entite = {}

        for match in self.matchs:
            if saison_filtre is not None:
                saison_du_match = match.saison
                if saison_du_match is None or str(saison_du_match) != str(saison_filtre):
                    continue

            if match.equipe1_id not in points_par_entite:
                points_par_entite[match.equipe1_id] = 0
            if match.equipe2_id not in points_par_entite:
                points_par_entite[match.equipe2_id] = 0

            id_vainqueur = match.vainqueur_id()

            if id_vainqueur is not None:
                points_par_entite[id_vainqueur] += 3
            else:
                points_par_entite[match.equipe1_id] += 1
                points_par_entite[match.equipe2_id] += 1

        classement = sorted(points_par_entite.items(), key=lambda x: x[1], reverse=True)
        return classement

    def get_equipe(self, nom: str):
        resultats = self.get_equipe_matches(nom)
        return resultats[0] if resultats else None

    def get_equipe_matches(self, nom: str):
        resultats = []
        for equipe in self.equipes.values():
            if equipe.nom and nom.lower() in equipe.nom.lower():
                resultats.append(equipe)
        return resultats

    def get_joueur(self, nom: str):
        resultats = self.get_joueur_matches(nom)
        return resultats[0] if resultats else None

    def get_joueur_matches(self, nom: str):
        resultats = []
        for joueur in self.joueurs.values():
            if joueur.nom_complet() and nom.lower() in joueur.nom_complet().lower():
                resultats.append(joueur)
        return resultats

    def __repr__(self) -> str:
        return (f"Sport({self.nom!r}, "
                f"{len(self.equipes)} equipes, "
                f"{len(self.joueurs)} joueurs, "
                f"{len(self.matchs)} matchs)")