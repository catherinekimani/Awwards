from django.test import TestCase
from .models import *
# Create your tests here.
class ProfileTest(TestCase):
    def setUp(self):
        self.user = User(username='moringa',email="moringa@gmail.com", password='kate')
        self.user.save()

    def test_instance(self):
        self.assertTrue(isinstance(self.user, User))

    def test_save_user(self):
        self.user.save()

    def test_delete_user(self):
        self.user.delete()
        
class PostTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='moringa',email="moringa@gmail.com")
        self.post = Post.objects.create(title='Personal Blog', image='img.png', description='project test', user=self.user, url="https://github.com/catherinekimani/personal-blog")
    def test_instance(self):
        self.assertTrue(isinstance(self.post, Post))
        
    def test_save_post(self):
        self.post.save()
        
    def test_delete_post(self):
        self.post.save()
        
class RatingTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='moringa',email="moringa@gmail.com")
        self.post = Post.objects.create(title='Personal Blog', image='img.png', description='project test', user=self.user, url="https://github.com/catherinekimani/personal-blog")
        self.rating = Rating.objects.create(design_rate=4,usability_rate=7,content_rate=2,user=self.user,post=self.post,date_posted=2022-6-15)
    def test_instance(self):
        self.assertTrue(isinstance(self.rating, Rating))
        
    def test_save_rate(self):
        self.post.save()
        
    def test_delete_rate(self):
        self.post.save()
        