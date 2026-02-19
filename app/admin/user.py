from django.contrib import admin
from app.models.user import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    search_fields = ('email', 'full_name')
    list_display = ("id","email","full_name", "is_active", "is_staff", "updated_at", "created_at")
    list_filter = ("is_active", "is_staff",)
    ordering = ("is_active", "is_staff", "updated_at", "created_at",)