import { useEffect, useMemo, useState } from "react";
import PromptFilters from "../components/prompts/PromptFilters";
import PromptForm from "../components/prompts/PromptForm";
import PromptList from "../components/prompts/PromptList";
import PromptDetail from "../components/prompts/PromptDetail";
import { useCollections } from "../hooks/useCollections";
import { usePrompts } from "../hooks/usePrompts";

const buildFilters = (collectionId, search) => ({
  collectionId: collectionId || undefined,
  search: search || undefined,
});

const PromptsPage = ({ collectionId, onCollectionChange }) => {
  const [search, setSearch] = useState("");
  const [activePrompt, setActivePrompt] = useState(null);

  const { prompts, status, error, reload, addPrompt, isSubmitting } = usePrompts();
  const { collections, status: collectionsStatus, error: collectionsError } = useCollections();

  const filters = useMemo(() => buildFilters(collectionId, search), [collectionId, search]);

  useEffect(() => {
    reload(filters);
  }, [filters, reload]);

  const handleCreate = async (payload) => {
    await addPrompt(payload);
  };

  const isLoading = status === "loading";
  const isCollectionsLoading = collectionsStatus === "loading";

  const handlePromptSelect = (prompt) => {
    setActivePrompt(prompt);
  };

  const handleCloseDetail = () => setActivePrompt(null);

  return (
    <main className="flex flex-1 flex-col gap-6">
      <div className="grid gap-6 lg:grid-cols-[1fr,360px]">
        <PromptFilters
          collectionId={collectionId}
          searchValue={search}
          collections={collections}
          loading={isLoading || isCollectionsLoading}
          error={collectionsError}
          onCollectionChange={onCollectionChange}
          onSearchChange={setSearch}
        />
        <PromptForm
          collections={collections}
          onSave={handleCreate}
          isSubmitting={isSubmitting}
        />
      </div>

      <section className="space-y-4">
        <div className="flex flex-col gap-1">
          <p className="text-xs uppercase tracking-[0.3em] text-slate-500">Prompts</p>
          <h2 className="text-2xl font-semibold">
            {prompts.length} prompt{prompts.length === 1 ? "" : "s"} stored
          </h2>
        </div>
        <PromptList
          prompts={prompts}
          status={status}
          error={error}
          searchQuery={search}
          onPromptSelect={handlePromptSelect}
        />
      </section>

      <PromptDetail
        prompt={activePrompt}
        isOpen={Boolean(activePrompt)}
        onClose={handleCloseDetail}
      />
    </main>
  );
};

export default PromptsPage;
