from __future__ import annotations

import json
from dataclasses import asdict
from datetime import date, datetime
from pathlib import Path
from typing import List, Optional

from .models import Facture, Fleur, fleur_from_dict, fleur_to_dict


def _parse_date(value: str | date) -> date:
    if isinstance(value, date):
        return value
    return datetime.strptime(value, "%Y-%m-%d").date()


class JsonRepository:
    def __init__(self, flowers_path: Path, invoices_path: Path) -> None:
        self.flowers_path = flowers_path
        self.invoices_path = invoices_path
        self.flowers_path.parent.mkdir(parents=True, exist_ok=True)
        self.invoices_path.parent.mkdir(parents=True, exist_ok=True)

    def _read_json_list(self, path: Path) -> list:
        if not path.exists():
            return []
        text = path.read_text(encoding="utf-8").strip()
        if not text:
            return []
        return json.loads(text)

    def _write_json_list(self, path: Path, items: list) -> None:
        path.write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8")

    # ---------------- Flowers ----------------

    def list_flowers(self) -> List[Fleur]:
        data = self._read_json_list(self.flowers_path)
        return [fleur_from_dict(x) for x in data]

    def get_flower(self, flower_id: str) -> Optional[Fleur]:
        for f in self.list_flowers():
            if f.id == flower_id:
                return f
        return None

    def add_flower(self, flower: Fleur) -> Fleur:
        flowers = self._read_json_list(self.flowers_path)
        if any(x["id"] == flower.id for x in flowers):
            raise ValueError("flower id already exists")
        flowers.append(fleur_to_dict(flower))
        self._write_json_list(self.flowers_path, flowers)
        return flower

    def delete_flower(self, flower_id: str) -> None:
        flowers = self._read_json_list(self.flowers_path)
        new_flowers = [x for x in flowers if x["id"] != flower_id]
        self._write_json_list(self.flowers_path, new_flowers)

    def search_flowers_price_between(self, prix_min: float, prix_max: float) -> List[Fleur]:
        if prix_min > prix_max:
            raise ValueError("prix_min must be <= prix_max")
        return [f for f in self.list_flowers() if prix_min <= f.prix <= prix_max]

    def search_flowers_by_cut_date(self, cut_date: str | date) -> List[Fleur]:
        d = _parse_date(cut_date)
        return [f for f in self.list_flowers() if f.date_coupe == d]

    # ---------------- Invoices ----------------

    def list_invoices(self) -> List[Facture]:
        data = self._read_json_list(self.invoices_path)
        return [Facture.from_dict(x) for x in data]

    def get_invoice(self, invoice_id: str) -> Optional[Facture]:
        for inv in self.list_invoices():
            if inv.id == invoice_id:
                return inv
        return None

    def add_invoice(self, invoice: Facture) -> Facture:
        known_flowers = {f.id for f in self.list_flowers()}
        for f in invoice.bouquet:
            if f.id not in known_flowers:
                raise ValueError("invoice contains unknown flower")

        invoices = self._read_json_list(self.invoices_path)
        if any(x["id"] == invoice.id for x in invoices):
            raise ValueError("invoice id already exists")

        invoices.append(invoice.to_dict())
        self._write_json_list(self.invoices_path, invoices)
        return invoice

    def delete_invoice(self, invoice_id: str) -> None:
        invoices = self._read_json_list(self.invoices_path)
        new_invoices = [x for x in invoices if x["id"] != invoice_id]
        self._write_json_list(self.invoices_path, new_invoices)

    def invoices_by_client(self, client: str) -> List[Facture]:
        return [inv for inv in self.list_invoices() if inv.client == client]
