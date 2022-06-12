from django.db import models
from django.contrib.auth.models import User

from cloudinary.models import CloudinaryField

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_profile = CloudinaryField('pictures')
    bio = models.TextField()
    contact = models.EmailField(max_length=100)
    
    def __str__(self):
        return f'{self.user.username} Profile'
    
class Post(models.Model):
    image = CloudinaryField('image')
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=400)
    url = models.URLField(max_length=200)
    date_posted = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    technologies = models.CharField(max_length=200)
    
    def __str__(self):
        return f'{self.description}'