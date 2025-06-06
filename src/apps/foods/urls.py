from django.urls import path

from apps.foods import views

urlpatterns = [
    # === Food Section URLS ===
    path("sections/", views.FoodSectionListCreateAPIView.as_view()),
    path("sections/<str:pk>/", views.FoodSectionUpdateDestroyRetrieveAPIView.as_view()),
    # === RecipeFood URLs === 
    path('recipe_foods/', views.RecipeFoodListCreateAPIView.as_view()),
    path('recipe_foods/<str:pk>/', views.RecipeFoodRetrieveUpdateDestroyAPIView.as_view()),
    path('recipe_foods/on/food/<str:pk>/', views.RecipeFoodsOnFood.as_view()),

    # === Food URLs === 
    path('', views.FoodListCreateAPIView.as_view()),
    path('<str:pk>/', views.FoodRetrieveUpdateDestroyAPIView.as_view()),
    path('on/menu/<str:pk>/', views.FoodsOnMenu.as_view()),
]
