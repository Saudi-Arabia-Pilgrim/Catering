from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'full_name', 'role', 'is_staff', 'is_active',)
    list_filter = ('role', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('full_name',)}),
        (_('Department'), {'fields': ('role',)}),
        (_('Additional info'), {
            'fields': ('date_come', 'from_come', 'passport_number', 'given_by', 'validity_period', 
                      'expenses', 'monthly_salary', 'general_expenses'),
        }),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'full_name', 'role', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('username', 'full_name',)
    ordering = ('username',)

admin.site.register(CustomUser, CustomUserAdmin)
