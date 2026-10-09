from django.core.management.base import BaseCommand
from news.models import Author, Category, Article
from django.utils import timezone
from django.utils.text import slugify
from django.core.files.base import ContentFile
from PIL import Image, ImageDraw, ImageFont
import io
import datetime

class Command(BaseCommand):
    help = 'Seeds the database'

    def handle(self, *args, **options):
        if Category.objects.exists() or Author.objects.exists() or Article.objects.exists():
            self.stdout.write("Database already seeded. Skipping.")
            return

        # Create Categories
        categories = ['Tecnología', 'Deportes', 'Cultura']
        category_objs = [Category.objects.create(name=c, slug=slugify(c)) for c in categories]

        # Create Authors
        authors = [
            Author.objects.create(name='Autor Uno', bio='Bio del autor uno'),
            Author.objects.create(name='Autor Dos', bio='Bio del autor dos')
        ]

        # Create Articles
        for i in range(6):
            title = f"Artículo {i+1}"
            category = category_objs[i % 3]
            author = authors[i % 2]
            published_at = timezone.now() - datetime.timedelta(days=i)
            
            summary = "Este es un resumen muy largo para el artículo, que debe tener más de veinticinco palabras para cumplir con el requisito solicitado en la tarea de siembra de datos."
            body = "Primer párrafo del artículo. Debe tener contenido suficiente.\n\nSegundo párrafo del artículo. También debe tener contenido suficiente para cumplir con los requerimientos."
            
            article = Article.objects.create(
                title=title,
                slug=f"articulo-{i+1}",
                summary=summary,
                body=body,
                published_at=published_at,
                author=author
            )
            article.categories.add(category)
            
            # Generate Image
            img = Image.new('RGB', (800, 450), color=(73, 109, 137))
            d = ImageDraw.Draw(img)
            try:
                font = ImageFont.truetype("arial.ttf", 36)
            except:
                font = ImageFont.load_default()
            d.text((10, 10), title, fill=(255, 255, 0), font=font)
            
            buffer = io.BytesIO()
            img.save(buffer, format='JPEG')
            article.featured_image.save(f"article_{i+1}.jpg", ContentFile(buffer.getvalue()), save=True)

        self.stdout.write("Database seeded successfully.")
