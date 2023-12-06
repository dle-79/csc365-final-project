from fastapi import APIRouter
from pydantic import BaseModel
from src.database import engine
import sqlalchemy 
from src import database as db

router = APIRouter(
    prefix="/fridge",
    tags=["fridge"]
)

@router.get("/get_ingredient_catalog")
def get_catalog():
    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text(
            """
            SELECT ingredient.ingredient_id, ingredient.name
            FROM ingredient
            ORDER BY ingredient.ingredient_id;
            """
        )).all()
    
    return_dict = {}
    for item in result:
        return_dict[item.ingredient_id] = item.name
    return [return_dict]


class FridgeRequest(BaseModel):
    ingredient_id : int
    quantity : float


# complex endpoint 
@router.post("/add_ingredients")
def add_to_fridge(user_id: int, fridge_request: FridgeRequest):
    if user_id is None:
        return "No user_id"
    if fridge_request.quantity is None:
        return "No quantity"
    if fridge_request.ingredient_id is None:
        return "No ingredient ID"
    if fridge_request.ingredient_id < 1 or fridge_request.ingredient_id > 1662:
        return "invalid ingredient id"
    if fridge_request.quantity < 0:
        return "invalid ingredient quantity"
    

    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text(
            """
            SELECT quantity 
            FROM fridge
            WHERE user_id = :user_id AND ingredient_id = :ingredient_id; 
            """
        ), [{"user_id" : user_id, "ingredient_id" : fridge_request.ingredient_id}]).scalar()
        
        # Add to fridge
        if result is None:
            connection.execute(sqlalchemy.text(
                """
                INSERT INTO fridge (user_id, ingredient_id, quantity)
                VALUES (:user_id, :ingredient_id, :quantity);
                """
            ), [{"user_id" : user_id, "ingredient_id" : fridge_request.ingredient_id, "quantity" : fridge_request.quantity}])
            return "Added ingredient"
        # Update quantity
        else: 
            connection.execute(sqlalchemy.text(
                """
                UPDATE fridge
                SET quantity = quantity + :quantity
                WHERE user_id = :user_id AND ingredient_id = :ingredient_id; 
                """
            ), [{"user_id" :  user_id, "ingredient_id" : fridge_request.ingredient_id, "quantity" : fridge_request.quantity}])
            return "Updated ingredient"



# Secound Complex Endpoint
@router.put("/remove_recipe_ingredients")
def remove_recipe_ingredients_from_fridge(recipe_id: int, user_id: int):
    if recipe_id is None:
        return "No recipe ID"
    if user_id is None:
        return "No user ID"
    if recipe_id < 1 or recipe_id > 2031:
        return "invalid recipe_id"

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

        for ingredient in ingredients:
            remove_ingredients_from_fridge(ingredient.ingredient_id, user_id, ingredient.quantity)
    return "OK"

@router.delete("/remove_ingredient")
def remove_ingredients_from_fridge(ingredient_id: int, user_id: int, quantity: int):
    with db.engine.begin() as connection:
        current_quantity = connection.execute(sqlalchemy.text(
            """
            SELECT quantity
            FROM fridge
            WHERE ingredient_id = :ingredient_id AND user_id = :user_id;
            """
            ), [{"ingredient_id" : ingredient_id, "user_id": user_id}]).scalar()
    

        if current_quantity is None:
            return "No ingredient to delete"

        if current_quantity - quantity <= 0:
            connection.execute(sqlalchemy.text(
                """
                DELETE FROM fridge
                WHERE ingredient_id = :ingredient_id AND user_id = :user_id;
                """
                ), [{"ingredient_id" : ingredient_id, "user_id": user_id}])
            return "ingredient removed from fridge"
        else:
            connection.execute(sqlalchemy.text(
                """
                UPDATE fridge
                SET quantity = quantity - :quantity
                WHERE ingredient_id = :ingredient_id AND user_id = :user_id;
                """),
                [{"ingredient_id" : ingredient_id, "user_id": user_id, "quantity": quantity}])
            return "ingredient updated"

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