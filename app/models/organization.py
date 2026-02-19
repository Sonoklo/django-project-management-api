from django.db import models
from django.db import models
from django.utils.text import slugify
from app.models.user import User

class Organization(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, blank=True)
    def __generate_slug(self):
        slug = slugify(self.name,allow_unicode=True)
        text_slug = slug
        counter = 1
        while Organization.objects.filter(slug=slug).exists():
            slug = f"{text_slug}_{counter}"
            counter += 1
        return slug

    def save(self, *args, **kwargs):
        if not self.pk or not self.slug: 
            self.slug = self.__generate_slug()
        elif self.name != Organization.objects.get(pk=self.pk).name: 
            self.slug = self.__generate_slug()
        super().save(*args, **kwargs)

    description = models.CharField(max_length=200)
    owner = models.ForeignKey(User, related_name="organizations", on_delete=models.CASCADE) 
    is_active = models.BooleanField(default=False)
    created_at =  models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name