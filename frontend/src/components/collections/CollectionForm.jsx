import { useState } from "react";
import Button from "../shared/Button";
import ErrorMessage from "../shared/ErrorMessage";
import { createCollection } from "../../api/collections";

const CollectionForm = ({ onCreated, onClose }) => {
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const canSubmit = name.trim().length > 0;

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!canSubmit) {
      setError("Collection name is required");
      return;
    }

    setLoading(true);
    setError("");
    try {
      await createCollection({ name: name.trim(), description: description.trim() });
      setName("");
      setDescription("");
      onCreated?.();
      onClose?.();
    } catch (err) {
      setError(err?.message || "Unable to create collection");
    } finally {
      setLoading(false);
    }
  };

  return (
    <form className="space-y-4" onSubmit={handleSubmit}>
      {error && <ErrorMessage message={error} />}
      <label className="block text-sm text-slate-200">
        Name
        <input
          value={name}
          onChange={(event) => setName(event.target.value)}
          className="mt-2 w-full rounded-xl border border-slate-800 bg-slate-950/70 px-3 py-2 text-sm text-slate-100 outline-none focus:border-sky-400"
          placeholder="e.g., Summarization"
        />
      </label>
      <label className="block text-sm text-slate-200">
        Description
        <textarea
          value={description}
          onChange={(event) => setDescription(event.target.value)}
          className="mt-2 w-full rounded-xl border border-slate-800 bg-slate-950/70 px-3 py-2 text-sm text-slate-100 outline-none focus:border-sky-400"
          rows={3}
          placeholder="Optional description"
        />
      </label>
      <div className="flex items-center justify-end gap-3">
        <Button variant="ghost" type="button" onClick={onClose}>
          Cancel
        </Button>
        <Button variant="primary" type="submit" className="disabled:opacity-50" disabled={!canSubmit || loading}>
          {loading ? "Creating…" : "Create Collection"}
        </Button>
      </div>
    </form>
  );
};

export default CollectionForm;
