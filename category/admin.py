from django.contrib import admin
from .models import CategoryModel

# Register your models here.
# Admin class for CategoryModel
class CategoryModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at','id')
    list_filter = ('created_at', 'updated_at')
    prepopulated_fields = {'slug': ('name',)}
# Admin class for CategoryModel
admin.site.register(CategoryModel, CategoryModelAdmin)