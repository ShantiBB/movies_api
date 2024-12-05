from rest_framework import serializers
from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer
from rest_framework.exceptions import ValidationError

from movie.models import Movie, FavoriteMovie

User = get_user_model()


class MovieSerializerList(serializers.ModelSerializer):
    author = serializers.CharField(source='author.username', read_only=True)

    is_favorite = serializers.SerializerMethodField()
    class Meta:
        model = Movie
        fields = (
            'id', 'author', 'title', 'description',
            'release_year', 'is_favorite'
        )

    def get_is_favorite(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return bool(obj.favorite_movies_for_user)
        return False


class MovieSerializerDetail(MovieSerializerList):

    def get_is_favorite(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            favorite = obj.favorite_users.filter(movie=obj, user=request.user)
            return favorite.exists()
        return False


class MovieSerializerCreate(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = ('title', 'description', 'release_year', 'author')
        extra_kwargs = {'author': {'read_only': True}}


class FavoriteMovieSerializerCreate(serializers.ModelSerializer):

    class Meta:
        model = FavoriteMovie
        fields = ('id',)

    def create(self, validated_data):
        user = validated_data.get('user')
        movie_id = validated_data.get('movie_id')
        movie = Movie.objects.get(id=movie_id)
        favorite_movie, flag = FavoriteMovie.objects.get_or_create(
            user=user, movie=movie
        )
        if not flag:
            raise ValidationError('Вы уже добавили фильм в избранное')
        return favorite_movie
