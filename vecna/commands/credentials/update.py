from typing import Optional

import typer
from typing_extensions import Annotated

from ...core.session import is_session_active
from ...core.vault import (
    get_credential,
    update_credential,
)
from ...models import (
    Credential,
    UpdateCredential,
)
from ...utils import generate_password


app = typer.Typer()


def prompt_for_updates(current: Credential) -> UpdateCredential:
    """
    Prompt the user for updates to an existing credential.

    This function interactively asks the user for new values for each field of the credential.
    For each field, the current value is used as the default if the user provides no input.
    For passwords, the user can either provide a new password or have one generated automatically.

    Args:
        current: The existing Credential object to be updated

    Returns:
        UpdateCredential: An object containing the updated credential information

    Raises:
        typer.Exit: If the password confirmation doesn't match the entered password
    """
    new_cred = UpdateCredential(name=current.name)

    new_name = typer.prompt("New credential name", default=current.name, show_default=False).strip()
    if new_name != current.name:
        new_cred.new_name = new_name

    new_cred.username = typer.prompt(
        "New username", default=current.username, show_default=False
    ).strip()

    password = typer.prompt(
        "New Password (leave empty to generate a secure password)",
        default="",
        hide_input=True,
        show_default=False,
    ).strip()
    if not password:
        password = generate_password()
        typer.secho("Generated secure password.", fg=typer.colors.CYAN)
    else:
        confirm = typer.prompt("Confirm password", hide_input=True)
        if confirm != password:
            typer.secho("Passwords do not match.", fg=typer.colors.RED)
            raise typer.Exit(1)
    new_cred.password = password

    new_cred.notes = typer.prompt("Notes", default=current.notes or "", show_default=False).strip()

    tags_input = typer.prompt(
        "Tags (comma-separated)", default=",".join(current.tags or []), show_default=False
    ).strip()
    new_cred.tags = [tag.strip() for tag in tags_input.split(",") if tag.strip()]

    return new_cred


@app.command()
def update(
    name: Annotated[str, typer.Argument(help="Name of the credential", show_default=False)],
    new_name: Annotated[
        Optional[str],
        typer.Option("--new-name", help="New credential name", show_default=False),
    ] = None,
    username: Annotated[
        Optional[str], typer.Option("--username", "-u", help="Updated username", show_default=False)
    ] = None,
    password: Annotated[
        Optional[str], typer.Option("--password", "-p", help="Updated password", show_default=False)
    ] = None,
    autogenerate_pwd: Annotated[
        bool,
        typer.Option(
            "--autogenerate-pwd", "-a", help="Generate a secure password", show_default=False
        ),
    ] = False,
    notes: Annotated[
        Optional[str], typer.Option("--notes", "-n", help="Updated notes", show_default=False)
    ] = None,
    tags: Annotated[
        Optional[str],
        typer.Option("--tags", "-t", help="Comma-separated updated tags", show_default=False),
    ] = None,
    interactive: Annotated[
        bool,
        typer.Option("--interactive", "-i", help="Prompt interactively instead of using flags"),
    ] = False,
):
    """
    🔄 Update an existing credential in your vault.

    You can use either --interactive mode or individual options to update fields.
    """
    if not is_session_active():
        typer.secho("No active session. Please unlock your vault.", fg=typer.colors.RED)
        raise typer.Exit(1)

    current_cred = get_credential(name)
    if current_cred is None:
        typer.secho(f"Credential '{name}' not found.", fg=typer.colors.YELLOW)
        raise typer.Exit(1)

    if interactive:
        new_cred = prompt_for_updates(current_cred)
    else:
        if not any([new_name, username, password, autogenerate_pwd, notes, tags]):
            typer.secho("Nothing to update. Use flags or --interactive.", fg=typer.colors.YELLOW)
            raise typer.Exit(0)

        new_cred = UpdateCredential(name=name)
        new_cred.new_name = new_name
        new_cred.username = username

        if autogenerate_pwd:
            password = generate_password()
            typer.secho("Generated secure password.", fg=typer.colors.CYAN)
            new_cred.password = password
        elif password:
            new_cred.password = password

        new_cred.notes = notes
        if tags:
            new_cred.tags = [tag.strip() for tag in tags.split(",") if tag.strip()]

    if update_credential(new_cred):
        typer.secho(f"Credential '{name}' updated successfully.", fg=typer.colors.GREEN)
    else:
        typer.secho(f"Failed to update credential '{name}'.", fg=typer.colors.RED)
