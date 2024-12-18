from fastapi import APIRouter, Request, HTTPException

router = APIRouter()

@router.get("/common_movies", response_description="Get the number of common movies between MongoDB and Neo4j")
def get_common_movies(request: Request):
    # Query MongoDB to get the list of movie titles
    mongo_movies = request.app.database["movies"].find({}, {"title": 1, "_id": 0})
    mongo_movie_titles = {movie["title"] for movie in mongo_movies}

    # Query Neo4j to get the list of movie titles
    session = request.app.neo4j_driver.session()
    try:
        query = """
        MATCH (m:Movie)
        RETURN m.title AS title
        """
        result = session.run(query)
        neo4j_movie_titles = {record["title"] for record in result}
    finally:
        session.close()

    # Find the intersection of the two sets
    common_movies = mongo_movie_titles.intersection(neo4j_movie_titles)

    # Return the count of common movies
    return {"common_movie_count": len(common_movies)}