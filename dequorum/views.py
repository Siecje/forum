from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import Category, Forum, Thread
from .forms import CreateProfileForm, LoginForm, CreateThreadForm, CreatePostForm


def index(request):
    categories = Category.objects.all()
    return render(request, 'dequorum/index.html', {'categories': categories})


def register(request):
    form = CreateProfileForm()
    if request.method == 'POST':
        form = CreateProfileForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect(reverse('forum_index'))
    return render(request, 'dequorum/register.html', {'form': form})


def login(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect(reverse('forum_index'))
    return render(request, 'dequorum/login.html', {'form': form})


def profile(request):
    return render(request, 'dequorum/profile.html')


def view_category(request, category_id):
    try:
        category = Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        return render(request, 'dequorum/error.html', {'error_title': 'Category Does Not Exist'})

    forums = category.forums.all()
    return render(request, 'dequorum/view_category.html', {'category': category, 'forums': forums})


def view_forum(request, forum_id):
    try:
        forum = Forum.objects.get(id=forum_id)
    except Forum.DoesNotExist:
        return render(request, 'dequorum/error.html', {'error_title': 'Forum Does Not Exist'})

    threads = forum.threads.all()

    return render(request, 'dequorum/view_forum.html',
        {'forum': forum, 'threads': threads})

#TODO: require login
def create_thread(request, forum_id):
    try:
        forum = Forum.objects.get(id=forum_id)
    except Forum.DoesNotExist:
        return render(request, 'dequorum/error.html',
            {'error_title': 'Forum Not Found', 'error_message': 'Cannot create Thread since the Forum cannot be found'})

    thread_form = CreateThreadForm()
    post_form = CreatePostForm()
    if request.method == 'POST':
        thread_form = CreateThreadForm(request.POST)
        post_form = CreatePostForm(request.POST)
        if thread_form.is_valid() and post_form.is_valid():
            new_thread = thread_form.save(commit=False)
            new_thread.forum = forum
            new_thread.save()
            new_post = post_form.save(commit=False)
            new_post.subject = new_thread.subject
            new_post.thread = new_thread
            new_post.author = request.user
            new_post.save()
            return HttpResponseRedirect(reverse('view_thread', args=(new_thread.id,)))
    return render(request, 'dequorum/create_thread.html',
        {'thread_form': thread_form, 'post_form': post_form})


def view_thread(request, forum_id, thread_id):
    try:
        forum = Forum.objects.get(id=forum_id)
    except Forum.DoesNotExist:
        return render(request, 'dequorum/error.html',
            {'error_title': 'Thread Not Found'})

    try:
        thread = Thread.objects.get(id=thread_id)
    except Thread.DoesNotExist:
        return render(request, 'dequorum/error.html',
            {'error_title': 'Thread Not Found'})

    posts = thread.posts.all()

    return render(request, 'dequorum/view_thread.html', {'forum': forum, 'thread': thread, 'posts': posts})
