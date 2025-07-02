import json
import os

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from ..config import (
    KEY_CACHE_FILE,
    KEY_DERIVATION_ITERATIONS,
    KEY_LENGTH,
    VAULT_FILE,
    VECNA_DIR,
)
from ..models import Credential
from ..utils import (
    delete_secure_file,
    read_secure_file,
    write_secure_file,
)


def derive_key(
    password: bytes,
    salt: bytes,
) -> bytes:
    """
    Derives an encryption key from a password using PBKDF2.

    This function generates a cryptographic key from a user password by applying
    the PBKDF2 (Password-Based Key Derivation Function 2) key stretching algorithm.
    It uses SHA-256 as the hash function and applies a configurable number of iterations
    to increase resistance against brute-force attacks.

    Args:
        password : bytes
            The user-supplied password bytes to derive the key from
        salt : bytes
            Random bytes used to salt the key derivation process, preventing
            precomputed attacks

    Returns:
        bytes
            The derived key of length KEY_LENGTH bytes

    Notes:
        The security of the derived key depends on:
        - The strength of the original password
        - The number of iterations (KEY_DERIVATION_ITERATIONS)
        - The salt uniqueness
    """
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=KEY_LENGTH,
        salt=salt,
        iterations=KEY_DERIVATION_ITERATIONS,
        backend=default_backend(),
    )
    return kdf.derive(password)


def create_vault(
    password: str,
):
    """
    Create a new vault encrypted with the provided password.

    This function initializes a new empty vault by:
    1. Creating the Vecna directory if it doesn't exist
    2. Generating cryptographic components (salt and nonce)
    3. Deriving an encryption key from the password
    4. Creating an empty JSON structure and encrypting it
    5. Writing the encrypted data along with the salt and nonce to the vault file

    Args:
        password (str): The password to encrypt the vault with

    Returns:
        None

    Side effects:
        - Creates VECNA_DIR if it doesn't exist
        - Creates or overwrites the vault file at VAULT_FILE
    """
    VECNA_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    salt = os.urandom(16)
    nonce = os.urandom(12)
    key = derive_key(
        password.encode(),
        salt,
    )

    aesgcm = AESGCM(key)
    data = json.dumps({}).encode()
    encrypted = aesgcm.encrypt(nonce, data, None)

    write_secure_file(
        VAULT_FILE,
        salt + nonce + encrypted,
    )


def unlock_vault(
    password: str,
) -> dict:
    """
    Attempts to unlock the vault using the provided password.

    This function reads the encrypted vault file, extracts the salt and nonce,
    and attempts to decrypt the contents using the derived key from the password.
    If successful, it caches the encryption key for future use.

    Args:
        password (str): The password to use for unlocking the vault

    Returns:
        dict: The decrypted vault contents

    Raises:
        ValueError: If the password is incorrect or the vault cannot be unlocked
    """
    data = read_secure_file(VAULT_FILE)
    salt = data[:16]
    nonce = data[16:28]
    encrypted = data[28:]

    key = derive_key(
        password.encode(),
        salt,
    )
    aesgcm = AESGCM(key)

    try:
        aesgcm.decrypt(
            nonce,
            encrypted,
            None,
        )
        write_secure_file(
            KEY_CACHE_FILE,
            key,
        )
    except Exception as e:
        raise ValueError("Failed to unlock vault. Check your password.") from e


def lock_vault():
    """
    Lock the vault by removing the cached key and clearing the vault file.

    This function securely deletes the cached encryption key and clears the contents
    of the vault file, effectively locking it until unlocked again with a password.

    Returns:
        None

    Side effects:
        - Deletes the KEY_CACHE_FILE
        - Clears the VAULT_FILE contents
    """
    if KEY_CACHE_FILE.exists():
        delete_secure_file(KEY_CACHE_FILE)


def add_credential(
    credential: Credential,
):
    """
    Add a new credential to the vault.

    This function appends a new credential to the existing vault contents.
    It reads the current vault, adds the new credential, and writes the updated
    vault back to the file.

    Args:
        credential (Credential): The credential object to add

    Returns:
        None

    Raises:
        ValueError: If the vault is not unlocked or if there is an error writing to the vault
    """

    data = read_secure_file(VAULT_FILE)
    salt = data[:16]
    nonce = data[16:28]
    encrypted = data[28:]

    key = read_secure_file(KEY_CACHE_FILE)
    aesgcm = AESGCM(key)

    try:
        decrypted_data = aesgcm.decrypt(
            nonce,
            encrypted,
            None,
        )
        vault_contents = json.loads(decrypted_data.decode())
    except Exception as e:
        raise ValueError("Failed to read vault contents.") from e

    vault_contents[credential.name] = credential.model_dump()

    new_data = json.dumps(vault_contents).encode()
    encrypted_new_data = aesgcm.encrypt(
        nonce,
        new_data,
        None,
    )
    print(
        "Added new data",
        new_data,
        "\n",
    )
    write_secure_file(
        VAULT_FILE,
        salt + nonce + encrypted_new_data,
    )


