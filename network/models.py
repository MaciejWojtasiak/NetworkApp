from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)    

    def __str__(self):
        return f"Post {self.author}"    

class Like(models.Model):
    post = models.ManyToManyField(Post, blank=True)
    user = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return f"Like {self.user} on {self.post}"

class Comment(models.Model):
    post = models.ManyToManyField(Post)
    author = models.ManyToManyField(User)
    text = models.CharField(max_length=100)

    def __str__(self):
        return f"Comment {self.author} on {self.post}"