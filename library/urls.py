from django.urls import path
from . import views

urlpatterns = [
    path('books/<int:pk>/', views.book_detail, name='book_detail'),
]