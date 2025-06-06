from django.urls import path

from apps.products import views


urlpatterns = [
    # == Product URLs ===
    path("", views.ProductListCreateAPIView.as_view()),
    path("<str:pk>/", views.ProductRetrieveUpdateDestroyAPIView.as_view()),
    path("in/warehouse/<str:pk>/", views.ProductInWarehouse.as_view()),
]
