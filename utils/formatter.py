from rich.table import Table
from rich.console import Console

def print_cost_report(data, total):
    console = Console()
    table = Table(title="AWS Free Tier Cost Report")

    table.add_column("Service", style="cyan", justify="left")
    table.add_column("Cost ($)", style="magenta", justify="right")

    for service, cost in sorted(data, key=lambda x: -x[1]):
        emoji = "⚠️" if cost > 0 else "✅"
        table.add_row(f"{emoji} {service}", f"{cost:.2f}")

    table.add_row("💰 TOTAL", f"{total:.2f}")
    console.print(table)
