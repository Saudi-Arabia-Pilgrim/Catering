from django.contrib import admin
from django.urls import path, include

from config.yasg import schema_view

urlpatterns = [
    # ======== Django ========
    path('i18n/', include('django.conf.urls.i18n')),  # <-- Add this clearly
    path("admin/", admin.site.urls),

    # ======== Debug Toolbar ========
    path('__debug__/', include('debug_toolbar.urls')),

    # ======== Ckeditor-5 =========
    path("ckeditor5/", include('django_ckeditor_5.urls')),

    # ✅ === DRF-YASG Endpoints ===
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='yasg-swagger'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='yasg-redoc'),

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
