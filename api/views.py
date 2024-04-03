from ninja import NinjaAPI
from .models import *
from .Schemas import *
from datetime import datetime
from typing import List
from ninja.responses import codes_4xx, codes_5xx

app = NinjaAPI(
    title="FilmFolio APIs", description="A simple movie rating site", docs_url="/"
)


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


@app.get("movie/search/", response=List[MovieSchema])
def search_movies(request, query: str):
    movies = Movie.objects.filter(name__icontains=query)
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
def get_all_rating(request):
    movies = Rating.objects.all()
    return movies


@app.get("rating/{rating_id}/", response=RatingSchema)
def get_single_rating(request, rating_id: int):
    movie = Rating.objects.get(id=rating_id)
    return movie

@app.get("user/",response={200:UserSchema,codes_4xx:MessageSchema})
def confirm_user(request,email:str,password:str):
    user=User.objects.filter(email=email,password=password).first()
    if user:
        return 200,user
    else:
        return 404,"User not found"