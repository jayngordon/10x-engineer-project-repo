import pytest
from datetime import datetime
from app.utils import sort_prompts_by_date, filter_prompts_by_collection, search_prompts, validate_prompt_content  # Added import
from app.models import Prompt

# Extended Mock Prompt class for testing
class MockPrompt:
    def __init__(self, created_at, title="", description="", content=""):
        self.created_at = created_at
        self.title = title
        self.description = description
        self.content = content

# Test Cases for sort_prompts_by_date
def test_sort_prompts_by_date_descending():
    prompt1 = MockPrompt(datetime(2023, 10, 5))
    prompt2 = MockPrompt(datetime(2023, 10, 6))
    prompt3 = MockPrompt(datetime(2023, 9, 30))
    prompts = [prompt1, prompt2, prompt3]
    
    sorted_prompts = sort_prompts_by_date(prompts)

    assert sorted_prompts == [prompt2, prompt1, prompt3]

def test_sort_prompts_by_date_ascending():
    prompt1 = MockPrompt(datetime(2023, 10, 5))
    prompt2 = MockPrompt(datetime(2023, 10, 6))
    prompt3 = MockPrompt(datetime(2023, 9, 30))
    prompts = [prompt1, prompt2, prompt3]
    
    sorted_prompts = sort_prompts_by_date(prompts, descending=False)

    assert sorted_prompts == [prompt3, prompt1, prompt2]

def test_sort_prompts_empty_list():
    assert sort_prompts_by_date([]) == []

def test_sort_prompts_single_prompt():
    prompt = MockPrompt(datetime(2023, 10, 5))
    assert sort_prompts_by_date([prompt]) == [prompt]

def test_sort_prompts_malformed_objects():
    class IncompletePrompt:
        pass

    with pytest.raises(AttributeError):
        sort_prompts_by_date([IncompletePrompt()])

def test_sort_prompts_none_input():
    with pytest.raises(TypeError):
        sort_prompts_by_date(None)

# Test Cases for filter_prompts_by_collection
def test_filter_prompts_by_collection_found():
    prompt1 = MockPrompt(datetime(2023, 10, 5))
    prompt2 = MockPrompt(datetime(2023, 10, 6))
    prompt3 = MockPrompt(datetime(2023, 9, 30))
    prompt1.collection_id = "collection_1"
    prompt2.collection_id = "collection_2"
    prompt3.collection_id = "collection_1"
    prompts = [prompt1, prompt2, prompt3]

    filtered_prompts = filter_prompts_by_collection(prompts, "collection_1")
    assert filtered_prompts == [prompt1, prompt3]

def test_filter_prompts_by_collection_not_found():
    prompt1 = MockPrompt(datetime(2023, 10, 5))
    prompt2 = MockPrompt(datetime(2023, 10, 6))
    prompt1.collection_id = "collection_2"
    prompt2.collection_id = "collection_3"
    prompts = [prompt1, prompt2]

    filtered_prompts = filter_prompts_by_collection(prompts, "collection_1")
    assert filtered_prompts == []

def test_filter_prompts_empty_list():
    assert filter_prompts_by_collection([], "collection_1") == []

def test_filter_prompts_single_matching_prompt():
    prompt = MockPrompt(datetime(2023, 10, 5))
    prompt.collection_id = "collection_1"
    assert filter_prompts_by_collection([prompt], "collection_1") == [prompt]

def test_filter_prompts_single_non_matching_prompt():
    prompt = MockPrompt(datetime(2023, 10, 5))
    prompt.collection_id = "collection_2"
    assert filter_prompts_by_collection([prompt], "collection_1") == []

def test_filter_prompts_none_input():
    with pytest.raises(TypeError):
        filter_prompts_by_collection(None, "collection_1")

def test_filter_prompts_malformed_objects():
    class IncompletePrompt:
        pass

    with pytest.raises(AttributeError):
        filter_prompts_by_collection([IncompletePrompt()], "collection_1")

# Test Cases for search_prompts
def test_search_prompts_by_title():
    prompt1 = MockPrompt(datetime(2023, 10, 5), title="Search This Title")
    prompt2 = MockPrompt(datetime(2023, 10, 6), title="Another Title")
    prompts = [prompt1, prompt2]

    result = search_prompts(prompts, "Search This Title")
    assert result == [prompt1]

def test_search_prompts_by_description():
    prompt1 = MockPrompt(datetime(2023, 10, 5), description="Find This Description")
    prompt2 = MockPrompt(datetime(2023, 10, 6), description="Another Description")
    prompts = [prompt1, prompt2]

    result = search_prompts(prompts, "Find This Description")
    assert result == [prompt1]

def test_search_prompts_empty_list():
    result = search_prompts([], "query")
    assert result == []

def test_search_prompts_all_match():
    prompt1 = MockPrompt(datetime(2023, 10, 5), title="Title One")
    prompt2 = MockPrompt(datetime(2023, 10, 6), title="Title Two")
    prompts = [prompt1, prompt2]

    result = search_prompts(prompts, "Title")
    assert result == prompts

def test_validate_prompt_content():
    # Test for an empty string
    assert validate_prompt_content('') == False
    
    # Test for a string with only spaces
    assert validate_prompt_content('    ') == False
    
    # Test for a string less than 10 characters
    assert validate_prompt_content('short') == False
    
    # Test for a string exactly 10 characters
    assert validate_prompt_content('1234567890') == True
    
    # Test for a string longer than 10 characters
    assert validate_prompt_content('This is a long enough string') == True
    
    # Test for a valid string starting and ending in spaces
    assert validate_prompt_content('     A valid prompt   ') == True
