from django.urls import path
from . import views

# app_name = 'recommender'

urlpatterns = [
    path('advanced-search/', views.searchform_get, name='advanced-search'),
    path('advanced-results/', views.searchform_post, name='advanced-results'),
    path('results/', views.results, name='results'),
    # path('album-info/', views.display_album, name='album-info'),
]
