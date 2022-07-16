from django.contrib import admin
from .models import NewUser
# Register your models here.

@admin.register(NewUser)
class NewUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'avatar', 'is_active')
    list_display_links = ('id', 'username', 'email', 'is_active')
