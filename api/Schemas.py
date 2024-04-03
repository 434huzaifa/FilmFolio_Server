from ninja import ModelSchema, Schema
from .models import *


class UserSchema(ModelSchema):
    class Meta:
        model = User
        fields = ("id", "name", "phone", "email")


class MovieSchema(ModelSchema):
    class Meta:
        model = Movie
        fields = ("id", "name", "genre", "rating", "release_date")


class RatingSchema(ModelSchema):
    user_id: UserSchema
    movie_id: ModelSchema

    class Meta:
        model = Rating
        fields = ("id", "user_id", "movie_id", "rating")


class RatingSchemaBody(Schema):
    user_id: int
    movie_id: int
    rating: float


class MovieSchemaBody(Schema):
    name: str
    genre: str | None
    rating: str | None
    release_date: str | None


class MessageSchema(Schema):
    msg: str
