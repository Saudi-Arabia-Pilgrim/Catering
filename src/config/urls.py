from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
)

from config.yasg import schema_view


urlpatterns = [
    # ======== Django ========
    path("admin/", admin.site.urls),

    # ======== Debug Toolbar ========
    path('__debug__/', include('debug_toolbar.urls')),

    # ======== Ckeditor-5 =========
    path("ckeditor5/", include('django_ckeditor_5.urls')),

    # ======== DRF-Spectacular ========
    path('api/v1/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/v1/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),


    # === URLs of Mukhsin ===
        path('api/v1/users/', include('apps.users.urls')),
        # ======== Authentication =========
        path('api/v1/auth/', include('apps.authentication.urls')),

    ]

    # ========== URLS OF OYBEK ==============
urlpatterns += [
    path("api/v1/rooms/", include("apps.rooms.urls")),
    path("api/v1/hotels/", include("apps.hotels.urls")),
    path("api/v1/guests/", include("apps.guests.urls")),
    path("api/v1/orders/", include("apps.orders.urls")),
]
