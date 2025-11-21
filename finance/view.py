from rich.console import Console
from rich.table import Table
from rich import box
from collections import defaultdict
from .models import OperationType, Currency

console = Console()

def render_table(transactions, title="Транзакции"):
    table = Table(title=title, box=box.SIMPLE)
    table.add_column("Дата", style="cyan", no_wrap=True)
    table.add_column("Тип", style="dim")
    table.add_column("Название", style="white")
    table.add_column("Сумма", justify="right")
    table.add_column("Сумма (р)", justify="right")
    table.add_column("Место", style="blue")
    table.add_column("Кат.", style="yellow")
    
    for t in transactions:
        color = "red" if t.amount < 0 else "green"
        table.add_row(
            t.date.strftime("%Y-%m-%d"),
            t.op_type.name[:3],
            t.title,
            f"[{color}]{t.amount:+.2f} {t.currency.value}[/{color}]",
            f"[{color}]{t.amount * t.rate:+.2f} {Currency.RUB}[/{color}]",
            t.place,
            t.category or ""
        )
    console.print(table)

def render_balance(transactions):
    balances = defaultdict(lambda: {"native": 0.0, "rub": 0.0, "curr": ""})
    total_rub = 0.0

    for t in transactions:
        balances[t.place]["native"] += t.amount
        balances[t.place]["rub"] += t.amount * t.rate
        balances[t.place]["curr"] = t.currency.value
        total_rub += t.amount * t.rate

    table = Table(title="Баланс по счетам", box=box.SIMPLE)
    table.add_column("Счет", style="cyan")
    table.add_column("Баланс", justify="right", style="green")
    table.add_column("В рублях", justify="right", style="yellow")

    for place, data in sorted(balances.items()):
        table.add_row(
            place,
            f"{data['native']:,.2f} {data['curr']}",
            f"{data['rub']:,.2f} ₽"
        )
    
    console.print(table)
    console.print(f"[bold]Всего:[/bold] [green]{total_rub:,.2f} RUB[/green]")