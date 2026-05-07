import pytest
from src.Model.Team import Team


def test_team_creation_attributs():
    """Vérifie que les attributs d'une Team sont correctement initialisés."""
    equipe = Team(id=1, nom="Real Madrid", nom_court="RMA", pays_id="ESP")
    assert equipe.id == 1
    assert equipe.nom == "Real Madrid"
    assert equipe.nom_court == "RMA"
    assert equipe.pays_id == "ESP"
    assert equipe.statistiques == {}


def test_team_ajouter_statistiques():
    """Vérifie que ajouter_statistiques stocke bien les stats par saison."""
    equipe = Team(id=1, nom="Arsenal", nom_court="ARS")
    stats = {"Victoires": 20, "Defaites": 5, "Nuls": 13}
    equipe.ajouter_statistiques("2023/2024", stats)
    assert "2023/2024" in equipe.statistiques
    assert equipe.statistiques["2023/2024"]["Victoires"] == 20


def test_team_ajouter_statistiques_plusieurs_saisons():
    """Vérifie que les stats peuvent être stockées pour plusieurs saisons."""
    equipe = Team(id=2, nom="Chelsea", nom_court="CHE")
    equipe.ajouter_statistiques(2022, {"Victoires": 10})
    equipe.ajouter_statistiques(2023, {"Victoires": 12})
    assert len(equipe.statistiques) == 2
    assert equipe.statistiques[2022]["Victoires"] == 10
    assert equipe.statistiques[2023]["Victoires"] == 12


def test_team_repr():
    """Vérifie que la représentation string d'une Team est correcte."""
    equipe = Team(id=3, nom="Paris Saint-Germain")
    assert repr(equipe) == "Team('Paris Saint-Germain')"


def test_team_pays_id_optionnel():
    """Vérifie que pays_id est None par défaut."""
    equipe = Team(id=4, nom="Test FC")
    assert equipe.pays_id is None
