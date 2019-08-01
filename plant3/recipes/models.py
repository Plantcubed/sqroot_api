from django.db import models
import time

class Recipe(models.Model):
    name = models.CharField(max_length=100, blank=True)
    description = models.CharField(max_length=200, blank=True)
    index = models.PositiveIntegerField(editable=True)
    file = models.FileField(upload_to='recipes')
    type = models.PositiveIntegerField(editable=True)

class RecipeRuns(models.Model):
    class Meta:
        ordering = ['start_timestamp']
        get_latest_by = 'start_timestamp'

    start_timestamp = models.IntegerField(blank=True, default=time.time)
    end_timestamp = models.IntegerField(blank=True)
    recipe = models.ForeignKey(Recipe, related_name='runs')
    name = models.CharField(max_length=100, blank=True)

class RecipeControl(models.Model):
    current_recipe = models.PositiveIntegerField(editable=True)
    current_run = models.PositiveIntegerField(editable=True)
    startup = models.ForeignKey(Recipe, related_name='startup')
    shutdown = models.ForeignKey(Recipe, related_name='shutdown')
