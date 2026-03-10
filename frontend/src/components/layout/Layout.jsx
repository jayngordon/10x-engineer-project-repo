import Header from "./Header";
import Sidebar from "./Sidebar";

const Layout = ({
  children,
  selectedCollectionId,
  onCollectionSelect = () => {},
}) => (
  <div className="min-h-screen bg-slate-950 text-slate-100">
    <div className="mx-auto flex max-w-7xl flex-col gap-6 p-6">
      <Header />
      <div className="grid gap-6 lg:grid-cols-[280px,1fr]">
        <Sidebar
          selectedCollectionId={selectedCollectionId}
          onCollectionSelect={onCollectionSelect}
        />
        <div className="space-y-6">{children}</div>
      </div>
    </div>
  </div>
);

export default Layout;
