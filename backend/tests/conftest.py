import pytest
from fastapi.testclient import TestClient
from app.api import app, storage as api_storage
from app.storage import Storage

@pytest.fixture
def storage():
    return Storage()

@pytest.fixture
def client():
    """Create a test client for the API."""
    return TestClient(app)

@pytest.fixture(autouse=True)
def clear_api_storage():
    """Clear shared API storage before each test."""
    api_storage.clear()
    yield
    api_storage.clear()


@pytest.fixture
def sample_prompt_data():
    """Sample prompt data for testing."""
    return {
        "title": "Code Review Prompt",
        "content": "Review the following code and provide feedback:\n\n{{code}}",
        "description": "A prompt for AI code review"
    }

@pytest.fixture
def sample_collection_data():
    """Sample collection data for testing."""
    return {
        "name": "Development",
        "description": "Prompts for development tasks"
    }
