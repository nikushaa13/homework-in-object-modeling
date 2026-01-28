from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import List, Optional

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel

from .models import Facture, Fleur
from .repositories import JsonRepository


DATA_DIR = Path("exercice2/data")
repo = JsonRepository(DATA_DIR / "flowers.json", DATA_DIR / "invoices.json")

app = FastAPI(title="Florist API", version="1.0")


class FleurIn(BaseModel):
    espece: str
    date_coupe: date
    qualite: str
    prix: float


class FleurOut(FleurIn):
    id: str


class FactureIn(BaseModel):
    client: str
    date_vente: date
    bouquet_ids: List[str]


class FactureOut(BaseModel):
    id: str
    client: str
    date_vente: date
    prix_vente: float
    bouquet: List[FleurOut]


def _fleur_to_out(f: Fleur) -> FleurOut:
    return FleurOut(
        id=f.id,
        espece=f.espece,
        date_coupe=f.date_coupe,
        qualite=f.qualite,
        prix=f.prix,
    )


@app.get("/flowers", response_model=List[FleurOut])
def list_flowers() -> List[FleurOut]:
    return [_fleur_to_out(f) for f in repo.list_flowers()]


@app.post("/flowers", response_model=FleurOut, status_code=201)
def create_flower(payload: FleurIn) -> FleurOut:
    try:
        f = Fleur(
            espece=payload.espece,
            date_coupe=payload.date_coupe,
            qualite=payload.qualite,
            prix=payload.prix,
        )
        repo.add_flower(f)
        return _fleur_to_out(f)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.delete("/flowers/{flower_id}", status_code=204)
def delete_flower(flower_id: str) -> None:
    repo.delete_flower(flower_id)
    return None


@app.get("/flowers/search/price", response_model=List[FleurOut])
def search_flowers_price(
    prix_min: float = Query(..., ge=0),
    prix_max: float = Query(..., ge=0),
) -> List[FleurOut]:
    try:
        res = repo.search_flowers_price_between(prix_min, prix_max)
        return [_fleur_to_out(f) for f in res]
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/flowers/search/cut-date", response_model=List[FleurOut])
def search_flowers_cut_date(d: date) -> List[FleurOut]:
    res = repo.search_flowers_by_cut_date(d)
    return [_fleur_to_out(f) for f in res]


@app.get("/invoices", response_model=List[FactureOut])
def list_invoices(client: Optional[str] = None) -> List[FactureOut]:
    invoices = repo.invoices_by_client(client) if client else repo.list_invoices()
    out: List[FactureOut] = []
    for inv in invoices:
        out.append(
            FactureOut(
                id=inv.id,
                client=inv.client,
                date_vente=inv.date_vente,
                prix_vente=inv.prix_vente,
                bouquet=[_fleur_to_out(f) for f in inv.bouquet],
            )
        )
    return out


@app.post("/invoices", response_model=FactureOut, status_code=201)
def create_invoice(payload: FactureIn) -> FactureOut:
    bouquet: List[Fleur] = []
    for fid in payload.bouquet_ids:
        f = repo.get_flower(fid)
        if f is None:
            raise HTTPException(status_code=400, detail="unknown flower id in bouquet")
        bouquet.append(f)

    try:
        inv = Facture(client=payload.client, date_vente=payload.date_vente, bouquet=bouquet)
        repo.add_invoice(inv)
        return FactureOut(
            id=inv.id,
            client=inv.client,
            date_vente=inv.date_vente,
            prix_vente=inv.prix_vente,
            bouquet=[_fleur_to_out(f) for f in inv.bouquet],
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.delete("/invoices/{invoice_id}", status_code=204)
def delete_invoice(invoice_id: str) -> None:
    repo.delete_invoice(invoice_id)
    return None
