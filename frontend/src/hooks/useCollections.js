import { useCallback, useEffect, useState } from "react";
import { getCollections } from "../api/collections";

const normalizeError = (error) => ({
  message: error?.message || "Unable to fetch collections right now.",
  isNetworkError: Boolean(error?.isNetworkError),
});

export const useCollections = () => {
  const [collections, setCollections] = useState([]);
  const [status, setStatus] = useState("idle");
  const [error, setError] = useState(null);

  const reload = useCallback(async () => {
    setStatus("loading");
    setError(null);
    try {
      const response = await getCollections();
      setCollections(response?.collections ?? response ?? []);
      setStatus("success");
    } catch (err) {
      setError(normalizeError(err));
      setStatus("error");
    }
  }, []);

  useEffect(() => {
    reload();
  }, [reload]);

  return { collections, status, error, reload };
};
