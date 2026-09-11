from django.contrib import admin
from .models import Author, AuthorProfile, Category, Publisher, Book, Publication

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    pass

@admin.register(AuthorProfile)
class AuthorProfileAdmin(admin.ModelAdmin):
    pass

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    pass

class PublicationInline(admin.TabularInline):
    model = Publication
    extra = 1

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author')
    filter_horizontal = ('categories',)
    inlines = [PublicationInline]
