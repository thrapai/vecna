from typing import Annotated

import typer

from ...core.session import is_session_active
from ...core.vault import Vault
from ...models import Alias

app = typer.Typer()


@app.command()
def add(
    name: Annotated[
        str,
        typer.Argument(
            help="The name of the alias",
            show_default=False,
        ),
    ],
):
    """
    Add a new alias to the vault.
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

    command = typer.prompt("Command").strip()

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

    alias = Alias(
        name=name,
        command=command,
        notes=notes,
        tags=tags,
    )
    vault.add_alias(alias)

    typer.secho(f"Alias '{name}' added successfully.", fg=typer.colors.GREEN)
