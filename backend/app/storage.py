"""In-memory storage for PromptLab

This module provides simple in-memory storage for prompts and collections.
In a production environment, this would be replaced with a database.
"""

from typing import Dict, List, Optional
from app.models import Prompt, Collection


class Storage:
    """A class to represent in-memory storage for prompts and collections."""

    def __init__(self):
        """Initializes the Storage instance."""
        self._prompts: Dict[str, Prompt] = {}
        self._collections: Dict[str, Collection] = {}
        self._prompt_versions: Dict[str, List[Prompt]] = {}
    
    # ============== Prompt Operations ==============
    
    def create_prompt(self, prompt: Prompt) -> Prompt:
        """Creates a new prompt.

        Args:
            prompt (Prompt): The prompt to add.

        Returns:
            Prompt: The added prompt.

        Example:
            prompt = Prompt(id="123", content="Sample prompt")
            storage.create_prompt(prompt)
        """
        if prompt.id == "":
            raise KeyError("Prompt id cannot be empty")
        prompt.version_number = 1
        self._prompts[prompt.id] = prompt
        self._prompt_versions[prompt.id] = [prompt]
        return prompt
    
    def get_prompt(self, prompt_id: str) -> Optional[Prompt]:
        """Retrieves a prompt by its ID.

        Args:
            prompt_id (str): The ID of the prompt.

        Returns:
            Optional[Prompt]: The prompt if found, otherwise None.

        Example:
            prompt = storage.get_prompt("123")
        """
        return self._prompts.get(prompt_id)
    
    def get_all_prompts(self) -> List[Prompt]:
        """Retrieves all prompts.

        Returns:
            List[Prompt]: A list of all prompts.

        Example:
            all_prompts = storage.get_all_prompts()
        """
        return list(self._prompts.values())
    
    def update_prompt(self, prompt_id: str, prompt: Prompt) -> Optional[Prompt]:
        """Updates an existing prompt and records the new version.

        Args:
            prompt_id (str): The ID of the prompt to update.
            prompt (Prompt): The updated prompt.

        Returns:
            Optional[Prompt]: The updated prompt if it was found, otherwise None.

        Example:
            prompt = Prompt(id="123", content="Updated prompt")
            updated_prompt = storage.update_prompt("123", prompt)
        """
        existing = self._prompts.get(prompt_id)
        if not existing:
            return None
        new_version_number = existing.version_number + 1
        updated_prompt = Prompt(**prompt.model_dump())
        updated_prompt.id = prompt_id
        updated_prompt.version_number = new_version_number
        updated_prompt.created_at = existing.created_at
        self._prompts[prompt_id] = updated_prompt
        self._prompt_versions.setdefault(prompt_id, []).append(updated_prompt)
        return updated_prompt
    
    def delete_prompt(self, prompt_id: str) -> bool:
        """Deletes a prompt and its version history by its ID.

        Args:
            prompt_id (str): The ID of the prompt to delete.

        Returns:
            bool: True if deleted, False otherwise.

        Example:
            success = storage.delete_prompt("123")
        """
        if prompt_id in self._prompts:
            del self._prompts[prompt_id]
            self._prompt_versions.pop(prompt_id, None)
            return True
        return False
    
    # ============== Collection Operations ==============
    
    def create_collection(self, collection: Collection) -> Collection:
        """Creates a new collection.

        Args:
            collection (Collection): The collection to add.

        Returns:
            Collection: The added collection.

        Example:
            collection = Collection(id="456", name="Sample Collection")
            storage.create_collection(collection)
        """
        self._collections[collection.id] = collection
        return collection
    
    def get_collection(self, collection_id: str) -> Optional[Collection]:
        """Retrieves a collection by its ID.

        Args:
            collection_id (str): The ID of the collection.

        Returns:
            Optional[Collection]: The collection if found, otherwise None.

        Example:
            collection = storage.get_collection("456")
        """
        return self._collections.get(collection_id)
    
    def get_all_collections(self) -> List[Collection]:
        """Retrieves all collections.

        Returns:
            List[Collection]: A list of all collections.

        Example:
            all_collections = storage.get_all_collections()
        """
        return list(self._collections.values())
    
    def delete_collection(self, collection_id: str) -> bool:
        """Deletes a collection by its ID.

        Args:
            collection_id (str): The ID of the collection to delete.

        Returns:
            bool: True if deleted, False otherwise.

        Example:
            success = storage.delete_collection("456")
        """
        if collection_id in self._collections:
            del self._collections[collection_id]
            return True
        return False
    
    def get_prompts_by_collection(self, collection_id: str) -> List[Prompt]:
        """Retrieves all prompts in a specific collection.

        Args:
            collection_id (str): The ID of the collection.

        Returns:
            List[Prompt]: A list of prompts in the collection.

        Example:
            prompts = storage.get_prompts_by_collection("456")
        """
        return [p for p in self._prompts.values() if p.collection_id == collection_id]

    def get_prompt_version(self, prompt_id: str, version: int) -> Optional[Prompt]:
        """Retrieve a specific version snapshot of a prompt.

        Args:
            prompt_id (str): The prompt identifier.
            version (int): The version number to retrieve.

        Returns:
            Optional[Prompt]: The prompt snapshot if it exists, otherwise None.
        """
        if not prompt_id or version < 1:
            return None
        versions = self._prompt_versions.get(prompt_id)
        if not versions:
            return None
        for prompt in versions:
            if prompt.version_number == version:
                return prompt
        return None

    def list_prompt_versions(self, prompt_id: str) -> List[Prompt]:
        """Returns the stored version history for a prompt.

        Args:
            prompt_id (str): The prompt identifier.

        Returns:
            List[Prompt]: All versions recorded for the prompt.
        """
        if not prompt_id:
            return []
        return list(self._prompt_versions.get(prompt_id, []))
    
    # ============== Utility ==============
    
    def clear(self):
        """Clears all stored prompts, collections, and their version history.

        Example:
            storage.clear()
        """
        self._prompts.clear()
        self._collections.clear()
        self._prompt_versions.clear()
