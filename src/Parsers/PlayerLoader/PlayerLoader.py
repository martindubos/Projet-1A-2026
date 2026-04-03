from src.Model.Player import Player
from .FootballPlayerLoader import FootballPlayerLoader
# from .LolPlayerLoader import LolPlayerLoader
# from .BasketPlayerLoader import BasketPlayerLoader
from .TennisWomenPlayerLoader import TennisWomenPlayerLoader
from .TennisMenPlayerLoader import TennisMenPlayerLoader
# from .VolleyPlayerLoader import VolleyPlayerLoader

class PlayerLoader():
    @staticmethod
    def load_all_player(sport_name: str, dossier: str) -> dict:
        if sport_name == "Football":
            return FootballPlayerLoader.load_all_player(dossier)
        elif sport_name == "Tennis":
            # On combine ATP et WTA pour le Tennis
            players = {}
            players.update(TennisMenPlayerLoader.load_all_player(dossier))
            players.update(TennisWomenPlayerLoader.load_all_player(dossier))
            return players
        elif sport_name == "Basketball":
            return {}
        elif sport_name == "Volleyball":
            return {}
        elif sport_name == "LoL":
            return {}
        else:
            raise Exception("Sport non supporte")
