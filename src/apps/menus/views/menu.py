from django.db.models import Q

from rest_framework.filters import SearchFilter
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend

from apps.base.views import (
    CustomListCreateAPIView,
    CustomRetrieveUpdateDestroyAPIView,
    CustomGenericAPIView,
)
from apps.menus.models import Menu
from apps.menus.serializers import (
    MenuSerializer,
    MenuCreateUpdateSerializer,
    OptimizedMenuSerializer,
)
from apps.menus.utils.missing_products import (
    calculate_missing_products_for_menu,
    calculate_missing_products_batch_menus,
)
from apps.warehouses.utils import validate_uuid


class MenuRetrieveUpdateDestroyAPIView(CustomRetrieveUpdateDestroyAPIView):
    queryset = Menu.objects.all().prefetch_related(
        "foods", "foods__recipes", "foods__recipes__product"
    )
    serializer_class = OptimizedMenuSerializer

    def get_serializer(self, *args, **kwargs):
        if self.request.method in ["PUT", "PATCH"] and self.request.data:
            return MenuCreateUpdateSerializer(*args, **kwargs)
        return super().get_serializer(*args, **kwargs)

    def update(self, request, *args, **kwargs):
        """
        Override update to use optimized serializer for response.
        """
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()

        # Use optimized serializer for response to avoid N+1 queries
        response_serializer = OptimizedMenuSerializer(
            instance, context=self.get_serializer_context()
        )
        return Response(response_serializer.data)

    def get_serializer_context(self):
        """
        Add batch missing products data to serializer context for optimization.
        """
        context = super().get_serializer_context()

        # Only calculate batch missing products for GET requests
        if self.request.method == "GET":
            instance = self.get_object()
            # Use individual calculation since we only have one instance
            # and it's already prefetched in the queryset
            missing_products = calculate_missing_products_for_menu(instance)
            context["missing_products_batch"] = {instance.id: missing_products}

        return context


class MenuListCreateAPIView(CustomListCreateAPIView):
    queryset = Menu.objects.all().prefetch_related(
        "foods", "foods__recipes", "foods__recipes__product"
    )
    serializer_class = OptimizedMenuSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["status", "menu_type"]
    search_fields = ["name", "gross_price", "profit"]

    def get_serializer(self, *args, **kwargs):
        if self.request.method == "POST":
            return MenuCreateUpdateSerializer(*args, **kwargs)
        return super().get_serializer(*args, **kwargs)

    def create(self, request, *args, **kwargs):
        """
        Override create to use optimized serializer for response.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()

        # Use optimized serializer for response to avoid N+1 queries
        response_serializer = OptimizedMenuSerializer(
            instance, context=self.get_serializer_context()
        )
        return Response(response_serializer.data, status=201)

    def get_serializer_context(self):
        """
        Add batch missing products data to serializer context for optimization.
        """
        context = super().get_serializer_context()

        # Only calculate batch missing products for list views (GET requests)
        if self.request.method == "GET":
            queryset = self.get_queryset()
            # Pre-calculate missing products for all menus in the queryset
            missing_products_batch = calculate_missing_products_batch_menus(queryset)
            context["missing_products_batch"] = missing_products_batch

        return context


class MenusOnRecipe(CustomGenericAPIView):
    queryset = Menu.objects.all().prefetch_related(
        "foods", "foods__recipes", "foods__recipes__product"
    )
    serializer_class = OptimizedMenuSerializer

    def get(self, request, pk):
        validate_uuid(pk)
        queryset = (
            self.get_queryset()
            .filter(
                Q(breakfast_recipes__id=pk)
                | Q(lunch_recipes__id=pk)
                | Q(dinner_recipes__id=pk)
            )
            .distinct()
        )

        # Pre-calculate missing products for batch optimization
        missing_products_batch = calculate_missing_products_batch_menus(queryset)

        serializer = self.get_serializer(
            queryset,
            many=True,
            context={"missing_products_batch": missing_products_batch},
        )
        return Response(serializer.data, status=200)
