from fastapi import FastAPI
from dotenv import dotenv_values
from neo4j import GraphDatabase
from pymongo import MongoClient
from routes_movies import router as movie_router
from routes_neo4j import router as neo4j_router
from routes_common import router as common_router

config = dotenv_values(".env")

app = FastAPI()

@app.on_event("startup")
def startup_mongodb_client():
    app.mongodb_client = MongoClient(config["ATLAS_URI"])
    app.database = app.mongodb_client[config["DB_NAME"]]
    print("Connected to the MongoDB database!")

@app.on_event("startup")
def startup_neo4j_client():
    app.neo4j_driver = GraphDatabase.driver(
        config["NEO4J_URI"],
        auth=(config["NEO4J_USER"], config["NEO4J_PASSWORD"])
    )
    print("Connected to the Neo4j database!")

@app.on_event("shutdown")
def shutdown_mongodb_client():
    app.mongodb_client.close()

@app.on_event("shutdown")
def shutdown_neo4j_client():
    app.neo4j_driver.close()


app.include_router(movie_router, tags=["mongodb"], prefix="/mongodb")
app.include_router(neo4j_router, tags=["neo4j"], prefix="/neo4j")
app.include_router(common_router, tags=["common"], prefix="/common")