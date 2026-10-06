const Card = ({ children, ...props }) => (
  <div
    {...props}
    style={{
      border: "1px solid #e5e7eb",
      borderRadius: "12px",
      boxShadow: "0 8px 24px rgba(15, 23, 42, 0.06)",
      padding: "1.5rem",
      width: "min(100%, 42rem)",
      boxSizing: "border-box",
      backgroundColor: "#ffffff",
      ...props.style,
    }}
  >
    {children}
  </div>
);

export default Card;
