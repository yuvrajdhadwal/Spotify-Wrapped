from django.db import models

# Create your models here.
from django.db import models

class Song(models.Model):
    title = models.CharField(max_length=100)
    runTime = models.IntegerField()