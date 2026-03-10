import { request } from "./client";

export const getCollections = () => request("/collections");

export const createCollection = (payload) =>
  request("/collections", {
    method: "POST",
    body: JSON.stringify(payload),
  });

export const deleteCollection = (id) => {
  if (!id) {
    throw new Error("Collection ID is required");
  }
  return request(`/collections/${id}`, {
    method: "DELETE",
  });
};
