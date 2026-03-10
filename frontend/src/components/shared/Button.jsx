const VARIANT_STYLES = {
  primary: "bg-sky-500 text-white shadow hover:bg-sky-400 focus-visible:outline-sky-300",
  secondary: "bg-slate-800 text-slate-100 hover:bg-slate-700 focus-visible:outline-slate-400",
  ghost: "bg-transparent text-slate-100 hover:bg-slate-900/70 focus-visible:outline-slate-300",
};

const Button = ({
  children,
  variant = "primary",
  className = "",
  type = "button",
  ...rest
}) => {
  const variantClass = VARIANT_STYLES[variant] ?? VARIANT_STYLES.primary;
  return (
    <button
      type={type}
      className={`inline-flex items-center justify-center rounded-2xl px-4 py-2 text-sm font-semibold shadow transition focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 ${variantClass} ${className}`}
      {...rest}
    >
      {children}
    </button>
  );
};

export default Button;
