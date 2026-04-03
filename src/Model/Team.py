class Team:
    def __init__(self, id, nom: str, pays_id=None, nom_court: str = None):
        self.id          = id
        self.nom         = nom
        self.pays_id     = pays_id
        self.nom_court   = nom_court
        self.statistiques = {}

    def ajouter_statistiques(self, annee: int, stats: dict) -> None:
        self.statistiques[annee] = stats

    def __repr__(self):
        return f"Team({self.nom!r})"
