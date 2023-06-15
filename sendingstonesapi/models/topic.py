from django.db import models

class Topic(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    game = models.ForeignKey("Game", on_delete=models.CASCADE)