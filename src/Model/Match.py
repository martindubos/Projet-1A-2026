class Match:
    def __init__(self, id, equipe1_id, equipe2_id,
                 score1, score2, date=None, saison=None):
        self.id         = id
        self.equipe1_id = equipe1_id
        self.equipe2_id = equipe2_id
        self.score1     = score1
        self.score2     = score2
        self.date       = date
        self.saison     = saison 

    def vainqueur_id(self):
        if self.score1 > self.score2:
            return self.equipe1_id
        if self.score2 > self.score1:
            return self.equipe2_id
        return None

class MatchTennis(Match):
    def __init__(self, *args, surface=None, round=None,
                 tournoi=None, circuit=None, saison=None,
                 w_ace=None, w_df=None, w_svpt=None, w_1stIn=None,
                 w_1stWon=None, w_2ndWon=None, w_SvGms=None,
                 w_bpSaved=None, w_bpFaced=None,
                 l_ace=None, l_df=None, l_svpt=None, l_1stIn=None,
                 l_1stWon=None, l_2ndWon=None, l_SvGms=None,
                 l_bpSaved=None, l_bpFaced=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.surface = surface   
        self.round   = round    
        self.tournoi = tournoi
        self.circuit = circuit   
        self.saison  = saison
        
        self.w_ace = w_ace
        self.w_df = w_df
        self.w_svpt = w_svpt
        self.w_1stIn = w_1stIn
        self.w_1stWon = w_1stWon
        self.w_2ndWon = w_2ndWon
        self.w_SvGms = w_SvGms
        self.w_bpSaved = w_bpSaved
        self.w_bpFaced = w_bpFaced
        
        self.l_ace = l_ace
        self.l_df = l_df
        self.l_svpt = l_svpt
        self.l_1stIn = l_1stIn
        self.l_1stWon = l_1stWon
        self.l_2ndWon = l_2ndWon
        self.l_SvGms = l_SvGms
        self.l_bpSaved = l_bpSaved
        self.l_bpFaced = l_bpFaced

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

class MatchVolley(Match):
    def __init__(self, *args, gender=None, stage=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.gender = gender
        self.stage = stage
