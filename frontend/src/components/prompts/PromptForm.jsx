import { useMemo, useState } from "react";
import Button from "../shared/Button";
import ErrorMessage from "../shared/ErrorMessage";

const defaultForm = {
  title: "",
  description: "",
  content: "",
  collectionId: "",
};

const PromptForm = ({
  collections = [],
  onSave,
  submitLabel = "Save prompt",
  isSubmitting: externalSubmitting = false,
}) => {
  const [formState, setFormState] = useState(defaultForm);
  const [localSubmitting, setLocalSubmitting] = useState(false);
  const [error, setError] = useState("");
  const isSubmitting = externalSubmitting || localSubmitting;

  const collectionOptions = useMemo(
    () => [{ id: "", name: "No collection" }, ...collections],
    [collections]
  );

  const clearForm = () => setFormState(defaultForm);

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!formState.title.trim() || !formState.content.trim()) {
      setError("Please add a title and content for the prompt");
      return;
    }

    setLocalSubmitting(true);
    setError("");
    try {
      await onSave({
        title: formState.title.trim(),
        description: formState.description.trim(),
        content: formState.content.trim(),
        collection_id: formState.collectionId || undefined,
      });
      clearForm();
    } catch (err) {
      setError(err?.message || "Unable to save prompt");
      throw err;
    } finally {
      setLocalSubmitting(false);
    }
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="space-y-4 rounded-2xl border border-slate-800 bg-slate-900/70 p-6 shadow-lg shadow-slate-950"
    >
      <p className="text-xs uppercase tracking-[0.4em] text-slate-400">New prompt</p>
      <div className="grid gap-4 md:grid-cols-2">
        <label className="text-sm text-slate-300">
          Title
          <input
            type="text"
            value={formState.title}
            onChange={(event) => setFormState((prev) => ({ ...prev, title: event.target.value }))}
            disabled={isSubmitting}
            className="mt-2 w-full rounded-xl border border-slate-800 bg-slate-950/70 px-3 py-2 text-sm text-slate-200 outline-none transition focus:border-sky-400 focus:ring focus:ring-sky-500/30"
            placeholder="AI-assisted executive summary"
          />
        </label>
        <label className="text-sm text-slate-300">
          Collection
          <select
            value={formState.collectionId}
            onChange={(event) => setFormState((prev) => ({ ...prev, collectionId: event.target.value }))}
            disabled={isSubmitting}
            className="mt-2 w-full rounded-xl border border-slate-800 bg-slate-950/70 px-3 py-2 text-sm text-slate-200 outline-none transition focus:border-sky-400 focus:ring focus:ring-sky-500/30"
          >
            {collectionOptions.map((collection) => (
              <option key={collection.id} value={collection.id}>
                {collection.name}
              </option>
            ))}
          </select>
        </label>
      </div>
      <label className="text-sm text-slate-300">
        Description
        <textarea
          value={formState.description}
          onChange={(event) => setFormState((prev) => ({ ...prev, description: event.target.value }))}
          disabled={isSubmitting}
          className="mt-2 w-full rounded-xl border border-slate-800 bg-slate-950/70 px-3 py-2 text-sm text-slate-200 outline-none transition focus:border-sky-400 focus:ring focus:ring-sky-500/30"
          rows={2}
          placeholder="Short note about the prompt"
        />
      </label>
      <label className="text-sm text-slate-300">
        Content
        <textarea
          value={formState.content}
          onChange={(event) => setFormState((prev) => ({ ...prev, content: event.target.value }))}
          disabled={isSubmitting}
          className="mt-2 w-full rounded-xl border border-slate-800 bg-slate-950/70 px-3 py-2 text-sm text-slate-200 outline-none transition focus:border-sky-400 focus:ring focus:ring-sky-500/30"
          rows={4}
          placeholder="Describe what this prompt should accomplish"
        />
      </label>
      {error && <ErrorMessage message={error} />}
      <div className="flex justify-end">
        <Button type="submit" disabled={isSubmitting}>
          {isSubmitting ? "Saving…" : submitLabel}
        </Button>
      </div>
    </form>
  );
};

export default PromptForm;
