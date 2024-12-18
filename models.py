from typing import Optional, List

from pydantic import BaseModel

class Artist(BaseModel):
    _id: str
    last_name: str
    first_name: str
    birth_date: str

class UpdateMovieModel(BaseModel):
    plot: Optional[str] = None
    genres: Optional[List[str]] = None
    runtime: Optional[int] = None
    cast: Optional[List[str]] = None
    poster: Optional[str] = None
    title: Optional[str] = None
    fullplot: Optional[str] = None
    languages: Optional[List[str]] = None
    released: Optional[str] = None
    directors: Optional[List[str]] = None
    rated: Optional[str] = None
    awards: Optional[dict] = None
    lastupdated: Optional[str] = None
    year: Optional[int] = None
    imdb: Optional[dict] = None
    countries: Optional[List[str]] = None
    type: Optional[str] = None
    tomatoes: Optional[dict] = None
    num_mflix_comments: Optional[int] = None