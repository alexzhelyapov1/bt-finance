#!/usr/bin/env python3
from pathlib import Path
from finance.cli import app, ctx
from finance.core.services import FinanceService
from finance.storage.csv_storage import CsvStorage

DB_PATH = Path("data/finance.csv")

def main():
    storage = CsvStorage(DB_PATH)
    service = FinanceService(storage)
    ctx.service = service
    app()

if __name__ == "__main__":
    main()