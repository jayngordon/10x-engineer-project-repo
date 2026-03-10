import Button from "../shared/Button";

const formatDate = (value) => {
  if (!value) {
    return "—";
  }
  return new Date(value).toLocaleString();
};

const PromptCard = ({ prompt, onView }) => {
  return (
    <div className="flex h-full flex-col justify-between gap-4 rounded-2xl border border-slate-800 bg-slate-900/70 p-5 shadow-xl shadow-slate-950/40">
      <div>
        <div className="flex items-center justify-between">
          <h3 className="text-lg font-semibold text-white">{prompt.title}</h3>
          <span className="text-xs uppercase tracking-wide text-slate-500">ID: {prompt.id.slice(0, 6)}</span>
        </div>
        <p className="mt-2 text-sm text-slate-300">{prompt.description || "No description"}</p>
      </div>
      <div className="space-y-1 text-sm text-slate-400">
        <p className="text-slate-300">
          <span className="font-semibold text-slate-200">Collection:</span> {prompt.collection_id || "Unassigned"}
        </p>
        <p>
          <span className="font-semibold text-slate-200">Created:</span> {formatDate(prompt.created_at)}
        </p>
        <p>
          <span className="font-semibold text-slate-200">Updated:</span> {formatDate(prompt.updated_at)}
        </p>
      </div>
      <div className="flex items-center justify-end">
        <Button variant="secondary" onClick={() => onView?.(prompt)}>
          View details
        </Button>
      </div>
    </div>
  );
};

export default PromptCard;
