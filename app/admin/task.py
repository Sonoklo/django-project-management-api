from django.contrib import admin
from app.models.task import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    search_fields = ("project", "title","reporter","assignee")
    list_display = ("id", "project", "title","description","reporter","assignee", "status",  "priority", "due_date", "deleted_at")
    list_filter = ("status", "assignee", "priority",)
    ordering = ("status", "assignee", "priority", "due_date")
    list_per_page = 10