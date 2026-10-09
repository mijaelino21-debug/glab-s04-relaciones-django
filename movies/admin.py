from django.contrib import admin
from .models import Genre, Person, Movie, Rating

admin.site.register(Genre)
admin.site.register(Person)
admin.site.register(Movie)
admin.site.register(Rating)
