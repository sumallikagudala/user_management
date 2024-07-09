from django.db import models

# Create your models here.
class user_data(models.Model):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.TextField()
    

    def __str__(self):
        return self.username


