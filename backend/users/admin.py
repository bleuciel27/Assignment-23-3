from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'created_at')
    search_fields = ('username', 'email')
    readonly_fields = ('created_at', 'updated_at')
    
    # Add custom fields to the user admin
    fieldsets = UserAdmin.fieldsets + (
        ('Profile Info', {'fields': ('profile_image', 'bio', 'created_at', 'updated_at')}),
    )