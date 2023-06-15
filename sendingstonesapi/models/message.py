from django.db import models

class Message(models.Model):
    sender = models.ForeignKey("Gamer", related_name='sender', on_delete=models.CASCADE)
    recipient = models.ForeignKey("Gamer", related_name='recipient', on_delete=models.CASCADE)
    content = models.TextField()
    sent_on = models.DateTimeField(auto_now_add=True)