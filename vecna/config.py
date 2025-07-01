from pathlib import Path

# Root directory for vecna CLI data
VECNA_DIR = Path.home() / ".vecna"

# Encrypted vault file
VAULT_FILE = VECNA_DIR / "vault.enc"

# Session metadata here
SESSION_FILE = VECNA_DIR / "session.json"

# config file
CONFIG_FILE = VECNA_DIR / "config.json"

# Encryption parameters
KEY_DERIVATION_ITERATIONS = 200_000  # PBKDF2 or Argon2
KEY_LENGTH = 32  # 256 bits for AES
ENCRYPTION_ALGORITHM = "AES-GCM"  # Used by default

# Metadata
CLI_VERSION = "0.1.0"
