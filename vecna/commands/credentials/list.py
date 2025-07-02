import typer
from rich import print as rich_print

from ...core.session import is_session_active
from ...core.vault import list_credentials


app = typer.Typer()


@app.command()
def list():
    """
    📜 List all credentials stored in Vecna's vault.

    This command retrieves and displays all credentials in a formatted table.
    """
    if not is_session_active():
        typer.secho(
            "No active session found. Please unlock your vault first.",
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)

    credentials = list_credentials()
    if not credentials:
        typer.secho("No credentials found in the vault.", fg=typer.colors.YELLOW)
        return

    rich_print("-" * 40)
    for credential in credentials:
        rich_print("[bold cyan]Name:[/bold cyan] {}".format(credential.name))
        rich_print("[bold cyan]Username:[/bold cyan] {}".format(credential.username))
        if credential.notes:
            rich_print("[bold cyan]Notes:[/bold cyan] {}".format(credential.notes))
        if credential.tags:
            rich_print("[bold cyan]Tags:[/bold cyan] {}".format(", ".join(credential.tags)))
        rich_print("-" * 40)
