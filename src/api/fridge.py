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


def check_ingredients(user_id: int, recipe_id: int, servings: int):

    with db.engine.begin() as connection:
    #get recipe quant and fridge quant
        ingredients = connection.execute(sqlalchemy.text(
            """
            WITH fridgeIngred AS(
                SELECT ingredient_id, quantity AS fridge_quant
                FROM fridge
                WHERE user_id = :user_id
                )
            SELECT recipe_ingredients.ingredient_id, fridgeIngred.fridge_quant AS fridge_quant, quantity AS recipe_quant, ingredient.name, ingredient.units
            FROM recipe_ingredients
            LEFT JOIN fridgeIngred
            ON recipe_ingredients.ingredient_id = fridgeIngred.ingredient_id
            JOIN ingredient
            ON ingredient.ingredient_id = recipe_ingredients.ingredient_id
            WHERE recipe_id = :recipe
            """
            ), [{"recipe": recipe_id, "user_id": user_id}]).all()

        num_ingredients = connection.execute(sqlalchemy.text(
                """
                SELECT COUNT(ingredient_id) AS num_ingredients
                FROM recipe_ingredients
                WHERE recipe_id = :recipe_id
                """
            ), [{"recipe_id": recipe_id}]).scalar_one()
        
        serving_size = connection.execute(sqlalchemy.text(
            """
            SELECT servings
            FROM recipe
            WHERE recipe_id = :recipe"""
        ), [{"recipe": recipe_id}]).scalar_one()

        good_ingredients = 0
        serving_ratio = servings/serving_size

        for ingredient in ingredients:
            fridge_amount = ingredient.fridge_quant
            if fridge_amount is None:
                fridge_amount = 0
            if fridge_amount >= ingredient.recipe_quant*serving_ratio:
                good_ingredients += 1
                

        if good_ingredients == num_ingredients:
            return True
        else: 
            return False



# complex endpoint 
@router.post("/add_ingredients")
def add_to_fridge(user_id: int, fridge_request: FridgeRequest):
    if user_id is None:
        return "No user_id"
    if fridge_request.quantity is None:
        return "No quantity"
    if fridge_request.ingredient_id is None:
        return "No ingredient ID"
    if fridge_request.quantity < 0:
        return "invalid ingredient quantity"
    

    with db.engine.begin() as connection:
        check = connection.execute(sqlalchemy.text(
            """
            SELECT user_id 
            FROM users
            WHERE user_id = :user_id 
            """
        ), [{"user_id" : user_id}]).scalar()

        if check is None:
            return "no user_id found"


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
def remove_recipe_ingredients_from_fridge(recipe_id: int, user_id: int, servings: int):
    if recipe_id is None:
        return "No recipe ID"
    if user_id is None:
        return "No user ID"
    if servings <= 0:
        return "invalid serving size"

    with db.engine.begin() as connection:

        check = connection.execute(sqlalchemy.text(
                """
                SELECT user_id 
                FROM users
                WHERE user_id = :user_id 
                """
            ), [{"user_id" : user_id}]).scalar()

        if check is None:
            return "no user_id found"
        
        check2 = connection.execute(sqlalchemy.text(
            """
            SELECT recipe_id 
            FROM recipe
            WHERE recipe_id = :recipe_id 
            """
        ), [{"user_id" : recipe_id}]).scalar()

        if check2 is None:
            return "no recipe_id found"

        ingredients = connection.execute(sqlalchemy.text(
            """
            SELECT quantity, ingredient_id
            FROM recipe_ingredients
            WHERE recipe_id = :recipe_id
            """
        ), [{"recipe_id" : recipe_id}]).all()

        
        if ingredients == []:
            return "No ingredients found"

        serving_size = connection.execute(sqlalchemy.text(
            """
            SELECT servings
            FROM recipe
            WHERE recipe_id = :recipe"""
        ), [{"recipe": recipe_id}]).scalar_one()

        serving_ratio = servings/serving_size

        test = check_ingredients(user_id, recipe_id, servings)
        if test == False:
            return "not all ingredients in fridge"

        for ingredient in ingredients:
            remove_ingredients_from_fridge(ingredient.ingredient_id, user_id, ingredient.quantity*serving_ratio)
    return "OK"

@router.delete("/remove_ingredient")
def remove_ingredients_from_fridge(ingredient_id: int, user_id: int, quantity: int):
    if quantity < 0:
        return "input valid quantity"

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
        check = connection.execute(sqlalchemy.text(
            """
            SELECT user_id 
            FROM users
            WHERE user_id = :user_id 
            """
        ), [{"user_id" : user_id}]).scalar()

        if check is None:
            return "no user_id found"

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




