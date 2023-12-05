import sqlalchemy
from src import database as db
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.api import auth

router = APIRouter(
    prefix="/shoppingList",
    tags=["shoppingList"],
    dependencies=[Depends(auth.get_api_key)],
)

class Ingredient(BaseModel):
    ingredient_id: int
    quantity: int

@router.post("/add_ingredients")
#input: a list of the ingredients needed and the quantity needed to make the recipe
def add_to_shopList(ingredients_needed: list[Ingredient], user_id: int):
    for ingredient in ingredients_needed:
        with db.engine.begin() as connection:
            connection.execute(sqlalchemy.text("""
            INSERT INTO shopping_list (user_id, ingredient_id, quantity, purchase)
            VALUES (:user_id, :ingredient, :amount_needed, False)
            """),
            [{"user_id": user_id,
            "ingredient": ingredient.ingredient_id,
            "amount_needed": ingredient.quantity}])
        # checking if there's already ingredients in fridge
        # with db.engine.begin() as connection:
        #     result = connection.execute(sqlalchemy.text("""
        #     SELECT quantity
        #     FROM fridge
        #     WHERE ingredient_id = :ingredient
        #     AND :user_id = fridge.user_id;
        #     """),
        #     [{"ingredient": ingredient.id,
        #     "user_id": user_id}]).first()
        #     quant = result.quantity

        # if quant is None:
        #     quant = 0

        # if quant >= ingredient.quantity:
        #     continue
        # else:
    return "OK"

@router.delete("/remove_ingredients")
#input: a list of the ingredients removed and the quantity needed to make the recipe
def remove_shopList(ingredients_needed: list[Ingredient], user_id: int):
    for ingredient in range(len(ingredients_needed)):
        # checking if there's isn't ingredients in fridge
        with db.engine.begin() as connection:
            result = connection.execute(sqlalchemy.text("""
            SELECT quantity
            FROM fridge
            WHERE ingredient_id = :ingredient
            AND :user_id = fridge.user_id
            """),
            [{"ingredient": ingredient.ingredient_id,
            "user_id": user_id}]).scalar_one()
            quant = result.quantity

        if quant is None:
            quant = 0

        if quant < ingredient.quantity:
            continue
        else:
            with db.engine.begin() as connection:
                connection.execute(sqlalchemy.text("""
                DELETE FROM shopping_list
                WHERE user_id = :user_id
                AND ingredient_id = :ingredient
                """),
                [{"user_id": user_id,
                "ingredient": ingredient.ingredient_id}]).scalar_one()
    return "OK"

@router.get("/sort_ingredients")
#input: a list of the ingredients needed and the quantity needed to make the recipe
def sort_shopList(user_id: int, parameter: str):
        # checking if there's already ingredients in fridge
    if parameter != "aisle" and parameter != "name" and parameter != "amount":
        return("Error: Invalid parameter type")
    
    with db.engine.begin() as connection:
        if parameter == "aisle":
            ingredients = connection.execute(sqlalchemy.text("""
                SELECT name, aisle, shopping_list.quantity AS amount, units
                FROM ingredient
                JOIN shopping_list 
                ON ingredient.ingredient_id = shopping_list.ingredient_id
                WHERE shopping_list.user_id = :user_id
                ORDER BY aisle
                """),
                [{"user_id": user_id}]).all()
        elif parameter == "name":
            ingredients = connection.execute(sqlalchemy.text("""
                SELECT name, aisle, shopping_list.quantity AS amount, units
                FROM ingredient
                JOIN shopping_list 
                ON ingredient.ingredient_id = shopping_list.ingredient_id
                WHERE shopping_list.user_id = :user_id
                ORDER BY name
                """),
                [{"user_id": user_id}]).all()
        else:
            ingredients = connection.execute(sqlalchemy.text("""
                SELECT name, aisle, shopping_list.quantity AS amount, units
                FROM ingredient
                JOIN shopping_list 
                ON ingredient.ingredient_id = shopping_list.ingredient_id
                WHERE shopping_list.user_id = :user_id
                ORDER BY amount
                """),
                [{"user_id": user_id}]).all()
 
    ingredient_list = []

    for ingredient in ingredients:
        ingredient_list.append({
            "ingredient": ingredient.name,
            "quantity": ingredient.amount,
            "units": ingredient.units,
            "aisle": ingredient.aisle
        })
    
    if len(ingredient_list) == 0:
        return("No ingredients on shop list")
    return ingredient_list







