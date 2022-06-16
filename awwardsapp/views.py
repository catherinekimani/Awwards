from django.shortcuts import render,redirect
from django.http.response import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterForm,LoginForm,UserProfileForm,ProfileUpdateForm,PostProjectForm,RatingProjectForm
from .models import *
from django.contrib.auth.models import User
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
    Profile.objects.get_or_create(user=request.user)
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
@login_required(login_url='/login/') 
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
    if 'title' in request.GET and request.GET["title"]:
        search_term = request.GET["title"]
        searched_posts =Post.search_by_title(search_term)
        message = f"{search_term}"
        return render(request, 'search.html',{"message":message,"searched_posts": searched_posts})
    else:
        message = "You haven't searched for any term"
    return render(request, 'search.html',{"message":message})
def logout_user(request):
    logout (request)
    return redirect('login')

def rate(request, post_id):
    form = RatingProjectForm()
    current_user = request.user
    all_ratings = Rating.objects.filter(post=post_id).all()
    post = Post.objects.get(pk = post_id)
    ratings = Rating.objects.filter(user=request.user,post=post_id).first()
    rating_status = None
    if ratings is None:
        rating_status = False
    else:
        rating_status = True
    if request.method == 'POST':
        form = RatingProjectForm(request.POST)
        if form.is_valid():
            rate = form.save(commit=False)
            rate.user = request.user
            rate.post = post
            rate.save()
            post_ratings = Rating.objects.filter(post=post_id)
#calculating design
            design_rate = [design.design_rate for design in post_ratings]
            design_rating_average = sum(design_rate) / len(design_rate)
#calculating content
            content_rate = [content.content_rate for content in post_ratings]
            content_rating_average = sum(content_rate) / len(content_rate)
#calculating usability
            usability_rate = [usability.usability_rate for usability in post_ratings]
            usability_rating_average = sum(usability_rate) / len(usability_rate)
#calculating average
            average_rate = (design_rating_average + usability_rating_average + content_rating_average) / 3
            print(average_rate)
            rate.design_rating_average = round(design_rating_average, 2)
            rate.usability_rating_average = round(usability_rating_average, 2)
            rate.content_rating_average = round(content_rating_average, 2)
            rate.average_rate = round(average_rate, 2)
            rate.save()
            return HttpResponseRedirect(request.path_info)
    else:
        form = RatingProjectForm()
        return render(request, 'project_details.html', {'current_user':current_user,'all_ratings':all_ratings,'post':post,'form': form,'rating_status': rating_status})
def home(request):
    return render(request,'home.html')