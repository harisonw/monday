"""Rich terminal output — progress display and summary tables for the live demo."""
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.text import Text
from rich import box

from src.models import RiskAssessment, OnboardingSummary

console = Console(force_terminal=False, force_jupyter=False)

RISK_COLORS = {
    "Low":    "green",
    "Medium": "yellow",
    "High":   "red",
}

COMPLEXITY_COLORS = {
    "Standard": "green",
    "Moderate": "yellow",
    "Complex":  "red",
}

RISK_ICONS = {
    "Low":    "🟢",
    "Medium": "🟡",
    "High":   "🔴",
}


def print_header():
    console.print()
    console.rule("[bold cyan]Crestview Capital Group — AI Client Intake Pipeline[/bold cyan]")
    console.print()


def print_step(step_num: int, title: str):
    console.print()
    console.rule(f"[bold white]STEP {step_num}: {title}[/bold white]")
    console.print()


def print_ingest_result(created: int, skipped: int, subitems_added: int):
    console.print(Panel(
        f"[green]✓ Created:[/green] [bold]{created}[/bold] new items\n"
        f"[yellow]⟳ Skipped:[/yellow] [bold]{skipped}[/bold] already on board (dedup)\n"
        f"[cyan]+ Subitems added:[/cyan] [bold]{subitems_added}[/bold] subitem sets created",
        title="[bold]Ingestion Complete[/bold]",
        border_style="cyan",
    ))


def print_application_result(
    app: dict,
    risk: RiskAssessment,
    summary: OnboardingSummary,
    index: int,
    total: int,
):
    risk_color = RISK_COLORS[risk.risk_level]
    risk_icon = RISK_ICONS[risk.risk_level]

    flags_str = ", ".join(risk.compliance_flags) if risk.compliance_flags else "None"
    actions_str = "\n  ".join(f"• {a}" for a in risk.recommended_actions[:3])
    next_steps_str = "\n  ".join(f"• {s}" for s in summary.next_steps[:3])

    content = (
        f"[dim]Application:[/dim] {app['application_id']}  |  "
        f"[dim]AUM:[/dim] ${app['estimated_aum']:,.0f}  |  "
        f"[dim]Type:[/dim] {app['client_type']}\n\n"
        f"[bold]Risk:[/bold] [{risk_color}]{risk_icon} {risk.risk_level} (score: {risk.risk_score}/100)[/{risk_color}]  "
        f"| [bold]EDD:[/bold] {'[red]Yes[/red]' if risk.requires_enhanced_due_diligence else '[green]No[/green]'}\n"
        f"[dim]Flags:[/dim] {flags_str}\n\n"
        f"[bold]Complexity:[/bold] {summary.complexity_rating}  "
        f"| [bold]Est. Days:[/bold] {summary.estimated_onboarding_days}  "
        f"| [bold]Priority:[/bold] {summary.priority}\n\n"
        f"[bold]Compliance Actions:[/bold]\n  {actions_str}\n\n"
        f"[bold]Ops Next Steps:[/bold]\n  {next_steps_str}"
    )

    console.print(Panel(
        content,
        title=f"[bold {risk_color}][{index}/{total}] {app['client_name']}[/bold {risk_color}]",
        border_style=risk_color,
        padding=(0, 1),
    ))


def print_summary_table(results: list[dict]):
    """Print the final summary table of all processed applications."""
    console.print()
    console.rule("[bold cyan]Pipeline Complete — Summary[/bold cyan]")
    console.print()

    table = Table(
        box=box.ROUNDED,
        show_header=True,
        header_style="bold cyan",
        border_style="dim",
        show_lines=True,
    )

    table.add_column("App ID", style="dim", width=16)
    table.add_column("Client", width=30)
    table.add_column("Risk", width=8, justify="center")
    table.add_column("Score", width=6, justify="right")
    table.add_column("EDD", width=5, justify="center")
    table.add_column("Complexity", width=10, justify="center")
    table.add_column("Days", width=5, justify="right")
    table.add_column("Priority", width=9, justify="center")
    table.add_column("Board", width=8, justify="center")

    for r in results:
        risk = r.get("risk_assessment", {})
        summ = r.get("onboarding_summary", {})
        risk_level = risk.get("risk_level", "?")
        color = RISK_COLORS.get(risk_level, "white")
        icon = RISK_ICONS.get(risk_level, "?")

        edd = "✓" if risk.get("requires_enhanced_due_diligence") else "—"
        board_status = "[green]✓[/green]" if r.get("monday_item_id") else "[red]✗[/red]"

        table.add_row(
            r["application_id"],
            r["client_name"][:28] + ("…" if len(r["client_name"]) > 28 else ""),
            Text(f"{icon} {risk_level}", style=color),
            str(risk.get("risk_score", "?")),
            f"[red]{edd}[/red]" if edd == "✓" else edd,
            summ.get("complexity_rating", "?"),
            str(summ.get("estimated_onboarding_days", "?")),
            summ.get("priority", "?"),
            board_status,
        )

    console.print(table)

    # Stats
    total = len(results)
    high_risk = sum(1 for r in results if r.get("risk_assessment", {}).get("risk_level") == "High")
    edd_required = sum(1 for r in results if r.get("risk_assessment", {}).get("requires_enhanced_due_diligence"))
    board_ok = sum(1 for r in results if r.get("monday_item_id"))

    console.print(
        f"\n[bold]Total processed:[/bold] {total}  "
        f"| [red]High risk:[/red] {high_risk}  "
        f"| [red]EDD required:[/red] {edd_required}  "
        f"| [green]Board updated:[/green] {board_ok}/{total}\n"
    )


def make_progress() -> Progress:
    return Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        console=console,
        transient=False,
        disable=False,
    )
