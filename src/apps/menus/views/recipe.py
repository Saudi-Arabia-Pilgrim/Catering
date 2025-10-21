from rest_framework.filters import SearchFilter

from django_filters.rest_framework import DjangoFilterBackend

from apps.base.views import CustomListCreateAPIView, CustomRetrieveUpdateDestroyAPIView
from apps.menus.models import Recipe
from apps.menus.serializers import RecipeSerializer, OptimizedRecipeSerializer
from apps.menus.utils.missing_products import calculate_missing_products_batch_recipes


class RecipeRetrieveUpdateDestroyAPIView(CustomRetrieveUpdateDestroyAPIView):
    queryset = Recipe.objects.all().select_related(
        "menu_breakfast", "menu_lunch", "menu_dinner"
    )
    serializer_class = RecipeSerializer


class RecipeListCreateAPIView(CustomListCreateAPIView):
    queryset = Recipe.objects.all().select_related(
        "menu_breakfast", "menu_lunch", "menu_dinner"
    ).prefetch_related(
        "menu_breakfast__foods__recipes__product",
        "menu_lunch__foods__recipes__product",
        "menu_dinner__foods__recipes__product"
    )
    serializer_class = OptimizedRecipeSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["status"]
    search_fields = ["name", "gross_price", "profit"]

    def get_serializer_context(self):
        """
        Add batch missing products data to serializer context for optimization.
        """
        context = super().get_serializer_context()

        # Only calculate batch missing products for list views (GET requests)
        if self.request.method == "GET":
            queryset = self.get_queryset()
            # Pre-calculate missing products for all recipes in the queryset
            missing_products_batch = calculate_missing_products_batch_recipes(queryset)
            context['missing_products_batch'] = missing_products_batch

        return context
