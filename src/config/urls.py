from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from config.yasg import schema_view


urlpatterns = [
    # ======== Django ========
    path("admin/", admin.site.urls),

    # ======== Debug Toolbar ========
    path('__debug__/', include('debug_toolbar.urls')),

    # ======== Ckeditor-5 =========
    path("ckeditor5/", include('django_ckeditor_5.urls')),

    # ======== Simple JWT =========
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # ======== DRF-Spectacular ========
    path('api/v1/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/v1/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),


    # ======== Django Apps =========
    path('api/v1/users/', include('apps.users.urls')),

]
