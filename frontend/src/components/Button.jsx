const Button = ({ type = "button", children, ...props }) => (
  <button {...props} type={type}>
    {children}
  </button>
);

export default Button;