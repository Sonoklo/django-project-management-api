from django.contrib import admin
from app.models.project import Project

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    search_fields = ("title", "organization","created_by",)
    list_display = ("id", "title", "organization", "status", "visibillity", "created_by", "start_date", "due_date",)
    list_filter = ("status", "visibillity", "created_by",)
    ordering = ("status", "visibillity", "start_date", "due_date",)
    list_per_page = 10