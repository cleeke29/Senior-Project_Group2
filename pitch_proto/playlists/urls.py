from django.urls import path
from . import views

urlpatterns = [ 
    path('playlists/', views.playlists, name='playlists'),
    path('newplaylists/', views.newPlaylist, name='newPlaylist'),
    
]