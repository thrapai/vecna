from typing import Annotated

import typer

from ...core.session import is_session_active
from ...core.vault import add_credential
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
    🗝️ Add a new credential to your vault.
    """
    if not is_session_active():
        typer.secho(
            "No active session found. Please unlock your vault first.",
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)

    username = typer.prompt("Username (or email)").strip()

    password = typer.prompt(
        "Password (leave empty to generate a secure password)",
        default="",
        hide_input=True,
        show_default=False,
    ).strip()
    if not password:
        password = generate_password()
        typer.secho(
            "Generated secure password.",
            fg=typer.colors.CYAN,
        )
    else:
        password = password.strip()
        confirm_password = typer.prompt(
            "Confirm Password",
            hide_input=True,
        )
        if password != confirm_password:
            typer.secho(
                "Passwords do not match.",
                fg=typer.colors.RED,
            )
            raise typer.Exit(1)

    notes = typer.prompt(
        "Notes (optional)",
        default="",
        show_default=False,
    ).strip()
    notes = "" if not notes else notes

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
    add_credential(credential)
    typer.secho(
        f"Credential '{name}' added successfully!",
        fg=typer.colors.GREEN,
    )
