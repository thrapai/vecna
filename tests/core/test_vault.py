import shutil
import tempfile
from pathlib import Path

import pytest
from pytest import MonkeyPatch

from vecna.core.vault import Vault
from vecna.models import Alias, Credential, UpdateAlias, UpdateCredential


@pytest.fixture
def vault_env(monkeypatch: MonkeyPatch):
    temp_dir = tempfile.mkdtemp()
    monkeypatch.setattr("vecna.config.VECNA_DIR", Path(temp_dir))
    monkeypatch.setattr("vecna.config.KEY_CACHE_DIR", Path(temp_dir))
    yield temp_dir
    shutil.rmtree(temp_dir)


@pytest.fixture
def sample_credential():
    return Credential(name="test", username="user", password="pass")


@pytest.fixture
def sample_alias():
    return Alias(
        name="test_alias", command="echo Hello", notes="Sample alias", tags=["tag1", "tag2"]
    )


def test_create_vault(vault_env):
    vault = Vault()
    vault.create("password123")
    assert vault.exists()


def test_unlock_with_invalid_password(vault_env):
    vault = Vault()
    vault.create("password123")
    with pytest.raises(ValueError):
        vault.unlock("wrongpassword")


def test_add_and_get_credential(vault_env, sample_credential):
    vault = Vault()
    vault.create("password123").unlock("password123")
    vault.add_credential(sample_credential)
    result = vault.get_credential("test")
    assert result.username == "user"
    assert result.password == "pass"


def test_list_credentials(vault_env, sample_credential):
    vault = Vault()
    vault.create("password123").unlock("password123")
    vault.add_credential(sample_credential)
    creds = vault.list_credentials()
    assert len(creds) == 1
    assert creds[0].name == "test"


def test_delete_credential(vault_env, sample_credential):
    vault = Vault()
    vault.create("password123").unlock("password123")
    vault.add_credential(sample_credential)
    vault.delete_credential("test")
    assert vault.get_credential("test") is None


def test_update_credential(vault_env, sample_credential):
    vault = Vault()
    vault.create("password123").unlock("password123")
    vault.add_credential(sample_credential)
    update = UpdateCredential(name="test", username="new_user")
    vault.update_credential(update)
    updated = vault.get_credential("test")
    assert updated.username == "new_user"


def test_add_duplicate_credential_raises(vault_env, sample_credential):
    vault = Vault()
    vault.create("password123").unlock("password123")
    vault.add_credential(sample_credential)
    with pytest.raises(KeyError):
        vault.add_credential(sample_credential)


def test_delete_non_existing_credential_raises(vault_env):
    vault = Vault()
    vault.create("password123").unlock("password123")
    with pytest.raises(KeyError):
        vault.delete_credential("ghost")


def test_add_and_get_alias(vault_env, sample_alias):
    vault = Vault()
    vault.create("password123").unlock("password123")
    vault.add_alias(sample_alias)
    result = vault.get_alias("test_alias")
    assert result.command == "echo Hello"
    assert result.notes == "Sample alias"
    assert result.tags == ["tag1", "tag2"]


def test_list_aliases(vault_env, sample_alias):
    vault = Vault()
    vault.create("password123").unlock("password123")
    vault.add_alias(sample_alias)
    aliases = vault.list_aliases()
    assert len(aliases) == 1
    assert aliases[0].name == "test_alias"


def test_delete_alias(vault_env, sample_alias):
    vault = Vault()
    vault.create("password123").unlock("password123")
    vault.add_alias(sample_alias)
    vault.delete_alias("test_alias")
    assert vault.get_alias("test_alias") is None


def test_update_alias(vault_env, sample_alias):
    vault = Vault()
    vault.create("password123").unlock("password123")
    vault.add_alias(sample_alias)
    update = UpdateAlias(name="test_alias", new_name="updated_alias", command="echo Updated")
    vault.update_alias(update)
    updated = vault.get_alias("updated_alias")
    assert updated.name == "updated_alias"
    assert updated.command == "echo Updated"


def test_add_duplicate_alias_raises(vault_env, sample_alias):
    vault = Vault()
    vault.create("password123").unlock("password123")
    vault.add_alias(sample_alias)
    with pytest.raises(KeyError):
        vault.add_alias(sample_alias)


def test_delete_non_existing_alias_raises(vault_env):
    vault = Vault()
    vault.create("password123").unlock("password123")
    with pytest.raises(KeyError):
        vault.delete_alias("ghost_alias")
