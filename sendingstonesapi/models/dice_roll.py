from django.db import models

class DiceRoll(models.Model):
    gamer = models.ForeignKey("Gamer", on_delete=models.CASCADE)
    dice_type = models.CharField(max_length=200)
    roll_result = models.IntegerField()