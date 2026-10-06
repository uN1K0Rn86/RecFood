import Button from "./Button.jsx";
import Card from "./Card.jsx";
import Input from "./Input.jsx";

const RecipeFilters = ({
  ingredientFilters,
  onAddIngredient,
  onIngredientChange,
  onRemoveIngredient,
  onSearchChange,
  searchTerm,
}) => (
  <Card>
    <h1 style={{ fontSize: "1.5rem", margin: "0 0 1.25rem" }}>
      Find a recipe
    </h1>
    <Input
      onChange={(event) => onSearchChange(event.target.value)}
      placeholder="Filter recipes by name"
      style={{
        border: "1px solid #cbd5e1",
        borderRadius: "8px",
        boxSizing: "border-box",
        fontSize: "1rem",
        padding: "0.7rem 0.85rem",
        width: "100%",
      }}
      value={searchTerm}
    />
    <div style={{ marginTop: "1.25rem" }}>
      <p style={{ fontWeight: "600", margin: "0 0 0.75rem" }}>
        Filter by ingredients
      </p>
      {ingredientFilters.map((filter, index) => (
        <div
          key={index}
          style={{
            alignItems: "center",
            display: "flex",
            gap: "0.5rem",
            marginBottom: "0.5rem",
          }}
        >
          <Input
            onChange={(event) =>
              onIngredientChange(index, event.target.value)
            }
            placeholder={`Ingredient ${index + 1}`}
            style={{
              border: "1px solid #cbd5e1",
              borderRadius: "8px",
              boxSizing: "border-box",
              flex: "1",
              padding: "0.65rem 0.75rem",
            }}
            value={filter}
          />
          {ingredientFilters.length > 1 ? (
            <Button
              aria-label={`Remove ingredient filter ${index + 1}`}
              onClick={() => onRemoveIngredient(index)}
              style={{
                backgroundColor: "transparent",
                border: "none",
                color: "#64748b",
                cursor: "pointer",
                padding: "0.5rem",
              }}
            >
              ×
            </Button>
          ) : null}
        </div>
      ))}
      <Button
        onClick={onAddIngredient}
        style={{
          backgroundColor: "#e0f2fe",
          border: "none",
          borderRadius: "8px",
          color: "#0369a1",
          cursor: "pointer",
          fontWeight: "600",
          padding: "0.65rem 0.9rem",
        }}
      >
        + Add ingredient
      </Button>
    </div>
  </Card>
);

export default RecipeFilters;
