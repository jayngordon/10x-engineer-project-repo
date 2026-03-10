const ErrorMessage = ({ message }) => (
  <div className="rounded-2xl border border-rose-500/70 bg-rose-500/10 px-4 py-3 text-sm text-rose-200">
    <strong className="block text-xs uppercase tracking-[0.4em] text-rose-300">Error</strong>
    <p>{message}</p>
  </div>
);

export default ErrorMessage;
