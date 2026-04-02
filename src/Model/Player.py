from typing import Union
from src.Common.utils import parse_boolean
import datetime


class Player:
    def __init__(
        self,
        lastname: str,
        firstname: str,
        birthdate: datetime.date | None,
        country: str,
        hand: str,
        height: int | None
    ) -> None:
        self.lastname = lastname
        self.firstname = firstname
        self.birthdate = birthdate
        self.country = country
        self.hand = hand
        self.height = height
        self.statistiques = {}

    def calculer_nombre_tournois_gagnes() -> pd.Series:

    list_player = []
    with open(os.path.join(os.path.join("")))
