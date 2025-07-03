from typing import Annotated

import typer
from rich import print as rich_print

from ...core.session import is_session_active
from ...core.vault import get_credential
from ...utils import copy_to_clipboard

app = typer.Typer()


@app.command()
def get(
    name: Annotated[
        str,
        typer.Argument(
            help="The name of the credential",
            show_default=False,
        ),
    ],
    username: Annotated[
        bool,
        typer.Option(
            "--username",
            "-u",
            help="Show the username",
        ),
    ] = False,
    password: Annotated[
        bool,
        typer.Option(
            "--password",
            "-p",
            help="Show the password in plain text",
        ),
    ] = False,
    details: Annotated[
        bool,
        typer.Option(
            "--details",
            "-d",
            help="Show detailed JSON output",
        ),
    ] = False,
):
    """
    📜 Retrieve a secret from Vecna's vault.

    By default, the password is copied to your clipboard without displaying it.

    Use flags to reveal the password, view the username, or show full credential details.
    """
    if not is_session_active():
        typer.secho(
            "No active session found. Please unlock your vault first.",
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)

    credential = get_credential(name)

    if credential is None:
        typer.secho(
            f"Credential '{name}' not found.",
            fg=typer.colors.YELLOW,
        )
        raise typer.Exit(1)

    if details:
        rich_print(credential.model_dump_json(indent=2))
        return

    if username:
        typer.secho(
            f"{credential.username}",
            fg=typer.colors.CYAN,
        )
        return

    if password:
        typer.secho(
            f"{credential.password}",
            fg=typer.colors.CYAN,
        )
        return

    if not password:
        copied = copy_to_clipboard
        if not copied(credential.password):
            typer.secho(
                "Failed to copy password to clipboard. Run command with --password to display it.",
                fg=typer.colors.YELLOW,
            )
            return
        typer.secho(
            "Password copied to clipboard.",
            fg=typer.colors.GREEN,
        )
    return
