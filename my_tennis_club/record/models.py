from django.db import models

class PlayRecord(models.Model):
    username = models.CharField(max_length=20)
    score = models.IntegerField()
    date = models.DateTimeField()