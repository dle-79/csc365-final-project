import sqlalchemy
from src import database as db
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.api import auth

router = APIRouter(
    prefix="/review",
    tags=["review"]
)

class Review(BaseModel):
    user_id: int
    recipe_id: int
    #rating is an integer between 1-5, inclusive
    rating: int
    review: str

@router.post("/add_review")
def add_review(review: Review):
    with db.engine.begin() as connection:
        connection.execute(sqlalchemy.text(
                """
                INSERT INTO review (user_id, recipe_id, rating, review_description)
                VALUES (:user_id, :recipe_id, :rating, :review_description);
                """
            ), [{"user_id" : review.user_id, 
            "recipe_id": review.recipe_id, 
            "rating": review.rating,
            "review_description": review.review}])
    return("Review added!")


@router.get("/get_rating_by_recipe")
def get_avg_rating_by_recipe(recipe_id: int):
    with db.engine.begin() as connection:
        avg_rating = connection.execute(sqlalchemy.text(
            """SELECT AVG(rating)
            FROM review
            WHERE recipe_id = :recipe_id
            """
        ), [{"recipe_id" : recipe_id}]).scalar_one()

        num_reviews = connection.execute(sqlalchemy.text(
            """SELECT COUNT(rating)
            FROM review
            WHERE recipe_id = :recipe_id
            """
        ), [{"recipe_id" : recipe_id}]).scalar_one()


    return("This recipe has an average rating of " + avg_rating + " stars from " + num_reviews + " reviews.")



@router.get("/get_review_by_recipe")
def get_review_by_recipe(recipe_id: int):
    with db.engine.begin() as connection:
        reviews = connection.execute(sqlalchemy.text(
            """SELECT *
            FROM review
            WHERE recipe_id = :recipe_id
            """
        ), [{"recipe_id" : recipe_id}]).all()
    
    if reviews == None:
        return("No reviews made")

    reviews = []

    for review in reviews:
        reviews.append({
            "user_id": review.user_id,
            "rating": review.rating,
            "review": review.review_description,
            "review_created": review.review_date})
    
    return reviews

@router.get("/get_review_by_user")
def get_review_by_user(user_id: int):
    with db.engine.begin() as connection:
        reviews = connection.execute(sqlalchemy.text(
            """SELECT recipe_id, rating, review_description, review_date
            FROM review
            WHERE user_id = :user_id
            """
        ), [{"user_id" : user_id}]).all()
    
    if reviews == None:
        return("No reviews made")
    
    reviews = []
    for review in reviews:
        reviews.append({
            "recipe_id": review.recipe_id,
            "rating": review.rating,
            "review": review.review_description,
            "review_created": review.review_date
        })
    
    return(reviews)

@router.get("/get_rating_by_user_and_recipe")
def get_review_by_user(user_id: int, recipe_id: int):
    with db.engine.begin() as connection:
        reviews = connection.execute(sqlalchemy.text(
            """SELECT rating, review_description, review_date
            FROM review
            WHERE user_id = :user_id AND recipe_id = :recipe_id
            """
        ), [{"user_id" : user_id,
        "recipe_id": recipe_id}]).all()
    
    if reviews == None:
        return("No reviews made")
    
    reviews = []
    for review in reviews:
        reviews.append({
            "rating": review.rating,
            "review": review.review_description,
            "review_date": review.review_date
        })
    
    return(reviews)


    