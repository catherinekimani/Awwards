from django.shortcuts import render,redirect

from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterForm
# Create your views here.
def index(request):
    return render(request,'index.html')

def register(request):
    form = RegisterForm()
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    return render(request,'register.html',{'form':form})