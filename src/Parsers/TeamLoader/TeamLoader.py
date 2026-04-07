from .FootballTeamLoader import FootballTeamLoader
# from .LolTeamLoader import LolTeamLoader
from .BasketTeamLoader import BasketTeamLoader
# from .VolleyTeamLoader import VolleyTeamLoader

class TeamLoader():
    @staticmethod
    def load_all_team(sport_name: str, dossier: str) -> dict:
        if sport_name == "Football":
            return FootballTeamLoader.load_all_team(dossier)
        elif sport_name == "Tennis":
            return {} # Le tennis n'a pas vraiment d'equipes dans ce dataset
        elif sport_name == "Basketball":
            return BasketTeamLoader.load_all_team(dossier)
        elif sport_name == "Volleyball":
            return {}
        elif sport_name == "LoL":
            return {}
        else:
            raise Exception("Sport non supporte")
