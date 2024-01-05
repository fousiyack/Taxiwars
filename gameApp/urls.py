from django.urls import path
from .views import *
urlpatterns = [
    path('create_user/', create_user, name='create_user'),
    path('delete_user/<int:user_id>/', delete_user, name='delete_user'),
    path('update_user/<int:user_id>/', update_user, name='update_user'),
    path('login/', login_user, name='login_user'),
    path('start_game/', start_game, name='start_game'),
    path('get_board/<int:game_id>/', get_board, name='get_board'),
    path('update_board/<int:game_id>/', update_board, name='update_board'),
    path('list_games/', list_games, name='list_games'),
]