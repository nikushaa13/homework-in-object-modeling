from datetime import date

import pytest

from exercice2.src.florist.loyalty import CarteDeFidelite
from exercice2.src.florist.models import Fleur, Facture


def make_flower(price: float = 99.99, cut: date = date(2026, 1, 1)) -> Fleur:
    return Fleur(espece="Rose", date_coupe=cut, qualite="A", prix=price)


def make_invoice(client: str, sale: date, flower_count: int = 1, price: float = 99.99) -> Facture:
    bouquet = [make_flower(price=price, cut=date(2026, 1, 1)) for _ in range(flower_count)]
    return Facture(client=client, date_vente=sale, bouquet=bouquet)


def test_add_invoice_success_and_client_match() -> None:
    card = CarteDeFidelite(client="Niko")
    inv = make_invoice(client="Niko", sale=date(2026, 1, 2))
    card.ajouter_facture(inv)
    assert len(card.factures) == 1
    assert card.factures[0].client == "Niko"


def test_add_invoice_wrong_client_raises() -> None:
    card = CarteDeFidelite(client="Niko")
    inv = make_invoice(client="Other", sale=date(2026, 1, 2))
    with pytest.raises(ValueError):
        card.ajouter_facture(inv)


def test_reset_historique_clears_and_sets_bronze() -> None:
    card = CarteDeFidelite(client="Niko")
    card.ajouter_facture(make_invoice(client="Niko", sale=date(2026, 1, 2)))
    assert len(card.factures) == 1
    card.reset_historique()
    assert len(card.factures) == 0
    assert card.niveau == "Bronze"


def test_calculer_niveau_bronze_argent_or() -> None:
    card = CarteDeFidelite(client="Niko")

    card.ajouter_facture(make_invoice(client="Niko", sale=date(2026, 1, 2)))
    assert card.niveau == "Bronze"

    card.ajouter_facture(make_invoice(client="Niko", sale=date(2026, 1, 3)))
    assert card.niveau == "Argent"

    for i in range(3):
        card.ajouter_facture(make_invoice(client="Niko", sale=date(2026, 1, 4 + i)))
    assert card.niveau == "Or"


def test_factures_entre_inclusive_filtering() -> None:
    card = CarteDeFidelite(client="Niko")
    inv1 = make_invoice(client="Niko", sale=date(2026, 1, 2))
    inv2 = make_invoice(client="Niko", sale=date(2026, 1, 10))
    inv3 = make_invoice(client="Niko", sale=date(2026, 1, 20))
    card.ajouter_facture(inv1)
    card.ajouter_facture(inv2)
    card.ajouter_facture(inv3)

    res = card.factures_entre(date(2026, 1, 10), date(2026, 1, 20))
    assert [f.id for f in res] == [inv2.id, inv3.id]


def test_factures_entre_invalid_range_raises() -> None:
    card = CarteDeFidelite(client="Niko")
    with pytest.raises(ValueError):
        card.factures_entre(date(2026, 2, 1), date(2026, 1, 1))
