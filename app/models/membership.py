from django.db import models
from django.db import models
from django.utils.text import slugify
from app.models.user import User
from app.models.organization import Organization

class Membership(models.Model):
    user = models.ForeignKey(User, related_name="memberships", on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization,related_name="memberships", on_delete=models.CASCADE)
    ROLE_CHOICES = [
        ("owner", "owner"),
        ("admin", "admin"),
        ("manager", "manager"),
        ("developer", "developer"),
        ("viewer", "viewer"),
    ]
    role = models.CharField(max_length=9, choices=ROLE_CHOICES)
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.role
    class Meta:
        unique_together = ['user', 'organization']