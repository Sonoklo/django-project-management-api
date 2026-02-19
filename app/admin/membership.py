from django.contrib import admin
from app.models.membership import Membership

@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    search_fields = ("user","organization","role",)
    list_display = ("id", "user", "organization", "role", "joined_at")
    list_filter = ("role", "user",)
    ordering = ("joined_at",)
    list_per_page = 10