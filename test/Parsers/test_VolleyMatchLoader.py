import os
import csv
import pytest
from src.Parsers.MatchLoader.VolleyMatchLoader import VolleyMatchLoader


def creer_csv_matchs_hommes(dossier: str):
    """Crée un fichier volleyball_match_men.csv minimal."""
    chemin = os.path.join(dossier, "volleyball_match_men.csv")
    with open(chemin, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["date", "stage", "country_code_1", "country_code_2",
                         "set_country_1", "set_country_2"])
        writer.writerow(["2024-07-27", "Preliminary Round", "USA", "ARG", "3", "0"])
        writer.writerow(["2024-07-30", "Preliminary Round", "ITA", "EGY", "3", "0"])
    return chemin


def creer_csv_matchs_femmes(dossier: str):
    """Crée un fichier volleyball_match_women.csv minimal."""
    chemin = os.path.join(dossier, "volleyball_match_women.csv")
    with open(chemin, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["date", "stage", "country_1", "country_2",
                         "set_country_1", "set_country_2"])
        writer.writerow(["2024-07-29", "Preliminary Round", "Brazil", "Kenya", "3", "0"])
    return chemin


def test_volley_match_loader_retourne_une_liste(tmp_path):
    """Vérifie que load_all_match retourne une liste."""
    creer_csv_matchs_hommes(str(tmp_path))
    matchs = VolleyMatchLoader.load_all_match(str(tmp_path))
    assert isinstance(matchs, list)


def test_volley_match_loader_combine_hommes_et_femmes(tmp_path):
    """Vérifie que les matchs hommes et femmes sont combinés."""
    creer_csv_matchs_hommes(str(tmp_path))
    creer_csv_matchs_femmes(str(tmp_path))
    matchs = VolleyMatchLoader.load_all_match(str(tmp_path))
    # 2 matchs hommes + 1 match femmes = 3 au total
    assert len(matchs) == 3


def test_volley_match_loader_score_correct(tmp_path):
    """Vérifie que le score (nombre de sets) est correctement chargé."""
    creer_csv_matchs_hommes(str(tmp_path))
    matchs = VolleyMatchLoader.load_all_match(str(tmp_path))
    assert matchs[0].score1 == 3
    assert matchs[0].score2 == 0


def test_volley_match_loader_equipe_id(tmp_path):
    """Vérifie que l'identifiant d'équipe est le code pays."""
    creer_csv_matchs_hommes(str(tmp_path))
    matchs = VolleyMatchLoader.load_all_match(str(tmp_path))
    assert matchs[0].equipe1_id == "USA"
    assert matchs[0].equipe2_id == "ARG"


def test_volley_match_loader_saison_extraite(tmp_path):
    """Vérifie que la saison est extraite de la date."""
    creer_csv_matchs_hommes(str(tmp_path))
    matchs = VolleyMatchLoader.load_all_match(str(tmp_path))
    assert matchs[0].saison == 2024


def test_volley_match_loader_vainqueur(tmp_path):
    """Vérifie que la méthode vainqueur_id() retourne le bon gagnant."""
    creer_csv_matchs_hommes(str(tmp_path))
    matchs = VolleyMatchLoader.load_all_match(str(tmp_path))
    # USA 3 sets, ARG 0 sets → USA gagne
    assert matchs[0].vainqueur_id() == "USA"


def test_volley_match_loader_fichier_absent(tmp_path):
    """Vérifie que la fonction retourne [] si les fichiers sont absents."""
    matchs = VolleyMatchLoader.load_all_match(str(tmp_path))
    assert matchs == []
