from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    
    path('register/',views.register,name='register'),
    path('login/', views.login_user,name='login'),
    
    path('profile/',views.profile,name='profile'),
    path('edit-profile',views.edit_profile,name='edit-profile')
]