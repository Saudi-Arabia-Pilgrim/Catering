from apps.base.views import CustomListCreateAPIView, CustomRetrieveUpdateDestroyAPIView
from apps.products.models import Product
from apps.products.serializers import ProductSerializer


class ProductRetrieveUpdateDestroyAPIView(CustomRetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all().select_related("measure_warehouse", "measure", "section")
    serializer_class = ProductSerializer


class ProductListCreateAPIView(CustomListCreateAPIView):
    queryset = Product.objects.all().select_related("measure_warehouse", "measure", "section")
    serializer_class = ProductSerializer