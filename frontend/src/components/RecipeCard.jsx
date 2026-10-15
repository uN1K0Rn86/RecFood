import Button from "./Button.jsx";
import Card from "./Card.jsx";

const formatAmount = (amount) => {
  if (!amount || amount === "None") {
    return "";
  }

  const numericAmount = Number(amount);
  return Number.isFinite(numericAmount) ? String(numericAmount) : amount;
};

const RecipeCard = ({ isExpanded, onToggle, recipe }) => (
  <Card>
    <div
      style={{
        alignItems: "center",
        display: "flex",
        gap: "0.5rem",
        justifyContent: "space-between",
      }}
    >
      <h2 style={{ fontSize: "1.2rem", margin: 0 }}>{recipe.name}</h2>
      <Button
        aria-label={
          isExpanded ? `Supista ${recipe.name}` : `Laajenna ${recipe.name}`
        }
        onClick={onToggle}
        style={{
          backgroundColor: "#e0f2fe",
          border: "none",
          borderRadius: "50%",
          color: "#0369a1",
          cursor: "pointer",
          fontSize: "1rem",
          height: "2rem",
          width: "2rem",
        }}
      >
        {isExpanded ? "^" : "v"}
      </Button>
    </div>
    {isExpanded ? (
      <div
        style={{
          borderTop: "1px solid #e2e8f0",
          marginTop: "1rem",
          paddingTop: "1rem",
        }}
      >
        <p>{recipe.instructions}</p>
        <p>
          Valmisteluaika: {recipe.preparation_time} | Kypsennysaika:{" "}
          {recipe.cooking_time} | Annoksia: {recipe.servings}
        </p>
        <ul
          style={{
            display: "grid",
            gap: "0.6rem",
            gridTemplateColumns: "repeat(auto-fit, minmax(12rem, 1fr))",
            listStyle: "none",
            margin: "1rem 0 0",
            padding: 0,
          }}
        >
          {recipe.ingredients.map(({ amount, ingredient, unit }) => (
            <li
              key={ingredient.id}
              style={{
                alignItems: "center",
                backgroundColor: "#f8fafc",
                border: "1px solid #e2e8f0",
                borderRadius: "10px",
                display: "flex",
                gap: "0.65rem",
                minHeight: "2.75rem",
                padding: "0.55rem 0.7rem",
              }}
            >
              {formatAmount(amount) ? (
                <span
                  style={{
                    backgroundColor: "#dbeafe",
                    borderRadius: "999px",
                    color: "#1d4ed8",
                    flexShrink: 0,
                    fontSize: "0.85rem",
                    fontWeight: "700",
                    padding: "0.25rem 0.5rem",
                  }}
                >
                  {formatAmount(amount)}
                  {unit ? ` ${unit}` : ""}
                </span>
              ) : null}
              <span style={{ fontWeight: "500" }}>{ingredient.name}</span>
            </li>
          ))}
        </ul>
      </div>
    ) : null}
  </Card>
);

export default RecipeCard;
