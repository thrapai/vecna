from ..config import VECNA_DIR, VAULT_FILE, KEY_DERIVATION_ITERATIONS, KEY_LENGTH
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.backends import default_backend
import os
import json


def derive_key(password: bytes, salt: bytes) -> bytes:
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


def create_vault(password: str):
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
    VECNA_DIR.mkdir(parents=True, exist_ok=True)

    salt = os.urandom(16)
    nonce = os.urandom(12)
    key = derive_key(password.encode(), salt)

    aesgcm = AESGCM(key)
    data = json.dumps({}).encode()
    encrypted = aesgcm.encrypt(nonce, data, None)

    with open(VAULT_FILE, "wb") as f:
        f.write(salt + nonce + encrypted)


def unlock_vault(password: str) -> dict:
    """
    Unlock the vault using the provided password and return its contents.
    
    This function reads the encrypted vault file, derives the key using the provided
    password, and decrypts the contents to return as a dictionary.
    The consists of:
    - Salt: The salt used for key derivation (first 16 bytes)
    - Nonce: The nonce used for AES-GCM encryption (next 12 bytes)
    - Encrypted data: The actual encrypted JSON data (remaining bytes)
    
    Args:
        password (str): The password to unlock the vault
        
    Returns:
        dict: The decrypted contents of the vault
        
    Raises:
        ValueError: If the password is incorrect or the vault is corrupted
    """
    if not VAULT_FILE.exists():
        raise FileNotFoundError(f"Vault file {VAULT_FILE} does not exist.")

    with open(VAULT_FILE, "rb") as f:
        data = f.read()

    salt = data[:16]
    nonce = data[16:28]
    encrypted = data[28:]

    key = derive_key(password.encode(), salt)
    aesgcm = AESGCM(key)


    try:
        decrypted = aesgcm.decrypt(nonce, encrypted, None)
        return json.loads(decrypted.decode())
    except Exception as e:
        raise ValueError("Failed to unlock vault. Check your password.") from e