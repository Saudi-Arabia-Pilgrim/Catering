from rest_framework.filters import SearchFilter

from django_filters.rest_framework import DjangoFilterBackend

from apps.base.views import CustomListCreateAPIView, CustomRetrieveUpdateDestroyAPIView
from apps.menus.models import Recipe
from apps.menus.serializers import RecipeSerializer


class RecipeRetrieveUpdateDestroyAPIView(CustomRetrieveUpdateDestroyAPIView):
    queryset = Recipe.objects.all().select_related(
        "menu_breakfast", "menu_lunch", "menu_dinner"
    )
    serializer_class = RecipeSerializer


class RecipeListCreateAPIView(CustomListCreateAPIView):
    queryset = Recipe.objects.all().select_related(
        "menu_breakfast", "menu_lunch", "menu_dinner"
    )
    serializer_class = RecipeSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["status"]
    search_fields = ["name", "gross_price", "profit"]
