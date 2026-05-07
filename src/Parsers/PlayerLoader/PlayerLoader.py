from src.Model.Player import Player
from .FootballPlayerLoader import FootballPlayerLoader
from .BasketPlayerLoader import BasketPlayerLoader
from .TennisWomenPlayerLoader import TennisWomenPlayerLoader
from .TennisMenPlayerLoader import TennisMenPlayerLoader
from .BadmintonPlayerLoader import BadmintonPlayerLoader
from .VolleyballPlayerLoader import VolleyballPlayerLoader


class PlayerLoader():
    @staticmethod
    def load_all_player(sport_name: str, dossier: str) -> dict:
        """
        Dispatcher principal pour le chargement des joueurs selon le sport.

        Délègue le chargement au loader spécifique à chaque sport.
        Pour le Tennis, combine les circuits ATP (hommes) et WTA (femmes).
        Pour le Volleyball, combine les joueurs masculins et féminins.

        Args:
            sport_name (str): Nom du sport (ex: 'Football', 'Tennis', 'Basketball',
                              'Badminton', 'Volleyball').
            dossier (str): Chemin vers le dossier contenant les fichiers CSV.

        Returns:
            dict: Dictionnaire {id_joueur: Player}.

        Raises:
            Exception: Si le sport n'est pas supporté.
        """
        if sport_name == "Football":
            return FootballPlayerLoader.load_all_player(dossier)
        elif sport_name == "Tennis":
            # On combine ATP et WTA pour le Tennis
            players = {}
            players.update(TennisMenPlayerLoader.load_all_player(dossier))
            players.update(TennisWomenPlayerLoader.load_all_player(dossier))
            return players
        elif sport_name == "Basketball":
            return BasketPlayerLoader.load_all_player(dossier)
        elif sport_name == "Badminton":
            return BadmintonPlayerLoader.load_all_player(dossier)
        elif sport_name == "Volleyball":
            return VolleyballPlayerLoader.load_all_player(dossier)
        else:
            raise Exception("Sport non supporte")
