from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from .forms import NewPostForm
from .models import Post, Group


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

    return render(request, 'profile.html', {})