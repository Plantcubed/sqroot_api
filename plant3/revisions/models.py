from django.db import models

class Revision(models.Model):
    name = models.CharField(max_length=100, blank=True)
    major = models.IntegerField(blank=True, default=0)
    minor = models.IntegerField(blank=True, default=0)
    build = models.IntegerField(blank=True, default=0)
