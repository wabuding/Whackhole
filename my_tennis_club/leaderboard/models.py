from django.db import models

class Leaderboard(models.Model):
    username = models.CharField(max_length=20, default='')
    bestscore = models.IntegerField(default=0)
        