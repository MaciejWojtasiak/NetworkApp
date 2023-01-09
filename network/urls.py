
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("add_post",views.add_post, name="add_post"),
    path("user/<int:id>",views.user, name="user"),
    path("like/<int:id>",views.like, name="like"),
    path("follow/<int:id>",views.follow, name="follow"),
    path("unfollow/<int:id>",views.unfollow, name="unfollow"),
    path("following/<int:id>",views.following, name="following"),
    path("edit/<int:post_id>",views.edit, name="edit")

]
