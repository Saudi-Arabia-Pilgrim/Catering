from apps.base.views import CustomListCreateAPIView, CustomRetrieveUpdateDestroyAPIView
from apps.foods.models import RecipeFood
from apps.foods.serializers import RecipeFoodSerializer


class RecipeFoodRetrieveUpdateDestroyAPIView(CustomRetrieveUpdateDestroyAPIView):
    queryset = RecipeFood.objects.all()
    serializer_class = RecipeFoodSerializer


class RecipeFoodListCreateAPIView(CustomListCreateAPIView):
    queryset = RecipeFood.objects.all()
    serializer_class = RecipeFoodSerializer