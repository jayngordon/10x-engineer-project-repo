import pytest
from pydantic import ValidationError
from app.storage import Storage
from app.models import Prompt
from app.models import Collection

@pytest.fixture

def storage():
    return Storage()

@pytest.fixture(autouse=True)
def clear_storage(storage):
    storage.clear()
    yield
    storage.clear()


def build_prompt(**overrides):
    base = {
        "title": "Test Prompt",
        "content": "Sample prompt content",
    }
    base.update(overrides)
    return Prompt(**base)


def test_create_prompt_adds_prompt(storage):

    prompt = build_prompt(id="test1", content="Sample prompt")
    result = storage.create_prompt(prompt)
    assert result == prompt
    assert storage._prompts[prompt.id] == prompt

def test_create_prompt_overwrites_existing_prompt(storage):
    prompt1 = build_prompt(id="test2", content="Sample prompt")
    prompt2 = build_prompt(id="test2", content="Updated prompt")
    storage.create_prompt(prompt1)
    result = storage.create_prompt(prompt2)
    assert result == prompt2
    assert storage._prompts[prompt2.id] == prompt2

def test_create_prompt_with_empty_id(storage):
    # Test that creating a prompt with an empty id raises a KeyError
    with pytest.raises(KeyError):
        prompt = build_prompt(id="")
        storage.create_prompt(prompt)

def test_create_prompt_with_none_id(storage):
    # Test that creating a prompt with a None id raises a ValidationError
    with pytest.raises(ValidationError):
        build_prompt(id=None)

def test_create_prompt_with_empty_content(storage):
    # Empty prompt content should fail validation
    with pytest.raises(ValidationError):
        build_prompt(id="test4", content="")

def test_get_prompt_retrieves_existing_prompt(storage):
    prompt = build_prompt(id="test1", content="Sample prompt")
    storage.create_prompt(prompt)
    result = storage.get_prompt("test1")
    assert result == prompt

def test_get_prompt_returns_none_for_nonexistent_id(storage):
    # Test that retrieving a prompt with a nonexistent id returns None
    result = storage.get_prompt("nonexistent")
    assert result is None

def test_get_prompt_with_empty_id(storage):
    # Test that retrieving a prompt with an empty id returns None
    result = storage.get_prompt("")
    assert result is None

def test_get_prompt_with_none_id(storage):
    # Test that retrieving a prompt with a None id returns None
    result = storage.get_prompt(None)
    assert result is None

def test_get_all_prompts_returns_all_prompts(storage):
    prompt1 = build_prompt(id="test1", content="Prompt 1")
    prompt2 = build_prompt(id="test2", content="Prompt 2")
    storage.create_prompt(prompt1)
    storage.create_prompt(prompt2)
    result = storage.get_all_prompts()
    assert len(result) == 2
    assert prompt1 in result
    assert prompt2 in result

def test_get_all_prompts_returns_empty_list_when_no_prompts(storage):
    # Test that retrieving all prompts returns an empty list when no prompts exist
    result = storage.get_all_prompts()
    assert result == []

def test_update_prompt_successfully(storage):
    prompt = build_prompt(id="test1", content="Old Content")
    storage.create_prompt(prompt)
    updated_prompt = build_prompt(id="test1", content="New Content")
    result = storage.update_prompt("test1", updated_prompt)
    assert result.id == "test1"
    assert result.content == "New Content"
    assert result.version_number == 2
    assert storage._prompts["test1"] == result

def test_update_prompt_nonexistent_id(storage):
    prompt = build_prompt(id="nonexistent")
    result = storage.update_prompt("nonexistent", prompt)
    assert result is None

def test_update_prompt_with_partial_update(storage):
    prompt = build_prompt(id="test2", content="Original Content")
    storage.create_prompt(prompt)
    partial_update = build_prompt(id="test2", content="Updated Content")
    result = storage.update_prompt("test2", partial_update)
    assert result.content == "Updated Content"
    assert result.version_number == 2
    assert storage._prompts["test2"] == result

