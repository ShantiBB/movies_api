from django.contrib import admin
from django.contrib.auth import get_user_model

from movie.models import FavoriteMovie

User = get_user_model()


class FavoriteInline(admin.TabularInline):
    model = FavoriteMovie
    extra = 1
    fk_name = 'user'


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name')
    search_fields = ('username', 'email')
    list_filter = ('username', 'email')
    inlines = (FavoriteInline,)
