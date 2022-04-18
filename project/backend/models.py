from django.db import models

# Create your models here.
class User(models.Model):
    user_name = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=256)


    def __str__(self) -> str:
        return self.user_name
    
