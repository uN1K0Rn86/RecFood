import { useMemo, useState } from "react";

const useRecipeFilters = (recipes) => {
  const [searchTerm, setSearchTerm] = useState("");
  const [ingredientFilters, setIngredientFilters] = useState([""]);

  const filteredRecipes = useMemo(
    () =>
      recipes.filter((recipe) => {
        const matchesName = recipe.name
          .toLowerCase()
          .includes(searchTerm.trim().toLowerCase());
        const recipeIngredients = recipe.ingredients.map(({ ingredient }) =>
          ingredient.name.toLowerCase(),
        );
        const matchesIngredients = ingredientFilters
          .filter((filter) => filter.trim())
          .every((filter) =>
            recipeIngredients.some((ingredient) =>
              ingredient.includes(filter.trim().toLowerCase()),
            ),
          );

        return matchesName && matchesIngredients;
      }),
    [ingredientFilters, recipes, searchTerm],
  );

  const updateIngredientFilter = (index, value) => {
    setIngredientFilters((currentFilters) =>
      currentFilters.map((filter, filterIndex) =>
        filterIndex === index ? value : filter,
      ),
    );
  };

  const addIngredientFilter = () => {
    setIngredientFilters((currentFilters) => [...currentFilters, ""]);
  };

  const removeIngredientFilter = (indexToRemove) => {
    setIngredientFilters((currentFilters) =>
      currentFilters.filter((_, index) => index !== indexToRemove),
    );
  };

  return {
    addIngredientFilter,
    filteredRecipes,
    ingredientFilters,
    removeIngredientFilter,
    searchTerm,
    setSearchTerm,
    updateIngredientFilter,
  };
};

export default useRecipeFilters;
