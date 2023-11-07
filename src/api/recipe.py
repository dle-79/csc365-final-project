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
        AND time_to_make >= :time_to_make
        """
        ), [{ "protein": recipe_constraints.protein, 
             "calories": recipe_constraints.calories, 
             "vegan": recipe_constraints.vegan, 
             "vegetarian": recipe_constraints.vegetarian, 
             "paleo": recipe_constraints.paleo, 
             "carbs": recipe_constraints.carbs, 
            "time_to_make": recipe_constraints.time_to_make}]).all()

        for recipe_id in recipes:
        #counts number of ingredients that you have enough of
            good_ingredients = 0

        #checks if you have ingredients in pantry
            ingredient_count = connection.execute(sqlalchemy.text(
            """
            SELECT COUNT(ingredient_id) AS numIngredient
            FROM recipe_ingredients
            WHERE recipe_id = :recipe
            """
            ), [{"recipe": recipe_id[0]}]).scalar_one()

            pantry_count = connection.execute(sqlalchemy.text(
            """
            SELECT COUNT(fridge.ingredient_id) AS numPantry
            FROM fridge
            JOIN recipe_ingredients
            ON recipe_ingredients.ingredient_id = fridge.ingredient_id
            WHERE user_id = :user_id
            """
            ), [{"user_id": user_id}]).scalar_one()

            if pantry_count < ingredient_count:
                continue

            #add ingredients from recipe to a list
            ingredient_ids = connection.execute(sqlalchemy.text(
            """
            SELECT ingredient_id
            FROM recipe_ingredients
            WHERE recipe_id = :recipe
            """
            ), [{"recipe": recipe_id[0]}]).all()

            for ingredient_id in ingredient_ids:
                #checks if you have enough of each ingredient
                recipe_quant = connection.execute(sqlalchemy.text(
                """
                SELECT quantity
                FROM recipe_ingredients
                WHERE recipe_id = :recipe
                AND ingredient_id = :ingredient
                """
                ), [{"recipe": recipe_id[0],
                "ingredient": ingredient_id[0]}]).scalar_one()

                fridge_quant = connection.execute(sqlalchemy.text(
                """
                SELECT quantity
                FROM fridge
                WHERE user_id = :user_id
                AND ingredient_id = :ingredient
                """ 
                ), [{"user_id": user_id,
                "ingredient": ingredient_id[0]}]).first()
                
                if recipe_quant is None:
                    recipe_quant = 0

                if fridge_quant is None:
                    fridge_quant = 0
                else:
                    fridge_quant = fridge_quant.quantity

                if fridge_quant >= recipe_quant:
                    good_ingredients += 1

            if good_ingredients == ingredient_count:
                recipe = connection.execute(sqlalchemy.text(
                """
                SELECT recipe_id, sku, name, steps
                FROM recipe
                WHERE recipe_id = :recipe
                """
                ), [{"recipe": recipe_id[0]}]).first()

                final_recipes.append(
                {"recipe_id": recipe.recipe_id,
                "sku": recipe.sku,
                "name": recipe.name,
                "steps": recipe.steps}
                )


    if len(final_recipes) == 0:
        return "no recipes available"
    return final_recipes