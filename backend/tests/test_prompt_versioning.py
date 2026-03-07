import pytest

from app.models import Prompt


def build_prompt(**overrides) -> Prompt:
    base = {
        "id": "prompt-version-test",
        "title": "Versioned Prompt",
        "content": "Initial prompt content",
        "description": "Tracks prompt versions",
    }
    base.update(overrides)
    return Prompt(**base)


# ============================ Happy Path ==================================

def test_create_prompt_initializes_version_history(storage):
    prompt = build_prompt(id="prompt-100")
    created = storage.create_prompt(prompt)

    assert created.version_number == 1

    versions = storage.list_prompt_versions(prompt.id)
    assert len(versions) == 1
    assert versions[0].version_number == 1
    assert versions[0] == created


def test_update_prompt_increments_version(storage):
    prompt = build_prompt(id="prompt-101", content="Original content")
    storage.create_prompt(prompt)

    updated_prompt = build_prompt(id="prompt-101", content="Updated content")
    second_version = storage.update_prompt(prompt.id, updated_prompt)

    assert second_version.version_number == 2

    versions = storage.list_prompt_versions(prompt.id)
    assert [version.version_number for version in versions] == [1, 2]
    assert versions[-1].content == "Updated content"


def test_get_prompt_returns_latest_version(storage):
    prompt = build_prompt(id="prompt-102", content="Original")
    storage.create_prompt(prompt)

    storage.update_prompt(prompt.id, build_prompt(id=prompt.id, content="Second"))
    storage.update_prompt(prompt.id, build_prompt(id=prompt.id, content="Third"))

    latest = storage.get_prompt(prompt.id)
    assert latest.version_number == 3
    assert latest.content == "Third"


def test_get_prompt_version_retrieves_specific_snapshot(storage):
    prompt = build_prompt(id="prompt-103")
    storage.create_prompt(prompt)
    storage.update_prompt(prompt.id, build_prompt(id=prompt.id, content="Second"))

    first_snapshot = storage.get_prompt_version(prompt.id, 1)
    second_snapshot = storage.get_prompt_version(prompt.id, 2)

    assert first_snapshot.content == "Initial prompt content"
    assert first_snapshot.version_number == 1
    assert second_snapshot.content == "Second"
    assert second_snapshot.version_number == 2


def test_list_prompt_versions_returns_all_versions(storage):
    prompt = build_prompt(id="prompt-104")
    storage.create_prompt(prompt)
    storage.update_prompt(prompt.id, build_prompt(id=prompt.id, content="Second"))
    storage.update_prompt(prompt.id, build_prompt(id=prompt.id, content="Third"))

    history = storage.list_prompt_versions(prompt.id)
    assert len(history) == 3
    assert [version.version_number for version in history] == [1, 2, 3]


# ============================ Edge Cases ==================================

def test_update_prompt_without_changes_records_new_version(storage):
    prompt = build_prompt(id="prompt-105", content="Static content")
    storage.create_prompt(prompt)

    storage.update_prompt(prompt.id, build_prompt(id=prompt.id, content="Static content"))

    versions = storage.list_prompt_versions(prompt.id)

    assert len(versions) == 2
    assert versions[-1].version_number == 2


def test_list_prompt_versions_returns_empty_for_unknown_prompt(storage):
    assert storage.list_prompt_versions("nonexistent") == []


# ============================ Negative Tests ==============================

@pytest.mark.parametrize("prompt_id", ["", None])
def test_get_prompt_version_invalid_ids_returns_none(storage, prompt_id):
    assert storage.get_prompt_version(prompt_id, 1) is None


def test_get_prompt_version_nonexistent_version_returns_none(storage):
    prompt = build_prompt(id="prompt-106")
    storage.create_prompt(prompt)

    assert storage.get_prompt_version(prompt.id, 10) is None


def test_versioning_resets_on_delete(storage):
    prompt = build_prompt(id="prompt-107")
    storage.create_prompt(prompt)
    storage.update_prompt(prompt.id, build_prompt(id=prompt.id, content="Second"))

    storage.delete_prompt(prompt.id)
    recreated = storage.create_prompt(build_prompt(id=prompt.id))

    assert recreated.version_number == 1
    assert storage.list_prompt_versions(prompt.id) == [recreated]


def test_list_prompt_versions_after_prompt_deleted(storage):
    prompt = build_prompt(id="prompt-108")
    storage.create_prompt(prompt)
    storage.delete_prompt(prompt.id)

    assert storage.list_prompt_versions(prompt.id) == []
