from django.contrib import admin
from django.db.models import Sum
from django.urls import reverse
from django.utils.html import format_html

from apps.expenses.models.hiring import HiringExpense
from apps.expenses.models.monthly_salary import MonthlySalary


@admin.register(HiringExpense)
class HiringExpenseAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user_link', 'formatted_date', 'formatted_cost', 'payment_status', 'created_at')
    list_filter = ('status', 'date', 'created_at', 'user')
    search_fields = ('title', 'user__email', 'user__full_name')
    date_hierarchy = 'date'
    # list_editable = ('status',)
    readonly_fields = ('id', 'created_at', 'created_by', 'updated_at', 'updated_by')
    actions = ['mark_as_paid', 'mark_as_unpaid']
    list_per_page = 20

    fieldsets = (
        ('Expense Information', {
            'fields': ('title', 'user', 'date', 'cost', 'status'),
            'classes': ('wide', 'extrapretty'),
        }),
        ('Audit Information', {
            'fields': ('id', 'created_at', 'created_by', 'updated_at', 'updated_by'),
            'classes': ('collapse',),
        }),
    )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('user', 'created_by', 'updated_by')

    def user_link(self, obj):
        url = reverse("admin:users_customuser_change", args=[obj.user.id])
        return format_html('<a href="{}">{}</a>', url, obj.user.email)
    user_link.short_description = 'User'
    user_link.admin_order_field = 'user__email'

    def formatted_date(self, obj):
        return obj.date.strftime("%d %b %Y, %H:%M")
    formatted_date.short_description = 'Date'
    formatted_date.admin_order_field = 'date'

    def formatted_cost(self, obj):
        color = 'red' if float(obj.cost) > 1000 else 'green'
        formatted_value = "${:.2f}".format(float(obj.cost))
        return format_html('<span style="color: {}; font-weight: bold;">{}</span>', 
                          color,
                          formatted_value)
    formatted_cost.short_description = 'Cost (USD)'
    formatted_cost.admin_order_field = 'cost'

    def payment_status(self, obj):
        if obj.status:
            return format_html('<span style="color: green; font-weight: bold;">✓ Paid</span>')
        return format_html('<span style="color: red; font-weight: bold;">✗ Unpaid</span>')
    payment_status.short_description = 'Payment Status'
    payment_status.admin_order_field = 'status'

    def mark_as_paid(self, request, queryset):
        updated = queryset.update(status=True)
        self.message_user(request, "{} expenses marked as paid.".format(updated))
    mark_as_paid.short_description = "Mark selected expenses as paid"

    def mark_as_unpaid(self, request, queryset):
        updated = queryset.update(status=False)
        self.message_user(request, "{} expenses marked as unpaid.".format(updated))
    mark_as_unpaid.short_description = "Mark selected expenses as unpaid"

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context)

        try:
            qs = response.context_data['cl'].queryset
            total_cost = qs.aggregate(total=Sum('cost'))['total'] or 0
            paid_cost = qs.filter(status=True).aggregate(total=Sum('cost'))['total'] or 0
            unpaid_cost = qs.filter(status=False).aggregate(total=Sum('cost'))['total'] or 0

            extra_context = extra_context or {}
            extra_context['total_cost'] = total_cost
            extra_context['paid_cost'] = paid_cost
            extra_context['unpaid_cost'] = unpaid_cost
            response.context_data.update(extra_context)
        except (AttributeError, KeyError):
            pass

        return response


@admin.register(MonthlySalary)
class MonthlySalaryAdmin(admin.ModelAdmin):
    list_display = ('employee_name', 'formatted_salary', 'month_year_display', 'payment_status', 'created_at')
    list_filter = ('status', 'date', 'created_at', 'user')
    search_fields = ('title', 'user__email', 'user__full_name')
    date_hierarchy = 'date'
    # list_editable = ('status',)
    readonly_fields = ('id', 'created_at', 'created_by', 'updated_at', 'updated_by', 'month_year_display')
    actions = ['mark_as_paid', 'mark_as_unpaid']
    list_per_page = 20

    fieldsets = (
        ('Salary Information', {
            'fields': ('user', 'salary', 'date', 'status', 'month_year_display'),
            'classes': ('wide', 'extrapretty'),
        }),
        ('Audit Information', {
            'fields': ('id', 'created_at', 'created_by', 'updated_at', 'updated_by'),
            'classes': ('collapse',),
        }),
    )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('user', 'created_by', 'updated_by')

    def employee_name(self, obj):
        url = reverse("admin:users_customuser_change", args=[obj.user.id])
        full_name = "{} {}".format(obj.user.first_name, obj.user.last_name) if obj.user.first_name else obj.user.email
        return format_html('<a href="{}">{}</a>', url, full_name)
    employee_name.short_description = 'Employee'
    employee_name.admin_order_field = 'user__email'

    def month_year_display(self, obj):
        return format_html('<span style="font-weight: bold;">{}</span>', obj.month_year)
    month_year_display.short_description = 'Month/Year'
    month_year_display.admin_order_field = 'date'

    def formatted_salary(self, obj):
        color = 'purple' if obj.salary > 5000 else 'blue'
        formatted_value = "${:.2f}".format(float(obj.salary))
        return format_html('<span style="color: {}; font-weight: bold;">{}</span>', 
                          color,
                          formatted_value)
    formatted_salary.short_description = 'Salary (USD)'
    formatted_salary.admin_order_field = 'salary'

    def payment_status(self, obj):
        if obj.status:
            return format_html('<span style="color: green; font-weight: bold;">✓ Paid</span>')
        return format_html('<span style="color: red; font-weight: bold;">✗ Unpaid</span>')
    payment_status.short_description = 'Payment Status'
    payment_status.admin_order_field = 'status'

    def mark_as_paid(self, request, queryset):
        updated = queryset.update(status=True)
        self.message_user(request, "{} salaries marked as paid.".format(updated))
    mark_as_paid.short_description = "Mark selected salaries as paid"

    def mark_as_unpaid(self, request, queryset):
        updated = queryset.update(status=False)
        self.message_user(request, "{} salaries marked as unpaid.".format(updated))
    mark_as_unpaid.short_description = "Mark selected salaries as unpaid"

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context)

        try:
            qs = response.context_data['cl'].queryset
            total_salary = qs.aggregate(total=Sum('salary'))['total'] or 0
            paid_salary = qs.filter(status=True).aggregate(total=Sum('salary'))['total'] or 0
            unpaid_salary = qs.filter(status=False).aggregate(total=Sum('salary'))['total'] or 0

            extra_context = extra_context or {}
            extra_context['total_salary'] = total_salary
            extra_context['paid_salary'] = paid_salary
            extra_context['unpaid_salary'] = unpaid_salary
            response.context_data.update(extra_context)
        except (AttributeError, KeyError):
            pass

        return response
