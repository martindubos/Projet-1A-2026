from src.Parsers.PlayerLoader.PlayerLoader import PlayerLoader
from src.Parsers.MatchLoader.MatchLoader import MatchLoader
from src.Parsers.TeamLoader.TeamLoader import TeamLoader

class Sport:
    def __init__(self, nom: str, dossier: str = None, sport_en_equipe: bool = False):
        self.nom = nom
        self.dossier = dossier
        self.sport_en_equipe = sport_en_equipe
        self.equipes = {}   # id -> Team
        self.joueurs = {}   # id -> Player
        self.matchs = []    # list of Match
        self.classement = []
        
        if self.dossier:
            self.charger_donnees()

    def charger_donnees(self) -> None:
        # Delegation to parsers via Factory Pattern
        print(f"Chargement des Donnees pour le sport: {self.nom}")
        
        try:
            self.joueurs = PlayerLoader.load_all_player(self.nom, self.dossier)
        except Exception as e:
            print(f"[{self.nom}] Erreur chargement joueurs: {e}")
            
        try:
            self.equipes = TeamLoader.load_all_team(self.nom, self.dossier)
        except Exception as e:
            # Some sports don't have teams, that's fine
            print(f"[{self.nom}] Erreur chargement equipes: {e}")
            
        try:
            self.matchs = MatchLoader.load_all_match(self.nom, self.dossier)
        except Exception as e:
            print(f"[{self.nom}] Erreur chargement matchs: {e}")
            
        # Optional: compute a basic ranking if needed
        self.calculer_classement()

    def calculer_classement(self) -> list:
        points_par_equipe = {}
        for match_en_cours in self.matchs:
            for eid in [match_en_cours.equipe1_id, match_en_cours.equipe2_id]:
                points_par_equipe.setdefault(eid, 0)
            vainqueur_id = match_en_cours.vainqueur_id()
            if vainqueur_id is not None:
                points_par_equipe[vainqueur_id] += 3
            else:  # draw
                points_par_equipe[match_en_cours.equipe1_id] += 1
                points_par_equipe[match_en_cours.equipe2_id] += 1
                
        self.classement = sorted(points_par_equipe.items(), key=lambda x: -x[1])
        return self.classement

    def get_equipe(self, nom: str):
        for equipe_courante in self.equipes.values():
            if equipe_courante.nom and equipe_courante.nom.lower() == nom.lower():
                return equipe_courante
        return None

    def get_joueur(self, nom: str):
        for joueur_courant in self.joueurs.values():
            if joueur_courant.nom_complet() and nom.lower() in joueur_courant.nom_complet().lower():
                return joueur_courant
        return None

    def __repr__(self) -> str:
        return (f"Sport({self.nom!r}, "
                f"{len(self.equipes)} equipes, "
                f"{len(self.joueurs)} joueurs, "
                f"{len(self.matchs)} matchs)")