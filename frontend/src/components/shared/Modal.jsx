import { Fragment } from "react";

const Modal = ({
  title,
  isOpen,
  onClose,
  children,
  size = "md",
}) => {
  if (!isOpen) {
    return null;
  }

  const sizeClasses = {
    sm: "max-w-md",
    md: "max-w-2xl",
    lg: "max-w-4xl",
  };

  return (
    <div className="fixed inset-0 z-40 flex items-center justify-center bg-slate-950/80 px-4 py-6">
      <div
        className={`w-full ${sizeClasses[size]} rounded-3xl border border-slate-800 bg-slate-950/90 p-6 shadow-2xl shadow-slate-900/60`}
      >
        <div className="mb-4 flex items-center justify-between">
          <h3 className="text-xl font-semibold text-white">{title}</h3>
          <button
            type="button"
            className="rounded-full border border-slate-700 px-3 py-1 text-xs uppercase tracking-[0.4em] text-slate-400 hover:border-slate-500"
            onClick={onClose}
          >
            Close
          </button>
        </div>
        {children}
      </div>
    </div>
  );
};

export default Modal;
