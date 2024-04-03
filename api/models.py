from django.db import models

# Create your models here.


class User(models.Model):
    name = models.CharField(max_length=100, null=True, default=None)
    phone = models.CharField(max_length=50, null=True, default=None)
    password = models.CharField(max_length=20, null=True, default=None)
    email = models.EmailField(max_length=254, null=True, default=None)

    def __str__(self):
        return f"{self.name}"


class Movie(models.Model):
    name = models.CharField(max_length=100, null=True, default=None)
    genre = models.CharField(max_length=20, null=True, default=None)
    rating = models.CharField(max_length=10, null=True, default=None)
    release_date = models.DateField(null=True, default=None)

    def __str__(self):
        return f"{self.name}"


class Rating(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    movie_id = models.ForeignKey(
        Movie, on_delete=models.CASCADE, related_name="movie_ratings"
    )
    rating = models.FloatField(null=True, default=None)

    def __str__(self):
        return f"{self.user_id}|{self.movie_id}"
