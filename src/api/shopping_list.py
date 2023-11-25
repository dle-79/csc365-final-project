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
    id: int
    name: str
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
            "ingredient": ingredient.id,
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
            [{"ingredient": ingredient.id,
            "user_id": user_id}]).first()
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
                "ingredient": ingredient.id}]).first()
    return "OK"

@router.get("/sort_ingredients")
#input: a list of the ingredients needed and the quantity needed to make the recipe
def sort_shopList(user_id: int):
        # checking if there's already ingredients in fridge
    with db.engine.begin() as connection:
        ingredients = connection.execute(sqlalchemy.text("""
            SELECT name, aisle, shopping_list.quantity AS amount, quantity AS unit
            FROM ingredient
            JOIN shopping_list 
            ON ingredient.id = shopping_list.ingredient_id
            WHERE :user_id = fridge.user_id
            ORDER BY aisle
            """),
            [{"user_id": user_id}]).all()
 
    ingredient_list = []

    for ingredient in ingredients:
        ingredient_list.append({
            "ingredient": ingredient.name,
            "quantity": ingredient.amount,
            "units": ingredient.unit
        })
    
    if len(ingredient_list) == 0:
        return []
    return ingredient_list







