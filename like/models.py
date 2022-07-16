from django.db import models
from oAuth.models import NewUser
from svg.models import SvgPackage
# Create your models here.

class Like(models.Model):
    uid = models.ForeignKey(NewUser, on_delete=models.CASCADE)
    pid = models.ForeignKey(SvgPackage, on_delete=models.CASCADE)
    is_like = models.IntegerField(default=1)

class LikeCountRank(models.Model):
    pid = models.ForeignKey(SvgPackage, on_delete=models.CASCADE)
    range_count = models.IntegerField(default=0)
    created_data = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-range_count', )