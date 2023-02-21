from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import RegisterForm
from .models import *
from django.contrib.admin import AdminSite

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):

    fieldsets = (
        (None, {'fields':('email',)}),
        ('Personal info',{'fields': ('first_name','last_name',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',
                                    'groups', 'user_permissions',)}),
    )
    add_fieldsets = (
        (None,{
            'classes':('wide',),
            'fields':('email','password1','password2',
                                             'first_name','last_name','sex','is_active','is_staff')}),
    )
    ordering = ['id']
    list_display = ['email','first_name','id']
    list_display_links = ['first_name','email']
    readonly_fields = ['last_login']
