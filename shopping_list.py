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
    aisle: str

@router.post("/add_ingredients")
#input: a list of the ingredients needed and the quantity needed to make the recipe
def add_to_shopList(ingredients_needed: list[Ingredient]):
    # checking if there's already ingredients in fridge
    for ingredient in range(len(ingredients_needed)):
        with db.engine.begin() as connection:
            result = connection.execute(sqlalchemy.text("""
            SELECT quantity
            FROM fridge
            JOIN users ON users.id = fridge.user_id
            JOIN ingredient ON ingredient.id = fridge.ingredient_id
            WHERE ingredient.id = :ingredient
            AND users.id = fridge.user_id
            """),
            [{"ingredient": ingredient.id}]).first()
        
        quant = result.quantity

        if quant is None:
            quant = 0

        if quant >= ingredient.quantity:
            continue
        else:
            connection.execute(sqlalchemy.text("""
            INSERT INTO 
            """),
            [{"ingredient": ingredient.id}]).first()




