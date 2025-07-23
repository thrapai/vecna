from typing import Annotated

import typer

from ...core.session import is_session_active
from ...core.vault import Vault
from ...models import Credential
from ...utils import generate_password

app = typer.Typer()


@app.command()
def add(
    name: Annotated[
        str,
        typer.Argument(
            help="The name of the credential",
            show_default=False,
        ),
    ],
):
    """
    Add a new credential to the vault.
    """
    if not is_session_active():
        typer.secho(
            "No active session. Please unlock the vault first.",
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)

    try:
        vault = Vault().load()
    except Exception as e:
        typer.secho(
            "Vault is locked or inaccessible. Please unlock it first.",
            fg=typer.colors.RED,
        )
        raise typer.Exit(1) from e

    username = typer.prompt("Username (or email)").strip()

    password = typer.prompt(
        "Password (leave empty to generate a secure password)",
        default="",
        hide_input=True,
        show_default=False,
    ).strip()

    if not password:
        password = generate_password()
        typer.secho("A secure password has been generated.", fg=typer.colors.CYAN)
    else:
        confirm_password = typer.prompt("Confirm password", hide_input=True)
        if password != confirm_password:
            typer.secho("Passwords do not match.", fg=typer.colors.RED)
            raise typer.Exit(1)

    notes = typer.prompt(
        "Notes (optional)",
        default="",
        show_default=False,
    ).strip()

    tags = typer.prompt(
        "Tags (comma-separated, optional)",
        default="",
        show_default=False,
    ).strip()
    tags = [tag.strip() for tag in tags.split(",") if tag.strip()] if tags else []

    credential = Credential(
        name=name,
        username=username,
        password=password,
        notes=notes,
        tags=tags,
    )
    vault.add_credential(credential)

    typer.secho(f"Credential '{name}' added successfully.", fg=typer.colors.GREEN)
