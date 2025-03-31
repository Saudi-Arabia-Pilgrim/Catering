from django.urls import path

from apps.counter_agents import views


urlpatterns = [
    # === Counter Agents URLs === 
    path('', views.CounterAgentListCreateAPIView.as_view()),
    path('<str:pk>/', views.CounterAgentRetrieveUpdateDestroyAPIView.as_view()),
]