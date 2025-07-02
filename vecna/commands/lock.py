import typer
from ..core.vault import lock_vault
from ..core.session import end_session

app = typer.Typer()


@app.command()
def lock():
    """
    🔒🏰Secures vault and end active session.
    """
    lock_vault()
    end_session()
    typer.secho("🔒🏰 The vault is now sealed with silence...", fg=typer.colors.GREEN)
