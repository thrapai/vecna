# Security

## How Vecna Secures Your Data

Vecna is designed to store and manage secrets securely on your local machine. It uses strong encryption, safe key handling practices, and does not rely on any external services.

Vecna is local-first and makes no outbound network requests. Your secrets never leave your machine.

### Core Security Features

- **Encryption**: AES-256 in GCM mode (authenticated encryption)
- **Key Derivation**: PBKDF2 with 200,000 iterations
- **Key Size**: 256-bit (32 bytes)
- **Vault File**: Stored locally at `~/.vecna/vault.enc`
- **Master Password**: Never stored; used solely to derive the encryption key at runtime
- **Session Management**: The derived encryption key is temporarily cached in memory using a file at `/dev/shm/key.cache`. The key is removed when:
  - The vault is manually locked (`vecna lock`)
  - The system is restarted
  - A command is executed after the 15-minute session timeout

> **Note:** Session expiration is enforced lazily. The timer is only checked the next time a command is run. Until then, the session remains active even if 15 minutes have passed.

## Trust Assumptions

Vecna assumes the following conditions for secure use:

- The system running Vecna is trusted and free from compromise (e.g., malware, rogue users).
- The user’s master password is strong and unique.
- If the master password or the encrypted vault is lost, the data is unrecoverable.
- The user understands session expiration is not automatic, and manual locking is encouraged for sensitive environments.
- **While the encryption key is cached, anyone with sufficient system access may decrypt the vault until the session is explicitly locked or expired by a triggered command.**

## Key Exposure Window

During an active session, the derived encryption key is temporarily cached in `/dev/shm/key.cache`, a RAM-based filesystem available on most Linux systems. This ensures the key is never written to disk and is automatically cleared on reboot.

While cached:

- Any process or user with sufficient privileges could potentially access the key.
- The vault remains decryptable during this time, even after the 15-minute session timeout — unless a command is run to trigger expiration.
- Restarting the system or locking the vault manually removes the cached key.

### Recommendations

To minimize exposure:

- Always run `vecna lock` when finished using the CLI.
- Configure shorter session timeouts if needed.
- Avoid using Vecna in multi-user environments where `/dev/shm` is not isolated.
