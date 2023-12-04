from fastapi import APIRouter
from pydantic import BaseModel
from src.database import engine
import sqlalchemy 
from src import database as db

router = APIRouter(
    prefix="/fridge",
    tags=["fridge"]
)

class FridgeRequest(BaseModel):
    user_id : int
    quantity : int

# complex endpoint 
@router.post("/add_ingredients")
def add_to_fridge(ingredient_id: int, fridge_request: FridgeRequest):
    if fridge_request.user_id is None:
        return "No user_id"
    if fridge_request.quantity is None:
        return "No quantity"
    if ingredient_id is None:
        return "No ingredient ID"
    

    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text(
            """
            SELECT quantity 
            FROM fridge
            WHERE user_id = :user_id AND ingredient_id = :ingredient_id; 
            """
        ), [{"user_id" : fridge_request.user_id, "ingredient_id" : ingredient_id}]).first()
        
        # Add to fridge
        if result is None:
            connection.execute(sqlalchemy.text(
                """
                INSERT INTO fridge (user_id, ingredient_id, quantity)
                VALUES (:user_id, :ingredient_id, :quantity);
                """
            ), [{"user_id" : fridge_request.user_id, "ingredient_id" : ingredient_id, "quantity" : fridge_request.quantity}])
            return "Added ingredient"
        # Update quantity
        else: 
            connection.execute(sqlalchemy.text(
                """
                UPDATE fridge
                SET quantity = quantity + :quantity
                WHERE user_id = :user_id AND ingredient_id = :ingredient_id; 
                """
            ), [{"user_id" : fridge_request.user_id, "ingredient_id" : ingredient_id, "quantity" : fridge_request.quantity}])
            return "Updated ingredient"

# Secound Complex Endpoint
@router.put("/remove_recipe_ingredients")
def remove_recipe_ingredients(recipe_id: int, user_id: int):
    if recipe_id is None:
        return "No recipe ID"
    if user_id is None:
        return "No user ID"

    with db.engine.begin() as connection:
        ingredients = connection.execute(sqlalchemy.text(
            """
            SELECT quantity, ingredient_id
            FROM recipe_ingredients
            WHERE recipe_id = :recipe_id
            """
        ), [{"recipe_id" : recipe_id}]).all()
        
        if ingredients == []:
            return "No ingredients found"

        print(ingredients)
        for ingredient in ingredients:
            connection.execute(sqlalchemy.text(
                """
                UPDATE fridge
                SET quantity = quantity - :quantity
                WHERE ingredient_id = :ingredient_id AND user_id = :user_id;
                """
            ), [{"quantity" : ingredient.quantity, "ingredient_id" : ingredient.ingredient_id, "user_id": user_id}])
    return "OK"

@router.delete("/remove_ingredient")
def remove_fridge_ingredients(ingredient_id: int, quantity: int, user_id: int):
    with db.engine.begin() as connection:
        connection.execute(sqlalchemy.text(
            """
                DELETE FROM fridge
                WHERE ingredient_id = :ingredient_id AND user_id = :user_id;
            """
            ), [{"ingredient_id" : ingredient_id, "user_id": user_id}])
        
    return "OK"

@router.get("/get_fridge_ingredients")
def get_fridge_ingredients(user_id: int):
    with db.engine.begin() as connection:
        ingredients = connection.execute(sqlalchemy.text(
            """
                SELECT ingredient.name AS name, fridge.quantity AS quant, ingredient.units AS units
                FROM fridge
                JOIN ingredient
                ON ingredient.ingredient_id = fridge.ingredient_id
                WHERE user_id = :user_id
            """
            ), [{"user_id": user_id}]).all()
    
    ingredients_list = []
    if ingredients == None:
        return "No ingredients in fridge"
    
    for ingredient in ingredients:
        ingredients_list.append(
            {
                "ingredient": ingredient.name,
                "quantity": ingredient.quant,
                "units": ingredient.units
            }
        )

        
    return ingredients_list