import { useCallback, useRef, useState } from "react";
import { createPrompt, getPrompts } from "../api/prompts";

const normalizeError = (error) => ({
  message: error?.message || "Unable to reach PromptLab right now.",
  isNetworkError: Boolean(error?.isNetworkError),
});

export const usePrompts = () => {
  const [prompts, setPrompts] = useState([]);
  const [status, setStatus] = useState("idle");
  const [error, setError] = useState(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const lastFilters = useRef({});

  const reload = useCallback(async (filters = {}) => {
    setStatus("loading");
    setError(null);
    try {
      lastFilters.current = filters;
      const response = await getPrompts(filters);
      setPrompts(response?.prompts ?? response ?? []);
      setStatus("success");
    } catch (err) {
      setError(normalizeError(err));
      setStatus("error");
    }
  }, []);

  const addPrompt = useCallback(
    async (payload) => {
      setIsSubmitting(true);
      try {
        await createPrompt(payload);
        await reload(lastFilters.current);
      } catch (err) {
        setError(normalizeError(err));
        throw err;
      } finally {
        setIsSubmitting(false);
      }
    },
    [reload]
  );

  return {
    prompts,
    status,
    error,
    isSubmitting,
    reload,
    addPrompt,
  };
};
