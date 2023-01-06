from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator

from .models import User, Post, Like


def get_liked_posts(posts,user):
    liked_posts = []
    for post in posts:
        for p in post.LikedPost.all():
            for user in p.user.all():
                if(user == user):
                    liked_posts.append(post)
    return liked_posts


def index(request):
    posts = Post.objects.all().order_by('-date')
    liked_posts = get_liked_posts(posts,request.user)
    
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    posts_of_the_page = paginator.get_page(page_number)


    return render(request, "network/index.html", {
        "posts": posts, 
        "liked_posts": liked_posts,
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
    if(User.objects.get(pk=id)):
        user = User.objects.get(pk=id)        
        try:
            posts = Post.objects.filter(author = user)     
        except Post.DoesNotExist:
            posts = None

        return render(request, "network/user.html", {
            "user":user,
            "posts":posts
        })
    else:
        print('no user')

    return index(request)

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