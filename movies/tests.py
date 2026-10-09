from django.test import TestCase, Client
from django.urls import reverse
from django.core.management import call_command
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from .models import Movie, Genre, Rating, Person

class MoviesTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # 1. Seed data
        call_command('seed_movies')
        
        # 2. Setup Superuser
        cls.superuser = User.objects.create_superuser('admin', 'admin@test.com', 'devpass')
        
        # 3. Setup Editor
        cls.editor = User.objects.create_user('editor_test', 'editor@test.com', 'devpass')
        cls.editor.is_staff = True
        cls.editor.save()
        editor_group = Group.objects.create(name='editores')
        
        # Assign permissions (view, add, change for Movie and Rating)
        for model in [Movie, Rating]:
            ct = ContentType.objects.get_for_model(model)
            perms = Permission.objects.filter(content_type=ct, codename__in=[f'{action}_{model.__name__.lower()}' for action in ['view', 'add', 'change']])
            editor_group.permissions.add(*perms)
            
        cls.editor.groups.add(editor_group)

    def test_seed_counts(self):
        self.assertEqual(Movie.objects.count(), 10)
        self.assertEqual(Genre.objects.count(), 4)

    def test_cascade_delete_movie(self):
        movie = Movie.objects.first()
        initial_ratings_count = Rating.objects.count()
        ratings_in_movie_count = movie.ratings.count()
        
        movie.delete()
        
        self.assertEqual(Rating.objects.count(), initial_ratings_count - ratings_in_movie_count)

    def test_superuser_admin_access(self):
        self.client.login(username='admin', password='devpass')
        for model in [Movie, Genre, Rating, Person]:
            url = reverse(f'admin:{model._meta.app_label}_{model._meta.model_name}_changelist')
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)

    def test_editor_permissions(self):
        self.client.login(username='editor_test', password='devpass')
        
        # Test 403 on delete movie
        movie = Movie.objects.first()
        response = self.client.post(reverse(f'admin:movies_movie_delete', args=[movie.pk]))
        self.assertEqual(response.status_code, 403)
        
        # Test 403 on access users
        response = self.client.get(reverse('admin:auth_user_changelist'))
        self.assertEqual(response.status_code, 403)

    def test_recommendation_view(self):
        # Test order by average rating
        response = self.client.get(reverse('movies:recommendations'))
        self.assertEqual(response.status_code, 200)
        
        movies = response.context['movies']
        # Check exclusion of movies without ratings (Dune in seed_movies has empty ratings)
        for movie in movies:
            self.assertGreater(movie.ratings_count, 0)
        
        # Check ordering
        avg_scores = [m.avg_score for m in movies]
        # Sort manually because of potential tie-breaks in release_year, title
        self.assertEqual(avg_scores, sorted(avg_scores, reverse=True))
        
        # Check 404 with nonexistent genre
        response = self.client.get(reverse('movies:recommendations') + '?genre=999')
        self.assertEqual(response.status_code, 404)
