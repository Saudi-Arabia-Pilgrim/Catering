from rest_framework.filters import SearchFilter

from django_filters.rest_framework import DjangoFilterBackend

from apps.base.views import CustomListCreateAPIView, CustomRetrieveUpdateDestroyAPIView
from apps.products.models import Product
from apps.products.serializers import ProductSerializer


class ProductRetrieveUpdateDestroyAPIView(CustomRetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all().select_related(
        "measure_warehouse", "measure", "section"
    )
    serializer_class = ProductSerializer


class ProductListCreateAPIView(CustomListCreateAPIView):
    queryset = Product.objects.all().select_related(
        "measure_warehouse", "measure", "section"
    )
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["status", "section"]
    search_fields = [
        "measure__name",
        "measure_warehouse__name",
        "measure__abbreviation",
        "measure_warehouse__abbreviation",
        "name",
        "section__name",
    ]
