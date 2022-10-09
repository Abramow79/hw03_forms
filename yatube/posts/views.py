from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required


from .forms import PostForm
from .models import Group, Post, User


def get_page_context(queryset, request):
    return Paginator(queryset, 10).get_page(request.GET.get('page'))


def index(request):
    post_list = Post.objects.all()
    page_obj = get_page_context(post_list, request)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group: str = get_object_or_404(Group, slug=slug)
    post_list = Post.objects.all()
    page_obj = get_page_context(post_list, request)

    context: dict = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    page_obj = get_page_context(author.posts.all(), request)
    context = {
        'author': author,
        'page_obj': page_obj,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    related = Post.objects.select_related('author', 'group')
    post = get_object_or_404(related, pk=post_id)
    context = {
        'post': post,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    form = PostForm(request.POST or None)
    if not form.is_valid():
        context = {'form': form}
        return render(request, 'posts/create_post.html', context)
    post = form.save(commit=False)
    post.author = request.user
    post.save()
    return redirect('posts:profile', username=post.author)


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user != post.author:
        return redirect('posts:post_detail', post_id)
    form = PostForm(request.POST or None, instance=post or None)
    if form.is_valid():
        form.save()
        return redirect('posts:post_detail', post_id)
    context = {
        'form': form,
        'is_edit': True,
        'post_id': post_id,
    }
    return render(request, 'posts/create_post.html', context)
