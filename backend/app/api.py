
@app.get("/health", response_model=HealthResponse)
def health_check():
    """Health check endpoint for the PromptLab API.

    Returns:
        HealthResponse: A response model containing the status and version of the service.

    Example:
        >>> health_check()
        HealthResponse(status='healthy', version='1.0.0')
    """
    return HealthResponse(status="healthy", version=__version__)


# ============== Prompt Endpoints ==============

@app.get("/prompts", response_model=PromptList)
def list_prompts(
    collection_id: Optional[str] = None,
    search: Optional[str] = None
):
    """List all prompts with optional filtering and search capabilities.

    Args:
        collection_id (Optional[str]): Identifier of the collection to filter prompts by.
        search (Optional[str]): String query to search within prompt contents.

    Returns:
        PromptList: A list of prompts and the total count available after filtering.

    Example:
        >>> list_prompts(collection_id='12345', search='summarize')
        PromptList(prompts=[...], total=1)
    """
    prompts = storage.get_all_prompts()
    # Filter by collection if specified
    if collection_id:
        prompts = filter_prompts_by_collection(prompts, collection_id)
    # Search if query provided
    if search:
        prompts = search_prompts(prompts, search)
    # Sort by date (newest first)
    prompts = sort_prompts_by_date(prompts, descending=True)
    return PromptList(prompts=prompts, total=len(prompts))


@app.get("/prompts/{prompt_id}", response_model=Prompt)
def get_prompt(prompt_id: str):
    """Retrieve a specific prompt by its unique identifier.

    Args:
        prompt_id (str): The unique identifier of the prompt to retrieve.

    Returns:
        Prompt: The corresponding prompt for the given ID.

    Raises:
        HTTPException: Raised with a 404 status if the prompt is not found.

    Example:
        >>> get_prompt(prompt_id='abcdef')
        Prompt(title='Summarize', content='Summarize the text.', ...)
    """
    prompt = storage.get_prompt(prompt_id)
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    return prompt


@app.post("/prompts", response_model=Prompt, status_code=201)
def create_prompt(prompt_data: PromptCreate):
    """Create a new prompt with the provided data.

    Args:
        prompt_data (PromptCreate): The data to create the new prompt.

    Returns:
        Prompt: A newly created prompt that fits the provided data.

    Raises:
        HTTPException: Raised with a 400 status if collection ID is invalid.

    Example:
        >>> create_prompt(PromptCreate(title='Write a haiku', content='...'))
        Prompt(id='new-id', title='Write a haiku', ...)
    """
    if prompt_data.collection_id:
        collection = storage.get_collection(prompt_data.collection_id)
        if not collection:
            raise HTTPException(status_code=400, detail="Collection not found")
    prompt = Prompt(**prompt_data.model_dump())
    return storage.create_prompt(prompt)


