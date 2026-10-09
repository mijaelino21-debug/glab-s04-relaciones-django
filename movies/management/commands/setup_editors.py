from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from movies.models import Movie, Genre, Person, Rating

class Command(BaseCommand):
    help = 'Sets up the editors group and user'

    def handle(self, *args, **options):
        # 1. Create group
        group, created = Group.objects.get_or_create(name='editores')
        
        # 2. Permissions
        permissions_codes = [
            'add_movie', 'change_movie', 'view_movie',
            'view_genre', 'view_person',
            'view_rating', 'add_rating', 'change_rating'
        ]
        
        # Get content types
        content_types = {
            'movie': ContentType.objects.get_for_model(Movie),
            'genre': ContentType.objects.get_for_model(Genre),
            'person': ContentType.objects.get_for_model(Person),
            'rating': ContentType.objects.get_for_model(Rating),
        }
        
        for code in permissions_codes:
            model_name = code.split('_')[1]
            content_type = content_types[model_name]
            permission = Permission.objects.get(codename=code, content_type=content_type)
            group.permissions.add(permission)
            
        # 3. Create user
        User = get_user_model()
        user, created = User.objects.get_or_create(username='editor_test')
        if created:
            user.set_password('editor12345')
            user.is_staff = True
            user.save()
            
        user.groups.add(group)
        self.stdout.write(self.style.SUCCESS('Successfully set up editors group and user'))
