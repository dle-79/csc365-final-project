import random
import sqlalchemy
import string
from src import database as db
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.api import auth

router = APIRouter(
    prefix="/user",
    tags=["user"],
    dependencies=[Depends(auth.get_api_key)],
)

class NewUser(BaseModel):
    name: str

@router.post("/create_user")
def create_user(new_user : NewUser):
    with db.engine.begin() as connection:
        user_id = connection.execute(sqlalchemy.text(
            """
            INSERT INTO users (name)
            VALUES (:name)
            RETURNING user_id
            """),
            [{"name" : new_user.name}]).scalar()
    return {"user_id": user_id}


@router.get("/get_user/{userid}")
def get_user_id(user_id: int):
    with db.engine.begin() as connection:
        name = connection.execute(sqlalchemy.text(
        """
        SELECT name
        FROM users
        WHERE user_id = :user_id;
        """
        ),
        [{"user_id" : user_id}]).scalar()

    if name is None:
        return "No user with that id"
    
    return [{"user_id" : user_id, "name" : name}]