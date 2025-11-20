from collections import defaultdict
from pathlib import Path
from rich.console import Console
from rich.table import Table

from finance.storage.csv_storage import CsvStorage
from finance.models.schemas import OperationType

DB_PATH = Path("data/finance.csv")

def show_account_summary():
    console = Console()
    storage = CsvStorage(DB_PATH)
    transactions = storage.get_all()

    # Структура: place -> {currency: str, native_balance: float, rub_balance: float}
    accounts = defaultdict(lambda: {"currency": None, "native": 0.0, "rub": 0.0})

    for t in transactions:
        place = t.place

        # 1. Проверка валюты счета
        if accounts[place]["currency"] is None:
            accounts[place]["currency"] = t.currency
        elif accounts[place]["currency"] != t.currency:
            console.print(f"[bold red]Ошибка:[/bold red] На счете [yellow]{place}[/yellow] смешаны валюты: {accounts[place]['currency'].value} и {t.currency.value}")
            console.print(f"{t.title}")
            return

        amount = t.amount

        accounts[place]["native"] += amount
        accounts[place]["rub"] += amount * t.rate

    # 4. Вывод таблицы
    table = Table(title="Сводка по счетам")
    table.add_column("Счет / Место", style="cyan")
    table.add_column("Валюта", style="magenta", justify="center")
    table.add_column("Баланс (в валюте)", style="green", justify="right")
    table.add_column("Баланс (в рублях)", style="yellow", justify="right")

    total_all_rub = 0.0

    for place, data in sorted(accounts.items()):
        native_fmt = f"{data['native']:,.2f}"
        rub_fmt = f"{data['rub']:,.2f}"
        table.add_row(place, data["currency"].value, native_fmt, rub_fmt)
        total_all_rub += data["rub"]

    console.print(table)
    console.print(f"\n[bold]Итоговый капитал:[/bold] [green]{total_all_rub:,.2f} RUB[/green]")

if __name__ == "__main__":
    show_account_summary()