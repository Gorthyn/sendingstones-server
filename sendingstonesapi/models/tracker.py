from django.db import models

class Tracker(models.Model):
    gamer = models.ForeignKey("Gamer", on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    input_name = models.CharField(max_length=200)
    initiative = models.IntegerField()