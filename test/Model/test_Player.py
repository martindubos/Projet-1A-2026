import datetime
from src.Model.Player import Player


def test_player_creation_attributs():
    """Vérifie que les attributs d'un Player sont correctement initialisés."""
    joueur = Player(
        id=1,
        lastname="Zidane",
        firstname="Zinedine",
        birthdate=datetime.date(1972, 6, 23),
        country="FRA",
        height=185,
        gender="H"
    )
    assert joueur.id == 1
    assert joueur.lastname == "Zidane"
    assert joueur.firstname == "Zinedine"
    assert joueur.birthdate == datetime.date(1972, 6, 23)
    assert joueur.country == "FRA"
    assert joueur.height == 185
    assert joueur.gender == "H"
    assert joueur.statistiques == {}


def test_player_nom_complet():
    """Vérifie que nom_complet() gère bien les prénoms vides."""
    joueur1 = Player(id=1, lastname="Mbappe", firstname="Kylian", birthdate=None, country="FRA")
    assert joueur1.nom_complet() == "Kylian Mbappe"

    joueur2 = Player(id=2, lastname="Lionel Messi", firstname="", birthdate=None, country="ARG")
    assert joueur2.nom_complet() == "Lionel Messi"


def test_player_properties():
    """Vérifie que les properties renvoient les bonnes valeurs."""
    joueur = Player(
        id=3,
        lastname="Curry",
        firstname="Stephen",
        birthdate=datetime.date(1988, 3, 14),
        country="USA",
        height=188,
        gender="M"
    )
    assert joueur.pays == "USA"
    assert joueur.taille == 188
    assert joueur.date_naissance == datetime.date(1988, 3, 14)
    assert joueur.sexe == "M"


def test_player_ajouter_statistiques():
    """Vérifie que ajouter_statistiques fonctionne."""
    joueur = Player(id=4, lastname="Nadal", firstname="Rafael", birthdate=None, country="ESP")
    joueur.ajouter_statistiques(2022, {"Victoires": 40})
    assert 2022 in joueur.statistiques
    assert joueur.statistiques[2022]["Victoires"] == 40
