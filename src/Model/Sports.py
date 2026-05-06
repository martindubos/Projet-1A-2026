from src.Parsers.PlayerLoader.PlayerLoader import PlayerLoader
from src.Parsers.MatchLoader.MatchLoader import MatchLoader
from src.Parsers.TeamLoader.TeamLoader import TeamLoader

class Sport:
    def __init__(self, nom: str, dossier: str = None, sport_en_equipe: bool = False, type_sport: str = None):
        self.nom = nom
        self.type_sport = type_sport if type_sport else nom
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
            self.joueurs = PlayerLoader.load_all_player(self.type_sport, self.dossier)
        except Exception as e:
            print(f"[{self.nom}] Erreur chargement joueurs: {e}")
            
        try:
            self.equipes = TeamLoader.load_all_team(self.type_sport, self.dossier)
        except Exception as e:
            # Some sports don't have teams, that's fine
            print(f"[{self.nom}] Erreur chargement equipes: {e}")
            
        try:
            self.matchs = MatchLoader.load_all_match(self.type_sport, self.dossier)
        except Exception as e:
            print(f"[{self.nom}] Erreur chargement matchs: {e}")
            
        # Optional: compute a basic ranking if needed
        self.calculer_classement()

    def calculer_classement(self, saison_filtre=None) -> list:
        points_par_entite = {}
        for match_en_cours in self.matchs:
            # Filtrage par saison si demande
            if saison_filtre:
                s_match = getattr(match_en_cours, 'saison', None)
                if s_match:
                    if str(s_match) != str(saison_filtre):
                        continue
                elif hasattr(match_en_cours, 'date') and match_en_cours.date:
                    # Pour le Tennis via l'annee de la date
                    if str(match_en_cours.date.year) != str(saison_filtre):
                        continue
            
            for eid in [match_en_cours.equipe1_id, match_en_cours.equipe2_id]:
                points_par_entite.setdefault(eid, 0)
            vainqueur_id = match_en_cours.vainqueur_id()
            if vainqueur_id is not None:
                points_par_entite[vainqueur_id] += 3
            else:  # match nul
                if match_en_cours.equipe1_id in points_par_entite:
                    points_par_entite[match_en_cours.equipe1_id] += 1
                if match_en_cours.equipe2_id in points_par_entite:
                    points_par_entite[match_en_cours.equipe2_id] += 1
                
        return sorted(points_par_entite.items(), key=lambda x: -x[1])

    def get_equipe(self, nom: str):
        matches = self.get_equipe_matches(nom)
        return matches[0] if matches else None

    def get_equipe_matches(self, nom: str):
        matches = []
        for equipe_courante in self.equipes.values():
            if equipe_courante.nom and nom.lower() in equipe_courante.nom.lower():
                matches.append(equipe_courante)
        return matches

    def get_joueur(self, nom: str):
        matches = self.get_joueur_matches(nom)
        return matches[0] if matches else None

    def get_joueur_matches(self, nom: str):
        matches = []
        for joueur_courant in self.joueurs.values():
            if joueur_courant.nom_complet() and nom.lower() in joueur_courant.nom_complet().lower():
                matches.append(joueur_courant)
        return matches

    def __repr__(self) -> str:
        return (f"Sport({self.nom!r}, "
                f"{len(self.equipes)} equipes, "
                f"{len(self.joueurs)} joueurs, "
                f"{len(self.matchs)} matchs)")