from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from database import get_db
from models import Recipe, RecipeIngredient


app = FastAPI(title="RecFood API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "RecFood API is running"}


@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/db-health")
async def db_health(db: AsyncSession = Depends(get_db)):
    result = await db.execute(text("SELECT 1"))
    return {"database": result.scalar_one()}

@app.get("/recipes")
async def get_recipes(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Recipe)
        .options(
            selectinload(Recipe.ingredients)
            .selectinload(RecipeIngredient.ingredient)
        )
        .order_by(Recipe.id)
    )
    recipes = result.scalars().all()

    return [
        {
            "id": recipe.id,
            "name": recipe.name,
            "instructions": recipe.instructions,
            "preparation_time": recipe.preparation_time,
            "cooking_time": recipe.cooking_time,
            "servings": recipe.servings,
            "ingredients": [
                {
                    "recipe_id": relation.recipe_id,
                    "ingredient_id": relation.ingredient_id,
                    "ingredient": {
                        "id": relation.ingredient.id,
                        "name": relation.ingredient.name,
                    },
                }
                for relation in recipe.ingredients
            ],
        }
        for recipe in recipes
    ]