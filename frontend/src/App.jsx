import { useState, useEffect } from "react";
import axios from "axios";
import RecipeCard from "./components/RecipeCard.jsx";
import RecipeFilters from "./components/RecipeFilters.jsx";
import StatusCard from "./components/StatusCard.jsx";
import useRecipeFilters from "./hooks/useRecipeFilters.js";
import useRecipes from "./hooks/useRecipes.js";

const App = () => {
  const [apiError, setApiError] = useState("");
  const [dbError, setDbError] = useState("");
  const [expandedRecipeId, setExpandedRecipeId] = useState(null);
  const {
    recipes,
    isLoading: recipesLoading,
    error: recipesError,
  } = useRecipes();
  const {
    addIngredientFilter,
    filteredRecipes,
    ingredientFilters,
    removeIngredientFilter,
    searchTerm,
    setSearchTerm,
    updateIngredientFilter,
  } = useRecipeFilters(recipes);

  useEffect(() => {
    const loadData = async () => {
      const [apiResponse, dbResponse] = await Promise.allSettled([
        axios.get("/api/"),
        axios.get("/api/db-health"),
      ]);

      if (apiResponse.status === "rejected") {
        console.error(apiResponse.reason);
        setApiError(apiResponse.reason.message);
      }

      if (dbResponse.status === "rejected") {
        console.error(dbResponse.reason);
        setDbError(dbResponse.reason.message);
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
      <StatusCard
        apiError={apiError}
        dbError={dbError}
        recipesError={recipesError}
      />
      {recipesLoading ? <p>Loading recipes...</p> : null}
      <RecipeFilters
        ingredientFilters={ingredientFilters}
        onAddIngredient={addIngredientFilter}
        onIngredientChange={updateIngredientFilter}
        onRemoveIngredient={removeIngredientFilter}
        onSearchChange={setSearchTerm}
        searchTerm={searchTerm}
      />
      {!recipesLoading && !recipesError
        ? filteredRecipes.map((recipe) => (
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
          ))
        : null}
      {!recipesLoading && !recipesError && filteredRecipes.length === 0 ? (
        <p style={{ color: "#64748b" }}>No recipes found.</p>
      ) : null}
    </div>
  );
};

export default App;