def get_credential(
    name: str,
) -> Credential:
    """
    Retrieve a credential from the vault by name.

    This function reads the vault contents, decrypts them, and returns the
    specified credential as a Credential object.

    Args:
        name (str): The name of the credential to retrieve

    Returns:
        Credential: The requested credential object

    Raises:
        ValueError: If the vault is not unlocked or if the credential does not exist
    """
    data = read_secure_file(VAULT_FILE)
    nonce = data[16:28]
    encrypted = data[28:]

    key = read_secure_file(KEY_CACHE_FILE)
    aesgcm = AESGCM(key)

    try:
        decrypted_data = aesgcm.decrypt(
            nonce,
            encrypted,
            None,
        )
        vault_contents = json.loads(decrypted_data.decode())
    except Exception as e:
        raise ValueError("Failed to read vault contents.") from e

    if name not in vault_contents:
        raise ValueError(f"Credential '{name}' not found in vault.")

    return Credential(**vault_contents[name])


def list_credentials() -> list[Credential]:
    """
    List all credentials stored in the vault.

    This function retrieves all credentials from the vault, decrypts them,
    and returns a list of Credential objects.

    Returns:
        list[Credential]: A list of all credentials in the vault

    Raises:
        ValueError: If the vault is not unlocked or if there is an error reading the vault
    """
    data = read_secure_file(VAULT_FILE)
    nonce = data[16:28]
    encrypted = data[28:]

    key = read_secure_file(KEY_CACHE_FILE)
    aesgcm = AESGCM(key)

    try:
        decrypted_data = aesgcm.decrypt(
            nonce,
            encrypted,
            None,
        )
        vault_contents = json.loads(decrypted_data.decode())
    except Exception as e:
        raise ValueError("Failed to read vault contents.") from e

    return [Credential(**cred) for cred in vault_contents.values()]


def delete_credential(
    name: str,
) -> bool:
    """
    Delete a credential from the vault by name.

    This function removes the specified credential from the vault contents
    and updates the vault file accordingly.

    Args:
        name (str): The name of the credential to delete

    Returns:
        bool: True if the credential was deleted, False if it was not found

    Raises:
        ValueError: If the vault is not unlocked or if there is an error reading/writing the vault
    """
    data = read_secure_file(VAULT_FILE)
    nonce = data[16:28]
    encrypted = data[28:]

    key = read_secure_file(KEY_CACHE_FILE)
    aesgcm = AESGCM(key)

    try:
        decrypted_data = aesgcm.decrypt(
            nonce,
            encrypted,
            None,
        )
        vault_contents = json.loads(decrypted_data.decode())
    except Exception as e:
        raise ValueError("Failed to read vault contents.") from e

    if name not in vault_contents:
        return False

    del vault_contents[name]

    new_data = json.dumps(vault_contents).encode()
    encrypted_new_data = aesgcm.encrypt(
        nonce,
        new_data,
        None,
    )

    write_secure_file(
        VAULT_FILE,
        data[:16] + nonce + encrypted_new_data,
    )

    return True


def update_credential(
    credential: Credential,
) -> bool:
    """
    Update an existing credential in the vault.

    This function modifies the specified credential in the vault contents
    and writes the updated contents back to the vault file.

    Args:
        credential (Credential): The updated credential object

    Returns:
        bool: True if the credential was updated, False if it was not found

    Raises:
        ValueError: If the vault is not unlocked or if there is an error reading/writing the vault
    """
    data = read_secure_file(VAULT_FILE)
    nonce = data[16:28]
    encrypted = data[28:]

    key = read_secure_file(KEY_CACHE_FILE)
    aesgcm = AESGCM(key)

    try:
        decrypted_data = aesgcm.decrypt(
            nonce,
            encrypted,
            None,
        )
        vault_contents = json.loads(decrypted_data.decode())
    except Exception as e:
        raise ValueError("Failed to read vault contents.") from e

    if credential.name not in vault_contents:
        return False

    vault_contents[credential.name] = credential.model_dump()

    new_data = json.dumps(vault_contents).encode()
    encrypted_new_data = aesgcm.encrypt(
        nonce,
        new_data,
        None,
    )

    write_secure_file(
        VAULT_FILE,
        data[:16] + nonce + encrypted_new_data,
    )

    return True
