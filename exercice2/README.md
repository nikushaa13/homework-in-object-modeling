# Exercise 2 — Florist System (JSON + REST API)

## What this project does
This exercise implements a simple florist management system:
- Flowers (`Fleur`)
- Invoices (`Facture`)
- Loyalty card (`CarteDeFidelite`) + unit tests
- JSON files used as a lightweight database
- REST API built with FastAPI

## Business rules implemented
- A flower price must end with `.99` (e.g., 1.99, 4.99)
- An invoice sale date cannot be earlier than the cut date of any flower in the bouquet
- Invoice price = sum of flower prices + 20% VAT
- Loyalty card can only contain invoices of the same client
- Loyalty level depends on total invoice amount:
  - Bronze: total < 200
  - Argent: total < 500
  - Or: total < 2000 (and above)

## Structure
- `src/florist/models.py` : `Fleur`, `Facture` + validations and pricing rules
- `src/florist/loyalty.py` : `CarteDeFidelite`
- `src/florist/repositories.py` : JSON persistence and search helpers
- `src/florist/api.py` : REST API (FastAPI)
- `tests/test_loyalty_card.py` : unit tests for `CarteDeFidelite`
- `data/flowers.json` and `data/invoices.json` : JSON “database” files

## Install
From repository root:

```bash
py -m pip install pytest fastapi uvicorn
