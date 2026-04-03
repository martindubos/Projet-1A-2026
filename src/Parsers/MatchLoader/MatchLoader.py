from .FootballMatchLoader import FootballMatchLoader
# from .LolMatchLoader import LolMatchLoader
# from .BasketballMatchLoader import BasketballMatchLoader
from .TennisMatchLoader import TennisMatchLoader
# from .VolleyMatchLoader import VolleyMatchLoader

class MatchLoader():
    @staticmethod
    def load_all_match(sport_name: str, dossier: str) -> list:
        if sport_name == "Football":
            return FootballMatchLoader.load_all_match(dossier)
        elif sport_name == "Tennis":
            return TennisMatchLoader.load_all_match(dossier)
        elif sport_name == "Basketball":
            return []
        elif sport_name == "Volleyball":
            return []
        elif sport_name == "LoL":
            return []
        else:
            raise Exception("Sport non supporte")
