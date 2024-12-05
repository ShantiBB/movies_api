from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    IsAuthenticated
)

from api.controllers import (
    get_movies_list,
    get_movie_detail,
    create_movie,
    update_movie,
    delete_movie,
    create_favorite_movie,
    delete_favorite_movie
)
from api.serializers import (
    MovieSerializerList,
    MovieSerializerDetail,
    MovieSerializerCreate,
    FavoriteMovieSerializerCreate
)
from api.permissions import IsAuthorOrReadOnly
from movie.models import Movie, FavoriteMovie


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def movies_list_or_create(request):
    if request.method == 'POST':
        return create_movie(request, MovieSerializerCreate)
    return get_movies_list(request, Movie, FavoriteMovie, MovieSerializerList)


@api_view(['GET', 'PATCH', 'DELETE'])
@permission_classes([IsAuthorOrReadOnly])
def movie_detail(request, pk):
    if request.method == 'PATCH':
        return update_movie(request, pk, Movie, MovieSerializerCreate)
    elif request.method == 'DELETE':
        return delete_movie(request, pk, Movie)
    return get_movie_detail(request, pk, Movie, MovieSerializerDetail)


@api_view(['POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def favorite_movie_create_or_delete(request, pk):
    if request.method == 'POST':
        return create_favorite_movie(
            request, pk, FavoriteMovieSerializerCreate
        )
    return delete_favorite_movie(request, pk, Movie, FavoriteMovie)
