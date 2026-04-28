from src.Model.Match import Match
from .FootballMatchLoader import FootballMatchLoader
# from .LolMatchLoader import LolMatchLoader
from .BasketballMatchLoader import BasketballMatchLoader
from .TennisMatchLoader import TennisMatchLoader
# from .VolleyMatchLoader import VolleyMatchLoader

match_loaders_by_sports = {
    "football": FootballMatchLoader,
    "tennis": TennisMatchLoader,
    # "volleyball": VolleyMatchLoader,
    "basketball": BasketballMatchLoader
}

class MatchLoader():
    @staticmethod
    def load_all_match(nom_sport: str, dossier: str) -> list:
        loader = match_loaders_by_sports.get(nom_sport.lower())

        if loader is None:
            raise Exception("Sport non supporte")
        return loader.load_all_match(dossier)