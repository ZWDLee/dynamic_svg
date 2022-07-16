from django.db import models

from oAuth.models import NewUser
from svg.models import SvgPackage, Svg
# Create your models here.
class Collection(models.Model):
    coll_name = models.CharField(max_length=18, blank=False, null=False)
    author = models.ForeignKey(NewUser, on_delete=models.CASCADE)
    package = models.ForeignKey(SvgPackage, on_delete=models.SET_NULL, blank=True, null=True)
    is_coll = models.IntegerField(default=1)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.coll_name

class CollectionSvgList(models.Model):
    svg = models.ForeignKey(Svg, on_delete=models.SET_NULL, blank=True, null=True)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)
    is_coll = models.IntegerField(default=1)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)