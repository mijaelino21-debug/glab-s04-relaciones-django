from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path('', views.recommendations, name='recommendations'),
    path('<int:pk>/', views.movie_detail, name='movie_detail'),
]
