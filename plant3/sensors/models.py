from django.db import models

class Sensor(models.Model):
    name = models.CharField(max_length=100, blank=True)
    index = models.PositiveIntegerField(editable=True)
    instruction_code = models.CharField(max_length=20, blank=True)
    instruction_id = models.PositiveIntegerField(editable=True)
    extra = models.CharField(max_length=200, blank=True)
    value = models.FloatField(editable=True)