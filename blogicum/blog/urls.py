# blog/urls.py - ПРАВИЛЬНО
from django.urls import path

from . import views

app_name = "blog"

urlpatterns = [
    path("profile/edit/", views.edit_profile, name="edit_profile"),
    path(
        "posts/<int:pk>/delete_comment/<int:comment_id>/",
        views.delete_comment,
        name="delete_comment",
    ),
    path(
        "posts/<int:pk>/delete_comment/<int:comment_id>/",
        views.delete_comment,
        name="delete_comment",
    ),
    path("posts/<int:pk>/edit/", views.edit_post, name="edit_post"),
    path(
        "posts/<int:pk>/edit_comment/<int:comment_id>/",
        views.edit_comment,
        name="edit_comment",
    ),
    path("posts/<int:pk>/delete/", views.delete_post, name="delete_post"),
    path("profile/<str:username>/", views.profile, name="profile"),
    path("posts/create/", views.create_post, name="create_post"),
    path("", views.index, name="index"),
    path("posts/<int:pk>/", views.post_detail, name="post_detail"),
    # <int:pk> а не <int:id>
    path(
        "category/<slug:category_slug>/",
        views.category_posts,
        name="category_posts",
    ),
]
