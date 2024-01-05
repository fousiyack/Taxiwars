from django.db import models
from django.contrib.auth.models import User

class Game(models.Model):
    board = models.CharField(max_length=50, default='')
    is_palindrome = models.BooleanField(default=False)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    games_played = models.ManyToManyField(Game)