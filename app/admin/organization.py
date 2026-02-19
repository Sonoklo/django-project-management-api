from django.contrib import admin
from app.models.organization import Organization

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    search_fields = ("name","slug","owner",)
    list_display = ("id", "name", "slug", "description", "owner", "is_active", "updated_at", "created_at")
    list_filter = ("is_active", "slug",)
    list_editable = ("is_active",)
    ordering = ("is_active", "updated_at", "created_at",)
    list_per_page = 5