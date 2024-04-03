from django.db import models
from django.db.models import Avg
import math

# Create your models here.


class User(models.Model):
    name = models.CharField(max_length=100, null=True, default=None)
    phone = models.CharField(max_length=50, null=True, default=None)
    password = models.CharField(max_length=20, null=True, default=None)
    email = models.EmailField(max_length=254, null=True, default=None)

    def __str__(self):
        return f"{self.name}"


def custom_round(number, ndigits=1):
    """
    Round a number to a specified number of decimal places.
    Rounds up if the next decimal is 7 or above.
    """
    if number is None:
        return 0
    multiplier = 10**ndigits
    return math.floor(number * multiplier + 0.5) / multiplier


class Movie(models.Model):
    name = models.CharField(max_length=100, null=True, default=None)
    genre = models.CharField(max_length=20, null=True, default=None)
    rating = models.CharField(max_length=10, null=True, default=None)
    release_date = models.DateField(null=True, default=None)

    def __str__(self):
        return f"{self.name}"

    @property
    def average_rating(self):
        avg_rating = self.movie_ratings.aggregate(Avg("rating"))["rating__avg"]
        if avg_rating is None:
            return 0
        rounded_avg_rating = custom_round(avg_rating, 1)
        return rounded_avg_rating


class Rating(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    movie_id = models.ForeignKey(
        Movie, on_delete=models.CASCADE, related_name="movie_ratings"
    )
    rating = models.FloatField(null=True, default=None)
    class Meta:
        unique_together = ('user_id', 'movie_id')
    def __str__(self):
        return f"{self.user_id}|{self.movie_id}"
