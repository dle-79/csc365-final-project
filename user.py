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
    email: str

@router.post("/")
def create_user(new_user : NewUser):

    with db.engine.begin() as connection:
        user_id = connection.execute(sqlalchemy.text(
            """
            INSERT INTO user (name, email)
            VALUES (:name, :email)
            RETURNING user_id
            """),
            [{"name" : new_user.name, "email" : new_user.email}]).first().user_id
    return {"user_id": user_id}

