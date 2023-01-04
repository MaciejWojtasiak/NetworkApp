from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):    
    pass

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)  
    likesNumber = models.IntegerField(default=0)  

    def __str__(self):
        return f"{self.author} {self.text}"    

class Like(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE, related_name="LikedPost")
    user = models.ManyToManyField(User, blank =True, related_name="userInfo")

    def __str__(self):
        return f"{self.user} liked {self.post}"

class Comment(models.Model):
    post = models.ManyToManyField(Post)
    author = models.ManyToManyField(User)
    text = models.CharField(max_length=100)

    def __str__(self):
        return f"Comment {self.author} on {self.post}"

class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE,related_name="Follower")
    following = models.ManyToManyField(User,blank =True,related_name="Following") 
   
    def __str__ (self):  
        return f" {self.id}: {self.follower} follows {self.following.all().values('id','username')}"