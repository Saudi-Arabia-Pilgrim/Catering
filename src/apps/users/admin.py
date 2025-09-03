from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('id', 'email', 'full_name', 'role', 'is_staff', 'is_active',)
    list_filter = ('role', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('full_name',)}),
        (_('Department'), {'fields': ('role',)}),
        (_('Additional info'), {
            'fields': ('date_come', 'from_come', 'passport_number', 'given_by', 'validity_period', 
                      'total_expenses', 'base_salary', 'total_general_expenses'),
        }),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'full_name', 'role', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email', 'full_name',)
    ordering = ('email',)

    # Override the default labels to make it clear that email is for email
    # def get_form(self, request, obj=None, **kwargs):
    #     form = super().get_form(request, obj, **kwargs)
    #     if 'username' in form.base_fields:
    #         form.base_fields['username'].label = _('Email address')
    #     return form

admin.site.register(CustomUser, CustomUserAdmin)
