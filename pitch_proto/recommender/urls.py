from django.urls import path
from . import views

# app_name = 'recommender'

urlpatterns = [
    path('advanced-search/', views.searchform_get, name='advanced-search'),
    path('advanced-results/', views.searchform_post, name='advanced-results'),
]
