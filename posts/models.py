from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    content = models.CharField(max_length=140)
    created_at = models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateTimeField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.content}->({self.user})"