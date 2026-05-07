import os
import csv
import pytest
from src.Parsers.MatchLoader.BadmintonMatchLoader import BadmintonMatchLoader


def creer_csv_matchs_badminton(dossier: str):
    """Crée un fichier match.csv minimal pour les tests."""
    chemin = os.path.join(dossier, "match.csv")
    with open(chemin, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["tournament", "city", "country", "date", "tournament_type",
                         "round", "player_1", "player_2", "winner",
                         "game_1_score", "game_2_score", "game_3_score"])
        # Match 1 : player_1 gagne
        writer.writerow(["BWF World Tour", "Paris", "France", "2020-03-15",
                         "Super 750", "Final",
                         "Akane Yamaguchi", "Carolina Marin",
                         "Akane Yamaguchi", "21-18", "21-15", ""])
        # Match 2 : player_2 gagne
        writer.writerow(["BWF World Tour", "Tokyo", "Japan", "2021-06-10",
                         "Super 750", "Semi-final",
                         "Viktor Axelsen", "Lee Zii Jia",
                         "Lee Zii Jia", "18-21", "21-19", "21-17"])
    return chemin


def test_badminton_match_loader_retourne_une_liste(tmp_path):
    """Vérifie que load_all_match retourne une liste."""
    creer_csv_matchs_badminton(str(tmp_path))
    matchs = BadmintonMatchLoader.load_all_match(str(tmp_path))
    assert isinstance(matchs, list)


def test_badminton_match_loader_charge_le_bon_nombre_de_matchs(tmp_path):
    """Vérifie que tous les matchs du CSV sont chargés."""
    creer_csv_matchs_badminton(str(tmp_path))
    matchs = BadmintonMatchLoader.load_all_match(str(tmp_path))
    assert len(matchs) == 2


def test_badminton_match_loader_player1_gagne(tmp_path):
    """Vérifie que le score est 1/0 quand player_1 gagne."""
    creer_csv_matchs_badminton(str(tmp_path))
    matchs = BadmintonMatchLoader.load_all_match(str(tmp_path))
    match1 = matchs[0]
    assert match1.equipe1_id == "Akane Yamaguchi"
    assert match1.score1 == 1
    assert match1.score2 == 0


def test_badminton_match_loader_player2_gagne(tmp_path):
    """Vérifie que le score est 0/1 quand player_2 gagne."""
    creer_csv_matchs_badminton(str(tmp_path))
    matchs = BadmintonMatchLoader.load_all_match(str(tmp_path))
    match2 = matchs[1]
    assert match2.equipe2_id == "Lee Zii Jia"
    assert match2.score1 == 0
    assert match2.score2 == 1


def test_badminton_match_loader_saison_extraite(tmp_path):
    """Vérifie que la saison est extraite correctement de la date."""
    creer_csv_matchs_badminton(str(tmp_path))
    matchs = BadmintonMatchLoader.load_all_match(str(tmp_path))
    assert matchs[0].saison == 2020
    assert matchs[1].saison == 2021


def test_badminton_match_loader_fichier_absent(tmp_path):
    """Vérifie que la fonction retourne [] si le fichier CSV est absent."""
    matchs = BadmintonMatchLoader.load_all_match(str(tmp_path))
    assert matchs == []
