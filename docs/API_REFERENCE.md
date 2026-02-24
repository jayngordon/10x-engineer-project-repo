# API Reference

This document provides a comprehensive overview of all API endpoints available in the PromptLab project. Each endpoint is detailed with descriptions, example requests and responses, error formats, and any authentication requirements.

## Authentication

Currently, no authentication is required to access the PromptLab API endpoints. This may change in future revisions.

---

## Endpoints Overview

### Health Check

- **Endpoint:** `GET /health`
- **Description:** Check the health status of the API.
- **Request:**
  ```bash
  curl -X GET http://localhost:8000/health
  ```
- **Success Response:**
  - **Code:** 200 OK
  - **Content:** `{ "status": "healthy" }`
- **Error Response:**
  - **Code:** 500 INTERNAL SERVER ERROR
  - **Content:** `{ "error": "Service Unavailable" }`

### Prompts

- **List All Prompts**
  - **Endpoint:** `GET /prompts`
  - **Description:** Retrieve a list of all stored prompts.
  - **Request:**
    ```bash
    curl -X GET http://localhost:8000/prompts
    ```
  - **Success Response:**
    - **Code:** 200 OK
    - **Content:** `[{"id": "1", "template": "Hello {{name}}!"}, ...]`
  - **Error Response:**
    - **Code:** 404 NOT FOUND
    - **Content:** `{ "error": "No prompts found" }`

- **Retrieve a Single Prompt**
  - **Endpoint:** `GET /prompts/{id}`
  - **Description:** Retrieve details of a specific prompt by ID.
  - **Request:**
    ```bash
    curl -X GET http://localhost:8000/prompts/1
    ```
  - **Success Response:**
    - **Code:** 200 OK
    - **Content:** `{ "id": "1", "template": "Hello {{name}}!" }`
  - **Error Response:**
    - **Code:** 404 NOT FOUND
    - **Content:** `{ "error": "Prompt not found" }`

- **Create a New Prompt**
  - **Endpoint:** `POST /prompts`
  - **Description:** Create a new prompt with a given template.
  - **Request:**
    ```bash
    curl -X POST -H "Content-Type: application/json" -d '{"template": "Hi {{name}}!"}' http://localhost:8000/prompts
    ```
  - **Success Response:**
    - **Code:** 201 CREATED
    - **Content:** `{ "id": "2", "template": "Hi {{name}}!" }`
  - **Error Response:**
    - **Code:** 400 BAD REQUEST
    - **Content:** `{ "error": "Invalid input" }`

- **Update an Existing Prompt**
  - **Endpoint:** `PUT /prompts/{id}`
  - **Description:** Update the template of an existing prompt.
  - **Request:**
    ```bash
    curl -X PUT -H "Content-Type: application/json" -d '{"template": "Hello again, {{name}}!"}' http://localhost:8000/prompts/1
    ```
  - **Success Response:**
    - **Code:** 200 OK
    - **Content:** `{ "id": "1", "template": "Hello again, {{name}}!" }`
  - **Error Response:**
    - **Code:** 404 NOT FOUND
    - **Content:** `{ "error": "Prompt not found" }

- **Delete a Prompt**
  - **Endpoint:** `DELETE /prompts/{id}`
  - **Description:** Delete a specific prompt by ID.
  - **Request:**
    ```bash
    curl -X DELETE http://localhost:8000/prompts/1
    ```
  - **Success Response:**
    - **Code:** 204 NO CONTENT
  - **Error Response:**
    - **Code:** 404 NOT FOUND
    - **Content:** `{ "error": "Prompt not found" }`

### Collections

- **List All Collections**
  - **Endpoint:** `GET /collections`
  - **Description:** Retrieve a list of all collections.
  - **Request:**
    ```bash
    curl -X GET http://localhost:8000/collections
    ```
  - **Success Response:**
    - **Code:** 200 OK
    - **Content:** `[{"id": "1", "name": "First Collection"}, ...]`
  - **Error Response:**
    - **Code:** 404 NOT FOUND
    - **Content:** `{ "error": "No collections found" }`

- **Retrieve Collection Details**
  - **Endpoint:** `GET /collections/{id}`
  - **Description:** Get details of a specific collection by ID.
  - **Request:**
    ```bash
    curl -X GET http://localhost:8000/collections/1
    ```
  - **Success Response:**
    - **Code:** 200 OK
    - **Content:** `{ "id": "1", "name": "First Collection" }`
  - **Error Response:**
    - **Code:** 404 NOT FOUND
    - **Content:** `{ "error": "Collection not found" }`

- **Create a New Collection**
  - **Endpoint:** `POST /collections`
  - **Description:** Create a new collection.
  - **Request:**
    ```bash
    curl -X POST -H "Content-Type: application/json" -d '{"name": "New Collection"}' http://localhost:8000/collections
    ```
  - **Success Response:**
    - **Code:** 201 CREATED
    - **Content:** `{ "id": "2", "name": "New Collection" }`
  - **Error Response:**
    - **Code:** 400 BAD REQUEST
    - **Content:** `{ "error": "Invalid input" }`

- **Remove a Collection**
  - **Endpoint:** `DELETE /collections/{id}`
  - **Description:** Delete a collection by ID.
  - **Request:**
    ```bash
    curl -X DELETE http://localhost:8000/collections/1
    ```
  - **Success Response:**
    - **Code:** 204 NO CONTENT
  - **Error Response:**
    - **Code:** 404 NOT FOUND
    - **Content:** `{ "error": "Collection not found" }`