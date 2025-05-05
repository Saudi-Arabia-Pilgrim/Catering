from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)

urlpatterns = [
    # ======== Django ========
    path('i18n/', include('django.conf.urls.i18n')),  # <-- Add this clearly
    path("admin/", admin.site.urls),

    # ======== Debug Toolbar ========
    path('__debug__/', include('debug_toolbar.urls')),

    # ======== Ckeditor-5 =========
    path("ckeditor5/", include('django_ckeditor_5.urls')),

    # ✅ === DRF-SPECTACULAAPIViewR Endpoints ===
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    ]

    # === URLs of Mukhsin ===
urlpatterns += [
    # ======== Authentication =========
    path('api/v1/auth/', include('apps.authentication.urls')),
    # ======== Users =========
    path('api/v1/users/', include('apps.users.urls')),
    # ======== HR =========
    path('api/v1/employee/', include('apps.expenses.urls')),
    # ======== Transports =========
    path('api/v1/transports/', include('apps.transports.urls')),
]

    # ========== URLS OF OYBEK ==============
urlpatterns += [
    path("api/v1/rooms/", include("apps.rooms.urls")),
    path("api/v1/hotels/", include("apps.hotels.urls")),
    path("api/v1/orders/", include("apps.orders.urls")),
    path("api/v1/statistics/", include("apps.statistics.urls"))
]


    # ========== URLS OF MUHAMMADALI ==============
urlpatterns += [
    path("api/v1/foods/", include("apps.foods.urls")),
    path("api/v1/menus/", include("apps.menus.urls")),
    path("api/v1/products/", include("apps.products.urls")),
    path("api/v1/warehouses/", include("apps.warehouses.urls")),
    path("api/v1/counter_agents/", include("apps.counter_agents.urls")),
    path("api/v1/sections/", include("apps.sections.urls")),
]


# ======== Static & Media Files (Development) ========
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)  # ======== Serve media files during development ========
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)  # ======== Serve static files during development ========
