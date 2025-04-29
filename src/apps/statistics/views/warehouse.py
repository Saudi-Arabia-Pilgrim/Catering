from rest_framework.response import Response

from apps.base.views import CustomGenericAPIView
from apps.warehouses.models import Experience


class CheckoutListAPIView(CustomGenericAPIView):
    def get(self, request, *args, **kwargs):
        experiences = Experience.objects.all()
        data = {}

        for experience in experiences:
            product = experience.warehouse.product

            if experience.warehouse.product.name not in data:
                data = {
                    product.name : {
                        "measure": product.measure_warehouse.abbreviation,
                        "count": int(experience.count) / product.measure_warehouse.difference_measures,
                        "section": product.section.name,
                        "price": experience.price,
                        "image": request.build_absolute_uri(product.image.url) if product.image else None
                    }
                }
            else:
                data[product.name]["count"] += int(experience.count) / product.measure_warehouse.difference_measures
                data[product.name]["price"] += experience.price

        return Response(data)
