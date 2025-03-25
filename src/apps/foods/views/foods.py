from apps.base.views import CustomListCreateAPIView, CustomRetrieveUpdateDestroyAPIView
from apps.foods.models import Food
from apps.foods.serializers import FoodSerializer


class FoodRetrieveUpdateDestroyAPIView(CustomRetrieveUpdateDestroyAPIView):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer


class FoodListCreateAPIView(CustomListCreateAPIView):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer