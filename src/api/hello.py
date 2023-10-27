from fastapi import APIRouter

router = APIRouter()


@router.get("/hello/", tags=["hello"])
def say_hello():
    return "hello, world!"
