from rest_framework import viewsets

from apps.base.serializers import EmptySerializer
from apps.base.views.api_tags import AutoTaggedAPIViewSets


class CustomViewSet(viewsets.ViewSet, AutoTaggedAPIViewSets):
    """
    Basic ViewSet providing standard CRUD operations.
    Most basic and flexible ViewSet with minimal built-in functionality.
    Requires manual implementation of list, create, retrieve, update, destroy methods.

        Example usage:
            router.register(r'items', CustomViewSet, basename='item')
    """
    serializer_class = EmptySerializer
    queryset = []


class CustomGenericViewSet(viewsets.GenericViewSet, AutoTaggedAPIViewSets):
    """
    Generic ViewSet that provides base functionality like
    queryset and serializer handling, but no default actions.
    Typically used when you want to mix in specific action mixins.

    Example usage: Combine with mixins like ListModelMixin for specific functionality

        class MyCustomViewSet(mixins.ListModelMixin, CustomGenericViewSet):
            queryset = MyModel.objects.all()
            serializer_class = MyModelSerializer
    """
    serializer_class = EmptySerializer
    queryset = []


class CustomModelViewSet(viewsets.ModelViewSet, AutoTaggedAPIViewSets):
    """
    Full-featured ViewSet providing complete CRUD operations.
    Includes list, create, retrieve, update, partial_update, and destroy actions.
    Automatically handles database model operations with minimal custom code.

        Example usage:
            router.register(r'products', CustomModelViewSet, basename='product')
            Automatically provides GET, POST, PUT, PATCH, DELETE endpoints
    """
    serializer_class = EmptySerializer
    queryset = []


class CustomReadOnlyModelViewSet(viewsets.ReadOnlyModelViewSet, AutoTaggedAPIViewSets):
    """
    Read-only ViewSet providing only list and retrieve actions.
    Prevents modification of resources, useful for public/restricted access endpoints.

        Example usage:
            router.register(r'reports', CustomReadOnlyModelViewSet, basename='report')
            Only provides GET list and GET single item endpoints
    """
    serializer_class = EmptySerializer
    queryset = []