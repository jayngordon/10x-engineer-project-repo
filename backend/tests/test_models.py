from pydantic import ValidationError
import pytest
from app.models import PromptBase, PromptCreate

# Model Validation Test for PromptBase
def test_prompt_base_validation():
    with pytest.raises(ValidationError):
        PromptBase(title="", content="Valid content")  # Should raise due to empty title

    try:
        PromptBase(title="Valid title", content="Valid content")
    except ValidationError:
        pytest.fail("Validation should pass for a valid instance")

# Default Values Test for PromptBase
def test_prompt_base_defaults():
    prompt = PromptBase(title="Test", content="Testing")
    assert prompt.description is None
    assert prompt.collection_id is None

# Serialization Test for PromptBase
def test_prompt_base_serialization():
    prompt = PromptBase(
        title="Serialize Test",
        content="Check serialization",
        description="A test",
        collection_id="test-123"
    )
    prompt_dict = prompt.dict()
    expected_dict = {
        "title": "Serialize Test",
        "content": "Check serialization",
        "description": "A test",
        "collection_id": "test-123"
    }
    assert prompt_dict == expected_dict

# Model Validation Test for PromptCreate
def test_prompt_create_validation():
    with pytest.raises(ValidationError):
        PromptCreate(title="", content="Valid content")  # Should raise due to empty title

    try:
        PromptCreate(title="Valid title", content="Valid content")
    except ValidationError:
        pytest.fail("Validation should pass for a valid instance")

# Default Values Test for PromptCreate
def test_prompt_create_defaults():
    prompt = PromptCreate(title="Test", content="Testing")
    assert prompt.description is None
    assert prompt.collection_id is None

# Serialization Test for PromptCreate
def test_prompt_create_serialization():
    prompt = PromptCreate(
        title="Serialize Test",
        content="Check serialization",
        description="A test",
        collection_id="test-123"
    )
    prompt_dict = prompt.dict()
    expected_dict = {
        "title": "Serialize Test",
        "content": "Check serialization",
        "description": "A test",
        "collection_id": "test-123"
    }
    assert prompt_dict == expected_dict

