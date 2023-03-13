from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class CostumUser(AbstractUser):
    in_company = models.BooleanField(default=False)

class Profile(models.Model):
    user = models.OneToOneField(CostumUser, on_delete=models.CASCADE)
    avatar = models.ImageField( upload_to="static/images/avatars", null=True, blank=True)
    fullname = models.CharField( max_length=200, null=True, blank=True)
 
    @property
    def getavatar(self):
        try:
            url = self.avatar.url
        except:
            url = ''
        return url

    def __str__(self):
        return f"profile of {self.user.username}"
