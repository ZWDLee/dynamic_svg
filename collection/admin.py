from django.contrib import admin
from .models import Collection, CollectionSvgList
# Register your models here.

@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['id', 'coll_name', 'author', 'package', 'is_coll', 'created_date', 'updated_date']

@admin.register(CollectionSvgList)
class CollectionSvgListAdmin(admin.ModelAdmin):
    list_display = ['id', 'collection', 'svg', 'is_coll', 'created_date', 'updated_date']