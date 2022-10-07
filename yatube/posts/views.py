from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required


from .models import Group, Post, User
from .forms import PostForm


def get_page_context(queryset, request):
    paginator = Paginator(queryset, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj


def index(request):
    post_list = Post.objects.all().order_by('-pub_date')
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group: str = get_object_or_404(Group, slug=slug)
    post_list = Post.objects.all().order_by('-pub_date')
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context: dict = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    page_obj = get_page_context(Post.objects.filter(author=author), request)
    context = {
        'author': author,
        'page_obj': page_obj,
    }
    return render(request, 'posts/profile.html', context)


# @login_required
def post_detail(request, post_id):
    template = 'posts/post_detail.html'
    post_info = get_object_or_404(Post, pk=post_id)
    post_author = post_info.author.posts.count()
    context = {
        'post_info': post_info,
        'post_author': post_author,
    }
    return render(request, template, context)


@login_required
def post_create(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        post_create = form.save(commit=False)
        post_create.author = request.user
        post_create.save()
        return redirect('posts:profile', post_create.author)
    context = {'form': form}
    return render(request, 'posts/create_post.html', context)


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user != post.author:
        return redirect('posts:post_detail', post_id)
    else:
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
