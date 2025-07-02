import typer
from ..core.vault import unlock_vault
from ..core.session import create_session

app = typer.Typer()


@app.command()
def unlock():
    """
    🔓📖 Unlock the encrypted vault and begin your session.
    """
    typer.echo("🧙 The Whispered One demands your incantation...")
    master = typer.prompt("Speak thy master incantation", hide_input=True)
    try:
        unlock_vault(master)
        typer.secho(
            "🔓📖  The seals break. Secrets awaken at Vecna's call.",
            fg=typer.colors.GREEN,
        )
    except ValueError:
        typer.secho(
            "The runes reject your incantation. Access denied.", fg=typer.colors.RED
        )
        raise typer.Exit(1)
    create_session()
