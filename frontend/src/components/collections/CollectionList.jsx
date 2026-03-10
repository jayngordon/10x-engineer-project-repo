import Button from "../shared/Button";
import LoadingSpinner from "../shared/LoadingSpinner";
import ErrorMessage from "../shared/ErrorMessage";

const CollectionList = ({
  collections = [],
  status,
  error,
  selectedCollectionId,
  onCollectionSelect,
}) => {
  if (status === "loading") {
    return <LoadingSpinner />;
  }

  if (error) {
    return <ErrorMessage message={error.message} />;
  }

  if (!collections.length && status === "success") {
    return (
      <div className="rounded-2xl border border-dashed border-slate-700 bg-slate-950/50 p-4 text-sm text-slate-500">
        No collections yet. Create one to organize your prompts.
      </div>
    );
  }

  return (
    <div className="space-y-3">
      {collections.map((collection) => (
        <Button
          key={collection.id}
          variant={selectedCollectionId === collection.id ? "primary" : "ghost"}
          className="w-full justify-between text-left text-sm"
          onClick={() => onCollectionSelect(collection.id)}
        >
          <div>
            <p className="text-sm font-semibold text-white">{collection.name}</p>
            <p className="text-xs text-slate-400">{collection.description}</p>
          </div>
          <span className="text-xs text-slate-500">{collection.id.slice(0, 6)}</span>
        </Button>
      ))}
    </div>
  );
};

export default CollectionList;
