from django.db.models import Avg, Count
from django.shortcuts import get_object_or_404, render

from .models import Genre, Movie


def recommendations(request):
    """Public view: top-rated movies, optionally filtered by genre."""
    genre_id = request.GET.get('genre')
    selected = get_object_or_404(Genre, pk=genre_id) if genre_id else None

    movies = (
        Movie.objects.annotate(avg_score=Avg('ratings__score'), ratings_count=Count('ratings'))
        .filter(ratings_count__gt=0)
        .select_related('director')
        .prefetch_related('genres')
    )
    if selected:
        movies = movies.filter(genres=selected)
    movies = movies.order_by('-avg_score', '-release_year', 'title')

    genres = Genre.objects.annotate(movie_count=Count('movies'))
    return render(request, 'movies/recommendations.html',
                  {'movies': movies, 'genres': genres, 'selected': selected})


def movie_detail(request, pk):
    movie = get_object_or_404(
        Movie.objects.select_related('director').prefetch_related('genres', 'ratings'), pk=pk)
    return render(request, 'movies/movie_detail.html', {'movie': movie})
