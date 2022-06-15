from django.urls import path
from . import views

urlpatterns = [
    path('index',views.index,name='index'),
    path('',views.home,name='home'),
    path('register/',views.register,name='register'),
    path('login/', views.login_user,name='login'),
    path('logout/',views.logout_user,name='logout'),
    
    path('profile/',views.profile,name='profile'),
    path('edit-profile',views.edit_profile,name='edit-profile'),
    
    path('project',views.project,name='project'),
    path('api/post/',views.ProjectList.as_view(),name=''),
    path('api/profile/',views.ProfileList.as_view(),name=''),
    
    path('search/', views.search_results, name='search_results'),
    path("rate/<post_id>/",views.rate, name='rate'),
]