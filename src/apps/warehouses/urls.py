from django.urls import path

from apps.warehouses import views 


urlpatterns = [
    # === RecipeFood URLs === 
    path('', views.WarehouseListCreateAPIView.as_view()),
    path('<str:pk>/', views.WarehouseRetrieveAPIView.as_view()),
]