import typer
from ..core.vault import create_vault, unlock_vault
from ..core.session import create_session
from ..config import VAULT_FILE

app = typer.Typer()


@app.command()
def init(
    force: bool = typer.Option(
        False, "--force", "-f", help="Overwrite existing vault if it exists"
    )
):
    """
    🔮 Begin a new arcane pact. Initializes your encrypted vault.
    """
    if VAULT_FILE.exists() and not force:
        typer.secho(
            "A vault already exists. Use --force to overwrite it.",
            fg=typer.colors.YELLOW,
        )
        raise typer.Exit()

    typer.echo("🧙 The Whispered One stirs...")

    master = typer.prompt("Craft thy master incantation", hide_input=True)
    confirm = typer.prompt("Repeat thy incantation", hide_input=True)

    if master != confirm:
        typer.secho(
            "The ritual failed — the incantations do not match.", fg=typer.colors.RED
        )
        raise typer.Exit()

    create_vault(master)
    typer.secho(
        f"🏰 A new vault has been conjured into existence.",
        fg=typer.colors.GREEN,
    )
    unlock_vault(master)
    create_session()
