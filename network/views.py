from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import User, Post, Profile

from .forms import PostForm, Post


def index(request):
    return render(request, "network/index.html")


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

def new_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
        return render(request, "network/index.html")
    else:
        form = PostForm()
    return render(request, "network/new_post.html",{
        'form': form,
    })

def all_post(request):
    posts = Post.objects.all().order_by("-created")

    paginator = Paginator(posts, 10)
    page = request.GET.get('page')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
        
    return render(request, 'network/all_post.html', {
        'posts': posts,
    })

@login_required
def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    print('usuario --> ', request.user.id)
    # print('user ---> ', user)
    profile = user.profile
    # print('profile ---> ', profile)
    posts = Post.objects.filter(user=user).order_by('-created')
    # print('posts ---> ', posts)
    is_following = False

    if request.user.is_authenticated:
        is_following = request.user in profile.followers.all()

    context = {
        'profile_user': user,
        'profile': profile,
        'posts': posts,
        'is_following': is_following,
    }

    return render(request, 'network/profile.html', context)

@login_required
def toggle_follow(request, username):
    usuario_iniciado = get_object_or_404(User, username=request.user)
    perfil_seguidor = usuario_iniciado.profile
    
    usuario_a_seguir = get_object_or_404(User, username=username)
    perfil_a_seguir = usuario_a_seguir.profile

    if request.user in perfil_seguidor.followers.all():
        perfil_seguidor.followers.remove(User.objects.filter(username=username).first().pk)
    else:
        perfil_seguidor.followers.add(User.objects.filter(username=username).first().pk)

    return redirect('profile_view', username=username)

@login_required
def following_posts(request):
    profile = request.user.profile
    following_users = profile.followers.all()
    posts = []
    for follow in following_users:
        print("Follow --> ", follow)
        id = User.objects.filter(username=follow).first()
        user_post = Post.objects.filter(user_id=id).order_by('-created')
        posts.extend(user_post)
        # print('id --> ', id.pk)
        # posts.append(Post.objects.filter(user_id=id).all())
        # Post.objects.filter(user_id=3).order_by('-created')
    print('post --> ', posts)
    paginator = Paginator(posts, 1)
    page = request.GET.get('page')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    
    return render(request, 'network/following.html', {
        'posts': posts
    })

def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.user != request.user:
        return JsonResponse({
            'error': 'Usted no tiene un usuario registrado',
        }, status=403)
    
    content = request.POST.get('content', '')
    if content:
        post.content = content
        post.save()
        return JsonResponse({
            'sucess': 'Post actualizado correctamente :D'
        })
    else:
        return JsonResponse({
            'error': 'Este post no existe D:'
        })
