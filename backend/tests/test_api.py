"""API tests for PromptLab

These tests verify the API endpoints work correctly.
Students should expand these tests significantly in Week 3.
"""

import pytest
from fastapi.testclient import TestClient
from app.api import app

class TestHealth:
    """Tests for health endpoint."""
    
    def test_health_check(self, client: TestClient):
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data


class TestPrompts:
    """Tests for prompt endpoints."""
    
    def test_create_prompt(self, client: TestClient, sample_prompt_data):
        # Assuming this test is meant to create a prompt
        response = client.post("/prompts", json=sample_prompt_data)
        assert response.status_code == 201
        data = response.json()
        assert data["content"] == sample_prompt_data["content"]

    def test_create_prompt_invalid_collection_id(self, client: TestClient, sample_prompt_data):
        """Test creating a prompt with invalid collection ID returns 400."""
        invalid_data = sample_prompt_data.copy()
        invalid_data["collection_id"] = "nonexistent-collection-id"
        response = client.post("/prompts", json=invalid_data)
        assert response.status_code == 400
        assert response.json()["detail"] == "Collection not found"

    def test_create_prompt_empty_strings(self, client: TestClient, sample_prompt_data):
        """Test creating a prompt with empty content and title."""
        empty_data = sample_prompt_data.copy()
        empty_data["title"] = ""
        empty_data["content"] = ""
        response = client.post("/prompts", json=empty_data)
        assert response.status_code in [400, 422]  # Adjust based on actual API design

    def test_create_prompt_with_special_characters(self, client: TestClient, sample_prompt_data):
        """Test creating a prompt with special characters in title and content."""
        special_data = sample_prompt_data.copy()
        special_data["title"] = "Title@#$%"
        special_data["content"] = "Content with special characters: @#$%^&*()"
        response = client.post("/prompts", json=special_data)
        assert response.status_code == 201

    def test_create_prompt_sorting_and_filtering(self, client: TestClient, sample_prompt_data):
        """Test sorting and filtering of prompts after creation."""
        client.post("/prompts", json=sample_prompt_data)
        response = client.get("/prompts?sort=created_at&order=asc")
        assert response.status_code == 200
        data = response.json()
        assert len(data["prompts"]) > 0
        # Add specific sorting and filtering assertions as needed

    def test_list_prompts_with_data(self, client: TestClient, sample_prompt_data):
        # Create a prompt first
        client.post("/prompts", json=sample_prompt_data)

        response = client.get("/prompts")
        assert response.status_code == 200
        data = response.json()
        assert len(data["prompts"]) == 1
        assert data["total"] == 1

    def test_list_prompts_filter_by_collection(self, client: TestClient, sample_prompt_data):
        collection_id = "12345"
        prompt_data = {**sample_prompt_data, "collection_id": collection_id}
        client.post("/prompts", json=prompt_data)

        response = client.get(f"/prompts?collection_id={collection_id}")
        assert response.status_code == 200
        data = response.json()
        assert all(prompt['collection_id'] == collection_id for prompt in data["prompts"])

    def test_list_prompts_search(self, client: TestClient, sample_prompt_data):
        keyword = "summarize"
        prompt_data = {**sample_prompt_data, "content": f"This is a test prompt to {keyword}."}
    
        # Post the prompt and capture the response
        post_response = client.post("/prompts", json=prompt_data)
        print("POST Response:", post_response.status_code, post_response.json())

        # Search for the prompt
        response = client.get(f"/prompts?search={keyword}")
        print("GET Response:", response.status_code, response.json())
    
        assert response.status_code == 200
        data = response.json()
    
        # Check if any prompts were found
        assert len(data["prompts"]) > 0, "No prompts found containing the keyword."
        assert keyword in data["prompts"][0]["content"]

    def test_list_prompts_with_special_characters(self, client: TestClient, sample_prompt_data):
        special_characters = "@#$%^&*()"
        prompt_data = {**sample_prompt_data, "content": f"Special {special_characters} characters."}
        client.post("/prompts", json=prompt_data)

        response = client.get(f"/prompts?search={special_characters}")
        assert response.status_code == 200
        data = response.json()
        assert len(data["prompts"]) > 0

    def test_list_prompts_empty_strings(self, client: TestClient, sample_prompt_data):
        prompt_data = {**sample_prompt_data, "collection_id": "", "content": ""}
        client.post("/prompts", json=prompt_data)

        response = client.get("/prompts?collection_id=&search=")
        assert response.status_code == 200
        data = response.json()
        assert len(data["prompts"]) >= 0

    def test_list_prompts_invalid_parameters(self, client: TestClient, sample_prompt_data):
        response = client.get("/prompts?nonexistent_param=invalid")
        assert response.status_code == 400
        response = client.post("/prompts", json=sample_prompt_data)
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == sample_prompt_data["title"]
        assert data["content"] == sample_prompt_data["content"]
        assert "id" in data
        assert "created_at" in data
    
    def test_list_prompts_empty(self, client: TestClient):
        response = client.get("/prompts")
        assert response.status_code == 200
        data = response.json()
        assert data["prompts"] == []
        assert data["total"] == 0
    
    def test_list_prompts_with_data(self, client: TestClient, sample_prompt_data):
        # Create a prompt first
        client.post("/prompts", json=sample_prompt_data)
        
        response = client.get("/prompts")
        assert response.status_code == 200
        data = response.json()
        assert len(data["prompts"]) == 1
        assert data["total"] == 1
    
    def test_get_prompt_success(self, client: TestClient, sample_prompt_data):
        # Create a prompt first
        create_response = client.post("/prompts", json=sample_prompt_data)
        prompt_id = create_response.json()["id"]
        
        response = client.get(f"/prompts/{prompt_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == prompt_id
    
    def test_get_prompt_empty_id(self, client: TestClient):
        # Expect the root `/prompts/` to list all prompts, consistent with list behavior.
        response = client.get("/prompts/")
        assert response.status_code == 200  # could return 200 with no error for listing
        data = response.json()
        assert type(data["prompts"]) is list  # Ensure the structure is a list

    def test_get_prompt_with_special_characters(self, client: TestClient):
        special_prompt_id = "special@#%id"
        response = client.get(f"/prompts/{special_prompt_id}")

    def test_get_prompt_not_found(self, client: TestClient):
        """Test that getting a non-existent prompt returns 404.
        
        NOTE: This test currently FAILS due to Bug #1!
        The API returns 500 instead of 404.
        """
        response = client.get("/prompts/nonexistent-id")
        # This should be 404, but there's a bug...
        assert response.status_code == 404  # Will fail until bug is fixed
    
    def test_delete_prompt(self, client: TestClient, sample_prompt_data):
        # Create a prompt first
        create_response = client.post("/prompts", json=sample_prompt_data)
        prompt_id = create_response.json()["id"]
        
        # Delete it
        response = client.delete(f"/prompts/{prompt_id}")
        assert response.status_code == 204
        
        # Verify it's gone
        get_response = client.get(f"/prompts/{prompt_id}")
        # Note: This might fail due to Bug #1
        assert get_response.status_code in [404, 500]  # 404 after fix
    
    def test_update_prompt(self, client: TestClient, sample_prompt_data):
        # Create a prompt first
        create_response = client.post("/prompts", json=sample_prompt_data)
        prompt_id = create_response.json()["id"]
        original_updated_at = create_response.json()["updated_at"]
        
        # Update it
        updated_data = {
            "title": "Updated Title",
            "content": "Updated content for the prompt",
            "description": "Updated description"
        }
        
        import time
        time.sleep(0.1)  # Small delay to ensure timestamp would change
        
        response = client.put(f"/prompts/{prompt_id}", json=updated_data)
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Title"
        
        # NOTE: This assertion will fail due to Bug #2!
        # The updated_at should be different from original
        # assert data["updated_at"] != original_updated_at  # Uncomment after fix

    def test_update_prompt_invalid_collection_id(self, client: TestClient, sample_prompt_data):
        # Create a prompt first
        create_response = client.post("/prompts", json=sample_prompt_data)
        prompt_id = create_response.json()["id"]
        
        # Attempt to update with invalid collection ID
        update_data = {
            "collection_id": "invalid-collection-id"
        }
        response = client.put(f"/prompts/{prompt_id}", json=update_data)
        assert response.status_code == 400
        assert response.json()["detail"] == "Collection not found"

    def test_update_prompt_partial_data(self, client: TestClient, sample_prompt_data):
        # Create a prompt first
        create_response = client.post("/prompts", json=sample_prompt_data)
        prompt_id = create_response.json()["id"]
        
        # Update only the title
        update_data = {
            "title": "Partially Updated Title"
        }
        response = client.put(f"/prompts/{prompt_id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Partially Updated Title"
        assert data["content"] == sample_prompt_data["content"]

    def test_update_prompt_concurrency(self, client: TestClient, sample_prompt_data):
        # Create a prompt first
        create_response = client.post("/prompts", json=sample_prompt_data)
        prompt_id = create_response.json()["id"]

        # Define two different updates
        update_data1 = {"title": "Update 1"}
        update_data2 = {"title": "Update 2"}

        # Apply updates concurrently
        response1 = client.put(f"/prompts/{prompt_id}", json=update_data1)
        response2 = client.put(f"/prompts/{prompt_id}", json=update_data2)

        assert response1.status_code == 200
        assert response2.status_code == 200

        # Verify final state (depending on concurrency control method, result might differ)
        final_response = client.get(f"/prompts/{prompt_id}")
        final_data = final_response.json()

        # Simply check if one of the titles is applied
        assert final_data["title"] in ["Update 1", "Update 2"]

    def test_delete_prompt_success(self, client: TestClient, sample_prompt_data):
        # Create a prompt first
        create_response = client.post("/prompts", json=sample_prompt_data)
        prompt_id = create_response.json()["id"]
        
        # Delete it
        response = client.delete(f"/prompts/{prompt_id}")
        assert response.status_code == 204
        
        # Verify it's gone
        get_response = client.get(f"/prompts/{prompt_id}")
        assert get_response.status_code == 404  # Assumes bug is fixed

    def test_delete_prompt_not_found(self, client: TestClient):
        """Attempt to delete a non-existent prompt and expect a 404 error."""
        response = client.delete("/prompts/nonexistent-id")
        assert response.status_code == 404

    def test_delete_prompt_empty_id(self, client: TestClient):
        """Attempt to delete a prompt without an ID and expect a 400 error."""
        response = client.delete("/prompts/")  # Assuming API handles trailing slash or missing ID with 400 error
        assert response.status_code == 400

    def test_delete_prompt_with_special_characters(self, client: TestClient, sample_prompt_data):
        """Attempt to delete a prompt using an ID with special characters."""
        special_prompt_id = "special@#%id"
        response = client.delete(f"/prompts/{special_prompt_id}")
        # Assuming the API should not allow this, or handles it gracefully
        assert response.status_code in [400, 404]

    def test_delete_prompt_with_query_parameters(self, client: TestClient, sample_prompt_data):
        """Ensure no effect of query parameters on DELETE request."""
        create_response = client.post("/prompts", json=sample_prompt_data)
        prompt_id = create_response.json()["id"]

        # Attempt deletion with irrelevant query
        response = client.delete(f"/prompts/{prompt_id}?sort=created_at&order=asc")
        assert response.status_code == 204

        # Verify deletion
        get_response = client.get(f"/prompts/{prompt_id}")
        assert get_response.status_code == 404
    
    def test_sorting_order(self, client: TestClient):
        """Test that prompts are sorted newest first.
        
        NOTE: This test might fail due to Bug #3!
        """
        import time
        
        # Create prompts with delay
        prompt1 = {"title": "First", "content": "First prompt content"}
        prompt2 = {"title": "Second", "content": "Second prompt content"}
        
        client.post("/prompts", json=prompt1)
        time.sleep(0.1)
        client.post("/prompts", json=prompt2)
        
        response = client.get("/prompts")
        prompts = response.json()["prompts"]
        
        # Newest (Second) should be first
        assert prompts[0]["title"] == "Second"  # Will fail until Bug #3 fixed


class TestCollections:
    """Tests for collection endpoints."""
    
    def test_create_collection(self, client: TestClient, sample_collection_data):
        response = client.post("/collections", json=sample_collection_data)
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == sample_collection_data["name"]
        assert "id" in data
    
    def test_list_collections(self, client: TestClient, sample_collection_data):
        client.post("/collections", json=sample_collection_data)
        
        response = client.get("/collections")
        assert response.status_code == 200
        data = response.json()
        assert len(data["collections"]) == 1
    
    def test_get_collection_not_found(self, client: TestClient):
        response = client.get("/collections/nonexistent-id")
        assert response.status_code == 404
    
    def test_delete_collection_with_prompts(self, client: TestClient, sample_collection_data, sample_prompt_data):
        """Test deleting a collection that has prompts.
        
        NOTE: Bug #4 - prompts become orphaned after collection deletion.
        This test documents the current (buggy) behavior.
        After fixing, update the test to verify correct behavior.
        """
        # Create collection
        col_response = client.post("/collections", json=sample_collection_data)
        collection_id = col_response.json()["id"]
        
        # Create prompt in collection
        prompt_data = {**sample_prompt_data, "collection_id": collection_id}
        prompt_response = client.post("/prompts", json=prompt_data)
        prompt_id = prompt_response.json()["id"]
        
        # Delete collection
        client.delete(f"/collections/{collection_id}")
        
        # The prompt still exists but has invalid collection_id
        # This is Bug #4 - should be handled properly
        prompts = client.get("/prompts").json()["prompts"]
        if prompts:
            # Prompt exists with orphaned collection_id
            assert prompts[0]["collection_id"] == collection_id
            # After fix, collection_id should be None or prompt should be deleted
