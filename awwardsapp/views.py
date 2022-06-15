from django.shortcuts import render,redirect

from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterForm,LoginForm,UserProfileForm,ProfileUpdateForm,PostProjectForm,RatingProjectForm
from .models import *

from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializer import ProjectSerializer,ProfileSerializer
from awwardsapp import serializer
from .permissions import IsAdminOrReadOnly

# Create your views here.
@login_required(login_url='/login/')
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

@login_required(login_url='/login/')
def profile(request):
    current_user = request.user
    profile = Profile.objects.filter(user_id=current_user.id).first()
    post = Post.objects.filter(user_id=current_user.id).all() 
    return render(request,'profile/profile.html',{"profile":profile,'post':post})

@login_required(login_url='/login/')
def edit_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST,instance=request.user)
        form = ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)
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

class ProjectList(APIView):
    permission_classes=(IsAdminOrReadOnly, )
    def get(self,request, format=None):
        all_projects = Post.objects.all()
        serializers = ProjectSerializer(all_projects, many=True)
        return Response(serializers.data)
    
    def post(self,request,format=None):
        serializers = ProjectSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data,status=status.HTTP_201_CREATED)
        return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)
    
class ProfileList(APIView):
    permission_classes=(IsAdminOrReadOnly, )
    def get(self,request, format=None):
        all_projects = Profile.objects.all()
        serializers = ProfileSerializer(all_projects, many=True)
        return Response(serializers.data)
    
    def post(self,request,format=None):
        serializers = ProjectSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data,status=status.HTTP_201_CREATED)
        return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)
    
def search_results(request):
    if 'title' in request.GET and request.GET['title']:
        search_term = request.GET['title'].lower()
        posts = Post.search_by_title(search_term)
        message = f'{search_term}'

        return render(request, 'search.html', {'found': message, 'posts': posts})
    else:
        message = 'Not found'
        return render(request, 'search.html', {'danger': message})

def logout_user(request):
    logout (request)
    return redirect('login')

def rate(request,post_id):
    form = RatingProjectForm()
    if request.method == 'POST':
        post = Post.objects.get(id = post_id)
        current_user= request.user
        design_rate = request.POST['design_rate']
        content_rate = request.POST['content_rate']
        usability_rate = request.POST['usability_rate']
        return render(request,"project_details.html",{"post":post,'userbility':usability_rate,'design':design_rate,'usability':content_rate,'user':current_user,'form':form})
    else:
        post = Post.objects.get(id = post_id) 
        return render(request,"project_details.html",{"post":post,'form':form})