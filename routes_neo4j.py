from fastapi import APIRouter, Request, HTTPException

router = APIRouter()

@router.get("/users_rated", response_description="List users who rated a movie")
def list_users_rated_movie(request: Request, movie_name: str):
    session = request.app.neo4j_driver.session()
    try:
        query = """
        MATCH (u:User)-[r:RATED]->(m:Movie {title: $movie_name})
        RETURN u
        """
        result = session.run(query, movie_name=movie_name)
        users = [record["u"] for record in result]
        return users
    finally:
        session.close()

@router.get("/user_ratings", response_description="Get a user with the number of movies they have rated and the list of rated movies")
def get_user_ratings(request: Request, user_name: str):
    session = request.app.neo4j_driver.session()
    try:
        query = """
        MATCH (u:User {name: $user_name})-[r:RATED]->(m:Movie)
        RETURN u.name AS user_name, count(m) AS movie_count, collect(m.title) AS rated_movies
        """
        result = session.run(query, user_name=user_name)
        user_data = result.single()
        if not user_data:
            raise HTTPException(status_code=404, detail=f"User with name {user_name} not found")
        return {
            "user_name": user_data["user_name"],
            "movie_count": user_data["movie_count"],
            "rated_movies": user_data["rated_movies"]
        }
    finally:
        session.close()