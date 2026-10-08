from sqlalchemy import ForeignKey, String, Text, Float
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Recipe(Base):
    __tablename__ = "recipes"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    instructions: Mapped[str | None] = mapped_column(Text)
    preparation_time: Mapped[str | None] = mapped_column(String)
    cooking_time: Mapped[str | None] = mapped_column(String)
    servings: Mapped[str | None] = mapped_column(String)

    ingredients: Mapped[list["RecipeIngredient"]] = relationship(
        back_populates="recipe"
    )


class Ingredient(Base):
    __tablename__ = "ingredients"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(
        String,
        nullable=False,
        unique=True
    )

    recipes: Mapped[list["RecipeIngredient"]] = relationship(
        back_populates="ingredient"
    )


class RecipeIngredient(Base):
    __tablename__ = "recipe_ingredients"

    recipe_id: Mapped[int] = mapped_column(
        ForeignKey("recipes.id"),
        primary_key=True
    )

    ingredient_id: Mapped[int] = mapped_column(
        ForeignKey("ingredients.id"),
        primary_key=True
    )

    recipe: Mapped["Recipe"] = relationship(
        back_populates="ingredients"
    )

    ingredient: Mapped["Ingredient"] = relationship(
        back_populates="recipes"
    )

    amount: Mapped[str | None] = mapped_column(String)

    unit: Mapped[str | None] = mapped_column(String)