import typer

from ...core.session import is_session_active
from ...core.vault import delete_credential


app = typer.Typer()


@app.command()
def delete(credential_name: str):
    """
    🗑️ Delete a credential from Vecna's vault.

    This command removes a specified credential from the vault.
    """
    if not is_session_active():
        typer.secho(
            "No active session found. Please unlock your vault first.",
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)

    # Assuming delete_credential is a function that deletes a credential by name
    success = delete_credential(credential_name)
    if success:
        typer.secho(f"Credential '{credential_name}' deleted successfully.", fg=typer.colors.GREEN)
    else:
        typer.secho(f"Credential '{credential_name}' not found.", fg=typer.colors.RED)
