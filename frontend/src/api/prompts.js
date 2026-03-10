import { request } from "./client";

const buildQuery = (params = {}) => {
  const query = new URLSearchParams();
  if (params.collectionId) {
    query.append("collection_id", params.collectionId);
  }
  if (params.search) {
    query.append("search", params.search);
  }
  return query.toString();
};

export const getPrompts = (params) => {
  const queryString = buildQuery(params);
  const path = queryString ? `/prompts?${queryString}` : "/prompts";
  return request(path);
};

export const getPrompt = (id) => {
  if (!id) {
    throw new Error("Prompt ID is required");
  }
  return request(`/prompts/${id}`);
};

export const createPrompt = (payload) =>
  request("/prompts", {
    method: "POST",
    body: JSON.stringify(payload),
  });

export const updatePrompt = (id, payload) => {
  if (!id) {
    throw new Error("Prompt ID is required");
  }
  return request(`/prompts/${id}`, {
    method: "PUT",
    body: JSON.stringify(payload),
  });
};

export const deletePrompt = (id) => {
  if (!id) {
    throw new Error("Prompt ID is required");
  }
  return request(`/prompts/${id}`, {
    method: "DELETE",
  });
};
