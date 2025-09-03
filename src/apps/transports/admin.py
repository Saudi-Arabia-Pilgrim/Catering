from django.contrib import admin

from apps.transports.models import Transport
from apps.transports.models.orders import Order


@admin.register(Transport)
class TransportAdmin(admin.ModelAdmin):
    """Admin interface for a Transport model."""
    list_display = ('id', 'name', 'name_of_driver', 'phone_number', 'amount_of_people', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('name', 'name_of_driver', 'phone_number', 'address')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at', 'created_by', 'updated_by')
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'name_of_driver', 'address', 'phone_number', 'amount_of_people', 'status')
        }),
        ('Timestamps and Audit', {
            'fields': ('created_at', 'created_by', 'updated_at', 'updated_by'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Admin interface for an Order model."""
    list_display = ('order_number', 'transport', 'perform_date', 'from_location', 'to_location', 'status', 'service_fee')
    list_filter = ('status', 'perform_date')
    search_fields = ('order_number', 'from_location', 'to_location')
    readonly_fields = ('id', 'created_at', 'updated_at', 'created_by', 'updated_by', 'order_number')
    fieldsets = (
        (None, {
            'fields': ('order_number', 'transport', 'perform_date', 'from_location', 'to_location', 'status')
        }),
        ('Additional Information', {
            'fields': ('passenger_count', 'service_fee')
        }),
        ('Timestamps and Audit', {
            'fields': ('created_at', 'created_by', 'updated_at', 'updated_by'),
            'classes': ('collapse',)
        }),
    )
