import { useEffect, useState } from "react";
import { fetchRecipes } from "../api/recipes.js";

const useRecipes = () => {
  const [recipes, setRecipes] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    let isMounted = true;

    const loadRecipes = async () => {
      try {
        setIsLoading(true);
        setError("");

        const data = await fetchRecipes();

        if (isMounted) {
          setRecipes(data);
        }
      } catch (error) {
        if (isMounted) {
          setError(error.message || "Failed to load recipes.");
        }
      } finally {
        if (isMounted) {
          setIsLoading(false);
        }
      }
    };

    loadRecipes();

    return () => {
      isMounted = false;
    };
  }, []);

  return { recipes, isLoading, error };
};

export default useRecipes;
