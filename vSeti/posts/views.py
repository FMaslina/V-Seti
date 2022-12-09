from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from .forms import NewPostForm
from .models import Post, Group, User


def index(request):
    post_list = Post.objects.order_by('-pub_date').all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        'index.html',
        {"page": page, "paginator": paginator}
    )


def group_post(request, slug):
    group = get_object_or_404(Group, slug=slug)
    group_post_list = Post.objects.filter(group=group).order_by('-pub_date').all()
    paginator = Paginator(group_post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request,
                  "group.html",
                  {"group": group, "paginator": paginator, "page": page})


@login_required
def new_post(request):
    if request.method == "POST":
        form = NewPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('index')
        return render(request, 'new_post.html', {"form": form})
    form = NewPostForm()
    return render(request, 'new_post.html', {"form": form})


@login_required
def profile(request, username):
    user = get_object_or_404(User, username=username)
    post_list = Post.objects.order_by('-pub_date').filter(author=user).all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'profile.html', {"user": user, "page": page, "paginator": paginator})


def post_view(request, username, post_id):
    post = get_object_or_404(Post, id=post_id)
    username = get_object_or_404(User, username=username)
    return render(request, 'post.html', {"post": post, "username": username})


def post_edit(request, username, post_id):
    post = get_object_or_404(Post, id=post_id)
    username = get_object_or_404(User, username=username)
    is_edit = True
    if post.author != request.user:
        return redirect(
            'post', post.author.username, post.id
        )
    if request.method == "POST":
        form = NewPostForm(request.POST, instance=post)
        if form.is_valid():
            post.save()
            return redirect('index')
        return render(request, 'new_post.html', {"form": form, "post": post, "username": username, "is_edit": is_edit})
    form = NewPostForm(instance=post)
    return render(request, 'new_post.html', {"form": form, "post": post, "username": username, "is_edit": is_edit})


def post_delete(request, post_id, username):
    post = get_object_or_404(Post, id=post_id)
    user = get_object_or_404(User, username=username)
    post_list = Post.objects.order_by('-pub_date').filter(author=user).all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    if request.method == "POST":
        post.delete()
        return render(request, 'profile.html', {"post": post, "user": user, "page": page, "paginator": paginator})
    return render(request, 'profile.html', {"post": post, "user": user, "page": page, "paginator": paginator})


def page_not_found(request, exception):
    # Переменная exception содержит отладочную информацию,
    # выводить её в шаблон пользователской страницы 404 мы не станем
    return render(
        request,
        "misc/404.html",
        {"path": request.path},
        status=404
    )


def server_error(request):
    return render(request, "misc/500.html", status=500)