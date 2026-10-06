import { useState, useEffect } from "react";
import axios from "axios";
import RecipeCard from "./components/RecipeCard.jsx";
import RecipeFilters from "./components/RecipeFilters.jsx";
import StatusCard from "./components/StatusCard.jsx";
import dummyRecipes from "./data/recipes.js";
import useRecipeFilters from "./hooks/useRecipeFilters.js";

const App = () => {
  const [message, setMessage] = useState("");
  const [dbHealth, setDbHealth] = useState("");
  const [error, setError] = useState("");
  const [expandedRecipeId, setExpandedRecipeId] = useState(null);
  const {
    addIngredientFilter,
    filteredRecipes,
    ingredientFilters,
    removeIngredientFilter,
    searchTerm,
    setSearchTerm,
    updateIngredientFilter,
  } = useRecipeFilters(dummyRecipes);

  useEffect(() => {
    const loadData = async () => {
      try {
        const [messageResponse, dbResponse] = await Promise.all([
          axios.get("http://127.0.0.1:8000/"),
          axios.get("http://127.0.0.1:8000/db-health"),
        ]);

        setMessage(messageResponse.data.message);
        setDbHealth(String(dbResponse.data.database));
      } catch (error) {
        console.error(error);
        setError(error.message);
      }
    };

    loadData();
  }, []);

  return (
    <div
      style={{
        alignItems: "center",
        backgroundColor: "#f8fafc",
        color: "#1e293b",
        display: "flex",
        flexDirection: "column",
        gap: "1rem",
        justifyContent: "flex-start",
        minHeight: "100vh",
        padding: "2rem 1rem 4rem",
      }}
    >
      <StatusCard dbHealth={dbHealth} error={error} message={message} />
      <RecipeFilters
        ingredientFilters={ingredientFilters}
        onAddIngredient={addIngredientFilter}
        onIngredientChange={updateIngredientFilter}
        onRemoveIngredient={removeIngredientFilter}
        onSearchChange={setSearchTerm}
        searchTerm={searchTerm}
      />
      {filteredRecipes.map((recipe) => (
        <RecipeCard
          isExpanded={expandedRecipeId === recipe.id}
          key={recipe.id}
          onToggle={() =>
            setExpandedRecipeId((currentId) =>
              currentId === recipe.id ? null : recipe.id,
            )
          }
          recipe={recipe}
        />
      ))}
      {filteredRecipes.length === 0 ? (
        <p style={{ color: "#64748b" }}>No recipes found.</p>
      ) : null}
    </div>
  );
};

export default App;
