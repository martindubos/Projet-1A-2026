import datetime
import pytest
from src.Model.Match import Match, MatchTennis, MatchFootball, MatchBasketball


def test_match_vainqueur_equipe1():
    """Vérifie que vainqueur_id() retourne l'id de l'équipe 1 quand elle gagne."""
    m = Match(id=1, equipe1_id="A", equipe2_id="B", score1=3, score2=1)
    assert m.vainqueur_id() == "A"


def test_match_vainqueur_equipe2():
    """Vérifie que vainqueur_id() retourne l'id de l'équipe 2 quand elle gagne."""
    m = Match(id=2, equipe1_id="A", equipe2_id="B", score1=0, score2=2)
    assert m.vainqueur_id() == "B"


def test_match_nul_retourne_none():
    """Vérifie que vainqueur_id() retourne None en cas d'égalité."""
    m = Match(id=3, equipe1_id="A", equipe2_id="B", score1=1, score2=1)
    assert m.vainqueur_id() is None


def test_match_tennis_attributs():
    """Vérifie que MatchTennis stocke correctement ses attributs spécifiques."""
    m = MatchTennis(
        id=10, equipe1_id="player1", equipe2_id="player2",
        score1=1, score2=0,
        surface="Clay", round="Final", tournoi="Roland Garros",
        circuit="ATP", saison=2024
    )
    assert m.surface == "Clay"
    assert m.circuit == "ATP"
    assert m.saison == 2024
    assert m.vainqueur_id() == "player1"


def test_match_football_compositions_vides_par_defaut():
    """Vérifie que les compositions joueurs sont vides par défaut pour MatchFootball."""
    m = MatchFootball(id=100, equipe1_id=1, equipe2_id=2, score1=2, score2=1)
    assert m.joueurs_dom == []
    assert m.joueurs_ext == []


def test_match_basketball_saison_et_type():
    """Vérifie que MatchBasketball stocke saison et season_type."""
    m = MatchBasketball(
        id=200, equipe1_id=10, equipe2_id=20,
        score1=110, score2=95,
        saison=2022, season_type="Playoffs"
    )
    assert m.saison == 2022
    assert m.season_type == "Playoffs"
    assert m.vainqueur_id() == 10
