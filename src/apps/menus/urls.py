from django.urls import path

from apps.menus import views 


urlpatterns = [
    # === Recipe URLs === 
    path('recipes/', views.RecipeListCreateAPIView.as_view()),
    path('recipes/<str:pk>/', views.RecipeRetrieveUpdateDestroyAPIView.as_view()),

    # === Menu URLs === 
    path('', views.MenuListCreateAPIView.as_view()),
    path('<str:pk>/', views.MenuRetrieveUpdateDestroyAPIView.as_view()),
    path('on/recipe/<str:pk>/', views.MenusOnRecipe.as_view()),

]