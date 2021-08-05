from rest_framework import serializers
from django.contrib.auth.models import User


from .models import Post, Vote


class PostSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='created_by.username', read_only=True)

    class Meta:
        model = Post
        fields = '__all__'
        extra_kwargs = {'created_by': {'default': serializers.CurrentUserDefault()}}
        
class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
