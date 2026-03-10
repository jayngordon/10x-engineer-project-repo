const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8080";

const buildUrl = (path) => {
  if (!path) {
    throw new Error("Path is required for API requests");
  }
  return path.startsWith("http") ? path : `${API_BASE_URL}${path}`;
};

const tryParseJson = (value) => {
  try {
    return JSON.parse(value);
  } catch {
    return null;
  }
};

const parseResponse = async (response) => {
  if (response.status === 204) {
    return null;
  }

  const text = await response.text();
  const payload = text ? tryParseJson(text) : null;

  if (!response.ok) {
    const detail = payload?.detail || payload?.message;
    const error = new Error(detail || response.statusText || "Request failed");
    error.status = response.status;
    error.payload = payload;
    throw error;
  }

  return payload;
};

export const request = async (path, options = {}) => {
  const url = buildUrl(path);
  const headers = {
    ...(options.headers ?? {}),
  };

  if (options.body && !Object.keys(headers).some((name) => name.toLowerCase() === "content-type")) {
    headers["Content-Type"] = "application/json";
  }

  const config = {
    ...options,
    headers,
  };

  try {
    const response = await fetch(url, config);
    return parseResponse(response);
  } catch (error) {
    const networkError = new Error(
      error?.message || "Unable to reach the backend. Please check your connection."
    );
    networkError.isNetworkError = true;
    networkError.originalError = error;
    throw networkError;
  }
};
