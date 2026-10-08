import axios from "axios";

const api = axios.create({
  baseURL: "/api",
});

export const fetchRecipes = async () => {
  const response = await api.get("/recipes");
  return response.data;
};
