class Match:
    def __init__(self, id, equipe1_id, equipe2_id,
                 score1, score2, date=None):
        self.id         = id
        self.equipe1_id = equipe1_id
        self.equipe2_id = equipe2_id
        self.score1     = score1
        self.score2     = score2
        self.date       = date

    def vainqueur_id(self):
        if self.score1 > self.score2: return self.equipe1_id
        if self.score2 > self.score1: return self.equipe2_id
        return None  # match nul

class MatchTennis(Match):
    def __init__(self, *args, surface=None, round=None,
                 tournoi=None, circuit=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.surface = surface   # Hard / Clay / Grass
        self.round   = round     # F, SF, QF, R16...
        self.tournoi = tournoi
        self.circuit = circuit   # ATP ou WTA

class MatchFootball(Match):
    def __init__(self, *args, league_id=None, saison=None,
                 joueurs_dom=None, joueurs_ext=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.league_id   = league_id
        self.saison      = saison
        self.joueurs_dom = joueurs_dom or []
        self.joueurs_ext = joueurs_ext or []

class MatchBasketball(Match):
    def __init__(self, *args, saison=None, season_type=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.saison = saison
        self.season_type = season_type
