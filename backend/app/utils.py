"""Utility functions for PromptLab"""

import re
from typing import List
from app.models import Prompt

def sort_prompts_by_date(prompts: List[Prompt], descending: bool = True) -> List[Prompt]:
    """Sort prompts by creation date.
    
    Args:
        prompts (List[Prompt]): A list of Prompt objects to sort.
        descending (bool, optional): If True, sorts the list in descending order by date. Defaults to True.

    Returns:
        List[Prompt]: Sorted list of prompts by creation date.

    Example:
        >>> sort_prompts_by_date(prompts)
        [Prompt(...), Prompt(...)]
    """
    return sorted(prompts, key=lambda p: p.created_at, reverse=descending)

def filter_prompts_by_collection(prompts: List[Prompt], collection_id: str) -> List[Prompt]:
    """Filter prompts by collection ID.

    Args:
        prompts (List[Prompt]): A list of Prompt objects to filter.
        collection_id (str): The ID of the collection to filter prompts by.

    Returns:
        List[Prompt]: A list of prompts that belong to the specified collection.
    """
    return [p for p in prompts if p.collection_id == collection_id]

def _matches_query(prompt: Prompt, query_lower: str) -> bool:
    return (
        query_lower in prompt.title.lower()
        or (prompt.description and query_lower in prompt.description.lower())
        or (prompt.content and query_lower in prompt.content.lower())
    )


def search_prompts(prompts: List[Prompt], query: str) -> List[Prompt]:
    """Search prompts by query string.

    Args:
        prompts (List[Prompt]): A list of Prompt objects to search through.
        query (str): The query string to search for in prompt titles and descriptions.

    Returns:
        List[Prompt]: A list of prompts that match the search query.

    Example:
        >>> search_prompts(prompts, "search term")
        [Prompt(...)]
    """
    query_lower = query.lower()
    return [p for p in prompts if _matches_query(p, query_lower)]

def validate_prompt_content(content: str) -> bool:
    """Validate if the prompt content is valid.

    Args:
        content (str): The content of the prompt to validate.

    Returns:
        bool: True if the content is valid, False otherwise.

    Example:
        >>> validate_prompt_content('This is a valid prompt')
        True

    A valid prompt should:
    - Not be empty
    - Not be just whitespace
    - Be at least 10 characters
    """
    normalized = content.strip()
    if not normalized:
        return False
    return len(normalized) >= 10

def validate_collection_id(collection_id: str) -> bool:
    """Simple validation for collection IDs."""
    normalized = (collection_id or "").strip()
    if len(normalized) < 6:
        return False
    cleaned = normalized.replace("-", "").replace("_", "")
    return cleaned.isalnum()

def extract_variables(content: str) -> List[str]:
    """Extract variables from the prompt content.

    Args:
        content (str): The content of the prompt from which to extract variables.

    Returns:
        List[str]: A list of variable names extracted from the content.

    Example:
        >>> extract_variables('Hi, {{name}}. Your email is {{email}}.')
        ['name', 'email']

    Variables are in the format {{variable_name}}
    """
    pattern = r'\{\{(\w+)\}\}'
    return re.findall(pattern, content)

