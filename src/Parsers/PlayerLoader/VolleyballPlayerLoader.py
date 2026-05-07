from .VolleyMenPlayerLoader import VolleyMenPlayerLoader
from .VolleyWomenPlayerLoader import VolleyWomenPlayerLoader


class VolleyballPlayerLoader():
    @staticmethod
    def load_all_player(dossier: str) -> dict:
        """
        Charge tous les joueurs de volleyball (hommes et femmes) depuis le dossier.

        Combine les résultats de VolleyMenPlayerLoader (gender='H')
        et de VolleyWomenPlayerLoader (gender='F').

        Args:
            dossier (str): Chemin vers le dossier contenant les fichiers CSV de volleyball.

        Returns:
            dict: Dictionnaire {nom_joueur: Player} combinant hommes et femmes.
        """
        joueurs = {}
        joueurs.update(VolleyMenPlayerLoader.load_all_player(dossier))
        joueurs.update(VolleyWomenPlayerLoader.load_all_player(dossier))
        return joueurs
