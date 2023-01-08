from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):    
    pass

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True) 

    def __str__(self):
        return f"post {self.id} made by {self.author} on {self.date.strftime('%d.%m.%Y')}"    

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_who_liked")
    post = models.ForeignKey(Post,on_delete=models.CASCADE, related_name="liked_post")

    def __str__(self):
        return f"{self.user} liked {self.post}"

class Comment(models.Model):
    post = models.ManyToManyField(Post)
    author = models.ManyToManyField(User)
    text = models.CharField(max_length=100)

    def __str__(self):
        return f"Comment {self.author} on {self.post}"

class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="following_user")
    user_follower = models.ForeignKey(User,on_delete=models.CASCADE,related_name="followed_user") 
   
    def __str__ (self):  
        return f"{self.user} follows {self.user_follower}"