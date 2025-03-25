from apps.base.views import CustomListCreateAPIView, CustomRetrieveUpdateDestroyAPIView
from apps.menus.models import Recipe
from apps.menus.serializers import RecipeSerializer


class RecipeRetrieveUpdateDestroyAPIView(CustomRetrieveUpdateDestroyAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer


class RecipeListCreateAPIView(CustomListCreateAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer