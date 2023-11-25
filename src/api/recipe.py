import sqlalchemy
from src import database as db
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.api import auth

router = APIRouter(
    prefix="/recipe",
    tags=["recipe"]
)

class RecipeRequestObject(BaseModel):
    protein : int
    calories : int
    vegan : bool
    vegetarian : bool
    paleo : bool
    carbs : int
    servings : int
    time_to_make : int

@router.post("/get_recipe")
def get_recipes(user_id : int, recipe_constraints : RecipeRequestObject):
    with db.engine.begin() as connection:
        final_recipes = []
        recipes = connection.execute(sqlalchemy.text(
        """
        SELECT recipe_id
        FROM recipe
        WHERE protein >= :protein 
        AND calories >= :calories
        AND vegan = :vegan
        AND vegetarian = :vegetarian
        AND paleo = :paleo
        AND carbs >= :carbs
        AND time_to_make <= :time_to_make
        """
        ), [{ "protein": recipe_constraints.protein, 
             "calories": recipe_constraints.calories, 
             "vegan": recipe_constraints.vegan, 
             "vegetarian": recipe_constraints.vegetarian, 
             "paleo": recipe_constraints.paleo, 
             "carbs": recipe_constraints.carbs, 
            "time_to_make": recipe_constraints.time_to_make}]).all()

        for recipe_id in recipes:

        #get recipe quant and fridge quant
            ingredients = connection.execute(sqlalchemy.text(
            """
            WITH fridgeIngred AS(
                SELECT ingredient_id, quantity AS fridge_quant
                FROM fridge
                WHERE user_id = :user_id
                )
            SELECT recipe_ingredients.ingredient_id, fridgeIngred.fridge_quant AS fridge_quant, quantity AS recipe_quant
            FROM recipe_ingredients
            LEFT JOIN fridgeIngred
            ON recipe_ingredients.ingredient_id = fridgeIngred.ingredient_id
            WHERE recipe_id = :recipe
            """
            ), [{"recipe": recipe_id, "user_id": user_id}]).all()

            num_ingredients = connection.execute(sqlalchemy.text(
                """
                SELECT COUNT(ingredient_id) AS num_ingredients
                FROM recipe_ingredients
                WHERE recipe_id = :recipe_id
                """
            ), [{"recipe": recipe_id}]).scalar_one()

            good_ingredients = 0

            for ingredient in ingredients:
                if ingredient.fridge_quant is not None & ingredient.fridge_quant >= ingredient.recipe_quant:
                    good_ingredient += 1

            if good_ingredients == num_ingredients:
                recipe = connection.execute(sqlalchemy.text(
                """
                SELECT recipe_id, sku, name, steps
                FROM recipe
                WHERE recipe_id = :recipe
                """
                ), [{"recipe": recipe_id}]).first()

                final_recipes.append(
                {"recipe_id": recipe.recipe_id,
                "sku": recipe.sku,
                "name": recipe.name,
                "steps": recipe.steps}
                )


    if len(final_recipes) == 0:
        return "no recipes available"
    return final_recipes