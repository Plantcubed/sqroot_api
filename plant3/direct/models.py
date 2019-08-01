from django.db import models
import time

class Direct(models.Model):
    command = models.CharField(max_length=100, blank=True)
    command_timestamp = models.IntegerField(blank=True, default=time.time)
    command_waitto = models.IntegerField(blank=True, default=time.time)
    command_timeo = models.BooleanField(editable=True)
    command_rdy = models.BooleanField(editable=True)
    results = models.CharField(max_length=100, blank=True)
    results_timestamp = models.IntegerField(blank=True, default=time.time)
    results_rdy = models.BooleanField(editable=True)

class Runs(models.Model):
    current_run = models.PositiveIntegerField(editable=True)
    current_run_index = models.PositiveIntegerField(editable=True)
