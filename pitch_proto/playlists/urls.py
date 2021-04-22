from django.urls import path
from . import views

urlpatterns = [ 
    path('playlists/', views.playlists, name='playlists'),
    path('newplaylist/', views.newPlaylist, name='newplaylist'),
    path('playlists/<str:list>/', views.displayPlaylist, name='displayplaylist'),
    path('playlists/<str:list>/remove/<str:song>/', views.removeSong, name='removesong'),
    path('playlists/remove/<str:list>/', views.removePlaylist, name='removePlaylist'),
    path('playlists/copyNewPlaylist/<str:list>/<int:id>/', views.copyPlaylist, name='copyplaylist'),
    
]
