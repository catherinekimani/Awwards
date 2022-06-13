from dataclasses import fields
from rest_framework import serializers
from .models import Post,Profile

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
        
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'
        