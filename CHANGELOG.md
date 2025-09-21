# Changelog

All notable changes to this project will be documented in this file.

## [0.1.2] - 2025-09-21
- Re-published with updated `README.md` to include logo

## [0.1.1] - 2025-08-05

### Fixed
- Re-published with proper project description and `README.md` rendering on PyPI

---

## [0.1.0] - 2025-08-05

### Added
- Initial public release of Vecna CLI
- AES-256-GCM encrypted vault with master password authentication
- Credential management (add, get, update, delete, list)
- Alias management for reusable CLI commands (add, get, update, list, delete)
- Auto-expiring sessions with timeout control
- Built-in secure password generator
- Clipboard integration for password copying
- Tagging and note support for credentials and aliases
- Rich CLI output using `rich`
- Linux-only support (uses `/dev/shm` for in-memory key caching)
- CI setup with GitHub Actions for testing, coverage, and PyPI publishing
