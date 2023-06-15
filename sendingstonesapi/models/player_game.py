from django.db import models

class PlayerGame(models.Model):
    gamer = models.ForeignKey("Gamer", on_delete=models.CASCADE)
    game = models.ForeignKey("Game", on_delete=models.CASCADE)
    role = models.CharField(max_length=200)