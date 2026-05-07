import os
import csv
import pytest
from src.Parsers.PlayerLoader.FootballPlayerLoader import FootballPlayerLoader


def creer_csv_joueurs_football(dossier: str):
    """Crée un fichier player.csv minimal au format football européen."""
    chemin = os.path.join(dossier, "player.csv")
    with open(chemin, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "player_api_id", "player_name", "birthday",
                         "weight (kg)", "height (cm)"])
        writer.writerow(["6176", "30981", "Lionel Messi", "1987-06-24", "72.1", "170"])
        writer.writerow(["1234", "12345", "Cristiano Ronaldo", "1985-02-05", "83.0", "187"])
    return chemin


def test_football_player_loader_retourne_un_dictionnaire(tmp_path):
    """Vérifie que load_all_player retourne un dictionnaire."""
    creer_csv_joueurs_football(str(tmp_path))
    joueurs = FootballPlayerLoader.load_all_player(str(tmp_path))
    assert isinstance(joueurs, dict)


def test_football_player_loader_messi_present(tmp_path):
    """Vérifie que Messi est correctement chargé depuis le CSV."""
    creer_csv_joueurs_football(str(tmp_path))
    joueurs = FootballPlayerLoader.load_all_player(str(tmp_path))
    assert 30981 in joueurs


def test_football_player_loader_messi_nom(tmp_path):
    """Vérifie que le nom complet de Messi est correct."""
    creer_csv_joueurs_football(str(tmp_path))
    joueurs = FootballPlayerLoader.load_all_player(str(tmp_path))
    messi = joueurs[30981]
    assert messi.nom_complet() == "Lionel Messi"


def test_football_player_loader_messi_taille(tmp_path):
    """Vérifie que la taille de Messi est correctement lue depuis 'height (cm)'."""
    creer_csv_joueurs_football(str(tmp_path))
    joueurs = FootballPlayerLoader.load_all_player(str(tmp_path))
    messi = joueurs[30981]
    assert messi.height == 170


def test_football_player_loader_date_naissance(tmp_path):
    """Vérifie que la date de naissance est correctement parsée."""
    import datetime
    creer_csv_joueurs_football(str(tmp_path))
    joueurs = FootballPlayerLoader.load_all_player(str(tmp_path))
    messi = joueurs[30981]
    assert messi.birthdate == datetime.date(1987, 6, 24)


def test_football_player_loader_fichier_absent(tmp_path):
    """Vérifie que la fonction retourne {} si le fichier est absent."""
    joueurs = FootballPlayerLoader.load_all_player(str(tmp_path))
    assert joueurs == {}
