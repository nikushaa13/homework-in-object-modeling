from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import List

from .models import Facture


@dataclass
class CarteDeFidelite:
    client: str
    factures: List[Facture] = field(default_factory=list)
    niveau: str = field(init=False, default="Bronze")

    def __post_init__(self) -> None:
        if not self.client or not self.client.strip():
            raise ValueError("client must be non-empty")
        for f in self.factures:
            if f.client != self.client:
                raise ValueError("all invoices must belong to the card owner")
        self.niveau = self.calculer_niveau()

    def ajouter_facture(self, f: Facture) -> None:
        if f.client != self.client:
            raise ValueError("invoice client must match card owner")
        self.factures.append(f)
        self.niveau = self.calculer_niveau()

    def reset_historique(self) -> None:
        self.factures.clear()
        self.niveau = "Bronze"

    def calculer_niveau(self) -> str:
        total = sum(f.prix_vente for f in self.factures)
        if total < 200:
            return "Bronze"
        if total < 500:
            return "Argent"
        if total < 2000:
            return "Or"
        return "Or"

    def factures_entre(self, debut: date, fin: date) -> List[Facture]:
        if debut > fin:
            raise ValueError("debut must be <= fin")
        return [f for f in self.factures if debut <= f.date_vente <= fin]
