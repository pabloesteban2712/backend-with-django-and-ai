from django.db import models

# Create your models here.
class User(models.Model):
    name      = models.CharField(max_length=30)
    surname   = models.CharField(max_length=100)
    nick      = models.CharField(max_length=30)
    email     = models.EmailField(max_length=50)
    bio       = models.CharField(max_length=220)
    password  = models.CharField(max_length=150)
    createdAt = models.DateField(auto_now_add=True)

class Article(models.Model):
    title     = models.CharField(max_length=100)
    content   = models.TextField()
    user      = models.ForeignKey(User, on_delete=models.CASCADE)
    createdAt = models.DateField(auto_now_add=True) 

