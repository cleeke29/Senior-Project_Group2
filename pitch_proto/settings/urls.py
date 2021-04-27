from django.urls import path
from . import views

urlpatterns = [
    path('settingsForm/', views.settingsPage, name='settingsForm'),
    path('settingsResetRec/', views.settingsReset, name = 'resetRec'),
    path('settingsToggleDark/', views.toggleDark, name = 'darkMode'),
    path('settingsChangeUsername/', views.changeUsername, name = 'changeUsername')
]
 
