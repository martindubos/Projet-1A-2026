import datetime

class Player:
    def __init__(
        self,
        id,
        lastname: str,
        firstname: str,
        birthdate: datetime.date | None,
        country: str,
        hand: str = None,
        height: int = None
    ) -> None:
        self.id = id
        self.lastname = lastname
        self.firstname = firstname
        self.birthdate = birthdate
        self.country = country
        self.hand = hand
        self.height = height
        self.statistiques = {}  # { annee: {cle: valeur} }

    def ajouter_statistiques(self, annee: int, stats: dict) -> None:
        self.statistiques[annee] = stats

    def nom_complet(self) -> str:
        name_parts = filter(None, [self.firstname, self.lastname])
        return " ".join(name_parts)

    @property
    def pays(self):
        return self.country
        
    @property
    def taille(self):
        return self.height
        
    @property
    def date_naissance(self):
        return self.birthdate

    def __repr__(self):
        return f"Player({self.nom_complet()!r}, {self.country})"
