from django.urls import path, include

from api.views import (
    movies_list_or_create,
    movie_detail,
    favorite_movie_create_or_delete
)

urlpatterns = [
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('movies/', movies_list_or_create, name='movies-list'),
    path('movies/<int:pk>/', movie_detail, name='movies-detail'),
    path(
        'movies/<int:pk>/favorite/',
        favorite_movie_create_or_delete,
        name='movies-favorite'
    )
]
