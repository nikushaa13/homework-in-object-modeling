from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from typing import List
from uuid import uuid4


def _parse_date(value: str | date) -> date:
    if isinstance(value, date):
        return value
    return datetime.strptime(value, "%Y-%m-%d").date()


def _is_price_ending_99(value: float) -> bool:
    cents = int(round(value * 100))
    return cents % 100 == 99


@dataclass(frozen=True)
class Fleur:
    espece: str
    date_coupe: date
    qualite: str
    prix: float
    id: str = field(default_factory=lambda: str(uuid4()))

    def __post_init__(self) -> None:
        if not self.espece or not self.espece.strip():
            raise ValueError("espece must be non-empty")
        if not self.qualite or not self.qualite.strip():
            raise ValueError("qualite must be non-empty")
        if self.prix <= 0:
            raise ValueError("prix must be positive")
        if not _is_price_ending_99(self.prix):
            raise ValueError("prix must end with .99")


@dataclass
class Facture:
    client: str
    date_vente: date
    bouquet: List[Fleur]
    id: str = field(default_factory=lambda: str(uuid4()))
    prix_vente: float = field(init=False)

    TVA: float = 0.20

    def __post_init__(self) -> None:
        if not self.client or not self.client.strip():
            raise ValueError("client must be non-empty")
        if self.bouquet is None or len(self.bouquet) == 0:
            raise ValueError("bouquet must contain at least one flower")

        for f in self.bouquet:
            if self.date_vente < f.date_coupe:
                raise ValueError("date_vente cannot be earlier than date_coupe of bouquet flowers")

        self.prix_vente = self.calculer_prix_vente()

    def calculer_prix_vente(self) -> float:
        total = sum(f.prix for f in self.bouquet)
        total_ttc = total * (1.0 + self.TVA)
        return round(total_ttc, 2)

    @staticmethod
    def from_dict(data: dict) -> "Facture":
        bouquet = [
            Fleur(
                id=f["id"],
                espece=f["espece"],
                date_coupe=_parse_date(f["date_coupe"]),
                qualite=f["qualite"],
                prix=float(f["prix"]),
            )
            for f in data["bouquet"]
        ]
        obj = Facture(
            id=data.get("id", str(uuid4())),
            client=data["client"],
            date_vente=_parse_date(data["date_vente"]),
            bouquet=bouquet,
        )
        return obj

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "client": self.client,
            "date_vente": self.date_vente.isoformat(),
            "bouquet": [
                {
                    "id": f.id,
                    "espece": f.espece,
                    "date_coupe": f.date_coupe.isoformat(),
                    "qualite": f.qualite,
                    "prix": f.prix,
                }
                for f in self.bouquet
            ],
            "prix_vente": self.prix_vente,
        }


def fleur_from_dict(data: dict) -> Fleur:
    return Fleur(
        id=data.get("id", str(uuid4())),
        espece=data["espece"],
        date_coupe=_parse_date(data["date_coupe"]),
        qualite=data["qualite"],
        prix=float(data["prix"]),
    )


def fleur_to_dict(f: Fleur) -> dict:
    return {
        "id": f.id,
        "espece": f.espece,
        "date_coupe": f.date_coupe.isoformat(),
        "qualite": f.qualite,
        "prix": f.prix,
    }
