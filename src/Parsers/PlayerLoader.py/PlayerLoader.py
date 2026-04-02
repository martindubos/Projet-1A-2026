from src.Model.Sports import Sport
from src.Model.Player import Player
from .PlayerLoader.FootballPlayerLoader import FootballPlayerLoader
from .PlayerLoader.LolPlayerLoader import LolPlayerLoader
from .PlayerLoader.BasketPlayerLoader import BasketPlayerLoader
from .PlayerLoader.TennisPlayerLoader import TennisPlayerLoader
from .PlayerLoader.VolleyPlayerLoader import VolleyPlayerLoader

class PlayerLoader():
    def load_all_player(sport: Sport) -> [Player]:
        if sport.name == "Football":
            return FootballPlayerLoader().load_all_player()
        elif sport.name == "Lol":
            return LolPlayerLoader().load_all_player()
        elif sport.name == "Basket":
            return BasketPlayerLoader().load_all_player()
        elif sport.name == "Tennis":
            return TennisPlayerLoader().load_all_player()
        elif sport.name == "Volley":
            return VolleyPlayerLoader().load_all_player()
        else:
            raise Exception("Sport non supportté")
