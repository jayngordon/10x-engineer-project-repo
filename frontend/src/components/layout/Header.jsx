import HealthStatus from "../HealthStatus";
import Button from "../shared/Button";

const Header = () => (
  <header className="flex flex-col gap-4 rounded-3xl border border-slate-800 bg-slate-950/70 p-6 shadow-lg shadow-slate-900/40 md:flex-row md:items-center md:justify-between">
    <div>
      <p className="text-xs uppercase tracking-[0.5em] text-slate-500">PromptLab</p>
      <h1 className="text-3xl font-semibold text-white">Prompt Engineering Workspace</h1>
      <p className="text-sm text-slate-400">
        Catalog, categorize, and preview prompts without leaving your browser.
      </p>
    </div>
    <div className="flex items-center gap-3">
      <HealthStatus />
      <a
        className="rounded-2xl border border-slate-800 px-4 py-2 text-xs font-semibold uppercase tracking-widest text-slate-300 transition hover:border-slate-600"
        href="http://localhost:8000/docs"
        target="_blank"
        rel="noreferrer"
      >
        API Docs
      </a>
    </div>
  </header>
);

export default Header;
