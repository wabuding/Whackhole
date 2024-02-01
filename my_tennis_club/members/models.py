from django.db import models

class Member(models.Model):
    username = models.CharField(max_length=20, default='')
    password1 = models.CharField(max_length=256, default='')
    password2 = models.CharField(max_length=256, default='')
    is_login = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'