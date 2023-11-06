from fastapi import APIRouter
from pydantic import BaseModel
from src.database import engine
from sqlalchemy import text

router = APIRouter(
    prefix="/ingredients",
    tags=["ingredients"]
)


class RecipeRequest(BaseModel):
    recipe_id: int


def get_recipe_id(user_id: int, connection):
    query = text("SELECT recipe_id from recipe WHERE recipe_id = :recipe_id")
    binds = {"user_id": user_id}
    result = connection.execute(query, binds).scalar_one()
    return result


@router.post("/add_ingredients_to_recipe")
def add_to_recipe(ingredient_id: int, recipe_request: RecipeRequest):
    with engine.begin() as connection:
        recipe_id = get_recipe_id(RecipeRequest.recipe_id, connection)
        query = text(
            "SELECT ingredients from recipe WHERE recipe_id = :recipe_id"
        )
        binds = {"recipe_id": recipe_id}
        result = connection.execute(query, binds)
        if result:
            query = text(
                "INSERT INTO recipe(ingredients) VALUES ('{:ingredient_id}') WHERE recipe_id = :recipe_id"
            )
            binds = {
                "ingredient_id": ingredient_id,
                "recipe_id": recipe_id,
            }
            connection.execute(query, binds)
    

@router.post("/remove_ingredients_recipe")
def remove_ingredients_recipe(ingredient_id: int, recipe_request: RecipeRequest):
    recipe_id = get_recipe_id(RecipeRequest.recipe_id, connection)
    with engine.begin() as connection:
        query = text(
                """
                UPDATE recipe
                SET ingredients = ARRAY_DELETE (:ingredient_id)
                WHERE recipe_id = :recipe_id
                """)
        binds = {"recipe_id" : recipe_id,
                 "ingredient_id" : ingredient_id}
        ingredients_remove_recipe = connection.execute(query, binds)
    return "OK"

@router.post("/get_recipe_content")
def check_recipe_macros(recipe_id: int, recipe_request: RecipeRequest):
    with engine.begin() as connection:
        query = text(
                """
                SELECT *
                FROM recipe
                WHERE recipe_id = :recipe_id
                """)
        binds = {"recipe_id" : recipe_id}
        recipe_content = connection.execute(query, binds)
    return "OK"

@router.post("/short_time_recipe")
def short_recipe(recipe_id: int, recipe_request: RecipeRequest, time_constraint: int):
    with engine.begin() as connection:
        query = text(
                """
                SELECT *
                FROM recipe
                WHERE recipe_id = :recipe_id AND time_constraint < :time_constraint
                """)
        binds = {"recipe_id" : recipe_id,
                 "time_constraint" : time_constraint}
        recipe_content = connection.execute(query, binds)
    return "OK"

@router.post("/macro_friendly_recipe")
def suggest_recipe_macros(recipe_id: int, recipe_request: RecipeRequest, calorie_count: int, protein_min: int):
    with engine.begin() as connection:
        query = text(
                """
                SELECT *
                FROM recipe
                WHERE recipe_id = :recipe_id AND calories <= :calorie_count AND protein >= :protein_min
                """)
        binds = {"recipe_id" : recipe_id,
                 "calories" : calorie_count,
                 "protein": protein_min}
        recipe_content = connection.execute(query, binds)
    return "OK"


@router.post("/available_recipe")
def check_recipe_availability(fridge_id: int ):
    #checks to see the most feasible recipe based on the ingredients from the user's fridge
    with engine.begin() as connection:
        query = text(
                """
                SELECT ingredient_id
                FROM fridge
                """)
        binds = {""}
        ingredients_for_recipe = connection.execute(query, binds)
        for ingredient in ingredients_for_recipe:
            query = text(
                    """
                    UPDATE fridge
                    SET quantity = quantity - :quantity
                    WHERE ingredient_id = :ingredient and fridge_id = :fridge_id;
                    """)
            binds = { "ingredient_id" : ingredient, "fridge_id": fridge_id}
            connection.execute(query, binds)
        query = text(
                """
                SELECT :ingredient in UNNEST(recipe.ingredients) as available_ingredients
                FROM recipe
                WHERE in_id = :recipe_id
                """)
        binds = {}
        recipe_content = connection.execute(query, binds)
    return "OK"


