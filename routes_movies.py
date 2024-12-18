from fastapi import APIRouter, Request, HTTPException, Body
from bson import ObjectId

from models import UpdateMovieModel

router = APIRouter()

def convert_object_id(doc):
    if "_id" in doc:
        doc["_id"] = str(doc["_id"])
    return doc

@router.get("/", response_description="List first 4 movies")
def list_movies(request: Request):
    movies = list(request.app.database["movies"].find().limit(10))
    movies = [convert_object_id(movie) for movie in movies]
    return movies

@router.get("/search", response_description="Search for a movie by name or actor")
def search_movie(request: Request, movie_name: str = None, actor_name: str = None):
    query = {}
    if movie_name:
        query["title"] = movie_name
    if actor_name:
        query["cast"] = actor_name

    if not query:
        raise HTTPException(status_code=400, detail="At least one query parameter (movie_name or actor_name) must be provided")

    movies = list(request.app.database["movies"].find(query))
    movies = [convert_object_id(movie) for movie in movies]
    return movies

@router.put("/update/{movie_name}", response_description="Update a movie by name")
def update_movie(request: Request, movie_name: str, movie: UpdateMovieModel = Body(...)):
    update_data = {k: v for k, v in movie.dict().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No update data provided")

    result = request.app.database["movies"].update_one({"title": movie_name}, {"$set": update_data})

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail=f"Movie with name {movie_name} not found")

    updated_movie = request.app.database["movies"].find_one({"title": movie_name})
    return convert_object_id(updated_movie)

