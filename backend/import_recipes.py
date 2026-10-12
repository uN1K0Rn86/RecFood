import argparse
import asyncio
import json
from pathlib import Path

from sqlalchemy import select


BASE_DIR = Path(__file__).resolve().parent

with (BASE_DIR / "ingredient_overrides.json").open(encoding="utf-8") as file:
    INGREDIENT_OVERRIDES = json.load(file)


def get_best_lemma(token_data):
    token = token_data["token"].lower()
    override = INGREDIENT_OVERRIDES.get(token)
    if override:
        return override

    candidates = []
    for analysis in token_data.get("analysis", []):
        if analysis.get("CLASS") != "nimisana":
            continue

        baseform = analysis.get("BASEFORM", "").lower()
        if baseform and baseform not in candidates:
            candidates.append(baseform)

    if len(candidates) > 1:
        print(
            f"WARNING: ambiguous token {token!r}; "
            f"selected {candidates[0]!r} from {candidates!r}"
        )

    return candidates[0] if candidates else token


def get_ingredient_name(ingredient_data):
    token_data = ingredient_data.get("lemmatized", [])
    if not token_data:
        return ingredient_data.get("name", "").strip().lower()

    lemmas = [get_best_lemma(token) for token in token_data]
    return " ".join(dict.fromkeys(lemmas))


def normalize_amount(amount):
    return "" if amount is None else str(amount)


def print_dry_run(recipes):
    for recipe in recipes:
        print(f"\nRecipe: {recipe['name']}")
        for ingredient_data in recipe.get("ingredients", []):
            amount = normalize_amount(ingredient_data.get("amount"))
            unit = ingredient_data.get("unit") or ""
            quantity = " ".join(value for value in (amount, unit) if value)
            quantity_text = f" ({quantity})" if quantity else ""
            print(
                f"  {ingredient_data.get('name', '')!r} -> "
                f"{get_ingredient_name(ingredient_data)!r}{quantity_text}"
            )


async def import_recipes(recipes):
    from database import SessionLocal
    from models import Ingredient, Recipe, RecipeIngredient

    async with SessionLocal.begin() as session:
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

            for ingredient_data in recipe_data.get("ingredients", []):
                ingredient_name = get_ingredient_name(ingredient_data)
                if not ingredient_name:
                    continue

                result = await session.execute(
                    select(Ingredient).where(Ingredient.name == ingredient_name)
                )
                ingredient = result.scalar_one_or_none()

                if ingredient is None:
                    ingredient = Ingredient(name=ingredient_name)
                    session.add(ingredient)
                    await session.flush()

                existing_relation = await session.execute(
                    select(RecipeIngredient).where(
                        RecipeIngredient.recipe_id == recipe.id,
                        RecipeIngredient.ingredient_id == ingredient.id,
                    )
                )
                if existing_relation.scalar_one_or_none() is None:
                    session.add(
                        RecipeIngredient(
                            recipe_id=recipe.id,
                            ingredient_id=ingredient.id,
                            amount=normalize_amount(
                                ingredient_data.get("amount")
                            ),
                            unit=ingredient_data.get("unit") or "",
                        )
                    )


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview ingredient mappings without changing the database",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    with (BASE_DIR / "recipes_tokenized.json").open(encoding="utf-8") as file:
        recipes = json.load(file)

    if args.dry_run:
        print_dry_run(recipes)
    else:
        asyncio.run(import_recipes(recipes))


if __name__ == "__main__":
    main()
