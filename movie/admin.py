from django.contrib import admin

from movie.models import Movie, FavoriteMovie


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'release_year', 'author__username', 'times_favorited'
    )
    search_fields = ('title', 'author__username')
    list_filter = ('title', 'release_year', 'author__username')

    def times_favorited(self, obj):
        return FavoriteMovie.objects.filter(movie=obj).count()

    times_favorited.short_description = 'Добавлений в избранное'


@admin.register(FavoriteMovie)
class FavoriteMovieAdmin(admin.ModelAdmin):
    list_display = ('user__username', 'movie__title')
    search_fields = ('user__username', 'movie__title')
    list_filter = ('user__username', 'movie__title')
