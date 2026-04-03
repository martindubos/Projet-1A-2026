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
        pts = {}
        for m in self.matchs:
            for eid in [m.equipe1_id, m.equipe2_id]:
                pts.setdefault(eid, 0)
            v = m.vainqueur_id()
            if v is not None:
                pts[v] += 3
            else:  # draw
                pts[m.equipe1_id] += 1
                pts[m.equipe2_id] += 1
                
        self.classement = sorted(pts.items(), key=lambda x: -x[1])
        return self.classement

    def get_equipe(self, nom: str):
        for eq in self.equipes.values():
            if eq.nom and eq.nom.lower() == nom.lower():
                return eq
        return None

    def get_joueur(self, nom: str):
        for j in self.joueurs.values():
            if j.nom_complet() and nom.lower() in j.nom_complet().lower():
                return j
        return None

    def __repr__(self) -> str:
        return (f"Sport({self.nom!r}, "
                f"{len(self.equipes)} equipes, "
                f"{len(self.joueurs)} joueurs, "
                f"{len(self.matchs)} matchs)")