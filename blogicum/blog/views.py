# blogicum/blog/views.py

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView

from .forms import CommentForm, PostForm
from .models import Category, Comment, Post

User = get_user_model()


class RegistrationView(CreateView):
    form_class = UserCreationForm
    template_name = "registration/registration_form.html"
    success_url = reverse_lazy("login")


@login_required
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("blog:profile", username=request.user.username)
    else:
        form = PostForm()

    return render(request, "blog/create.html", {"form": form})


def profile(request, username):
    profile_user = get_object_or_404(User, username=username)

    qs = Post.objects.select_related("category", "location", "author").filter(
        author=profile_user
    )

    # Чужим показываем только опубликованное
    if request.user != profile_user:
        qs = qs.filter(
            is_published=True,
            category__is_published=True,
            pub_date__lte=timezone.now(),
        )

    qs = qs.order_by("-pub_date")

    paginator = Paginator(qs, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {"profile_user": profile_user, "page_obj": page_obj}
    return render(request, "blog/profile.html", context)


def index(request):
    qs = (
        Post.objects.select_related("category", "location", "author")
        .filter(
            is_published=True,
            category__is_published=True,
            pub_date__lte=timezone.now(),
        )
        .order_by("-pub_date")
    )

    paginator = Paginator(qs, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "blog/index.html", {"page_obj": page_obj})


def post_detail(request, pk):
    post = get_object_or_404(
        Post.objects.select_related("category", "location", "author"),
        pk=pk,
    )

    # Чужим нельзя видеть неопубликованное/будущее/категория скрыта
    if request.user != post.author:
        if (
            not post.is_published
            or not post.category.is_published
            or post.pub_date > timezone.now()
        ):
            raise Http404

    comments = post.comments.select_related("author").all()
    form = CommentForm()

    if request.method == "POST":
        # Анонимов — на логин
        if not request.user.is_authenticated:
            return redirect("login")

        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect("blog:post_detail", pk=pk)

    context = {"post": post, "comments": comments, "form": form}
    return render(request, "blog/detail.html", context)


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category, slug=category_slug, is_published=True)

    qs = (
        Post.objects.select_related("category", "location", "author")
        .filter(
            category=category,
            is_published=True,
            pub_date__lte=timezone.now(),
        )
        .order_by("-pub_date")
    )

    paginator = Paginator(qs, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {"category": category, "page_obj": page_obj}
    return render(request, "blog/category.html", context)


@login_required
def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if post.author != request.user:
        return redirect("blog:post_detail", pk=pk)

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect("blog:post_detail", pk=post.pk)
    else:
        form = PostForm(instance=post)

    return render(request, "blog/create.html", {"form": form, "post": post})


@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if post.author != request.user:
        return redirect("blog:post_detail", pk=pk)

    if request.method == "POST":
        post.delete()
        return redirect("blog:profile", username=request.user.username)

    return render(request, "blog/create.html", {"form": None, "post": post})


@login_required
def edit_comment(request, pk, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id, post__pk=pk)

    if comment.author != request.user:
        return redirect("blog:post_detail", pk=pk)

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect("blog:post_detail", pk=pk)
    else:
        form = CommentForm(instance=comment)

    return render(request, "blog/comment.html",
                  {"form": form, "comment": comment})


@login_required
def delete_comment(request, pk, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id, post__pk=pk)

    if comment.author != request.user:
        return redirect("blog:post_detail", pk=pk)

    if request.method == "POST":
        comment.delete()
        return redirect("blog:post_detail", pk=pk)

    # GET: страница подтверждения удаления (200), без "form" в контексте
    return render(request, "blog/comment_delete.html", {"comment": comment})


@login_required
def edit_profile(request):
    form = UserChangeForm(request.POST or None, instance=request.user)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("blog:profile", username=request.user.username)
    return render(request, "blog/edit_profile.html", {"form": form})
