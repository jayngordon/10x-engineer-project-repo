import { useState } from "react";
import Button from "../shared/Button";
import Modal from "../shared/Modal";
import CollectionList from "../collections/CollectionList";
import CollectionForm from "../collections/CollectionForm";
import { useCollections } from "../../hooks/useCollections";

const Sidebar = ({ selectedCollectionId, onCollectionSelect = () => {} }) => {
  const { collections, status, error, reload } = useCollections();
  const [isModalOpen, setIsModalOpen] = useState(false);

  const handleCollectionCreated = async () => {
    await reload();
  };

  return (
    <aside className="space-y-6 rounded-3xl border border-slate-800 bg-slate-900/70 p-6 shadow-lg shadow-slate-900/40">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-xs uppercase tracking-[0.5em] text-slate-500">Collections</p>
          <h2 className="text-xl font-semibold text-white">Organize your prompts</h2>
        </div>
        <Button variant="secondary" onClick={() => setIsModalOpen(true)}>
          + New
        </Button>
      </div>
      <CollectionList
        collections={collections}
        status={status}
        error={error}
        selectedCollectionId={selectedCollectionId}
        onCollectionSelect={onCollectionSelect}
      />
      <Modal
        title="Create collection"
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
      >
        <CollectionForm
          onCreated={handleCollectionCreated}
          onClose={() => setIsModalOpen(false)}
        />
      </Modal>
    </aside>
  );
};

export default Sidebar;
