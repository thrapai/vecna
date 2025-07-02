from pathlib import Path


# Root directory for vecna CLI data
VECNA_DIR = Path.home() / ".vecna"

# Encrypted vault file
VAULT_FILE = VECNA_DIR / "vault.enc"

# Session metadata here
SESSION_FILE = VECNA_DIR / "session.json"
SESSION_LIFESPAN = 60 * 30  # 30 minutes

# Encryption parameters
KEY_DERIVATION_ITERATIONS = 200_000  # PBKDF2 or Argon2
KEY_LENGTH = 32  # 256 bits for AES
KEY_CACHE_FILE = VECNA_DIR / "key.cache"
KEY_ENCRYPTION_ALGORITHM = "AES-GCM"

# config file
CONFIG_FILE = VECNA_DIR / "config.json"

# Metadata
CLI_VERSION = "0.1.0"
