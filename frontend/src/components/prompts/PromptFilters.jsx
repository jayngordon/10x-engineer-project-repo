import { useEffect, useState } from "react";
import SearchBar from "../shared/SearchBar";
import LoadingSpinner from "../shared/LoadingSpinner";
import ErrorMessage from "../shared/ErrorMessage";

const PromptFilters = ({
  collectionId,
  searchValue,
  collections = [],
  onSearchChange,
  onCollectionChange,
  loading,
  error,
}) => {
  const [localSearch, setLocalSearch] = useState(searchValue ?? "");

  useEffect(() => {
    setLocalSearch(searchValue ?? "");
  }, [searchValue]);

  useEffect(() => {
    const handler = setTimeout(() => {
      onSearchChange(localSearch.trim());
    }, 300);
    return () => clearTimeout(handler);
  }, [localSearch, onSearchChange]);

  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-900/70 p-4 shadow-lg shadow-slate-900/40">
      {error && <ErrorMessage message={error.message} />}
      <div className="space-y-4">
        <SearchBar
          value={localSearch}
          onChange={setLocalSearch}
          placeholder="Search prompts, keywords, or instructions"
        />
        <div>
          <span className="text-xs uppercase tracking-[0.5em] text-slate-400">Collection</span>
          <div className="relative">
            {loading && (
              <div className="absolute right-3 top-1/2 -translate-y-1/2">
                <LoadingSpinner />
              </div>
            )}
            <select
              value={collectionId}
              onChange={(event) => onCollectionChange(event.target.value)}
              className="mt-2 w-full rounded-2xl border border-slate-800 bg-slate-950/70 px-4 py-3 text-sm text-slate-200 outline-none focus:border-sky-400 focus:ring focus:ring-sky-500/30"
            >
              <option value="">All Collections</option>
              {collections.map((collection) => (
                <option key={collection.id} value={collection.id}>
                  {collection.name}
                </option>
              ))}
            </select>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PromptFilters;
