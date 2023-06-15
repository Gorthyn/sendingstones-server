from django.db import models

class Game(models.Model):
    name = models.CharField(max_length=200)
    game_master = models.ForeignKey("Gamer", on_delete=models.CASCADE, related_name='games_moderated')
    description = models.TextField()
    players = models.ManyToManyField("Gamer", related_name='games')