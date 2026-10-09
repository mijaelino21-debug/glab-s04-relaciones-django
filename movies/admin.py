from django.contrib import admin
from .models import Genre, Person, Movie, Rating

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class RatingInline(admin.TabularInline):
    model = Rating
    extra = 1
    fields = ('score', 'comment', 'created_at')
    readonly_fields = ('created_at',)

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'release_year', 'director', 'genre_list', 'avg_rating', 'created_at')
    list_filter = ('genres', 'release_year')
    list_select_related = ('director',)
    search_fields = ('title', 'director__name')
    filter_horizontal = ('genres',)
    readonly_fields = ('created_at', 'updated_at')
    inlines = [RatingInline]

    def genre_list(self, obj):
        return ", ".join([genre.name for genre in obj.genres.all()])
    genre_list.short_description = "Genres"

    def avg_rating(self, obj):
        rating = obj.average_rating
        return f"{rating:.1f}/10" if rating is not None else "-"
    avg_rating.short_description = "Average Rating"

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('genres', 'ratings')

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('movie', 'score', 'created_at')
    list_filter = ('score',)
    search_fields = ('movie__title', 'comment')