def test_update_prompt_with_empty_id(storage):
    prompt = build_prompt(id="", content="No ID Content")
    result = storage.update_prompt("", prompt)
    assert result is None

def test_delete_prompt_successfully(storage):
    prompt = build_prompt(id="test1", content="To be deleted")
    storage.create_prompt(prompt)
    result = storage.delete_prompt("test1")
    assert result is True
    assert "test1" not in storage._prompts

def test_delete_prompt_nonexistent_id(storage):
    # Test that deleting a prompt with a nonexistent id returns False
    result = storage.delete_prompt("nonexistent")
    assert result is False

def test_delete_prompt_with_empty_id(storage):
    # Test that deleting a prompt with an empty id returns False
    result = storage.delete_prompt("")
    assert result is False

def test_delete_prompt_multiple_times(storage):
    # Test that deleting the same prompt multiple times works as expected
    prompt = build_prompt(id="test2", content="Content")
    storage.create_prompt(prompt)
    first_deletion = storage.delete_prompt("test2")
    second_deletion = storage.delete_prompt("test2")
    assert first_deletion is True
    assert second_deletion is False

def test_create_collection_adds_collection(storage):
    collection = Collection(id="coll1", name="Collection 1")
    result = storage.create_collection(collection)
    assert result == collection
    assert storage._collections[collection.id] == collection

def test_create_collection_overwrites_existing_collection(storage):
    collection1 = Collection(id="coll2", name="Collection 1")
    collection2 = Collection(id="coll2", name="Collection 2")
    storage.create_collection(collection1)
    result = storage.create_collection(collection2)
    assert result == collection2
    assert storage._collections[collection2.id] == collection2

def test_create_collection_with_empty_id(storage):
    collection = Collection(id="", name="No ID Collection")
    result = storage.create_collection(collection)
    assert result == collection 
    assert storage._collections[collection.id] == collection

def test_get_collection_retrieves_existing_collection(storage):
    collection = Collection(id="coll1", name="Sample Collection")
    storage.create_collection(collection)
    result = storage.get_collection("coll1")
    assert result == collection

def test_get_collection_returns_none_for_nonexistent_id(storage):
    result = storage.get_collection("nonexistent")
    assert result is None

def test_get_collection_with_empty_id(storage):
    result = storage.get_collection("")
    assert result is None

def test_get_collection_with_none_id(storage):
    result = storage.get_collection(None)
    assert result is None

def test_delete_collection_successfully(storage):
    collection = Collection(id="coll1", name="To be deleted")
    storage.create_collection(collection)
    result = storage.delete_collection("coll1")
    assert result is True
    assert "coll1" not in storage._collections

def test_delete_collection_nonexistent_id(storage):
    result = storage.delete_collection("nonexistent")
    assert result is False


def test_delete_collection_with_empty_id(storage):
    result = storage.delete_collection("")
    assert result is False

def test_delete_collection_multiple_times(storage):
    collection = Collection(id="coll2", name="Content")
    storage.create_collection(collection)
    first_deletion = storage.delete_collection("coll2")
    second_deletion = storage.delete_collection("coll2")
    assert first_deletion is True
    assert second_deletion is False

def test_get_prompts_by_existing_collection(storage):
    collection_id = "coll1"
    prompt1 = build_prompt(id="prompt1", content="Prompt 1", collection_id=collection_id)
    prompt2 = build_prompt(id="prompt2", content="Prompt 2", collection_id=collection_id)
    storage.create_prompt(prompt1)
    storage.create_prompt(prompt2)
    result = storage.get_prompts_by_collection(collection_id)
    assert len(result) == 2
    assert prompt1 in result
    assert prompt2 in result

def test_get_prompts_by_nonexistent_collection(storage):
    result = storage.get_prompts_by_collection("nonexistent")
    assert result == []

def test_get_prompts_by_empty_collection_id(storage):
    result = storage.get_prompts_by_collection("")
    assert result == []

def test_get_prompts_by_none_collection_id(storage):
    result = storage.get_prompts_by_collection(None)
    assert result == []