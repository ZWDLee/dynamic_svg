from django.contrib import admin

from .models import SvgPackage, Svg
# Register your models here.

@admin.register(Svg)
class SvgAdmin(admin.ModelAdmin):
    list_display = ['id', 'svg_name', 'svg_code', 'pure_svg', 'package', 'author', 'updated_date', 'created_date']
    list_display_links = ['svg_name', 'svg_code', 'package', 'author']

@admin.register(SvgPackage)
class SvgPackageAdmin(admin.ModelAdmin):
    list_display = ['id', 'package_name', 'package_description', 'author', 'updated_date', 'created_date']
    list_display_links = ['id', 'package_name', 'package_description']