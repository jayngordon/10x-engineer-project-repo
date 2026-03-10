const SearchBar = ({
  value,
  onChange,
  placeholder = "Search",
  disabled = false,
}) => {
  return (
    <label className="w-full">
      <span className="sr-only">Search</span>
      <div className="flex items-center gap-2 rounded-2xl border border-slate-800 bg-slate-950/70 px-4 py-3 text-sm text-slate-200 focus-within:border-sky-400 focus-within:ring focus-within:ring-sky-500/30">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          className="h-5 w-5 text-slate-500"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 21l-4.35-4.35m0 0A7.5 7.5 0 1110.5 3a7.5 7.5 0 016.15 12.65z" />
        </svg>
        <input
          className="flex-1 bg-transparent outline-none"
          type="search"
          value={value}
          onChange={(event) => onChange(event.target.value)}
          placeholder={placeholder}
          disabled={disabled}
        />
      </div>
    </label>
  );
};

export default SearchBar;
