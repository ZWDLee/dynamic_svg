from django.contrib import admin
from .models import Like, LikeCountRank
# Register your models here.

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['id', 'uid', 'pid', 'is_like']
    list_display_links = ['id', 'uid', 'pid', 'is_like']

@admin.register(LikeCountRank)
class LikeCountRankAdmin(admin.ModelAdmin):
    list_display = ['id', 'pid', 'range_count']