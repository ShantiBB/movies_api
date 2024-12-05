from django.db.models import Prefetch


def favorite_filter_queryset(request, model, related_model):
    favorites = related_model.objects.filter(user=request.user)
    is_favorite = request.query_params.get('is_favorite', None)

    if is_favorite == '1':
        queryset = model.objects.filter(id__in=favorites.values('movie_id'))
    elif is_favorite == '0':
        queryset = model.objects.exclude(id__in=favorites.values('movie_id'))
    else:
        queryset = model.objects.all()

    queryset = queryset.prefetch_related(
        Prefetch(
            'favorite_users',
            queryset=favorites,
            to_attr='favorite_movies_for_user'
        )
    )
    return queryset
