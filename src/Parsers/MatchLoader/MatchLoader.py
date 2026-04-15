from src.Model.Match import Match
from src.Model.Sport import Sport
from .FootballMatchLoader import FootballMatchLoader
# from .LolMatchLoader import LolMatchLoader
from .BasketballMatchLoader import BasketballMatchLoader
from .TennisMatchLoader import TennisMatchLoader
# from .VolleyMatchLoader import VolleyMatchLoader
from pandas import df


match_loaders_by_sports = {
    "football": FootbalMatchLoader,
    "tennis": TennisMatchLoader,
    "volleyball": VolleyMatchLoader,
    "basketball": BasketballMatchLoader
}

class MatchLoader():
    @staticmethod
    def load_all_matches(sport: Sport) -> df[Match]:


        loader = match_loaders_by_sports[sport]


        if loader is None :
            raise Exception("Sport non supporté")
        return loader.load_all_matches()