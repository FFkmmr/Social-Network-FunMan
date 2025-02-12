from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import MyUser

class MyUserAdmin(UserAdmin):
    model = MyUser
    list_display = ('username', 'email', 'birthdate', 'is_active', 'is_staff')
    search_fields = ('username', 'email')
    ordering = ('username',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('email', 'birthdate')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'birthdate', 'password1', 'password2', 'is_active', 'is_staff')}
        ),
    )

admin.site.register(MyUser, MyUserAdmin)
