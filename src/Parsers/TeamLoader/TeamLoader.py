from .FootballTeamLoader import FootballTeamLoader
from .BasketTeamLoader import BasketTeamLoader
from .BadmintonTeamLoader import BadmintonTeamLoader
from .VolleyTeamLoader import VolleyTeamLoader


class TeamLoader():
    @staticmethod
    def load_all_team(sport_name: str, dossier: str) -> dict:
        """
        Dispatcher principal pour le chargement des équipes selon le sport.

        Délègue le chargement au loader spécifique à chaque sport.
        Le Tennis et le Badminton sont des sports individuels : ils retournent {}.
        Le Football, Basketball et Volleyball ont des équipes avec statistiques.

        Args:
            sport_name (str): Nom du sport (ex: 'Football', 'Tennis', 'Basketball',
                              'Badminton', 'Volleyball').
            dossier (str): Chemin vers le dossier contenant les fichiers CSV.

        Returns:
            dict: Dictionnaire {id_equipe: Team}.

        Raises:
            Exception: Si le sport n'est pas supporté.
        """
        if sport_name == "Football":
            return FootballTeamLoader.load_all_team(dossier)
        elif sport_name == "Tennis":
            return {}  
        elif sport_name == "Basketball":
            return BasketTeamLoader.load_all_team(dossier)
        elif sport_name == "Badminton":
            return BadmintonTeamLoader.load_all_team(dossier)
        elif sport_name == "Volleyball":
            return VolleyTeamLoader.load_all_team(dossier)
        else:
            raise Exception("Sport non supporte")
