from django.db import models
import time

class Actuator(models.Model):
    name = models.CharField(max_length=100, blank=True)
    index = models.PositiveIntegerField(editable=True)
    instruction_code = models.CharField(max_length=20, blank=True)
    instruction_id = models.PositiveIntegerField(editable=True)
    extra = models.CharField(max_length=200, blank=True)
    value = models.FloatField(editable=True)
    pre_over_value = models.FloatField(editable=True)
    timestamp = models.IntegerField(blank=True, default=time.time)
    override = models.BooleanField(editable=True)
    override_start = models.IntegerField(blank=True)
    override_end = models.IntegerField(blank=True)
    value_min = models.FloatField(editable=True)
    value_max = models.FloatField(editable=True)
    error_state = models.IntegerField(blank=True)
    dose_to = models.IntegerField(blank=True)
