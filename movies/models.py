from django.db import models
from django.db.models import Avg


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = 'Genre'
        verbose_name_plural = 'Genres'
        ordering = ['name']

    def __str__(self):
        return self.name


class Person(models.Model):
    name = models.CharField(max_length=200)
    birth_date = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = 'Person'
        verbose_name_plural = 'People'
        ordering = ['name']

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=200)
    release_year = models.PositiveIntegerField()
    director = models.ForeignKey(Person, null=True, blank=True, on_delete=models.SET_NULL, related_name='directed_movies')
    synopsis = models.TextField(blank=True)
    poster = models.ImageField(upload_to='posters/', null=True, blank=True)
    genres = models.ManyToManyField(Genre, related_name='movies')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def average_rating(self):
        return self.ratings.aggregate(Avg('score'))['score__avg']

    class Meta:
        verbose_name = 'Movie'
        verbose_name_plural = 'Movies'
        ordering = ['-release_year', 'title']

    def __str__(self):
        return f"{self.title} ({self.release_year})"


class Rating(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='ratings')
    score = models.PositiveSmallIntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Rating'
        verbose_name_plural = 'Ratings'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.movie.title} ({self.movie.release_year}) — {self.score}/10"
