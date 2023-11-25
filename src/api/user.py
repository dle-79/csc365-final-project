import sqlalchemy
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

@router.post("/")
def create_user(new_user : NewUser):
    with db.engine.begin() as connection:
        user_id = connection.execute(sqlalchemy.text(
            """
            INSERT INTO users (name)
            VALUES (:name)
            RETURNING user_id
            """),
            [{"name" : new_user.name}]).first().user_id
    return {"user_id": user_id}

@router.get("/{userid}")
def get_user(user_id: int):
    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text(
        """
        SELECT name
        FROM users
        WHERE user_id = :user_id;
        """
        ),
        [{"user_id" : user_id}]).first()
    return [{
        "user_id" : user_id,
        "name" : result.name
    }]