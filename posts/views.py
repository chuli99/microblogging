from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from .forms import PostForm
from .models import Post

# Create your views here.


def home(request):
    return render(request, 'home.html')


def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm
        })
    else:
        print(request.POST)
        if request.POST['password1'] == request.POST['password2']:
            try:
                # Guardar Usuario con un modelo Django si las password coinciden
                user = User.objects.create_user(
                    username=request.POST['username'],
                    password=request.POST['password1']
                )
                user.save()
                login(request, user)
                return redirect('posts')
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': 'User already exists'
                })
        return render(request, 'signup.html', {
            'form': UserCreationForm,
            'error': 'Las contraseñas no coinciden'
        })
def signout(request):
    logout(request)
    return redirect('home')

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html',{
            'form': AuthenticationForm()
        })
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html',{
                'form': AuthenticationForm(),
                'error': 'User or password incorrect'
        })
        else:
            login(request, user)
            return redirect('home')
    
        

def posts(request):
    posts = Post.objects.all().order_by('-created_at')  # El signo '-' indica orden descendente
    return render(request, 'posts.html',{'posts':posts})

def post_detail(request, post_id):
    post = get_object_or_404(Post,pk=post_id)
    return render(request, 'post_detail.html',{'post':post})

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post,pk=post_id, user=request.user)
    if request.method == 'POST':
        post.delete()
        return redirect('posts')

@login_required
def create_post(request):
    if request.method == 'GET':
        return render(request, 'create_post.html',{
            'form': PostForm
        })
    else:
        try:
            form = PostForm(request.POST)
            new_post = form.save(commit=False)
            new_post.user = request.user
            new_post.save()
            return redirect('posts')
        except ValueError:
            return render(request,'create_post.html',{
                'form': PostForm(),
                'error': 'Por favor ingrese solo datos validos'
            })
