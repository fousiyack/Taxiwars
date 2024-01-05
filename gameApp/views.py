from rest_framework.authtoken.models import Token
from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.response import Response
from .serializers import UserSerializer,GameSerializer
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
from .models import Game,UserProfile

@api_view(['POST'])
def create_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(['DELETE'])
def delete_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
def update_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['POST'])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
   
    user = authenticate(request,username=username, password=password)
    
    if user is not None:
        token, created = Token.objects.get_or_create(user=user)
        print(f'Token: {token.key}, User: {user.username}')
        return Response({'token': token.key}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)    
    
@api_view(['POST'])
def start_game(request):
    game = Game.objects.create()
    serializer = GameSerializer(game)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def get_board(request, game_id):
    try:
        game = Game.objects.get(id=game_id)
        serializer = GameSerializer(game)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Game.DoesNotExist:
        return Response({'error': 'Game not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def update_board(request, game_id):
    try:
        game = Game.objects.get(id=game_id)
        if len(game.board) < 6:
            character = request.data.get('character', '').lower()
            game.board += character
            game.is_palindrome = game.board == game.board[::-1] and len(game.board) == 6
            game.save()
            serializer = GameSerializer(game)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'error': 'Game board is already complete'}, status=status.HTTP_400_BAD_REQUEST)
    except Game.DoesNotExist:
        return Response({'error': 'Game not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def list_games(request):
    games = Game.objects.all()
    serializer = GameSerializer(games, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)    


    
    