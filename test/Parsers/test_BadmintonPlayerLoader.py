import os
import tempfile
import csv
import pytest
from src.Parsers.PlayerLoader.BadmintonPlayerLoader import BadmintonPlayerLoader


def creer_csv_joueurs_badminton(dossier: str):
    """Crée un fichier player.csv minimal pour les tests."""
    chemin = os.path.join(dossier, "player.csv")
    with open(chemin, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["name", "country", "continent"])
        writer.writerow(["Akane Yamaguchi", "Japan", "Asia"])
        writer.writerow(["Viktor Axelsen", "Denmark", "Europe"])
    return chemin


def test_badminton_player_loader_retourne_un_dictionnaire(tmp_path):
    """Vérifie que load_all_player retourne bien un dictionnaire."""
    creer_csv_joueurs_badminton(str(tmp_path))
    joueurs = BadmintonPlayerLoader.load_all_player(str(tmp_path))
    assert isinstance(joueurs, dict)


def test_badminton_player_loader_charge_le_bon_nombre_de_joueurs(tmp_path):
    """Vérifie que tous les joueurs du CSV sont chargés."""
    creer_csv_joueurs_badminton(str(tmp_path))
    joueurs = BadmintonPlayerLoader.load_all_player(str(tmp_path))
    assert len(joueurs) == 2


def test_badminton_player_loader_id_est_le_nom(tmp_path):
    """Vérifie que l'identifiant d'un joueur est son nom."""
    creer_csv_joueurs_badminton(str(tmp_path))
    joueurs = BadmintonPlayerLoader.load_all_player(str(tmp_path))
    assert "Akane Yamaguchi" in joueurs
    assert joueurs["Akane Yamaguchi"].id == "Akane Yamaguchi"


def test_badminton_player_loader_charge_le_pays(tmp_path):
    """Vérifie que le pays du joueur est correctement chargé."""
    creer_csv_joueurs_badminton(str(tmp_path))
    joueurs = BadmintonPlayerLoader.load_all_player(str(tmp_path))
    assert joueurs["Viktor Axelsen"].country == "Denmark"


def test_badminton_player_loader_fichier_absent(tmp_path):
    """Vérifie que la fonction retourne {} si le fichier CSV est absent."""
    joueurs = BadmintonPlayerLoader.load_all_player(str(tmp_path))
    assert joueurs == {}
