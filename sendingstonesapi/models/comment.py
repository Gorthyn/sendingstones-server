from django.db import models

class Comment(models.Model):
    content = models.TextField()
    gamer = models.ForeignKey("Gamer", on_delete=models.CASCADE)
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    image_url = models.CharField(max_length=200)
    created_on = models.DateTimeField(auto_now_add=True)

    @property
    def can_edit(self):
        return self.__can_edit

    @can_edit.setter
    def can_edit(self, value):
        self.__can_edit = value

    @property
    def can_delete(self):
        return self.__can_delete
    
    @can_delete.setter
    def can_delete(self, value):
        self.__can_delete = value