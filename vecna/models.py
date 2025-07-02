from typing import Optional

from pydantic import (
    BaseModel,
    Field,
)
from typer import secho


class Session(BaseModel):
    """
    Represents a user session in the Vecna CLI.

    Attributes:
        unlocked (bool): Indicates if the session is currently unlocked.
        timestamp (str): ISO formatted timestamp of when the session was created or last modified.
    """

    unlocked: bool = Field(
        default=True,
        description="Indicates if the session is currently unlocked.",
    )
    timestamp: str = Field(
        ...,
        description="ISO formatted timestamp of when the session was created or last modified.",
    )


class Credential(BaseModel):
    """
    Represents a credential stored in the Vecna CLI vault.

    Attributes:
        name (str): The name of the credential.
        value (str): The value of the credential, which is encrypted.
        metadata (dict): Additional metadata associated with the credential.
    """

    name: str = Field(
        ...,
        description="The name of the credential.",
    )
    username: str = Field(
        ...,
        description="The username associated with the credential.",
    )
    password: str = Field(
        ...,
        description="The password associated with the credential.",
    )
    notes: Optional[str] = Field(
        "",
        description="Optional notes associated with the credential.",
    )
    tags: Optional[list[str]] = Field(
        None,
        description="Optional tags associated with the credential.",
    )

    def __str__(self):
        return secho(
            f"Credential(name={self.name}, username={self.username},"
            f" notes={self.notes}), tags={self.tags}",
            fg="blue",
        )