@app.put("/prompts/{prompt_id}", response_model=Prompt)
def update_prompt(prompt_id: str, prompt_data: PromptUpdate):
    """Update an existing prompt with new data.

    Args:
        prompt_id (str): The identifier of the prompt to be updated.
        prompt_data (PromptUpdate): The new data to update the prompt with.

    Returns:
        Prompt: The updated prompt.

    Raises:
        HTTPException: Raised with a 404 status if the prompt is not found.
        HTTPException: Raised with a 400 status if collection ID is invalid.

    Example:
        >>> update_prompt(prompt_id='abcdef', prompt_data=PromptUpdate(title='New Title'))
        Prompt(id='abcdef', title='New Title', ...)
    """
    existing = storage.get_prompt(prompt_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Prompt not found")
    if prompt_data.collection_id:
        collection = storage.get_collection(prompt_data.collection_id)
        if not collection:
            raise HTTPException(status_code=400, detail="Collection not found")
    updated_prompt = Prompt(
        id=existing.id,
        title=prompt_data.title,
        content=prompt_data.content,
        description=prompt_data.description,
        collection_id=prompt_data.collection_id,
        created_at=existing.created_at,
        updated_at=get_current_time()
    )
    return storage.update_prompt(prompt_id, updated_prompt)


@app.patch("/prompts/{prompt_id}", response_model=Prompt)
def partial_update_prompt(prompt_id: str, prompt_data: PromptUpdate):
    """Partially update a prompt with the fields provided.

    Args:
        prompt_id (str): The identifier of the prompt to be updated.
        prompt_data (PromptUpdate): The data with fields to update the prompt.

    Returns:
        Prompt: The updated prompt.

    Raises:
        HTTPException: Raised with a 404 status if the prompt is not found.
        HTTPException: Raised with a 400 status if collection ID is invalid.

    Example:
        >>> partial_update_prompt(prompt_id='abcdef', prompt_data=PromptUpdate(description='New Description'))
        Prompt(id='abcdef', description='New Description', ...)
    """
    existing = storage.get_prompt(prompt_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Prompt not found")
    if prompt_data.collection_id:
        collection = storage.get_collection(prompt_data.collection_id)
        if not collection:
            raise HTTPException(status_code=400, detail="Collection not found")
    updated_prompt = Prompt(
        id=existing.id,
        title=prompt_data.title if prompt_data.title is not None else existing.title,
        content=prompt_data.content if prompt_data.content is not None else existing.content,
        description=prompt_data.description if prompt_data.description is not None else existing.description,
        collection_id=prompt_data.collection_id if prompt_data.collection_id is not None else existing.collection_id,
        created_at=existing.created_at,
        updated_at=get_current_time()
    )
    return storage.update_prompt(prompt_id, updated_prompt)


@app.delete("/prompts/{prompt_id}", status_code=204)
def delete_prompt(prompt_id: str):
    """Delete a specific prompt by its identifier.

    Args:
        prompt_id (str): The identifier of the prompt to delete.

    Raises:
        HTTPException: Raised with a 404 status if the prompt is not found.

    Example:
        >>> delete_prompt(prompt_id='abcdef')
        # Returns None if successful
    """
    if not storage.delete_prompt(prompt_id):
        raise HTTPException(status_code=404, detail="Prompt not found")
    return None


# ============== Collection Endpoints ==============

@app.get("/collections", response_model=CollectionList)
def list_collections():
    """List all collections in PromptLab API.

    Returns:
        CollectionList: A list of collections and the total count available.

    Example:
        >>> list_collections()
        CollectionList(collections=[...], total=3)
    """
    collections = storage.get_all_collections()
    return CollectionList(collections=collections, total=len(collections))


@app.get("/collections/{collection_id}", response_model=Collection)
def get_collection(collection_id: str):
    """Retrieve a collection by its unique identifier.

    Args:
        collection_id (str): The unique identifier of the collection.

    Returns:
        Collection: The collection corresponding to the given ID.

    Raises:
        HTTPException: Raised with a 404 status if the collection is not found.

    Example:
        >>> get_collection(collection_id='12345')
        Collection(name='Education', description='Teaching prompts', ...)
    """
    collection = storage.get_collection(collection_id)
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    return collection


@app.post("/collections", response_model=Collection, status_code=201)
def create_collection(collection_data: CollectionCreate):
    """Create a new collection with the provided data.

    Args:
        collection_data (CollectionCreate): The data to create the new collection.

    Returns:
        Collection: The newly created collection.

    Example:
        >>> create_collection(CollectionCreate(name='New Collection', description='...'))
        Collection(id='new-id', name='New Collection', ...)
    """
    collection = Collection(**collection_data.model_dump())
    return storage.create_collection(collection)


@app.delete("/collections/{collection_id}", status_code=204)
def delete_collection(collection_id: str):
    """Delete a collection and its associated prompts by the collection ID.

    Args:
        collection_id (str): The identifier of the collection to delete.

    Raises:
        HTTPException: Raised with a 404 status if the collection is not found.

    Example:
        >>> delete_collection(collection_id='12345')
        # Returns None if successful
    """
    associated_prompts = storage.get_prompts_by_collection(collection_id)
    for prompt in associated_prompts:
        storage.delete_prompt(prompt.id)
    if not storage.delete_collection(collection_id):
        raise HTTPException(status_code=404, detail="Collection not found")
    return None

