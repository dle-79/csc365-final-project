import sqlalchemy
from src import database as db
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.api import auth
from fridge import add_to_fridge

router = APIRouter(
    prefix="/shoppingList",
    tags=["shoppingList"],
    dependencies=[Depends(auth.get_api_key)],
)

class Ingredient(BaseModel):
    ingredient_id: int
    quantity: float

@router.post("/add_ingredients")
#input: a list of the ingredients needed and the quantity needed to make the recipe
def add_to_shopList(ingredient_id: int, user_id: int, quantity: int):
    if user_id is None:
        return "No user_id"
    if quantity is None:
        return "No quantity"
    if ingredient_id is None:
        return "No ingredient ID"
    if ingredient_id < 1 or ingredient_id > 1662:
        return "invalid ingredient id"
    if quantity < 0:
        return "invalid ingredient quantity"
    

    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text(
            """
            SELECT quantity 
            FROM shopping_list
            WHERE user_id = :user_id AND ingredient_id = :ingredient_id; 
            """
        ), [{"user_id" : user_id, "ingredient_id" : ingredient_id}]).scalar()
        
        # Add to fridge
        if result is None:
            connection.execute(sqlalchemy.text(
                """
                INSERT INTO shopping_list (user_id, ingredient_id, quantity)
                VALUES (:user_id, :ingredient_id, :quantity);
                """
            ), [{"user_id" : user_id, "ingredient_id" : ingredient_id, "quantity" : quantity}])
            return "Added ingredient"
        # Update quantity
        else: 
            connection.execute(sqlalchemy.text(
                """
                UPDATE shopping_list
                SET quantity = quantity + :quantity
                WHERE user_id = :user_id AND ingredient_id = :ingredient_id; 
                """
            ), [{"user_id" :  user_id, "ingredient_id" : ingredient_id, "quantity" : quantity}])
            return "Updated ingredient"

@router.delete("/remove_ingredients")
def remove_shopList(ingredients_needed: Ingredient, user_id: int):
    with db.engine.begin() as connection:
        current_quantity = connection.execute(sqlalchemy.text(
            """
            SELECT quantity
            FROM shopping_list
            WHERE ingredient_id = :ingredient_id AND user_id = :user_id;
            """
            ), [{"ingredient_id" : ingredients_needed.ingredient_id, "user_id": user_id}]).scalar()
    

        if current_quantity is None:
            return "No ingredient to delete"

        if current_quantity - ingredients_needed.quantity <= 0:
            connection.execute(sqlalchemy.text(
                """
                DELETE FROM shopping_list
                WHERE ingredient_id = :ingredient_id AND user_id = :user_id;
                """
                ), [{"ingredient_id" : ingredients_needed.ingredient_id, "user_id": user_id}])
            return "Ingredient removed"
        else:
            connection.execute(sqlalchemy.text(
                """
                UPDATE shopping_list
                SET quantity = quantity - :quantity
                WHERE ingredient_id = :ingredient_id AND user_id = :user_id;
                """),
                [{"ingredient_id" : ingredients_needed.ingredient_id, "user_id": user_id, "quantity": ingredients_needed.quantity}])
            return "Ingredient updated"
        


@router.get("/sort_ingredients")
def sort_shopList(user_id: int, parameter: str):
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

@router.put("/add_recipe_ingredients")
def add_recipe_ingredients_to_shop_list(recipe_id: int, user_id: int):
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
            add_to_shopList(ingredient.ingredient_id, user_id, ingredient.quantity)
    return "OK"




