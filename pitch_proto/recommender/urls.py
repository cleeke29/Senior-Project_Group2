from django.urls import path
from . import views

# app_name = 'recommender'

urlpatterns = [
    path('advanced-search/', views.searchform_get, name='advanced-search'),
    path('advanced-results/', views.searchform_post, name='advanced-results'),
    path('results/', views.results, name='results'),
    path('search/<str:song_name>/', views.searchSong, name="search_song"),
    path('Song_info/<str:track>/', views.Song_info, name='Song_info'),
    path('Album_info/<str:album>/', views.Album_info, name='Album_info'),
    path('song_discuss/<str:track>/', views.discuss, name='discuss'),
    path('start_discuss/<str:track>/', views.startDiscuss, name='startDiscuss'),
    # path('album-info/', views.display_album, name='album-info'),
]
