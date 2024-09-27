from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import *
# Register your models here.


class UserAdmin(BaseUserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'name', 'phone', 'city', 'role', 'otp')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('username', 'name', 'phone', 'city', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions')}),
    )
    search_fields = ('email',)
    ordering = ('email',)


class EmpAdmin(admin.ModelAdmin):
    list_display = ['emp_name', 'emp_email', 'emp_department', 'emp_role', 'emp_city']

class ActivityAdmin(admin.ModelAdmin):
    list_display = ['user', 'activity', 'timestamp']


admin.site.register(CustomUser, UserAdmin)
admin.site.register(Department)
admin.site.register(UserRole)
admin.site.register(Expense)
admin.site.register(Employee, EmpAdmin)
admin.site.register(ActivityLog, ActivityAdmin)
