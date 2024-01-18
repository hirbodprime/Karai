from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class BaseCategoryModel(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=500, allow_unicode=True, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    hidden = models.BooleanField(default=False)
    class Meta:
        abstract = True
        
    def __str__(self):
        return self.name
class CategoryModel(BaseCategoryModel):
    image = models.ImageField(upload_to='category/', blank=True, null=True)
    class Meta:
        verbose_name_plural = "Categories"
    def __str__(self):
        return self.name
