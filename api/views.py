from ninja import NinjaAPI
from .models import *
from .Schemas import *
from datetime import datetime
from typing import List
from ninja.responses import codes_4xx, codes_5xx

app = NinjaAPI()


@app.post(
    "movie/",
    response={201: MovieSchema, codes_4xx: MessageSchema, codes_5xx: MessageSchema},
)
def create_movie(request, movie: MovieSchemaBody):
    try:
        movie_data = movie.model_dump()
        if movie_data["release_date"]:
            movie_data["release_date"] = datetime.strptime(
                movie_data["release_date"], "%d-%m-%Y"
            ).date()
        movie_model = Movie.objects.create(**movie_data)
        return 201, movie_model
    except Exception as e:
        return 500, e.message


@app.get("movie/", response=List[MovieSchema])
def get_movies(request):
    movies = Movie.objects.all()
    return movies


@app.get("movie/{movie_id}/", response=MovieSchema)
def get_movie(request, movie_id: int):
    movie = Movie.objects.get(id=movie_id)
    return movie


@app.post(
    "rating/",
    response={201: RatingSchema, codes_4xx: MessageSchema, codes_5xx: MessageSchema},
)
def create_rating(request, rating: RatingSchemaBody):
    try:
        rating_data = rating.model_dump()
        if rating_data["user_id"]:
            rating_data["user_id"] = User.objects.filter(
                id=rating_data["user_id"]
            ).first()
        if rating_data["movie_id"]:
            rating_data["movie_id"] = Movie.objects.filter(
                id=rating_data["movie_id"]
            ).first()
        rating_model = Rating.objects.create(**rating_data)
        return 201, rating_model
    except Exception as e:
        return 500, e.message


@app.get("rating/", response=List[RatingSchema])
def get_movies(request):
    movies = Rating.objects.all()
    return movies


@app.get("rating/{rating_id}/", response=RatingSchema)
def get_movie(request, rating_id: int):
    movie = Rating.objects.get(id=rating_id)
    return movie
