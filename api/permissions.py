from django.shortcuts import get_object_or_404
from rest_framework.permissions import BasePermission, SAFE_METHODS

from movie.models import Movie


class IsAnonCreateUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_anonymous


class IsAuthUserOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if view.action == 'me' and request.user.is_anonymous:
            return False
        return True

    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or request.user == obj


class IsAuthorOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        obj_id = view.kwargs.get('pk')
        obj = get_object_or_404(Movie, id=obj_id)
        if request.method in SAFE_METHODS:
            return True
        if request.user and request.user.is_authenticated:
            return request.user == obj.author
