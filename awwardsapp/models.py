from django.db import models
from django.contrib.auth.models import User

from cloudinary.models import CloudinaryField

from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_profile = CloudinaryField('pictures')
    bio = models.TextField()
    contact = models.EmailField(max_length=100)
    
    def save_profile(self):
        self.save()
        
    def delete_profile(self):
        self.delete()
    
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
    
    @classmethod
    def search_by_title(cls, title):
        return cls.objects.filter(title__icontains=title).all()
    
    def save_post(self):
        self.save()

    def delete_post(self):
        self.delete()
    
    def __str__(self):
        return f'{self.description}'
    
    
class Rating(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    design_rate = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(10)],default=0)
    usability_rate = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(10)],default=0)
    content_rate = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(10)],default=0) 
    average_rate = models.IntegerField(default=0, blank=True, null=True,validators=[MinValueValidator(1),MaxValueValidator(10)])
    date_posted = models.DateTimeField(auto_now_add=True)
    
    def save_rating(self):
        self.save()

    def delete_rating(self):
        self.delete()
    
    def __str__(self):
        return f'{self.post}'