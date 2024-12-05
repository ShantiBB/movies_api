from functools import partial

from django.contrib.auth import get_user_model
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.response import Response

from api.filters import favorite_filter_queryset

User = get_user_model()


def get_movies_list(request, model, related_model, model_serializer):
    context = {'request': request}
    if request.user.is_authenticated:
        queryset = favorite_filter_queryset(request, model, related_model)
    else:
        queryset = model.objects.all()
    queryset = queryset.select_related('author')
    serializer = model_serializer(queryset, context=context, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


def get_movie_detail(request, pk, model, model_serializer):
    context = {'request': request}
    obj = get_object_or_404(model, id=pk)
    serializer = model_serializer(instance=obj, context=context)
    response_data = serializer.data
    return Response(response_data, status=status.HTTP_200_OK)


def create_movie(request, model_serializer):
    serializer = model_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save(author=request.user)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


def update_movie(request, pk, model, model_serializer):
    obj = get_object_or_404(model, id=pk)
    serializer = model_serializer(
        instance=obj, data=request.data, partial=True
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)


def delete_movie(request, pk, model):
    obj = get_object_or_404(model, id=pk)
    obj.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


def create_favorite_movie(request, pk, model_serializer):
    context = {'request': request}
    serializer = model_serializer(data=request.data, context=context)
    serializer.is_valid(raise_exception=True)
    serializer.save(user=request.user, movie_id=pk)
    message = {'message': 'Вы успешно добавили фильм в избранное'}
    return Response(message, status=status.HTTP_201_CREATED)


def delete_favorite_movie(request, pk, model, related_model):
    movie = get_object_or_404(model, id=pk)
    obj = get_object_or_404(related_model, user=request.user, movie=movie)
    obj.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
