
from django.db import models
from django.db import models
from django.utils.text import slugify
from app.models.user import User
from app.models.project import Project

class Task(models.Model):
    project = models.ForeignKey(Project, related_name="tasks", on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    reporter = models.ForeignKey(User, related_name="reported_tasks", on_delete=models.DO_NOTHING)
    assignee = models.ForeignKey(User, related_name="assigned_tasks", null=True, on_delete=models.DO_NOTHING)
    PRIORITY_CHOICES = [
        ("low", "low"),
        ("medium", "medium"),
        ("high", "high")
    ]
    priority = models.CharField(max_length=6, choices=PRIORITY_CHOICES)
    STATUS_CHOICES = [
        ("todo", "todo"),
        ("in_progress", "in_progress"),
        ("done", "done"),
        ("archived", "archived")
    ]
    status = models.CharField(max_length=11, choices=STATUS_CHOICES)
    due_date = models.DateTimeField()
    created_at =  models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title