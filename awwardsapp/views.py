from django.shortcuts import render,redirect

from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterForm,LoginForm,UserProfileForm,ProfileUpdateForm,PostProjectForm
from .models import *

from django.contrib.auth import login,logout,authenticate
# Create your views here.
def index(request):
    post = Post.objects.all()
    all = Profile.objects.all()
    return render(request,'index.html',{"all":all,'post':post})

def register(request):
    form = RegisterForm()
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    return render(request,'register.html',{'form':form})

def login_user(request):
    form = LoginForm()
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password1')
        
        user = authenticate(request, username = username, password = password)
        
        if user is not None:
            login(request,user)
            return redirect('index')
    return render(request, 'login.html',{'form':form})

def profile(request):
    
    return render(request,'profile/profile.html')
    
def edit_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST,instance=request.user)
        form = ProfileUpdateForm(request.POST,request.FILES,instance = request.user.profile)
        if form.is_valid() and form.is_valid():
            form.save()
            form.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)
        form = ProfileUpdateForm(instance=request.user.profile)
    return render(request,'profile/edit-profile.html', {'form':form})

def project(request):
    current_user = request.user
    if request.method == 'POST':
        form = PostProjectForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = current_user
            post.save()
        return redirect('index')

    else:
        form = PostProjectForm()
    return render(request,'project.html',{"user":current_user,"form":form})
