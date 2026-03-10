import Modal from "../shared/Modal";
import Button from "../shared/Button";

const formatDate = (value) => {
  if (!value) {
    return "—";
  }
  return new Date(value).toLocaleString();
};

const PromptDetail = ({ prompt, isOpen, onClose }) => {
  if (!prompt) {
    return null;
  }

  return (
    <Modal title={prompt.title} isOpen={isOpen} onClose={onClose} size="lg">
      <section className="space-y-5">
        <div>
          <p className="text-xs uppercase tracking-[0.4em] text-slate-500">Description</p>
          <p className="mt-2 text-sm text-slate-200">{prompt.description || "No description provided."}</p>
        </div>
        <div>
          <p className="text-xs uppercase tracking-[0.4em] text-slate-500">Content</p>
          <p className="mt-2 text-sm text-slate-100">{prompt.content}</p>
        </div>
        <div className="grid grid-cols-1 gap-3 text-sm text-slate-400 md:grid-cols-2">
          <p>
            <span className="font-semibold text-slate-200">Collection:</span> {prompt.collection_id || "Unassigned"}
          </p>
          <p>
            <span className="font-semibold text-slate-200">Created:</span> {formatDate(prompt.created_at)}
          </p>
          <p>
            <span className="font-semibold text-slate-200">Updated:</span> {formatDate(prompt.updated_at)}
          </p>
        </div>
      </section>
      <div className="mt-6 flex justify-end">
        <Button variant="ghost" onClick={onClose}>
          Close
        </Button>
      </div>
    </Modal>
  );
};

export default PromptDetail;
