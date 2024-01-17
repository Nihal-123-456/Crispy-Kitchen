from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Food)
admin.site.register(Review)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('name',)}
    list_display = ['name', 'slug']
    
admin.site.register(Category, CategoryAdmin)