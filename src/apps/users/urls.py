from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import UserViewSet, UserProfileAPIView

router = DefaultRouter()
router.register(r'', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('profile/', UserProfileAPIView.as_view(), name='profile'),
]
