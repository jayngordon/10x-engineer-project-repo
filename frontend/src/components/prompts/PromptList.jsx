import PromptCard from "./PromptCard";
import LoadingSpinner from "../shared/LoadingSpinner";
import ErrorMessage from "../shared/ErrorMessage";

const PromptList = ({ prompts = [], status, error, searchQuery, onPromptSelect }) => {
  if (status === "loading") {
    return <LoadingSpinner />;
  }

  if (error) {
    return <ErrorMessage message={error.message} />;
  }

  if (!prompts.length && status === "success") {
    return (
      <div className="rounded-2xl border border-slate-800 bg-slate-900/70 p-6 text-sm text-slate-400">
        {searchQuery
          ? `No prompts match “${searchQuery}”. Try a different keyword.`
          : "No prompts available yet. Create one to get started."}
      </div>
    );
  }

  return (
    <div className="grid gap-6 md:grid-cols-2">
      {prompts.map((prompt) => (
        <PromptCard prompt={prompt} key={prompt.id} onView={onPromptSelect} />
      ))}
    </div>
  );
};

export default PromptList;
