import { useState } from "react";
import Layout from "./components/layout/Layout";
import PromptsPage from "./pages/PromptsPage";

function App() {
  const [collectionId, setCollectionId] = useState("");

  return (
    <Layout
      selectedCollectionId={collectionId}
      onCollectionSelect={setCollectionId}
    >
      <PromptsPage
        collectionId={collectionId}
        onCollectionChange={setCollectionId}
      />
    </Layout>
  );
}

export default App;
