from django.db import models

class Post(models.Model):
    name = models.CharField(max_length=200)
    content = models.TextField()
    gamer = models.ForeignKey("Gamer", on_delete=models.CASCADE)
    topic = models.ForeignKey("Topic", on_delete=models.CASCADE)
    image_url = models.CharField(max_length=200)
    created_on = models.DateTimeField(auto_now_add=True)