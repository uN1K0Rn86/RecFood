import asyncio
import json

from sqlalchemy import select

from database import SessionLocal
from models import Recipe, Ingredient, RecipeIngredient

def get_baseform(ingredient_data):
    baseforms = []
    for lemmatized in ingredient_data["lemmatized"]:
        for analysis in lemmatized["analysis"]:
            if analysis.get("CLASS") == "nimisana":
                baseform = analysis["BASEFORM"].lower()

                if baseform not in baseforms:
                    baseforms.append(baseform)

    return baseforms

async def import_recipes():
    with open("recipes_tokenized.json", "r", encoding="utf-8") as file:
        recipes = json.load(file)

    async with SessionLocal() as session:
        for recipe_data in recipes:

            instructions = recipe_data.get("instructions")
            if isinstance(instructions, list):
                instructions = "\n".join(instructions)
            
            recipe = Recipe(
                name=recipe_data["name"],
                instructions=instructions,
                preparation_time=recipe_data.get("preparation_time"),
                cooking_time=recipe_data.get("cooking_time"),
                servings=recipe_data.get("servings"),
            )
            session.add(recipe)
            await session.flush()

            for ingredient_data in recipe_data["ingredients"]:
                baseforms = get_baseform(ingredient_data)

                #testailua
                #print(ingredient_data["name"], "->", baseforms)

                if not baseforms:
                    continue

                for baseform in baseforms:
                    result = await session.execute(
                        select(Ingredient).where(Ingredient.name == baseform)
                    )

                    ingredient = result.scalar_one_or_none()

                    if ingredient is None:
                        ingredient = Ingredient(name=baseform)
                        session.add(ingredient)
                        await session.flush()

                    existing_relation = await session.execute(
                        select(RecipeIngredient).where(
                            RecipeIngredient.recipe_id == recipe.id,
                            RecipeIngredient.ingredient_id == ingredient.id,
                        )
                    )

                    relation = existing_relation.scalar_one_or_none()

                    if relation is None:
                        relation = RecipeIngredient(
                            recipe_id=recipe.id,
                            ingredient_id=ingredient.id,
                            amount=recipe_data.get("amount"),
                            unit=recipe_data.get("unit"),
                        )

                        session.add(relation)

        await session.commit()

asyncio.run(import_recipes())
