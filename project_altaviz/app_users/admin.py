from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# Register your models here.
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('username', 'first_name', 'last_name',
                                        'middle_name', 'phone', 'wphone',
                                        'address', 'department', 'deliveries',
                                        'pendings', 'is_deleted', 'profile_picture',
                                        'aboutme',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',
                                    'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'first_name',
                        'last_name', 'middle_name', 'phone', 'wphone', 'address',
                        'department', 'deliveries', 'pendings', 'is_deleted',
                        'profile_picture', 'aboutme',),
        }),
    )
    search_fields = ('email',)
    # search_fields = ('email', 'username',)
    ordering = ('email',)
    
admin.site.register(User, CustomUserAdmin)
