function Button({ children, variant = "primary", onClick, type = "button" }) {
  return (
    <button
      className={`button button-${variant}`}
      onClick={onClick}
      type={type}
    >
      {children}
    </button>
  );
}

export default Button;