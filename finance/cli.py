import typer
from datetime import datetime
from typing import List, Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from finance.core.services import FinanceService
from finance.models.schemas import Currency, OperationType

console = Console()
app = typer.Typer(name="finance", no_args_is_help=True)

class AppContext:
    service: FinanceService

ctx = AppContext()

@app.command("add")
def add_transaction(
    title: str = typer.Argument(..., help="Название операции"),
    amount: float = typer.Argument(..., help="Сумма"),
    op_type: OperationType = typer.Option(..., "--type", "-t", help="Тип операции"),
    place: str = typer.Option("Cash", "--place", "-p", help="Место/Счет"),
    currency: Currency = typer.Option(Currency.RUB, "--currency", "-c", help="Валюта"),
    rate: float = typer.Option(1.0, "--rate", "-r", help="Курс к рублю"),
    category: Optional[str] = typer.Option(None, "--cat", help="Категория (для трат)"),
    tags: Optional[str] = typer.Option(None, "--tags", help="Теги через запятую"),
    # Добавили опцию даты
    date: Optional[datetime] = typer.Option(None, "--date", "-d", help="Дата (YYYY-MM-DD HH:MM:SS)")
):
    tags_list = [t.strip() for t in tags.split(",")] if tags else []

    try:
        # Передаем date в сервис
        t = ctx.service.add_transaction(
            title=title, place=place, amount=amount, currency=currency,
            op_type=op_type, category=category, rate=rate, tags=tags_list,
            date=date
        )
        console.print(f"[bold green]Запись добавлена:[/bold green] {t.title} ({t.amount} {t.currency.value}) от {t.date}")
    except ValueError as e:
        console.print(f"[bold red]Ошибка:[/bold red] {e}")

@app.command("list")
def list_transactions(limit: int = typer.Option(10, help="Количество последних записей")):
    txs = ctx.service.get_history()[:limit]
    table = Table(title="История операций")
    table.add_column("Дата", style="cyan", no_wrap=True)
    table.add_column("Тип", style="magenta")
    table.add_column("Название", style="white")
    table.add_column("Сумма", style="green")
    table.add_column("Место", style="blue")
    table.add_column("Категория", style="yellow")

    for t in txs:
        date_str = t.date.strftime("%Y-%m-%d %H:%M")
        amount_str = f"{t.amount} {t.currency.value}"
        table.add_row(date_str, t.op_type.value, t.title, amount_str, t.place, t.category or "-")
    
    console.print(table)

@app.command("balance")
def show_balance():
    data = ctx.service.calculate_balance()
    
    content = f"[bold]Общий баланс (RUB eq):[/bold] [green]{data['total_rub_eq']:.2f} ₽[/green]\n\n"
    content += "[bold]По валютам:[/bold]\n"
    for curr, val in data['currencies'].items():
        color = "green" if val >= 0 else "red"
        content += f"  {curr}: [{color}]{val:.2f}[/{color}]\n"
        
    console.print(Panel(content, title="Финансовый отчет", border_style="cyan"))