import os
import csv
import pytest
from src.Parsers.PlayerLoader.VolleyMenPlayerLoader import VolleyMenPlayerLoader
from src.Parsers.PlayerLoader.VolleyWomenPlayerLoader import VolleyWomenPlayerLoader
from src.Parsers.PlayerLoader.VolleyballPlayerLoader import VolleyballPlayerLoader


def creer_csv_joueurs_volley_hommes(dossier: str):
    """Crée un fichier volleyball_player_men.csv minimal pour les tests."""
    chemin = os.path.join(dossier, "volleyball_player_men.csv")
    with open(chemin, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["name", "country_code", "height", "birth_date", "birth_place", "nickname"])
        writer.writerow(["FROMM Christian", "GER", "204", "1990-08-15", "Berlin", ""])
        writer.writerow(["NGAPETH Earvin", "FRA", "196", "1990-02-12", "Nice", ""])
    return chemin


def creer_csv_joueurs_volley_femmes(dossier: str):
    """Crée un fichier volleyball_player_women.csv minimal pour les tests."""
    chemin = os.path.join(dossier, "volleyball_player_women.csv")
    with open(chemin, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["name", "country_code", "height", "birth_date", "birth_place", "nickname"])
        writer.writerow(["EGONU Paola Ogechi", "ITA", "193", "1998-12-18", "Cittadella", ""])
    return chemin


def test_volley_men_loader_retourne_un_dictionnaire(tmp_path):
    """Vérifie que VolleyMenPlayerLoader retourne un dictionnaire."""
    creer_csv_joueurs_volley_hommes(str(tmp_path))
    joueurs = VolleyMenPlayerLoader.load_all_player(str(tmp_path))
    assert isinstance(joueurs, dict)


def test_volley_men_loader_genre_est_H(tmp_path):
    """Vérifie que le genre des joueurs masculins est 'H'."""
    creer_csv_joueurs_volley_hommes(str(tmp_path))
    joueurs = VolleyMenPlayerLoader.load_all_player(str(tmp_path))
    for joueur in joueurs.values():
        assert joueur.gender == "H"


def test_volley_men_loader_taille_en_cm(tmp_path):
    """Vérifie que la taille est correctement chargée en centimètres."""
    creer_csv_joueurs_volley_hommes(str(tmp_path))
    joueurs = VolleyMenPlayerLoader.load_all_player(str(tmp_path))
    assert joueurs["FROMM Christian"].height == 204


def test_volley_men_loader_pays(tmp_path):
    """Vérifie que le pays est correctement chargé."""
    creer_csv_joueurs_volley_hommes(str(tmp_path))
    joueurs = VolleyMenPlayerLoader.load_all_player(str(tmp_path))
    assert joueurs["NGAPETH Earvin"].country == "FRA"


def test_volley_women_loader_genre_est_F(tmp_path):
    """Vérifie que le genre des joueuses féminines est 'F'."""
    creer_csv_joueurs_volley_femmes(str(tmp_path))
    joueurs = VolleyWomenPlayerLoader.load_all_player(str(tmp_path))
    for joueur in joueurs.values():
        assert joueur.gender == "F"


def test_volleyball_player_loader_combine_hommes_et_femmes(tmp_path):
    """Vérifie que VolleyballPlayerLoader combine les deux fichiers."""
    creer_csv_joueurs_volley_hommes(str(tmp_path))
    creer_csv_joueurs_volley_femmes(str(tmp_path))
    joueurs = VolleyballPlayerLoader.load_all_player(str(tmp_path))
    assert len(joueurs) == 3
    assert "EGONU Paola Ogechi" in joueurs
    assert "FROMM Christian" in joueurs


def test_volley_loader_fichier_absent(tmp_path):
    """Vérifie que les loaders retournent {} si les fichiers sont absents."""
    assert VolleyMenPlayerLoader.load_all_player(str(tmp_path)) == {}
    assert VolleyWomenPlayerLoader.load_all_player(str(tmp_path)) == {}
