import json
from dataclasses import (
    asdict,
    dataclass,
    field,
)
from datetime import datetime


@dataclass
class Session:
    """
    Represents a user session in the Vecna CLI.

    Attributes:
        unlocked (bool): Indicates if the session is currently unlocked.
        timestamp (str): ISO formatted timestamp of when the session was created or last modified.
    """

    unlocked: bool = field(
        default=True,
        metadata={"description": "Indicates if the session is currently unlocked."},
    )
    timestamp: str = field(
        default_factory=lambda: datetime.utcnow().isoformat(),
        metadata={
            "description": (
                "ISO formatted timestamp of when the session was created or last modified."
            )
        },
    )


@dataclass
class Credential:
    """
    Represents a credential stored in the Vecna CLI vault.

    Attributes:
        name (str): The name of the credential.
        username (str): The username associated with the credential.
        password (str): The password associated with the credential.
        notes (Optional[str]): Optional notes associated with the credential.
        tags (Optional[List[str]]): Optional tags associated with the credential.
    """

    name: str = field(metadata={"description": "The name of the credential."})
    username: str = field(
        metadata={"description": "The username associated with the credential."}
    )
    password: str = field(
        metadata={"description": "The password associated with the credential."}
    )
    notes: str | None = field(
        default="",
        metadata={"description": "Optional notes associated with the credential."},
    )
    tags: list[str] | None = field(
        default=None,
        metadata={"description": "Optional tags associated with the credential."},
    )

    def model_dump_json(self, indent: int = 2) -> str:
        """
        Dumps the credential as a JSON string with indentation.

        Args:
            indent (int): The number of spaces to use for indentation.

        Returns:
            str: The JSON representation of the credential.
        """
        return json.dumps(asdict(self), indent=indent)

    def model_dump(self) -> dict:
        """
        Dumps the credential as a dictionary.

        Returns:
            dict: The dictionary representation of the credential.
        """
        return asdict(self)


@dataclass
class UpdateCredential(Credential):
    """
    Represents an update operation for a credential in the Vecna CLI vault.
    Inherits from Credential and allows for updating specific fields.

    Attributes:
        new_name (Optional[str]): New name for the credential, if being updated.
        username (Optional[str]): New username for the credential, if being updated.
        password (Optional[str]): New password for the credential, if being updated.
        notes (Optional[str]): New notes for the credential, if being updated.
        tags (Optional[List[str]]): New tags for the credential, if being updated.
    """

    new_name: str | None = field(
        default=None,
        metadata={"description": "New name for the credential, if being updated."},
    )
    username: str | None = field(
        default=None,
        metadata={"description": "New username for the credential, if being updated."},
    )
    password: str | None = field(
        default=None,
        metadata={"description": "New password for the credential, if being updated."},
    )
    notes: str | None = field(
        default=None,
        metadata={"description": "New notes for the credential, if being updated."},
    )
    tags: list[str] | None = field(
        default=None,
        metadata={"description": "New tags for the credential, if being updated."},
    )
