from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.utils.translation import gettext_lazy
# Create your models here.

class NewUser(AbstractUser):
    avatar = models.ImageField(upload_to='user_avatar/%Y/%m/%d', null=True, blank=True,
                               default='default/avatar.svg')
    email = models.EmailField(null=False, unique=True, max_length=100)
    last_login = models.DateTimeField(gettext_lazy('last login'), blank=True, null=True, auto_now=True)
    objects = UserManager()

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'
        pass

    def __str__(self):
        return self.username
