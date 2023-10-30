from fastapi import APIRouter
from pydantic import BaseModel
from src.api.database import engine
from sqlalchemy import text

router = APIRouter()


class FridgeRequest(BaseModel):
    user_id: int
    quantity: float


def get_fridge_id(user_id: int, connection):
    query = text("SELECT fridge_id from user WHERE user_id = :user_id")
    binds = {"user_id": user_id}
    result = connection.execute(query, binds).scalar_one()
    return result


@router.post("/ingredients/{ingredient_id}", tags=["ingredients"])
def add_to_fridge(ingredient_id: int, fridge_request: FridgeRequest):
    # checking if there's already ingredients in fridge
    with engine.begin() as connection:
        fridge_id = get_fridge_id(FridgeRequest.user_id, connection)
        query = text(
            "SELECT quantity from fridge WHERE ingredient_id = :ingredient_id AND fridge_id = :fridge_id"
        )
        binds = {"ingredient_id": ingredient_id, "fridge_id": fridge_id}
        result = connection.execute(query, binds)
        # updating amount if there is
        if result:
            query = text(
                "UPDATE fridge SET quantity = quantity + :gained WHERE ingredient_id = :ingredient_id AND fridge_id = :fridge_id"
            )
            binds = {
                "gained": fridge_request.quantity,
                "ingredient_id": ingredient_id,
                "fridge_id": fridge_id,
            }
            connection.execute(query, binds)
        # and inserting if there isn't
        else:
            query = text("INSERT INTO fridge (:ingredient_id, :quantity, :fridge_id)")
            binds = {
                "ingredient_id": ingredient_id,
                "quantity": fridge_request.quantity,
                "fridge_id": fridge_id,
            }
            connection.execute(query, binds)
