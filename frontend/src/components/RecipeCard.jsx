import Button from "./Button.jsx";
import Card from "./Card.jsx";

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
          isExpanded ? `Collapse ${recipe.name}` : `Expand ${recipe.name}`
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
          Preparation: {recipe.preparation_time} | Cooking:{" "}
          {recipe.cooking_time} | Servings: {recipe.servings}
        </p>
        <ul>
          {recipe.ingredients.map(({ amount, ingredient, unit }) => (
            <li key={ingredient.id}>
              {amount && amount !== "None"
                ? `${amount}${unit ? ` ${unit}` : ""} `
                : ""}
              {ingredient.name}
            </li>
          ))}
        </ul>
      </div>
    ) : null}
  </Card>
);

export default RecipeCard;
