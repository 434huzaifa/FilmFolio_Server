from ninja import ModelSchema, Schema
from .models import *
from datetime import date
from typing import Optional


class UserSchema(ModelSchema):
    class Meta:
        model = User
        fields = ("id", "name", "phone", "email")


class MovieSchema(ModelSchema):
    average_rating: float
    user_rating: Optional[float] = None

    class Meta:
        model = Movie
        fields = "__all__"
        from_attributes  = True

    def get_user_rating(self, user_id: int) -> float:
        try:
            rating = Rating.objects.get(
                movie_id__id=self.id, user_id__id=user_id
            ).rating
            return rating
        except Rating.DoesNotExist:
            return -1  # Return 0 if the user does not have a rating for the movie


class RatingSchema(ModelSchema):
    user_id: UserSchema
    movie_id: MovieSchema

    class Meta:
        model = Rating
        fields = ("id", "user_id", "movie_id", "rating")


class UserRatingSchema(ModelSchema):
    class Meta:
        model = Rating
        fields = ("movie_id", "rating")


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
