from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich import box

from finance.storage.csv_storage import CsvStorage
from finance.models.schemas import OperationType

DB_PATH = Path("data/finance.csv")
NAME='RMB Наличка'

def show_name_statement():
    console = Console()
    storage = CsvStorage(DB_PATH)
    
    all_txs = storage.get_all()
    name_txs = [t for t in all_txs if t.place == NAME]
    
    name_txs.sort(key=lambda x: x.date)

    table = Table(title=f"Выписка по счету {NAME}", box=box.SIMPLE)
    table.add_column("Дата", style="cyan", no_wrap=True)
    table.add_column("Название", style="white")
    table.add_column("Категория", style="blue")
    table.add_column("Изменение", justify="right")
    table.add_column("Баланс", justify="right", style="bold yellow")

    running_balance = 0.0

    for t in name_txs:
        if t.op_type in [OperationType.SPEND, OperationType.LENT]:
            change = -t.amount
            color = "red"
        else:
            change = t.amount
            color = "green"

        running_balance += change
        
        date_str = t.date.strftime("%Y-%m-%d %H:%M")
        change_str = f"[{color}]{change:+.2f}[/{color}]"
        balance_str = f"{running_balance:,.2f}"

        table.add_row(
            date_str, 
            t.title, 
            t.category or "-", 
            change_str, 
            balance_str
        )

    console.print(table)
    currency = name_txs[0].currency.value if name_txs else ""
    console.print(f"\n[bold]Текущий остаток:[/bold] [yellow]{running_balance:,.2f} {currency}[/yellow]")

if __name__ == "__main__":
    show_name_statement()