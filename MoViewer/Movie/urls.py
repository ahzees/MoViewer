from django.contrib import admin
from django.urls import path
from Movie.views import *

urlpatterns = [
    path('api/v1/movie', MovieAPIView.as_view()),
    path('api/v1/movie/<int:pk>/', TheMovieApiView.as_view()),
    path('media/', all_films, name='all_films'),
    path('filter/', FilterMovieView.as_view(), name='filter'),
    path('media/<slug:movie_slug>/', movie, name='movie'),
    path('media/like/<slug:movie_slug>', like_movie, name='like_movie'),
    path('media/dislike/<slug:movie_slug>', dislike_movie, name='dislike_movie'),
    path('media/<slug:category_slug>', category_movie, name='category_movie'),

]
