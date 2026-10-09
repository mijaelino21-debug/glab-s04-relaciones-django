import json
import urllib.request
import io
from PIL import Image, ImageDraw, ImageFont
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from movies.models import Movie, Person, Genre, Rating

class Command(BaseCommand):
    help = 'Seeds the database with movies'

    def handle(self, *args, **options):
        # 1. Create genres
        genre_names = ['Action', 'Comedy', 'Drama', 'Science Fiction']
        genres = {name: Genre.objects.get_or_create(name=name)[0] for name in genre_names}

        # 2. Define data
        movie_data = [
            ("The Dark Knight", 2008, "Christopher Nolan", ["Action", "Drama"], [(9, "Amazing"), (10, "Masterpiece")], "The_Dark_Knight_(film)"),
            ("Inception", 2010, "Christopher Nolan", ["Action", "Science Fiction"], [(8, "Great"), (9, "Mind-bending")], "Inception"),
            ("Interstellar", 2014, "Christopher Nolan", ["Drama", "Science Fiction"], [(8, "Emotional")], "Interstellar_(film)"),
            ("The Grand Budapest Hotel", 2014, "Wes Anderson", ["Comedy", "Drama"], [(9, "Delightful")], "The_Grand_Budapest_Hotel"),
            ("Mad Max: Fury Road", 2015, "George Miller", ["Action", "Science Fiction"], [(9, "Intense"), (10, "Unbelievable")], "Mad_Max:_Fury_Road"),
            ("The Martian", 2015, "Ridley Scott", ["Comedy", "Science Fiction"], [(7, "Good"), (8, "Very good")], "The_Martian_(film)"),
            ("Arrival", 2016, "Denis Villeneuve", ["Drama", "Science Fiction"], [(9, "Thought-provoking")], "Arrival_(film)"),
            ("Parasite", 2019, "Bong Joon-ho", ["Comedy", "Drama"], [(9, "Stunning"), (10, "Best movie ever")], "Parasite_(2019_film)"),
            ("Knives Out", 2019, "Rian Johnson", ["Comedy", "Drama"], [(9, "Fun")], "Knives_Out"),
            ("Dune", 2021, "Denis Villeneuve", ["Drama", "Science Fiction"], [], "Dune_(2021_film)"),
        ]

        for title, year, director_name, genre_names_list, ratings_list, wiki_title in movie_data:
            director, _ = Person.objects.get_or_create(name=director_name)
            movie, created = Movie.objects.get_or_create(
                title=title,
                release_year=year,
                defaults={'director': director, 'synopsis': f"A great movie: {title}"}
            )

            # Assign genres
            for g_name in genre_names_list:
                movie.genres.add(genres[g_name])

            # Assign ratings if not exists
            if not movie.ratings.exists():
                for score, comment in ratings_list:
                    Rating.objects.create(movie=movie, score=score, comment=comment)

            # Assign poster
            if not movie.poster:
                self.download_or_create_poster(movie, wiki_title)
                movie.save()
            
            self.stdout.write(self.style.SUCCESS(f'Processed {title}'))

    def download_or_create_poster(self, movie, wiki_title):
        url = f"https://en.wikipedia.org/w/api.php?action=query&titles={wiki_title}&prop=pageimages&format=json&pithumbsize=500"
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode('utf-8'))
                pages = data.get('query', {}).get('pages', {})
                for page_id in pages:
                    thumbnail = pages[page_id].get('thumbnail', {})
                    img_url = thumbnail.get('source')
                    if img_url:
                        with urllib.request.urlopen(img_url) as img_resp:
                            movie.poster.save(f"{movie.title.replace(' ', '_')}.jpg", ContentFile(img_resp.read()), save=False)
                            return
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'Could not download poster for {movie.title}: {e}'))
        
        # Fallback to placeholder
        self.create_placeholder_poster(movie)

    def create_placeholder_poster(self, movie):
        img = Image.new('RGB', (500, 750), color=(30, 30, 30))
        d = ImageDraw.Draw(img)
        # Using default font, might need adjustment
        d.text((50, 375), movie.title, fill=(255, 255, 255))
        
        buf = io.BytesIO()
        img.save(buf, format='JPEG')
        movie.poster.save(f"{movie.title.replace(' ', '_')}_placeholder.jpg", ContentFile(buf.getvalue()), save=False)
