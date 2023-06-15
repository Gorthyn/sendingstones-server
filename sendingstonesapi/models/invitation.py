from django.db import models

class Invitation(models.Model):
    sender = models.ForeignKey("Gamer", on_delete=models.CASCADE, related_name="game_master")
    receiver = models.ForeignKey("Gamer", on_delete=models.CASCADE, related_name="player")
    status = models.CharField(max_length=10, default='pending')
    game =  models.ForeignKey("Game", on_delete=models.CASCADE, null=True)
