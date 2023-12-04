import sqlalchemy
from src import database as db
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.api import auth

router = APIRouter(
    prefix="/recipe",
    tags=["recipe"]
)

class RecipeMarcosObject(BaseModel):
    min_protein: int = 0
    max_protein: int = 10000000
    min_calories: int = 0
    max_calories: int = 100000
    vegan: bool = False
    vegetarian: bool = False
    paleo: bool = False
    min_carbs: int = 0
    max_carbs: int = 1000000
    max_time_to_make : int = 10000
    country_origin: str = "United States"
    meal_type: str = "Dinner"

@router.post("/get_recipe_macros")
def get_recipes_parameter(recipe_constraints : RecipeMarcosObject):
    final_recipes = []
    with db.engine.begin() as connection:
        recipes = connection.execute(sqlalchemy.text(
        """
        SELECT recipe_id, name, steps
        FROM recipe
        WHERE protein >= :min_protein 
        AND protein <= :max_protein 
        AND calories >= :min_calories 
        AND calories <= :max_calories
        AND  carbs >= :min_carbs
        AND carbs <= :max_carbs
        AND paleo = :paleo
        AND vegan = :vegan
        AND vegetarian = :vegetarian
        AND time_to_make <= :max_time_to_make
        AND country_origin = :country_origin
        AND meal_type = :meal_type
        LIMIT 10
        """
        ), [{ "min_protein": recipe_constraints.min_protein, 
            "max_protein": recipe_constraints.max_protein, 
             "min_calories": recipe_constraints.min_calories,
             "max_calories": recipe_constraints.max_calories, 
             "min_carbs": recipe_constraints.min_carbs,
             "max_carbs": recipe_constraints.max_carbs, 
             "vegan": recipe_constraints.vegan, 
             "vegetarian": recipe_constraints.vegetarian, 
             "paleo": recipe_constraints.paleo, 
            "max_time_to_make": recipe_constraints.max_time_to_make,
            "country_origin": recipe_constraints.country_origin,
            "meal_type": recipe_constraints.meal_type}]).all()

        for recipe_id in recipes:
            ingredient_list = []
            ingredients = connection.execute(sqlalchemy.text(
                """ SELECT name, recipe_ingredients.quantity AS quant, units
                FROM ingredient
                JOIN recipe_ingredients
                ON ingredient.ingredient_id = recipe_ingredients.ingredient_id
                WHERE recipe_ingredients.recipe_id = :recipe_id"""),
                [{"recipe_id": recipe_id.recipe_id}]).all()
            for ingredient in ingredients:
                ingredient_list.append(ingredient.name + str(ingredient.quant) + ingredient.units)

            final_recipes.append({
                "recipe_id": recipe_id.recipe_id,
                "ingredients": ingredient_list,
                "name": recipe_id.name,
                "steps": recipe_id.steps}
                )


    if len(final_recipes) == 0:
        return "no recipes available"
    return final_recipes


@router.post("/get_recipe_name")
def get_recipes_by_name(recipe_name: str):
    final_recipes = []
    recipe_name = recipe_name.lower()
    recipe_name = recipe_name.title()
    with db.engine.begin() as connection:
        recipes = connection.execute(sqlalchemy.text(
        """
        SELECT recipe_id, name, steps
        FROM recipe
        WHERE name LIKE ":name%"
        LIMIT 10
        """
        ), [{ "name": recipe_name}]).all()

        for recipe_id in recipes:
            ingredient_list = []
            ingredients = connection.execute(sqlalchemy.text(
                """ SELECT name, recipe_ingredients.quantity AS quant, units
                FROM ingredient
                JOIN recipe_ingredients
                ON ingredient.ingredient_id = recipe_ingredients.ingredient_id
                WHERE recipe_ingredients.recipe_id = :recipe_id"""),
                [{"recipe_id": recipe_id.recipe_id}]).all()
            for ingredient in ingredients:
                ingredient_list.append({
                    "ingredient": ingredient.name,
                    "quantity": ingredient.quant,
                    "units": ingredient.units
                })

            final_recipes.append({
                "recipe_id": recipe_id.recipe_id,
                "ingredients": ingredient_list,
                "name": recipe_id.name,
                "steps": recipe_id.steps}
                )


    if len(final_recipes) == 0:
        return "no recipes available"
    return final_recipes


# @router.post("/check_recipe_ingredient")
# def get_recipes_parameter(user_id: int, recipe_id: int):

#     #get recipe quant and fridge quant
#             ingredients = connection.execute(sqlalchemy.text(
#             """
#             WITH fridgeIngred AS(
#                 SELECT ingredient_id, quantity AS fridge_quant
#                 FROM fridge
#                 WHERE user_id = :user_id
#                 )
#             SELECT recipe_ingredients.ingredient_id, fridgeIngred.fridge_quant AS fridge_quant, quantity AS recipe_quant
#             FROM recipe_ingredients
#             LEFT JOIN fridgeIngred
#             ON recipe_ingredients.ingredient_id = fridgeIngred.ingredient_id
#             WHERE recipe_id = :recipe
#             """
#             ), [{"recipe": recipe_id, "user_id": user_id}]).all()

#             num_ingredients = connection.execute(sqlalchemy.text(
#                 """
#                 SELECT COUNT(ingredient_id) AS num_ingredients
#                 FROM recipe_ingredients
#                 WHERE recipe_id = :recipe_id
#                 """
#             ), [{"recipe": recipe_id}]).scalar_one()

#             good_ingredients = 0

#             for ingredient in ingredients:
#                 if ingredient.fridge_quant is not None & ingredient.fridge_quant >= ingredient.recipe_quant:
#                     good_ingredient += 1

#             if good_ingredients == num_ingredients:
#                 recipe = connection.execute(sqlalchemy.text(
#                 """
#                 SELECT recipe_id, sku, name, steps
#                 FROM recipe
#                 WHERE recipe_id = :recipe
#                 """
#                 ), [{"recipe": recipe_id}]).first()