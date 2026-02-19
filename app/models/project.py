from django.db import models
from django.db import models
from django.utils.text import slugify
from app.models.organization import Organization
from app.models.user import User

class Project(models.Model):
    organization = models.ForeignKey(Organization, related_name="projects", on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    status = models.BooleanField() # active - True, archived - False
    visibillity = models.BooleanField() # public - True, private - False
    created_by = models.ForeignKey(User, related_name="projects", on_delete=models.DO_NOTHING)
    start_date = models.DateTimeField()
    due_date = models.DateTimeField() 
    created_at =  models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    