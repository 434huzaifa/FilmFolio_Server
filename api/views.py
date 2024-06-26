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
        return 500, str(e)


@app.get("movie/", response=List[MovieSchema])
def get_movies(request, user_id: int):
    movies = Movie.objects.all()
    movie_schemas = []
    for movie in movies:
        movie_schema = MovieSchema.from_orm(movie)
        movie_schema.user_rating = movie_schema.get_user_rating(user_id)
        movie_schemas.append(movie_schema)
    return movie_schemas


@app.get("movie/search/", response=List[MovieSchema])
def search_movies(request, query: str,user_id:str):
    movies = Movie.objects.filter(name__icontains=query)
    movie_schemas = []
    for movie in movies:
        movie_schema = MovieSchema.from_orm(movie)
        movie_schema.user_rating = movie_schema.get_user_rating(user_id)
        movie_schemas.append(movie_schema)
    return movie_schemas


@app.get("movie/{movie_id}/", response=MovieSchema)
def get_movie(request, movie_id: int, user_id: int):
    movie = Movie.objects.get(id=movie_id)
    movie_schema = MovieSchema.from_orm(movie)
    user_id = request.user_id
    movie_schema.user_rating = movie_schema.get_user_rating(user_id)
    return movie_schema


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
        return 500, str(e)


@app.get("rating/", response=List[RatingSchema])
def get_all_rating(request):
    movies = Rating.objects.all()
    return movies


@app.get("rating/{rating_id}/", response=RatingSchema)
def get_single_rating(request, rating_id: int):
    movie = Rating.objects.get(id=rating_id)
    return movie


@app.get("/user_rating/{user_id}/", response=List[UserRatingSchema])
def get_all_user_rating(request, user_id: int):
    user = User.objects.get(id=user_id)
    rating = Rating.objects.filter(user_id=user)
    return rating


@app.get("user/", response={200: UserSchema, codes_4xx: MessageSchema})
def confirm_user(request, email: str, password: str):
    user = User.objects.filter(email=email, password=password).first()
    if user:
        return 200, user
    else:
        return 404, {"msg": "User not found"}
