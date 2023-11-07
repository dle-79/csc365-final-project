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

@router.post("/add_ingredients")
def add_to_fridge(ingredient_id: int, fridge_request: FridgeRequest):
    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text(
            """
            SELECT quantity 
            FROM fridge
            WHERE user_id = :user_id AND ingredient_id = :ingredient_id; 
            """
        ), [{"user_id" : fridge_request.user_id, "ingredient_id" : ingredient_id}]).first()
        if result is None:
            connection.execute(sqlalchemy.text(
                """
                INSERT INTO fridge (user_id, ingredient_id, quantity)
                VALUES (:user_id, :ingredient_id, :quantity);
                """
            ), [{"user_id" : fridge_request.user_id, "ingredient_id" : ingredient_id, "quantity" : fridge_request.quantity}])
            return "Added ingredient"
        else: 
            connection.execute(sqlalchemy.text(
                """
                UPDATE fridge
                SET quantity = quantity + :quantity
                WHERE user_id = :user_id AND ingredient_id = :ingredient_id; 
                """
            ), [{"user_id" : fridge_request.user_id, "ingredient_id" : ingredient_id, "quantity" : fridge_request.quantity}])
            return "Updated ingredient"

@router.post("/remove_repice_ingredients")
def remove_fridge_ingredients(recipe_id: int, user_id: int):
    with db.engine.begin() as connection:
        ingredients = connection.execute(sqlalchemy.text(
            """
            SELECT quantity, ingredient_id
            FROM recipe_ingredients
            WHERE recipe_id = :recipe_id
            """
        ), [{"recipe_id" : recipe_id}]).all()
        print(ingredients)
        for ingredient in ingredients:
            connection.execute(sqlalchemy.text(
                """
                UPDATE fridge
                SET quantity = quantity - :quantity
                WHERE ingredient_id = :ingredient_id AND user_id = :user_id;
                """
            ), [{"quantity" : ingredient.quantity, "ingredient_id" : ingredient.ingredient_id, "user_id": user_id}])
        
    # with engine.begin() as connection:
    #     query = text(
    #             """
    #             SELECT *
    #             FROM recipe_ingredients
    #             WHERE recipe_id = :recipe_id
    #             """)
    #     binds = {"recipe_id" : recipe_id}
    #     ingredients_for_recipe = connection.execute(query, binds)
    #     for ingrendient in ingredients_for_recipe:
    #         user_id = get_user_id(fridge_request.user_id, connection)
    #         query = text(
    #                 """
    #                 UPDATE fridge
    #                 SET quantity = quantity - :quantity
    #                 WHERE ingredient_id = :ingredient_id and user_id = :user_id;
    #                 """)
    #         binds = {"quantity" : ingrendient.quantity, "ingredient_id" : ingrendient.ingredient_id, "user_id": user_id}
    #         connection.execute(query, binds)
    return "OK"