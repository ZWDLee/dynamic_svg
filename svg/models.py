from django.db import models
from  oAuth.models import NewUser
# Create your models here.

class SvgPackage(models.Model):
    package_name = models.CharField(max_length=20, blank=False, null=False)
    package_description = models.CharField(max_length=64, blank=True, null=True)
    package_tag = models.CharField(max_length=100, blank=False, null=False)
    pure_svg_package = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(NewUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.package_name

class Svg(models.Model):
    svg_name = models.CharField(max_length=64, blank=False, null=False)
    svg_code = models.TextField()
    pure_svg = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    package = models.ForeignKey(SvgPackage, on_delete=models.CASCADE)
    author = models.ForeignKey(NewUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.svg_name

    def get_author(self):
        return self.author

    def get_package(self):
        return self.package
