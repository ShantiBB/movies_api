from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Movie(models.Model):
    title = models.CharField(
        verbose_name='Название фильма',
        max_length=100, unique=True
    )
    description = models.CharField(
        verbose_name='Описание фильма',
        max_length=255, blank=True, null=True
    )
    release_year = models.PositiveSmallIntegerField(
        verbose_name='Год выпуска фильма'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='movies',
        verbose_name='Автор фильма'
    )
    is_favorite = models.ManyToManyField(User, through='FavoriteMovie')

    class Meta:
        verbose_name = "Фильм"
        verbose_name_plural = "Фильмы"

    def __str__(self):
        return self.title


class FavoriteMovie(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='favorite_movies'
    )
    movie = models.ForeignKey(
        Movie, on_delete=models.CASCADE, related_name='favorite_users'
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'

    def __str__(self):
        return f'{self.user.username}-{self.movie.title}'
