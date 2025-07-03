import typer

from ..core.session import end_session
from ..core.vault import lock_vault

app = typer.Typer()


@app.command()
def lock():
    """
    🔒🏰Secures vault and end active session.
    """
    lock_vault()
    end_session()
    typer.secho(
        "🔒🏰 The vault is now sealed with silence...",
        fg=typer.colors.GREEN,
    )
