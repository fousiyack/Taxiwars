from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Game,UserProfile


class UserSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True)
    class Meta:
        model=User
        fields=('id','username','password')
        
        
    def create(self,validated_data):
        user=User.objects.create_user(**validated_data)    
        password = validated_data.pop('password', None)
        if password:
            user.set_password(password)
        user.save()
        return user
class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ('id', 'board', 'is_palindrome')

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('id', 'user', 'games_played')    
    
        
        