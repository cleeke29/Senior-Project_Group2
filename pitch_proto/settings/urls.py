from django.urls import path
from . import views

urlpatterns = [
    path('settingsForm/', views.settingsPage, name='settingsForm'),
    path('settingsUpdate/', views.settingsUpdate, name = 'settingsUpdate')
]
 