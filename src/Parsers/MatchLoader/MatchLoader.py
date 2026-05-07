from src.Model.Match import Match
from .FootballMatchLoader import FootballMatchLoader
from .BasketballMatchLoader import BasketballMatchLoader
from .TennisMatchLoader import TennisMatchLoader
from .BadmintonMatchLoader import BadmintonMatchLoader
from .VolleyMatchLoader import VolleyMatchLoader


match_loaders_by_sports = {
    "football":   FootballMatchLoader,
    "tennis":     TennisMatchLoader,
    "basketball": BasketballMatchLoader,
    "badminton":  BadmintonMatchLoader,
    "volleyball": VolleyMatchLoader,
}


class MatchLoader():
    @staticmethod
    def load_all_match(nom_sport: str, dossier: str) -> list:
        """
        Dispatcher principal pour le chargement des matchs selon le sport.

        Délègue le chargement au loader spécifique en se basant sur le nom
        du sport (insensible à la casse).

        Sports supportés : Football, Tennis, Basketball, Badminton, Volleyball.

        Args:
            nom_sport (str): Nom du sport (ex: 'Football', 'Tennis').
            dossier (str): Chemin vers le dossier contenant les fichiers CSV.

        Returns:
            list: Liste d'objets Match.

        Raises:
            Exception: Si le sport n'est pas supporté.
        """
        loader = match_loaders_by_sports.get(nom_sport.lower())

        if loader is None:
            raise Exception("Sport non supporte")
        return loader.load_all_match(dossier)