from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json

from .models import User, Post, Like, Follow


def index(request):
    posts = Post.objects.all().order_by('-date')    
    
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    posts_of_the_page = paginator.get_page(page_number)    

    return render(request, "network/index.html", {
        "posts": posts,         
        "posts_of_the_page":posts_of_the_page
        })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def add_post(request):
    if request.method == "POST":                
        newPost = Post.objects.create(text=request.POST["post"],author=request.user)
        newPost.save()
       
        return HttpResponseRedirect(reverse("index"))
    
    return HttpResponse("Error: This page only accept POST requests.")
   
def user(request,id):  
   
        user = User.objects.get(pk=id)        
        posts = Post.objects.filter(author = user)   
        
        following = Follow.objects.filter(user=user)
        followers = Follow.objects.filter(user_follower=user)  
          
        #paginator
        paginator = Paginator(posts, 5)
        page_number = request.GET.get('page')
        posts_of_the_page = paginator.get_page(page_number)  

        try:
            checkFollow = followers.filter(user = User.objects.get(pk = request.user.id))                     
            if len(checkFollow) != 0:
                isFollowing = False
            else:
                isFollowing = True            
        except:
            isFollowing = False
       
        return render(request, "network/user.html", {
            "username":user.username,
            "posts":posts_of_the_page,
            "following":following,
            "followers":followers,
            "user_profile": user,
            "isFollowing":isFollowing
        })    

def like(request, id):
    # if request.method == "POST":        
    #     post = Post.objects.get(pk = id)    
    #     like = Like.objects.create(post=post,user=user)
    #     post.likesNumber = post.likesNumber + 1
    #     post.save()
    #     like.save()
        
    #     return HttpResponseRedirect(reverse("index")) 
    # else: 
    #     return index(request)
    pass

def follow(request, id):
    if request.method == "POST":
        if(id != request.user.id):
            user_to_follow = User.objects.get(pk = id)
            follow = Follow.objects.create(user = request.user, user_follower = user_to_follow)
            follow.save()

        return HttpResponseRedirect(reverse("index"))

    return HttpResponse("Error: This page only accept POST requests.")

def unfollow(request, id):
    if request.method == "POST":
        user_to_unfollow = User.objects.get(pk = id)
        Follow.objects.filter(user = request.user, user_follower = user_to_unfollow).delete()

        return HttpResponseRedirect(reverse("index"))

    return HttpResponse("Error: This page only accept POST requests.")

@csrf_exempt
@login_required
def edit(request,post_id):
    
    # Composing a edit must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    data = json.loads(request.body)
    post = Post.objects.get(pk = post_id)
    post.text = data
    post.save()    

    return JsonResponse({"message": "Post edited successfully."}, status=201)