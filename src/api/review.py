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
    if review.rating != 1 and review.rating != 2 and review.rating != 3 and review.rating != 4 and review.rating != 5:
        return "insert valid rating, int from 1-5"
    with db.engine.begin() as connection:

        check = connection.execute(sqlalchemy.text(
            """
            SELECT user_id 
            FROM users
            WHERE user_id = :user_id 
            """
        ), [{"user_id" : review.user_id}]).scalar()

        if check is None:
            return "no user_id found"
        
        check2 = connection.execute(sqlalchemy.text(
            """
            SELECT recipe_id 
            FROM recipe
            WHERE recipe_id = :recipe_id 
            """
        ), [{"recipe_id" : review.recipe_id}]).scalar()

        if check2 is None:
            return "no recipe_id found"

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
        check2 = connection.execute(sqlalchemy.text(
            """
            SELECT recipe_id 
            FROM recipe
            WHERE recipe_id = :recipe_id 
            """
        ), [{"recipe_id" : recipe_id}]).scalar()

        if check2 is None:
            return "no recipe_id found"

        avg_rating = connection.execute(sqlalchemy.text(
            """SELECT ROUND(AVG(rating), 2)
            FROM review
            WHERE recipe_id = :recipe_id
            """
        ), [{"recipe_id" : recipe_id}]).scalar()

        num_reviews = connection.execute(sqlalchemy.text(
            """SELECT ROUND(COUNT(rating), 2)
            FROM review
            WHERE recipe_id = :recipe_id
            """
        ), [{"recipe_id" : recipe_id}]).scalar()
    
    if avg_rating == None or num_reviews == None:
        return("There are no reviews for recipe " + str(recipe_id))

    return("This recipe has an average rating of " + str(avg_rating) + " stars from " + str(num_reviews) + " reviews.")



@router.get("/get_review_by_recipe")
def get_review_by_recipe(recipe_id: int):
    with db.engine.begin() as connection:
        check2 = connection.execute(sqlalchemy.text(
            """
            SELECT recipe_id 
            FROM recipe
            WHERE recipe_id = :recipe_id 
            """
        ), [{"recipe_id" : recipe_id}]).scalar()

        if check2 is None:
            return "no recipe_id found"

        reviews = connection.execute(sqlalchemy.text(
            """SELECT *
            FROM review
            WHERE recipe_id = :recipe_id
            """
        ), [{"recipe_id" : recipe_id}]).all()

    review_list = []

    for review in reviews:
        review_list.append({
            "user_id": review.user_id,
            "rating": review.rating,
            "review": review.review_description,
            "review_created": review.review_date})
    
    if review_list == []:
        return("Recipe " + str(recipe_id) + " does not have any reviews")
    return review_list

@router.get("/get_review_by_user")
def get_review_by_user(user_id: int):
    with db.engine.begin() as connection:
        check = connection.execute(sqlalchemy.text(
            """
            SELECT user_id 
            FROM users
            WHERE user_id = :user_id 
            """
        ), [{"user_id" : user_id}]).scalar()

        if check is None:
            return "user_id does not exist"

        reviews = connection.execute(sqlalchemy.text(
            """SELECT review.recipe_id, rating, review_description, review_date, recipe.name AS name
            FROM review
            JOIN recipe
            ON recipe.recipe_id = review.recipe_id
            WHERE user_id = :user_id
            """
        ), [{"user_id" : user_id}]).all()
    
    
    review_list = []
    for review in reviews:
        review_list.append({
            "recipe": review.name,
            "recipe_id": review.recipe_id,
            "rating": review.rating,
            "review": review.review_description,
            "review_created": review.review_date
        })

    if review_list == []:
        return("User " + str(user_id) + " did not review any recipes")
    return(review_list)

@router.get("/get_rating_by_user_and_recipe")
def get_review_by_user(user_id: int, recipe_id: int):
    with db.engine.begin() as connection:
        check = connection.execute(sqlalchemy.text(
            """
            SELECT user_id 
            FROM users
            WHERE user_id = :user_id 
            """
        ), [{"user_id" : user_id}]).scalar()

        if check is None:
            return "user_id does not exist"
        
        check2 = connection.execute(sqlalchemy.text(
            """
            SELECT recipe_id 
            FROM recipe
            WHERE recipe_id = :recipe_id 
            """
        ), [{"recipe_id" : recipe_id}]).scalar()

        if check2 is None:
            return "no recipe_id found"

        reviews = connection.execute(sqlalchemy.text(
            """SELECT rating, review_description, review_date, recipe.name AS name
            FROM review
            JOIN recipe
            ON review.recipe_id = recipe.recipe_id
            WHERE user_id = :user_id AND review.recipe_id = :recipe_id
            """
        ), [{"user_id" : user_id,
        "recipe_id": recipe_id}]).all()
    
    if reviews == None:
        return("No reviews made")
    
    review_list = []
    for review in reviews:
        review_list.append({
            "recipe": review.name, 
            "rating": review.rating,
            "review": review.review_description,
            "review_date": review.review_date
        })
    
    if review_list == []:
        return("User " + str(user_id) + " did not review recipe " + str(recipe_id))
    return(review_list)


    