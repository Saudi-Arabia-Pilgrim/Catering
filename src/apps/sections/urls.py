from django.urls import path

from apps.sections import views


urlpatterns = [
    # === Measure URLs ===
    path("measures/", views.MeasureListCreateAPIView.as_view()),
    path("measures/<str:pk>/", views.MeasureRetrieveUpdateDestroyAPIView.as_view()),

    # === Section URLs ===
    path("", views.SectionListCreateAPIView.as_view()),
    path("<str:pk>/", views.SectionRetrieveUpdateDestroyAPIView.as_view()),
]
