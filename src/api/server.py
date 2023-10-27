from fastapi import FastAPI, exceptions
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from src.api import catalog, hello
import json
import logging
import sys

description = """
Find the recipe of your dreams
"""

app = FastAPI(
    title="Recipe Finder",
    description=description,
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "foo fun",
        "email": "abuchko@calpoly.edu",
    },
)

app.include_router(catalog.router)
app.include_router(hello.router)


@app.exception_handler(exceptions.RequestValidationError)
@app.exception_handler(ValidationError)
async def validation_exception_handler(request, exc):
    logging.error(f"The client sent invalid data!: {exc}")
    exc_json = json.loads(exc.json())
    response = {"message": [], "data": None}
    for error in exc_json:
        response["message"].append(f"{error['loc']}: {error['msg']}")

    return JSONResponse(response, status_code=422)


@app.get("/")
async def root():
    return {"message": "Welcome to Recipe Finder"}
